from django.test import TestCase
from django.contrib.auth import get_user_model
from users.services import create_user

User = get_user_model()


class CreateUserServiceTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }

    def test_create_user_service(self):
        """Test create_user service function"""
        user = create_user(self.user_data)
        
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('TestPass123!'))
        self.assertTrue(User.objects.filter(username='test_user').exists())

    def test_password_hashing(self):
        """Test that password is properly hashed"""
        user = create_user(self.user_data)
        
        # Password should be hashed, not stored in plain text
        self.assertNotEqual(user.password, 'TestPass123!')
        self.assertTrue(user.check_password('TestPass123!'))
