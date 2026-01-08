from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendRequest(BaseModel):
    query: str = Field(...)
    limit: int = Field(5, ge=1, le=50)

class Tool(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str] = ""
    category: Optional[str] = ""
    tags: Optional[List[str]] = None
    url: Optional[str] = None
    rating: Optional[float] = None
    pricing: Optional[str] = None
    trending: Optional[bool] = False
    popularity: Optional[int] = 0
    reviews: Optional[List[dict]] = None

class RecommendResponse(BaseModel):
    recommendations: List[Tool]
    detected_category: Optional[str] = None
    suggested_categories: Optional[List[str]] = []
