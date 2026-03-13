from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# ── Additional directory sources ─────────────────────────────────────────────
DIRECTORY_SOURCES = [
    {
        "name": "aitoptools",
        "url": "https://aitoptools.com",
        "card_selector": "a[href*='/tool/']",
        "name_tags": ["h2", "h3", "h4"],
    },
    {
        "name": "aitoolsdirectory",
        "url": "https://aitoolsdirectory.com",
        "card_selector": "a[href*='/tools/']",
        "name_tags": ["h2", "h3", "h4"],
    },
    {
        "name": "topai.tools",
        "url": "https://topai.tools",
        "card_selector": "a[href*='/t/']",
        "name_tags": ["h2", "h3", "h4", "strong"],
    },
    {
        "name": "insidr.ai",
        "url": "https://www.insidr.ai/ai-tools/",
        "card_selector": "a[href*='/ai-tools/']",
        "name_tags": ["h2", "h3", "h4"],
    },
]


def _scrape_directory(page, source):
    """Generic scraper for AI tool directory sites."""
    tools = []
    url = source["url"]
    name_tags = source["name_tags"]

    try:
        print(f"  Loading {source['name']} ...")
        page.goto(url, timeout=60000)

        # Scroll to load lazy content
        for _ in range(6):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1500)

        html = page.content()
    except Exception as e:
        print(f"  [WARN] Failed to load {url}: {e}")
        return tools

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(source["card_selector"])

    if not cards:
        # Broad fallback
        cards = soup.select("article") or soup.select(".tool-card") or soup.select(".card")

    seen = set()
    for card in cards:
        name_tag = card.find(name_tags)
        if not name_tag:
            # Try any heading
            name_tag = card.find(["h2", "h3", "h4", "strong"])
        if not name_tag:
            continue

        name = name_tag.get_text(strip=True)
        if not name or name in seen or len(name) < 3:
            continue
        seen.add(name)

        desc_tag = card.find("p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        href = card.get("href", "")
        if href.startswith("/"):
            from urllib.parse import urlparse
            base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
            website = base + href
        elif href.startswith("http"):
            website = href
        else:
            website = url

        # Try to extract category from badge/tag element
        category_tag = card.find(class_=lambda c: c and any(
            k in c.lower() for k in ["category", "tag", "badge", "label", "chip"]
        ))
        category = category_tag.get_text(strip=True) if category_tag else "Other"

        tools.append({
            "name": name,
            "description": description,
            "category": category,
            "website": website,
        })

    print(f"  [{source['name']}] → {len(tools)} tools")
    return tools


def scrape_directories():
    """Scrape all configured AI tool directory sites."""
    all_tools = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for source in DIRECTORY_SOURCES:
            tools = _scrape_directory(page, source)
            all_tools.extend(tools)

        browser.close()

    print(f"Directories total (pre-dedup): {len(all_tools)}")
    return all_tools