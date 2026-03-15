"""
backend/scraper/sources/github_scraper.py
--------------------------------------------
REPLACE your existing github_scraper.py

Parallel scraping using multiple Groq API keys.
Repos are split across workers — each worker uses its own key
so they don't share rate limits and run simultaneously.

Setup:
  In your backend/.env add:
    GROQ_API_KEY=gsk_key1here
    GROQ_API_KEY_2=gsk_key2here      ← optional, halves the time
    GROQ_API_KEY_3=gsk_key3here      ← optional, cuts time by 2/3

  Get free keys at https://console.groq.com
  Use Gmail + trick: youremail+groq2@gmail.com, youremail+groq3@gmail.com
"""

import os
import threading
from dotenv import load_dotenv

from scraper.pipeline.groq_extractor import extract_tools_with_ai, fetch_markdown_via_jina

load_dotenv()

# ── All repos to scrape ───────────────────────────────────────────────────────
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


def _load_api_keys() -> list:
    """
    Load all configured Groq API keys from .env.
    Returns a list — always at least 1 key.
    """
    keys = []
    # Primary key
    k1 = os.environ.get("GROQ_API_KEY", "")
    if k1 and k1 != "your_groq_api_key_here":
        keys.append(k1)
    # Optional extra keys
    for i in range(2, 6):   # supports up to 5 keys
        k = os.environ.get(f"GROQ_API_KEY_{i}", "")
        if k and k != "your_groq_api_key_here":
            keys.append(k)

    if not keys:
        raise ValueError(
            "\nNo GROQ_API_KEY found in .env\n"
            "Get a free key at https://console.groq.com\n"
        )

    print(f"  Using {len(keys)} Groq API key{'s' if len(keys) > 1 else ''} in parallel")
    return keys


def _scrape_batch(urls: list, api_key: str, results: list, lock: threading.Lock, worker_id: int):
    """
    Worker function — scrapes a list of URLs using one specific API key.
    Appends results to the shared `results` list (thread-safe via lock).
    """
    for url in urls:
        print(f"\n  [Worker {worker_id}] GitHub → {url}")

        markdown = fetch_markdown_via_jina(url)
        if not markdown:
            print(f"    [Skip] No content returned from Jina")
            continue

        tools = extract_tools_with_ai(markdown, source_hint=url, api_key=api_key)

        with lock:
            results.extend(tools)
            print(f"    [Worker {worker_id}] Running total: {len(results)}")


def scrape_github() -> list:
    """
    Scrape all GitHub repos in parallel across available API keys.

    With 1 key:  repos run sequentially   (~2-3 hours for all 8)
    With 2 keys: repos split 4+4 parallel (~1-1.5 hours)
    With 3 keys: repos split 3+3+2 parallel (~45-60 min)
    """
    api_keys   = _load_api_keys()
    num_workers = len(api_keys)

    # Split repos evenly across workers
    # e.g. 8 repos + 2 keys → [[url1,url2,url3,url4], [url5,url6,url7,url8]]
    batches = [[] for _ in range(num_workers)]
    for i, url in enumerate(GITHUB_URLS):
        batches[i % num_workers].append(url)

    print(f"\n  Splitting {len(GITHUB_URLS)} repos across {num_workers} worker(s):")
    for i, batch in enumerate(batches):
        print(f"    Worker {i+1} (key {i+1}): {len(batch)} repos")

    # Shared results list + lock for thread safety
    all_tools = []
    lock      = threading.Lock()
    threads   = []

    # Launch one thread per worker
    for i, (batch, key) in enumerate(zip(batches, api_keys)):
        t = threading.Thread(
            target=_scrape_batch,
            args=(batch, key, all_tools, lock, i + 1),
            daemon=True
        )
        threads.append(t)
        t.start()

    # Wait for all workers to finish
    for t in threads:
        t.join()

    print(f"\n  GitHub scraper done — {len(all_tools)} tools collected")
    return all_tools