from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch

User = get_user_model()


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('register-user')
        self.valid_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }

    def test_successful_registration(self):
        """Test successful user registration"""
        response = self.client.post(self.url, self.valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully')

    def test_registration_with_invalid_data(self):
        """Test registration with invalid data"""
        invalid_data = self.valid_data.copy()
        invalid_data['username'] = 'ab'  # Too short
        
        response = self.client.post(self.url, invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    @patch('users.views.logger')
    def test_logging_on_registration(self, mock_logger):
        """Test that registration attempt is logged"""
        self.client.post(self.url, self.valid_data)
        mock_logger.debug.assert_called_once()


class LoginViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('user-login')
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='TestPass123!'
        )

    def test_successful_login(self):
        """Test successful login"""
        login_data = {
            'username': 'test_user',
            'password': 'TestPass123!'
        }
        
        response = self.client.post(self.url, login_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'username': 'test_user',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.url, login_data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('user-profile')
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='TestPass123!'
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_authenticated_profile_retrieval(self):
        """Test retrieving profile with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'test_user')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_unauthenticated_profile_access(self):
        """Test accessing profile without authentication"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('logout-user')
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='TestPass123!'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)

    def test_successful_logout(self):
        """Test successful logout"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        logout_data = {'refresh': self.refresh_token}
        response = self.client.post(self.url, logout_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful')

    def test_logout_without_authentication(self):
        """Test logout without authentication"""
        logout_data = {'refresh': self.refresh_token}
        response = self.client.post(self.url, logout_data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_with_invalid_token(self):
        """Test logout with invalid refresh token"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        logout_data = {'refresh': 'invalid_token'}
        response = self.client.post(self.url, logout_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token')

    def test_logout_without_refresh_token(self):
        """Test logout without providing refresh token"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        response = self.client.post(self.url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
