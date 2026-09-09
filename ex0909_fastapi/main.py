#fastapi get, post 예제

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Champion(BaseModel):
    name: str
    price: int

#http://127.0.0.1:8000/
@app.get("/")
async def root():
    return {"message": "안녕하세요"}

#http://127.0.0.1:8000/champion
@app.post("/champion")
async def create_champion(champion: Champion):
    tot = champion.price * 1.1

    return {
        "message": "하기 챔피언의 가격은 이렇습니다.",
        "name": champion.name,
        "price": champion.price,
        "total": tot
    }

@app.get("/champion")
async def get_champion():
    return {
        "message": "하기 챔피언의 가격은 이렇습니다.",
        "name": "트린다미어",
        "price": 1350
    }

#http://127.0.0.1:8000/ad_range
@app.get("/ad_range")
async def ad_range():
    return {"트린다미어 사거리": "175"}

#http://127.0.0.1:8000/ultimate
@app.get("/ultimate")
async def ultimate():
    return {"트린다미어 무적 시간": "5초"}