import pandas as pd

def generate_enrichment_data():
    # Massive dictionary of career data
    # Fields: Salary, Roadmap, Exams, JK_Colleges
    career_data = [
        # --- TECH & DATA ---
        {
            "Career_Name": "Data Scientist",
            "Salary": "Entry: ₹6-12 LPA | Senior: ₹25-50+ LPA",
            "Roadmap": "Step 1: B.Tech (CS/Math) or B.Stat. Step 2: Master Python, SQL, ML algorithms. Step 3: Build projects (Kaggle). Step 4: Intern as Data Analyst. Step 5: Transition to Data Scientist.",
            "Exams": "GATE (for M.Tech), ISI Admission Test, CMI Entrance.",
            "JK_Colleges": "NIT Srinagar (M.Tech), IUST Awantipora (CS Dept), Central University of Jammu."
        },
        {
            "Career_Name": "Software Engineer",
            "Salary": "Entry: ₹5-15 LPA | Senior: ₹30-80+ LPA",
            "Roadmap": "Step 1: B.Tech in CSE/IT. Step 2: DSA (LeetCode) & Dev (Web/App). Step 3: Internships. Step 4: Campus Placements/Off-campus drives.",
            "Exams": "JEE Mains/Advanced, BITSAT, VITEEE.",
            "JK_Colleges": "NIT Srinagar, GCET Jammu, GCET Safapora, IUST, SSM College of Engineering."
        },
        {
            "Career_Name": "AI Researcher",
            "Salary": "Entry: ₹10-20 LPA | Senior: ₹50L-1Cr+ LPA",
            "Roadmap": "Step 1: B.Tech CS. Step 2: MS/PhD in AI/ML. Step 3: Publish papers (NeurIPS, ICML). Step 4: Join Research Labs (Google DeepMind, OpenAI).",
            "Exams": "GATE, GRE (for abroad).",
            "JK_Colleges": "NIT Srinagar (Research Dept), IIT Jammu (Research Programs)."
        },
        {
            "Career_Name": "Web Developer",
            "Salary": "Entry: ₹3-8 LPA | Senior: ₹20-40 LPA",
            "Roadmap": "Step 1: Learn HTML/CSS/JS. Step 2: Learn React/Node.js. Step 3: Build Portfolio. Step 4: Freelance or Junior Dev role.",
            "Exams": "None specific. Portfolio matters.",
            "JK_Colleges": "Any CS degree from GDC/University of Kashmir/Jammu + Online Bootcamps."
        },
        {
            "Career_Name": "Mobile App Developer",
            "Salary": "Entry: ₹4-9 LPA | Senior: ₹25-45 LPA",
            "Roadmap": "Step 1: Learn Java/Kotlin (Android) or Swift (iOS). Step 2: Build Apps. Step 3: Publish to Play Store/App Store.",
            "Exams": "None specific.",
            "JK_Colleges": "NIELIT Srinagar/Jammu (Certifications), CS Depts of KU/JU."
        },
        {
            "Career_Name": "Cyber Security Analyst",
            "Salary": "Entry: ₹5-10 LPA | Senior: ₹25-50 LPA",
            "Roadmap": "Step 1: B.Tech CS. Step 2: Learn Networking, Linux, Python. Step 3: Certifications (CEH, CISSP). Step 4: Security Analyst role.",
            "Exams": "CEH, OSCP, CISSP.",
            "JK_Colleges": "NIELIT J&K (Cyber Security Courses), Central University Jammu."
        },

        # --- MEDICAL & SCIENCE ---
        {
            "Career_Name": "Doctor",
            "Salary": "Entry: ₹8-12 LPA | Specialist: ₹30-1Cr+ LPA",
            "Roadmap": "Step 1: PCB in 12th. Step 2: Crack NEET UG. Step 3: MBBS (5.5 yrs). Step 4: NEET PG for Specialization (MD/MS).",
            "Exams": "NEET UG, NEET PG, INI-CET.",
            "JK_Colleges": "GMC Srinagar, GMC Jammu, SKIMS Soura, ASCOMS, AIIMS Vijaypur (Jammu)."
        },
        {
            "Career_Name": "Clinical Nurse",
            "Salary": "Entry: ₹3-6 LPA | Senior: ₹10-15 LPA",
            "Roadmap": "Step 1: 12th PCB. Step 2: B.Sc Nursing. Step 3: Nursing Council Registration. Step 4: Hospital Job.",
            "Exams": "JKBOPEE B.Sc Nursing Entrance.",
            "JK_Colleges": "Govt Nursing College Srinagar/Jammu, SKIMS Nursing College, Baba Mehar Singh College."
        },
        {
            "Career_Name": "Dental Surgeon",
            "Salary": "Entry: ₹4-8 LPA | Senior: ₹15-30 LPA",
            "Roadmap": "Step 1: NEET UG. Step 2: BDS (5 yrs). Step 3: MDS (Optional). Step 4: Private Practice or Govt Job.",
            "Exams": "NEET UG, NEET MDS.",
            "JK_Colleges": "Govt Dental College (GDC) Srinagar, GDC Jammu."
        },
        {
            "Career_Name": "Biotech Researcher",
            "Salary": "Entry: ₹4-7 LPA | Senior: ₹15-25 LPA",
            "Roadmap": "Step 1: B.Sc/B.Tech Biotechnology. Step 2: M.Sc/M.Tech. Step 3: PhD (for Research).",
            "Exams": "GAT-B, JAM, CSIR NET.",
            "JK_Colleges": "University of Kashmir (Biotech Dept), SMVDU Katra, SKUAST."
        },

        # --- BUSINESS & FINANCE ---
        {
            "Career_Name": "Chartered Accountant",
            "Salary": "Entry: ₹7-10 LPA | Senior: ₹20-50+ LPA",
            "Roadmap": "Step 1: Register for CA Foundation after 12th. Step 2: Clear Intermediate. Step 3: Articleship (3 yrs). Step 4: Clear CA Final.",
            "Exams": "ICAI CA Foundation, Intermediate, Final.",
            "JK_Colleges": "ICAI Chapters in Srinagar and Jammu (Self-study + Coaching)."
        },
        {
            "Career_Name": "Investment Banker",
            "Salary": "Entry: ₹12-25 LPA | Senior: ₹50L-2Cr+ LPA",
            "Roadmap": "Step 1: B.Com/Eco/Engg. Step 2: CFA (Level 1/2) or MBA Finance. Step 3: Intern at Banks. Step 4: Analyst Role.",
            "Exams": "CFA, CAT (for MBA).",
            "JK_Colleges": "The Business School (KU), TBS (JU), IIM Jammu."
        },
        {
            "Career_Name": "Business Analyst",
            "Salary": "Entry: ₹6-10 LPA | Senior: ₹20-35 LPA",
            "Roadmap": "Step 1: Graduation. Step 2: Learn SQL, Excel, Tableau. Step 3: MBA (Optional). Step 4: Analyst Role.",
            "Exams": "CAT, MAT, CMAT.",
            "JK_Colleges": "IIM Jammu, University of Kashmir (MBA), SMVDU."
        },
        {
            "Career_Name": "Product Manager",
            "Salary": "Entry: ₹10-18 LPA | Senior: ₹40-80+ LPA",
            "Roadmap": "Step 1: B.Tech/BBA. Step 2: MBA (Preferred). Step 3: Learn Agile, UX, Analytics. Step 4: APM Role.",
            "Exams": "CAT, GMAT.",
            "JK_Colleges": "IIM Jammu (MBA Program)."
        },
        {
            "Career_Name": "Financial Analyst",
            "Salary": "Entry: ₹5-9 LPA | Senior: ₹18-30 LPA",
            "Roadmap": "Step 1: B.Com/BBA. Step 2: M.Com or MBA Finance. Step 3: Certifications (CFP/CFA).",
            "Exams": "CFA, NISM Certifications.",
            "JK_Colleges": "Islamia College Srinagar (Commerce), SPMR College of Commerce Jammu."
        },

        # --- CIVIL SERVICES & GOVT ---
        {
            "Career_Name": "Civil Services (IAS/IPS)",
            "Salary": "Entry: ₹56,100/mo (Basic) + Perks | Senior: Cabinet Secretary Level",
            "Roadmap": "Step 1: Graduation (Any Stream). Step 2: Prepare for UPSC CSE (1-2 yrs). Step 3: Clear Prelims, Mains, Interview.",
            "Exams": "UPSC Civil Services Exam (CSE), JKAS (State PSC).",
            "JK_Colleges": "Any GDC (Govt Degree College) for Graduation. IMPA (J&K) for Training."
        },
        {
            "Career_Name": "Teacher",
            "Salary": "Entry: ₹3-6 LPA (Pvt) / ₹40k-60k/mo (Govt) | Senior: ₹10-12 LPA",
            "Roadmap": "Step 1: Graduation. Step 2: B.Ed. Step 3: CTET/State TET. Step 4: Apply for Govt/Pvt Schools.",
            "Exams": "CTET, JK-SET (for Lecturers), NET.",
            "JK_Colleges": "Govt College of Education (Srinagar/Jammu), Central University B.Ed."
        },
        {
            "Career_Name": "Professor",
            "Salary": "Entry: ₹57,700/mo (Asst. Prof) | Senior: ₹1.5-2.5L/mo",
            "Roadmap": "Step 1: Masters Degree. Step 2: Clear UGC NET / CSIR NET. Step 3: PhD (Mandatory for Univ). Step 4: Assistant Professor.",
            "Exams": "UGC NET, CSIR NET, JK-SET.",
            "JK_Colleges": "University of Kashmir, University of Jammu, CUK, CUJ."
        },

        # --- ARTS, MEDIA & DESIGN ---
        {
            "Career_Name": "Journalist",
            "Salary": "Entry: ₹3-5 LPA | Senior: ₹10-20 LPA",
            "Roadmap": "Step 1: BA in Journalism/Mass Comm. Step 2: Internships at Media Houses. Step 3: Reporter/Editor Role.",
            "Exams": "Entrance Exams for IIMC, Jamia Millia.",
            "JK_Colleges": "Media Education Research Centre (MERC) KU, Govt College for Women Parade (Jammu)."
        },
        {
            "Career_Name": "Graphic Designer",
            "Salary": "Entry: ₹3-6 LPA | Senior: ₹12-20 LPA",
            "Roadmap": "Step 1: B.Des or Certification. Step 2: Master Photoshop, Illustrator. Step 3: Portfolio. Step 4: Agency/Freelance.",
            "Exams": "NID DAT, UCEED.",
            "JK_Colleges": "Institute of Music & Fine Arts (KU/JU), Shri Mata Vaishno Devi University (Architecture/Design)."
        },
        {
            "Career_Name": "Fashion Designer",
            "Salary": "Entry: ₹4-8 LPA | Senior: ₹15-30 LPA",
            "Roadmap": "Step 1: B.Des in Fashion. Step 2: Intern with Designers. Step 3: Launch Label or Join Brand.",
            "Exams": "NIFT Entrance, NID.",
            "JK_Colleges": "NIFT Srinagar (Ompora Budgam)."
        },
        {
            "Career_Name": "Lawyer",
            "Salary": "Entry: ₹3-8 LPA | Senior: ₹25-50+ LPA",
            "Roadmap": "Step 1: 12th (Any stream). Step 2: CLAT for 5-yr LLB OR Graduation + 3-yr LLB. Step 3: Bar Council Exam.",
            "Exams": "CLAT, AILET.",
            "JK_Colleges": "School of Law (University of Kashmir), Law School (University of Jammu), Dogra Law College."
        },

        # --- ENGINEERING & ARCHITECTURE ---
        {
            "Career_Name": "Civil Engineer",
            "Salary": "Entry: ₹4-8 LPA | Senior: ₹15-25 LPA",
            "Roadmap": "Step 1: B.Tech Civil. Step 2: GATE (for PSU/M.Tech) or Site Experience. Step 3: Project Manager.",
            "Exams": "JEE, JKCET.",
            "JK_Colleges": "NIT Srinagar, GCET Jammu, SSM College."
        },
        {
            "Career_Name": "Architect",
            "Salary": "Entry: ₹4-7 LPA | Senior: ₹15-30 LPA",
            "Roadmap": "Step 1: B.Arch (5 yrs). Step 2: Internship. Step 3: COA Registration. Step 4: Architect.",
            "Exams": "NATA, JEE Paper 2.",
            "JK_Colleges": "SMVDU Katra (School of Architecture), GCET Jammu (Architecture Dept)."
        },
        {
            "Career_Name": "Mechanical Engineer",
            "Salary": "Entry: ₹4-8 LPA | Senior: ₹15-25 LPA",
            "Roadmap": "Step 1: B.Tech Mechanical. Step 2: GATE (for PSU). Step 3: Core Industry Job.",
            "Exams": "JEE, JKCET.",
            "JK_Colleges": "NIT Srinagar, GCET Jammu, IUST."
        },

        # --- OTHERS ---
        {
            "Career_Name": "Hotel Manager",
            "Salary": "Entry: ₹3-6 LPA | Senior: ₹12-25 LPA",
            "Roadmap": "Step 1: BHM (Bachelor of Hotel Mgmt). Step 2: Internships (Industrial Training). Step 3: MT Program in Hotels.",
            "Exams": "NCHMCT JEE.",
            "JK_Colleges": "Institute of Hotel Management (IHM) Srinagar."
        },
        {
            "Career_Name": "Agriculture Scientist",
            "Salary": "Entry: ₹5-9 LPA | Senior: ₹15-25 LPA",
            "Roadmap": "Step 1: B.Sc Agriculture. Step 2: M.Sc/PhD. Step 3: ARS Exam or Pvt Sector.",
            "Exams": "ICAR AIEEA.",
            "JK_Colleges": "SKUAST Kashmir (Shalimar), SKUAST Jammu (Chatha)."
        },
        {
            "Career_Name": "Veterinary Doctor",
            "Salary": "Entry: ₹6-10 LPA | Senior: ₹15-25 LPA",
            "Roadmap": "Step 1: 12th PCB. Step 2: NEET/State Vet Exam. Step 3: BVSc & AH (5.5 yrs).",
            "Exams": "NEET, JKBOPEE CET.",
            "JK_Colleges": "SKUAST Kashmir (Faculty of Vet Sciences), SKUAST Jammu."
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(career_data)
    
    # Format for Master File with JK Context
    df['text_content'] = df.apply(
        lambda row: (f"CAREER GUIDE: {row['Career_Name']} || "
                     f"💰 SALARY: {row['Salary']} || "
                     f"🗺️ ROADMAP: {row['Roadmap']} || "
                     f"🎓 EXAMS: {row['Exams']} || "
                     f"🏔️ J&K COLLEGES: {row['JK_Colleges']}"),
        axis=1
    )
    df['Source_Type'] = 'Career_Roadmap_Guide'
    df['Career_Options'] = df['Career_Name']
    df['JK_GOVT_PRIORITY'] = 'FALSE' # Default
    
    # Select columns to match master schema
    df_final = df[['Career_Name', 'text_content', 'Source_Type', 'Career_Options', 'JK_GOVT_PRIORITY']]
    
    output_file = 'Career_Enrichment_Data.csv'
    df_final.to_csv(output_file, index=False)
    print(f"✅ Generated Massive Enrichment Data: {output_file} ({len(df)} records)")

if __name__ == "__main__":
    generate_enrichment_data()
