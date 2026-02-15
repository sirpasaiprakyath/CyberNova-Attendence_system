
import requests
import sys

BASE_URL = "http://127.0.0.1:5001"
USERNAME = "admin"
PASSWORD = "hackathon2026"

def test_refresh():
    session = requests.Session()
    
    # Login
    print(f"Logging in to {BASE_URL}...")
    login_data = {'username': USERNAME, 'password': PASSWORD, 'role': 'admin'}
    response = session.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code != 200:
        print(f"Login failed: {response.status_code} {response.text}")
        sys.exit(1)
    
    print("Login successful.")
    
    # Test Refresh Endpoint
    print("Testing Refresh Endpoint (attendance-feed)...")
    response = session.get(f"{BASE_URL}/api/admin/attendance-feed")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Refresh successful! Received {len(data)} records.")
            print("Status: OK")
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            sys.exit(1)
    else:
        print(f"Refresh failed: {response.status_code} {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    test_refresh()
