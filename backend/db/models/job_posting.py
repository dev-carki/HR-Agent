from pydantic import BaseModel

from backend.db.base import BaseResponse


class JobPostingBase(BaseModel):
    company_id: int
    title: str
    required_skills: list[str]
    jd_text: str


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingResponse(JobPostingBase, BaseResponse):
    pass
