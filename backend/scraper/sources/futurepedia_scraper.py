"""
backend/scraper/sources/futurepedia_scraper.py
------------------------------------------------
REPLACE your existing futurepedia_scraper.py

Fix: the previous version was getting 1,285 chars per page which means
Playwright wasn't waiting long enough for JS to render the tool cards.
This version waits for actual tool cards to appear before extracting text.
"""

from playwright.sync_api import sync_playwright
from scraper.pipeline.groq_extractor import extract_tools_with_ai

BASE_URL  = "https://www.futurepedia.io/ai-tools"
MAX_PAGES = 8


def _get_page_text(page) -> str:
    """
    Wait for tool cards to fully render then return page text.
    Futurepedia is JS-heavy — we must wait for actual card content.
    """
    try:
        # Wait up to 15s for tool card links to appear
        page.wait_for_selector("a[href*='/tool/']", timeout=15000)
    except Exception:
        print("    [Warn] Tool card selector timed out — trying anyway")

    # Extra wait for lazy images and dynamic content to settle
    page.wait_for_timeout(3000)

    # Scroll down twice to trigger any lazy-loaded cards
    for _ in range(2):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

    # Count how many tool links are visible — if too few, page didn't load
    card_count = page.locator("a[href*='/tool/']").count()
    print(f"    Found {card_count} tool card links on page")

    if card_count < 3:
        return ""

    # Get text from main content only
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


def scrape_futurepedia() -> list:
    all_tools = []

    with sync_playwright() as p:
        # Use non-headless so JS loads properly — change to True if you want background
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()

        for page_num in range(1, MAX_PAGES + 1):
            url = BASE_URL if page_num == 1 else f"{BASE_URL}?page={page_num}"
            print(f"\n  Futurepedia page {page_num} → {url}")

            try:
                page.goto(url, timeout=30000, wait_until="networkidle")
            except Exception as e:
                print(f"    [Error] Could not load: {e}")
                break

            text = _get_page_text(page)

            if not text:
                print(f"    [Stop] No content on page {page_num} — stopping")
                break

            tools = extract_tools_with_ai(
                text, source_hint=f"futurepedia-page{page_num}"
            )

            if not tools:
                print(f"    [Stop] No tools found — reached end")
                break

            all_tools.extend(tools)
            print(f"    Running total: {len(all_tools)}")

        browser.close()

    print(f"\n  Futurepedia scraper done — {len(all_tools)} tools collected")
    return all_tools