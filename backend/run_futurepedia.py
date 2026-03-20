"""
backend/run_futurepedia.py
---------------------------
Standalone script — runs ONLY Futurepedia and inserts to Supabase.

Run:
  cd backend
  python run_futurepedia.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from scraper.pipeline.groq_extractor import extract_tools_with_ai
from scraper.pipeline.normalize      import normalize_tool
from scraper.pipeline.deduplicate    import remove_duplicates
from utils.supabase_client           import get_client

BASE_URL  = "https://www.futurepedia.io/ai-tools"
MAX_PAGES = 8


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


def get_page_text(page) -> str:
    """Extract tool text from a loaded Futurepedia page."""
    # Wait for tool card links to appear
    try:
        page.wait_for_selector("a[href*='/tool/']", timeout=20000)
    except PlaywrightTimeout:
        print("    [Warn] Tool cards timed out")
        return ""
    except Exception as e:
        print(f"    [Warn] Selector error: {e}")
        return ""

    # Settle wait
    try:
        page.wait_for_timeout(2000)
    except Exception:
        pass

    # Scroll to load lazy cards
    try:
        for _ in range(2):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1500)
    except Exception:
        pass

    # Count cards
    try:
        card_count = page.locator("a[href*='/tool/']").count()
        print(f"    Found {card_count} tool cards")
        if card_count < 3:
            return ""
    except Exception:
        return ""

    # Get text from main content
    for selector in ["main", "#__next", "body"]:
        try:
            el = page.query_selector(selector)
            if el:
                text = el.inner_text()
                if len(text.strip()) > 500:
                    return text
        except Exception:
            continue

    return ""


def run():
    print("\n" + "=" * 60)
    print("  Futurepedia Scraper — Standalone Run")
    print("=" * 60)

    print("\nConnecting to Supabase...")
    supabase       = get_client()
    existing_names = fetch_existing_names(supabase)

    total_extracted = 0
    total_inserted  = 0

    with sync_playwright() as p:
        # headless=True — runs in background, no window to accidentally close
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )

        for page_num in range(1, MAX_PAGES + 1):
            url = BASE_URL if page_num == 1 else f"{BASE_URL}?page={page_num}"
            print(f"\n  Page {page_num}/{MAX_PAGES} → {url}")

            # Create a fresh page per iteration — avoids TargetClosedError
            page = context.new_page()

            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
            except Exception as e:
                print(f"    [Error] Could not load: {e}")
                page.close()
                break

            text = get_page_text(page)
            page.close()  # close page immediately after extracting text

            if not text:
                print(f"    [Stop] No content — stopping pagination")
                break

            tools = extract_tools_with_ai(
                text, source_hint=f"futurepedia-page{page_num}"
            )

            if not tools:
                print(f"    [Stop] No tools found — reached end of results")
                break

            total_extracted += len(tools)
            print(f"    Extracted {len(tools)} tools — inserting into Supabase now...")

            count = insert_tools(tools, existing_names, supabase)
            total_inserted += count
            print(f"    Page {page_num} done — {count} new tools inserted")

        browser.close()

    print("\n" + "=" * 60)
    print(f"  Total extracted:  {total_extracted}")
    print(f"  Total inserted:   {total_inserted} new tools")
    print(f"  Tools in DB now:  ~{len(existing_names)}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run()