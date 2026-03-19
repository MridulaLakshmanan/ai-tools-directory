"""
backend/scraper/sources/theresanai_scraper.py
-----------------------------------------------
REPLACE your existing theresanai_scraper.py

theresanai.com blocks Jina (HTTP 422) so we switch to two new sources
that work well with Jina Reader:
  1. aitoolsdirectory.com  — large public AI tool directory
  2. topai.tools           — curated AI tools, good category coverage

Both are static-enough for Jina to fetch cleanly.
"""

from scraper.pipeline.groq_extractor import extract_tools_with_ai, fetch_markdown_via_jina

SOURCES = [
    "https://aitoolsdirectory.com",
    "https://topai.tools",
    "https://www.toolify.ai/category/writing-ai-tools",
    "https://www.toolify.ai/category/image-ai-tools",
    "https://www.toolify.ai/category/video-ai-tools",
    "https://www.toolify.ai/category/code-ai-tools",
    "https://www.toolify.ai/category/audio-ai-tools",
    "https://www.toolify.ai/category/productivity-ai-tools",
]


def scrape_theresanai() -> list:
    """
    Scrape alternative AI tool directory sources using Jina + Groq.
    Function name kept as scrape_theresanai so run_scraper.py needs no changes.
    """
    all_tools = []

    for url in SOURCES:
        print(f"\n  Scraping → {url}")

        markdown = fetch_markdown_via_jina(url)

        if not markdown:
            print(f"    [Skip] No content returned")
            continue

        tools = extract_tools_with_ai(markdown, source_hint=url)
        all_tools.extend(tools)
        print(f"    Running total: {len(all_tools)}")

    print(f"\n  Directory scraper done — {len(all_tools)} tools collected")
    return all_tools