import unittest
from unittest.mock import patch
from app import create_app

class AuthTestCase(unittest.TestCase):
    """Test user authentication routes"""

    def setUp(self):
        """Set up test client"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

    @patch('app.routes.User.query.filter_by')
    @patch('app.routes.db.session.add')
    @patch('app.routes.db.session.commit')
    def test_signup(self, mock_commit, mock_add, mock_filter_by):
        """Test user registration"""
        mock_filter_by.return_value.first.return_value = None  # No existing user
        
        response = self.client.post('/users/signup', json={
            'username': 'testuser',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

        # Check that user was added and committed to DB
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

    @patch('app.routes.User.query.filter_by')
    def test_login(self, mock_filter_by):
        """Test user login"""
        mock_user = unittest.mock.Mock()
        mock_user.check_password.return_value = True  # Simulate correct password
        mock_filter_by.return_value.first.return_value = mock_user

        response = self.client.post('/users/login', json={
            'username': 'testuser',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

        # Ensure the user was queried
        mock_filter_by.assert_called_once_with(username='testuser')

if __name__ == '__main__':
    unittest.main()