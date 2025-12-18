from pydantic import BaseModel
from typing import List

class CategoryCount(BaseModel):
    category: str
    count: int

class ProfilingSummary(BaseModel):
    total_records: int
    breakdown: List[CategoryCount]
