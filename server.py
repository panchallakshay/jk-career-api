from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import ai_answer     # ⬅ REAL AI imported

app = FastAPI(title="JK Career Guidance API")

class Query(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_model(query: Query):
    response_text = ai_answer(query.prompt)
    return {"ok": True, "response": response_text}

class Answers(BaseModel):
    answers: list

@app.post("/recommend")
async def recommend(data: Answers):
    prompt = "Student responses: " + ", ".join(data.answers) + \
             ". Suggest best career options for Jammu & Kashmir students."
    result = ai_answer(prompt)
    return {"ok": True, "result": result}
