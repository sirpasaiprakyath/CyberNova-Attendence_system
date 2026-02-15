# QR Code Fix - Code Reference

## Admin Panel Changes (admin.html)

### 1. HTML: QR Data Display (insert after QR code div)
Location: Line ~545 in admin.html
```html
<div style="margin-top: 15px; display: none;" id="qrDataContainer">
    <div style="background: #f5f5f5; padding: 10px; border-radius: 6px; word-break: break-all; font-family: monospace; font-size: 12px; color: #666;" id="qrDataDisplay"></div>
    <button onclick="copyQRData()" class="copy-qr-btn" style="margin-top: 10px; width: 100%; padding: 8px; background: #667eea; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px;">Copy QR Data</button>
</div>
```

### 2. JavaScript: generateQRCode Function (REPLACEMENT)
Location: Line ~771 in admin.html
```javascript
function generateQRCode(qrData) {
    const container = document.getElementById('qrCode');
    container.innerHTML = '';
    
    // Store current QR data for copy functionality
    window.currentQRData = qrData;
    
    // Show QR data container
    document.getElementById('qrDataContainer').style.display = 'block';
    document.getElementById('qrDataDisplay').textContent = qrData;
    
    new QRCode(container, {
        text: qrData,
        width: 300,
        height: 300,
        colorDark: '#000000',
        colorLight: '#ffffff',
        correctLevel: QRCode.CorrectLevel.H
    });
}
```

### 3. JavaScript: copyQRData Function (NEW)
Location: Add after generateQRCode function
```javascript
function copyQRData() {
    if (!window.currentQRData) return;
    
    navigator.clipboard.writeText(window.currentQRData).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        btn.style.background = '#28a745';
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = '#667eea';
        }, 2000);
    }).catch(() => {
        alert('Failed to copy QR data');
    });
}
```

---

## Team Panel Changes (team.html)

### 1. HTML: Enhanced QR Input Section (REPLACEMENT)
Location: Lines ~398-404 in team.html
```html
<!-- QR Scanner Section -->
<div id="scannerSection" class="scanner-section">
    <h2>📱 Scan Session QR Code</h2>
    <p style="color: #666; margin-bottom: 15px; font-size: 14px;">Ask admin to display the QR code. You can either scan it with your device camera, paste the data below, or copy it from the admin panel.</p>
    
    <div id="qrInputContainer">
        <input type="text" id="qrInput" class="scanner-input" placeholder="Paste QR code data or scan here..." autocomplete="off">
        <button onclick="startQRScan()" class="scanner-btn" id="scanCameraBtn" style="background: #764ba2; margin-top: 10px;">📸 Use Camera to Scan</button>
        <button onclick="validateQRCode()" class="scanner-btn" id="validateBtn">Validate QR Code</button>
    </div>
    
    <div id="qrScannerContainer" style="display: none; margin-top: 15px;">
        <h3 style="margin-bottom: 10px;">Point camera at QR Code</h3>
        <div style="position: relative; max-width: 500px;">
            <video id="qrScanVideo" style="width: 100%; border-radius: 8px;" playsinline></video>
            <canvas id="qrScanCanvas" style="display: none;"></canvas>
        </div>
        <button onclick="stopQRScan()" class="scanner-btn" style="margin-top: 10px; background: #dc3545;">Cancel</button>
    </div>
</div>
```

### 2. JavaScript: Global Variables (ADD at start of script section)
Location: After line ~465 in team.html
```javascript
let qrScanningActive = false;
let qrScanStream = null;
let qrScanInterval = null;
```

### 3. JavaScript: QR Scanning Functions (ADD before validateQRCode)
Location: Around line ~490 in team.html
```javascript
// QR Code Camera Scanning
let qrScanningActive = false;
let qrScanStream = null;
let qrScanInterval = null;

async function startQRScan() {
    try {
        const video = document.getElementById('qrScanVideo');
        const canvas = document.getElementById('qrScanCanvas');
        const container = document.getElementById('qrScannerContainer');
        const inputContainer = document.getElementById('qrInputContainer');
        
        inputContainer.style.display = 'none';
        container.style.display = 'block';
        
        qrScanStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment' }
        });
        
        video.srcObject = qrScanStream;
        qrScanningActive = true;
        
        // Start scanning
        qrScanInterval = setInterval(scanQRFrame, 500);
    } catch (error) {
        showMessage('error', 'Camera access denied or not available');
        document.getElementById('qrInputContainer').style.display = 'block';
        document.getElementById('qrScannerContainer').style.display = 'none';
    }
}

function scanQRFrame() {
    const video = document.getElementById('qrScanVideo');
    const canvas = document.getElementById('qrScanCanvas');
    
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.hidden = false;
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: 'dontInvert',
        });
        
        if (code && code.data) {
            // Validate that it's proper QR data (should be JSON)
            try {
                const parsed = JSON.parse(code.data);
                if (parsed.sessionId && parsed.sessionType) {
                    // Found valid QR code!
                    stopQRScan();
                    document.getElementById('qrInput').value = code.data;
                    showMessage('success', 'QR code scanned successfully!');
                    
                    // Auto-validate after a short delay
                    setTimeout(() => validateQRCode(), 500);
                }
            } catch (e) {
                // Not valid JSON, continue scanning
            }
        }
    }
}

function stopQRScan() {
    qrScanningActive = false;
    
    if (qrScanStream) {
        qrScanStream.getTracks().forEach(track => track.stop());
        qrScanStream = null;
    }
    
    if (qrScanInterval) {
        clearInterval(qrScanInterval);
        qrScanInterval = null;
    }
    
    document.getElementById('qrInputContainer').style.display = 'block';
    document.getElementById('qrScannerContainer').style.display = 'none';
}
```

### 4. JavaScript: Enhanced validateQRCode Function (REPLACEMENT)
Location: Around line ~490 in team.html (after above functions)
```javascript
// QR Code Validation
async function validateQRCode() {
    hideMessage('error');
    hideMessage('success');
    
    const qrInput = document.getElementById('qrInput');
    const qrData = qrInput.value.trim();
    
    if (!qrData) {
        showMessage('error', 'Please enter or scan QR code data. It should look like: {"sessionId":"XXXXX","sessionType":"Morning"}');
        return;
    }
    
    // Validate that qrData is valid JSON
    try {
        JSON.parse(qrData);
    } catch (e) {
        showMessage('error', 'Invalid QR code format. The data must be valid JSON. You may have scanned an invalid QR code.');
        return;
    }
    
    const validateBtn = document.getElementById('validateBtn');
    validateBtn.disabled = true;
    validateBtn.innerHTML = '<span class="spinner"></span>Validating...';
    
    try {
        const response = await fetch('/api/team/validate-qr', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({qrData: qrData})
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentSessionData = {
                sessionId: data.sessionId,
                sessionType: data.sessionType
            };
            sessionStartTime = new Date().getTime();
            
            showMessage('success', data.message);
            openCamera();
            document.getElementById('scannerSection').style.display = 'none';
            
            // Start session timer
            updateSessionTimer();
            sessionTimerInterval = setInterval(updateSessionTimer, 1000);
        } else {
            showMessage('error', data.error || 'QR validation failed');
            validateBtn.disabled = false;
            validateBtn.textContent = 'Validate QR Code';
        }
    } catch (error) {
        showMessage('error', 'Error: ' + error.message);
        validateBtn.disabled = false;
        validateBtn.textContent = 'Validate QR Code';
    }
}
```

### 5. HTML: jsQR Library Import (ADD before closing </body> tag)
Location: Line ~791 in team.html
```html
<script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>
</body>
</html>
```

---

## Backend (app.py)

### No Changes Required! ✅

The backend code in `app.py` is already correctly handling QR validation:

```python
@app.route('/api/team/validate-qr', methods=['POST'])
@team_login_required
def validate_qr():
    """Validate QR code data"""
    if not FIREBASE_ENABLED:
        return jsonify({'success': False, 'error': 'Firebase not configured...'}), 503
    
    data = request.get_json()
    qr_data = data.get('qrData', '')
    
    try:
        qr_json = json.loads(qr_data)  # ← Expects JSON string
        session_id = qr_json.get('sessionId')
        session_type = qr_json.get('sessionType')
    except:
        return jsonify({'success': False, 'error': 'Invalid QR code'}), 400
    
    # ... rest of validation
```

---

## Summary of Changes

| Component | Old | New | Impact |
|-----------|-----|-----|--------|
| Admin HTML | QR only | QR + data + copy button | Better UX |
| Team HTML | Text input | Text input + camera scanner | More options |
| Admin JS | generateQRCode | Enhanced version | Displays data |
| Team JS | validateQRCode | Enhanced + new functions | Better validation |
| Backend | (no changes) | (no changes) | ✅ Compatible |
| Libraries | (none) | jsQR from CDN | Enables scanning |

---

## Installation Checklist

- [ ] Update `templates/admin.html`
- [ ] Update `templates/team.html`
- [ ] No changes to `app.py`
- [ ] No changes to database
- [ ] No new packages to install
- [ ] Clear browser cache (Ctrl+Shift+Del)
- [ ] Test admin copy button
- [ ] Test team paste validation
- [ ] Test team camera scan
- [ ] Verify error messages

---

## Rollback Instructions

If you need to revert to the previous version:

1. Restore original `admin.html` from backup
2. Restore original `team.html` from backup
3. No database or backend changes to revert

---

## Testing Endpoints

### Generate QR Code
```
GET /admin → Start Session → Creates QR
```

### Validate QR Code
```
POST /api/team/validate-qr
Body: {"qrData": "{\"sessionId\":\"ABC\",\"sessionType\":\"Morning\"}"}
Response: {"success": true, ...}
```

---

**Code Version:** 2.0  
**Last Updated:** 2024  
**Status:** ✅ Complete
