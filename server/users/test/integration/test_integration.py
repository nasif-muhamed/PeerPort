from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserRegistrationIntegrationTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register-user')
        self.valid_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }

    def test_successful_user_registration(self):
        """Test complete user registration flow"""
        response = self.client.post(self.register_url, self.valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully')
        
        # Verify user was created in database
        self.assertTrue(User.objects.filter(username='test_user').exists())
        user = User.objects.get(username='test_user')
        self.assertEqual(user.email, 'test@example.com')

    def test_registration_with_invalid_data(self):
        """Test registration with invalid data"""
        invalid_data = self.valid_data.copy()
        invalid_data['password'] = 'weak'
        
        response = self.client.post(self.register_url, invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        
        # Verify user was not created
        self.assertFalse(User.objects.filter(username='test_user').exists())

    def test_duplicate_registration(self):
        """Test registration with duplicate username/email"""
        # Create first user
        self.client.post(self.register_url, self.valid_data)
        
        # Try to create duplicate user
        duplicate_data = self.valid_data.copy()
        response = self.client.post(self.register_url, duplicate_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username='test_user').count(), 1)


class UserAuthenticationIntegrationTest(APITestCase):
    def setUp(self):
        self.login_url = reverse('user-login')
        self.logout_url = reverse('logout-user')
        self.refresh_url = reverse('refresh-token')
        self.profile_url = reverse('user-profile')
        
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='TestPass123!'
        )

    def test_successful_login(self):
        """Test successful login flow"""
        login_data = {
            'username': 'test_user',
            'password': 'TestPass123!'
        }
        
        response = self.client.post(self.login_url, login_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'test_user')

    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials"""
        invalid_login_data = {
            'username': 'test_user',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, invalid_login_data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        """Test token refresh functionality"""
        # Get initial tokens
        login_data = {'username': 'test_user', 'password': 'TestPass123!'}
        login_response = self.client.post(self.login_url, login_data)
        refresh_token = login_response.data['refresh']
        
        # Refresh token
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(self.refresh_url, refresh_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_successful_logout(self):
        """Test successful logout flow"""
        # Login first
        login_data = {'username': 'test_user', 'password': 'TestPass123!'}
        login_response = self.client.post(self.login_url, login_data)
        refresh_token = login_response.data['refresh']
        access_token = login_response.data['access']
        
        # Set authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Logout
        logout_data = {'refresh': refresh_token}
        response = self.client.post(self.logout_url, logout_data)
        
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data['message'], 'Logout successful')

    def test_logout_with_invalid_token(self):
        """Test logout with invalid refresh token"""
        # Get access token first
        login_data = {'username': 'test_user', 'password': 'TestPass123!'}
        login_response = self.client.post(self.login_url, login_data)
        access_token = login_response.data['access']
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Try logout with invalid token
        logout_data = {'refresh': 'invalid_token'}
        response = self.client.post(self.logout_url, logout_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid token')


class UserProfileIntegrationTest(APITestCase):
    def setUp(self):
        self.profile_url = reverse('user-profile')
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='TestPass123!'
        )
        # Create and set JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_authenticated_profile_access(self):
        """Test accessing profile with valid token"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'test_user')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertNotIn('password', response.data)

    def test_unauthenticated_profile_access(self):
        """Test accessing profile without token"""
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_access_with_invalid_token(self):
        """Test accessing profile with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CompleteUserFlowIntegrationTest(APITestCase):
    """Test complete user workflow from registration to profile access"""
    
    def test_complete_user_workflow(self):
        """Test complete user flow: register -> login -> access profile -> logout"""
        # Step 1: Register
        register_data = {
            'username': 'workflow_user',
            'email': 'workflow@example.com',
            'password': 'WorkflowPass123!'
        }
        register_response = self.client.post(reverse('register-user'), register_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        
        # Step 2: Login
        login_data = {
            'username': 'workflow_user',
            'password': 'WorkflowPass123!'
        }
        login_response = self.client.post(reverse('user-login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']
        
        # Step 3: Access profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_response = self.client.get(reverse('user-profile'))
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['username'], 'workflow_user')
        
        # Step 4: Logout
        logout_data = {'refresh': refresh_token}
        logout_response = self.client.post(reverse('logout-user'), logout_data)
        self.assertEqual(logout_response.status_code, status.HTTP_205_RESET_CONTENT)
        
        # Step 5: Verify token is blacklisted (try to refresh)
        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(reverse('refresh-token'), refresh_data)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
