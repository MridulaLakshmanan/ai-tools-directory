"""
backend/scraper/sources/futurepedia_scraper.py
------------------------------------------------
REPLACE your existing file at: backend/scraper/sources/futurepedia_scraper.py

Scrapes futurepedia.io across multiple pages using:
  - Playwright to render JS-heavy pages
  - Groq AI to extract tools from page text
  - Stops automatically when no more tools are found
"""

from playwright.sync_api import sync_playwright
from scraper.pipeline.groq_extractor import extract_tools_with_ai

BASE_URL  = "https://www.futurepedia.io/ai-tools"
MAX_PAGES = 10  # increase if you want more results


def _get_page_text(page) -> str:
    """Scroll to load lazy content then return visible page text."""
    try:
        page.wait_for_selector("a[href*='/tool/']", timeout=10000)
    except Exception:
        pass  # Continue even if selector never appears

    # Scroll 3 times to trigger lazy-loaded cards
    for _ in range(3):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1500)

    # Try to get just the main content area first (cleaner text)
    for selector in ["main", "#__next", "body"]:
        try:
            el = page.query_selector(selector)
            if el:
                text = el.inner_text()
                if len(text.strip()) > 100:
                    return text
        except Exception:
            continue

    return ""


def scrape_futurepedia() -> list:
    """
    Scrape Futurepedia across multiple pages using AI extraction.
    """
    all_tools = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page    = browser.new_page()

        for page_num in range(1, MAX_PAGES + 1):
            url = BASE_URL if page_num == 1 else f"{BASE_URL}?page={page_num}"
            print(f"\n  Futurepedia page {page_num} → {url}")

            try:
                page.goto(url, timeout=30000)
            except Exception as e:
                print(f"    [Error] Could not load: {e}")
                break

            text = _get_page_text(page)

            if not text:
                print(f"    [Stop] No content on page {page_num}")
                break

            tools = extract_tools_with_ai(
                text, source_hint=f"futurepedia-page{page_num}"
            )

            if not tools:
                print(f"    [Stop] No tools found — reached end of results")
                break

            all_tools.extend(tools)
            print(f"    Running total: {len(all_tools)}")

        browser.close()

    print(f"\n  Futurepedia scraper done — {len(all_tools)} tools collected")
    return all_tools