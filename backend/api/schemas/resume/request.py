from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    company_name: str
    company_address: str
    required_skills: list[str]
    jd_text: str
