"""
backend/scraper/pipeline/embedding.py
----------------------------------------
NO CHANGE NEEDED — This is the same as your existing file.
Included here only for reference.

Generates 384-dim vector embeddings for tool descriptions.
Runs 100% locally using sentence-transformers — completely free.

Model: all-MiniLM-L6-v2
  - ~80MB one-time download
  - Fast inference
  - Matches your Supabase vector(384) column exactly
"""

from sentence_transformers import SentenceTransformer

# Load model once — reused across all tools in a single scrape run
_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print("  Loading embedding model (one-time ~80MB download)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("  Embedding model ready.")
    return _model


def generate_embedding(text: str):
    """
    Generate a 384-dimensional embedding vector.

    Args:
        text: Tool description or any string

    Returns:
        List of 384 floats, or None if text is empty
    """
    if not text or not text.strip():
        return None

    vector = _get_model().encode(text.strip())
    return vector.tolist()