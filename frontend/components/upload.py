import requests
import streamlit as st

API_URL = "http://localhost:8000/api/v1/resume/analyze"


def render_upload(company_info: dict):
    st.subheader("이력서 업로드")

    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

    if st.button("분석 시작", type="primary", disabled=uploaded_file is None):
        if not company_info["company_name"]:
            st.error("회사명을 입력해주세요.")
            return
        if not company_info["required_skills"]:
            st.error("요구 기술을 입력해주세요.")
            return
        if not company_info["jd_text"]:
            st.error("채용 공고 전문을 입력해주세요.")
            return

        with st.spinner("이력서 분석 중..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                data = [
                    ("company_name", company_info["company_name"]),
                    ("company_address", company_info["company_address"]),
                    ("jd_text", company_info["jd_text"]),
                ] + [("required_skills", skill) for skill in company_info["required_skills"]]

                response = requests.post(API_URL, files=files, data=data, timeout=180)
                response.raise_for_status()

                st.session_state["result"] = response.json()["data"]
                st.rerun()

            except requests.exceptions.Timeout:
                st.error("분석 시간이 초과되었습니다. 다시 시도해주세요.")
            except requests.exceptions.ConnectionError:
                st.error("API 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
