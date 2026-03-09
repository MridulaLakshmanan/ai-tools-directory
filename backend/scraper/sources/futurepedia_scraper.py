from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://www.futurepedia.io/ai-tools"

def scrape_futurepedia():

    tools = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)

        page.wait_for_timeout(5000)

        html = page.content()

        browser.close()

    soup = BeautifulSoup(html,"html.parser")

    cards = soup.select("a[href*='/tool/']")

    for card in cards:

        name_tag = card.find("h3")

        if not name_tag:
            continue

        name = name_tag.text.strip()

        description_tag = card.find("p")
        description = description_tag.text.strip() if description_tag else ""

        website = "https://www.futurepedia.io" + card.get("href")

        tools.append({
            "name": name,
            "description": description,
            "category": "AI Tool",
            "website": website
        })

    return tools