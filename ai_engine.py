import os
from openai import OpenAI

MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-3.5-turbo")
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not set.")

client = OpenAI(api_key=API_KEY)

def chat(messages, max_tokens=500, temperature=0.2):
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return resp.choices[0].message.content
