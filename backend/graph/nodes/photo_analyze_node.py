from backend.graph.state import GraphState
from backend.llm.openai import OpenAILLM
from backend.prompts.photo import PHOTO_ANALYZE_SYSTEM_PROMPT

def photo_analyze_node(state: GraphState) -> dict:
    photo_path = state["photo_path"]
    
    if not photo_path:
        return {
            "photo_result": {
                "has_photo": False
            }
        }
        
    llm = OpenAILLM()
    photo_result = llm.chat_vision(image_path=state["photo_path"], system_prompt=PHOTO_ANALYZE_SYSTEM_PROMPT)
    photo_result["has_photo"] = True
    
    return {"photo_result": photo_result}