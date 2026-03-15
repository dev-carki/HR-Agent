from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.orm.analysis_result import AnalysisResult
from backend.api.schemas.analysis.response import AnalysisResultSummary
from backend.api.schemas.common.wrapper import BaseResponseWrapper
from backend.services.database import get_db

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

@router.get("/results", response_model=BaseResponseWrapper[list[AnalysisResultSummary]])
async def get_all_analyze_datas(db: AsyncSession = Depends(get_db)):
    stmt = select(AnalysisResult).order_by(AnalysisResult.created_at.desc()) # stmt = statement / query, stmt로 사용 가능
    
    result = await db.execute(stmt)
    
    rows = result.scalars().all()
    
    items = [
        AnalysisResultSummary(
            id=data.id,
            candidate_name=data.final_report["candidate_name"],
            overall_score=data.overall_score,
            recommendation=data.recommendation,
            created_at=data.created_at,
        )
        for data in rows
    ]
    
    return BaseResponseWrapper(
        code=200,
        message="전체 이력서 분석 내역 조회 성공",
        data=items
    )

@router.get("/results/{id}", response_model=BaseResponseWrapper[AnalysisResultSummary])
async def get_analyze_data_with_id(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(AnalysisResult).where(AnalysisResult.id == id)
    
    result = await db.execute(stmt)
    
    row = result.scalar_one_or_none()
    
    if row is None:
        raise HTTPException(status_code=404, detail="분석 결과를 찾을 수 없습니다.")
    
    data = AnalysisResultSummary(
        id=row.id,
        candidate_name=row.final_report["candidate_name"],
        overall_score=row.overall_score,
        recommendation=row.recommendation,
        created_at=row.created_at,
    )
    
    return BaseResponseWrapper(
        code=200,
        message="특정 이력서 분석 내역 조회 성공",
        data=data
    )