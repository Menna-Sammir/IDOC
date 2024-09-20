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

# Improve home route test error handling

# Add more assertions for home route

# Refactor home route test function

# Improve test coverage for home route

# Adjust mock data for home route test

# Fix typo in specialization variable

# Change response content check in home route test

# Add logging for debugging home route

# Remove unused imports in home route test

# Update test client setup for home route

# Fix HTTP status code check in home route test

# Enhance test reliability for home route

# Improve performance of home route test

# Fix flaky home route test issue

# Modify test for new home route endpoint
