from pydantic import BaseModel, EmailStr

from backend.models.base import BaseResponse
from common.types import PhoneNumber

# ── Company ───────────────────────────────────────────────────────────────────
class CompanyBase(BaseModel):
    name: str
    address: str

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase, BaseResponse):
    pass


# ── JobPosting ─────────────────────────────────────────────────────────────────
class JobPostingBase(BaseModel):
    company_id: int
    title: str
    required_skills: list[str]
    jd_text: str
    
class JobPostingCreate(JobPostingBase):
    pass

class JobPostingResponse(JobPostingBase, BaseResponse):
    pass


# ── Candidate ───────────────────────────────────────────────────────────────────
class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneNumber
    resume_path: str

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase, BaseResponse):
    pass


# ── AnalysisResult ────────────────────────────────────────────────────────────────
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
