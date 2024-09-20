import unittest
from app import app
from flask import session

class TestSendEmail(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False  

    def test_send_email(self):
        with self.app:
            data = {
                'name': 'Test User',  
                'email_address': 'test@example.com',
                'subject': 'Test Email',
                'message': 'This is a test email'
            }

            result = self.app.post('/email', data=data, content_type='application/x-www-form-urlencoded', follow_redirects=True)

            self.assertEqual(result.status_code, 200)

            self.assertIn(b'email sent successfully', result.data)

if __name__ == '__main__':
    unittest.main()
