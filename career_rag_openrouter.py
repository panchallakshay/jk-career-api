import os
import subprocess
from openai import OpenAI
from datetime import datetime

# Firebase imports
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("⚠️  Firebase not installed. Run: pip3 install firebase-admin")

# --- CONFIGURATION ---
DATASET_PATH = 'Career_Knowledge_Master_JK_Augmented.csv'
MODEL_NAME = 'openai/gpt-3.5-turbo'
API_KEY = "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"
FIREBASE_KEY_PATH = 'firebase-key.json'

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

def initialize_firebase():
    """Initialize Firebase connection"""
    if not FIREBASE_AVAILABLE:
        return None
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_KEY_PATH)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"⚠️  Firebase initialization failed: {e}")
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
            raw_data = doc.to_dict()
            
            # Map Firebase fields to expected format (updated for new structure)
            user_data = {
                'name': raw_data.get('fullName') or raw_data.get('preferredName') or 'Student',
                'preferred_name': raw_data.get('preferredName') or raw_data.get('fullName') or 'Not specified',
                'gender': raw_data.get('gender') or 'Not specified',
                'district': raw_data.get('district') or 'Not specified',
                'state': raw_data.get('state') or 'Jammu & Kashmir',
                'school_name': raw_data.get('currentSchool') or raw_data.get('tenthSchool') or 'Not specified',
                '10th_percentage': raw_data.get('tenthMarks') or 'Not available',
                '12th_stream': raw_data.get('stream') or 'Not specified',
                '12th_percentage': raw_data.get('currentMarks') or 'Not available',
                'fav_subject_10th': raw_data.get('tenthFavSubject') or raw_data.get('tenthTopSubject') or 'Not specified',
                'fav_subject_12th': raw_data.get('favSubject11_12') or 'Not specified',
                'interests': ', '.join(raw_data.get('subjectsOfInterest', [])) if raw_data.get('subjectsOfInterest') else 'Not specified',
                'email': raw_data.get('email') or 'Not provided',
                'mobile': raw_data.get('mobile') or 'Not provided',
                'birth_year': str(raw_data.get('birthYear')) if raw_data.get('birthYear') else 'Not provided',
                'education_type': raw_data.get('educationType') or 'Class 12th',
                'education_status': raw_data.get('educationStatus') or 'appearing',
                'current_goal': raw_data.get('currentGoal') or 'Not specified',
                'other_plans': raw_data.get('otherPlans') or 'Not specified',
                'last_search': raw_data.get('lastSearch') or 'Not specified',
            }
            return user_data
        else:
            print(f"⚠️  No user found with ID: {user_id}")
            return None
    except Exception as e:
        print(f"❌ Error fetching user data: {e}")
        import traceback
        traceback.print_exc()
        return None

# --- TOOL DEFINITION ---
def search_dataset(query: str) -> str:
    """
    Searches the career dataset for relevant information using keywords.
    """
    print(f"\n[Tool] Searching dataset for: '{query}'...")
    
    keywords = [k for k in query.split() if len(k) > 3]
    if not keywords:
        keywords = [query]
        
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
                    matches.extend(new_matches[:5])
            except Exception:
                pass
    
    # Deduplicate and limit
    unique_matches = list(set(matches))[:20]
    
    if not unique_matches:
        return "No direct matches found in the dataset."
        
    return "\n".join(unique_matches)

SYSTEM_PROMPT = """You are 'KashmirDisha', an expert Career Counselor for students in J&K.

CRITICAL RULES:
1. When a user asks a career question, you MUST first search the dataset by calling the search_dataset function.
2. If the dataset returns results, answer ONLY using that data. Do not add outside information.
3. EXCEPTION: If search_dataset returns "No direct matches found", then use your general knowledge and start with: "⚠️ Note: This career is not in our local J&K database, but here is general guidance:"
4. Always emphasize J&K colleges (NIT Srinagar, GMC, etc.) when mentioned in the data.
"""

def conduct_career_assessment(user_data, client):
    """Conduct focused career counseling with user data from Firebase"""
    
    greeting = get_greeting()
    name = user_data.get('name', 'Student')
    
    print("\n" + "="*80)
    print(f"✨ Hey {name}, {greeting}!")
    print("="*80)
    print("\nI've retrieved your academic profile from the database.")
    print("Let me show you what I have and ask some focused career questions.")
    print("="*80)
    
    # Show fetched data
    print("\n📊 YOUR PROFILE:")
    print(f"   Full Name: {user_data.get('name', 'N/A')}")
    print(f"   Preferred Name: {user_data.get('preferred_name', 'N/A')}")
    print(f"   Email: {user_data.get('email', 'N/A')}")
    print(f"   Mobile: {user_data.get('mobile', 'N/A')}")
    print(f"   Birth Year: {user_data.get('birth_year', 'N/A')}")
    print(f"   Gender: {user_data.get('gender', 'N/A')}")
    print(f"   State: {user_data.get('state', 'N/A')}")
    print(f"   District: {user_data.get('district', 'N/A')}")
    print(f"   Current School: {user_data.get('school_name', 'N/A')}")
    print(f"   Education: {user_data.get('education_type', 'N/A')} ({user_data.get('education_status', 'N/A')})")
    print(f"   10th Marks: {user_data.get('10th_percentage', 'N/A')}")
    print(f"   10th Favorite Subject: {user_data.get('fav_subject_10th', 'N/A')}")
    print(f"   12th Stream: {user_data.get('12th_stream', 'N/A')}")
    print(f"   12th Marks: {user_data.get('12th_percentage', 'N/A')}")
    print(f"   12th Favorite Subject: {user_data.get('fav_subject_12th', 'N/A')}")
    print(f"   Subjects of Interest: {user_data.get('interests', 'N/A')}")
    print(f"   Current Goal: {user_data.get('current_goal', 'N/A')}")
    print(f"   Other Plans: {user_data.get('other_plans', 'N/A')}")
    print(f"   Last Search: {user_data.get('last_search', 'N/A')}")
    print("="*80)
    
    # Build comprehensive profile for AI
    profile = f"""
STUDENT PROFILE (From Database):
- Name: {user_data.get('name', 'N/A')}
- Gender: {user_data.get('gender', 'N/A')}
- District (J&K): {user_data.get('district', 'N/A')}
- School: {user_data.get('school_name', 'N/A')}
- 10th Percentage: {user_data.get('10th_percentage', 'N/A')}%
- 12th Stream: {user_data.get('12th_stream', 'N/A')}
- 12th Percentage: {user_data.get('12th_percentage', 'N/A')}%
- Favorite Subject (10th): {user_data.get('fav_subject_10th', 'N/A')}
- Favorite Subject (12th): {user_data.get('fav_subject_12th', 'N/A')}
- General Interests: {user_data.get('interests', 'N/A')}
"""
    
    # Search dataset based on profile
    search_terms = f"{user_data.get('12th_stream', '')} {user_data.get('fav_subject_12th', '')} {user_data.get('interests', '')}"
    dataset_results = search_dataset(search_terms)
    
    # Enhanced system prompt for career counseling
    system_prompt = f"""You are NavRiti AI, an expert career counselor for J&K students with 20+ years of experience.

{profile}

J&K CAREER DATABASE:
{dataset_results}

CRITICAL INSTRUCTIONS:
- Write in PROPER ENGLISH ONLY (no Hinglish, no spelling errors)
- This is a 15-minute professional career guidance session
- Be INTERACTIVE and CONVERSATIONAL - acknowledge their previous answers
- Build on previous responses to ask relevant follow-up questions
- Show empathy and understanding
- Make the student feel heard and understood

YOUR TASK: Conduct an interactive 10-question career counseling session.

CONVERSATION STYLE:
- After each answer, acknowledge what they said before asking the next question
- Example: "I see you're interested in government jobs. That's a stable choice! Now, regarding..."
- Reference their previous answers when relevant
- Be encouraging and supportive
- Use their name occasionally to make it personal

ASK THESE 10 QUESTIONS (adapt based on their answers):

1. **Career Goal**: 
   "{user_data.get('name')}, based on your {user_data.get('12th_stream')} background and interest in {user_data.get('interests')}, what is your primary career goal after 12th?"
   Options: Government job, Private sector, Business/Startup, Higher studies & Research, Still exploring

2. **Motivation** (acknowledge their goal first):
   "That's interesting! Now, what matters most to you in a career?"
   Options: High salary, Job security, Passion/Interest, Social impact, Work-life balance

3. **Work Environment** (connect to their motivation):
   "Given your priorities, what type of work environment appeals to you?"
   Options: Office/Corporate, Field work/Outdoor, Laboratory/Research, Healthcare/Hospital, Remote/Freelance, Creative studio

4. **Location Preference** (acknowledge their environment choice):
   "I understand. Where would you prefer to work?"
   Options: Stay in J&K (close to home), Major Indian cities, Abroad, Anywhere with good opportunity

5. **Exam Preparation** (connect to their goals):
   "Based on your career goal, are you currently preparing or planning to prepare for any competitive exam?"
   Options: JEE (Engineering), NEET (Medical), CUET (Central Universities), CLAT (Law), CAT/MAT (Management), UPSC/JKAS (Civil Services), Banking/SSC, Not preparing

6. **Study Duration** (acknowledge exam prep status):
   "I see. How many more years are you willing to study after 12th?"
   Options: 3 years (Bachelor's only), 4-5 years (Professional degree), 5-7 years (Master's/Specialization), Open to PhD/Research

7. **Financial Capacity** (be sensitive):
   "Thank you for sharing. What is your family's realistic budget for higher education per year?"
   Options: Less than ₹25,000 (Need GDC/Free education), ₹25,000-₹1,00,000 (Moderate fees), ₹1,00,000-₹3,00,000 (Private colleges), Above ₹3,00,000 (No constraint)

8. **Scholarship Interest** (connect to their budget):
   "That helps me understand. Are you interested in applying for scholarships and education loans?"
   Options: Yes, actively looking, Yes, if available, Will take loan if needed, No, not needed

9. **Biggest Strength** (be encouraging):
   "Great! What would you say is your biggest strength?"
   Options: Analytical/Problem-solving, Creative/Innovative, Communication/People skills, Technical/Hands-on, Leadership/Management, Hard work/Dedication

10. **Main Concern** (show empathy):
    "I appreciate your honesty. What is your biggest concern about choosing a career?"
    Options: Job availability, Financial constraints, High competition, Family pressure, Lack of guidance, Confusion about interests

AFTER ALL 10 ANSWERS, YOU MUST:

1. **Summarize their profile** in 2-3 sentences acknowledging their journey
2. **Recommend ONE specific course** (B.Tech in [Branch], B.Sc in [Subject], BBA, BA, B.Com, MBBS, etc.)
3. **Explain WHY** this course matches their profile (200 words)
4. **Provide 2-3 alternative courses**
5. **Give detailed roadmap** (month-by-month for 12 months, then yearly)
6. **List specific J&K colleges** (GDCs first, with exact fees)
7. **Recommend entrance exams** and preparation strategy
8. **Suggest scholarships** they're eligible for (with amounts)
9. **Provide resources** (YouTube, books, websites, apps)
10. **Address their specific concern** mentioned in question 10

IMPORTANT:
- Ask ONE question at a time
- ALWAYS acknowledge their previous answer before asking next question
- Be warm, professional, and encouraging
- Reference their profile (stream, subjects, interests) when relevant
- Make them feel this is a personalized conversation, not a form
- Use PROPER ENGLISH spelling throughout"""



    
    # Start conversation
    messages = [{"role": "system", "content": system_prompt}]
    
    print("\n💬 Let's begin the career counseling session!")
    print("(Type 'done' when you want the final roadmap and guidance)")
    print("--------------------------------------------------")
    
    question_count = 0
    
    while True:
        if question_count == 0:
            # AI asks first question
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages + [{
                        "role": "user",
                        "content": "Please start the career counseling by asking me about my primary career goal."
                    }],
                    max_tokens=200
                )
                ai_message = response.choices[0].message.content
                messages.append({"role": "assistant", "content": ai_message})
                print(f"\nCounselor: {ai_message}")
                question_count += 1
            except Exception as e:
                print(f"❌ Error: {e}")
                break
        
        # Get user response
        user_input = input(f"\n{name}: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Session ended. Best of luck!")
            break
        
        if user_input.lower() == 'done' or question_count >= 10:
            # Generate final comprehensive guidance
            print("\n🔍 Analyzing your complete profile...")
            print("🗺️  Generating your personalized career roadmap...")
            print("\nThis may take a moment...\n")
            
            # Search for colleges based on recommended course
            print("🏫 Searching J&K colleges for recommended courses...")
            college_search = search_dataset("B.Sc IT BCA Computer")  # Search for tech-related colleges
            
            final_prompt = f"""You are providing a PROFESSIONAL 15-MINUTE CAREER GUIDANCE SESSION. Based on our conversation, generate a comprehensive report.

CRITICAL REQUIREMENTS:
- Write in PROPER ENGLISH ONLY (no Hinglish, no spelling errors)
- Be PROFESSIONAL, CONCISE, and ACTIONABLE
- This must be completable in 15 minutes of reading
- DO NOT use markdown formatting (no **, no #, no asterisks)
- Use PLAIN TEXT with clear section headers in CAPS
- Use simple dashes (-) for bullet points

STUDENT PROFILE SUMMARY:
- Stream: {user_data.get('12th_stream')}
- 12th Percentage: {user_data.get('12th_percentage')}%
- 10th Percentage: {user_data.get('10th_percentage')}%
- Favorite Subject: {user_data.get('fav_subject_12th')}
- Interests: {user_data.get('interests')}
- District: {user_data.get('district')}

J&K COLLEGES DATABASE:
{college_search}

MANDATORY REPORT STRUCTURE:

1. RECOMMENDED COURSE (CRITICAL - 250 words):
   
   Course Name: [Specify EXACTLY: B.Tech in Computer Science, B.Sc in IT, BBA, BA in Economics, MBBS, etc.]
   
   Why This Course is Perfect for You:
   - Based on {user_data.get('12th_stream')} stream
   - Your {user_data.get('12th_percentage')} in 12th and {user_data.get('10th_percentage')} in 10th
   - Your interest in {user_data.get('fav_subject_12th')} and {user_data.get('interests')}
   - Your career goal and strengths from our conversation
   - Job market demand and salary potential
   
   Career Outcomes: What jobs you'll get after this course

2. ALTERNATIVE COURSES (2-3 backup options):
   - Course 1: [Specific name] - Why suitable
   - Course 2: [Specific name] - Why suitable
   - Course 3: [Specific name] - Why suitable

3. 12-MONTH ROADMAP (Month-by-month):
   
   IMMEDIATE (Month 1-3):
   - Month 1: [Specific daily tasks, 2-3 hours/day]
   - Month 2: [Specific daily tasks, 2-3 hours/day]
   - Month 3: [Specific daily tasks, 2-3 hours/day]
   
   SHORT TERM (Month 4-6):
   - [Quarterly goals and milestones]
   
   MEDIUM TERM (Month 7-9):
   - [Quarterly goals and milestones]
   
   LONG TERM (Month 10-12):
   - [Quarterly goals and milestones]
   
   Year 2-3: [Annual goals]
   Year 3-5: [Career progression]

4. J&K COLLEGES - GDCs FIRST (CRITICAL - Use the database above):
   
   GOVERNMENT DEGREE COLLEGES in {user_data.get('district')} and nearby (TOP PRIORITY):
   - List 5-7 specific GDCs from the database with EXACT details:
     * GDC [Name], [District] - Fees: Rs.[exact amount], Courses: [list], Hostel: [Yes/No]
     * Include contact info if available
   
   Why GDCs: Rs.5,000-12,000/year fees, quality education, close to home
   
   CENTRAL UNIVERSITIES:
   - University of Kashmir, CUK, CUJ, IUST (with fees and courses)
   
   PREMIUM INSTITUTIONS (if percentile allows):
   - NIT Srinagar (Rs.1,46,000/year, JEE Main 85+ percentile)
   - IIT Jammu (Rs.2,00,000/year, JEE Advanced)

5. ENTRANCE EXAMS:
   - Which exam: [JEE/NEET/CUET/etc.]
   - Expected score: [Percentile/Rank needed]
   - Preparation: [Hours/day, coaching vs self-study]
   - Timeline: [When to start, key dates]

6. SCHOLARSHIPS (Be VERY specific):
   
   BASED ON JEE/NEET/CUET PERCENTILE:
   - 90+ percentile: INSPIRE Scholarship (Rs.80,000/year), [Others with amounts]
   - 80-90 percentile: [Specific scholarships with Rs.amounts]
   - 70-80 percentile: [Specific scholarships with Rs.amounts]
   
   J&K GOVERNMENT SCHEMES:
   - J&K Merit Scholarship: Rs.20,000-30,000/year, Eligibility: 60%+ in 12th
   - PM Scholarship for J&K: Rs.2,500/month, Eligibility: Family income < Rs.6 lakh
   - SC/ST/OBC scholarships: Rs.10,000-25,000/year
   
   EDUCATION LOANS:
   - J&K Bank: 8-10% interest, up to Rs.10 lakh
   - Collateral-free: Up to Rs.7.5 lakh

7. RESOURCES TO START TODAY:
   - YouTube: [3-5 specific channel names for the recommended course]
   - Books: [3-5 specific book titles]
   - Websites: [3-5 specific websites]
   - Apps: [3-5 specific app names]
   - Practice: [Platforms like HackerRank, Khan Academy, etc.]

8. SKILLS TO DEVELOP (with 6-month timeline):
   - Technical: [Specific skills for the course]
   - Soft: [Communication, leadership, etc.]
   - Certifications: [Specific cert names]

9. TOTAL COST & FINANCIAL PLAN:
   - 3-year cost at GDC: Rs.[total based on Rs.7,000-12,000/year]
   - Scholarships available: -Rs.[amount]
   - Net cost: Rs.[amount]
   - Loan if needed: Rs.[amount]

10. BACKUP PLAN (if primary doesn't work):
    - Plan A: [Specific alternative course and colleges]
    - Plan B: [Specific alternative course and colleges]

FORMAT: Use clear headings in CAPS, bullet points with dashes, be CONCISE. NO markdown formatting. Total reading time: 15 minutes max."""

            
            try:
                final_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages + [{"role": "user", "content": final_prompt}],
                    max_tokens=3500
                )
                
                guidance = final_response.choices[0].message.content
                
                print("\n" + "="*80)
                print(f"🌟 CAREER GUIDANCE REPORT FOR {name.upper()}")
                print("="*80)
                print(guidance)
                print("\n" + "="*80)
                
                # Add guidance to messages for follow-up questions
                messages.append({"role": "assistant", "content": guidance})
                
                # Optional save
                save = input("\n💾 Save this report? (yes/no): ").strip().lower()
                if save in ['yes', 'y']:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"Career_Report_{name.replace(' ', '_')}_{timestamp}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"KASHMIR DISHA - CAREER GUIDANCE\n{'='*80}\n\n")
                        f.write(profile)
                        f.write(f"\n{'='*80}\n\n")
                        f.write(guidance)
                    print(f"✅ Saved as: {filename}")
                
                # Follow-up Q&A Session
                print("\n" + "="*80)
                print("❓ DO YOU HAVE ANY QUESTIONS OR DOUBTS?")
                print("="*80)
                print(f"\n{name}, do you have any questions about your career guidance report?")
                print("\nYou can ask about:")
                print("  • Specific colleges or admission process")
                print("  • Scholarship details or financial planning")
                print("  • Study resources or preparation tips")
                print("  • Alternative career options")
                print("  • Anything else related to your career path")
                print("\nType your question, or type 'no' if you're all set!")
                print("─"*80)
                
                while True:
                    follow_up = input(f"\n{name}: ").strip()
                    
                    if follow_up.lower() in ['exit', 'quit', 'no', 'done']:
                        print(f"\n✅ Great! Best of luck with your career journey, {name}!")
                        break
                    
                    if not follow_up:
                        continue
                    
                    # Add context reminder for AI
                    follow_up_with_context = f"Based on the career guidance report I just provided, the student asks: {follow_up}"
                    messages.append({"role": "user", "content": follow_up_with_context})
                    
                    try:
                        follow_up_response = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=messages,
                            max_tokens=800
                        )
                        
                        answer = follow_up_response.choices[0].message.content
                        messages.append({"role": "assistant", "content": answer})
                        print(f"\nCounselor: {answer}")
                        
                    except Exception as e:
                        print(f"❌ Error: {e}")
                        messages.pop()
                
            except Exception as e:
                print(f"❌ Error: {e}")
            
            break
        
        if not user_input:
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        # AI responds and asks next question
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=300
            )
            
            ai_message = response.choices[0].message.content
            messages.append({"role": "assistant", "content": ai_message})
            print(f"\nCounselor: {ai_message}")
            question_count += 1
            
        except Exception as e:
            print(f"❌ Error: {e}")
            messages.pop()

def main():
    """Main function with Firebase integration"""
    if not os.path.exists(DATASET_PATH):
        print("❌ Dataset not found.")
        return
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
        )
        
        greeting = get_greeting()
        print("\n" + "="*80)
        print(f"🎓 {greeting}! Welcome to NAVRITI AI")
        print("Professional Career Counseling with Database Integration")
        print("="*80)
        
        # Check if Firebase is available
        if FIREBASE_AVAILABLE and os.path.exists(FIREBASE_KEY_PATH):
            print("\n🔥 Firebase Mode: Fetching your profile from database...")
            user_id = input("\n👤 Enter your Student ID: ").strip()
            
            if user_id:
                user_data = get_user_data_from_firebase(user_id)
                
                if user_data:
                    # Conduct assessment with Firebase data
                    conduct_career_assessment(user_data, client)
                else:
                    print("❌ Could not fetch user data. Please check your Student ID.")
            else:
                print("❌ Student ID required.")
        else:
            print("\n⚠️  Firebase not configured. Please set up firebase-key.json")
            print("See FIREBASE_SETUP.md for instructions.")
        
        print("\n" + "="*80)
        print("🙏 Thank you for using NavRiti AI!")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Session interrupted.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
