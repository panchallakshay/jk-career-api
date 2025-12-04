# Kashmir Disha API Documentation

## Base URL
```
http://YOUR_SERVER_IP:5000/api
```

---

## 📋 API Endpoints

### 1. Health Check
**GET** `/health`

Check if API server is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Kashmir Disha Career Guidance API",
  "version": "1.0"
}
```

---

### 2. Login / Authenticate Student
**POST** `/auth/login`

Fetch student profile from Firebase and create session.

**Request:**
```json
{
  "student_id": "student_001"
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "student_001_1701547890.123",
  "profile": {
    "name": "Lakshay Kumar",
    "gender": "Male",
    "district": "Srinagar",
    "school_name": "DPS Srinagar",
    "10th_percentage": "85",
    "12th_stream": "Science (PCM)",
    "12th_percentage": "82",
    "fav_subject_10th": "Mathematics",
    "fav_subject_12th": "Physics",
    "interests": "Technology, Coding, Gaming"
  }
}
```

---

### 3. Start Chat Session
**POST** `/chat/start`

Begin career counseling with first question.

**Request:**
```json
{
  "session_id": "student_001_1701547890.123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Lakshay, based on your Science (PCM) background and interest in Technology, Coding, Gaming, what is your primary career goal after 12th?",
  "question_number": 1,
  "total_questions": 10
}
```

---

### 4. Send Message
**POST** `/chat/message`

Send user's answer and get next question.

**Request:**
```json
{
  "session_id": "student_001_1701547890.123",
  "message": "I'm still exploring my options"
}
```

**Response:**
```json
{
  "success": true,
  "message": "That's completely normal! Many students are at this stage. Now, what matters most to you in a career - high salary, job security, passion, or social impact?",
  "question_number": 2,
  "total_questions": 10,
  "ready_for_report": false
}
```

After 10 questions:
```json
{
  "success": true,
  "message": "Thank you for answering all questions! Generating your personalized career guidance report...",
  "question_number": 10,
  "total_questions": 10,
  "ready_for_report": true
}
```

---

### 5. Generate Report
**POST** `/report/generate`

Generate comprehensive career guidance report.

**Request:**
```json
{
  "session_id": "student_001_1701547890.123"
}
```

**Response:**
```json
{
  "success": true,
  "student_name": "Lakshay Kumar",
  "report": "# CAREER GUIDANCE REPORT\n\n## RECOMMENDED COURSE\n**B.Sc in Computer Science**\n\nWhy this is perfect for you:\n- Your Science (PCM) background aligns perfectly...\n- Your 82% in 12th shows strong academic foundation...\n- Interest in Technology, Coding, Gaming indicates...\n\n## ALTERNATIVE COURSES\n1. BCA (Bachelor of Computer Applications)\n2. B.Tech in Information Technology\n3. B.Sc in IT\n\n## 12-MONTH ROADMAP\n**Month 1-3:**\n- Month 1: Learn Python basics (2-3 hours/day)...\n\n[Full detailed report continues...]"
}
```

---

### 6. Follow-up Questions
**POST** `/chat/followup`

Ask clarifying questions about the report.

**Request:**
```json
{
  "session_id": "student_001_1701547890.123",
  "question": "What if I don't get admission in these colleges?"
}
```

**Response:**
```json
{
  "success": true,
  "answer": "Great question! If you don't get admission in the recommended colleges, here are your backup options:\n\n1. **Other GDCs in J&K:**\n   - GDC Sopore (BCA)\n   - GDC Anantnag (BCA)\n   - Fees: ₹7,000-12,000/year\n\n2. **Distance Learning:**\n   - IGNOU BCA program\n   - Online degrees from recognized universities\n\n3. **Private Colleges:**\n   - If budget allows, consider private colleges in J&K\n\nWould you like more details on any of these options?"
}
```

---

### 7. End Session
**POST** `/session/end`

End counseling session and clear data.

**Request:**
```json
{
  "session_id": "student_001_1701547890.123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Session ended successfully"
}
```

---

## 🔒 Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

**Common Error Codes:**
- `400` - Bad Request (missing parameters)
- `401` - Unauthorized (invalid session)
- `404` - Not Found (student not found)
- `500` - Internal Server Error

---

## 📱 Example Mobile App Flow

```
1. User enters Student ID
   ↓
2. Call /api/auth/login
   ↓
3. Display profile, Call /api/chat/start
   ↓
4. Show first question
   ↓
5. User answers → Call /api/chat/message
   ↓
6. Repeat step 5 for 10 questions
   ↓
7. When ready_for_report=true, Call /api/report/generate
   ↓
8. Display report
   ↓
9. User can ask follow-up questions → Call /api/chat/followup
   ↓
10. When done, Call /api/session/end
```

---

## 🚀 How to Run the API Server

### 1. Install Dependencies
```bash
pip install flask flask-cors firebase-admin openai pandas
```

### 2. Configure API Key
Edit `api_server.py` line 20:
```python
API_KEY = "sk-or-v1-YOUR_ACTUAL_OPENROUTER_KEY"
```

### 3. Ensure Firebase Key Exists
Make sure `firebase-key.json` is in the same directory.

### 4. Run Server
```bash
python3 api_server.py
```

Server will start on `http://0.0.0.0:5000`

### 5. Test from Mobile App
Use your server's IP address:
```
http://192.168.1.100:5000/api
```

---

## 📲 Example Code for Mobile Apps

### Flutter (Dart)
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class KashmirDishaAPI {
  final String baseUrl = 'http://YOUR_SERVER_IP:5000/api';
  String? sessionId;
  
  Future<Map<String, dynamic>> login(String studentId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'student_id': studentId}),
    );
    
    final data = jsonDecode(response.body);
    if (data['success']) {
      sessionId = data['session_id'];
    }
    return data;
  }
  
  Future<Map<String, dynamic>> startChat() async {
    final response = await http.post(
      Uri.parse('$baseUrl/chat/start'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'session_id': sessionId}),
    );
    return jsonDecode(response.body);
  }
  
  Future<Map<String, dynamic>> sendMessage(String message) async {
    final response = await http.post(
      Uri.parse('$baseUrl/chat/message'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'session_id': sessionId,
        'message': message
      }),
    );
    return jsonDecode(response.body);
  }
  
  Future<Map<String, dynamic>> generateReport() async {
    final response = await http.post(
      Uri.parse('$baseUrl/report/generate'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'session_id': sessionId}),
    );
    return jsonDecode(response.body);
  }
}
```

### React Native (JavaScript)
```javascript
class KashmirDishaAPI {
  constructor() {
    this.baseUrl = 'http://YOUR_SERVER_IP:5000/api';
    this.sessionId = null;
  }
  
  async login(studentId) {
    const response = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({student_id: studentId})
    });
    
    const data = await response.json();
    if (data.success) {
      this.sessionId = data.session_id;
    }
    return data;
  }
  
  async startChat() {
    const response = await fetch(`${this.baseUrl}/chat/start`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({session_id: this.sessionId})
    });
    return await response.json();
  }
  
  async sendMessage(message) {
    const response = await fetch(`${this.baseUrl}/chat/message`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        session_id: this.sessionId,
        message: message
      })
    });
    return await response.json();
  }
  
  async generateReport() {
    const response = await fetch(`${this.baseUrl}/report/generate`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({session_id: this.sessionId})
    });
    return await response.json();
  }
}
```

### Android (Kotlin)
```kotlin
import okhttp3.*
import org.json.JSONObject

class KashmirDishaAPI {
    private val baseUrl = "http://YOUR_SERVER_IP:5000/api"
    private var sessionId: String? = null
    private val client = OkHttpClient()
    
    fun login(studentId: String, callback: (JSONObject) -> Unit) {
        val json = JSONObject().put("student_id", studentId)
        val body = RequestBody.create(
            MediaType.parse("application/json"), 
            json.toString()
        )
        
        val request = Request.Builder()
            .url("$baseUrl/auth/login")
            .post(body)
            .build()
        
        client.newCall(request).enqueue(object : Callback {
            override fun onResponse(call: Call, response: Response) {
                val data = JSONObject(response.body()?.string())
                if (data.getBoolean("success")) {
                    sessionId = data.getString("session_id")
                }
                callback(data)
            }
            
            override fun onFailure(call: Call, e: IOException) {
                callback(JSONObject().put("success", false))
            }
        })
    }
}
```

---

## 🔧 Production Deployment

For production, consider:

1. **Use HTTPS** (SSL certificate)
2. **Add authentication** (JWT tokens)
3. **Use Redis** for session storage (instead of in-memory)
4. **Add rate limiting**
5. **Deploy on cloud** (AWS, Google Cloud, Heroku)
6. **Use environment variables** for API keys
7. **Add logging** and monitoring

---

## 📞 Support

For issues or questions, contact the development team.
