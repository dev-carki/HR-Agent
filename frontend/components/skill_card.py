import streamlit as st


def render_skill_card(skill_result: dict):
    if not skill_result:
        st.info("기술 분석 결과가 없습니다.")
        return

    col_match, col_missing = st.columns(2)

    with col_match:
        st.markdown("**매칭된 기술**")
        matched = skill_result.get("matched_skills", [])
        if matched:
            st.success(", ".join(matched))
        else:
            st.write("없음")

    with col_missing:
        st.markdown("**미충족 기술**")
        missing = skill_result.get("missing_skills", [])
        if missing:
            st.error(", ".join(missing))
        else:
            st.write("없음")

    st.divider()

    col_candidate, col_required = st.columns(2)
    with col_candidate:
        st.markdown("**지원자 보유 기술**")
        for skill in skill_result.get("candidate_skills", []):
            st.markdown(f"- {skill}")

    with col_required:
        st.markdown("**회사 요구 기술**")
        for skill in skill_result.get("required_skills", []):
            st.markdown(f"- {skill}")
