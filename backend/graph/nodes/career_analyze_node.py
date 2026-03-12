from backend.graph.state import GraphState
from backend.llm.openai import OpenAILLM
from backend.prompts.career import CAREER_ANALYZE_SYSTEM_PROMPT

def career_analyze_node(state: GraphState) -> dict:
    applicant_carrer = state["resume_data"]["career_history"]
    company_required_carrer = state["company_info"]["jd_text"] # 채용 공고 전문
    
    content = f"""
    지원자 경력 정보: {applicant_carrer}
    회사 요구 경력 정보: {company_required_carrer}
    """
    
    llm = OpenAILLM()
    career_result = llm.chat_json(content=content, system_prompt=CAREER_ANALYZE_SYSTEM_PROMPT)
    
    return {"career_result": career_result}