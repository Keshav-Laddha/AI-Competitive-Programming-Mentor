# import openai
# from app.config import settings

# openai.api_key=settings.OPENAI_API_KEY

# def call_llm(prompt: str):
#     response=openai.ChatCompletion.create(model="gpt-4o", messages=[{"role": "system", "content": prompt}], temperature=0.3)
#     return response.choices[0].message.content

from openai import OpenAI
from app.config import settings

client=OpenAI(api_key=settings.OPENAI_API_KEY)

def call_llm(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # cheaper+fast
        messages=[
            {"role": "system", "content": "You are a Competitive Programming Mentor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content