"""
run_scraper.py  —  Master scraper runner
=========================================
Sources:
  1. github_scraper       — mahseema/awesome-ai-tools + 6 more awesome lists
  2. futurepedia_scraper  — futurepedia.io
  3. theresanai_scraper   — theresanai.com
  4. directories_scraper  — aitoptools, aitoolsdirectory, topai.tools, insidr.ai

Run:
    python run_scraper.py
"""

from scraper.sources.github_scraper import scrape_github
from scraper.sources.futurepedia_scraper import scrape_futurepedia
from scraper.sources.theresanai_scraper import scrape_theresanai
from scraper.sources.directories_scraper import scrape_directories

from scraper.pipeline.normalize import normalize_tool
from scraper.pipeline.deduplicate import remove_duplicates

from utils.supabase_client import get_client

supabase = get_client()


def run():
    print("\n=== Scraping GitHub awesome lists ===")
    github_tools = scrape_github()

    print("\n=== Scraping Futurepedia ===")
    futurepedia_tools = scrape_futurepedia()

    print("\n=== Scraping There's An AI ===")
    theresanai_tools = scrape_theresanai()

    print("\n=== Scraping AI Tool Directories ===")
    directory_tools = scrape_directories()

    # Combine all sources
    all_tools = github_tools + futurepedia_tools + theresanai_tools + directory_tools
    print(f"\nTotal raw tools collected: {len(all_tools)}")

    # Normalize + deduplicate
    normalized = [normalize_tool(t) for t in all_tools]
    normalized = remove_duplicates(normalized)
    print(f"After deduplication: {len(normalized)}")

    # Insert only new tools (skip existing by name)
    inserted = 0
    skipped = 0

    for tool in normalized:
        # Skip tools with no name or clearly invalid entries
        if not tool.get("name") or len(tool["name"]) < 3:
            skipped += 1
            continue

        # Skip anchor-only URLs
        url = tool.get("url", "") or ""
        if url.startswith("#") or not url:
            skipped += 1
            continue

        existing = supabase.table("ai_tools") \
            .select("name") \
            .eq("name", tool["name"]) \
            .execute()

        if existing.data:
            skipped += 1
            continue

        supabase.table("ai_tools").insert(tool).execute()
        inserted += 1
        print(f"  Inserted: {tool['name']}")

    print(f"\n✅ Done — Inserted: {inserted}, Skipped (existing/invalid): {skipped}")


if __name__ == "__main__":
    run()