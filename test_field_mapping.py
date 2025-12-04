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
    
    user_id = 'ybePalvTrqVb6NF3wjlpfVH2qrI2'
    
    print("\n" + "="*80)
    print("🔍 TESTING FIELD MAPPING")
    print("="*80)
    
    # Fetch raw data
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()
    
    if doc.exists:
        raw_data = doc.to_dict()
        
        print("\n📊 RAW Firebase Data:")
        print("-"*80)
        for key, value in raw_data.items():
            print(f"   {key}: {value}")
        
        # Map to expected format
        user_data = {
            'name': raw_data.get('fullName') or raw_data.get('preferredName', 'Student'),
            'gender': raw_data.get('gender', 'Not specified'),
            'district': raw_data.get('district', 'Unknown'),
            'school_name': raw_data.get('schoolName', 'Not specified'),
            '10th_percentage': raw_data.get('10th_percentage', 'Not available'),
            '12th_stream': raw_data.get('streamOrBranch', 'Not specified'),
            '12th_percentage': raw_data.get('percentageOrCgpa', 'Not available'),
            'fav_subject_10th': raw_data.get('fav_subject_10th', 'Not specified'),
            'fav_subject_12th': raw_data.get('fav_subject_12th', 'Not specified'),
            'interests': raw_data.get('interests', 'Not specified'),
            'email': raw_data.get('email', ''),
            'state': raw_data.get('state', 'Jammu & Kashmir'),
            'education_type': raw_data.get('educationType', ''),
            'education_status': raw_data.get('educationStatus', ''),
        }
        
        print("\n✅ MAPPED Data (What chatbot will see):")
        print("-"*80)
        for key, value in user_data.items():
            print(f"   {key}: {value}")
        
        print("\n" + "="*80)
        print("✅ Field mapping is working!")
        print("="*80)
        
    else:
        print(f"❌ User '{user_id}' not found")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
