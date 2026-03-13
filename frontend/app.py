import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from frontend.components.upload import render_upload
from frontend.components.results import render_results

st.set_page_config(
    page_title="HR Agent",
    page_icon="🤖",
    layout="wide",
)

# ── 사이드바: 회사 정보 입력 ────────────────────────────────────────────────────
with st.sidebar:
    st.header("회사 정보")

    company_name = st.text_input("회사명", placeholder="예) 테스트 회사")
    company_address = st.text_input("회사 주소", placeholder="예) 서울시 강남구")
    required_skills_input = st.text_input(
        "요구 기술",
        placeholder="Python, FastAPI, MySQL (쉼표로 구분)",
    )
    jd_text = st.text_area(
        "채용 공고 전문",
        height=200,
        placeholder="채용 공고 내용을 입력하세요.",
    )

    required_skills = [s.strip() for s in required_skills_input.split(",") if s.strip()]

# ── 메인: 제목 + 업로드 + 결과 ──────────────────────────────────────────────────
st.title("🤖 HR Agent")
st.caption("AI 기반 이력서 분석 시스템")
st.divider()

company_info = {
    "company_name": company_name,
    "company_address": company_address,
    "required_skills": required_skills,
    "jd_text": jd_text,
}

render_upload(company_info)

if "result" in st.session_state:
    st.divider()
    render_results(st.session_state["result"])
