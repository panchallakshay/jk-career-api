import os
import subprocess
from openai import OpenAI
from datetime import datetime

# --- CONFIGURATION ---
DATASET_PATH = 'Career_Knowledge_Master_JK_Augmented.csv'
MODEL_NAME = 'openai/gpt-3.5-turbo'
API_KEY = "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"

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
    """Search the career dataset for relevant information"""
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

def ask_question(question, options=None, question_type="text"):
    """Ask a question and get response"""
    print(f"\n💬 {question}")
    
    if options:
        for i, opt in enumerate(options, 1):
            print(f"   {i}. {opt}")
    
    while True:
        if question_type == "number":
            answer = input("\n👉 Your answer (enter number): ").strip()
        else:
            answer = input("\n👉 Your answer: ").strip()
        
        if answer:
            return answer
        print("⚠️  Please provide an answer.")

def conduct_assessment():
    """Conduct comprehensive 25-30 question assessment"""
    
    # Initial Greeting
    greeting = get_greeting()
    print("\n" + "="*80)
    print(f"🎓 {greeting}! Welcome to KASHMIR DISHA - Professional Career Counseling")
    print("="*80)
    print("\nI'm your personal career counselor, here to guide you towards the best")
    print("career path based on your unique profile, interests, and circumstances.")
    print("\nThis assessment will take about 10-15 minutes. Please answer honestly.")
    print("="*80)
    
    responses = {}
    
    # Get name first
    responses['name'] = ask_question("What is your name?")
    
    # Personalized greeting with name
    print("\n" + "="*80)
    print(f"✨ Hey {responses['name']}, {greeting}!")
    print(f"Great to have you here! Let's find the perfect career path for you.")
    print("="*80)
    
    # SECTION 1: BASIC INFORMATION
    print("\n" + "─"*80)
    print("📋 SECTION 1: BASIC INFORMATION")
    print("─"*80)
    
    responses['education_status'] = ask_question(
        "Are you currently studying in 12th class or have you already passed?",
        ["Currently in 12th", "Passed 12th", "Passed 12th and taking a gap year"],
        "choice"
    )
    
    responses['stream'] = ask_question(
        "What stream did you choose/are you choosing in 12th?",
        ["Science (PCM - Physics, Chemistry, Mathematics)",
         "Science (PCB - Physics, Chemistry, Biology)", 
         "Commerce",
         "Arts/Humanities"],
        "choice"
    )
    
    responses['12th_percentage'] = ask_question(
        "What is/was your percentage in 12th? (If currently studying, expected %)",
        ["Above 90%", "80-90%", "70-80%", "60-70%", "Below 60%"],
        "choice"
    )
    
    responses['10th_percentage'] = ask_question(
        "What was your percentage in 10th class?",
        ["Above 90%", "80-90%", "70-80%", "60-70%", "Below 60%"],
        "choice"
    )
    
    # SECTION 2: LOCATION & BACKGROUND
    print("\n" + "─"*80)
    print("📍 SECTION 2: LOCATION & BACKGROUND")
    print("─"*80)
    
    responses['region'] = ask_question(
        "Which region of J&K are you from?",
        ["Kashmir Valley (Srinagar, Anantnag, Baramulla, etc.)",
         "Jammu Division (Jammu, Udhampur, Kathua, etc.)",
         "Ladakh (Leh, Kargil)"],
        "choice"
    )
    
    responses['district'] = ask_question(
        "Which district do you belong to?",
        ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Budgam", "Pulwama", 
         "Shopian", "Udhampur", "Kathua", "Leh", "Kargil", "Other"],
        "choice"
    )
    
    responses['school_type'] = ask_question(
        "What type of school did you attend?",
        ["Government School", "Private School", "Central School (KV/JNV)"],
        "choice"
    )
    
    # SECTION 3: INTERESTS & APTITUDE
    print("\n" + "─"*80)
    print("💡 SECTION 3: INTERESTS & APTITUDE")
    print("─"*80)
    
    responses['subjects_enjoyed'] = ask_question(
        "Which subjects did you enjoy the most in school?",
        ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
         "English", "Economics", "History", "Geography", "Arts/Drawing"],
        "choice"
    )
    
    responses['subjects_good_at'] = ask_question(
        "Which subjects were you best at academically?",
        ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
         "English", "Economics", "History", "Geography", "Arts/Drawing"],
        "choice"
    )
    
    responses['hobbies'] = ask_question(
        "What are your hobbies or activities you enjoy?",
        ["Reading/Writing", "Sports/Fitness", "Coding/Technology", 
         "Art/Design", "Music/Dance", "Gaming", "Social Work", "Other"],
        "choice"
    )
    
    responses['skills'] = ask_question(
        "Do you have any special skills?",
        ["Coding/Programming", "Art/Design", "Sports", "Languages", 
         "Public Speaking", "Leadership", "None specific", "Other"],
        "choice"
    )
    
    responses['career_interest_area'] = ask_question(
        "Which career area interests you the most?",
        ["Technology & IT", "Medicine & Healthcare", "Engineering & Construction",
         "Business & Management", "Government & Civil Services", "Arts & Design",
         "Law & Legal Studies", "Teaching & Education", "Agriculture & Environment",
         "Media & Journalism", "Not sure yet"],
        "choice"
    )
    
    # SECTION 4: CAREER GOALS & PREFERENCES
    print("\n" + "─"*80)
    print("🎯 SECTION 4: CAREER GOALS & PREFERENCES")
    print("─"*80)
    
    responses['career_priority'] = ask_question(
        "What is your top priority in a career?",
        ["High salary & growth", "Job security & stability", 
         "Work-life balance", "Social impact & service",
         "Creativity & innovation", "Prestige & recognition"],
        "choice"
    )
    
    responses['job_type'] = ask_question(
        "What type of job appeals to you more?",
        ["Government job (stable, pension, benefits)",
         "Private sector job (higher salary, fast growth)",
         "Entrepreneurship/Own business",
         "Freelancing/Consulting",
         "Not decided yet"],
        "choice"
    )
    
    responses['startup_interest'] = ask_question(
        "Are you interested in starting your own business/startup?",
        ["Yes, very interested", "Maybe in the future", 
         "No, prefer employment", "Not sure"],
        "choice"
    )
    
    responses['work_location'] = ask_question(
        "Where would you prefer to work?",
        ["In J&K (stay close to home)",
         "Anywhere in India (willing to relocate)",
         "Abroad (international opportunities)",
         "Flexible/Open to all"],
        "choice"
    )
    
    # SECTION 5: EDUCATION PREFERENCES
    print("\n" + "─"*80)
    print("🏫 SECTION 5: EDUCATION PREFERENCES")
    print("─"*80)
    
    responses['college_preference'] = ask_question(
        "What is your preference for higher education?",
        ["Government College in J&K (GDC, NIT Srinagar, GMC, etc.)",
         "Central University (CUK, CUJ, IIT Jammu, AIIMS)",
         "Top colleges outside J&K (IITs, NITs, AIIMS, IIMs)",
         "Private colleges in J&K",
         "Private colleges outside J&K",
         "Online/Distance education"],
        "choice"
    )
    
    responses['exam_preparation'] = ask_question(
        "Are you preparing for any competitive exam?",
        ["JEE (Engineering)", "NEET (Medical)", "CLAT (Law)",
         "UPSC/JKAS (Civil Services)", "CAT/MAT (Management)",
         "Banking exams (IBPS, SBI)", "SSC/Railway exams",
         "Not preparing for any", "Other"],
        "choice"
    )
    
    responses['study_duration'] = ask_question(
        "How long are you willing to study after 12th?",
        ["3 years (Bachelor's)", "4-5 years (Bachelor's + Professional)",
         "5+ years (Bachelor's + Master's)", "Open to PhD/Research"],
        "choice"
    )
    
    # SECTION 6: FINANCIAL SITUATION
    print("\n" + "─"*80)
    print("💰 SECTION 6: FINANCIAL SITUATION")
    print("─"*80)
    
    responses['financial_capacity'] = ask_question(
        "What is your family's capacity for education expenses?",
        ["Need free/very affordable education (< ₹25k/year)",
         "Can afford moderate fees (₹25k - ₹1L/year)",
         "Can afford private college (₹1L - ₹3L/year)",
         "Can afford premium education (₹3L+/year)",
         "Prefer scholarship/education loan"],
        "choice"
    )
    
    responses['scholarship_interest'] = ask_question(
        "Are you interested in applying for scholarships?",
        ["Yes, actively looking", "Yes, if available", "No, not needed"],
        "choice"
    )
    
    # SECTION 7: PERSONALITY & WORK STYLE
    print("\n" + "─"*80)
    print("🧠 SECTION 7: PERSONALITY & WORK STYLE")
    print("─"*80)
    
    responses['personality'] = ask_question(
        "How would you describe yourself?",
        ["Analytical & logical thinker", "Creative & artistic",
         "People-oriented & social", "Practical & hands-on",
         "Leader & decision-maker", "Detail-oriented & organized"],
        "choice"
    )
    
    responses['work_environment'] = ask_question(
        "What work environment suits you best?",
        ["Office/Corporate setting", "Field work/Outdoor",
         "Laboratory/Research facility", "Creative studio",
         "Remote/Work from home", "Mix of all"],
        "choice"
    )
    
    responses['stress_handling'] = ask_question(
        "How do you handle pressure and deadlines?",
        ["Thrive under pressure", "Work well with moderate pressure",
         "Prefer low-stress environment", "Depends on the situation"],
        "choice"
    )
    
    # SECTION 8: ADDITIONAL INFORMATION
    print("\n" + "─"*80)
    print("📝 SECTION 8: ADDITIONAL INFORMATION")
    print("─"*80)
    
    responses['role_models'] = ask_question(
        "Do you have any career role models?",
        ["Yes, specific person/profession", "No specific role model", 
         "Inspired by family member", "Inspired by public figure"],
        "choice"
    )
    
    responses['family_expectations'] = ask_question(
        "What are your family's expectations regarding your career?",
        ["Supportive of my choice", "Want me to pursue specific field",
         "Prefer government job", "Want high-paying career",
         "No specific expectations"],
        "choice"
    )
    
    responses['biggest_concern'] = ask_question(
        "What is your biggest concern about choosing a career?",
        ["Job availability/market", "Financial constraints",
         "Competition/difficulty", "Family pressure",
         "Lack of guidance", "Not sure about interests"],
        "choice"
    )
    
    responses['confidence_level'] = ask_question(
        "How confident are you about your career choice?",
        ["Very confident", "Somewhat confident", 
         "Not very confident", "Completely confused"],
        "choice"
    )
    
    print("\n" + "="*80)
    print("✅ Assessment Complete! Thank you for your detailed responses.")
    print("="*80)
    
    return responses

def generate_professional_guidance(responses, client):
    """Generate comprehensive professional career guidance"""
    
    print("\n🔍 Analyzing your profile...")
    print("📊 Searching J&K career database...")
    print("🤖 Generating personalized roadmap...")
    print("\nThis may take a minute. Please wait...\n")
    
    # Build comprehensive profile
    profile = f"""
STUDENT PROFILE - KASHMIR DISHA CAREER ASSESSMENT
{'='*80}

PERSONAL INFORMATION:
- Name: {responses.get('name', 'N/A')}
- Education Status: {responses.get('education_status', 'N/A')}
- Stream: {responses.get('stream', 'N/A')}
- 12th Percentage: {responses.get('12th_percentage', 'N/A')}%
- 10th Percentage: {responses.get('10th_percentage', 'N/A')}%

LOCATION & BACKGROUND:
- Region: {responses.get('region', 'N/A')}
- District: {responses.get('district', 'N/A')}
- School Type: {responses.get('school_type', 'N/A')}

INTERESTS & APTITUDE:
- Enjoyed Subjects: {responses.get('subjects_enjoyed', 'N/A')}
- Strong Subjects: {responses.get('subjects_good_at', 'N/A')}
- Hobbies: {responses.get('hobbies', 'N/A')}
- Special Skills: {responses.get('skills', 'N/A')}
- Career Interest Area: {responses.get('career_interest_area', 'N/A')}

CAREER GOALS:
- Priority: {responses.get('career_priority', 'N/A')}
- Job Type Preference: {responses.get('job_type', 'N/A')}
- Startup Interest: {responses.get('startup_interest', 'N/A')}
- Work Location: {responses.get('work_location', 'N/A')}

EDUCATION PREFERENCES:
- College Preference: {responses.get('college_preference', 'N/A')}
- Exam Preparation: {responses.get('exam_preparation', 'N/A')}
- Study Duration: {responses.get('study_duration', 'N/A')}

FINANCIAL:
- Financial Capacity: {responses.get('financial_capacity', 'N/A')}
- Scholarship Interest: {responses.get('scholarship_interest', 'N/A')}

PERSONALITY:
- Type: {responses.get('personality', 'N/A')}
- Work Environment: {responses.get('work_environment', 'N/A')}
- Stress Handling: {responses.get('stress_handling', 'N/A')}

ADDITIONAL:
- Family Expectations: {responses.get('family_expectations', 'N/A')}
- Concerns: {responses.get('concerns', 'N/A')}
"""
    
    # Search dataset
    search_terms = f"{responses.get('stream', '')} {responses.get('career_interest_area', '')} {responses.get('subjects_enjoyed', '')}"
    dataset_results = search_dataset(search_terms)
    
    # Generate comprehensive guidance
    prompt = f"""You are a professional career counselor with 20+ years of experience guiding J&K students.

{profile}

RELEVANT DATA FROM J&K CAREER DATABASE:
{dataset_results}

Based on this comprehensive profile, provide a DETAILED, PROFESSIONAL career guidance report with:

1. **EXECUTIVE SUMMARY** (2-3 lines about the student's strengths)

2. **PRIMARY CAREER RECOMMENDATION**
   - Specific career title
   - Why this is perfect for them (match with their profile)
   - Expected salary range (entry-level and 5-year experience)
   - Growth prospects

3. **ALTERNATIVE CAREER OPTIONS** (2-3 backup options)
   - Brief explanation of each
   - Why these are suitable

4. **RECOMMENDED COLLEGES IN J&K**
   - Top 3 specific colleges with reasons
   - Admission process and cutoffs
   - Why these colleges specifically

5. **COLLEGES OUTSIDE J&K** (if applicable)
   - Top 3 options
   - Admission requirements

6. **ENTRANCE EXAMS & PREPARATION STRATEGY**
   - Which exams to target
   - Timeline and preparation tips
   - Expected scores needed

7. **DETAILED ROADMAP** (Month-by-month if possible)
   - Next 6 months
   - 1 year plan
   - 3-5 year vision

8. **FINANCIAL PLANNING**
   - Total estimated cost
   - Scholarship opportunities (specific names)
   - Education loan options
   - Part-time work possibilities

9. **SKILLS TO DEVELOP**
   - Technical skills
   - Soft skills
   - Certifications to pursue

10. **J&K SPECIFIC OPPORTUNITIES**
    - Local government schemes
    - J&K quota benefits
    - Regional industry opportunities

11. **IF STUDENT DOESN'T CHOOSE RECOMMENDED PATH**
    - What are the next best alternatives?
    - How to pivot if needed?

12. **ADDRESSING CONCERNS**
    - Address their specific concerns mentioned
    - Motivational advice

Be specific with college names, exam names, scholarship names, and timelines.
Use encouraging but realistic tone. Format professionally with clear sections.
"""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert career counselor specializing in J&K students. Provide detailed, practical, and encouraging guidance with specific actionable steps."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7
        )
        
        guidance = response.choices[0].message.content
        
        # Display the report in terminal
        print("\n" + "="*80)
        print(f"🌟 PROFESSIONAL CAREER GUIDANCE REPORT FOR {responses.get('name', 'Student').upper()}")
        print("="*80)
        print(guidance)
        print("\n" + "="*80)
        
        # Ask if they want to save
        print("\n💾 Would you like to save this report to a file?")
        save_choice = input("Enter 'yes' to save or press Enter to skip: ").strip().lower()
        
        if save_choice in ['yes', 'y']:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Career_Guidance_{responses.get('name', 'Student').replace(' ', '_')}_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("KASHMIR DISHA - PROFESSIONAL CAREER GUIDANCE REPORT\n")
                f.write("="*80 + "\n")
                f.write(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
                f.write("="*80 + "\n\n")
                f.write(profile)
                f.write("\n" + "="*80 + "\n\n")
                f.write(guidance)
                f.write("\n\n" + "="*80 + "\n")
                f.write("This report is confidential and prepared specifically for the student.\n")
            
            print(f"\n✅ Report saved as: {filename}")
            print("📧 You can share this file with your parents, teachers, or mentors.")
        else:
            print("\n📋 Report not saved. You can screenshot or copy the text above if needed.")
        
    except Exception as e:
        print(f"\n❌ Error generating guidance: {e}")
        print("Please check your internet connection and API key.")

def main():
    """Main function"""
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Error: Dataset '{DATASET_PATH}' not found.")
        print("Please ensure the career database is in the same folder.")
        return
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
        )
        
        # Conduct assessment
        responses = conduct_assessment()
        
        # Generate guidance
        generate_professional_guidance(responses, client)
        
        print("\n" + "="*80)
        print("🙏 Thank you for using Kashmir Disha!")
        print("We wish you all the best in your career journey.")
        print("Remember: Success comes to those who work hard and stay focused!")
        print("="*80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Assessment interrupted. You can restart anytime.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
