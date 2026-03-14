"""
backend/scraper/pipeline/groq_extractor.py
--------------------------------------------
NEW FILE — Add this to your scraper/pipeline/ folder.

Uses Groq's FREE API (Llama 3.3 70B) to extract structured AI tool
data from any page text or markdown.

Replaces BeautifulSoup tag-hunting entirely.
Works on any site layout — no selectors needed.

Free limits (Groq):
  - 14,400 requests/day
  - No credit card needed
  - Get key: https://console.groq.com
"""

import os
import json
import time
import urllib.request

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
MODEL        = "llama-3.3-70b-versatile"
CHUNK_SIZE   = 3500   # chars per request — safe under token limit
OVERLAP      = 200    # overlap between chunks so no tools are missed at edges
DELAY        = 1.5    # seconds between requests — stays under rate limit

# Your 14 Supabase categories (must match exactly what's in your DB)
VALID_CATEGORIES = [
    "AI Assistant",
    "Image Generation",
    "Video Generation",
    "Development & Code",
    "Writing & Content",
    "Research",
    "Design & Creativity",
    "Audio & Voice",
    "Productivity",
    "Marketing & Social",
    "Learning & Resources",
    "Customer Support & Chat",
    "Document & PDF",
    "Career & HR",
    "Other",
]

SYSTEM_PROMPT = f"""You extract AI tools from text and return structured JSON.

Return ONLY a raw JSON array — no explanation, no markdown, no code blocks.

Each object must have exactly these keys:
- "name": tool name (string)
- "description": 1-2 sentences about what the tool does (string)
- "category": MUST be exactly one of: {json.dumps(VALID_CATEGORIES)}
- "website": tool URL (string, empty string "" if not found)

Rules:
- Skip navigation links, section headings, table of contents, "back to top" links
- Skip anything that is not a real usable software tool
- Write a short description if one is missing
- Never duplicate the same tool name
- Return [] if no tools found
"""

# ── Lazy Groq client ──────────────────────────────────────────────────────────
_groq_client = None

def _get_client():
    global _groq_client
    if _groq_client is None:
        if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
            raise ValueError(
                "\nGROQ_API_KEY not set.\n"
                "Get a free key at https://console.groq.com\n"
                "Then add GROQ_API_KEY=your_key to your backend/.env file.\n"
            )
        _groq_client = Groq(api_key=GROQ_API_KEY)
    return _groq_client


def _call_groq(text_chunk: str, source: str) -> list:
    """Send one text chunk to Groq. Returns list of tool dicts. Never raises."""
    client = _get_client()

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Extract AI tools (source: {source}):\n\n{text_chunk}"},
            ],
            temperature=0.1,
            max_tokens=2048,
        )

        raw = resp.choices[0].message.content.strip()

        # Strip markdown fences the model sometimes adds despite instructions
        if "```" in raw:
            parts = raw.split("```")
            raw = parts[1] if len(parts) > 1 else parts[0]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        parsed = json.loads(raw)
        if not isinstance(parsed, list):
            return []

        results = []
        for item in parsed:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name", "")).strip()
            if not name or len(name) < 3:
                continue
            category = str(item.get("category", "Other")).strip()
            if category not in VALID_CATEGORIES:
                category = "Other"
            results.append({
                "name":        name,
                "description": str(item.get("description", "")).strip(),
                "category":    category,
                "website":     str(item.get("website", "")).strip(),
            })
        return results

    except json.JSONDecodeError:
        return []  # Malformed JSON — skip chunk silently

    except Exception as e:
        err = str(e).lower()
        if "rate" in err or "429" in err:
            print(f"    [Rate limit] Waiting 15s before retry...")
            time.sleep(15)
            try:
                return _call_groq(text_chunk, source)
            except Exception:
                return []
        print(f"    [Groq warn] {source}: {e}")
        return []


def extract_tools_with_ai(text: str, source_hint: str = "unknown") -> list:
    """
    Main extraction function.
    Takes any raw page text / markdown, returns deduplicated tool list.

    Args:
        text:        Raw text from Playwright inner_text() or Jina markdown
        source_hint: Label used in logs (usually the URL being scraped)

    Returns:
        List of dicts: [{"name", "description", "category", "website"}, ...]
    """
    if not text or len(text.strip()) < 50:
        return []

    # Split into overlapping chunks
    chunks = []
    start  = 0
    while start < len(text):
        chunks.append(text[start: start + CHUNK_SIZE])
        start += CHUNK_SIZE - OVERLAP

    all_tools  = []
    seen_names = set()

    print(f"    Extracting via AI: {source_hint} ({len(chunks)} chunk{'s' if len(chunks) != 1 else ''})")

    for i, chunk in enumerate(chunks):
        tools = _call_groq(chunk, source_hint)
        for tool in tools:
            key = tool["name"].lower().strip()
            if key not in seen_names:
                seen_names.add(key)
                all_tools.append(tool)
        if i < len(chunks) - 1:
            time.sleep(DELAY)

    print(f"    → {len(all_tools)} tools extracted")
    return all_tools


def fetch_markdown_via_jina(url: str) -> str:
    """
    Converts any URL → clean markdown using Jina Reader.
    Completely free, no API key needed.
    Best for GitHub READMEs and static pages.

    Args:
        url: Any webpage URL

    Returns:
        Markdown string, or empty string on failure
    """
    jina_url = f"https://r.jina.ai/{url}"
    try:
        req = urllib.request.Request(
            jina_url,
            headers={"Accept": "text/plain", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
        print(f"    Jina: {url} → {len(content):,} chars")
        return content
    except Exception as e:
        print(f"    [Jina warn] {url}: {e}")
        return ""