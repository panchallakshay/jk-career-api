from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
from download_data import download_all_files

# Download datasets when service starts
download_all_files()

DATA_DIR = "data"

def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

career_db = load_csv("Career_Database.csv")
recommender_db = load_csv("CareerRecommenderDataset.csv")

app = FastAPI(title="JK Career Guidance API")

class Query(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_model(query: Query):
    return {"ok": True, "response": f"You asked: {query.prompt}"}

class Answers(BaseModel):
    answers: list

@app.post("/recommend")
async def recommend_career(data: Answers):
    return {
        "ok": True,
        "result": {
            "career": "Software Engineer",
            "confidence": 0.92
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
