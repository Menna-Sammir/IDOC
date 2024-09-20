import unittest
from app import app

class TestSendEmail(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_send_email(self):
        with self.app:
            data = {
                'email_address': 'test@example.com',
                'subject': 'Test Email',
                'message': 'This is a test email'
            }
            result = self.app.post('/email', data=data)
            self.assertEqual(result.status_code, 302)
            self.assertIn(b'email sent successfully', result.data)

if __name__ == '__main__':
    unittest.main()

# Fix email sending test issue

# Improve email test error handling

# Add more assertions for email sending

# Refactor email sending test function

# Improve test coverage for email sending
