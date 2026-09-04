from pydantic import BaseModel
from typing import Optional


class BrandCreate(BaseModel):
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    gaming_history: Optional[str] = None
    marketing_activity: Optional[str] = None


class BrandResponse(BrandCreate):
    id: int
    opportunity_score: Optional[float] = None

    class Config:
        from_attributes = True