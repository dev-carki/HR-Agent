import os

import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def render_photo_card(photo_result: dict, photo_path: str):
    if not photo_result:
        st.info("사진 분석 결과가 없습니다.")
        return

    if not photo_result.get("has_photo"):
        st.warning("이력서에 사진이 없습니다.")
        return

    col_photo, col_info, col_status = st.columns(3)
    with col_photo:
        if photo_path:
            image_url = API_BASE_URL + "/api/v1/images/" + photo_path.replace("uploads/", "")
            st.image(image_url)
        else:
            st.markdown(
                """
                <div style="background:#f0f2f6; border-radius:8px;
                            height:150px; display:flex; align-items:center;
                            justify-content:center; color:#888;">
                    📷 사진 없음
                </div>
                """,
                unsafe_allow_html=True
            )


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
