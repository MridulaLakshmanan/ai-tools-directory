"""
backend/run_scraper.py
------------------------
REPLACE your existing run_scraper.py with this file.

AI-Powered Master Scraper — this is the only file you need to run.

Pipeline:
  1. GitHub scraper      — 8 awesome-list repos via Jina + Groq AI
  2. Futurepedia scraper — futurepedia.io paginated (up to 10 pages)
  3. theresanai scraper  — theresanai.com (14 category pages)
  4. Normalize           — shape data to match Supabase schema exactly
  5. Deduplicate         — remove duplicate names in-memory
  6. Insert              — skip tools already in Supabase, insert new ones

Safe to re-run anytime:
  Already-existing tools are checked by name before inserting.
  Running again will only add genuinely new tools.

Usage:
  cd backend
  python run_scraper.py
"""

from scraper.sources.github_scraper      import scrape_github
from scraper.sources.futurepedia_scraper import scrape_futurepedia
from scraper.sources.theresanai_scraper  import scrape_theresanai

from scraper.pipeline.normalize   import normalize_tool
from scraper.pipeline.deduplicate import remove_duplicates

from utils.supabase_client import get_client


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

    # ── Step 2: Combine all sources ───────────────────────────────
    raw_all = github_tools + futurepedia_tools + theresanai_tools
    print(f"\n{'=' * 60}")
    print(f"  Raw tools collected:   {len(raw_all)}")

    # ── Step 3: Normalize (shape to Supabase schema) ──────────────
    normalized = [normalize_tool(t) for t in raw_all]

    # ── Step 4: Deduplicate in-memory ─────────────────────────────
    normalized = remove_duplicates(normalized)
    print(f"  After deduplication:   {len(normalized)}")
    print("=" * 60)

    # ── Step 5: Insert new tools into Supabase ────────────────────
    print("\nInserting into Supabase (skipping already-existing tools)...\n")

    supabase         = get_client()
    inserted         = 0
    skipped_existing = 0
    skipped_invalid  = 0

    for tool in normalized:
        name    = tool.get("name", "")
        url     = tool.get("url", "") or tool.get("website", "") or ""

        # ── Guard 1: Skip invalid/empty entries ───────────────────
        if not name or len(name) < 3:
            skipped_invalid += 1
            continue

        # ── Guard 2: Skip anchor-only or missing URLs ─────────────
        if not url or url.startswith("#"):
            skipped_invalid += 1
            continue

        # ── Guard 3: Skip if already in Supabase (by name) ────────
        try:
            existing = (
                supabase
                .table("ai_tools")
                .select("name")
                .eq("name", name)
                .execute()
            )
        except Exception as e:
            print(f"  [DB warn] Could not check '{name}': {e}")
            skipped_invalid += 1
            continue

        if existing.data:
            skipped_existing += 1
            continue

        # ── Insert new tool ───────────────────────────────────────
        try:
            supabase.table("ai_tools").insert(tool).execute()
            inserted += 1
            print(f"  ✅  {name}")
        except Exception as e:
            print(f"  [DB error] Could not insert '{name}': {e}")
            skipped_invalid += 1

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"  ✅  Inserted:            {inserted} new tools")
    print(f"  ⏭   Already in DB:      {skipped_existing} tools (skipped)")
    print(f"  ❌  Invalid/skipped:    {skipped_invalid} entries")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run()