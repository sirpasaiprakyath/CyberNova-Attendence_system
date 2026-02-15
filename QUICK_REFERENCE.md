# QUICK REFERENCE CARD

## 🚀 LAUNCH APPLICATION

### Windows
```
Double-click: run.bat
```

### macOS/Linux
```bash
bash run.sh
```

### Manual (All Platforms)
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Unix: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Access**: http://127.0.0.1:5000

---

## 🔐 LOGIN CREDENTIALS

### Admin Portal
```
Username: admin
Password: hackathon2026
```

### Teams
```
TEAM001 / pass001
TEAM002 / pass002
TEAM003 / pass003
TEAM004 / pass004
TEAM005 / pass005
```

---

## 📊 PROJECT FILES

| File | Purpose |
|------|---------|
| `app.py` | Flask backend (420 lines) |
| `requirements.txt` | Python dependencies |
| `run.bat` | Windows launcher |
| `run.sh` | Unix launcher |
| `templates/login.html` | Login form |
| `templates/admin.html` | Admin dashboard |
| `templates/team.html` | Team page |
| `static/css/style.css` | Stylesheets |
| `uploads/` | Saved images |
| `attendance.db` | SQLite database |

---

## 🎯 WORKFLOW

### Admin (5 Steps)
1. Login with admin credentials
2. Select session type → Click "Start Session"
3. **Display QR code** to teams
4. Monitor attendance in real-time
5. **Verify** submissions, then "End Session"

### Team Lead (4 Steps)
1. Login with team credentials
2. **Scan QR code** displayed by admin
3. **Take selfie** → Review → Submit
4. See confirmation message

---

## 🔒 SECURITY ENFORCED

✅ **NO file upload** - Live camera only  
✅ **getUserMedia forced** - No file picker  
✅ **One submission per session** - DB constraint  
✅ **15-minute expiration** - Auto timeout  
✅ **Session binding** - teamId + sessionId  

---

## 📱 FEATURES

### Admin
- [x] Session creation (Morning/Evening/Night)
- [x] QR code generation
- [x] Real-time attendance feed
- [x] Image preview modal
- [x] Manual verification
- [x] Session timer
- [x] Live status updates

### Team
- [x] QR scanning/validation
- [x] Live camera stream
- [x] Selfie capture & preview
- [x] Retake functionality
- [x] One-click submission
- [x] Success confirmation
- [x] Session countdown timer

---

## 🗄️ DATABASE

### Tables
```sql
sessions(sessionId, sessionType, startTime, active)
attendance(id, teamId, sessionId, timestamp, imagePath, status)
```

### Storage
- Images: `/uploads` folder
- Database: `attendance.db`

---

## 🐛 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Change port in app.py |
| Camera denied | Allow in browser settings |
| Session expired | Ask admin to start new session |
| Already submitted | Cannot resubmit same session |
| Database locked | Delete attendance.db and restart |

---

## 📊 API ENDPOINTS

### Authentication
```
POST   /login              (admin/team)
GET    /logout             (clear session)
```

### Admin
```
GET    /admin              (dashboard)
POST   /api/admin/start-session
POST   /api/admin/end-session
GET    /api/admin/session-status
GET    /api/admin/attendance-feed
POST   /api/admin/verify-attendance/<id>
```

### Team
```
GET    /team               (page)
POST   /api/team/validate-qr
POST   /api/team/submit-attendance
GET    /api/team/attendance-status/<sessionId>
```

### Images
```
GET    /uploads/<filename>
```

---

## 📱 RESPONSIVE DESIGN

- ✅ Desktop (1024px+) - Full layout
- ✅ Tablet (768px+) - Optimized
- ✅ Mobile (320px+) - Stacked layout

---

## 🔧 CUSTOMIZE

### Add Team
Edit `app.py`:
```python
'TEAM006': {'name': 'Your Team', 'password': 'pass006'},
```

### Change Password
Edit `app.py`:
```python
ADMIN_PASSWORD = 'new_password'
```

### Change Port
Edit `app.py` (last line):
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

---

## ✅ VERIFICATION CHECKLIST

After startup:
- [ ] System launches without errors
- [ ] Admin login works
- [ ] Team login works
- [ ] Can start session
- [ ] QR code displays
- [ ] Camera access works
- [ ] Can take selfie
- [ ] Submission appears in admin dashboard
- [ ] Image saved in `/uploads`
- [ ] Record in `attendance.db`

---

## 📚 DOCUMENTATION

| File | Contents |
|------|----------|
| `README.md` | Full documentation (350+ lines) |
| `SETUP.md` | Setup guide & troubleshooting |
| `IMPLEMENTATION_SUMMARY.md` | Feature checklist |
| `QUICK_REFERENCE.md` | This file |

---

## 🎓 TYPICAL SETUP

**Time**: 2-3 minutes

1. Run startup script
2. Open browser to http://127.0.0.1:5000
3. Login as admin
4. Start session
5. Project QR code
6. Teams scan & submit

---

## 💡 PRO TIPS

- Display admin dashboard on projector
- Show QR code in full screen
- Teams use personal devices
- Verify submissions after physical check
- Save `/uploads` folder before event ends
- Reset with fresh team list if needed

---

## 🎯 SYSTEM SPECIFICATIONS

- **Backend**: Python 3.8+, Flask 3.0
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Camera**: WebRTC getUserMedia API
- **Storage**: Local `/uploads` folder
- **Images**: JPEG (95% quality, max 10MB)

---

## 📞 SUPPORT

1. Check README.md for detailed docs
2. Check SETUP.md for troubleshooting
3. Verify browser console for errors (F12)
4. Check Flask terminal output
5. Try different browser if issues persist

---

**Status**: ✅ Production Ready | **Version**: 1.0.0 | **Date**: January 2026
