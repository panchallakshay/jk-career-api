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
    print("📝 ADDING NEW USER TO FIREBASE")
    print("="*80)
    
    # Prompt for user data
    print(f"\nDocument ID: {user_id}")
    print("\nPlease enter the student's information:")
    print("-"*80)
    
    user_data = {
        'name': input("Name: ").strip(),
        'gender': input("Gender (Male/Female/Other): ").strip(),
        'district': input("District (J&K): ").strip(),
        'school_name': input("School Name: ").strip(),
        '10th_percentage': input("10th Percentage: ").strip(),
        '12th_stream': input("12th Stream (e.g., Science PCM, Commerce, Arts): ").strip(),
        '12th_percentage': input("12th Percentage: ").strip(),
        'fav_subject_10th': input("Favorite Subject in 10th: ").strip(),
        'fav_subject_12th': input("Favorite Subject in 12th: ").strip(),
        'interests': input("Interests (comma-separated): ").strip(),
    }
    
    # Add to Firestore
    print("\n🔄 Adding to Firestore...")
    db.collection('students').document(user_id).set(user_data)
    
    print("\n" + "="*80)
    print("✅ SUCCESS! User added to Firebase")
    print("="*80)
    print("\n📊 Added Data:")
    for key, value in user_data.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*80)
    print(f"✅ You can now use Student ID: {user_id}")
    print("   in career_rag_openrouter.py or kashmir_disha_firebase.py")
    print("="*80)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
