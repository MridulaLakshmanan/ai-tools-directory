"""
backend/scraper/sources/github_scraper.py
-------------------------------------------
REPLACE your existing github_scraper.py

Key fix: each worker now inserts tools into Supabase AS SOON AS it finishes
its repo — no longer waits for the other worker to complete first.

This means even if Worker 1 (e2b-dev) is slow or rate-limited,
Worker 2's 253 tools get saved immediately when it finishes.
"""

import os
import threading
from dotenv import load_dotenv

from scraper.pipeline.groq_extractor import extract_tools_with_ai, fetch_markdown_via_jina

load_dotenv()

GITHUB_URLS = [
    "https://github.com/e2b-dev/awesome-ai-agents",
    "https://github.com/Hannibal046/Awesome-LLM",
]


def _load_api_keys() -> list:
    keys = []
    k1 = os.environ.get("GROQ_API_KEY", "").strip()
    if k1 and k1 != "your_groq_api_key_here":
        keys.append(k1)
    k2 = os.environ.get("GROQ_API_KEY_2", "").strip()
    if k2 and k2 != "your_groq_api_key_here":
        keys.append(k2)
    if not keys:
        raise ValueError(
            "\nNo GROQ_API_KEY found in .env\n"
            "Get a free key at https://console.groq.com\n"
        )
    print(f"  Found {len(keys)} Groq API key{'s' if len(keys) > 1 else ''}")
    return keys


def _insert_tools(tools: list, existing_names: set, supabase, lock: threading.Lock) -> int:
    """
    Insert a list of tools into Supabase immediately.
    Thread-safe — uses lock so two workers don't insert simultaneously.
    Returns count of newly inserted tools.
    """
    from scraper.pipeline.normalize   import normalize_tool
    from scraper.pipeline.deduplicate import remove_duplicates

    if not tools:
        return 0

    # Normalize and deduplicate this batch
    normalized = [normalize_tool(t) for t in tools]
    normalized = remove_duplicates(normalized)

    inserted = 0
    with lock:
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
                print(f"  [DB error] Could not insert '{name}': {e}")

    return inserted


def _scrape_and_insert(url: str, api_key: str, existing_names: set,
                       supabase, db_lock: threading.Lock,
                       total_inserted: list, worker_id: int):
    """
    Worker: scrape one URL, then immediately insert results into Supabase.
    Does not wait for other workers — saves as soon as this repo is done.
    """
    print(f"\n  [Worker {worker_id}] Starting → {url}")

    markdown = fetch_markdown_via_jina(url)
    if not markdown:
        print(f"  [Worker {worker_id}] No content returned — skipping")
        return

    tools = extract_tools_with_ai(markdown, source_hint=url, api_key=api_key)

    if not tools:
        print(f"  [Worker {worker_id}] No tools extracted — skipping insert")
        return

    print(f"\n  [Worker {worker_id}] Scraping done — inserting {len(tools)} tools into Supabase NOW...")
    count = _insert_tools(tools, existing_names, supabase, db_lock)

    with db_lock:
        total_inserted[0] += count

    print(f"  [Worker {worker_id}] ✅ Inserted {count} new tools from {url}")


def scrape_github(existing_names: set, supabase) -> int:
    """
    Scrape both repos in parallel and insert results immediately as each finishes.

    Args:
        existing_names: lowercase set of tool names already in Supabase
        supabase:       Supabase client instance

    Returns:
        Total number of newly inserted tools
    """
    api_keys = _load_api_keys()

    print(f"\n  Repos to scrape: {len(GITHUB_URLS)}")
    for i, url in enumerate(GITHUB_URLS):
        key_num = (i % len(api_keys)) + 1
        print(f"    Repo {i+1}: {url}  →  Key {key_num}")

    db_lock        = threading.Lock()
    total_inserted = [0]   # list so threads can mutate it
    threads        = []

    for i, url in enumerate(GITHUB_URLS):
        api_key   = api_keys[i % len(api_keys)]
        worker_id = i + 1

        t = threading.Thread(
            target=_scrape_and_insert,
            args=(url, api_key, existing_names, supabase, db_lock, total_inserted, worker_id),
            daemon=True,
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\n  GitHub scraper done — {total_inserted[0]} tools inserted total")
    return total_inserted[0]