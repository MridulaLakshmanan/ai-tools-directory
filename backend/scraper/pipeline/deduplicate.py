"""
backend/scraper/pipeline/deduplicate.py
------------------------------------------
REPLACE your existing file at: backend/scraper/pipeline/deduplicate.py
"""


def remove_duplicates(tools: list) -> list:
    """
    Remove tools with duplicate names (case-insensitive).
    Keeps the first occurrence. Skips tools with no name.
    """
    seen   = set()
    unique = []

    for tool in tools:
        name = str(tool.get("name", "")).strip().lower()
        if not name:
            continue
        if name not in seen:
            seen.add(name)
            unique.append(tool)

    return unique