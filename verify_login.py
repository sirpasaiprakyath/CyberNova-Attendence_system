import requests
import json

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/login'

def test_login(username, password, expected_success, expected_redirect=None):
    print(f"Testing login for: {username} / {'*' * len(password)}")
    try:
        response = requests.post(LOGIN_URL, json={'username': username, 'password': password})
        data = response.json()
        
        if data.get('success') == expected_success:
            if expected_redirect and data.get('redirect') != expected_redirect:
                print(f"❌ Failed: Expected redirect to {expected_redirect}, got {data.get('redirect')}")
                return False
            print("✅ Success")
            return True
        else:
            print(f"❌ Failed: Expected success={expected_success}, got {data.get('success')} (Error: {data.get('error')})")
            print(f"Response: {data}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Failed: Could not connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

print("=== Starting Unified Login Verification ===")

# 1. Test Admin Login
print("\n--- Testing Admin Login ---")
if not test_login('admin', 'hackathon2026', True, '/admin'):
    print("CRITICAL: Admin login failed!")

# 2. Test Hunter Login
print("\n--- Testing Hunter Login ---")
if not test_login('HUNTER001', 'pass001', True, '/hunter'):
    print("CRITICAL: Hunter login failed!")

# 3. Test Invalid Credentials
print("\n--- Testing Invalid Credentials ---")
if not test_login('invalid', 'user', False):
    print("CRITICAL: Invalid login check failed!")

print("\n=== Verification Complete ===")
