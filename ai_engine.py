from career_rag_openrouter.py import answer_question_rag  # replace with your real function

def ai_answer(prompt: str) -> str:
    try:
        response = answer_question_rag(prompt)
        return response
    except Exception as e:
        return f"AI Error: {e}"
