from fastapi import APIRouter, HTTPException
from models.schemas import RecommendRequest, RecommendResponse, Tool
from utils.supabase_client import fetch_all_tools
from recommender.ai_engine import recommend as recommend_engine

router = APIRouter(prefix="/api", tags=["recommend"])


def remove_duplicates(tools):

    seen = set()
    unique = []

    for tool in tools:
        name = tool.get("name")

        if name not in seen:
            unique.append(tool)
            seen.add(name)

    return unique


@router.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):

    # Fetch tools from database
    try:
        tools = fetch_all_tools()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Run recommendation engine
    result = recommend_engine(req.query, tools, req.limit)

    # Remove duplicate tools
    result["recommendations"] = remove_duplicates(result["recommendations"])

    # Sort by popularity
    result["recommendations"] = sorted(
        result["recommendations"],
        key=lambda x: x.get("popularity", 0),
        reverse=True
    )

    normalized_tools = []

    for t in result["recommendations"]:
        normalized_tools.append(
            Tool(
                id=str(t.get("id")) if t.get("id") else None,
                name=t.get("name", ""),
                description=t.get("description", ""),
                category=t.get("category", ""),
                tags=t.get("tags") or [],
                url=t.get("url") or t.get("website"),
                rating=t.get("rating"),
                pricing=t.get("pricing"),
                trending=t.get("trending", False),
                popularity=t.get("popularity", 0),
                reviews=t.get("reviews", []),
            )
        )

    return RecommendResponse(
        recommendations=normalized_tools,
        detected_category=result.get("detected_category"),
        suggested_categories=result.get("suggested_categories", [])
    )