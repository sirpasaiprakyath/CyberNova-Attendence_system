import unittest
from app import app
from flask import session

class SessionTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        self.client = app.test_client()

    def test_session_isolation(self):
        with self.client as c:
            # 1. Login as Admin
            print("\n[TEST] Logging in as Admin...")
            c.post('/login', json={'username': 'admin', 'password': 'hackathon2026', 'role': 'admin'})
            
            # 2. Login as Team
            print("[TEST] Logging in as Team...")
            c.post('/login', json={'username': 'TEAM001', 'password': 'pass001', 'role': 'team'})
            
            # Verify both sessions exist
            with c.session_transaction() as sess:
                self.assertTrue(sess.get('admin'), "Admin key missing!")
                self.assertTrue(sess.get('teamId'), "Team ID missing!")

            # 3. Logout Team ONLY
            print("[TEST] Logging out Team (/logout/team)...")
            c.get('/logout/team')
            
            # Verify Admin is STILL there, but Team is gone
            with c.session_transaction() as sess:
                print(f"[TEST] Session after Team logout: {sess}")
                self.assertTrue(sess.get('admin'), "Admin session should persist after Team logout")
                self.assertFalse(sess.get('teamId'), "Team session should be gone")

            # 4. Access Admin Route (should succeed)
            resp = c.get('/admin')
            self.assertEqual(resp.status_code, 200, "Admin route should be accessible")
            
            # 5. Logout Admin
            print("[TEST] Logging out Admin (/logout/admin)...")
            c.get('/logout/admin')
            
            # Verify empty
            with c.session_transaction() as sess:
                self.assertFalse(sess.get('admin'), "Admin session should be gone")

if __name__ == '__main__':
    unittest.main()
