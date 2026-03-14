"""
backend/scraper/sources/github_scraper.py
--------------------------------------------
REPLACE your existing file at: backend/scraper/sources/github_scraper.py

Scrapes 8 GitHub awesome-list repos using:
  - Jina Reader (free, no key) to convert READMEs → clean markdown
  - Groq AI to extract structured tool data from that markdown
  - No CSS selectors — works on any README layout
"""

from scraper.pipeline.groq_extractor import extract_tools_with_ai, fetch_markdown_via_jina

GITHUB_URLS = [
    "https://github.com/mahseema/awesome-ai-tools",
    "https://github.com/steven2358/awesome-generative-ai",
    "https://github.com/e2b-dev/awesome-ai-agents",
    "https://github.com/Hannibal046/Awesome-LLM",
    "https://github.com/ai-for-developers/awesome-ai-coding-tools",
    "https://github.com/humanloop/awesome-chatgpt",
    "https://github.com/filipecalegario/awesome-generative-ai",
    "https://github.com/fr0gger/Awesome-GPT-Agents",
]


def scrape_github() -> list:
    """
    Scrape all GitHub awesome-list URLs.
    Uses Jina → markdown, then Groq AI → structured tool data.
    """
    all_tools = []

    for url in GITHUB_URLS:
        print(f"\n  GitHub → {url}")

        markdown = fetch_markdown_via_jina(url)

        if not markdown:
            print(f"    [Skip] No content returned from Jina")
            continue

        tools = extract_tools_with_ai(markdown, source_hint=url)
        all_tools.extend(tools)
        print(f"    Running total: {len(all_tools)}")

    print(f"\n  GitHub scraper done — {len(all_tools)} tools collected")
    return all_tools