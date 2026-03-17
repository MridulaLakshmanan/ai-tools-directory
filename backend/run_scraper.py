"""
backend/run_scraper.py
-----------------------
REPLACE your existing run_scraper.py

Key fix: GitHub scraping now inserts tools immediately as each worker
finishes — no longer waits for all sources to complete before inserting.

Futurepedia and theresanai still run after GitHub and insert at the end.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper.sources.github_scraper      import scrape_github
from scraper.sources.futurepedia_scraper import scrape_futurepedia
from scraper.sources.theresanai_scraper  import scrape_theresanai

from scraper.pipeline.normalize   import normalize_tool
from scraper.pipeline.deduplicate import remove_duplicates

from utils.supabase_client import get_client


def fetch_existing_names(supabase) -> set:
    """
    Load all existing tool names from Supabase in one query.
    Returns a lowercase set for fast case-insensitive lookup.
    """
    try:
        all_names = set()
        page      = 0
        page_size = 1000

        while True:
            res = (
                supabase
                .table("ai_tools")
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

        print(f"  Loaded {len(all_names)} existing tool names from Supabase")
        return all_names

    except Exception as e:
        print(f"  [WARN] Could not fetch existing names: {e}")
        return set()


def insert_batch(tools: list, existing_names: set, supabase) -> int:
    """
    Normalize, deduplicate and insert a batch of tools.
    Returns count inserted.
    """
    if not tools:
        return 0

    normalized = [normalize_tool(t) for t in tools]
    normalized = remove_duplicates(normalized)

    inserted        = 0
    skipped_exists  = 0
    skipped_invalid = 0

    for tool in normalized:
        name = tool.get("name", "")
        url  = tool.get("url", "") or tool.get("website", "") or ""

        if not name or len(name) < 3:
            skipped_invalid += 1
            continue
        if not url or url.startswith("#"):
            skipped_invalid += 1
            continue
        if name.strip().lower() in existing_names:
            skipped_exists += 1
            continue

        try:
            supabase.table("ai_tools").insert(tool).execute()
            inserted += 1
            existing_names.add(name.strip().lower())
            print(f"  ✅  {name}")
        except Exception as e:
            print(f"  [DB error] Could not insert '{name}': {e}")
            skipped_invalid += 1

    return inserted


def run():
    print("\n" + "=" * 60)
    print("  AI(n)AI — Scraper Starting")
    print("=" * 60)

    print("\nConnecting to Supabase...")
    supabase       = get_client()
    existing_names = fetch_existing_names(supabase)

    total_inserted = 0

    # ── GitHub: scrapes + inserts immediately per worker ──────────
    # Each worker inserts as soon as its repo finishes
    # So Awesome-LLM's 253 tools get saved without waiting for e2b-dev
    print("\n[1/3] Scraping GitHub repos (inserting as each finishes)...")
    github_inserted = scrape_github(existing_names, supabase)
    total_inserted += github_inserted
    print(f"\n  GitHub done — {github_inserted} tools inserted so far")

    # ── Futurepedia ───────────────────────────────────────────────
    print("\n[2/3] Scraping Futurepedia...")
    futurepedia_tools = scrape_futurepedia()
    if futurepedia_tools:
        print(f"\n  Inserting {len(futurepedia_tools)} Futurepedia tools...")
        count = insert_batch(futurepedia_tools, existing_names, supabase)
        total_inserted += count
        print(f"  Futurepedia done — {count} tools inserted")

    # ── There's An AI ─────────────────────────────────────────────
    print("\n[3/3] Scraping There's An AI...")
    theresanai_tools = scrape_theresanai()
    if theresanai_tools:
        print(f"\n  Inserting {len(theresanai_tools)} theresanai tools...")
        count = insert_batch(theresanai_tools, existing_names, supabase)
        total_inserted += count
        print(f"  theresanai done — {count} tools inserted")

    # ── Final summary ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"  ✅  Total new tools inserted: {total_inserted}")
    print(f"  📦  Approx tools in DB now:   {len(existing_names)}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run()