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
    
    print("\n🔍 Searching for user data in Firestore...")
    print("="*80)
    
    # Check common collection names
    collection_names = ['students', 'users', 'profiles', 'user_profiles']
    
    found = False
    for collection_name in collection_names:
        try:
            doc_ref = db.collection(collection_name).document(user_id)
            doc = doc_ref.get()
            
            if doc.exists:
                print(f"✅ FOUND in collection: '{collection_name}'")
                print("\n📊 User Data:")
                print("="*80)
                user_data = doc.to_dict()
                for key, value in user_data.items():
                    print(f"   {key}: {value}")
                print("="*80)
                found = True
                break
            else:
                print(f"❌ Not found in '{collection_name}'")
        except Exception as e:
            print(f"❌ Error checking '{collection_name}': {e}")
    
    if not found:
        print("\n" + "="*80)
        print("🔍 Let me list all collections in your database:")
        print("="*80)
        collections = db.collections()
        for collection in collections:
            print(f"   📁 Collection: {collection.id}")
            # List first 5 documents in each collection
            docs = collection.limit(5).stream()
            for doc in docs:
                print(f"      └─ Document ID: {doc.id}")
        
        print("\n" + "="*80)
        print("💡 SOLUTION:")
        print("="*80)
        print(f"The document ID '{user_id}' was not found.")
        print("\nPlease either:")
        print("1. Create a document with this ID in Firestore, OR")
        print("2. Tell me which collection and document ID to use")
        
except Exception as e:
    print(f"❌ Error: {e}")
