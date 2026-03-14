"""
backend/scraper/sources/github_scraper.py
--------------------------------------------
REPLACE your existing github_scraper.py with this file.

What changed:
  - Now scrapes 8 repos instead of 1
  - Uses Jina Reader (free) instead of Playwright for GitHub pages
  - Uses Groq AI instead of BeautifulSoup for extraction
  - No CSS selectors — works even if GitHub changes layout
  - Handles any README structure automatically

To add more repos: just append a URL to GITHUB_URLS below.
"""

from scraper.pipeline.groq_extractor import extract_tools_with_ai, fetch_markdown_via_jina

# ── Repos to scrape ───────────────────────────────────────────────────────────
# Jina converts GitHub READMEs to clean markdown — no Playwright needed here
GITHUB_URLS = [
    "https://github.com/mahseema/awesome-ai-tools",        # original source
    "https://github.com/steven2358/awesome-generative-ai",  # generative AI tools
    "https://github.com/e2b-dev/awesome-ai-agents",        # AI agents
    "https://github.com/Hannibal046/Awesome-LLM",          # LLM tools & resources
    "https://github.com/ai-for-developers/awesome-ai-coding-tools",  # coding tools
    "https://github.com/humanloop/awesome-chatgpt",        # ChatGPT ecosystem
    "https://github.com/filipecalegario/awesome-generative-ai",     # more gen AI
    "https://github.com/fr0gger/Awesome-GPT-Agents",       # GPT agents
]


def scrape_github() -> list:
    """
    Scrape all GitHub awesome-list repos.
    Uses Jina Reader to convert READMEs → markdown,
    then Groq AI to extract structured tool data.

    Returns:
        List of raw tool dicts: [{name, description, category, website}, ...]
    """
    all_tools = []

    for url in GITHUB_URLS:
        print(f"\n  GitHub → {url}")

        # Jina converts the README to plain text for free — no auth needed
        markdown = fetch_markdown_via_jina(url)

        if not markdown:
            print(f"    [Skip] No content returned from Jina")
            continue

        tools = extract_tools_with_ai(markdown, source_hint=url)
        all_tools.extend(tools)
        print(f"    Running total: {len(all_tools)}")

    print(f"\n  GitHub scraper done — {len(all_tools)} tools collected")
    return all_tools