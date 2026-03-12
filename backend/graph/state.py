from typing_extensions import TypedDict

from backend.models.graph_types import CompanyInfo, ResumeData

class GraphState(TypedDict):
    # ── Layer 1 - Input (워크플로우 시작 시 주입) ────────────────────────────────────────
    pdf_path: str
    company_info: CompanyInfo
    
    # ── Layer 2 - Parsed Resume (Parser 노드가 채움) ───────────────────────────────────
    resume_data: ResumeData | None
    photo_path: str | None
    
    # ── Layer 3 - Agent Results (각 병렬 에이전트가 채움) ─────────────────────────────────
    photo_result: dict | None
    personal_info_result: dict | None
    skill_match_result: dict | None
    self_intro_result: dict | None
    career_result: dict | None
    
    # ── Layer 4 - Final (Aggregator가 채움) ───────────────────────────────────────────
    final_report: dict | None
    overall_score: float | None