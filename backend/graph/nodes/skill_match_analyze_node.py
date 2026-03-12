from backend.graph.state import GraphState
from backend.llm.openai import OpenAILLM
from backend.prompts.skill_match import SKILL_MATCH_SYSTEM_PROMPT

def skill_match_analyze_node(state: GraphState) -> dict:
    applicant_skills_list = state["resume_data"]["skills"]
    company_required_skills = state["company_info"]["required_skills"]
    
    content = f"""
    지원자 보유 기술: {applicant_skills_list}
    회사 요구 기술: {company_required_skills}
    """
    
    llm = OpenAILLM()
    skill_match_result = llm.chat_json(content=content, system_prompt=SKILL_MATCH_SYSTEM_PROMPT)
    
    
    return {
        "skill_match_result": skill_match_result
    }