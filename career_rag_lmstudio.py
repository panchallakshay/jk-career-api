import os
import subprocess
from openai import OpenAI
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONFIGURATION ---
DATASET_PATH = 'Career_Knowledge_Master_JK_Augmented.csv'
FIREBASE_KEY_PATH = 'firebase-key.json'

# LM Studio Configuration
LM_STUDIO_URL = "http://localhost:1234/v1"  # LM Studio local server
MODEL_NAME = "local-model"  # LM Studio uses this as placeholder

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
            
            user_data = {
                'name': raw_data.get('fullName') or raw_data.get('preferredName') or 'Student',
                'preferred_name': raw_data.get('preferredName') or raw_data.get('fullName') or 'Not specified',
                'gender': raw_data.get('gender') or 'Not specified',
                'district': raw_data.get('district') or 'Not specified',
                'state': raw_data.get('state') or 'Jammu & Kashmir',
                'school_name': raw_data.get('schoolName') or 'Not specified',
                '10th_percentage': raw_data.get('10th_percentage') or 'Not available',
                '12th_stream': raw_data.get('streamOrBranch') or 'Not specified',
                '12th_percentage': raw_data.get('percentageOrCgpa') or 'Not available',
                'fav_subject_10th': raw_data.get('fav_subject_10th') or 'Not specified',
                'fav_subject_12th': raw_data.get('fav_subject_12th') or 'Not specified',
                'interests': raw_data.get('interests') or 'Not specified',
                'email': raw_data.get('email') or 'Not provided',
                'mobile': raw_data.get('mobile') or 'Not provided',
                'dob': str(raw_data.get('dob')) if raw_data.get('dob') else 'Not provided',
                'education_type': raw_data.get('educationType') or 'class12',
                'education_status': raw_data.get('educationStatus') or 'appearing',
            }
            return user_data
        else:
            print(f"⚠️  No user found with ID: {user_id}")
            return None
    except Exception as e:
        print(f"❌ Error fetching user data: {e}")
        return None

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
    return "\n".join(unique_matches) if unique_matches else "No direct matches found in the dataset."

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
    print(f"   Gender: {user_data.get('gender', 'N/A')}")
    print(f"   State: {user_data.get('state', 'N/A')}")
    print(f"   District: {user_data.get('district', 'N/A')}")
    print(f"   Education: {user_data.get('education_type', 'N/A')} ({user_data.get('education_status', 'N/A')})")
    print(f"   12th Stream: {user_data.get('12th_stream', 'N/A')}")
    print(f"   12th %: {user_data.get('12th_percentage', 'N/A')}")
    print("="*80)
    
    # Build comprehensive profile for AI
    profile = f"""
STUDENT PROFILE (From Database):
- Name: {user_data.get('name')}
- Gender: {user_data.get('gender')}
- District (J&K): {user_data.get('district')}
- State: {user_data.get('state')}
- 12th Stream: {user_data.get('12th_stream')}
- 12th Percentage: {user_data.get('12th_percentage')}
- Interests: {user_data.get('interests')}
"""
    
    # Search dataset
    search_terms = f"{user_data.get('12th_stream', '')} {user_data.get('interests', '')}"
    dataset_results = search_dataset(search_terms)
    
    # System prompt
    system_prompt = f"""You are NavRiti AI, an expert career counselor for J&K students with 20+ years of experience.

{profile}

J&K CAREER DATABASE:
{dataset_results}

Provide helpful, personalized career guidance. Be encouraging, professional, and specific.
Ask ONE question at a time to understand the student's career goals."""
    
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
                    max_tokens=200,
                    temperature=0.7
                )
                ai_message = response.choices[0].message.content
                messages.append({"role": "assistant", "content": ai_message})
                print(f"\nCounselor: {ai_message}")
                question_count += 1
            except Exception as e:
                print(f"❌ Error: {e}")
                print("\n⚠️  Make sure LM Studio server is running on http://localhost:1234")
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
            print("\nThis may take a moment (local AI processing)...\n")
            
            final_prompt = f"""Based on our conversation, generate a comprehensive career guidance report.

STUDENT PROFILE:
{profile}

Provide a detailed report with:
1. RECOMMENDED COURSE (specific name like B.Tech in Computer Science)
2. Why this course matches their profile
3. ALTERNATIVE COURSES (2-3 options)
4. 12-MONTH ROADMAP (month-by-month plan)
5. J&K COLLEGES (Government Degree Colleges first)
6. ENTRANCE EXAMS needed
7. SCHOLARSHIPS available
8. SKILLS TO DEVELOP
9. RESOURCES (YouTube, books, websites)

Use PLAIN TEXT format, NO markdown. Be specific and actionable."""
            
            try:
                final_response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages + [{"role": "user", "content": final_prompt}],
                    max_tokens=2000,
                    temperature=0.7
                )
                
                guidance = final_response.choices[0].message.content
                
                print("\n" + "="*80)
                print(f"🌟 CAREER GUIDANCE REPORT FOR {name.upper()}")
                print("="*80)
                print(guidance)
                print("\n" + "="*80)
                
                # Optional save
                save = input("\n💾 Save this report? (yes/no): ").strip().lower()
                if save in ['yes', 'y']:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"Career_Report_{name.replace(' ', '_')}_{timestamp}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"KASHMIR DISHA - CAREER GUIDANCE (LM Studio)\n{'='*80}\n\n")
                        f.write(profile)
                        f.write(f"\n{'='*80}\n\n")
                        f.write(guidance)
                    print(f"✅ Saved as: {filename}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
            
            break
        
        if not user_input:
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        # AI responds
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            ai_message = response.choices[0].message.content
            messages.append({"role": "assistant", "content": ai_message})
            print(f"\nCounselor: {ai_message}")
            question_count += 1
            
        except Exception as e:
            print(f"❌ Error: {e}")
            messages.pop()

def main():
    """Main function with LM Studio integration"""
    if not os.path.exists(DATASET_PATH):
        print("❌ Dataset not found.")
        return
    
    try:
        # Initialize OpenAI client pointing to LM Studio
        client = OpenAI(
            base_url=LM_STUDIO_URL,
            api_key="not-needed"  # LM Studio doesn't need API key
        )
        
        # Test LM Studio connection
        try:
            client.models.list()
            print("✅ Connected to LM Studio successfully!")
        except Exception as e:
            print("❌ Cannot connect to LM Studio!")
            print(f"Error: {e}")
            print("\n⚠️  Make sure:")
            print("1. LM Studio is running")
            print("2. Local server is started (port 1234)")
            print("3. A model is loaded")
            return
        
        greeting = get_greeting()
        print("\n" + "="*80)
        print(f"🎓 {greeting}! Welcome to NAVRITI AI (LM Studio Edition)")
        print("Professional Career Counseling with Local AI")
        print("="*80)
        
        user_id = input("\n👤 Enter your Student ID: ").strip()
        
        if not user_id:
            print("❌ Student ID required.")
            return
        
        print("\n🔄 Fetching your profile from database...")
        user_data = get_user_data_from_firebase(user_id)
        
        if not user_data:
            print("❌ Could not fetch user data. Please check your Student ID.")
            return
        
        # Conduct assessment
        conduct_career_assessment(user_data, client)
        
        print("\n" + "="*80)
        print("🙏 Thank you for using NavRiti AI!")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Session interrupted.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
