import os
from openai import OpenAI

def run_ai(prompt: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "❌ ERROR: OPENROUTER_API_KEY is missing."

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content
