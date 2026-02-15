import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:5000"
ADMIN_CREDENTIALS = {"username": "admin", "password": "hackathon2026", "role": "admin"}
TEAM_CREDENTIALS = {"username": "TEAM001", "password": "pass001", "role": "team"}

def test_session_persistence():
    s = requests.Session()
    
    print("1. Logging in as Admin...")
    resp = s.post(f"{BASE_URL}/login", json=ADMIN_CREDENTIALS)
    print(f"   Status: {resp.status_code}")
    print(f"   Cookies: {s.cookies.get_dict()}")
    
    if resp.status_code != 200 or 'redirect' not in resp.json():
        print("   ❌ Admin login failed")
        return

    print("\n2. Checking Admin Dashboard (should be allowed)...")
    resp = s.get(f"{BASE_URL}/admin")
    if resp.url.endswith('/login'):
        print("   ❌ Redirected to login! (Unexpected early failure)")
    else:
        print("   ✅ Access granted")

    print("\n3. Logging in as Team (same session)...")
    # This simulates the user logging in as Team IN THE SAME BROWSER SESSION
    resp = s.post(f"{BASE_URL}/login", json=TEAM_CREDENTIALS)
    print(f"   Status: {resp.status_code}")
    print(f"   Cookies: {s.cookies.get_dict()}")
    
    if resp.status_code != 200:
        print("   ❌ Team login failed")
        return

    print("\n4. Checking Admin Dashboard AGAIN (should still be allowed)...")
    resp = s.get(f"{BASE_URL}/admin")
    
    if resp.url.endswith('/login') or '<title>Hackathon Attendance - Login</title>' in resp.text:
        print("   ❌ Make sure the admin is not redirected to login.")
        print("   ❌ ISSUE REPRODUCED: Admin session lost after Team login!")
    else:
        print("   ✅ Admin Access preserved! (Issue NOT reproduced with simple login flow)")

    # If simple login didn't break it, let's try submitting attendance
    # We need a valid session ID for this.
    # Start a session as Admin first (we need to reclaim admin rights if lost, but let's assume we have them or use a separate admin session just to set up)
    
    # Actually, if we lost access, we can't start a session.
    # But if we didn't, let's try the full flow.

if __name__ == "__main__":
    try:
        test_session_persistence()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure app.py is running.")
