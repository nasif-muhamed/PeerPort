from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from chat.models import Room, Message
import json

User = get_user_model()


class RoomManagementIntegrationTest(APITestCase):
    """Test complete room management workflow"""
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='room_owner',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.participant = User.objects.create_user(
            username='participant',
            email='participant@example.com',
            password='TestPass123!'
        )
        
        # URLs
        self.create_room_url = reverse('create-room')
        self.all_rooms_url = reverse('all-room')
        
        # Tokens
        owner_refresh = RefreshToken.for_user(self.owner)
        self.owner_token = str(owner_refresh.access_token)
        
        participant_refresh = RefreshToken.for_user(self.participant)
        self.participant_token = str(participant_refresh.access_token)

    def test_complete_room_lifecycle(self):
        """Test complete room lifecycle: create -> list -> detail -> update -> delete"""
        
        # Step 1: Create room
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        room_data = {
            'name': 'Integration Test Room',
            'access': Room.PUBLIC,
            'limit': 5
        }
        
        create_response = self.client.post(self.create_room_url, room_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        room_id = create_response.data['id']
        
        # Step 2: List rooms (should include created room)
        list_response = self.client.get(self.create_room_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        room_names = [room['name'] for room in list_response.data['results']]
        self.assertIn('Integration Test Room', room_names)
        
        # Step 3: Get room detail
        detail_url = reverse('create-room', kwargs={'id': room_id})
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['name'], 'Integration Test Room')
        
        # Step 4: Update room
        update_data = {'name': 'Updated Integration Room', 'limit': 10}
        update_response = self.client.patch(detail_url, update_data)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], 'Updated Integration Room')
        
        # Step 5: Delete room
        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify room is deleted
        self.assertFalse(Room.objects.filter(id=room_id).exists())

    def test_room_visibility_workflow(self):
        """Test room visibility from creation to public listing"""
        
        # Owner creates room
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        room_data = {
            'name': 'Public Visibility Room',
            'access': Room.PUBLIC,
            'status': Room.ACTIVE
        }
        
        create_response = self.client.post(self.create_room_url, room_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        
        # Switch to participant user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.participant_token}')
        
        # Participant should see room in public listing
        public_response = self.client.get(self.all_rooms_url)
        self.assertEqual(public_response.status_code, status.HTTP_200_OK)
        room_names = [room['name'] for room in public_response.data['results']]
        self.assertIn('Public Visibility Room', room_names)
        
        # Check is_participant flag (should be False initially)
        room_data = next(room for room in public_response.data['results'] 
                        if room['name'] == 'Public Visibility Room')
        self.assertFalse(room_data['is_participant'])


class MessageIntegrationTest(APITestCase):
    """Test complete messaging workflow"""
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='room_owner',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.participant = User.objects.create_user(
            username='participant',
            email='participant@example.com',
            password='TestPass123!'
        )
        
        self.room = Room.objects.create(
            owner=self.owner,
            name='Message Test Room'
        )
        self.room.participants.add(self.participant)
        
        self.messages_url = reverse('room-messages', kwargs={'room_id': self.room.id})
        
        # Tokens
        owner_refresh = RefreshToken.for_user(self.owner)
        self.owner_token = str(owner_refresh.access_token)
        
        participant_refresh = RefreshToken.for_user(self.participant)
        self.participant_token = str(participant_refresh.access_token)

    def test_messaging_workflow(self):
        """Test complete messaging workflow: send -> receive -> list"""
        
        # Create messages from both users
        Message.objects.create(
            sender=self.owner,
            room=self.room,
            content='Hello from owner'
        )
        
        Message.objects.create(
            sender=self.participant,
            room=self.room,
            content='Hello from participant'
        )
        
        # Owner retrieves messages
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        owner_response = self.client.get(self.messages_url)
        
        self.assertEqual(owner_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(owner_response.data['results']), 2)
        
        # Check message types from owner's perspective
        messages = owner_response.data['results']
        owner_message = next(msg for msg in messages if msg['sender'] == self.owner.id)
        participant_message = next(msg for msg in messages if msg['sender'] == self.participant.id)
        
        self.assertEqual(owner_message['msg_type'], 'sent')
        self.assertEqual(participant_message['msg_type'], 'received')
        
        # Participant retrieves messages
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.participant_token}')
        participant_response = self.client.get(self.messages_url)
        
        self.assertEqual(participant_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(participant_response.data['results']), 2)
        
        # Check message types from participant's perspective
        p_messages = participant_response.data['results']
        p_owner_message = next(msg for msg in p_messages if msg['sender'] == self.owner.id)
        p_participant_message = next(msg for msg in p_messages if msg['sender'] == self.participant.id)
        
        self.assertEqual(p_owner_message['msg_type'], 'received')
        self.assertEqual(p_participant_message['msg_type'], 'sent')

    def test_last_message_update_workflow(self):
        """Test that room's last_message updates when messages are created"""
        
        # Initially no last message
        self.assertIsNone(self.room.last_message)
        
        # Create first message
        message1 = Message.objects.create(
            sender=self.owner,
            room=self.room,
            content='First message'
        )
        
        self.room.refresh_from_db()
        self.assertEqual(self.room.last_message, message1)
        
        # Create second message
        message2 = Message.objects.create(
            sender=self.participant,
            room=self.room,
            content='Second message'
        )
        
        self.room.refresh_from_db()
        self.assertEqual(self.room.last_message, message2)
        
        # Verify last_message appears in room serialization
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        room_url = reverse('create-room')
        response = self.client.get(room_url)
        
        room_data = response.data['results'][0]  # Should be our room
        self.assertIsNotNone(room_data['last_message'])
        self.assertEqual(room_data['last_message']['content'], 'Second message')


class RoomParticipationIntegrationTest(APITestCase):
    """Test room participation workflows"""
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='room_owner',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='TestPass123!'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='TestPass123!'
        )
        
        self.public_room = Room.objects.create(
            owner=self.owner,
            name='Public Participation Room',
            access=Room.PUBLIC,
            limit=3
        )
        
        # Tokens
        owner_refresh = RefreshToken.for_user(self.owner)
        self.owner_token = str(owner_refresh.access_token)

    def test_room_capacity_workflow(self):
        """Test room capacity management workflow"""
        
        # Initially room has owner as participant (count = 1)
        self.assertEqual(self.public_room.participants.count(), 1)
        self.assertTrue(self.public_room.can_add_participant())
        
        # Add participants up to limit
        self.public_room.participants.add(self.user1, self.user2)
        self.public_room.refresh_from_db()
        
        # Room should now be at capacity (3/3)
        self.assertEqual(self.public_room.participants.count(), 3)
        self.assertFalse(self.public_room.can_add_participant())
        
        # Verify participant count in API response
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        room_detail_url = reverse('create-room', kwargs={'id': self.public_room.id})
        response = self.client.get(room_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['participants']), 3)


class SearchAndFilterIntegrationTest(APITestCase):
    """Test search and filtering workflows"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='user@example.com',
            password='TestPass123!'
        )
        
        # Create rooms with different attributes
        Room.objects.create(
            owner=self.user,
            name='Gaming Room',
            status=Room.ACTIVE
        )
        
        Room.objects.create(
            owner=self.user,
            name='Study Group',
            status=Room.ACTIVE
        )
        
        Room.objects.create(
            owner=self.user,
            name='Gaming Lounge',
            status=Room.INACTIVE  # Should not appear in public listings
        )
        
        self.all_rooms_url = reverse('all-room')
        
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_search_workflow(self):
        """Test search functionality workflow"""
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Search for "Gaming" - should find only active gaming rooms
        search_response = self.client.get(self.all_rooms_url, {'search': 'Gaming'})
        
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(search_response.data['results']), 1)
        self.assertEqual(search_response.data['results'][0]['name'], 'Gaming Room')
        
        # Search for "Group" - should find Study Group
        group_response = self.client.get(self.all_rooms_url, {'search': 'Group'})
        
        self.assertEqual(group_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(group_response.data['results']), 1)
        self.assertEqual(group_response.data['results'][0]['name'], 'Study Group')
        
        # Search for non-existent term
        empty_response = self.client.get(self.all_rooms_url, {'search': 'NonExistent'})
        
        self.assertEqual(empty_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(empty_response.data['results']), 0)

    def test_status_filter_workflow(self):
        """Test that only active rooms appear in public listings"""
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Get all public rooms (should only include active ones)
        response = self.client.get(self.all_rooms_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Only active rooms
        
        room_names = [room['name'] for room in response.data['results']]
        self.assertIn('Gaming Room', room_names)
        self.assertIn('Study Group', room_names)
        self.assertNotIn('Gaming Lounge', room_names)  # Inactive room excluded


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
