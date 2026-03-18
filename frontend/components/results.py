import streamlit as st

from frontend.components.progress import render_progress
from frontend.components.skill_card import render_skill_card
from frontend.components.career_card import render_career_card
from frontend.components.photo_card import render_photo_card


RECOMMENDATION_STYLE = {
    "강력 추천": ("success", "✅ 강력 추천"),
    "추천":     ("info",    "👍 추천"),
    "보류":     ("warning", "⏸️ 보류"),
    "미추천":   ("error",   "❌ 미추천"),
}


def render_results(result: dict):
    report = result["final_report"]
    overall_score = result["overall_score"]

    # ── 헤더: 지원자명 + 추천 결과 ───────────────────────────────────────────────
    col_name, col_rec = st.columns([3, 1])
    with col_name:
        st.subheader(f"👤 {report.get('candidate_name', '지원자')}  —  {report.get('applied_position', '')}")
    with col_rec:
        rec = report.get("recommendation", "")
        style, label = RECOMMENDATION_STYLE.get(rec, ("warning", rec))
        getattr(st, style)(label)

    st.write(report.get("overall_summary", ""))

    # ── 점수 ─────────────────────────────────────────────────────────────────────
    render_progress(overall_score, report.get("scores", {}))

    st.divider()

    # ── 강점 / 우려사항 ───────────────────────────────────────────────────────────
    col_str, col_con = st.columns(2)
    with col_str:
        st.markdown("**✅ 강점**")
        for item in report.get("strengths", []):
            st.markdown(f"- {item}")
    with col_con:
        st.markdown("**⚠️ 우려사항**")
        concerns = report.get("concerns", [])
        if concerns:
            for item in concerns:
                st.markdown(f"- {item}")
        else:
            st.markdown("- 없음")

    st.divider()

    # ── 지원자 주소 + 통근 거리 ───────────────────────────────────────────────────
    personal_info = result.get("personal_info_result", {})
    if personal_info:
        location = personal_info.get("location", "")
        distance_info = personal_info.get("distance_info")

        if location:
            st.info(f"📍 지원자는 **{location}** 에 거주하는 것으로 확인됩니다.")

        if distance_info and not distance_info.get("error"):
            col_dist, col_car, col_transit = st.columns(3)
            with col_dist:
                st.metric("직선거리", f"{distance_info['distance_km']} km")
            with col_car:
                st.metric("차량 이동", distance_info["car_time"])
            with col_transit:
                st.metric("대중교통", distance_info["transit_time"])
        elif distance_info and distance_info.get("error"):
            st.caption(f"거리 정보 조회 실패: {distance_info['error']}")

    st.divider()

    # ── 상세 분석 탭 ──────────────────────────────────────────────────────────────
    tab_skill, tab_career, tab_photo = st.tabs(["기술 분석", "경력 분석", "사진 분석"])

    with tab_skill:
        render_skill_card(result.get("skill_match_result", {}))

    with tab_career:
        render_career_card(result.get("career_result", {}))

    with tab_photo:
        render_photo_card(result.get("photo_result", {}), photo_path=result.get("photo_path"))
