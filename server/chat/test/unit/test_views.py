from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch
from chat.models import Room, Message

User = get_user_model()


class OwnerRoomListCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='room_owner',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.other_user = User.objects.create_user(
            username='other_user',
            email='other@example.com',
            password='TestPass123!'
        )
        
        self.url = reverse('create-room')
        
        # Create JWT token for owner
        refresh = RefreshToken.for_user(self.owner)
        self.owner_token = str(refresh.access_token)
        
        # Create some rooms for testing
        self.room1 = Room.objects.create(
            owner=self.owner,
            name='Owner Room 1'
        )
        self.room2 = Room.objects.create(
            owner=self.owner,
            name='Owner Room 2'
        )
        # Room owned by other user (shouldn't appear in owner's list)
        Room.objects.create(
            owner=self.other_user,
            name='Other User Room'
        )

    def test_authenticated_room_list(self):
        """Test retrieving room list with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        room_names = [room['name'] for room in response.data['results']]
        self.assertIn('Owner Room 1', room_names)
        self.assertIn('Owner Room 2', room_names)
        self.assertNotIn('Other User Room', room_names)

    def test_unauthenticated_room_list(self):
        """Test retrieving room list without authentication"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_room_success(self):
        """Test creating room with valid data"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        
        room_data = {
            'name': 'New Test Room',
            'access': Room.PUBLIC,
            'limit': 15
        }
        
        response = self.client.post(self.url, room_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Test Room')
        self.assertEqual(response.data['access'], Room.PUBLIC)
        self.assertEqual(response.data['limit'], 15)
        
        # Verify room was created in database
        room = Room.objects.get(name='New Test Room')
        self.assertEqual(room.owner, self.owner)

    def test_create_room_invalid_data(self):
        """Test creating room with invalid data"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        
        invalid_data = {
            'name': 'AB',  # Too short
            'limit': 100   # Too high
        }
        
        response = self.client.post(self.url, invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('limit', response.data)

    def test_participant_count_annotation(self):
        """Test participant_count is properly annotated"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        
        # Add participants to room1
        self.room1.participants.add(self.other_user)
        
        response = self.client.get(self.url)
        
        room1_data = next(room for room in response.data['results'] if room['name'] == 'Owner Room 1')
        self.assertEqual(room1_data['participant_count'], 2)  # owner + other_user


class OwnerSingleRoomAPIViewTest(APITestCase):
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
            name='Test Room'
        )
        self.room.participants.add(self.participant)
        
        self.url = reverse('create-room', kwargs={'id': self.room.id})
        
        refresh = RefreshToken.for_user(self.owner)
        self.owner_token = str(refresh.access_token)

    def test_retrieve_own_room(self):
        """Test owner can retrieve their room details"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Room')
        self.assertIn('participants', response.data)
        self.assertEqual(len(response.data['participants']), 2)

    def test_update_own_room(self):
        """Test owner can update their room"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        
        update_data = {
            'name': 'Updated Room Name',
            'limit': 20
        }
        
        response = self.client.patch(self.url, update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Room Name')
        self.assertEqual(response.data['limit'], 20)

    def test_delete_own_room(self):
        """Test owner can delete their room"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Room.objects.filter(id=self.room.id).exists())

    def test_non_owner_access_denied(self):
        """Test non-owner cannot access room details"""
        refresh = RefreshToken.for_user(self.participant)
        participant_token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {participant_token}')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PublicAllRoomListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='user@example.com',
            password='TestPass123!'
        )
        
        # Create rooms with different statuses
        self.active_room = Room.objects.create(
            owner=self.user,
            name='Active Room',
            status=Room.ACTIVE
        )
        
        self.inactive_room = Room.objects.create(
            owner=self.user,
            name='Inactive Room',
            status=Room.INACTIVE
        )
        
        self.url = reverse('all-room')
        
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_list_active_rooms_only(self):
        """Test only active rooms are returned"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Active Room')

    def test_search_functionality(self):
        """Test search functionality"""
        Room.objects.create(
            owner=self.user,
            name='Searchable Room',
            status=Room.ACTIVE
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.url, {'search': 'Searchable'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Searchable Room')

    def test_is_participant_annotation(self):
        """Test is_participant field is properly annotated"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_participant', response.data['results'][0])


class PublicRoomDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='user@example.com',
            password='TestPass123!'
        )
        
        self.room = Room.objects.create(
            owner=self.user,
            name='Public Room',
            status=Room.ACTIVE
        )
        
        self.inactive_room = Room.objects.create(
            owner=self.user,
            name='Inactive Room',
            status=Room.INACTIVE
        )
        
        self.url = reverse('single-room', kwargs={'pk': self.room.pk})
        self.inactive_url = reverse('single-room', kwargs={'pk': self.inactive_room.pk})
        
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_retrieve_active_room(self):
        """Test retrieving active room details"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Public Room')
        self.assertIn('owner', response.data)

    def test_inactive_room_not_found(self):
        """Test inactive room returns 404"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.inactive_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RoomMessageListViewTest(APITestCase):
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
        self.non_participant = User.objects.create_user(
            username='non_participant',
            email='nonparticipant@example.com',
            password='TestPass123!'
        )
        
        self.room = Room.objects.create(
            owner=self.owner,
            name='Test Room'
        )
        self.room.participants.add(self.participant)
        
        # Create messages
        self.message1 = Message.objects.create(
            sender=self.owner,
            room=self.room,
            content='First message'
        )
        self.message2 = Message.objects.create(
            sender=self.participant,
            room=self.room,
            content='Second message'
        )
        
        self.url = reverse('room-messages', kwargs={'room_id': self.room.id})
        
        # Create tokens
        owner_refresh = RefreshToken.for_user(self.owner)
        self.owner_token = str(owner_refresh.access_token)
        
        participant_refresh = RefreshToken.for_user(self.participant)
        self.participant_token = str(participant_refresh.access_token)
        
        non_participant_refresh = RefreshToken.for_user(self.non_participant)
        self.non_participant_token = str(non_participant_refresh.access_token)

    def test_owner_access_messages(self):
        """Test room owner can access messages"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check message order (should be reversed: oldest to newest)
        messages = response.data['results']
        self.assertEqual(messages[0]['content'], 'First message')
        self.assertEqual(messages[1]['content'], 'Second message')

    def test_participant_access_messages(self):
        """Test room participant can access messages"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.participant_token}')
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_non_participant_denied_access(self):
        """Test non-participant cannot access messages"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.non_participant_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_msg_type_annotation(self):
        """Test msg_type is properly annotated based on sender"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        response = self.client.get(self.url)
        
        messages = response.data['results']
        
        # Owner's message should be 'sent'
        owner_message = next(msg for msg in messages if msg['sender'] == self.owner.id)
        self.assertEqual(owner_message['msg_type'], 'sent')
        
        # Participant's message should be 'received' for owner
        participant_message = next(msg for msg in messages if msg['sender'] == self.participant.id)
        self.assertEqual(participant_message['msg_type'], 'received')

    def test_nonexistent_room(self):
        """Test accessing messages for nonexistent room"""
        url = reverse('room-messages', kwargs={'room_id': 99999})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sender_username_annotation(self):
        """Test sender_username is properly annotated"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.owner_token}')
        response = self.client.get(self.url)
        
        messages = response.data['results']
        
        owner_message = next(msg for msg in messages if msg['sender'] == self.owner.id)
        self.assertEqual(owner_message['sender_username'], 'room_owner')
        
        participant_message = next(msg for msg in messages if msg['sender'] == self.participant.id)
        self.assertEqual(participant_message['sender_username'], 'participant')
