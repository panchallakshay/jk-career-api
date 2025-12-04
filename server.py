from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import run_ai

app = FastAPI(title="JK Career API with AI Engine")

class Query(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_ai(query: Query):
    response = run_ai(query.prompt)
    return {"ok": True, "response": response}

