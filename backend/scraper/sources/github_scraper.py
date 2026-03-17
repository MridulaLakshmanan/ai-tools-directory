"""
backend/scraper/sources/github_scraper.py

Runs repos SEQUENTIALLY — one after another, not in parallel.
Reason: both Groq keys are on the same account so they share
the same rate limit. Running in parallel doubles the request rate
and causes both workers to hit limits at the same time.

Sequential = one key used at a time = zero rate limit conflicts.
Each repo inserts into Supabase immediately after finishing.
"""

import os
from dotenv import load_dotenv

from scraper.pipeline.groq_extractor import extract_tools_with_ai, fetch_markdown_via_jina

load_dotenv()

# Two repos chosen for minimum overlap with your existing 362 DB tools
GITHUB_URLS = [
    "https://github.com/e2b-dev/awesome-ai-agents",
    "https://github.com/Hannibal046/Awesome-LLM",
]


def _get_key() -> str:
    """Get primary Groq API key."""
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key or key == "your_groq_api_key_here":
        raise ValueError(
            "\nGROQ_API_KEY not set in .env\n"
            "Get a free key at https://console.groq.com\n"
        )
    return key


def _insert_tools(tools: list, existing_names: set, supabase) -> int:
    """Normalize, deduplicate and insert tools. Returns count inserted."""
    from scraper.pipeline.normalize   import normalize_tool
    from scraper.pipeline.deduplicate import remove_duplicates

    if not tools:
        return 0

    normalized = [normalize_tool(t) for t in tools]
    normalized = remove_duplicates(normalized)

    inserted = 0
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


def scrape_github(existing_names: set, supabase) -> int:
    """
    Scrape repos one at a time and insert after each.
    Sequential = no rate limit conflicts.
    """
    api_key       = _get_key()
    total_inserted = 0

    for i, url in enumerate(GITHUB_URLS):
        print(f"\n  ── Repo {i + 1}/{len(GITHUB_URLS)}: {url}")

        markdown = fetch_markdown_via_jina(url)
        if not markdown:
            print(f"  [Skip] No content from Jina")
            continue

        tools = extract_tools_with_ai(markdown, source_hint=url, api_key=api_key)

        if not tools:
            print(f"  [Skip] No tools extracted")
            continue

        print(f"\n  Scraping done — inserting {len(tools)} tools into Supabase...")
        count = _insert_tools(tools, existing_names, supabase)
        total_inserted += count
        print(f"  ✅ Inserted {count} new tools from {url}")

    print(f"\n  GitHub scraper done — {total_inserted} total tools inserted")
    return total_inserted