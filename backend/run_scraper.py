"""
backend/run_scraper.py
-----------------------
REPLACE your existing run_scraper.py

Fixes in this version:
  1. Case-insensitive name check — uses ilike instead of eq
     so "ChatGPT" and "chatgpt" are treated as the same tool
  2. Bulk name fetch at start — one DB call instead of one per tool
     much faster and avoids hammering Supabase with hundreds of requests
  3. Better error logging — prints the actual DB error message
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
    Fetch all existing tool names from Supabase in one query.
    Returns a lowercase set for fast case-insensitive lookup.
    Much faster than checking each tool individually.
    """
    try:
        # Fetch in pages of 1000 to handle large tables
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
        print(f"  Continuing without duplicate check — may insert some duplicates")
        return set()


def run():
    print("\n" + "=" * 60)
    print("  AI(n)AI — Scraper Starting")
    print("=" * 60)

    # ── Step 1: Collect raw tools from all 3 sources ──────────────
    print("\n[1/3] Scraping GitHub awesome lists...")
    github_tools = scrape_github()

    print("\n[2/3] Scraping Futurepedia...")
    futurepedia_tools = scrape_futurepedia()

    print("\n[3/3] Scraping There's An AI...")
    theresanai_tools = scrape_theresanai()

    # ── Step 2: Combine + normalize + deduplicate ─────────────────
    raw_all = github_tools + futurepedia_tools + theresanai_tools
    print(f"\n{'=' * 60}")
    print(f"  Raw tools collected:   {len(raw_all)}")

    normalized = [normalize_tool(t) for t in raw_all]
    normalized = remove_duplicates(normalized)
    print(f"  After deduplication:   {len(normalized)}")
    print("=" * 60)

    # ── Step 3: Fetch all existing names in ONE query ─────────────
    print("\nConnecting to Supabase...")
    supabase       = get_client()
    existing_names = fetch_existing_names(supabase)

    # ── Step 4: Insert only genuinely new tools ───────────────────
    print("\nInserting new tools...\n")

    inserted        = 0
    skipped_exists  = 0
    skipped_invalid = 0

    for tool in normalized:
        name = tool.get("name", "")
        url  = tool.get("url", "") or tool.get("website", "") or ""

        # Guard 1: Skip invalid/empty entries
        if not name or len(name) < 3:
            skipped_invalid += 1
            continue

        # Guard 2: Skip anchor-only or missing URLs
        if not url or url.startswith("#"):
            skipped_invalid += 1
            continue

        # Guard 3: Case-insensitive duplicate check against existing DB names
        if name.strip().lower() in existing_names:
            skipped_exists += 1
            continue

        # Insert new tool
        try:
            supabase.table("ai_tools").insert(tool).execute()
            inserted += 1
            # Add to local set so later tools in same run don't duplicate it
            existing_names.add(name.strip().lower())
            print(f"  ✅  {name}")
        except Exception as e:
            print(f"  [DB error] Could not insert '{name}': {e}")
            skipped_invalid += 1

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"  ✅  Inserted:          {inserted} new tools")
    print(f"  ⏭   Already in DB:    {skipped_exists} tools (skipped)")
    print(f"  ❌  Invalid/skipped:  {skipped_invalid} entries")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run()