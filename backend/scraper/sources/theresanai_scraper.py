"""
scraper/sources/theresanai_scraper.py
----------------------------------------
NEW FILE — Add this to backend/scraper/sources/

Scrapes theresanai.com across 14 category pages.
theresanai.com is one of the largest AI tool directories with 5000+ tools.

Strategy:
  - Jina Reader fetches each category page as clean markdown (free, no key)
  - Groq AI extracts structured tool data from the markdown
  - No Playwright needed — Jina handles JS rendering for these pages

To add more categories: append URLs to THERESANAI_URLS below.
"""

from scraper.pipeline.groq_extractor import extract_tools_with_ai, fetch_markdown_via_jina

THERESANAI_URLS = [
    "https://theresanai.com",
    "https://theresanai.com/category/writing",
    "https://theresanai.com/category/image-generation",
    "https://theresanai.com/category/video",
    "https://theresanai.com/category/audio",
    "https://theresanai.com/category/coding",
    "https://theresanai.com/category/productivity",
    "https://theresanai.com/category/research",
    "https://theresanai.com/category/marketing",
    "https://theresanai.com/category/chatbots",
    "https://theresanai.com/category/design",
    "https://theresanai.com/category/education",
    "https://theresanai.com/category/business",
    "https://theresanai.com/category/social-media",
]


def scrape_theresanai() -> list[dict]:
    """
    Scrape all theresanai.com category pages.

    Returns:
        List of raw tool dicts: [{name, description, category, website}, ...]
    """
    all_tools = []

    for url in THERESANAI_URLS:
        print(f"\n  theresanai.com → {url}")

        markdown = fetch_markdown_via_jina(url)

        if not markdown:
            print(f"    [Skip] No content returned — moving on")
            continue

        tools = extract_tools_with_ai(markdown, source_hint=url)
        all_tools.extend(tools)
        print(f"    Running total: {len(all_tools)}")

    print(f"\n  theresanai.com scraper done — {len(all_tools)} tools")
    return all_tools