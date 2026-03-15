from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.sql import func

from backend.services.database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    skill_score = Column(Integer)
    career_score = Column(Integer)
    self_intro_score = Column(Integer)
    overall_score = Column(Integer)
    recommendation = Column(String(20))
    final_report = Column(JSON)
    skill_match_result = Column(JSON)
    career_result = Column(JSON)
    self_intro_result = Column(JSON)
    personal_info_result = Column(JSON)
    photo_result = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
