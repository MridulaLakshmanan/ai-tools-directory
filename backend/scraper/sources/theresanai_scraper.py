"""
backend/scraper/sources/theresanai_scraper.py
-----------------------------------------------
NEW FILE — place at: backend/scraper/sources/theresanai_scraper.py

Scrapes theresanai.com across 14 category pages using:
  - Jina Reader (free, no key) to fetch pages as clean markdown
  - Groq AI to extract structured tool data
  - No Playwright needed for this source
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


def scrape_theresanai() -> list:
    """
    Scrape all theresanai.com category pages.
    Uses Jina Reader to fetch markdown, Groq AI to extract tools.
    """
    all_tools = []

    for url in THERESANAI_URLS:
        print(f"\n  theresanai.com → {url}")

        markdown = fetch_markdown_via_jina(url)

        if not markdown:
            print(f"    [Skip] No content returned from Jina")
            continue

        tools = extract_tools_with_ai(markdown, source_hint=url)
        all_tools.extend(tools)
        print(f"    Running total: {len(all_tools)}")

    print(f"\n  theresanai.com scraper done — {len(all_tools)} tools collected")
    return all_tools