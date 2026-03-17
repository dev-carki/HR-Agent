# HR Agent

> LangGraph 기반 Multi-Agent Agentic Workflow로 구현한 AI 이력서 분석 시스템

PDF 이력서를 업로드하면 5개의 AI 에이전트가 **병렬로** 이력서를 분석하고, 채용 담당자에게 종합 리포트와 추천 등급을 제공합니다.

---

## 핵심 목표

단순한 LLM API 호출을 넘어 **Agentic Workflow 패턴을 직접 설계하고 구현**하는 것을 목표로 합니다.

- LangGraph **Fan-out / Fan-in** 패턴으로 다중 에이전트 병렬 실행
- LangChain **Tool Use + ReAct Agent** 패턴으로 GitHub 기여 이력 자율 수집
- FastAPI + MySQL + Streamlit + Docker + GCP 까지 **End-to-End 구현**

---

## 워크플로우

```
PDF 업로드
    │
    ▼
resume_parser ── PDF 텍스트 추출 + 구조화
    │
    ├───────────────────────────────────────────────────────┐
    ▼              ▼              ▼              ▼          ▼
photo_        personal_     skill_match_   self_        career_
analyze       info_analyze  analyze        intro_       analyze
                                           analyze 

(사진 분석)      (인적사항)     (기술 매칭)       (자기소개)      (경력)
                                ↑ 
                            ReAct Agent                
                            GitHub API Tool  
                            
    │                                                       │
    └──────────────── aggregator ───────────────────────────┘
                           │
                           ▼
              최종 리포트 + 추천 등급 + DB 저장
```

---

## 주요 기능

### AI 분석 항목
| 에이전트 | 분석 내용 |
|----------|----------|
| photo_analyze | 증명사진 전문성·복장·표정 평가 (GPT-4o-mini Vision) |
| personal_info_analyze | 인적사항·학력·자격증·수상이력 추출 |
| skill_match_analyze | 보유 기술 vs 요구 기술 매칭 + GitHub 기여 이력 반영 |
| self_intro_analyze | 자기소개서 논리성·직무 적합성 평가 |
| career_analyze | 경력 사항 연관성·성장 가능성 평가 |
| aggregator | 전체 결과 종합 → 점수(0~100) + 추천 등급 산출 |

### Tool Use (ReAct Agent)
이력서에 GitHub URL이 있으면 `skill_match_analyze` 에이전트가 **자율적으로 GitHub API를 호출**하여 실제 코드 기여 이력을 기술 평가에 반영합니다.

```
LLM → "GitHub 프로필 조회 필요" 판단
    → get_github_profile(url) 호출
    → 언어 통계, 레포 목록, 스타 수 수신
    → 기술 평가에 반영
```

---

## 기술 스택

### AI / Agent
LangGraph · LangChain · OpenAI GPT-4o-mini · LangSmith
### Backend
FastAPI · SQLAlchemy 2.0 (async) · aiomysql · Pydantic v2
### Frontend
Streamlit
### Database
MySQL 8.0
### Infra
Docker · Docker Compose · GCP Compute Engine · DockerHub

---

## 시작하기

### 사전 요구사항
- Docker, Docker Compose
- OpenAI API Key
- LangSmith API Key (선택)
- Kakao Developers API Key

### 1. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일에 API 키 입력
```

### 2. 실행

```bash
docker compose up -d
```

### 3. 접속

| 서비스 | URL |
|--------|-----|
| Streamlit UI | http://localhost:8501 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## 사용 방법 - Streamlit UI

1. **사이드바**에 회사명, 회사 주소, 요구 기술, 채용 공고를 입력
2. **이력서 PDF** 업로드
3. **분석 시작** 클릭 (약 30~60초 소요)
4. 분석 결과 확인
   - 종합 점수 및 추천 등급 (강력 추천 / 추천 / 보류 / 미추천)
   - 강점 및 우려사항
   - 기술·경력·사진 상세 분석 탭

---

## 프로젝트 구조

```
HR-Agent/
├── backend/
│   ├── api/            # FastAPI 라우터, 스키마, 미들웨어
│   ├── db/             # SQLAlchemy ORM 모델
│   ├── graph/
│   │   ├── nodes/      # 각 에이전트 노드 구현
│   │   ├── state.py    # GraphState (4-Layer)
│   │   └── workflow.py # LangGraph 워크플로우 빌드
│   ├── llm/            # OpenAI LLM 래퍼
│   ├── prompts/        # 각 에이전트 시스템 프롬프트
│   ├── services/       # DB 연결
│   └── tools/          # LangChain Tool (GitHub API, Geocoding)
├── frontend/           # Streamlit UI
├── Dockerfile.api
├── Dockerfile.streamlit
└── docker-compose.yml
```

---

## GraphState 설계

```
Layer 1  Input          pdf_path, company_info
Layer 2  Parsed         raw_pdf_text, resume_data, photo_path
Layer 3  Agent Results  photo / personal / skill / self_intro / career result
Layer 4  Final          final_report, overall_score
```
