from openai import OpenAI
from career_rag_openrouter import search_dataset, SYSTEM_PROMPT, MODEL_NAME, API_KEY

# Create OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

def run_ai(prompt: str) -> str:
    """
    Clean API wrapper that uses your dataset + OpenRouter model.
    Does NOT modify your original code.
    """

    # 1. search local dataset
    dataset_hits = search_dataset(prompt)

    final_prompt = f"""
User Query: {prompt}

Relevant Dataset Matches:
{dataset_hits}

Based on the KashmirDisha rules:
- Use dataset information first
- If not found, give general guidance
- Keep answer short (< 200 words)
    """

    # 2. Call OpenRouter GPT
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": final_prompt}
        ],
        max_tokens=400
    )

    return response.choices[0].message.content
