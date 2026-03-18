from backend.graph.state import GraphState
from backend.llm.openai import OpenAILLM
from backend.prompts.personal_info import PERSONAL_INFO_ANALYZE_SYSTEM_PROMPT
from backend.tools.geocoding import get_distance_info


def personal_info_analyze_node(state: GraphState) -> dict:
    content = state["raw_pdf_text"]
    company_address = state["company_info"]["address"]

    llm = OpenAILLM()
    personal_info_result = llm.chat_json(content=content, system_prompt=PERSONAL_INFO_ANALYZE_SYSTEM_PROMPT)

    # 지원자 주소가 있으면 회사 주소와 거리 계산
    candidate_address = personal_info_result.get("location", "")
    if candidate_address and company_address:
        personal_info_result["distance_info"] = get_distance_info(candidate_address, company_address)
    else:
        personal_info_result["distance_info"] = None

    return {"personal_info_result": personal_info_result}
