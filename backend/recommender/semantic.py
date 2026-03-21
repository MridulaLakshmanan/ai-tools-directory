"""
backend/recommender/semantic.py
---------------------------------
REPLACE your existing semantic.py

Fixes:
1. semantic_score_batch() — encodes query ONCE then scores all tools
   Old code re-encoded the query for every single tool (700x redundant)
2. Batch encodes all tool texts together — much faster than one at a time
"""

import numpy as np
from embeddings.embedder import embed
from sklearn.metrics.pairwise import cosine_similarity


def semantic_score(query: str, tool: dict) -> float:
    """Single tool scoring — kept for backward compatibility."""
    q_emb = embed(query)
    t_emb = embed(
        f"{tool.get('name','')} {tool.get('description','')} {tool.get('category','')}"
    )
    return float(cosine_similarity([q_emb], [t_emb])[0][0])


def semantic_score_batch(query: str, tools: list) -> list:
    """
    Score multiple tools against a query.
    Encodes query ONCE and all tool texts in one batch.
    10-50x faster than calling semantic_score() in a loop.

    Args:
        query: Search query string
        tools: List of tool dicts

    Returns:
        List of similarity scores (same order as tools)
    """
    if not tools:
        return []

    from sentence_transformers import SentenceTransformer
    from embeddings.embedder import _model

    # Encode query once
    q_emb = embed(query)

    # Build tool texts
    tool_texts = [
        f"{t.get('name','')} {t.get('description','')} {t.get('category','')}"
        for t in tools
    ]

    # Batch encode all tools at once — far faster than one at a time
    try:
        t_embs = _model.encode(tool_texts, normalize_embeddings=True, batch_size=32)
    except Exception:
        # Fallback: score one at a time if batch fails
        return [semantic_score(query, t) for t in tools]

    # Compute all cosine similarities at once
    sims = cosine_similarity([q_emb], t_embs)[0]
    return sims.tolist()