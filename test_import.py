import requests
import io

BASE_URL = 'http://127.0.0.1:5001'
ADMIN_USERNAME = 'CyberNova'
ADMIN_PASSWORD = 'Owasp@CyberNova'

def login():
    session = requests.Session()
    login_data = {
        'username': ADMIN_USERNAME,
        'password': ADMIN_PASSWORD
    }
    response = session.post(f'{BASE_URL}/login', data=login_data)
    if response.status_code == 200 and 'Admin Panel' in response.text:
        print("✅ Login successful")
        return session
    else:
        print(f"❌ Login failed. Status: {response.status_code}")
        # print(response.text)
        return None

def test_import(session):
    # Create a dummy CSV file
    csv_content = "Hunter ID,Hunter Name,Register No\nTEST_IMPORT_001,Test Hunter One,REG111\nTEST_IMPORT_002,Test Hunter Two,REG222"
    file_obj = io.BytesIO(csv_content.encode('utf-8'))
    
    files = {
        'file': ('test_hunters.csv', file_obj, 'text/csv')
    }
    
    print("📤 Uploading test CSV...")
    response = session.post(f'{BASE_URL}/api/admin/import-hunters', files=files)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"✅ Import successful: {data.get('message')}")
            return True
        else:
            print(f"❌ Import failed with error: {data.get('error')}")
            return False
    else:
        print(f"❌ Server error: {response.status_code}")
        print(response.text)
        return False

def verify_hunters(session):
    print("🔍 Verifying imported hunters...")
    response = session.get(f'{BASE_URL}/api/admin/hunters')
    if response.status_code == 200:
        data = response.json()
        hunters = data.get('hunters', [])
        
        found_one = False
        found_two = False
        
        for h in hunters:
            if h['id'] == 'TEST_IMPORT_001':
                if h['name'] == 'Test Hunter One' and h['password'] == 'REG111':
                    print("✅ Found Hunter One with correct details")
                    found_one = True
            if h['id'] == 'TEST_IMPORT_002':
                if h['name'] == 'Test Hunter Two' and h['password'] == 'REG222':
                    print("✅ Found Hunter Two with correct details")
                    found_two = True
                    
        if found_one and found_two:
            print("✅ Verification Complete: All test hunters found.")
            return True
        else:
            print("❌ Verification Failed: Some hunters missing.")
            return False
            
    else:
        print(f"❌ Failed to fetch hunters: {response.status_code}")
        return False

def cleanup(session):
    print("🧹 Cleaning up test data...")
    session.delete(f'{BASE_URL}/api/admin/hunters/TEST_IMPORT_001')
    session.delete(f'{BASE_URL}/api/admin/hunters/TEST_IMPORT_002')
    print("✅ Cleanup done.")

if __name__ == "__main__":
    s = login()
    if s:
        if test_import(s):
            if verify_hunters(s):
                cleanup(s)
            else:
                print("⚠️ Verification failed, skipping cleanup (inspect manually)")
        else:
            print("⚠️ Import failed")
