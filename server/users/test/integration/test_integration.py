from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


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
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        
        # Step 5: Verify token is blacklisted (try to refresh)
        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(reverse('refresh-token'), refresh_data)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
