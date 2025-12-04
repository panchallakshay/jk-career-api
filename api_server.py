import os
import secrets
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore
from openai import OpenAI
from datetime import datetime
import subprocess

# --- CONFIGURATION ---
DATASET_PATH = 'Career_Knowledge_Master_JK_Augmented.csv'
MODEL_NAME = 'openai/gpt-3.5-turbo'
API_KEY = "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"
FIREBASE_KEY_PATH = 'firebase-key.json'

# Generate a secure API key for your backend
# IMPORTANT: Save this key securely and use it in your backend requests
BACKEND_API_KEY = "navriti_" + secrets.token_urlsafe(32)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Firebase
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

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# --- API KEY AUTHENTICATION ---
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == BACKEND_API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid or missing API key'}), 401
    return decorated_function

# --- HELPER FUNCTIONS ---
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
            
            # Map Firebase fields to expected format
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

# --- API ENDPOINTS ---

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Kashmir Disha Career Counseling API',
        'version': '1.0.0'
    })

@app.route('/api/user/<user_id>', methods=['GET'])
@require_api_key
def get_user_profile(user_id):
    """Get user profile from Firebase"""
    user_data = get_user_data_from_firebase(user_id)
    
    if user_data:
        return jsonify({
            'success': True,
            'user_data': user_data
        })
    else:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404

@app.route('/api/chat', methods=['POST'])
@require_api_key
def chat():
    """Chat endpoint for career counseling"""
    data = request.json
    
    user_id = data.get('user_id')
    message = data.get('message')
    conversation_history = data.get('conversation_history', [])
    
    if not user_id or not message:
        return jsonify({
            'success': False,
            'error': 'user_id and message are required'
        }), 400
    
    # Get user data
    user_data = get_user_data_from_firebase(user_id)
    
    if not user_data:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    
    # Build profile
    profile = f"""
STUDENT PROFILE (From Database):
- Name: {user_data.get('name')}
- Gender: {user_data.get('gender')}
- District (J&K): {user_data.get('district')}
- State: {user_data.get('state')}
- School: {user_data.get('school_name')}
- 10th Percentage: {user_data.get('10th_percentage')}
- 12th Stream: {user_data.get('12th_stream')}
- 12th Percentage: {user_data.get('12th_percentage')}
- Favorite Subject (10th): {user_data.get('fav_subject_10th')}
- Favorite Subject (12th): {user_data.get('fav_subject_12th')}
- General Interests: {user_data.get('interests')}
"""
    
    # Search dataset
    search_terms = f"{user_data.get('12th_stream', '')} {user_data.get('fav_subject_12th', '')} {user_data.get('interests', '')}"
    dataset_results = search_dataset(search_terms)
    
    # System prompt
    system_prompt = f"""You are KashmirDisha, an expert career counselor for J&K students with 20+ years of experience.

{profile}

J&K CAREER DATABASE:
{dataset_results}

Provide helpful, personalized career guidance based on the student's profile and the J&K career database.
Be encouraging, professional, and specific in your recommendations."""
    
    # Build messages
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": message})
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=500
        )
        
        ai_message = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'response': ai_message,
            'user_name': user_data.get('name')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-report', methods=['POST'])
@require_api_key
def generate_report():
    """Generate comprehensive career guidance report"""
    data = request.json
    
    user_id = data.get('user_id')
    responses = data.get('responses', {})
    
    if not user_id:
        return jsonify({
            'success': False,
            'error': 'user_id is required'
        }), 400
    
    # Get user data
    user_data = get_user_data_from_firebase(user_id)
    
    if not user_data:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    
    # Merge user data with responses
    complete_profile = {**user_data, **responses}
    
    # Search for colleges
    college_search = search_dataset("B.Sc IT BCA Computer")
    
    # Build comprehensive prompt
    prompt = f"""Generate a comprehensive career guidance report for this J&K student.

STUDENT PROFILE:
{complete_profile}

J&K COLLEGES DATABASE:
{college_search}

Provide a detailed report with:
1. Recommended course (specific name)
2. Why this course matches their profile
3. Alternative courses
4. Month-by-month roadmap
5. J&K colleges to target
6. Entrance exams and preparation
7. Scholarships available
8. Financial planning
9. Skills to develop
10. Resources to start today

Be specific, actionable, and encouraging."""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert career counselor. Provide detailed, actionable roadmaps."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3500
        )
        
        report = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'report': report,
            'user_name': user_data.get('name')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# --- MAIN ---
if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 KASHMIR DISHA API SERVER")
    print("="*80)
    print(f"\n🔑 Your API Key (save this securely):")
    print(f"   {BACKEND_API_KEY}")
    print("\n📝 Add this to your backend requests as header:")
    print(f"   X-API-Key: {BACKEND_API_KEY}")
    print("\n🌐 API Endpoints:")
    print("   GET  /api/health - Health check")
    print("   GET  /api/user/<user_id> - Get user profile")
    print("   POST /api/chat - Chat with counselor")
    print("   POST /api/generate-report - Generate career report")
    print("\n" + "="*80)
    print("Starting server on http://localhost:5000")
    print("="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
