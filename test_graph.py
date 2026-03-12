import json
from backend.graph.workflow import build_graph

graph = build_graph()

initial_state = {
    "pdf_path": "data/raw/Resume_Sample.pdf",
    "company_info": {
        "name": "테스트 회사",
        "address": "서울시 강남구",
        "required_skills": ["Python", "FastAPI", "MySQL", "Docker"],
        "jd_text": "백엔드 개발자를 채용합니다. Python 기반 FastAPI 경험 3년 이상, MySQL 운용 경험 필수. Docker 및 클라우드 환경 경험 우대.",
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

print("그래프 실행 시작...\n")
result = graph.invoke(initial_state)

print("=" * 60)
print("최종 결과")
print("=" * 60)
print(f"overall_score: {result['overall_score']}")
print(f"\nfinal_report:\n{json.dumps(result['final_report'], ensure_ascii=False, indent=2)}")
