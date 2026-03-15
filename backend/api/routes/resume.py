import os
import shutil
import uuid

from fastapi import APIRouter, Depends, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.common.wrapper import BaseResponseWrapper
from backend.api.schemas.resume.request import AnalyzeRequest
from backend.api.schemas.resume.response import AnalyzeResponse
from backend.db.orm.analysis_result import AnalysisResult
from backend.db.orm.candidate import Candidate
from backend.db.orm.company import Company
from backend.db.orm.job_posting import JobPosting
from backend.graph.workflow import build_graph
from backend.services.database import get_db

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
    db: AsyncSession = Depends(get_db),
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

    # ── DB 저장 ─────────────────────────────────────────────────────────────
    final_report = result["final_report"]
    personal_info = result["personal_info_result"] or {}
    skill_match = result["skill_match_result"] or {}
    career = result["career_result"] or {}
    self_intro = result["self_intro_result"] or {}

    # Company insert
    company = Company(name=company_name, address=company_address)
    db.add(company)
    await db.flush()  # company.id 확보

    # JobPosting insert
    job_posting = JobPosting(
        company_id=company.id,
        title=final_report.get("applied_position", company_name),
        required_skills=required_skills,
        jd_text=jd_text,
    )
    db.add(job_posting)
    await db.flush()  # job_posting.id 확보

    # Candidate insert
    candidate = Candidate(
        name=final_report.get("candidate_name", ""),
        email=personal_info.get("email", ""),
        phone=personal_info.get("phone", ""),
        resume_path=temp_path,
        photo_path=result.get("photo_path"),
    )
    db.add(candidate)
    await db.flush()  # candidate.id 확보

    # AnalysisResult insert
    analysis = AnalysisResult(
        candidate_id=candidate.id,
        job_posting_id=job_posting.id,
        skill_score=skill_match.get("score"),
        career_score=career.get("score"),
        self_intro_score=self_intro.get("score"),
        overall_score=result["overall_score"],
        recommendation=final_report.get("recommendation"),
        final_report=final_report,
        skill_match_result=result["skill_match_result"],
        career_result=result["career_result"],
        self_intro_result=result["self_intro_result"],
        personal_info_result=result["personal_info_result"],
        photo_result=result["photo_result"],
    )
    db.add(analysis)
    await db.commit()
    # ────────────────────────────────────────────────────────────────────────

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
