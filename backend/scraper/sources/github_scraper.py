from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://github.com/mahseema/awesome-ai-tools"

INVALID_CATEGORIES = [
    "Text",
    "Editor's Choice"
]


def clean_text(text):
    return text.strip().replace("\n", " ").replace("  ", " ")


def is_valid_tool(name, description):
    """
    Filters out non-tool entries like section headings or noise
    """

    if not name:
        return False

    # remove emoji headings
    if name.startswith(("🌟", "📝", "👩", "🖼", "📽", "🎙", "🎨")):
        return False

    # too short = probably not a tool
    if len(name) < 3:
        return False

    # category titles often contain "AI"
    if "AI" in name and len(name.split()) <= 2:
        return False

    return True


def scrape_github():

    tools = []
    current_category = None

    # Launch Playwright browser
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)

        html = page.content()

        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    article = soup.select_one("article")

    if article is None:
        return tools

    for element in article.find_all(["h2", "li"]):

        # Detect category sections
        if element.name == "h2":

            header = clean_text(element.text)

            if header not in INVALID_CATEGORIES:
                current_category = header

        # Extract tools
        elif element.name == "li":

            link = element.find("a")

            if not link:
                continue

            name = clean_text(link.text)

            website = link.get("href")

            text = clean_text(element.text)

            description = text.replace(name, "").replace("-", "").strip()

            if not is_valid_tool(name, description):
                continue

            tool = {
                "name": name,
                "description": description,
                "category": current_category,
                "website": website
            }

            tools.append(tool)

    return tools