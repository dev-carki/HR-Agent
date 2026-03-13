import os
import shutil
import uuid

from fastapi import APIRouter, Form, UploadFile

from backend.api.schemas.common.wrapper import BaseResponseWrapper
from backend.api.schemas.resume.request import AnalyzeRequest
from backend.api.schemas.resume.response import AnalyzeResponse
from backend.graph.workflow import build_graph

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)

graph = build_graph()


@router.post("/analyze", response_model=BaseResponseWrapper[AnalyzeResponse])
async def analyze(
    file: UploadFile,
    company_name: str = Form(...),
    company_address: str = Form(...),
    required_skills: list[str] = Form(...),
    jd_text: str = Form(...),
):
    # PDF 임시 저장
    temp_path = f"uploads/temp/{uuid.uuid4()}_{file.filename}"
    os.makedirs("uploads/temp", exist_ok=True)
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    initial_state = {
        "pdf_path": temp_path,
        "company_info": {
            "name": company_name,
            "address": company_address,
            "required_skills": required_skills,
            "jd_text": jd_text,
        },
        "raw_pdf_text": None,
        "resume_data": None,
        "photo_path": None,
        "photo_result": None,
        "personal_info_result": None,
        "skill_match_result": None,
        "self_intro_result": None,
        "career_result": None,
        "final_report": None,
        "overall_score": None,
    }

    result = graph.invoke(initial_state)

    return BaseResponseWrapper(
        code=200,
        message="분석 완료",
        data=AnalyzeResponse(
            overall_score=result["overall_score"],
            final_report=result["final_report"],
            skill_match_result=result["skill_match_result"],
            career_result=result["career_result"],
            self_intro_result=result["self_intro_result"],
            personal_info_result=result["personal_info_result"],
            photo_result=result["photo_result"],
        ),
    )
