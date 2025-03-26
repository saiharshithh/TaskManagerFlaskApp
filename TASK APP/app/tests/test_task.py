import unittest
from unittest.mock import patch
from flask_login import FlaskLoginClient
from app import create_app
from app.models import User

class TaskTestCase(unittest.TestCase):
    """Test task-related routes"""

    def setUp(self):
        """Set up test client with login"""
        self.app = create_app('testing')
        self.app.test_client_class = FlaskLoginClient  # Enable login for tests
        self.client = self.app.test_client()
        
        self.user = User(id=1, username='testuser')
        with self.client:
            self.client.post('/users/login', json={
                'username': 'testuser',
                'password': 'password123'
            })

    @patch('app.routes.db.session.add')
    @patch('app.routes.db.session.commit')
    def test_create_task(self, mock_commit, mock_add):
        """Test creating a task"""
        response = self.client.post('/tasks/create', data={
            'title': 'Test Task',
            'description': 'This is a test task.'
        })

        self.assertEqual(response.status_code, 302)  # Redirect to task list
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
    