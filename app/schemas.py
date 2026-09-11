from datetime import datetime

from pydantic import BaseModel, Field


class RecycleItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=50)
    weight_kg: float = Field(ge=0)
    points: int = Field(default=0, ge=0)


class RecycleItemOut(RecycleItemCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class StatsOut(BaseModel):
    total_items: int
    total_weight_kg: float
    total_points: int
