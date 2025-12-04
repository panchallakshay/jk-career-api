# Firebase Setup Instructions for Kashmir Disha

## Step 1: Create Firebase Project
1. Go to https://console.firebase.google.com/
2. Click "Add Project"
3. Name it "Kashmir-Disha" or similar
4. Enable Google Analytics (optional)
5. Click "Create Project"

## Step 2: Enable Firestore Database
1. In Firebase Console, click "Firestore Database"
2. Click "Create Database"
3. Choose "Start in production mode"
4. Select region (asia-south1 for India)
5. Click "Enable"

## Step 3: Get Service Account Key
1. Click the gear icon ⚙️ next to "Project Overview"
2. Click "Project Settings"
3. Go to "Service Accounts" tab
4. Click "Generate New Private Key"
5. Click "Generate Key" - this downloads a JSON file
6. **Rename it to `firebase-key.json`**
7. **Move it to `/Users/lakshaly/Desktop/Datasets/`**

## Step 4: Set Up Firestore Structure

In Firestore, create a collection called `students` with documents like this:

```
students (collection)
  └── student_001 (document)
      ├── name: "Lakshay Kumar"
      ├── gender: "Male"
      ├── district: "Srinagar"
      ├── school_name: "Delhi Public School Srinagar"
      ├── 10th_percentage: "85"
      ├── 12th_stream: "Science (PCM)"
      ├── 12th_percentage: "82"
      ├── fav_subject_10th: "Mathematics"
      ├── fav_subject_12th: "Physics"
      └── interests: "Technology, Coding, Gaming"
```

## Step 5: Add Student Data

### Option A: Using Firebase Console (Manual)
1. Go to Firestore Database
2. Click "Start Collection"
3. Collection ID: `students`
4. Add documents with student IDs as document names
5. Add fields as shown above

### Option B: Using Python Script (Bulk Upload)
Create a file `add_students.py`:

```python
import firebase_admin
from firebase_admin import credentials, firestore

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
            'interests': 'Technology, Coding'
        }
    },
    # Add more students...
]

for student in students:
    db.collection('students').document(student['id']).set(student['data'])
    print(f"Added: {student['id']}")

print("✅ All students added!")
```

Run: `python3 add_students.py`

## Step 6: Run the Counselor

```bash
python3 kashmir_disha_firebase.py
```

When prompted, enter the Student ID (e.g., `student_001`)

## Security Rules (Important!)

In Firebase Console → Firestore → Rules, set:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /students/{studentId} {
      allow read: if true;  // For testing
      allow write: if false;  // Prevent unauthorized writes
    }
  }
}
```

For production, add proper authentication!

## Troubleshooting

**Error: "firebase-key.json not found"**
- Ensure the file is in `/Users/lakshaly/Desktop/Datasets/`
- Check the filename is exactly `firebase-key.json`

**Error: "No user found"**
- Check the Student ID matches the document ID in Firestore
- Verify the collection name is `students`

**Permission denied**
- Check Firestore security rules
- Ensure service account has proper permissions
