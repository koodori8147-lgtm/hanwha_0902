#fastapi put, delet 예제

import json
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel


app = FastAPI()


class Poketmon(BaseModel):
    name: str
    level: int
    desc: str | None=None

class PoketmonUpdate(BaseModel):
    name: str
    leve: int
    desc: str | None=None


poketmon_list = [
    {
        "name": "Pika-chu",
        "level": 14
    }
]


@app.get("/poketmon")
async def get_poketmon():

    result = "[\n"

    result +=",\n".join(
        json.dumps(poketmon, ensure_ascii=False)
        for poketmon in poketmon_list
    )

    result += "\n]"
    
    return Response(
        content=result,
        media_type="application/json"
    )

@app.put("/poketmon/{name}")
async def update_poketmon(name: str, level: int):

    for poketmon in poketmon_list:
        if poketmon["name"] == name:
            poketmon["level"] = level
            return poketmon

    return {"경고": "포켓몬을 찾을 수 없습니다."}


@app.delete("/poketmon/{name}")
async def delete_poketmon(name: str):

    for poketmon in poketmon_list:
        if poketmon["name"] == name:
            poketmon_list.remove(poketmon)
            return {"메시지": "포켓몬을 버렸습니다."}

    return {"경고": "포켓몬을 찾을 수 없습니다."}


@app.post("/poketmon")
async def add_poketmon(poketmon: Poketmon):

    poketmon_list.append(
        {
            "name": poketmon.name,
            "level": poketmon.level
        }
    )

    return poketmon_list