from backend.graph.state import GraphState
from backend.llm.openai import OpenAILLM
from backend.prompts.self_intro import SELF_INTRO_ANALYZE_SYSTEM_PROMPT

def self_intro_analyze_node(state: GraphState) -> dict:
    applicant_intro_sentence = state["resume_data"]["self_introduction"]
    company_required_carrer = state["company_info"]["jd_text"] # 채용 공고 전문
    
    content = f"""
    지원자의 자기소개 문구: {applicant_intro_sentence}
    회사 채용 공고 정보: {company_required_carrer}
    """
    
    llm = OpenAILLM()
    self_intro_result = llm.chat_json(content=content, system_prompt=SELF_INTRO_ANALYZE_SYSTEM_PROMPT)
    
    return {"self_intro_result": self_intro_result}