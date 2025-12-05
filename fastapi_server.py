from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import secrets
import firebase_admin
from firebase_admin import credentials, firestore
from openai import OpenAI

# --- CONFIGURATION ---
DATASET_PATH = 'Career_Knowledge_Master_JK_Augmented.csv'
MODEL_NAME = 'openai/gpt-3.5-turbo'
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', "YOUR_OPENROUTER_API_KEY_HERE")
FIREBASE_KEY_PATH = 'firebase-key.json'

# Generate secure API key for backend
BACKEND_API_KEY = os.getenv('BACKEND_API_KEY', "navriti_" + secrets.token_urlsafe(32))

# Initialize FastAPI
app = FastAPI(
    title="NavRiti AI Career Counseling API",
    description="AI-powered career counseling for J&K students",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase
_db = None

def get_firebase_db():
    """Lazy load Firebase connection"""
    global _db
    if _db is None:
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(FIREBASE_KEY_PATH)
                firebase_admin.initialize_app(cred)
            _db = firestore.client()
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
            return None
    return _db

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# --- REQUEST/RESPONSE MODELS ---

class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_history: Optional[List[Dict]] = []

class ChatResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    user_name: Optional[str] = None
    error: Optional[str] = None

class UserProfileResponse(BaseModel):
    success: bool
    user_data: Optional[Dict] = None
    error: Optional[str] = None

class ReportRequest(BaseModel):
    user_id: str
    responses: Optional[Dict] = {}

class ReportResponse(BaseModel):
    success: bool
    report: Optional[str] = None
    user_name: Optional[str] = None
    error: Optional[str] = None

# --- HELPER FUNCTIONS ---

def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key from header"""
    if x_api_key != BACKEND_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True

def get_user_data_from_firebase(user_id: str):
    """Fetch user data from Firebase"""
    db = get_firebase_db()
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
            }
            return user_data
        else:
            return None
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None

# --- API ENDPOINTS ---

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "NavRiti AI Career Counseling API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "NavRiti AI Career Counseling API",
        "version": "1.0.0"
    }

@app.get("/api/user/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(user_id: str, authorized: bool = Header(None, alias="X-API-Key", convert_underscores=False)):
    """Get user profile from Firebase"""
    verify_api_key(authorized)
    
    user_data = get_user_data_from_firebase(user_id)
    
    if user_data:
        return UserProfileResponse(success=True, user_data=user_data)
    else:
        return UserProfileResponse(success=False, error="User not found")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, x_api_key: str = Header(None)):
    """Chat with career counselor"""
    verify_api_key(x_api_key)
    
    user_data = get_user_data_from_firebase(request.user_id)
    
    if not user_data:
        return ChatResponse(success=False, error="User not found")
    
    # Build profile
    profile = f"""
STUDENT PROFILE:
- Name: {user_data.get('name')}
- Gender: {user_data.get('gender')}
- District: {user_data.get('district')}
- State: {user_data.get('state')}
- 12th Stream: {user_data.get('12th_stream')}
- 12th Marks: {user_data.get('12th_percentage')}
- Interests: {user_data.get('interests')}
- Current Goal: {user_data.get('current_goal')}
"""
    
    system_prompt = f"""You are NavRiti AI, an expert career counselor for J&K students.

{profile}

Provide helpful, personalized career guidance. Be encouraging, professional, and specific."""
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(request.conversation_history)
    messages.append({"role": "user", "content": request.message})
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        ai_message = response.choices[0].message.content
        
        return ChatResponse(
            success=True,
            response=ai_message,
            user_name=user_data.get('name')
        )
        
    except Exception as e:
        return ChatResponse(success=False, error=str(e))

@app.post("/api/generate-report", response_model=ReportResponse)
async def generate_report(request: ReportRequest, x_api_key: str = Header(None)):
    """Generate comprehensive career guidance report"""
    verify_api_key(x_api_key)
    
    user_data = get_user_data_from_firebase(request.user_id)
    
    if not user_data:
        return ReportResponse(success=False, error="User not found")
    
    complete_profile = {**user_data, **request.responses}
    
    prompt = f"""Generate a comprehensive career guidance report for this J&K student.

STUDENT PROFILE:
{complete_profile}

Provide a detailed report with:
1. RECOMMENDED COURSE (specific name)
2. Why this course matches their profile
3. ALTERNATIVE COURSES (2-3 options)
4. 12-MONTH ROADMAP
5. J&K COLLEGES (Government Degree Colleges first)
6. ENTRANCE EXAMS
7. SCHOLARSHIPS
8. SKILLS TO DEVELOP
9. RESOURCES

Use PLAIN TEXT format, NO markdown. Be specific and actionable."""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert career counselor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2500,
            temperature=0.7
        )
        
        report = response.choices[0].message.content
        
        return ReportResponse(
            success=True,
            report=report,
            user_name=user_data.get('name')
        )
        
    except Exception as e:
        return ReportResponse(success=False, error=str(e))

# --- STARTUP EVENT ---

@app.on_event("startup")
async def startup_event():
    """Print API key on startup"""
    print("\n" + "="*80)
    print("🚀 NAVRITI AI API SERVER (FastAPI)")
    print("="*80)
    print(f"\n🔑 Your API Key (save this securely):")
    print(f"   {BACKEND_API_KEY}")
    print("\n📝 Add this to your backend requests as header:")
    print(f"   X-API-Key: {BACKEND_API_KEY}")
    print("\n🌐 API Endpoints:")
    print("   GET  / - Root")
    print("   GET  /health - Health check")
    print("   GET  /api/user/{user_id} - Get user profile")
    print("   POST /api/chat - Chat with counselor")
    print("   POST /api/generate-report - Generate career report")
    print("\n📚 API Documentation:")
    print("   http://localhost:8000/docs - Swagger UI")
    print("   http://localhost:8000/redoc - ReDoc")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
