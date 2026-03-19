"""
backend/scraper/sources/github_scraper.py
"""

import os
from dotenv import load_dotenv
from scraper.pipeline.groq_extractor import extract_tools_with_ai, fetch_markdown_via_jina

load_dotenv()

# Only one repo for now
GITHUB_URL = "https://github.com/Hannibal046/Awesome-LLM"


def _insert_tools(tools: list, existing_names: set, supabase) -> int:
    from scraper.pipeline.normalize   import normalize_tool
    from scraper.pipeline.deduplicate import remove_duplicates

    if not tools:
        return 0

    normalized = [normalize_tool(t) for t in tools]
    normalized = remove_duplicates(normalized)

    inserted = 0
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


def scrape_github(existing_names: set, supabase) -> int:
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY not set in .env")

    print(f"\n  Scraping: {GITHUB_URL}")

    markdown = fetch_markdown_via_jina(GITHUB_URL)
    if not markdown:
        print("  [Skip] No content returned from Jina")
        return 0

    tools = extract_tools_with_ai(markdown, source_hint=GITHUB_URL, api_key=api_key)

    if not tools:
        print("  [Skip] No tools extracted")
        return 0

    print(f"\n  Scraping done — inserting {len(tools)} tools into Supabase...")
    count = _insert_tools(tools, existing_names, supabase)
    print(f"  ✅ Inserted {count} new tools")
    return count