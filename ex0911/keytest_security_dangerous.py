import os
from openai import OpenAI

api_key = os.getenv("OPEN_API_KEY")

if api_key is None:
    print("❌ API Key를 찾을 수 없습니다.")
else:
    print("✅ API Key 불러오기 성공")
    print("Key:", api_key[:8] + "..." + api_key[-4:])

    try:
        client = OpenAI(api_key=api_key)

        client.models.list()

        print("✅ OpenAI API 연결 성공")

    except Exception as e:
        print("❌ OpenAI API 연결 실패")
        print(e)