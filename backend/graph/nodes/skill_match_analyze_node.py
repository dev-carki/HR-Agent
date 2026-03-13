import re

from backend.graph.state import GraphState
from backend.llm.openai import OpenAILLM
from backend.prompts.skill_match import SKILL_MATCH_SYSTEM_PROMPT


def _normalize(skill: str) -> str:
    """하이픈·공백·언더스코어 제거 후 소문자 변환"""
    return re.sub(r"[-_\s]", "", skill).lower()


def skill_match_analyze_node(state: GraphState) -> dict:
    applicant_skills_list = state["resume_data"]["skills"]
    company_required_skills = state["company_info"]["required_skills"]

    content = f"""
    지원자 보유 기술: {applicant_skills_list}
    회사 요구 기술: {company_required_skills}
    """

    llm = OpenAILLM()
    skill_match_result = llm.chat_json(content=content, system_prompt=SKILL_MATCH_SYSTEM_PROMPT)

    # ── 후처리: LLM 결과의 이름 불일치 보정 ──────────────────────────────────────
    # required_skills 정규화 맵 {정규화값: 원본 이름}
    normalized_required = {_normalize(s): s for s in company_required_skills}

    # LLM이 matched라고 판단한 기술들의 정규화 집합
    normalized_matched = {_normalize(s) for s in skill_match_result.get("matched_skills", [])}

    # matched_skills: required_skills 원본 이름으로 교체
    matched = [normalized_required[n] for n in normalized_matched if n in normalized_required]

    # missing_skills: required_skills 중 매칭되지 않은 것만 (원본 이름 사용)
    missing = [s for s in company_required_skills if _normalize(s) not in normalized_matched]

    skill_match_result["matched_skills"] = matched
    skill_match_result["missing_skills"] = missing

    return {
        "skill_match_result": skill_match_result
    }
