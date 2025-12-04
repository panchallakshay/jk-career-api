import os
import subprocess
from openai import OpenAI
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONFIGURATION ---
DATASET_PATH = 'Career_Knowledge_Master_JK_Augmented.csv'
MODEL_NAME = 'openai/gpt-3.5-turbo'
API_KEY = "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"

# Firebase configuration
# Place your firebase service account key JSON file in the same directory
FIREBASE_KEY_PATH = 'firebase-key.json'

def initialize_firebase():
    """Initialize Firebase connection"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_KEY_PATH)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"⚠️  Firebase initialization failed: {e}")
        print("Please ensure 'firebase-key.json' is in the same folder.")
        return None

def get_user_data_from_firebase(user_id):
    """Fetch user data from Firebase"""
    db = initialize_firebase()
    if not db:
        return None
    
    try:
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"⚠️  No user found with ID: {user_id}")
            return None
    except Exception as e:
        print(f"❌ Error fetching user data: {e}")
        return None

def get_greeting():
    """Get time-appropriate greeting"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Hello"

def search_dataset(query: str) -> str:
    """Search the career dataset"""
    keywords = [k for k in query.split() if len(k) > 3]
    if not keywords:
        keywords = [query]
    
    matches = []
    try:
        result = subprocess.run(['grep', '-i', query, DATASET_PATH], 
                              capture_output=True, text=True)
        if result.stdout:
            matches.extend(result.stdout.strip().split('\n')[:15])
    except Exception:
        pass
    
    if len(matches) < 10:
        for kw in keywords[:3]:
            try:
                result = subprocess.run(['grep', '-i', kw, DATASET_PATH], 
                                      capture_output=True, text=True)
                if result.stdout:
                    matches.extend(result.stdout.strip().split('\n')[:5])
            except Exception:
                pass
    
    unique_matches = list(set(matches))[:25]
    return "\n".join(unique_matches) if unique_matches else "No matches found."

def ask_question(question, options=None):
    """Ask a question and get response"""
    print(f"\n💬 {question}")
    
    if options:
        for i, opt in enumerate(options, 1):
            print(f"   {i}. {opt}")
    
    while True:
        answer = input("\n👉 Your answer: ").strip()
        if answer:
            return answer
        print("⚠️  Please provide an answer.")

def conduct_career_focused_assessment(user_data):
    """Conduct focused career counseling questions only"""
    
    greeting = get_greeting()
    name = user_data.get('name', 'Student')
    
    print("\n" + "="*80)
    print(f"✨ Hey {name}, {greeting}!")
    print("="*80)
    print("\nI've already received your academic details from your profile.")
    print("Let me ask you some focused questions to provide the best career guidance.")
    print("="*80)
    
    # Show fetched data
    print("\n📊 YOUR PROFILE SUMMARY:")
    print(f"   Name: {user_data.get('name', 'N/A')}")
    print(f"   Gender: {user_data.get('gender', 'N/A')}")
    print(f"   District: {user_data.get('district', 'N/A')}")
    print(f"   School: {user_data.get('school_name', 'N/A')}")
    print(f"   10th Percentage: {user_data.get('10th_percentage', 'N/A')}%")
    print(f"   12th Stream: {user_data.get('12th_stream', 'N/A')}")
    print(f"   12th Percentage: {user_data.get('12th_percentage', 'N/A')}%")
    print(f"   Favorite Subject (10th): {user_data.get('fav_subject_10th', 'N/A')}")
    print(f"   Favorite Subject (12th): {user_data.get('fav_subject_12th', 'N/A')}")
    print(f"   Interests: {user_data.get('interests', 'N/A')}")
    print("="*80)
    
    responses = user_data.copy()
    
    # FOCUSED CAREER QUESTIONS
    print("\n" + "─"*80)
    print("🎯 CAREER COUNSELING QUESTIONS")
    print("─"*80)
    
    responses['career_goal'] = ask_question(
        "What is your primary career goal?",
        ["High-paying job in corporate sector",
         "Stable government job with benefits",
         "Start my own business/startup",
         "Social service & community development",
         "Research & academic career",
         "Creative field (arts, media, design)"]
    )
    
    responses['job_preference'] = ask_question(
        "Which type of work environment appeals to you?",
        ["Office/Corporate (9-5 job)",
         "Field work/On-site (travel, outdoor)",
         "Laboratory/Research facility",
         "Healthcare/Hospital setting",
         "Remote/Freelance",
         "Flexible/Mixed"]
    )
    
    responses['salary_vs_passion'] = ask_question(
        "What matters more to you?",
        ["High salary (even if not passionate)",
         "Passion & interest (even if moderate salary)",
         "Balance of both",
         "Job security over everything"]
    )
    
    responses['work_location_pref'] = ask_question(
        "Where would you prefer to work?",
        ["In J&K (close to home)",
         "Major Indian cities (Delhi, Mumbai, Bangalore)",
         "Abroad (international opportunities)",
         "Anywhere with good opportunity"]
    )
    
    responses['exam_preparation'] = ask_question(
        "Are you preparing for any competitive exam?",
        ["JEE (Engineering)", "NEET (Medical)", "CLAT (Law)",
         "UPSC/JKAS (Civil Services)", "CAT/MAT (Management)",
         "Banking/SSC exams", "Not preparing", "Other"]
    )
    
    responses['study_willingness'] = ask_question(
        "How many more years are you willing to study?",
        ["3 years (Bachelor's only)",
         "4-5 years (Professional degree)",
         "5-7 years (Master's/Specialization)",
         "Open to PhD/Long-term research"]
    )
    
    responses['financial_capacity'] = ask_question(
        "What is your family's budget for education?",
        ["Need free/affordable (< ₹50k/year)",
         "Can afford moderate (₹50k-2L/year)",
         "Can afford private (₹2L-5L/year)",
         "Budget not a constraint"]
    )
    
    responses['risk_appetite'] = ask_question(
        "How do you feel about taking career risks?",
        ["Very comfortable with risks & challenges",
         "Moderate risk is okay",
         "Prefer safe & stable path",
         "Completely risk-averse"]
    )
    
    responses['strength'] = ask_question(
        "What is your biggest strength?",
        ["Analytical & problem-solving",
         "Creative & innovative thinking",
         "Communication & people skills",
         "Technical & hands-on skills",
         "Leadership & management",
         "Hard work & dedication"]
    )
    
    responses['concern'] = ask_question(
        "What is your biggest career concern?",
        ["Job availability in chosen field",
         "Financial constraints for education",
         "Competition & difficulty level",
         "Family pressure/expectations",
         "Lack of proper guidance",
         "Confusion about interests"]
    )
    
    print("\n" + "="*80)
    print("✅ Assessment Complete!")
    print("="*80)
    
    return responses

def generate_comprehensive_guidance(responses, client):
    """Generate detailed career guidance with roadmap"""
    
    print("\n🔍 Analyzing your complete profile...")
    print("📊 Searching J&K career database...")
    print("🗺️  Creating personalized roadmap...")
    print("\nGenerating your career guidance report...\n")
    
    # Build profile
    profile = f"""
COMPLETE STUDENT PROFILE:
{'='*80}

PERSONAL & ACADEMIC:
- Name: {responses.get('name', 'N/A')}
- Gender: {responses.get('gender', 'N/A')}
- District: {responses.get('district', 'N/A')}
- School: {responses.get('school_name', 'N/A')}
- 10th Percentage: {responses.get('10th_percentage', 'N/A')}%
- 12th Stream: {responses.get('12th_stream', 'N/A')}
- 12th Percentage: {responses.get('12th_percentage', 'N/A')}%
- Favorite Subject (10th): {responses.get('fav_subject_10th', 'N/A')}
- Favorite Subject (12th): {responses.get('fav_subject_12th', 'N/A')}
- General Interests: {responses.get('interests', 'N/A')}

CAREER PREFERENCES:
- Career Goal: {responses.get('career_goal', 'N/A')}
- Work Environment: {responses.get('job_preference', 'N/A')}
- Priority: {responses.get('salary_vs_passion', 'N/A')}
- Work Location: {responses.get('work_location_pref', 'N/A')}
- Exam Preparation: {responses.get('exam_preparation', 'N/A')}
- Study Duration: {responses.get('study_willingness', 'N/A')}
- Financial Capacity: {responses.get('financial_capacity', 'N/A')}
- Risk Appetite: {responses.get('risk_appetite', 'N/A')}
- Biggest Strength: {responses.get('strength', 'N/A')}
- Main Concern: {responses.get('concern', 'N/A')}
"""
    
    # Search dataset
    search_terms = f"{responses.get('12th_stream', '')} {responses.get('fav_subject_12th', '')} {responses.get('interests', '')}"
    dataset_results = search_dataset(search_terms)
    
    # Enhanced prompt for detailed roadmap
    prompt = f"""You are an expert career counselor for J&K students with 20+ years of experience.

{profile}

J&K CAREER DATABASE RESULTS:
{dataset_results}

Provide a COMPREHENSIVE career guidance report with these MANDATORY sections:

1. **EXECUTIVE SUMMARY** (3-4 lines about student's profile)

2. **PRIMARY CAREER RECOMMENDATION**
   - Specific career title
   - Why perfect for this student (detailed reasoning)
   - Expected salary: Entry-level and 5-year experience (in INR)
   - Future growth prospects

3. **TOP 3 ALTERNATIVE CAREERS** (backup options with brief reasoning)

4. **DETAILED MONTH-BY-MONTH ROADMAP** (CRITICAL - MUST BE DETAILED)
   Example format:
   
   **IMMEDIATE (Next 3 Months):**
   - Month 1: [Specific actions]
   - Month 2: [Specific actions]
   - Month 3: [Specific actions]
   
   **SHORT TERM (3-12 Months):**
   - Months 4-6: [Specific milestones]
   - Months 7-12: [Specific milestones]
   
   **MEDIUM TERM (1-3 Years):**
   - Year 1: [Education/Training goals]
   - Year 2: [Skill development]
   - Year 3: [Career entry]
   
   **LONG TERM (3-5 Years):**
   - Years 3-5: [Career progression path]

5. **SPECIFIC J&K COLLEGES TO TARGET**
   - Top 3 colleges in J&K with admission process
   - Expected cutoffs/requirements
   - Why these specific colleges

6. **ENTRANCE EXAMS & PREPARATION**
   - Which exams to take
   - Expected scores needed
   - Preparation timeline and strategy

7. **SKILLS TO DEVELOP** (Technical + Soft skills with timeline)

8. **FINANCIAL PLANNING**
   - Total estimated cost
   - Specific scholarship names (J&K specific)
   - Education loan options

9. **J&K SPECIFIC OPPORTUNITIES**
   - Local government schemes
   - Regional industry opportunities
   - J&K quota benefits

10. **IF STUDENT DOESN'T CHOOSE PRIMARY PATH**
    - What are next best alternatives?
    - How to pivot?

11. **ADDRESSING STUDENT'S SPECIFIC CONCERN**
    - Direct answer to their stated concern
    - Practical solutions

Be SPECIFIC with names, dates, timelines. The roadmap MUST be detailed and actionable.
Use encouraging but realistic tone.
"""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert career counselor. Provide detailed, actionable roadmaps with specific timelines and steps."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3500,
            temperature=0.7
        )
        
        guidance = response.choices[0].message.content
        
        # Display in terminal
        print("\n" + "="*80)
        print(f"🌟 CAREER GUIDANCE REPORT FOR {responses.get('name', 'Student').upper()}")
        print("="*80)
        print(guidance)
        print("\n" + "="*80)
        
        # Optional save
        print("\n💾 Would you like to save this report?")
        save = input("Enter 'yes' to save or press Enter to skip: ").strip().lower()
        
        if save in ['yes', 'y']:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Career_Report_{responses.get('name', 'Student').replace(' ', '_')}_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("KASHMIR DISHA - CAREER GUIDANCE REPORT\\n")
                f.write("="*80 + "\\n\\n")
                f.write(profile)
                f.write("\\n" + "="*80 + "\\n\\n")
                f.write(guidance)
            
            print(f"✅ Saved as: {filename}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    if not os.path.exists(DATASET_PATH):
        print("❌ Dataset not found.")
        return
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
        )
        
        print("\n" + "="*80)
        print("🎓 KASHMIR DISHA - Professional Career Counseling (Firebase Edition)")
        print("="*80)
        
        # Get user ID
        user_id = input("\n👤 Enter your Student ID (from Firebase): ").strip()
        
        if not user_id:
            print("❌ Student ID required.")
            return
        
        # Fetch user data from Firebase
        print("\n🔄 Fetching your profile from database...")
        user_data = get_user_data_from_firebase(user_id)
        
        if not user_data:
            print("❌ Could not fetch user data. Please check your Student ID.")
            return
        
        # Conduct focused assessment
        responses = conduct_career_focused_assessment(user_data)
        
        # Generate guidance
        generate_comprehensive_guidance(responses, client)
        
        print("\n" + "="*80)
        print("🙏 Thank you for using Kashmir Disha!")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
