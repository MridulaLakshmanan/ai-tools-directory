"""
backend/run_futurepedia.py
---------------------------
Fixed version — Futurepedia blocks Playwright selectors.
Instead uses Jina Reader to fetch the page as clean text,
then Groq AI to extract tools from it.

Run:
  cd backend
  python run_futurepedia.py
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper.pipeline.groq_extractor import extract_tools_with_ai, fetch_markdown_via_jina
from scraper.pipeline.normalize      import normalize_tool
from scraper.pipeline.deduplicate    import remove_duplicates
from utils.supabase_client           import get_client

# Futurepedia category pages — more reliable than paginated index
# Each category page has a focused list of tools Jina can read cleanly
FUTUREPEDIA_URLS = [
    "https://www.futurepedia.io/ai-tools/writing",
    "https://www.futurepedia.io/ai-tools/image-editing",
    "https://www.futurepedia.io/ai-tools/video-editing",
    "https://www.futurepedia.io/ai-tools/coding",
    "https://www.futurepedia.io/ai-tools/audio-editing",
    "https://www.futurepedia.io/ai-tools/productivity",
    "https://www.futurepedia.io/ai-tools/marketing",
    "https://www.futurepedia.io/ai-tools/design",
    "https://www.futurepedia.io/ai-tools/research",
    "https://www.futurepedia.io/ai-tools/customer-support",
    "https://www.futurepedia.io/ai-tools/education",
    "https://www.futurepedia.io/ai-tools/business",
    "https://www.futurepedia.io/ai-tools/social-media",
    "https://www.futurepedia.io/ai-tools/sales",
]


def fetch_existing_names(supabase) -> set:
    all_names = set()
    page      = 0
    page_size = 1000
    while True:
        res = (
            supabase.table("ai_tools")
            .select("name")
            .range(page * page_size, (page + 1) * page_size - 1)
            .execute()
        )
        if not res.data:
            break
        for row in res.data:
            if row.get("name"):
                all_names.add(row["name"].strip().lower())
        if len(res.data) < page_size:
            break
        page += 1
    print(f"  Loaded {len(all_names)} existing names from Supabase")
    return all_names


def insert_tools(tools: list, existing_names: set, supabase) -> int:
    if not tools:
        return 0
    normalized = [normalize_tool(t) for t in tools]
    normalized = remove_duplicates(normalized)
    inserted   = 0
    for tool in normalized:
        name = tool.get("name", "")
        url  = tool.get("url", "") or tool.get("website", "") or ""
        if not name or len(name) < 3:
            continue
        if not url or url.startswith("#"):
            continue
        if name.strip().lower() in existing_names:
            continue
        try:
            supabase.table("ai_tools").insert(tool).execute()
            inserted += 1
            existing_names.add(name.strip().lower())
            print(f"  ✅  {name}")
        except Exception as e:
            print(f"  [DB error] '{name}': {e}")
    return inserted


def run():
    print("\n" + "=" * 60)
    print("  Futurepedia Scraper — Jina + Groq AI")
    print("=" * 60)

    print("\nConnecting to Supabase...")
    supabase       = get_client()
    existing_names = fetch_existing_names(supabase)

    total_extracted = 0
    total_inserted  = 0

    for i, url in enumerate(FUTUREPEDIA_URLS):
        print(f"\n  [{i+1}/{len(FUTUREPEDIA_URLS)}] {url}")

        # Jina converts the page to clean readable markdown
        markdown = fetch_markdown_via_jina(url)

        if not markdown or len(markdown.strip()) < 100:
            print(f"    [Skip] No content returned")
            continue

        tools = extract_tools_with_ai(markdown, source_hint=url)

        if not tools:
            print(f"    [Skip] No tools extracted")
            continue

        total_extracted += len(tools)
        print(f"    Inserting {len(tools)} tools into Supabase...")

        count = insert_tools(tools, existing_names, supabase)
        total_inserted += count
        print(f"    Done — {count} new tools inserted")

    print("\n" + "=" * 60)
    print(f"  Total extracted:  {total_extracted}")
    print(f"  Total inserted:   {total_inserted} new tools")
    print(f"  Tools in DB now:  ~{len(existing_names)}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run()