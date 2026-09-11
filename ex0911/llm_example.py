from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

question = "최태원의 부인은 누구야?"
temperature = 0.8

response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=temperature,
    messages=[
        {"role": "user", "content": question}
    ]
)

print(response.choices[0].message.content)