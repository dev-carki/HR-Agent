import streamlit as st


def render_photo_card(photo_result: dict):
    if not photo_result:
        st.info("사진 분석 결과가 없습니다.")
        return

    if not photo_result.get("has_photo"):
        st.warning("이력서에 사진이 없습니다.")
        return

    col_info, col_status = st.columns(2)

    with col_info:
        st.markdown("**사진 설명**")
        st.write(photo_result.get("description", "-"))

        st.markdown("**총평**")
        st.write(photo_result.get("summary", "-"))

    with col_status:
        face_visible = photo_result.get("face_visible", False)
        is_professional = photo_result.get("is_professional", False)

        st.metric(label="얼굴 식별", value="✅ 가능" if face_visible else "❌ 불가")
        st.metric(label="전문성", value="✅ 적합" if is_professional else "⚠️ 미흡")

        issues = photo_result.get("issues", [])
        if issues:
            st.markdown("**문제점**")
            for issue in issues:
                st.warning(issue)
