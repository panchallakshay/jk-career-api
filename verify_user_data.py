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
    print("🔍 FETCHING USER DATA FROM FIREBASE")
    print("="*80)
    
    # Fetch from 'users' collection
    doc_ref = db.collection('users').document(user_id)
    doc = doc_ref.get()
    
    if doc.exists:
        print(f"✅ SUCCESS! User '{user_id}' found in 'users' collection!")
        print("\n📊 User Data:")
        print("="*80)
        user_data = doc.to_dict()
        for key, value in user_data.items():
            print(f"   {key}: {value}")
        print("="*80)
        
        print("\n✅ Your chatbot is now connected to navriti-f7087!")
        print(f"✅ You can use Student ID: {user_id}")
        
    else:
        print(f"❌ User '{user_id}' not found")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
