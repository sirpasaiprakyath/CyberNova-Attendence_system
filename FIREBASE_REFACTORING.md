# Firebase Refactoring - Quick Start

The Hackathon Attendance System has been **fully refactored from SQLite to Firebase (Firestore + Storage)**.

## What Changed?

### Backend
- ✅ **No SQLite** - Replaced with Firestore (cloud database)
- ✅ **Local image storage** → **Firebase Storage** with public URLs
- ✅ **Database queries** → **Firestore queries** (real-time, scalable)
- ✅ **Session validation** - Enhanced with Firestore transactions
- ✅ **Image compression** - Added PIL for efficient storage

### Frontend
- ✅ **No changes** - Still forces live camera, same UI/UX

## Get Started in 3 Steps

### Step 1: Configure Firebase (5 minutes)

1. **Get credentials file** (FIREBASE_SETUP.md has detailed instructions):
   - Create Firebase project at console.firebase.google.com
   - Download service account key JSON file
   - Get your storage bucket name

2. **Set environment variables**:

   **Windows (Command Prompt):**
   ```batch
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\serviceAccountKey.json
   set FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
   ```

   **Windows (PowerShell):**
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\serviceAccountKey.json"
   $env:FIREBASE_STORAGE_BUCKET = "your-project-id.appspot.com"
   ```

   **Linux/Mac:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/serviceAccountKey.json"
   export FIREBASE_STORAGE_BUCKET="your-project-id.appspot.com"
   ```

### Step 2: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

This installs:
- `firebase-admin` - Firebase SDK for Python
- `Pillow` - Image compression library

### Step 3: Run the App (1 minute)

```bash
python app.py
```

You'll see:
```
HACKATHON ATTENDANCE SYSTEM - FIREBASE VERSION
Firebase Configuration:
  Credentials: [path]
  Storage Bucket: [bucket-name]
```

Open http://127.0.0.1:5000 and use it normally!

## Architecture

### Data Flow

```
TEAM SUBMISSION (Selfie):
1. Team takes photo with camera → Base64 image
2. POST /api/team/submit-attendance
3. Validate: session active, team registered, no duplicate
4. Compress image with PIL (JPEG, 1920x1440, 90% quality)
5. Upload to Firebase Storage → Get public URL
6. Store in Firestore: {teamId, sessionId, timestamp, imageURL, status}
7. Return success to frontend

ADMIN VIEW (Live Feed):
1. GET /api/admin/attendance-feed
2. Query Firestore: attendance collection, sorted by timestamp
3. For each record, get imageURL (public link from Storage)
4. Stream JSON response with real-time updates
```

### Firestore Collections

**sessions**
```json
{
  "sessionId": "session_1",
  "type": "Attendance",
  "startTime": "2024-01-15T10:00:00",
  "active": true
}
```

**attendance**
```json
{
  "teamId": "team1",
  "sessionId": "session_1",
  "sessionType": "Attendance",
  "timestamp": "2024-01-15T10:05:23",
  "imageURL": "https://storage.googleapis.com/...",
  "status": "Pending"
}
```

### Firebase Storage Structure

```
gs://bucket-name/
  └── selfies/
      ├── team1_session_1_1234567890.jpg
      ├── team2_session_1_1234567891.jpg
      └── ...
```

## Key Features Preserved

✅ Live camera capture enforced (getUserMedia only)
✅ No file upload dialog
✅ One submission per team per session (Firestore UNIQUE constraint)
✅ 15-minute session expiration
✅ Admin dashboard with real-time feed
✅ QR code validation
✅ All security checks maintained

## Security

- Service account credentials in JSON file (never commit to git!)
- Firebase security rules control who can read/write
- Images stored with public read access (for displaying in admin console)
- Attendance records restricted to authenticated users

## Troubleshooting

| Error | Fix |
|-------|-----|
| "Firebase not initialized" | Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable |
| "Bucket not found" | Set `FIREBASE_STORAGE_BUCKET` environment variable |
| Image upload fails | Check Storage security rules in Firebase console |
| No data in Firestore | Verify Firestore database is enabled |

See FIREBASE_SETUP.md for detailed troubleshooting.

## Next Steps

1. **Verify Setup**: Login as admin, create session, team submits selfie
2. **Check Firebase Console**: See session in Firestore, image in Storage
3. **Scale Up**: Add more teams and sessions
4. **Deploy**: Follow Firebase hosting docs for production

## Files Modified

- `app.py` - Complete Firebase integration (helper functions, routes)
- `requirements.txt` - Added firebase-admin, Pillow
- `FIREBASE_SETUP.md` - Detailed setup instructions (NEW)
- Frontend files - No changes needed (works with new API)

## API Endpoints (Unchanged)

All endpoints work the same from frontend:

**Admin:**
- POST `/api/admin/login` - Admin login
- POST `/api/admin/start-session` - Create new session
- POST `/api/admin/end-session` - Close session
- POST `/api/admin/verify-attendance` - Approve submission
- GET `/api/admin/attendance-feed` - Real-time attendance list
- GET `/api/admin/session-status` - Current session info

**Team:**
- POST `/api/team/login` - Team login
- POST `/api/team/validate-qr` - Validate QR code
- POST `/api/team/submit-attendance` - Submit selfie (uploads to Storage, saves to Firestore)
- GET `/api/team/attendance-status` - Check submission status

## Code Quality

✅ No SQLite imports or usage
✅ All Firestore queries properly structured
✅ Error handling for Firebase failures
✅ Image compression before upload (saves bandwidth)
✅ Public URL generation for Storage images
✅ Session expiration validation

