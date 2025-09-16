from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from chat.models import Room, Message
import json

User = get_user_model()


class CrossComponentIntegrationTest(APITestCase):
    """Test integration between different components"""
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.participant = User.objects.create_user(
            username='participant',
            email='participant@example.com',
            password='TestPass123!'
        )
        
        refresh = RefreshToken.for_user(self.owner)
        self.access_token = str(refresh.access_token)

    def test_room_creation_to_messaging_workflow(self):
        """Test complete workflow from room creation to messaging"""
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Step 1: Create room
        room_data = {
            'name': 'Cross Component Room',
            'access': Room.PUBLIC,
            'limit': 10
        }
        
        create_response = self.client.post(reverse('create-room'), room_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        room_id = create_response.data['id']
        
        # Step 2: Add participant to room
        room = Room.objects.get(id=room_id)
        room.participants.add(self.participant)
        
        # Step 3: Create message
        Message.objects.create(
            sender=self.owner,
            room=room,
            content='Welcome to the room!'
        )
        
        # Step 4: Retrieve messages
        messages_url = reverse('room-messages', kwargs={'room_id': room_id})
        messages_response = self.client.get(messages_url)
        
        self.assertEqual(messages_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(messages_response.data['results']), 1)
        self.assertEqual(messages_response.data['results'][0]['content'], 'Welcome to the room!')
        
        # Step 5: Verify room shows last message
        room_list_response = self.client.get(reverse('create-room'))
        room_data = room_list_response.data['results'][0]
        
        self.assertIsNotNone(room_data['last_message'])
        self.assertEqual(room_data['last_message']['content'], 'Welcome to the room!')

    def test_room_update_affects_all_views(self):
        """Test that room updates are reflected across all views"""
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Create room
        room = Room.objects.create(
            owner=self.owner,
            name='Update Test Room'
        )
        
        # Update room through owner API
        detail_url = reverse('create-room', kwargs={'id': room.id})
        update_data = {'name': 'Updated Room Name'}
        
        update_response = self.client.patch(detail_url, update_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
        # Verify update appears in owner list
        list_response = self.client.get(reverse('create-room'))
        room_names = [r['name'] for r in list_response.data['results']]
        self.assertIn('Updated Room Name', room_names)
        
        # Verify update appears in public list
        public_response = self.client.get(reverse('all-room'))
        public_names = [r['name'] for r in public_response.data['results']]
        self.assertIn('Updated Room Name', public_names)
        
        # Verify update appears in single room view
        single_response = self.client.get(reverse('single-room', kwargs={'pk': room.pk}))
        self.assertEqual(single_response.data['name'], 'Updated Room Name')
