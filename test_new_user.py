import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
FIREBASE_KEY_PATH = 'firebase-key.json'

try:
    if firebase_admin._apps:
        del firebase_admin._apps['[DEFAULT]']
    
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    # Use the correct user ID
    user_id = 'AW2jznNToeZ83Wzkwwx6228ZEMx1'
    
    print("\n" + "="*80)
    print("🔍 TESTING NEW FIREBASE STRUCTURE")
    print("="*80)
    
    # Fetch raw data
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()
    
    if doc.exists:
        raw_data = doc.to_dict()
        
        print("\n📊 RAW Firebase Data:")
        print("-"*80)
        for key, value in sorted(raw_data.items()):
            print(f"   {key}: {value}")
        
        # Map to expected format
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
        
        print("\n✅ MAPPED Data (What chatbot will see):")
        print("-"*80)
        for key, value in user_data.items():
            print(f"   {key}: {value}")
        
        print("\n" + "="*80)
        print("✅ Field mapping is working!")
        print("="*80)
        print(f"\n✅ Use this Student ID: {user_id}")
        
    else:
        print(f"❌ User '{user_id}' not found")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
