import pandas as pd
import os

def create_augmented_master_file():
    """Combines all datasets, adds J&K augmentation, and saves the final file."""
    
    FINAL_MASTER_FILE = 'Career_Knowledge_Master_JK_Augmented.csv'
    
    # High-Priority Roles for Govt. Focus (CRITICAL FOR J&K GOAL)
    GOVT_ROLES = ['Doctor', 'Engineer', 'Lawyer', 'Professor', 'Teacher', 
                  'Financial Analyst', 'Architect', 'Data Scientist', 'HR Manager', 
                  'Operations Manager', 'Public Administration', 'Civil Engineer']
    GOVT_ROLES_CLEANED = [r.lower().strip() for r in GOVT_ROLES]

    # The Core Counseling Message (CRITICAL AUGMENTATION)
    AUGMENTATION_TEXT = (
        "\n\n[COUNSELOR NOTE: For students in Jammu & Kashmir pursuing this career, "
        "we strongly recommend seeking admission into a **Government Institution** (like a GDC, NIT, IIM, or AIIMS) "
        "to ensure the highest quality education at the most affordable cost. "
        "Prioritize preparation for national exams (JEE/NEET/CLAT) or state exams (JKAS/UPSC) to secure these seats. "
        "High academic quality and low fees offer the best long-term success. "
        "Focus on Government Colleges (GDC) to save money and prepare for local competitive exams.]"
    )

    # --- 1. Load Data ---
    try:
        df_recommender = pd.read_csv('CareerRecommenderDataset.csv')
        df_qa = pd.read_csv('Career QA Dataset.csv')
    except FileNotFoundError:
        print("❌ ERROR: Please ensure all three original files are present in the folder.")
        return None

    # --- 2. Process QA Data (Augmentation and Stacking) ---
    df_qa['role_cleaned'] = df_qa['role'].str.lower().str.strip()
    df_qa['answer_augmented'] = df_qa.apply(
        lambda row: row['answer'] + AUGMENTATION_TEXT 
        if row['role_cleaned'] in GOVT_ROLES_CLEANED else row['answer'], 
        axis=1
    )
    df_qa_stack = pd.DataFrame()
    df_qa_stack['Career_Name'] = df_qa['role'].str.strip()
    df_qa_stack['text_content'] = df_qa.apply(lambda row: f"Q&A: {row['question']} || ANSWER: {row['answer_augmented']}", axis=1)
    df_qa_stack['Career_Options'] = df_qa['role']
    df_qa_stack['Source_Type'] = 'QA_Knowledge'

    # --- 3. Process Recommender Data (Profile Summaries) ---
    df_recommender_stack = pd.DataFrame()
    df_recommender_stack['Career_Name'] = df_recommender['Career_Options'].str.split(',').str[0].str.strip()
    df_recommender_stack['Career_Options'] = df_recommender['Career_Options']
    df_recommender_stack['Source_Type'] = 'Student_Profile'
    
    def create_profile_summary(row):
        interests = [col for col in df_recommender.columns[:-2] if row[col] == 'Yes']
        return f"PROFILE SUMMARY: Interests: {', '.join(interests)}. Course Taken: {row['Courses']}. Recommended Career: {row['Career_Options'].split(',')[0].strip()}"

    df_recommender_stack['text_content'] = df_recommender.apply(create_profile_summary, axis=1)

    # --- 4. Process Job Match Data ---
    try:
        df_job = pd.read_csv('Job Datsset.csv')
        df_job_stack = pd.DataFrame()
        # Since there is no specific role name, we use a generic identifier or the Job ID
        df_job_stack['Career_Name'] = 'Job_Match_Entry' 
        df_job_stack['Career_Options'] = df_job['Job_Requirements'] # Using requirements as options context
        df_job_stack['Source_Type'] = 'Job_Match_Data'
        
        def create_job_summary(row):
            return (f"JOB MATCH DATA: User Skills: {row['User_Skills']} || "
                    f"Job Requirements: {row['Job_Requirements']} || "
                    f"Match Score: {row['Match_Score']} || "
                    f"Recommended: {row['Recommended']}")

        df_job_stack['text_content'] = df_job.apply(create_job_summary, axis=1)
    except FileNotFoundError:
        print("⚠️ WARNING: 'Job Datsset.csv' not found. Skipping this dataset.")
        df_job_stack = pd.DataFrame()
    
    # --- 5. Process Enrichment Data (Roadmaps & Salaries) ---
    try:
        # Try to run the generator if the file doesn't exist or just to be fresh
        import enrichment_generator
        enrichment_generator.generate_enrichment_data()
        
        df_enrich = pd.read_csv('Career_Enrichment_Data.csv')
        # Ensure columns match
        df_enrich = df_enrich[['Career_Name', 'text_content', 'Source_Type', 'Career_Options', 'JK_GOVT_PRIORITY']]
        print(f"✅ Loaded Enrichment Data: {len(df_enrich)} records")
    except Exception as e:
        print(f"⚠️ WARNING: Could not process enrichment data: {e}")
        df_enrich = pd.DataFrame()

    # --- 6. Final Combination and Flagging ---
    df_final_master = pd.concat([df_recommender_stack, df_qa_stack, df_job_stack, df_enrich], ignore_index=True)

    # Add the final J&K Priority Flag (Re-apply to ensure new rows get it if applicable)
    df_final_master['JK_GOVT_PRIORITY'] = df_final_master['Career_Name'].apply(
        lambda x: 'TRUE' if str(x).lower().strip() in GOVT_ROLES_CLEANED else 'FALSE'
    )
    
    df_final_master = df_final_master[['Career_Name', 'text_content', 'Source_Type', 'Career_Options', 'JK_GOVT_PRIORITY']]

    # --- 7. Final Save ---
    df_final_master.to_csv(FINAL_MASTER_FILE, index=False)
    print(f"\n✅ SUCCESS: Final Master File Created: {FINAL_MASTER_FILE}")
    return FINAL_MASTER_FILE

if __name__ == "__main__":
    create_augmented_master_file()
