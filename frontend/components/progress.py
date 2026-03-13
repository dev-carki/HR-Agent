import streamlit as st


def _score_color(score: int) -> str:
    if score >= 80:
        return "normal"
    if score >= 60:
        return "normal"
    if score >= 40:
        return "off"
    return "inverse"


def render_progress(overall_score: int, scores: dict):
    st.markdown("#### 점수")

    col_total, col_skill, col_career, col_intro = st.columns(4)

    with col_total:
        st.metric(label="종합 점수", value=f"{overall_score}점")
        st.progress(overall_score / 100)

    with col_skill:
        score = scores.get("skill_match", 0)
        st.metric(label="기술 적합도 (40%)", value=f"{score}점")
        st.progress(score / 100)

    with col_career:
        score = scores.get("career", 0)
        st.metric(label="경력 적합도 (45%)", value=f"{score}점")
        st.progress(score / 100)

    with col_intro:
        score = scores.get("self_introduction", 0)
        st.metric(label="자기소개서 (15%)", value=f"{score}점")
        st.progress(score / 100)
