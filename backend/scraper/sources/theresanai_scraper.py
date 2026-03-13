from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://theresanai.com"


def scrape_theresanai():
    """
    Scrapes theresanai.com — one of the largest AI tool directories.
    Scrolls to load all lazy-loaded tool cards, then extracts name,
    description, category, and website URL for each tool.
    """
    tools = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Loading theresanai.com ...")
        page.goto(URL, timeout=60000)

        # Scroll down repeatedly to trigger lazy loading
        for _ in range(10):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1500)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # theresanai.com uses cards — try multiple selectors
    # Primary: anchor tags wrapping tool cards
    cards = soup.select("a[href*='/tool/']") or soup.select("a[href*='/ai/']")

    if not cards:
        # Fallback: any article or div with a link and heading
        cards = soup.select("article") or soup.select(".tool-card")

    print(f"  Found {len(cards)} raw cards on theresanai.com")

    seen = set()
    for card in cards:
        # Name — look for h2, h3, or strong inside the card
        name_tag = card.find(["h2", "h3", "h4", "strong"])
        if not name_tag:
            continue
        name = name_tag.get_text(strip=True)
        if not name or name in seen or len(name) < 3:
            continue
        seen.add(name)

        # Description
        desc_tag = card.find("p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        # Website URL
        href = card.get("href", "")
        if href.startswith("/"):
            website = URL + href
        elif href.startswith("http"):
            website = href
        else:
            website = URL

        # Category — look for a tag/badge element
        category_tag = card.find(class_=lambda c: c and any(
            k in c.lower() for k in ["category", "tag", "badge", "label"]
        ))
        category = category_tag.get_text(strip=True) if category_tag else "Other"

        tools.append({
            "name": name,
            "description": description,
            "category": category,
            "website": website,
        })

    print(f"  Extracted {len(tools)} tools from theresanai.com")
    return tools