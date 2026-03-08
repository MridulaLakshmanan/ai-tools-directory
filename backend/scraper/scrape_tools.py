import requests
from bs4 import BeautifulSoup
from utils.supabase_client import get_client

supabase = get_client()

URL = "https://github.com/mahseema/awesome-ai-tools"


INVALID_CATEGORIES = [
    "Text",
    "Editor's Choice"
]


def clean_text(text):
    return text.strip().replace("\n", " ").replace("  ", " ")


def scrape_tools():

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    article = soup.select_one("article")

    tools = []
    current_category = None

    for element in article.find_all(["h2", "li"]):

        # Detect section category
        if element.name == "h2":

            header = clean_text(element.text)

            if header not in INVALID_CATEGORIES:
                current_category = header

        # Extract tool entries
        elif element.name == "li":

            if not current_category:
                continue

            link = element.find("a")

            if not link:
                continue

            name = clean_text(link.text)
            website = link.get("href")

            text = clean_text(element.text)

            description = text.replace(name, "").replace("-", "").strip()

            if len(name) < 3 or len(name) > 60:
                continue

            tool = {
                "name": name,
                "description": description,
                "category": current_category,
                "tags": ["ai"],
                "website": website,
                "approved": True
            }

            tools.append(tool)

    # Limit scrape size
    tools = tools[:200]

    return tools


def insert_tools(tools):

    for tool in tools:

        try:

            existing = supabase.table("ai_tools") \
                .select("name") \
                .eq("name", tool["name"]) \
                .execute()

            if existing.data:
                continue

            supabase.table("ai_tools").insert(tool).execute()

            print("Inserted:", tool["name"])

        except Exception as e:
            print("Insert failed:", e)


if __name__ == "__main__":

    tools = scrape_tools()

    print("Scraped", len(tools), "tools")

    insert_tools(tools)

    print("Finished inserting tools")