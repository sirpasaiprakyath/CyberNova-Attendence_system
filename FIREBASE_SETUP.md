# Firebase Setup Guide

This guide walks you through configuring Firebase for the Hackathon Attendance System.

## Prerequisites

- A Google account
- Python 3.8+
- The Hackathon Attendance System files

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Create a project"**
3. Enter project name: `Hackathon-Attendance`
4. (Optional) Enable Google Analytics
5. Click **Create project** and wait for setup to complete

## Step 2: Set Up Firestore Database

1. In Firebase Console, go to **Build** → **Firestore Database**
2. Click **Create Database**
3. Select location (closest to your region)
4. Start in **Production mode** (we'll add security rules)
5. Click **Enable**

### Firestore Collections Structure

The system automatically creates these collections:

- **sessions**: Stores active attendance sessions
  ```
  Document ID: sessionId
  Fields:
    - sessionId: string
    - type: string (e.g., "Attendance", "Lunch Break")
    - startTime: ISO timestamp string
    - active: boolean
  ```

- **attendance**: Stores submitted attendance records
  ```
  Document ID: teamId_sessionId
  Fields:
    - teamId: string
    - sessionId: string
    - sessionType: string
    - timestamp: ISO timestamp string
    - imageURL: string (Firebase Storage public URL)
    - status: string ("Pending" or "Verified")
  ```

## Step 3: Set Up Cloud Storage

1. In Firebase Console, go to **Build** → **Storage**
2. Click **Get Started**
3. Select location (same as Firestore)
4. Start in **Production mode**
5. Click **Done**

### Storage Security Rules

Replace the default rules with these in the **Rules** tab:

```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Allow reading selfies (public read)
    match /selfies/{allPaths=**} {
      allow read;
      allow write: if request.auth != null;
    }
    
    // Deny everything else
    match /{allPaths=**} {
      allow read, write: if false;
    }
  }
}
```

## Step 4: Create Service Account Key

1. In Firebase Console, click **⚙️ Settings** (top-left)
2. Go to **Service Accounts**
3. Click **Generate New Private Key**
4. A JSON file will download (e.g., `hackathon-attendance-xxxxx.json`)
5. **Save this file securely** - it contains credentials

## Step 5: Configure Environment Variables

### Option A: Windows (Command Prompt)

```batch
# Set the service account key path
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\serviceAccountKey.json

# Set the storage bucket name
set FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com

# Run the app
python app.py
```

### Option B: Windows (PowerShell)

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\your\serviceAccountKey.json"
$env:FIREBASE_STORAGE_BUCKET = "your-project-id.appspot.com"
python app.py
```

### Option C: Linux/Mac

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/serviceAccountKey.json"
export FIREBASE_STORAGE_BUCKET="your-project-id.appspot.com"
python app.py
```

### Finding Your Storage Bucket Name

1. In Firebase Console, go to **Storage**
2. Your bucket name is displayed at the top
3. Format: `project-id.appspot.com`

## Step 6: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 7: Run the Application

```bash
python app.py
```

You should see output like:
```
============================================================
HACKATHON ATTENDANCE SYSTEM - FIREBASE VERSION
============================================================

Firebase Configuration:
  Credentials: C:\path\to\serviceAccountKey.json
  Storage Bucket: your-project-id.appspot.com

Admin Credentials:
  Username: admin
  Password: [admin_password]

Team Credentials (Sample):
  team1: Team Alpha / password1
  team2: Team Beta / password2
  team3: Team Gamma / password3

Server running on: http://127.0.0.1:5000
============================================================
```

## Step 8: Verify Firebase Connection

1. Open http://127.0.0.1:5000 in your browser
2. Login as admin
3. Create a new session
4. Login as a team and take a selfie
5. In Firebase Console → Firestore, verify:
   - **sessions** collection has your session
   - **attendance** collection has your submission
6. In Firebase Console → Storage, verify:
   - **selfies** folder contains your image

## Firestore Security Rules (Optional)

For production, add these rules in **Storage Rules** tab:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Sessions (read-only for auth users)
    match /sessions/{sessionId} {
      allow read: if request.auth != null;
      allow write: if false;
    }
    
    // Attendance (team can write, admin can read)
    match /attendance/{docId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
  }
}
```

## Troubleshooting

### Error: "GOOGLE_APPLICATION_CREDENTIALS not set"
- Verify the environment variable is set correctly
- Check file path exists and is readable
- Restart terminal/command prompt after setting variable

### Error: "Bucket not found"
- Verify storage bucket name is correct
- Check it's in the format `project-id.appspot.com`
- Verify Firebase Storage is enabled in your project

### Error: "Permission denied" when uploading image
- Check Storage security rules allow writes
- Verify service account has Storage permissions

### Images not uploading
- Check FIREBASE_STORAGE_BUCKET environment variable
- Verify Storage quota not exceeded
- Check browser console for JavaScript errors

### Firestore queries not working
- Verify Firestore database is created
- Check service account has Firestore permissions
- Verify collections/documents are being created in console

## Billing & Quotas

Firebase Free tier includes:
- Firestore: 1 GB storage, 50K reads/day
- Storage: 5 GB total, 1 GB/day download

For a hackathon with ~50 teams and ~5 sessions:
- ~250 attendance records (~1 KB each = 250 KB)
- ~250 images (~200 KB each = 50 MB)
- Total: ~50 MB storage, well within free tier

## Backing Up Your Data

### Firestore Backup
1. Go to **Firestore Database**
2. Click **Start Collection Export** (⋮ menu)
3. Choose destination GCS bucket
4. Export will be saved as JSON

### Storage Backup
1. Go to **Storage**
2. Download folder manually from console
3. Or use `gsutil cp -r gs://bucket-name/* local-folder`

## Production Deployment

When deploying to production:

1. Move `serviceAccountKey.json` to secure location
2. Use environment variables or secret manager
3. Never commit `serviceAccountKey.json` to git
4. Enable Firestore/Storage security rules
5. Set up billing alert
6. Enable audit logging

## Additional Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Best Practices](https://firebase.google.com/docs/firestore/best-practices)
- [Cloud Storage Security Rules](https://firebase.google.com/docs/storage/security)

