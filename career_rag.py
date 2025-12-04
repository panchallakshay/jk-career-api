import os
import time
import sys
from google import genai
from google.genai import types

# --- CONFIGURATION ---
# Using the enriched master file
DATASET_PATH = 'Career_Knowledge_Master_JK_Augmented.csv'
# Using Gemini 1.5 Pro (stable and works with your API key)
MODEL_NAME = 'gemini-1.5-pro' 

# --- TOOL DEFINITION ---
def search_dataset(query: str):
    """
    Searches the career dataset for relevant information using keywords.
    Args:
        query: The search query (e.g., "Data Scientist", "Salary of Doctor").
    Returns:
        A string containing relevant CSV rows.
    """
    import subprocess
    
    print(f"\n[Tool] Searching dataset for: '{query}'...")
    
    # Simple keyword extraction (naive but effective for grep)
    keywords = [k for k in query.split() if len(k) > 3] # Filter small words
    if not keywords:
        keywords = [query]
        
    # Construct grep command
    # We use -i for case insensitive
    # We limit to 20 matches to prevent context overflow
    matches = []
    
    # Try searching for the whole phrase first
    try:
        result = subprocess.run(
            ['grep', '-i', query, DATASET_PATH], 
            capture_output=True, text=True
        )
        if result.stdout:
            matches.extend(result.stdout.strip().split('\n')[:10])
    except Exception:
        pass
        
    # If few matches, search for individual keywords
    if len(matches) < 5:
        for kw in keywords:
            try:
                result = subprocess.run(
                    ['grep', '-i', kw, DATASET_PATH], 
                    capture_output=True, text=True
                )
                if result.stdout:
                    new_matches = result.stdout.strip().split('\n')
                    matches.extend(new_matches[:5]) # Add top 5 for each keyword
            except Exception:
                pass
    
    # Deduplicate and limit
    unique_matches = list(set(matches))[:20]
    
    if not unique_matches:
        return "No direct matches found in the dataset."
        
    return "\n".join(unique_matches)

SYSTEM_PROMPT = """
You are 'KashmirDisha', an expert Career Counselor for students in J&K.
Your goal is to provide accurate, data-driven career advice.

**CRITICAL INSTRUCTION**:
You have access to a tool called `search_dataset`. 
You **MUST** use this tool to look up information in the 'Career_Knowledge_Master_JK_Augmented.csv' file whenever a user asks a question.

RULES:
1. **SEARCH FIRST**: If the user asks "How to be a Pilot?", call `search_dataset("Pilot")`.
2. **USE DATASET**: If the tool returns data, you **MUST** answer using ONLY that data. Do not add outside info if the data is sufficient.
3. **EXCEPTION (FALLBACK)**: 
   - **ONLY** if the tool returns "No direct matches found", then (and only then) are you allowed to use your **General Knowledge** (API) to answer.
   - When doing this, start your answer with: "⚠️ **Note:** This career is not in our local J&K database, but here is general guidance from the web:"
4. **J&K CONTEXT**: Always emphasize local J&K colleges (NIT Srinagar, GMC, etc.) if mentioned in the data.
"""

def main():
    # Replace 'YOUR_GEMINI_API_KEY_HERE' with your actual Google Gemini API Key
    # Get it from: https://aistudio.google.com/apikey
    api_key = "YOUR_GEMINI_API_KEY_HERE"
    
    if not api_key:
        print("❌ Error: API Key is missing.")
        return

    if not os.path.exists(DATASET_PATH):
        print(f"❌ Error: Dataset '{DATASET_PATH}' not found.")
        return

    print("🚀 Initializing Gemini Client...")
    client = genai.Client(api_key=api_key)

    print("\n💬 KashmirDisha is ready! (Type 'exit' to quit)")
    print("--------------------------------------------------")
    
    # Initialize chat with the tool
    chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            tools=[search_dataset], # Register the python function as a tool
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3
        )
    )

    while True:
        user_input = input("\nStudent: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye! Best of luck with your career.")
            break
        
        if not user_input.strip():
            continue

        print("Counselor: Thinking...", end="\r")
        try:
            response = chat.send_message(user_input)
            
            # Check if the model wants to call a tool
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    # Execute tool
                    fn_name = part.function_call.name
                    fn_args = part.function_call.args
                    
                    if fn_name == 'search_dataset':
                        # Run the function
                        tool_result = search_dataset(**fn_args)
                        
                        # Send result back to model
                        response = chat.send_message(
                            types.Content(
                                parts=[
                                    types.Part.from_function_response(
                                        name=fn_name,
                                        response={'result': tool_result}
                                    )
                                ]
                            )
                        )
                        break
            
            print(f"Counselor: {response.text}")
            
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print(f"\n⏳ Rate limit hit. Waiting 20 seconds before retry...")
                time.sleep(20)
                print("Retrying your question...")
                try:
                    response = chat.send_message(user_input)
                    print(f"Counselor: {response.text}")
                except Exception as retry_error:
                    print(f"\n❌ Still hitting limits. Please wait a minute and try again.")
                    print(f"Error: {retry_error}")
            else:
                print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
