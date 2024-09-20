import unittest
from app import app

class TestHomeRoute(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_get(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Select a specialization', result.data)

if __name__ == '__main__':
    unittest.main()
# Fix home route test issue
