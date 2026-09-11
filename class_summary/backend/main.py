from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles

from pathlib import Path
import json
import uuid

# 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "lessons.json"
UPLOAD_DIR = BASE_DIR / "uploads"

# FastAPI 생성
app = FastAPI(
    title="Class Note API"
)

# 이미지 폴더 연결
app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)

# JSON 파일 읽기 함수
def load_data():

    with open(DATA_FILE, "r", encoding="utf-8") as file:

        data = json.load(file)

    return data

def save_data(data):

    with open(DATA_FILE, "w", encoding="utf-8") as file:

        json.dump(data, file, ensure_ascii=False, indent=4)

# 서버 동작 확인
@app.get("/")
def root():

    return {
        "message": "FastAPI 서버 정상 동작"
    }

# 전체 날짜 조회
@app.get("/lessons")
def get_lesson_dates():

    data = load_data()

    dates = sorted(
        data.keys(),
        reverse=True
    )

    return dates

# 특정 날짜 조회
@app.get("/lessons/{lesson_date}")
def get_lesson(lesson_date: str):

    data = load_data()

    if lesson_date not in data:

        raise HTTPException(
            status_code=404,
            detail="해당 날짜의 수업 내용이 없습니다."
        )

    lesson = data[lesson_date]

    return {
        "date": lesson_date,
        "text": lesson["text"],
        "images": lesson["images"]
    }

# 수업 내용 추가
@app.post("/lessons")
async def create_lesson(
    lesson_date: str = Form(...),
    text: str = Form(...),
    images: list[UploadFile] = File(default=[]))
):

    data = load_data()

    # 이미 해당 날짜가 존재하면 추가 금지
    if lesson_date in data:

        raise HTTPException(
            status_code=400,
            detail="이미 해당 날짜의 수업 내용이 존재합니다."
        )

    saved_images = []

    # 업로드한 이미지들을 하나씩 처리
    for image in images:

        # 파일 확장자 확인
        extension = Path(image.filename).suffix.lower()

        if extension not in [".jpg", ".jpeg"]:
            raise HTTPException(
                status_code=400,
                detail="JPG 또는 JPEG 파일만 업로드할 수 있습니다."
            )

    # 중복 방지를 위한 새로운 파일 이름 생성
    new_filename = f"{uuid.uuid4()}{extension}"

    save_path = UPLOAD_DIR / new_filename
