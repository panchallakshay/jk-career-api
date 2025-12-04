# Kashmir Disha - Mobile App Integration Guide

## 🎯 Complete Step-by-Step Implementation

---

## Step 1: Choose Your Platform

### Option A: Flutter (Recommended - Works on Android & iOS)
### Option B: React Native (JavaScript - Android & iOS)
### Option C: Native Android (Kotlin/Java)

Let's use **Flutter** as an example (most popular for cross-platform):

---

## Step 2: Create Flutter Project

```bash
# Install Flutter (if not already installed)
# Download from: https://flutter.dev/docs/get-started/install

# Create new project
flutter create kashmir_disha_app
cd kashmir_disha_app
```

---

## Step 3: Add Dependencies

Edit `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0          # For API calls
  provider: ^6.0.5      # State management
  shared_preferences: ^2.2.2  # Store session
```

Run:
```bash
flutter pub get
```

---

## Step 4: Create API Service Class

Create file: `lib/services/api_service.dart`

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class KashmirDishaAPI {
  // CHANGE THIS to your server IP
  static const String baseUrl = 'http://10.9.5.124:8080/api';
  
  String? _sessionId;
  
  // 1. Login and get student profile
  Future<Map<String, dynamic>> login(String studentId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'student_id': studentId}),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['success']) {
          _sessionId = data['session_id'];
          
          // Save session locally
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('session_id', _sessionId!);
          
          return data;
        }
      }
      
      return {'success': false, 'error': 'Login failed'};
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }
  
  // 2. Start chat session
  Future<Map<String, dynamic>> startChat() async {
    if (_sessionId == null) {
      return {'success': false, 'error': 'No active session'};
    }
    
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/chat/start'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'session_id': _sessionId}),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      
      return {'success': false, 'error': 'Failed to start chat'};
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }
  
  // 3. Send message
  Future<Map<String, dynamic>> sendMessage(String message) async {
    if (_sessionId == null) {
      return {'success': false, 'error': 'No active session'};
    }
    
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/chat/message'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'session_id': _sessionId,
          'message': message,
        }),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      
      return {'success': false, 'error': 'Failed to send message'};
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }
  
  // 4. Generate report
  Future<Map<String, dynamic>> generateReport() async {
    if (_sessionId == null) {
      return {'success': false, 'error': 'No active session'};
    }
    
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/report/generate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'session_id': _sessionId}),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      
      return {'success': false, 'error': 'Failed to generate report'};
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }
  
  // 5. Ask follow-up question
  Future<Map<String, dynamic>> askFollowUp(String question) async {
    if (_sessionId == null) {
      return {'success': false, 'error': 'No active session'};
    }
    
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/chat/followup'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'session_id': _sessionId,
          'question': question,
        }),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      
      return {'success': false, 'error': 'Failed to ask question'};
    } catch (e) {
      return {'success': false, 'error': e.toString()};
    }
  }
  
  // 6. End session
  Future<void> endSession() async {
    if (_sessionId != null) {
      try {
        await http.post(
          Uri.parse('$baseUrl/session/end'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'session_id': _sessionId}),
        );
      } catch (e) {
        print('Error ending session: $e');
      }
      
      _sessionId = null;
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('session_id');
    }
  }
}
```

---

## Step 5: Create UI Screens

### Login Screen (`lib/screens/login_screen.dart`)

```dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'chat_screen.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _studentIdController = TextEditingController();
  final _api = KashmirDishaAPI();
  bool _isLoading = false;
  
  void _login() async {
    if (_studentIdController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please enter Student ID')),
      );
      return;
    }
    
    setState(() => _isLoading = true);
    
    final result = await _api.login(_studentIdController.text);
    
    setState(() => _isLoading = false);
    
    if (result['success']) {
      // Navigate to chat screen
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ChatScreen(
            api: _api,
            profile: result['profile'],
          ),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(result['error'] ?? 'Login failed')),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Kashmir Disha'),
        backgroundColor: Colors.teal,
      ),
      body: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.school, size: 100, color: Colors.teal),
            SizedBox(height: 20),
            Text(
              'Career Guidance System',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 40),
            TextField(
              controller: _studentIdController,
              decoration: InputDecoration(
                labelText: 'Student ID',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.person),
              ),
            ),
            SizedBox(height: 20),
            _isLoading
                ? CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _login,
                    child: Text('Login'),
                    style: ElevatedButton.styleFrom(
                      minimumSize: Size(double.infinity, 50),
                    ),
                  ),
          ],
        ),
      ),
    );
  }
}
```

### Chat Screen (`lib/screens/chat_screen.dart`)

```dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'report_screen.dart';

class ChatScreen extends StatefulWidget {
  final KashmirDishaAPI api;
  final Map<String, dynamic> profile;
  
  ChatScreen({required this.api, required this.profile});
  
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _messageController = TextEditingController();
  final List<Map<String, String>> _messages = [];
  bool _isLoading = false;
  int _questionNumber = 0;
  bool _readyForReport = false;
  
  @override
  void initState() {
    super.initState();
    _startChat();
  }
  
  void _startChat() async {
    setState(() => _isLoading = true);
    
    final result = await widget.api.startChat();
    
    setState(() => _isLoading = false);
    
    if (result['success']) {
      setState(() {
        _messages.add({
          'sender': 'AI',
          'message': result['message'],
        });
        _questionNumber = result['question_number'];
      });
    }
  }
  
  void _sendMessage() async {
    if (_messageController.text.isEmpty) return;
    
    final userMessage = _messageController.text;
    _messageController.clear();
    
    setState(() {
      _messages.add({'sender': 'User', 'message': userMessage});
      _isLoading = true;
    });
    
    final result = await widget.api.sendMessage(userMessage);
    
    setState(() => _isLoading = false);
    
    if (result['success']) {
      setState(() {
        _messages.add({
          'sender': 'AI',
          'message': result['message'],
        });
        _questionNumber = result['question_number'];
        _readyForReport = result['ready_for_report'] ?? false;
      });
      
      // If ready for report, show button
      if (_readyForReport) {
        _showGenerateReportDialog();
      }
    }
  }
  
  void _showGenerateReportDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Generate Report'),
        content: Text('All questions answered! Generate your career guidance report?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Not Yet'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              _generateReport();
            },
            child: Text('Generate'),
          ),
        ],
      ),
    );
  }
  
  void _generateReport() async {
    setState(() => _isLoading = true);
    
    final result = await widget.api.generateReport();
    
    setState(() => _isLoading = false);
    
    if (result['success']) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ReportScreen(
            api: widget.api,
            report: result['report'],
            studentName: result['student_name'],
          ),
        ),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Chat - Question $_questionNumber/10'),
        backgroundColor: Colors.teal,
      ),
      body: Column(
        children: [
          // Profile card
          Container(
            padding: EdgeInsets.all(10),
            color: Colors.teal[50],
            child: Row(
              children: [
                CircleAvatar(
                  child: Text(widget.profile['name'][0]),
                ),
                SizedBox(width: 10),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      widget.profile['name'],
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Text(
                      '${widget.profile['12th_stream']} - ${widget.profile['12th_percentage']}%',
                      style: TextStyle(fontSize: 12),
                    ),
                  ],
                ),
              ],
            ),
          ),
          
          // Messages
          Expanded(
            child: ListView.builder(
              padding: EdgeInsets.all(10),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                final isAI = msg['sender'] == 'AI';
                
                return Align(
                  alignment: isAI ? Alignment.centerLeft : Alignment.centerRight,
                  child: Container(
                    margin: EdgeInsets.symmetric(vertical: 5),
                    padding: EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isAI ? Colors.grey[200] : Colors.teal[100],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    constraints: BoxConstraints(
                      maxWidth: MediaQuery.of(context).size.width * 0.75,
                    ),
                    child: Text(msg['message']!),
                  ),
                );
              },
            ),
          ),
          
          // Loading indicator
          if (_isLoading)
            Padding(
              padding: EdgeInsets.all(8),
              child: CircularProgressIndicator(),
            ),
          
          // Input field
          Container(
            padding: EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.grey.withOpacity(0.3),
                  blurRadius: 5,
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: InputDecoration(
                      hintText: 'Type your answer...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(25),
                      ),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                SizedBox(width: 10),
                FloatingActionButton(
                  onPressed: _sendMessage,
                  child: Icon(Icons.send),
                  mini: true,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

### Report Screen (`lib/screens/report_screen.dart`)

```dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ReportScreen extends StatelessWidget {
  final KashmirDishaAPI api;
  final String report;
  final String studentName;
  
  ReportScreen({
    required this.api,
    required this.report,
    required this.studentName,
  });
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Career Guidance Report'),
        backgroundColor: Colors.teal,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Report for $studentName',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 20),
            Text(report),
            SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: () {
                // TODO: Implement save/share functionality
              },
              icon: Icon(Icons.download),
              label: Text('Download Report'),
              style: ElevatedButton.styleFrom(
                minimumSize: Size(double.infinity, 50),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## Step 6: Update Main App

Edit `lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(KashmirDishaApp());
}

class KashmirDishaApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Kashmir Disha',
      theme: ThemeData(
        primarySwatch: Colors.teal,
      ),
      home: LoginScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
```

---

## Step 7: Run the App

### For Android:
```bash
flutter run
```

### For iOS (Mac only):
```bash
flutter run -d ios
```

### For Web (testing):
```bash
flutter run -d chrome
```

---

## Step 8: Test the Flow

1. **Enter Student ID**: `student_001`
2. **See Profile**: Name, stream, percentages
3. **Answer 10 Questions**: One by one
4. **Generate Report**: Click button after Q10
5. **View Report**: See detailed career guidance

---

## 🔧 Troubleshooting

### Issue: "Connection refused"
**Solution**: Make sure API server is running:
```bash
python3 api_server.py
```

### Issue: "Network error"
**Solution**: Check if phone and computer are on same WiFi

### Issue: "Timeout"
**Solution**: Update IP address in `api_service.dart` line 7

---

## 📱 Building APK (Android)

```bash
flutter build apk --release
```

APK will be in: `build/app/outputs/flutter-apk/app-release.apk`

---

## 🚀 Next Steps

1. Add loading animations
2. Implement report download/share
3. Add follow-up questions screen
4. Add error handling
5. Deploy API to cloud (Heroku/AWS)
6. Update API URL in production

---

**You're all set!** Your mobile app is now connected to the Kashmir Disha API! 🎉
