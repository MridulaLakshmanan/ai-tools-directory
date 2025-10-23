from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import RecommendRequest, RecommendResponse, Tool
from utils.supabase_client import fetch_all_tools
from utils.ai_engine import recommend as recommend_engine

router = APIRouter(prefix='/api', tags=['recommend'])

@router.post('/recommend', response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    try:
        tools = fetch_all_tools()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    top = recommend_engine(req.query, tools, req.limit)
    normalized = []
    for t in top:
        normalized.append(Tool(
            id=str(t.get('id')) if t.get('id') else None,
            name=t.get('name',''),
            description=t.get('description',''),
            category=t.get('category',''),
            tags=t.get('tags') if t.get('tags') else [],
            url=t.get('url') or t.get('website'),
            rating=t.get('rating'),
            pricing=t.get('pricing'),
            trending=t.get('trending', False),
            popularity=t.get('popularity', 0),
            reviews=t.get('reviews', [])
        ))
    return RecommendResponse(recommendations=normalized)
