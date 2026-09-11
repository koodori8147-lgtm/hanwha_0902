from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI()

#데이터 구조
class ChampionSchema(BaseModel):
    name: str
    price: int
    attack_range: Literal["근접", "원거리"]
    role: Literal["서포터", "딜러", "탱커"]

#추천 데이터 구조
class RecommendSchema(BaseModel):
    money: int = Field(ge=0)
    attack_range: Literal["근접", "원거리"]
    role: Literal["서포터", "딜러", "탱커"]

#임시 데이터베이스
champions_db: dict[int, dict] = {
    1: {
        "id": 1,
        "name": "가렌",
        "price": 450,
        "attack_range": "근접",
        "role": "탱커"
    },

    2: {
        "id": 2,
        "name": "애쉬",
        "price": 450,
        "attack_range": "원거리",
        "role": "딜러"
    },
    3: {
        "id": 3,
        "name": "럭스",
        "price": 1350,
        "attack_range": "원거리",
        "role": "서포터"
    },

    4: {
        "id": 4,
        "name": "레오나",
        "price": 1350,
        "attack_range": "근접",
        "role": "서포터"
    },

    5: {
        "id": 5,
        "name": "다리우스",
        "price": 3150,
        "attack_range": "근접",
        "role": "딜러"
    },

    6: {
        "id": 6,
        "name": "케이틀린",
        "price": 4800,
        "attack_range": "원거리",
        "role": "딜러"
    },
    7: {
        "id": 7,
        "name": "카타리나",
        "price": 3150,
        "attack_range": "근접",
        "role": "딜러"
    },

    8: {
        "id": 8,
        "name": "마오카이",
        "price": 4800,
        "attack_range": "근접",
        "role": "탱커"
    },

    9: {
        "id": 9,
        "name": "트린다미어",
        "price": 1350,
        "attack_range": "근접",
        "role": "딜러"
    },

    10: {
        "id": 10,
        "name": "소라카",
        "price": 450,
        "attack_range": "원거리",
        "role": "서포터"
    },
    11: {
        "id": 11,
        "name": "룰루",
        "price": 4800,
        "attack_range": "원거리",
        "role": "서포터"
    },

    12: {
        "id": 12,
        "name": "람머스",
        "price": 3150,
        "attack_range": "근접",
        "role": "탱커"
    },

    13: {
        "id": 13,
        "name": "라이즈",
        "price": 450,
        "attack_range": "원거리",
        "role": "딜러"
    },

    14: {
        "id": 14,
        "name": "트위치",
        "price": 4800,
        "attack_range": "원거리",
        "role": "딜러"
    }    
}

id_counter = 15

#생성 Create
@app.post("/champions", status_code=201)
async def create_champion(champion: ChampionSchema):
    global id_counter
    new_champion = champion.model_dump()
    new_champion["id"] = id_counter

    champions_db[id_counter] = new_champion
    id_counter += 1

    return {
        "message": "챔피언 등록 완료",
        "data": new_champion
    }

#조회 (전체)Read
@app.get("/champions")
async def get_all_champions():

    return {"message": "전체 챔피언 조회 완료", "data": list(champions_db.values())}

#조회 (단일)Read
@app.get("/champions/{champion_id}")
async def get_champion(champion_id: int):
    if champion_id not in champions_db:
        raise HTTPException(status_code=404, detail="챔피언을 찾을 수 없습니다.")

    return {"message": "챔피언 조회 완료", "data": champions_db[champion_id]}

#수정 Update 200
@app.put("/champions/{champion_id}")
async def update_champion(champion_id: int, champion: ChampionSchema):
    if champion_id not in champions_db :
        raise HTTPException(status_code=404, detail="챔피언을 찾을 수 없습니다.")

    updated_data = champion.model_dump()
    updated_data["id"] = champion_id
    champions_db[champion_id] = updated_data

    return {"message": "챔피언 수정 완료", "data": updated_data}

#삭제 Delete 200
@app.delete("/champions/{champion_id}")
async def delete_champion(champion_id: int):

    if champion_id not in champions_db:
        raise HTTPException(
            status_code=404,
            detail="챔피언을 찾을 수 없습니다."
        )

    deleted_champion = champions_db.pop(champion_id)

    return {
        "message": "챔피언 삭제 완료",
        "data": deleted_champion
    }

#챔피언 추천
@app.post("/recommend")
async def recommend_champion(user: RecommendSchema):

        # 1. 사용자가 가진 돈 이하의 챔피언
        affordable_champions = [
        champion
        for champion in champions_db.values()
        if champion["price"] <= user.money
    ]
          # 구매 가능한 챔피언 자체가 없는 경우
        if not affordable_champions:
            return {
                "message": "추천 챔피언이 없습니다. 다른 챔피언은 어떨까요?"
        }
    # 2. 사거리 + 역할군 모두 만족
        perfect_match = [
            champion
            for champion in affordable_champions
            if champion["attack_range"] == user.attack_range
            and champion["role"] == user.role
        ]


        if perfect_match:
            return {
                "message": "사거리와 역할군이 모두 일치하는 챔피언입니다.",
                "data": perfect_match
        }
    # 3. 역할군만 만족
        role_match = [
            champion
            for champion in affordable_champions
            if champion["role"] == user.role
        ]


        if role_match:
            return {
                "message": "사거리는 다르지만 역할군이 일치하는 챔피언입니다.",
                "data": role_match
            }
    # 4. 추천 결과 없음
        return {
            "message": "추천 챔피언이 없습니다. 다른 챔피언은 어떨까요?"
        }