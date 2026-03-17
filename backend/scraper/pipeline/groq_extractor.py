"""
backend/scraper/pipeline/groq_extractor.py
"""

import os
import json
import time
import urllib.request

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE           = 2500   # smaller chunks = fewer tokens per request
OVERLAP              = 150
DELAY_BETWEEN_CHUNKS = 25.0   # 25s gap — well under 6k tokens/min limit

VALID_CATEGORIES = [
    "AI Assistants",
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
- "website": tool URL (string, use empty string if not found)

Rules:
- Skip navigation links, section headings, table of contents entries
- Skip anything that is not a real usable software tool
- Write a short description if one is missing
- Never duplicate the same tool name
- Return [] if no tools found
"""


def _make_client(api_key: str) -> Groq:
    if not api_key or api_key.strip() in ("", "your_groq_api_key_here"):
        raise ValueError(
            "\nGroq API key missing.\n"
            "Get a free key at https://console.groq.com\n"
            "Add to backend/.env as GROQ_API_KEY=gsk_...\n"
        )
    return Groq(api_key=api_key.strip())


def _call_groq(client: Groq, text_chunk: str, source: str, retry: int = 0) -> list:
    """Send one chunk. Returns tool list. Never raises."""
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Extract AI tools (source: {source}):\n\n{text_chunk}"},
            ],
            temperature=0.1,
            max_tokens=1500,   # capped output tokens to reduce token usage
        )

        raw = resp.choices[0].message.content.strip()

        if "```" in raw:
            parts = raw.split("```")
            raw   = parts[1] if len(parts) > 1 else parts[0]
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
        return []

    except Exception as e:
        err = str(e).lower()
        if "rate" in err or "429" in err:
            if retry >= 3:
                print(f"    [Rate limit] Max retries — skipping chunk")
                return []
            wait = 30 * (2 ** retry)   # 30s → 60s → 120s
            print(f"    [Rate limit] Waiting {wait}s (retry {retry + 1}/3)...")
            time.sleep(wait)
            return _call_groq(client, text_chunk, source, retry=retry + 1)
        print(f"    [Groq warn] {source}: {e}")
        return []


def extract_tools_with_ai(text: str, source_hint: str = "unknown", api_key: str = None) -> list:
    """
    Extract AI tools from page text using Groq AI.
    Processes full page with 25s delay between chunks.
    """
    if not text or len(text.strip()) < 50:
        return []

    key    = api_key or os.environ.get("GROQ_API_KEY", "")
    client = _make_client(key)

    chunks = []
    start  = 0
    while start < len(text):
        chunks.append(text[start: start + CHUNK_SIZE])
        start += CHUNK_SIZE - OVERLAP

    est_minutes = round((len(chunks) * DELAY_BETWEEN_CHUNKS) / 60, 1)
    print(f"    Source:  {source_hint}")
    print(f"    Size:    {len(text):,} chars → {len(chunks)} chunks → ~{est_minutes} min")

    all_tools  = []
    seen_names = set()

    for i, chunk in enumerate(chunks):
        tools = _call_groq(client, chunk, source_hint)
        for tool in tools:
            key_name = tool["name"].lower().strip()
            if key_name not in seen_names:
                seen_names.add(key_name)
                all_tools.append(tool)

        if len(chunks) > 5:
            print(f"    chunk {i + 1}/{len(chunks)} — {len(all_tools)} tools so far")

        if i < len(chunks) - 1:
            time.sleep(DELAY_BETWEEN_CHUNKS)

    print(f"    → {len(all_tools)} tools extracted from {source_hint}")
    return all_tools


def fetch_markdown_via_jina(url: str) -> str:
    """Convert URL to markdown via Jina Reader. Free, no key needed."""
    jina_url = f"https://r.jina.ai/{url}"
    try:
        req = urllib.request.Request(
            jina_url,
            headers={"Accept": "text/plain", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
        print(f"    Jina fetched: {url} → {len(content):,} chars")
        return content
    except Exception as e:
        print(f"    [Jina warn] {url}: {e}")
        return ""