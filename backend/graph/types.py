from typing_extensions import TypedDict


# ── LangGraph 노드 간 공유 타입 ──────────────────────────────────────────────────

class CompanyInfo(TypedDict):
    name: str
    address: str
    required_skills: list[str]
    jd_text: str


class ResumeData(TypedDict):
    name: str
    email: str
    phone: str
    github_url: str
    skills: list[str]
    career_history: str
    self_introduction: str