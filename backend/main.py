from fastapi import FastAPI

from backend.api.routes.resume import router as resume_router
from backend.api.routes.analysis import router as analysis_router
from backend.api.routes.images import router as image_router
from backend.services.database import Base, engine
from backend.api.middleware.exception_handler import global_exception_hanlder

import backend.db.orm.company  # noqa: F401
import backend.db.orm.job_posting 
import backend.db.orm.candidate
import backend.db.orm.analysis_result

app = FastAPI(
    title="HR Agent API Server",
    description="지원자의 이력서가 회사에 Fit한 인재인지 판단하는 AI Agentic Workflow API 서버 입니다.",
    version="0.0.1",
)

app.include_router(resume_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(image_router, prefix="/api/v1")
app.add_exception_handler(Exception, global_exception_hanlder)


@app.on_event("startup")
async def startup():
    import asyncio
    for attempt in range(5):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            break
        except Exception as e:
            if attempt == 4:
                raise
            print(f"DB 연결 대기 중... ({attempt + 1}/5)")
            await asyncio.sleep(3)
