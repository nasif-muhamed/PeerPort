from django.test import TestCase
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, MiniUserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }

    def test_valid_user_serialization(self):
        """Test serializing a valid user"""
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_user_creation(self):
        """Test creating user through serializer"""
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('TestPass123!'))

    def test_password_write_only(self):
        """Test that password is write-only"""
        user = User.objects.create_user(**self.valid_data)
        serializer = UserSerializer(user)
        
        self.assertNotIn('password', serializer.data)
        self.assertIn('id', serializer.data)
        self.assertIn('username', serializer.data)
        self.assertIn('email', serializer.data)

    def test_invalid_username_validation(self):
        """Test username validation in serializer"""
        invalid_data = self.valid_data.copy()
        invalid_data['username'] = 'ab'  # Too short
        
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_invalid_email_validation(self):
        """Test email validation in serializer"""
        # Create existing user first
        User.objects.create_user(**self.valid_data)
        
        # Try to create another user with same email
        duplicate_data = self.valid_data.copy()
        duplicate_data['username'] = 'different_user'
        
        serializer = UserSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_invalid_password_validation(self):
        """Test password validation in serializer"""
        invalid_data = self.valid_data.copy()
        invalid_data['password'] = 'weak'  # Too weak
        
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)


class MiniUserSerializerTest(TestCase):
    def test_mini_user_serialization(self):
        """Test MiniUserSerializer contains only id and username"""
        user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='TestPass123!'
        )
        
        serializer = MiniUserSerializer(user)
        expected_fields = {'id', 'username'}
        
        self.assertEqual(set(serializer.data.keys()), expected_fields)
        self.assertEqual(serializer.data['username'], 'test_user')


class CustomTokenObtainPairSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='TestPass123!'
        )

    def test_custom_token_serializer_adds_user_data(self):
        """Test that custom token serializer includes user data"""
        data = {
            'username': 'test_user',
            'password': 'TestPass123!'
        }

        serializer = CustomTokenObtainPairSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        validated_data = serializer.validated_data

        self.assertIn('user', validated_data)
        self.assertEqual(validated_data['user']['id'], self.user.id)
        self.assertEqual(validated_data['user']['username'], 'test_user')
        self.assertIn('access', validated_data)
        self.assertIn('refresh', validated_data)
