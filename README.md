# 🎯 Hackathon Attendance System

A cloud-native full-stack web application for managing live selfie-based attendance using QR codes. Built with Python Flask, **Firebase (Firestore + Storage)**, and vanilla JavaScript.

**🔄 FIREBASE VERSION - Refactored from SQLite to cloud infrastructure**

## ✨ Features

### Core Functionality
- **QR-based Session Management**: Admin creates sessions and generates QR codes
- **Live Selfie Capture**: Teams must capture live selfies using camera (no file uploads)
- **Real-time Dashboard**: Admin sees attendance submissions in real-time with live image preview
- **Session Expiration**: Sessions auto-expire after 15 minutes
- **Attendance Verification**: Admin can verify submissions with physical checks
- **One Submission per Session**: Prevents duplicate submissions
- **Cloud Storage**: All images stored securely in Firebase Storage with public access URLs

### Security & Constraints
- ✅ **No File Upload Access**: Only live camera capture allowed
- ✅ **Session Validation**: QR codes contain session data
- ✅ **Team Authentication**: Hardcoded team credentials
- ✅ **Admin Panel**: Secured with admin login
- ✅ **Device Binding**: Attendance tied to sessionId, teamId, and timestamp
- ✅ **Cloud Credentials**: Firebase service account authentication
- ✅ **Image Compression**: Automatic JPEG compression (1920x1440, 90% quality)

### Technology Stack
- **Backend**: Python Flask 3.0.0
- **Database**: Firebase Firestore (NoSQL, real-time, scalable)
- **Storage**: Firebase Cloud Storage (secure, globally distributed)
- **Authentication**: Firebase Admin SDK with service account
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (no framework)
- **Image Processing**: Pillow/PIL for compression
- **Hosting**: Can be deployed to Firebase, Cloud Run, Heroku, AWS, etc.

---

## 📋 Project Structure

```
attendence/
├── app.py                      # Flask backend with Firebase integration
├── requirements.txt            # Python dependencies (firebase-admin, Pillow)
├── templates/
│   ├── login.html             # Login page (admin/team)
│   ├── admin.html             # Admin dashboard
│   └── team.html              # Team attendance page
├── static/
│   ├── css/
│   │   └── style.css          # Global styles
│   └── js/                    # JavaScript files
├── FIREBASE_SETUP.md          # Detailed Firebase configuration guide
├── FIREBASE_REFACTORING.md    # Architecture overview
├── FIREBASE_COMPLETION.md     # Completion summary
├── setup_firebase.bat         # Windows automated setup script
└── .env.example               # Environment variable template
```

---

## 🚀 Quick Start (Firebase Version)

### Prerequisites
- Python 3.8 or higher
- Modern web browser with camera access (Chrome, Firefox, Edge, Safari)
- Firebase account (free tier available)
- Service account JSON key from Firebase

### ⚡ Express Setup (Windows)
```batch
# 1. Download service account key (see FIREBASE_SETUP.md)
# 2. Run setup script
setup_firebase.bat
```

### Manual Setup (All Platforms)
```bash
# 1. Set environment variables
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/serviceAccountKey.json"
export FIREBASE_STORAGE_BUCKET="your-project-id.appspot.com"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python app.py
```

### Installation

1. **Navigate to the project folder**
```bash
cd attendence
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python app.py
```

**Output:**
```
============================================================
HACKATHON ATTENDANCE SYSTEM
============================================================

Admin Credentials:
  Username: admin
  Password: hackathon2026

Team Credentials (Sample):
  TEAM001: Alpha Squadron / pass001
  TEAM002: Beta Force / pass002
  TEAM003: Gamma Legends / pass003

Server running on: http://127.0.0.1:5000
============================================================
```

Open your browser to: **http://127.0.0.1:5000**

---

## 🎮 Usage Guide

### Admin Panel

#### Login
1. Go to http://127.0.0.1:5000
2. Select "Admin" role
3. Username: `admin`
4. Password: `hackathon2026`

#### Start a Session
1. Select session type: **Morning**, **Evening**, or **Night**
2. Click **"Start Session"**
3. A unique `sessionId` is generated
4. **QR Code is displayed** for team leads to scan
5. Session remains active for **15 minutes**

#### Monitor Attendance
1. Go to **"Attendance Records"** tab
2. See real-time submissions with:
   - Team ID & Name
   - Session type
   - Timestamp
   - Selfie preview (click to enlarge)
   - Current status (Pending/Verified)
3. Click **"Verify"** after physical confirmation

#### End Session
1. Click **"End Session"** button
2. Session becomes inactive
3. No more submissions accepted

---

### Team Lead Page

#### Login
1. Go to http://127.0.0.1:5000
2. Select "Team Lead" role
3. Team ID: `TEAM001` (or other team codes)
4. Password: `pass001` (corresponding to team)

#### Submit Attendance
1. **Scan QR Code**: Ask admin to display the QR code
   - Option A: Use camera to scan directly
   - Option B: Manually paste QR data

2. **Camera Opens Automatically**
   - Position team members in frame
   - Ensure good lighting
   - Include all team members

3. **Capture Selfie**: Click **"Capture Selfie"**

4. **Review**: Preview the captured image
   - **"Retake"**: Capture again if unclear
   - **"Submit Attendance"**: Submit to system

5. **Confirmation**: See success message with timestamp

---

## 👥 Demo Credentials

### Admin
```
Username: admin
Password: hackathon2026
```

### Teams (Hardcoded Sample Data)
```
TEAM001 / Alpha Squadron / pass001
TEAM002 / Beta Force / pass002
TEAM003 / Gamma Legends / pass003
TEAM004 / Delta Strike / pass004
TEAM005 / Epsilon Coders / pass005
```

---

## 🗄️ Database Schema

### Sessions Table
```sql
CREATE TABLE sessions (
    sessionId TEXT PRIMARY KEY,
    sessionType TEXT NOT NULL,      -- Morning/Evening/Night
    startTime TEXT NOT NULL,        -- ISO timestamp
    endTime TEXT,
    active BOOLEAN DEFAULT 1
);
```

### Attendance Table
```sql
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teamId TEXT NOT NULL,
    sessionId TEXT NOT NULL,
    sessionType TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    imagePath TEXT NOT NULL,        -- Filename in /uploads
    status TEXT DEFAULT 'Pending',  -- Pending/Verified
    UNIQUE(teamId, sessionId)       -- One submission per team per session
);
```

---

## 📁 Image Storage

- Location: `/uploads` folder
- Format: JPEG images
- Naming: `TEAMID_SESSIONID_TIMESTAMP.jpg`
- Size: Up to 10MB per image
- **Security**: Only accessible via admin dashboard

---

## 🔒 Security Features

1. **Session Binding**: Each submission tied to `sessionId + teamId`
2. **One-time Submission**: Duplicate submissions prevented via UNIQUE constraint
3. **Live Capture Only**: `getUserMedia()` enforced (no file upload)
4. **Time Expiration**: 15-minute session window enforced server-side
5. **No Directory Traversal**: Uploaded filenames validated
6. **CORS & Headers**: Secure request handling

---

## 🎨 Features Implemented

### Admin Features
- ✅ Session creation with type selection
- ✅ QR code generation and display
- ✅ Real-time attendance feed
- ✅ Image preview modal
- ✅ Manual verification toggle
- ✅ Session timer (15 minutes)
- ✅ Active/inactive status display
- ✅ Logout functionality

### Team Features
- ✅ QR code validation (scan or paste)
- ✅ Live camera access (getUserMedia)
- ✅ Selfie capture & preview
- ✅ Retake option
- ✅ Session timer display
- ✅ Real-time status messages
- ✅ Success/error handling
- ✅ Mobile-responsive design

### Backend Features
- ✅ RESTful API endpoints
- ✅ SQLite database with schema
- ✅ Base64 image encoding/decoding
- ✅ File management in /uploads
- ✅ Session expiration validation
- ✅ Error handling & logging

---

## 🌐 API Endpoints

### Authentication
```
POST /login                    # Login (admin/team)
GET  /logout                   # Logout
```

### Admin Routes
```
GET  /admin                    # Admin dashboard
POST /api/admin/start-session  # Start new session
POST /api/admin/end-session    # End current session
GET  /api/admin/session-status # Get session status
POST /api/admin/verify-attendance/<id>  # Verify record
GET  /api/admin/attendance-feed         # Real-time feed
```

### Team Routes
```
GET  /team                          # Team page
POST /api/team/validate-qr          # Validate QR code
POST /api/team/submit-attendance    # Submit selfie + data
GET  /api/team/attendance-status/<sessionId>  # Check submission
```

### Image Serving
```
GET  /uploads/<filename>    # Serve stored images
```

---

## 🛠️ Troubleshooting

### Camera Not Accessing
- **Check browser permissions**: Allow camera access in browser settings
- **Use HTTPS or localhost**: Some browsers require secure context
- **Try different browser**: Chrome/Firefox generally more reliable
- **Ensure good lighting**: Required for clear selfies

### Session Expired
- Sessions last exactly 15 minutes
- Ask admin to start a new session
- Re-scan the QR code

### Already Submitted Error
- One submission per team per session
- Cannot resubmit for same session
- Wait for admin to start new session

### Database Errors
- Delete `attendance.db` to reset (will recreate on startup)
- Check folder permissions on `/uploads`
- Ensure Flask has write access

---

## 📱 Mobile Considerations

- **Responsive Design**: Works on tablets and smartphones
- **Camera Orientation**: Automatically handles portrait/landscape
- **Touch Optimization**: Larger buttons for mobile
- **Bandwidth**: Images compressed to JPEG (95% quality)

---

## 🔧 Customization

### Add More Teams
Edit hardcoded `TEAMS` dictionary in `app.py`:
```python
TEAMS = {
    'TEAM006': {'name': 'New Team Name', 'password': 'pass006'},
    # ...
}
```

### Change Admin Credentials
Edit in `app.py`:
```python
ADMIN_USERNAME = 'your_username'
ADMIN_PASSWORD = 'your_password'
```

### Session Duration
Change 15-minute expiration in `app.py`:
```python
if elapsed > 15:  # Change this value
```

### Maximum Image Size
Edit in `app.py`:
```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

---

## 📊 Testing Workflow

1. **Open two browser windows/tabs**:
   - Tab 1: Admin dashboard (http://localhost:5000)
   - Tab 2: Team page (http://localhost:5000)

2. **Admin**: Start a Morning session
3. **Team**: Scan QR code (or copy sessionId from admin)
4. **Team**: Take selfie and submit
5. **Admin**: See submission in real-time
6. **Admin**: Click "Verify" after physical check

---

## 🚀 Deployment Tips

### For Production
1. Change secret key in `app.py`
2. Set `debug=False` in `app.run()`
3. Use proper WSGI server (Gunicorn, uWSGI)
4. Enable HTTPS
5. Move credentials to environment variables
6. Set up proper file permissions on `/uploads`

### Run with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📝 Notes

- All times are stored in ISO format
- Images are base64-encoded during transmission
- QR codes are generated client-side using QRCode.js library
- Camera stream is properly cleaned up on navigation
- Database uses SQLite3 (included with Python)

---

## 📄 License

This project is provided as-is for hackathon use.

---

## ✉️ Support

For issues or questions:
1. Check troubleshooting section above
2. Verify all files are in correct location
3. Check browser console for JavaScript errors
4. Verify Python version and dependencies

---

**Happy Hacking! 🎉**
