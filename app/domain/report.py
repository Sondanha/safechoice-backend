from pydantic import BaseModel
from app.domain.feature import Feature

class Report(BaseModel):
    session_id: str
    score: float
    feature: Feature
    summary: str
