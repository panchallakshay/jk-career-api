import os
import secrets
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore
from openai import OpenAI
import subprocess

# --- CONFIGURATION ---
DATASET_PATH = 'Career_Knowledge_Master_JK_Augmented.csv'
MODEL_NAME = 'openai/gpt-3.5-turbo'
API_KEY = os.getenv('OPENROUTER_API_KEY', "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")

# API key for backend authentication
BACKEND_API_KEY = os.getenv('BACKEND_API_KEY', "navriti_" + secrets.token_urlsafe(32))

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Firebase initialization (lazy loading)
_db = None

def get_firebase_db():
    """Lazy load Firebase connection"""
    global _db
    if _db is None:
        try:
            if not firebase_admin._apps:
                # For Vercel, use environment variable for Firebase config
                firebase_config = os.getenv('FIREBASE_CONFIG')
                if firebase_config:
                    import json
                    cred_dict = json.loads(firebase_config)
                    cred = credentials.Certificate(cred_dict)
                else:
                    # Fallback to local file
                    cred = credentials.Certificate('firebase-key.json')
                firebase_admin.initialize_app(cred)
            _db = firestore.client()
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
            return None
    return _db

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
        print(f"Error fetching user data: {e}")
        return None

def search_dataset(query: str) -> str:
    """Search the career dataset - simplified for serverless"""
    # For Vercel, we'll return a placeholder since file access is limited
    # In production, you'd want to use a database or cloud storage
    return "Dataset search is limited in serverless environment. Using general knowledge."

# --- API ENDPOINTS ---

@app.route('/', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Kashmir Disha Career Counseling API',
        'version': '1.0.0',
        'environment': 'production'
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
    
    user_data = get_user_data_from_firebase(user_id)
    
    if not user_data:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    
    profile = f"""
STUDENT PROFILE:
- Name: {user_data.get('name')}
- Gender: {user_data.get('gender')}
- District: {user_data.get('district')}
- State: {user_data.get('state')}
- 12th Stream: {user_data.get('12th_stream')}
- 12th Percentage: {user_data.get('12th_percentage')}
"""
    
    system_prompt = f"""You are KashmirDisha, an expert career counselor for J&K students.

{profile}

Provide helpful, personalized career guidance based on the student's profile.
Be encouraging, professional, and specific in your recommendations."""
    
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
    
    user_data = get_user_data_from_firebase(user_id)
    
    if not user_data:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404
    
    complete_profile = {**user_data, **responses}
    
    prompt = f"""Generate a comprehensive career guidance report for this J&K student.

STUDENT PROFILE:
{complete_profile}

Provide a detailed report with:
1. Recommended course
2. Alternative courses
3. Month-by-month roadmap
4. J&K colleges to target
5. Entrance exams and preparation
6. Scholarships available
7. Skills to develop

Be specific, actionable, and encouraging."""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert career counselor."},
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

# Vercel serverless function handler
app = app
