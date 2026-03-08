from typing import List, Dict, Any
from intent.category_intent import detect_category_intent
from recommender.semantic import semantic_score
from utils.keyword import keyword_score


def recommend(query: str, tools: List[Dict[str, Any]], limit: int = 5):

    if not query.strip():
        return {
            "detected_category": None,
            "suggested_categories": [],
            "recommendations": []
        }

    # Detect category
    detected_category = detect_category_intent(query)

    scored = []
    category_scores = {}

    for tool in tools:

        # Semantic similarity
        sem = semantic_score(query, tool)

        # Keyword similarity
        kw = keyword_score(query, tool)

        score = (0.7 * sem) + (0.3 * kw)

        # Category boost
        if detected_category and detected_category.lower() in (tool.get("category") or "").lower():
            score += 0.15

        scored.append((score, tool))

        # Aggregate category scores
        cat = tool.get("category")
        if cat:
            category_scores[cat] = category_scores.get(cat, 0) + score

    # Sort tools by score
    scored.sort(key=lambda x: x[0], reverse=True)

    # 🔹 Relevance threshold
    THRESHOLD = 0.45

    recommendations = [
        t for score, t in scored if score >= THRESHOLD
    ]

    # 🔹 Fallback if nothing passes threshold
    if not recommendations:
        recommendations = [t for _, t in scored[:limit]]
    else:
        recommendations = recommendations[:limit]

    # Suggested categories
    suggested_categories = sorted(
        category_scores,
        key=lambda c: category_scores[c],
        reverse=True
    )[:3]

    return {
        "detected_category": detected_category,
        "suggested_categories": suggested_categories,
        "recommendations": recommendations
    }