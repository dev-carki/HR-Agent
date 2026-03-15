from datetime import datetime

from pydantic import BaseModel

class AnalysisResultSummary(BaseModel):
    id: int
    candidate_name: str
    overall_score: int
    recommendation: str
    created_at: datetime