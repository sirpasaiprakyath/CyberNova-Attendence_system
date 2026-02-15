# SETUP & QUICK START GUIDE

## 🚀 One-Line Quick Start (Windows)

Simply double-click: **run.bat**

---

## 📋 Manual Setup (All Platforms)

### Step 1: Prerequisites
- Python 3.8+ installed
- Modern browser with camera support
- Administrator access (for virtual environment)

### Step 2: Navigate to Project
```bash
cd attendence
```

### Step 3: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run Application
```bash
# Windows
python app.py

# macOS/Linux
python3 app.py
```

### Step 6: Access Application
Open browser to: **http://127.0.0.1:5000**

---

## 🔐 Login Credentials

### Admin Login
- **URL**: http://127.0.0.1:5000
- **Role**: Admin
- **Username**: `admin`
- **Password**: `hackathon2026`

### Team Login
- **URL**: http://127.0.0.1:5000
- **Role**: Team Lead
- **Team ID**: `TEAM001` (or TEAM002, TEAM003, etc.)
- **Password**: `pass001` (corresponding to team)

---

## 📱 Typical Workflow

### For Admin
1. Login with admin credentials
2. Select session type (Morning/Evening/Night)
3. Click **"Start Session"**
4. QR code appears on screen
5. **Project the QR code** to team leads
6. Monitor **Attendance Records** tab
7. Click **"Verify"** after physical check
8. Click **"End Session"** when done

### For Team Lead
1. Login with team credentials
2. **Scan the QR code** shown by admin
3. Camera opens automatically
4. **Position team in frame** and click **"Capture Selfie"**
5. Review preview and click **"Submit Attendance"**
6. See confirmation message

---

## ✅ What to Verify

After startup, you should see:
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

If you see this, **the system is ready!**

---

## 🎯 Testing the System

### Quick Test Flow (5 minutes)
1. **Open two browser windows**
   - Window 1: Admin panel
   - Window 2: Team page

2. **In Admin window**
   - Login as admin
   - Start a session

3. **In Team window**
   - Login as TEAM001 / pass001
   - Scan/paste the session ID
   - Take a selfie
   - Submit

4. **Back in Admin window**
   - See submission appear in real-time
   - Click "Verify"

---

## 🚨 Common Issues & Fixes

### Issue: "Port 5000 already in use"
**Solution**: Change port in app.py
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Change 5000 to 5001
```

### Issue: "Camera access denied"
**Solutions**:
- Allow camera in browser permissions
- Restart browser
- Try incognito mode
- Use https://localhost instead of http://127.0.0.1

### Issue: "Database locked"
**Solution**:
1. Close the application
2. Delete `attendance.db`
3. Restart the application (DB will recreate)

### Issue: "Module not found"
**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: "Virtual environment not activating"
**Windows Solution**:
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux Solution**:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📂 Expected Project Structure After Setup

```
attendence/
├── app.py                    ✓ Main Flask app
├── requirements.txt          ✓ Python dependencies
├── README.md                 ✓ Full documentation
├── SETUP.md                  ✓ This file
├── run.bat                   ✓ Windows startup
├── run.sh                    ✓ macOS/Linux startup
├── .gitignore                ✓ Git ignore rules
│
├── templates/
│   ├── login.html            ✓ Login page
│   ├── admin.html            ✓ Admin dashboard
│   └── team.html             ✓ Team attendance
│
├── static/
│   └── css/
│       └── style.css         ✓ Global styles
│
├── uploads/                  ✓ Selfie images (created on first run)
│   ├── TEAM001_ABC123_1705107600.jpg
│   ├── TEAM002_ABC123_1705107621.jpg
│   └── ...
│
└── attendance.db             ✓ SQLite database (created on first run)
```

---

## 🔧 Configuration & Customization

### Add More Teams
Edit `app.py`:
```python
TEAMS = {
    'TEAM001': {'name': 'Alpha Squadron', 'password': 'pass001'},
    'TEAM002': {'name': 'Beta Force', 'password': 'pass002'},
    'TEAM006': {'name': 'Your Team', 'password': 'yourpass'},  # Add here
}
```

### Change Admin Password
Edit `app.py`:
```python
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'your_new_password'
```

### Adjust Session Duration
Edit `app.py` (find this line):
```python
if elapsed > 15:  # 15 minutes - change this number
```

### Change Port
Edit `app.py` (last line):
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Change 5000 to your port
```

---

## 📊 Database Management

### View All Attendance Records
```bash
# Windows
python
>>> import sqlite3
>>> conn = sqlite3.connect('attendance.db')
>>> c = conn.cursor()
>>> c.execute('SELECT * FROM attendance')
>>> for row in c.fetchall():
...     print(row)

# macOS/Linux
python3 (same commands)
```

### Reset Database
```bash
1. Close the application
2. Delete attendance.db
3. Restart application (automatically recreates)
```

### Backup Database
```bash
# Windows
copy attendance.db attendance_backup.db

# macOS/Linux
cp attendance.db attendance_backup.db
```

---

## 🎓 Recommended Usage

### For Hackathon Event
1. **Before Event**: Verify system is working, test camera
2. **During Event**: 
   - Run admin panel on projector/monitor
   - Teams use personal devices
   - Admin verifies each submission
3. **After Event**: Export attendance records

### For Testing
1. Use **run.bat** or **run.sh** for quick start
2. Open two browser windows
3. Test both admin and team flows
4. Delete attendance.db if you want to reset

---

## 💡 Pro Tips

1. **Projector Setup**: 
   - Display admin dashboard on projector
   - Show QR code in full screen
   - Teams can easily scan from distance

2. **Mobile Teams**:
   - System works great on phones
   - Camera orientation automatically adjusts
   - Responsive design for all screen sizes

3. **Backup Images**:
   - All selfies stored in `/uploads` folder
   - Can manually backup before event ends
   - Filenames include timestamp for sorting

4. **Session Management**:
   - Start new session for each period (morning/evening/night)
   - Each team submits once per session
   - Cannot resubmit for same session

---

## ❓ FAQ

**Q: Can multiple teams submit at the same time?**
A: Yes! The system handles concurrent submissions.

**Q: What if internet goes down?**
A: System works on localhost, no internet needed (except for QR library).

**Q: Can I add more team credentials later?**
A: Yes, edit the `TEAMS` dictionary in `app.py` and restart.

**Q: Are images compressed?**
A: Yes, JPEG at 95% quality to balance size and clarity.

**Q: What if a team forgets to submit?**
A: Admin can manually note the team as absent in records.

**Q: Can I use this on my phone?**
A: Yes, but admin features are better on desktop. Teams work great on phones.

---

## 📞 Getting Help

1. **Check README.md** for detailed documentation
2. **Check browser console** (F12) for JavaScript errors
3. **Check Flask output** for Python errors
4. **Verify camera permissions** in browser settings
5. **Try different browser** if issues persist

---

## ✨ Next Steps

After setup:
1. ✅ Verify system runs without errors
2. ✅ Test admin login
3. ✅ Test team login
4. ✅ Take a test selfie
5. ✅ Verify admin dashboard shows submission
6. ✅ Check `/uploads` folder for saved images
7. ✅ Review `attendance.db` database

**You're ready to go! 🎉**

---

**Last Updated**: January 2026
**Status**: Production Ready
**Version**: 1.0.0
