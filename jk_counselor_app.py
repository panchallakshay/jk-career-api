import os
import time
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# --- CONFIGURATION ---
FINAL_MASTER_FILE = 'Career_Knowledge_Master_JK_Augmented.csv' 
MODEL_NAME = 'gemini-2.5-pro' 

# --- J&K Counseling Logic (System Prompt) ---
SYSTEM_PROMPT = (
    "You are a compassionate, expert Career Counselor named 'KashmirDisha' for 12th-grade students in J&K. "
    "Your core mission is to provide accurate, data-grounded advice that **motivates students toward high-quality, affordable Government Institutions** to counter local admission declines. "
    "You must use the text content provided by the RAG tool. "
    "Prioritize careers with high 'JK_GOVT_PRIORITY: TRUE' based on the data."
)

# --- Structured Output Schema (Standardizes the final answer) ---
class CareerRecommendation(BaseModel):
    """A structured career recommendation including local context."""
    career_title: str = Field(description="The final recommended career title.")
    match_score_confidence: int = Field(description="Confidence score (1-100) based on student profile and data match.")
    required_course: str = Field(description="The specific course/degree required (e.g., B.Tech, BBA, B.Sc. IT).")
    local_jk_path: str = Field(description="The best path via a J&K Government Degree College (GDC) or Central University.")
    immediate_next_step: str = Field(description="The single most important action for the student to take now.")

# --- CORE EXECUTION ---

def setup_rag_and_run_chat():
    try:
        # Client initialization relies on the GEMINI_API_KEY environment variable
        client = genai.Client()
    except Exception:
        print("❌ ERROR: Please ensure you have set the GEMINI_API_KEY environment variable (export GEMINI_API_KEY='YOUR_KEY').")
        return

    # Check if the master file exists
    if not os.path.exists(FINAL_MASTER_FILE):
        print(f"❌ ERROR: Master file '{FINAL_MASTER_FILE}' not found. Please run data_processor.py first.")
        return

    print("\n--- Starting Gemini RAG Setup (Upload and Indexing) ---")
    
    try:
        # 1. Create File Search Store
        file_search_store = client.file_search_stores.create(
            config={'display_name': 'JK_Career_Guidance_Master_Store'}
        )
        store_name = file_search_store.name

        # 2. Upload the single master file
        print(f"Uploading {FINAL_MASTER_FILE}...")
        operation = client.file_search_stores.upload_to_file_search_store(
            file=FINAL_MASTER_FILE, 
            file_search_store_name=store_name,
            config={'display_name': FINAL_MASTER_FILE}
        )

        # Wait for indexing to complete
        while not operation.done:
            print("Indexing data...", end="", flush=True)
            time.sleep(5)
            operation = client.operations.get(operation)
        
        print("\n✅ RAG Setup Complete. Chatbot is ready. ✅")

        # 3. Define the Retrieval Tool
        retrieval_tool = types.Tool(
            file_search=types.FileSearch(
                retrieval_resources=types.FileSearchRetrievalResource(
                    file_search_store=store_name
                )
            )
        )

        # --- Interactive Chat Loop ---
        while True:
            user_input = input("\nStudent Query (Type 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            
            # Generate the advice
            response = client.generate_content(
                model=MODEL_NAME,
                contents=[
                    types.Content(role="system", parts=[types.Part.from_text(SYSTEM_PROMPT)]),
                    types.Content(role="user", parts=[types.Part.from_text(user_input)])
                ],
                config=types.GenerateContentConfig(
                    tools=[retrieval_tool], 
                    response_mime_type="application/json",
                    response_schema=CareerRecommendation,
                )
            )
            
            # Display the structured result
            recommendation_data = json.loads(response.text)
            print("\n=======================================================")
            print("⭐ KashmirDisha: Your Career Guide (Structured Result) ⭐")
            print("=======================================================")
            print(f"Career: {recommendation_data.get('career_title')}")
            print(f"Confidence Score: {recommendation_data.get('match_score_confidence')}%")
            print("-------------------------------------------------------")
            print(f"Required Course: {recommendation_data.get('required_course')}")
            print(f"J&K Local Path: {recommendation_data.get('local_jk_path')}")
            print("-------------------------------------------------------")
            print(f"Next Action: {recommendation_data.get('immediate_next_step')}")
            print("=======================================================")
            

    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        print("The RAG store failed to set up or query. Check your API key and file contents.")

# --- MAIN EXECUTION LOOP ---
if __name__ == "__main__":
    setup_rag_and_run_chat()
