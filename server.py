from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from ai_engine import chat

try:
    from career_rag_openrouter import get_user_data_from_firebase, search_dataset, SYSTEM_PROMPT
except:
    def get_user_data_from_firebase(x): return None
    def search_dataset(x): return "No dataset"
    SYSTEM_PROMPT = "You are KashmirDisha."

app = FastAPI()
sessions: Dict[str, Dict[str, Any]] = {}

class StartRequest(BaseModel):
    student_id: str

class ReplyRequest(BaseModel):
    student_id: str
    message: str

class ReportRequest(BaseModel):
    student_id: str

@app.post("/start")
async def start(req: StartRequest):
    sid = req.student_id.strip()
    user_data = get_user_data_from_firebase(sid)
    if not user_data:
        raise HTTPException(404, "Student not found")

    terms = f"{user_data.get('12th_stream','')} {user_data.get('fav_subject_12th','')} {user_data.get('interests','')}"
    data = search_dataset(terms)

    profile = f"PROFILE: {user_data}"
    system_txt = SYSTEM_PROMPT + "\n" + profile + "\n" + data

    msgs = [
        {"role":"system","content":system_txt},
        {"role":"user","content":"Start counseling with first question."}
    ]

    ai = chat(msgs, max_tokens=300)
    sessions[sid] = {"messages": msgs + [{"role":"assistant","content":ai}], "user_data": user_data}
    return {"ok": True, "next": ai}

@app.post("/reply")
async def reply(req: ReplyRequest):
    sid = req.student_id.strip()
    if sid not in sessions:
        raise HTTPException(404, "No session")

    msg = req.message.strip()
    s = sessions[sid]
    s["messages"].append({"role":"user","content":msg})

    if msg.lower() in ["done", "finish"]:
        return {"ok": True, "next": "Call /report now."}

    ai = chat(s["messages"], max_tokens=300)
    s["messages"].append({"role":"assistant","content":ai})
    return {"ok": True, "next": ai}

@app.post("/report")
async def report(req: ReportRequest):
    sid = req.student_id.strip()
    if sid not in sessions:
        raise HTTPException(404, "No session")

    s = sessions[sid]
    final = "Generate full career report.\n\n"
    for m in s["messages"]:
        final += f"{m['role'].upper()}: {m['content']}\n"

    out = chat([{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":final}], max_tokens=2500)
    return {"ok": True, "report": out}
