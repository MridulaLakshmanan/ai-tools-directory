"""
backend/scraper/pipeline/groq_extractor.py
--------------------------------------------
REPLACE your existing groq_extractor.py

Key changes in this version:
  1. NO truncation — all pages fully processed regardless of size
  2. Smart rate limiting — calculates pause based on chunk size
     so large repos (100+ chunks) process completely without hitting limits
  3. Exponential backoff on rate limit errors (15s → 30s → 60s)
  4. "AI Assistants" matches DB category exactly
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
CHUNK_SIZE   = 3000    # chars per request (~750 tokens input — leaves room for output)
OVERLAP      = 200     # overlap between chunks so no tools are missed at edges

# Groq free tier: 6000 tokens/minute
# Each chunk ≈ 750 input + ~500 output = ~1250 tokens
# So max safe rate = 6000 / 1250 = ~4.8 requests/min = ~12.5s between requests
# We use 13s to be safely under the limit with no rate limit errors at all
DELAY_BETWEEN_CHUNKS = 13.0

# !! Must match your Supabase DB categories EXACTLY (case-sensitive) !!
VALID_CATEGORIES = [
    "AI Assistants",           # with 's' — matches your DB
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
- "website": tool URL (string, use empty string "" if not found)

Rules:
- Skip navigation links, section headings, table of contents, "back to top" links
- Skip anything that is not a real usable software tool
- Write a short description if one is missing
- Never include the same tool name twice
- Return [] if no tools found
"""

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


def _call_groq(text_chunk: str, source: str, retry: int = 0) -> list:
    """
    Send one text chunk to Groq. Returns list of tool dicts. Never raises.
    Uses exponential backoff on rate limits: 15s → 30s → 60s, max 3 retries.
    """
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
            if retry >= 3:
                print(f"    [Rate limit] Max retries hit — skipping chunk from {source}")
                return []
            # Exponential backoff: 15s, 30s, 60s
            wait = 15 * (2 ** retry)
            print(f"    [Rate limit] Waiting {wait}s (retry {retry + 1}/3)...")
            time.sleep(wait)
            return _call_groq(text_chunk, source, retry=retry + 1)

        print(f"    [Groq warn] {source}: {e}")
        return []


def extract_tools_with_ai(text: str, source_hint: str = "unknown") -> list:
    """
    Extract AI tools from any page text or markdown using Groq AI.

    Processes the FULL page regardless of size — no truncation.
    Uses a 13s delay between chunks to stay safely under Groq's
    6,000 tokens/minute free tier limit.

    For a 350,000 char page (~117 chunks) this takes ~25 minutes.
    For a 30,000 char page (~10 chunks) this takes ~2 minutes.

    Args:
        text:        Raw text from Playwright inner_text() or Jina markdown
        source_hint: URL or label used in log output

    Returns:
        Deduplicated list of dicts: [{name, description, category, website}]
    """
    if not text or len(text.strip()) < 50:
        return []

    # Split into overlapping chunks
    chunks = []
    start  = 0
    while start < len(text):
        chunks.append(text[start: start + CHUNK_SIZE])
        start += CHUNK_SIZE - OVERLAP

    total_chars = len(text)
    est_minutes = round((len(chunks) * DELAY_BETWEEN_CHUNKS) / 60, 1)
    print(f"    Extracting: {source_hint}")
    print(f"    {total_chars:,} chars → {len(chunks)} chunks → ~{est_minutes} min estimated")

    all_tools  = []
    seen_names = set()

    for i, chunk in enumerate(chunks):
        tools = _call_groq(chunk, source_hint)
        for tool in tools:
            key = tool["name"].lower().strip()
            if key not in seen_names:
                seen_names.add(key)
                all_tools.append(tool)

        # Progress indicator for large repos
        if len(chunks) > 10:
            print(f"    chunk {i+1}/{len(chunks)} — {len(all_tools)} tools so far")

        # Always wait between chunks to respect rate limit
        if i < len(chunks) - 1:
            time.sleep(DELAY_BETWEEN_CHUNKS)

    print(f"    → {len(all_tools)} tools extracted from {source_hint}")
    return all_tools


def fetch_markdown_via_jina(url: str) -> str:
    """
    Convert any URL to clean markdown using Jina Reader.
    Completely free — no API key needed.
    Best for GitHub READMEs and simple static pages.

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