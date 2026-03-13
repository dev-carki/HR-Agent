import streamlit as st


def render_career_card(career_result: dict):
    if not career_result:
        st.info("경력 분석 결과가 없습니다.")
        return

    col_candidate, col_required = st.columns(2)

    with col_candidate:
        st.markdown("**지원자 경력 요약**")
        st.write(career_result.get("career_summary", "-"))

    with col_required:
        st.markdown("**회사 요구 경력**")
        st.write(career_result.get("required_summary", "-"))

    st.divider()

    st.markdown("**경력 적합성 분석**")
    st.write(career_result.get("analysis", "-"))
