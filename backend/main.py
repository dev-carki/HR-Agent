from fastapi import FastAPI

from backend.api.routes.resume import router as resume_router

app = FastAPI(
    title="HR Agent API Server",
    description="지원자의 이력서가 회사에 Fit한 인재인지 판단하는 AI Agentic Workflow API 서버 입니다.",
    version="0.0.1",
)

app.include_router(resume_router, prefix="/api/v1")
