"""
backend/scraper/pipeline/deduplicate.py
------------------------------------------
REPLACE your existing deduplicate.py with this file.

Removes duplicate tools by name (case-insensitive).
Also filters out tools with no name at all.
"""


def remove_duplicates(tools: list) -> list:
    """
    Keep only the first occurrence of each tool name.
    Case-insensitive comparison.

    Args:
        tools: List of tool dicts (normalized or raw)

    Returns:
        Deduplicated list — same order, first occurrence kept
    """
    seen   = set()
    unique = []

    for tool in tools:
        name = str(tool.get("name", "")).strip().lower()

        # Skip completely nameless tools
        if not name:
            continue

        if name not in seen:
            seen.add(name)
            unique.append(tool)

    return unique