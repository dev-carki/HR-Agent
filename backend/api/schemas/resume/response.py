from pydantic import BaseModel


class ScoresResponse(BaseModel):
    skill_match: int
    career: int
    self_introduction: int


class AnalyzeResponse(BaseModel):
    overall_score: int
    final_report: dict
    skill_match_result: dict
    career_result: dict
    self_intro_result: dict
    personal_info_result: dict
    photo_result: dict
