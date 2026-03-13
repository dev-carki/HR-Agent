from pydantic import BaseModel, EmailStr

from backend.db.base import BaseResponse
from common.types import PhoneNumber


class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneNumber
    resume_path: str


class CandidateCreate(CandidateBase):
    pass


class CandidateResponse(CandidateBase, BaseResponse):
    pass
