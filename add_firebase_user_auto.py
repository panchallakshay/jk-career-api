import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
FIREBASE_KEY_PATH = 'firebase-key.json'

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    user_id = 'ybePalvTrqVb6NF3wjlpfVH2qrI2'
    
    print("\n" + "="*80)
    print("📝 ADDING USER TO FIREBASE (AUTO MODE)")
    print("="*80)
    
    # Sample user data - REPLACE WITH ACTUAL DATA
    user_data = {
        'name': 'Sample Student',
        'gender': 'Male',
        'district': 'Srinagar',
        'school_name': 'Government Higher Secondary School',
        '10th_percentage': '85',
        '12th_stream': 'Science (PCM)',
        '12th_percentage': '82',
        'fav_subject_10th': 'Mathematics',
        'fav_subject_12th': 'Physics',
        'interests': 'Technology, Coding, Science',
    }
    
    print(f"\nDocument ID: {user_id}")
    print("\n📊 User Data to Add:")
    print("-"*80)
    for key, value in user_data.items():
        print(f"   {key}: {value}")
    
    # Add to Firestore
    print("\n🔄 Adding to Firestore...")
    db.collection('students').document(user_id).set(user_data)
    
    print("\n" + "="*80)
    print("✅ SUCCESS! User added to Firebase")
    print("="*80)
    
    # Verify by reading back
    print("\n🔍 Verifying by reading back from Firebase...")
    doc = db.collection('students').document(user_id).get()
    
    if doc.exists:
        print("✅ Verification successful!")
        print("\n📊 Data in Firebase:")
        retrieved_data = doc.to_dict()
        for key, value in retrieved_data.items():
            print(f"   {key}: {value}")
    else:
        print("❌ Verification failed - document not found")
    
    print("\n" + "="*80)
    print(f"✅ You can now use Student ID: {user_id}")
    print("   in your chatbot applications!")
    print("="*80)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
