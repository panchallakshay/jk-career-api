from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import run_ai

app = FastAPI()

class Query(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_ai(query: Query):
    try:
        answer = run_ai(query.prompt)
        return {"ok": True, "response": answer}
    except Exception as e:
        return {"ok": False, "error": str(e)}
