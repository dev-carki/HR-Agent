from backend.graph.state import GraphState
from backend.llm.openai import OpenAILLM
from backend.prompts.aggregator import AGGREGATOR_SYSTEM_PROMPT


def aggregator_node(state: GraphState) -> dict:
    skill_match_result = state["skill_match_result"]
    career_result = state["career_result"]
    self_intro_result = state["self_intro_result"]
    personal_info_result = state["personal_info_result"]
    photo_result = state["photo_result"]

    # overall_score: 가중 평균으로 코드에서 직접 계산 (career 45%, skill 40%, self_intro 15%)
    overall_score = round(
        skill_match_result["score"] * 0.4
        + career_result["score"] * 0.45
        + self_intro_result["score"] * 0.15
    )

    content = f"""
지원자 기술 분석 결과: {skill_match_result}
지원자 경력 분석 결과: {career_result}
지원자 자기소개서 분석 결과: {self_intro_result}
지원자 개인정보 분석 결과: {personal_info_result}
지원자 사진 분석 결과: {photo_result}
overall_score: {overall_score}
"""

    llm = OpenAILLM()
    final_report = llm.chat_json(content=content, system_prompt=AGGREGATOR_SYSTEM_PROMPT)

    # 점수는 코드에서 계산한 값으로 직접 추가
    final_report["scores"] = {
        "skill_match": skill_match_result["score"],
        "career": career_result["score"],
        "self_introduction": self_intro_result["score"],
    }
    final_report["overall_score"] = overall_score

    return {
        "final_report": final_report,
        "overall_score": overall_score,
    }
