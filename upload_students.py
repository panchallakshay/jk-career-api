import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('firebase-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Sample student data
students = [
    {
        'id': 'student_001',
        'data': {
            'name': 'Lakshay Kumar',
            'gender': 'Male',
            'district': 'Srinagar',
            'school_name': 'DPS Srinagar',
            '10th_percentage': '85',
            '12th_stream': 'Science (PCM)',
            '12th_percentage': '82',
            'fav_subject_10th': 'Mathematics',
            'fav_subject_12th': 'Physics',
            'interests': 'Technology, Coding, Gaming'
        }
    },
    # Add more students here if needed
]

# Upload to Firestore
print("📤 Uploading student data to Firebase...")

for student in students:
    db.collection('students').document(student['id']).set(student['data'])
    print(f"✅ Added: {student['id']} - {student['data']['name']}")

print("\n🎉 All students added successfully!")
print("\nYou can now run: python3 career_rag_openrouter.py")
print("And enter Student ID: student_001")
