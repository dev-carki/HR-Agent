from pydantic import BaseModel

from backend.db.base import BaseResponse


class AnalysisResultBase(BaseModel):
    candidate_id: int
    job_id: int
    skill_score: float
    career_score: float
    self_intro_score: float
    overall_score: float
    report: str


class AnalysisResultCreate(AnalysisResultBase):
    pass


class AnalysisResultResponse(AnalysisResultBase, BaseResponse):
    pass
