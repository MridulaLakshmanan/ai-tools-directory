from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# ── All GitHub awesome-list URLs to scrape ──────────────────────────────────
GITHUB_URLS = [
    # Original source
    "https://github.com/mahseema/awesome-ai-tools",
    # Additional high-quality awesome lists
    "https://github.com/ai-for-developers/awesome-ai-coding-tools",
    "https://github.com/steven2358/awesome-generative-ai",
    "https://github.com/e2b-dev/awesome-ai-agents",
    "https://github.com/Hannibal046/Awesome-LLM",
    "https://github.com/awesome-selfhosted/awesome-selfhosted",  # has AI section
    "https://github.com/eugeneyan/applied-ml",
]

INVALID_CATEGORIES = [
    "Text",
    "Editor's Choice",
    "Contents",
    "Table of Contents",
    "Contributing",
    "License",
    "Acknowledgements",
]

# Noise patterns that indicate a section header, not a tool
NOISE_STARTS = (
    "🌟", "📝", "👩", "🖼", "📽", "🎙", "🎨",
    "➡", "⬆", "🔝", "📌", "🗂", "💡", "📋"
)


def clean_text(text):
    return text.strip().replace("\n", " ").replace("  ", " ")


def is_valid_tool(name, description):
    if not name:
        return False
    if name.startswith(NOISE_STARTS):
        return False
    if len(name) < 3:
        return False
    # skip pure anchor/nav links
    if name.lower() in ("back to top", "contents", "table of contents", "contributing", "license"):
        return False
    # category titles with "AI" and ≤2 words are usually headings
    if "AI" in name and len(name.split()) <= 2:
        return False
    return True


def _scrape_single_github(page, url):
    """Scrape one GitHub awesome-list URL and return list of tool dicts."""
    tools = []
    current_category = None

    try:
        page.goto(url, timeout=30000)
        page.wait_for_timeout(2000)
        html = page.content()
    except Exception as e:
        print(f"  [WARN] Failed to load {url}: {e}")
        return tools

    soup = BeautifulSoup(html, "html.parser")
    article = soup.select_one("article")
    if article is None:
        return tools

    for element in article.find_all(["h2", "h3", "li"]):
        if element.name in ("h2", "h3"):
            header = clean_text(element.get_text())
            if header not in INVALID_CATEGORIES and len(header) > 2:
                current_category = header

        elif element.name == "li":
            link = element.find("a")
            if not link:
                continue

            name = clean_text(link.get_text())
            website = link.get("href", "")

            # Skip internal GitHub anchor links
            if not website or website.startswith("#"):
                continue

            text = clean_text(element.get_text())
            description = text.replace(name, "").lstrip(" -–—").strip()

            if not is_valid_tool(name, description):
                continue

            tools.append({
                "name": name,
                "description": description,
                "category": current_category or "Other",
                "website": website,
            })

    print(f"  [OK] {url}  →  {len(tools)} tools")
    return tools


def scrape_github():
    """Scrape all configured GitHub awesome-list URLs."""
    all_tools = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in GITHUB_URLS:
            print(f"Scraping: {url}")
            tools = _scrape_single_github(page, url)
            all_tools.extend(tools)

        browser.close()

    print(f"GitHub total (pre-dedup): {len(all_tools)}")
    return all_tools