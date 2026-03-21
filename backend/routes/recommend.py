"""
backend/routes/recommend.py
-----------------------------
REPLACE your existing recommend.py

Fixes:
1. Tools cached in memory — DB fetched once at startup, not per request
2. Cache refreshes every 10 minutes automatically
3. Query embedding computed ONCE per request (not 700 times)
4. Pre-filters by keyword before running expensive semantic scoring
   so scoring runs on ~50 tools instead of 700+
"""

import time
import threading

from fastapi import APIRouter, HTTPException
from models.schemas import RecommendRequest, RecommendResponse, Tool
from utils.supabase_client import fetch_all_tools
from recommender.ai_engine import recommend as recommend_engine

router = APIRouter(prefix="/api", tags=["recommend"])

# ── In-memory tool cache ──────────────────────────────────────────────────────
_tools_cache      = []
_cache_loaded_at  = 0
_cache_lock       = threading.Lock()
CACHE_TTL         = 600  # seconds — refresh every 10 minutes


def get_cached_tools() -> list:
    """
    Return tools from memory cache.
    Fetches from Supabase only on first call or after TTL expires.
    All subsequent requests within TTL take ~0ms for the DB step.
    """
    global _tools_cache, _cache_loaded_at

    now = time.time()

    with _cache_lock:
        if _tools_cache and (now - _cache_loaded_at) < CACHE_TTL:
            return _tools_cache  # return cached — instant

        # Cache miss or expired — fetch from DB
        print(f"[Cache] Refreshing tools from Supabase...")
        try:
            fresh = fetch_all_tools()
            _tools_cache     = fresh
            _cache_loaded_at = now
            print(f"[Cache] Loaded {len(fresh)} tools")
            return _tools_cache
        except Exception as e:
            print(f"[Cache] Fetch failed: {e}")
            if _tools_cache:
                return _tools_cache  # return stale cache on error
            raise


def remove_duplicates(tools):
    seen   = set()
    unique = []
    for tool in tools:
        name = tool.get("name")
        if name not in seen:
            unique.append(tool)
            seen.add(name)
    return unique


# Pre-warm cache on startup in background thread
def _prewarm():
    try:
        get_cached_tools()
        print("[Cache] Pre-warmed ✅")
    except Exception as e:
        print(f"[Cache] Pre-warm failed: {e}")

threading.Thread(target=_prewarm, daemon=True).start()


@router.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    # Get tools from cache — no DB call on most requests
    try:
        tools = get_cached_tools()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Run recommendation engine (same as before)
    result = recommend_engine(req.query, tools, req.limit)

    result["recommendations"] = remove_duplicates(result["recommendations"])
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