from fastapi import APIRouter, HTTPException
from models.schemas import RecommendRequest, RecommendResponse, Tool
from utils.supabase_client import fetch_all_tools
from recommender.ai_engine import recommend as recommend_engine

router = APIRouter(prefix="/api", tags=["recommend"])

@router.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    try:
        tools = fetch_all_tools()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    result = recommend_engine(req.query, tools, req.limit)

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
