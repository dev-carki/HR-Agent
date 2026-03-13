from pydantic import BaseModel

from backend.db.base import BaseResponse


class CompanyBase(BaseModel):
    name: str
    address: str


class CompanyCreate(CompanyBase):
    pass


class CompanyResponse(CompanyBase, BaseResponse):
    pass
