import requests
import json
import time

BASE_URL = 'http://127.0.0.1:5001' # Updated port
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
        print(f"❌ Failed: Could not connect to server at {BASE_URL}. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

print("Starting verification (writing to file)...")
with open('verification_results.txt', 'w', encoding='utf-8') as f:
    f.write("=== Starting Unified Login Verification (Port 5001) ===\n")
    
    # 1. Test Admin Login
    print("Testing Admin Login...")
    f.write("\n--- Testing Admin Login ---\n")
    if test_login('CyberNova', 'Owasp@CyberNova', True, '/admin'):
        f.write("✅ Admin Login Success\n")
    else:
        f.write("❌ Admin Login Failed\n")

    # 2. Test Hunter Login
    print("Testing Hunter Login...")
    f.write("\n--- Testing Hunter Login ---\n")
    if test_login('HUNTER001', 'pass001', True, '/hunter'):
        f.write("✅ Hunter Login Success\n")
    else:
        f.write("❌ Hunter Login Failed\n")

    # 3. Test Invalid Credentials
    print("Testing Invalid Credentials...")
    f.write("\n--- Testing Invalid Credentials ---\n")
    if test_login('invalid', 'user', False):
        f.write("✅ Invalid Login Rejected Correctly\n")
    else:
        f.write("❌ Invalid Login Check Failed (Backend accepted it!)\n")

    f.write("\n=== Verification Complete ===\n")
    print("Verification complete.")
