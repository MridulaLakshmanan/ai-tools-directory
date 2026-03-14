"""
backend/scraper/pipeline/normalize.py
----------------------------------------
REPLACE your existing normalize.py with this file.

Shapes raw scraped tool dicts into the exact Supabase ai_tools schema.

Supabase columns this writes to:
  name, description, category, tags, url, website,
  rating, pricing, embedding, approved, added_by

Does NOT include 'id' — Supabase auto-generates that as a UUID.
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

    # Both url and website columns store the same value
    url = website

    # Build simple tags from category — cheap, no AI needed
    tags = ["ai"]
    if category and category.lower() != "other":
        tags.append(
            category.lower().replace(" ", "_").replace("&", "and")
        )

    # Generate embedding locally using sentence-transformers (free, runs offline)
    embedding = None
    if description:
        try:
            embedding = generate_embedding(description)
        except Exception:
            embedding = None  # Column is nullable — safe to skip on error

    return {
        # NOTE: Do NOT include 'id' — Supabase auto-generates it
        "name":        name,
        "description": description,
        "category":    category,
        "tags":        tags,
        "url":         url,
        "website":     website,
        "rating":      None,      # Null at scrape time — can be filled later
        "pricing":     None,      # Null at scrape time — can be filled later
        "embedding":   embedding,
        "approved":    True,      # Auto-approve all scraped tools
        "added_by":    "scraper",
    }