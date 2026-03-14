"""
backend/scraper/pipeline/normalize.py
----------------------------------------
REPLACE your existing file at: backend/scraper/pipeline/normalize.py

Shapes raw scraped tool dicts into the exact Supabase ai_tools schema.
"""

from scraper.pipeline.embedding import generate_embedding


def normalize_tool(tool: dict) -> dict:
    """
    Convert a raw scraped tool dict into a Supabase-ready dict.
    Safe — never crashes, always returns a valid dict.
    """
    name        = str(tool.get("name", "")).strip()
    description = str(tool.get("description", "")).strip()
    category    = str(tool.get("category", "Other")).strip() or "Other"
    website     = str(tool.get("website", "")).strip()
    url         = website

    # Build simple tags from category
    tags = ["ai"]
    if category and category.lower() != "other":
        tags.append(
            category.lower().replace(" ", "_").replace("&", "and")
        )

    # Generate embedding locally — free, runs offline
    embedding = None
    if description:
        try:
            embedding = generate_embedding(description)
        except Exception:
            embedding = None  # Column is nullable — safe to skip

    return {
        # Do NOT include 'id' — Supabase auto-generates it as UUID
        "name":        name,
        "description": description,
        "category":    category,
        "tags":        tags,
        "url":         url,
        "website":     website,
        "rating":      None,
        "pricing":     None,
        "embedding":   embedding,
        "approved":    True,
        "added_by":    "scraper",
    }