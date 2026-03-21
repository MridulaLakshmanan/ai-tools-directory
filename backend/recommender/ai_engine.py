"""
backend/recommender/ai_engine.py
----------------------------------
REPLACE your existing ai_engine.py

Fixes:
1. Query embedding computed ONCE — not once per tool
2. Pre-filters to top 100 keyword matches before semantic scoring
   so cosine similarity runs on ~100 tools instead of 700+
3. Much faster overall — same quality results
"""

from typing import List, Dict, Any
from intent.category_intent import detect_category_intent
from recommender.semantic import semantic_score_batch
from utils.keyword import keyword_score


def recommend(query: str, tools: List[Dict[str, Any]], limit: int = 5):

    if not query.strip():
        return {
            "detected_category": None,
            "suggested_categories": [],
            "recommendations": []
        }

    # Detect category intent
    detected_category = detect_category_intent(query)

    query_lower = query.lower()

    # ── Step 1: Fast keyword pre-filter ──────────────────────────────────────
    # Score all tools by keyword match — very fast, no ML
    keyword_scored = []
    for tool in tools:
        kw = keyword_score(query, tool)
        # Category boost
        if detected_category and detected_category.lower() in (tool.get("category") or "").lower():
            kw += 0.2
        keyword_scored.append((kw, tool))

    keyword_scored.sort(key=lambda x: x[0], reverse=True)

    # Take top 100 by keyword — only run expensive semantic on these
    top_candidates = [t for _, t in keyword_scored[:100]]

    # ── Step 2: Semantic scoring on candidates only ───────────────────────────
    # Compute query embedding ONCE, score all candidates in one batch
    semantic_scores = semantic_score_batch(query, top_candidates)

    # ── Step 3: Combine scores ────────────────────────────────────────────────
    scored       = []
    cat_scores   = {}

    for tool, sem in zip(top_candidates, semantic_scores):
        kw    = keyword_score(query, tool)
        score = (0.7 * sem) + (0.3 * kw)

        if detected_category and detected_category.lower() in (tool.get("category") or "").lower():
            score += 0.15

        scored.append((score, tool))

        cat = tool.get("category")
        if cat:
            cat_scores[cat] = cat_scores.get(cat, 0) + score

    scored.sort(key=lambda x: x[0], reverse=True)

    # Relevance threshold
    THRESHOLD = 0.45
    recommendations = [t for score, t in scored if score >= THRESHOLD]

    if not recommendations:
        recommendations = [t for _, t in scored[:limit]]
    else:
        recommendations = recommendations[:limit]

    suggested_categories = sorted(
        cat_scores, key=lambda c: cat_scores[c], reverse=True
    )[:3]

    return {
        "detected_category":    detected_category,
        "suggested_categories": suggested_categories,
        "recommendations":      recommendations
    }