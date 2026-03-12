from backend.graph.state import GraphState
from backend.llm.openai import OpenAILLM
from backend.prompts.personal_info import PERSONAL_INFO_ANALYZE_SYSTEM_PROMPT

def personal_info_analyze_node(state: GraphState) -> dict:
    content = state["raw_pdf_text"]
    
    llm = OpenAILLM()
    personal_info_result = llm.chat_json(content=content, system_prompt=PERSONAL_INFO_ANALYZE_SYSTEM_PROMPT)
    
    return {"personal_info_result": personal_info_result}