import sys
sys.path.insert(0, '/Users/lakshaly/Desktop/Datasets')

from career_rag_openrouter import get_user_data_from_firebase, initialize_firebase

# Test the function
user_id = 'ybePalvTrqVb6NF3wjlpfVH2qrI2'

print("\n" + "="*80)
print("🧪 TESTING UPDATED FIELD MAPPING")
print("="*80)

user_data = get_user_data_from_firebase(user_id)

if user_data:
    print("\n✅ Successfully fetched and mapped user data!")
    print("\n📊 YOUR PROFILE:")
    print(f"   Full Name: {user_data.get('name', 'N/A')}")
    print(f"   Preferred Name: {user_data.get('preferred_name', 'N/A')}")
    print(f"   Email: {user_data.get('email', 'N/A')}")
    print(f"   Mobile: {user_data.get('mobile', 'N/A')}")
    print(f"   Date of Birth: {user_data.get('dob', 'N/A')}")
    print(f"   Gender: {user_data.get('gender', 'N/A')}")
    print(f"   State: {user_data.get('state', 'N/A')}")
    print(f"   District: {user_data.get('district', 'N/A')}")
    print(f"   School: {user_data.get('school_name', 'N/A')}")
    print(f"   Education: {user_data.get('education_type', 'N/A')} ({user_data.get('education_status', 'N/A')})")
    print(f"   10th %: {user_data.get('10th_percentage', 'N/A')}")
    print(f"   12th Stream: {user_data.get('12th_stream', 'N/A')}")
    print(f"   12th %: {user_data.get('12th_percentage', 'N/A')}")
    print(f"   Fav Subject (10th): {user_data.get('fav_subject_10th', 'N/A')}")
    print(f"   Fav Subject (12th): {user_data.get('fav_subject_12th', 'N/A')}")
    print(f"   Interests: {user_data.get('interests', 'N/A')}")
    print("="*80)
    print("\n✅ All Firebase data is now being fetched and displayed!")
else:
    print("\n❌ Failed to fetch user data")
