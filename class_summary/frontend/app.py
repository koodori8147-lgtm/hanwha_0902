import streamlit as st
import requests

# FastAPI 주소
API_URL = "http://127.0.0.1:8000"

# Streamlit 기본 설정
st.set_page_config(
    page_title="수업 내용 정리",
    layout="wide"
)

st.title("📚 수업 내용 정리")

# 날짜 목록 가져오기
try:
    response = requests.get(
        f"{API_URL}/lessons",
        timeout=5
    )

    response.raise_for_status()

    dates = response.json()

except requests.RequestException:
    st.error("FastAPI 서버에 연결할 수 없습니다.")
    st.stop()

# 저장된 날짜가 없을 경우
if not dates:
    st.info("저장된 수업 내용이 없습니다.")
    st.stop()

# 날짜 선택
selected_date = st.selectbox(
    "날짜를 선택하세요",
    dates
)

# 선택 날짜의 수업 데이터 가져오기
response = requests.get(
    f"{API_URL}/lessons/{selected_date}",
)

lesson = response.json()

# 날짜 표시
st.header(selected_date)

# 이미지 출력
for image_name in lesson["images"]:
    image_url = (
        f"{API_URL}/uploads/{image_name}"
    )
    st.image(image_url)

# 텍스트 출력
st.markdown(
    lesson["text"]
)