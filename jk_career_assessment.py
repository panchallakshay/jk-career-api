import os
import subprocess
from openai import OpenAI

# --- CONFIGURATION ---
DATASET_PATH = 'Career_Knowledge_Master_JK_Augmented.csv'
MODEL_NAME = 'openai/gpt-3.5-turbo'
API_KEY = "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"

# --- J&K SPECIFIC QUESTIONNAIRE ---
QUESTIONS = [
    {
        "id": "stream",
        "question": "What stream did you choose/are you choosing in 12th?",
        "options": ["1. Science (PCM - Physics, Chemistry, Math)", 
                   "2. Science (PCB - Physics, Chemistry, Biology)",
                   "3. Commerce",
                   "4. Arts/Humanities"],
        "type": "choice"
    },
    {
        "id": "location",
        "question": "Which region of J&K are you from?",
        "options": ["1. Kashmir Valley (Srinagar, Anantnag, Baramulla, etc.)",
                   "2. Jammu Division (Jammu, Udhampur, Kathua, etc.)",
                   "3. Ladakh (Leh, Kargil)"],
        "type": "choice"
    },
    {
        "id": "preference",
        "question": "What is your preference for higher education?",
        "options": ["1. Government College in J&K (GDC, NIT, GMC, etc.)",
                   "2. Central University (CUK, CUJ, IIT Jammu)",
                   "3. Outside J&K (Other states/abroad)",
                   "4. Not sure yet"],
        "type": "choice"
    },
    {
        "id": "interests",
        "question": "What are your main interests? (Select up to 3, comma-separated numbers)",
        "options": ["1. Technology & Coding",
                   "2. Medicine & Healthcare",
                   "3. Business & Management",
                   "4. Government Jobs & Civil Services",
                   "5. Engineering & Construction",
                   "6. Arts, Design & Media",
                   "7. Teaching & Education",
                   "8. Law & Legal Studies",
                   "9. Agriculture & Environment",
                   "10. Other"],
        "type": "multiple"
    },
    {
        "id": "exam_prep",
        "question": "Are you preparing for any competitive exam?",
        "options": ["1. JEE (Engineering)",
                   "2. NEET (Medical)",
                   "3. CLAT (Law)",
                   "4. UPSC/JKAS (Civil Services)",
                   "5. CAT/MAT (Management)",
                   "6. Not preparing for any",
                   "7. Other"],
        "type": "choice"
    },
    {
        "id": "financial",
        "question": "What is your family's financial situation for education?",
        "options": ["1. Need affordable/government college (low fees)",
                   "2. Can afford moderate fees (₹50k-2L/year)",
                   "3. Can afford private college (₹2L+/year)",
                   "4. Prefer scholarship/free education"],
        "type": "choice"
    },
    {
        "id": "career_goal",
        "question": "What is your primary career goal?",
        "options": ["1. High salary & corporate job",
                   "2. Government job with stability",
                   "3. Entrepreneurship/Own business",
                   "4. Social service & community work",
                   "5. Research & Academia",
                   "6. Not decided yet"],
        "type": "choice"
    }
]

def search_dataset(query: str) -> str:
    """Search the career dataset"""
    keywords = [k for k in query.split() if len(k) > 3]
    if not keywords:
        keywords = [query]
        
    matches = []
    
    try:
        result = subprocess.run(
            ['grep', '-i', query, DATASET_PATH], 
            capture_output=True, text=True
        )
        if result.stdout:
            matches.extend(result.stdout.strip().split('\n')[:10])
    except Exception:
        pass
        
    if len(matches) < 5:
        for kw in keywords:
            try:
                result = subprocess.run(
                    ['grep', '-i', kw, DATASET_PATH], 
                    capture_output=True, text=True
                )
                if result.stdout:
                    new_matches = result.stdout.strip().split('\n')
                    matches.extend(new_matches[:5])
            except Exception:
                pass
    
    unique_matches = list(set(matches))[:20]
    
    if not unique_matches:
        return "No direct matches found in the dataset."
        
    return "\n".join(unique_matches)

def ask_questions():
    """Conduct the interactive assessment"""
    print("\n" + "="*70)
    print("🎓 KASHMIR DISHA - J&K Career Counseling Assessment")
    print("="*70)
    print("\nWelcome! I'll ask you a few questions to understand your profile.")
    print("This will help me provide personalized career guidance for J&K students.\n")
    
    responses = {}
    
    for q in QUESTIONS:
        print(f"\n📋 {q['question']}")
        for opt in q['options']:
            print(f"   {opt}")
        
        while True:
            answer = input("\n👉 Your answer: ").strip()
            if answer:
                responses[q['id']] = answer
                break
            print("⚠️  Please provide an answer.")
    
    return responses

def generate_career_guidance(responses, client):
    """Generate personalized career guidance based on responses"""
    
    # Build profile summary
    profile = f"""
Student Profile (J&K - 12th Standard):
- Stream: {responses.get('stream', 'N/A')}
- Region: {responses.get('location', 'N/A')}
- Education Preference: {responses.get('preference', 'N/A')}
- Interests: {responses.get('interests', 'N/A')}
- Exam Preparation: {responses.get('exam_prep', 'N/A')}
- Financial Situation: {responses.get('financial', 'N/A')}
- Career Goal: {responses.get('career_goal', 'N/A')}
"""
    
    print("\n" + "="*70)
    print("🔍 Analyzing your profile and searching our J&K career database...")
    print("="*70)
    
    # Search dataset based on interests and stream
    search_query = f"{responses.get('stream', '')} {responses.get('interests', '')}"
    dataset_results = search_dataset(search_query)
    
    # Generate guidance using AI
    prompt = f"""You are KashmirDisha, an expert career counselor for J&K students.

{profile}

Dataset Search Results:
{dataset_results}

Based on this student's profile and the J&K career database, provide:

1. **Top 3 Career Recommendations** (most suitable for this student)
2. **Specific J&K Colleges** they should target (NIT Srinagar, GMC, GDCs, etc.)
3. **Entrance Exams** they should prepare for
4. **Roadmap** - Step-by-step plan from now until career
5. **Financial Advice** - Scholarships, affordable options
6. **J&K Specific Tips** - Local opportunities, government schemes

Be specific, practical, and encouraging. Focus on realistic options available in J&K.
"""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert career counselor for J&K students. Provide detailed, practical, and encouraging guidance."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        guidance = response.choices[0].message.content
        
        print("\n" + "="*70)
        print("🌟 YOUR PERSONALIZED CAREER GUIDANCE")
        print("="*70)
        print(guidance)
        print("\n" + "="*70)
        
        # Ask if they want to save the report
        save = input("\n💾 Would you like to save this guidance report? (yes/no): ").strip().lower()
        if save in ['yes', 'y']:
            filename = f"career_guidance_{responses.get('stream', 'student').replace(' ', '_')}.txt"
            with open(filename, 'w') as f:
                f.write("KASHMIR DISHA - Career Guidance Report\n")
                f.write("="*70 + "\n\n")
                f.write(profile)
                f.write("\n" + "="*70 + "\n\n")
                f.write(guidance)
            print(f"✅ Report saved as: {filename}")
        
    except Exception as e:
        print(f"\n❌ Error generating guidance: {e}")

def main():
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Error: Dataset '{DATASET_PATH}' not found.")
        return

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY,
    )
    
    # Conduct assessment
    responses = ask_questions()
    
    # Generate guidance
    generate_career_guidance(responses, client)
    
    print("\n👋 Thank you for using Kashmir Disha! Best of luck with your career journey!")

if __name__ == "__main__":
    main()
