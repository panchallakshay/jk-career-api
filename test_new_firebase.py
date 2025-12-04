import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase with new key
FIREBASE_KEY_PATH = 'firebase-key.json'

try:
    # Clear any existing Firebase apps
    if firebase_admin._apps:
        del firebase_admin._apps['[DEFAULT]']
    
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    print("\n" + "="*80)
    print("🔥 FIREBASE CONNECTION TEST - navriti-f7087")
    print("="*80)
    
    # Test 1: Check connection
    print("\n✅ Firebase initialized successfully!")
    print(f"📊 Project ID: navriti-f7087")
    
    # Test 2: List collections
    print("\n🔍 Checking for collections in Firestore...")
    collections = list(db.collections())
    
    if collections:
        print(f"✅ Found {len(collections)} collection(s):")
        for collection in collections:
            print(f"   📁 {collection.id}")
            
            # List documents in each collection
            docs = list(collection.limit(10).stream())
            if docs:
                print(f"      └─ {len(docs)} document(s):")
                for doc in docs:
                    print(f"         • {doc.id}")
            else:
                print(f"      └─ (empty collection)")
    else:
        print("⚠️  No collections found yet. Database is empty.")
        print("\n💡 You need to add data to Firestore first!")
    
    # Test 3: Try to fetch the specific user document
    print("\n" + "="*80)
    print("🔍 Testing specific user document...")
    print("="*80)
    
    user_id = 'ybePalvTrqVb6NF3wjlpfVH2qrI2'
    doc_ref = db.collection('students').document(user_id)
    doc = doc_ref.get()
    
    if doc.exists:
        print(f"✅ User document '{user_id}' found!")
        print("\n📊 User Data:")
        user_data = doc.to_dict()
        for key, value in user_data.items():
            print(f"   {key}: {value}")
    else:
        print(f"❌ User document '{user_id}' NOT found in 'students' collection")
        print("\n💡 Next step: Add this user to Firestore")
    
    print("\n" + "="*80)
    print("✅ Connection test complete!")
    print("="*80)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
