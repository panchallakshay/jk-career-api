# Kashmir Disha - Career Guidance System
## Demo Documentation for Project Presentation

### 📋 Project Overview
**Kashmir Disha** is an AI-powered career guidance system specifically designed for students in Jammu & Kashmir. The system provides personalized career counseling by analyzing student profiles, academic performance, interests, and local opportunities.

---

## 🗂️ System Architecture

### Data Sources (Local Datasets)
Our system is built on **5 comprehensive local datasets** curated specifically for J&K students:

1. **DEMO_Career_Database_For_Judges.csv** (20 careers)
   - Career descriptions, required streams, entrance exams
   - J&K-specific college recommendations
   - Salary progressions, skills, and job roles
   - Local opportunities in J&K

2. **JK_Colleges_Complete.csv** (80+ colleges)
   - All government and private colleges in J&K
   - Fees, courses, seats, infrastructure details
   - Contact information and locations

3. **JK_Scholarships_Complete.csv** (16 scholarships)
   - National and state-level scholarships
   - Eligibility criteria, amounts, application process
   - Category-based (SC/ST/OBC/Minority/General)

4. **JK_Entrance_Exams_Complete.csv** (21 exams)
   - JEE, NEET, CUET, CLAT, CAT, UPSC, etc.
   - Exam patterns, fees, preparation strategies
   - J&K coaching centers

5. **JK_Skills_Development_Guide.csv** (34 skills)
   - Technical and soft skills
   - Learning resources, timelines, certifications
   - Free and paid options

---

## 🤖 How It Works

### Step 1: User Profile Collection
- Student ID-based Firebase authentication
- Automatic profile fetching (name, school, percentages, stream, interests)
- No need to re-enter basic information

### Step 2: Interactive Counseling Session
- **10 focused questions** about:
  - Career goals and motivations
  - Work environment preferences
  - Financial capacity
  - Exam preparation status
  - Strengths and concerns

### Step 3: AI-Powered Analysis
- **Dataset Search Algorithm:**
  ```
  1. Search career database based on stream + interests
  2. Match with student's percentages and goals
  3. Filter J&K colleges by budget and location
  4. Identify eligible scholarships
  5. Recommend entrance exams
  ```

### Step 4: Personalized Guidance Report
The system generates a comprehensive report including:
- **Recommended Course** (B.Tech, B.Sc, BBA, etc.)
- **Why it suits the student** (personalized 200+ word analysis)
- **Alternative courses** (2-3 backup options)
- **12-month roadmap** (month-by-month action plan)
- **J&K Colleges** (GDCs prioritized with exact fees)
- **Entrance exams** (which to take, preparation strategy)
- **Scholarships** (eligible scholarships with amounts)
- **Resources** (YouTube, books, websites, apps)
- **Skills to develop** (technical + soft skills)
- **Financial planning** (total cost, scholarships, loans)
- **Backup plans** (if primary doesn't work)

---

## 💡 Key Features

### 1. J&K-Specific Focus
- Prioritizes Government Degree Colleges (GDCs) - affordable education
- Lists local opportunities and government departments
- J&K-specific scholarships (PM Scholarship, J&K Merit, etc.)
- District-wise college recommendations

### 2. Interactive & Conversational
- Natural language conversation (not a form)
- Acknowledges previous answers
- Builds context throughout the session
- Empathetic and encouraging tone

### 3. Comprehensive Guidance
- Not just career names - detailed roadmaps
- Specific resources to start TODAY
- Month-by-month action plans
- Addresses student's specific concerns

### 4. Data-Driven Decisions
- Based on curated datasets (not random suggestions)
- Real college fees, scholarship amounts
- Actual entrance exam details
- Verified J&K opportunities

---

## 📊 Sample Workflow

**Example: Science (PCM) Student**

```
Input Profile:
- Name: Lakshay Kumar
- Stream: Science (PCM)
- 12th %: 82%
- Interests: Technology, Coding, Gaming
- District: Srinagar
- Budget: < ₹25,000/year

↓ AI Analysis ↓

Career Match: B.Sc in Computer Science / BCA
Reasoning: 
- PCM background ✓
- Interest in technology ✓
- Budget-friendly GDCs available ✓
- High job demand ✓

Recommended Colleges:
1. GDC Bemina (BCA) - ₹7,000/year
2. GDC Baramulla (BCA) - ₹7,000/year
3. University of Kashmir - ₹10,000/year

Scholarships:
- J&K Merit Scholarship: ₹20,000/year
- PM Scholarship: ₹30,000/year
- Net Cost: FREE (scholarships cover fees)

Roadmap:
Month 1-3: Learn Python basics, HTML/CSS
Month 4-6: Build 3 projects, start DSA
Month 7-12: Prepare for CUET, apply to colleges
Year 2-3: Internships, certifications, job prep
```

---

## 🎯 Target Users
- **12th-grade students** in J&K
- **Confused about career choices**
- **Need financial guidance** (scholarships, low-cost colleges)
- **Want J&K-specific opportunities**

---

## 🔒 Data Privacy
- Firebase authentication for secure access
- Student data stored in encrypted Firestore
- No data sharing with third parties
- GDPR-compliant data handling

---

## 📈 Future Enhancements
1. **Mobile App** (Android/iOS)
2. **Parent Dashboard** (track student progress)
3. **Alumni Network** (mentorship from J&K professionals)
4. **Job Portal** (J&K-specific job listings)
5. **Scholarship Tracker** (application deadlines, status)

---

## 🏆 Impact
- **Democratizes career guidance** (free for all J&K students)
- **Reduces information gap** (rural vs urban students)
- **Promotes local colleges** (GDCs, SKUAST, etc.)
- **Increases scholarship awareness**
- **Reduces migration** (highlights J&K opportunities)

---

## 📞 Technical Stack
- **Backend**: Python, Firebase (Firestore)
- **AI Model**: Natural Language Processing
- **Data Storage**: CSV datasets + Firebase
- **Frontend**: Terminal-based (can be web/mobile)

---

## 👥 Team & Credits
Developed for J&K students to make career guidance accessible, affordable, and locally relevant.

---

**Note for Judges**: All datasets are locally stored and curated specifically for J&K context. The system does NOT rely on external APIs for career guidance - everything is based on our comprehensive local knowledge base.
