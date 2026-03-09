from scraper.sources.github_scraper import scrape_github
from scraper.sources.futurepedia_scraper import scrape_futurepedia

from scraper.pipeline.normalize import normalize_tool
from scraper.pipeline.deduplicate import remove_duplicates

from utils.supabase_client import get_client

supabase = get_client()


def run():

    github_tools = scrape_github()
    futurepedia_tools = scrape_futurepedia()

    tools = github_tools + futurepedia_tools

    normalized = [normalize_tool(t) for t in tools]

    normalized = remove_duplicates(normalized)

    print("Total tools:", len(normalized))

    for tool in normalized:

        existing = supabase.table("ai_tools") \
            .select("name") \
            .eq("name", tool["name"]) \
            .execute()

        if existing.data:
            continue

        supabase.table("ai_tools").insert(tool).execute()

        print("Inserted:", tool["name"])


if __name__ == "__main__":
    run()