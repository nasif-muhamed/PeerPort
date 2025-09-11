from django.test import TestCase
from django.contrib.auth import get_user_model
import asyncio
from chat.models import Room, Message
from chat.services import (
    permission_to_join_room, participant_leave_room, 
    remove_participant, save_message
)

User = get_user_model()


class ServicesTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='room_owner',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.user1 = User.objects.create_user(
            username='participant1',
            email='user1@example.com',
            password='TestPass123!'
        )
        self.user2 = User.objects.create_user(
            username='participant2',
            email='user2@example.com',
            password='TestPass123!'
        )
        
        self.public_room = Room.objects.create(
            owner=self.owner,
            name='Public Room',
            access=Room.PUBLIC,
            limit=3
        )
        
        self.private_room = Room.objects.create(
            owner=self.owner,
            name='Private Room',
            access=Room.PRIVATE,
            limit=3
        )
        
        self.inactive_room = Room.objects.create(
            owner=self.owner,
            name='Inactive Room',
            status=Room.INACTIVE
        )

    def test_permission_to_join_public_room_success(self):
        """Test user can join public room with space"""
        allowed, is_new = permission_to_join_room.func(self.user1, self.public_room.id)
        self.assertTrue(allowed)
        self.assertTrue(is_new)
        
        # Verify user was added to participants
        self.public_room.refresh_from_db()
        self.assertTrue(self.public_room.participants.filter(id=self.user1.id).exists())
        

    def test_permission_to_join_existing_participant(self):
        """Test existing participant can rejoin"""
        self.public_room.participants.add(self.user1)
        
        allowed, is_new = permission_to_join_room.func(self.user1, self.public_room.id)
        self.assertTrue(allowed)
        self.assertFalse(is_new)
        

    def test_permission_to_join_full_room(self):
        """Test user cannot join full room"""
        # Fill the room to capacity
        self.public_room.participants.add(self.user1, self.user2)
        
        user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='TestPass123!'
        )
        
        allowed, is_new =  permission_to_join_room.func(user3, self.public_room.id)
        self.assertFalse(allowed)
        self.assertFalse(is_new)

    def test_permission_to_join_private_room(self):
        """Test user cannot join private room"""
        allowed, is_new = permission_to_join_room.func(self.user1, self.private_room.id)
        self.assertFalse(allowed)
        self.assertFalse(is_new)
        
    def test_permission_to_join_inactive_room(self):
        """Test user cannot join inactive room"""
        allowed, is_new = permission_to_join_room.func(self.user1, self.inactive_room.id)
        self.assertFalse(allowed)
        self.assertFalse(is_new)
        
    def test_permission_to_join_nonexistent_room(self):
        """Test joining nonexistent room fails"""
        allowed, is_new = permission_to_join_room.func(self.user1, 99999)
        self.assertFalse(allowed)
        self.assertFalse(is_new)

    def test_participant_leave_room_success(self):
        """Test participant can leave room"""
        self.public_room.participants.add(self.user1)
        success = participant_leave_room.func(self.user1, self.public_room.id)
        self.assertTrue(success)
        
        # Verify user was removed from participants
        self.public_room.refresh_from_db()
        self.assertFalse(self.public_room.participants.filter(id=self.user1.id).exists())
        

    def test_owner_cannot_leave_room(self):
        """Test room owner cannot leave room"""
        success = participant_leave_room.func(self.owner, self.public_room.id)
        self.assertFalse(success)
        
        # Verify owner is still a participant
        self.public_room.refresh_from_db()
        self.assertTrue(self.public_room.participants.filter(id=self.owner.id).exists())
        

    def test_participant_leave_nonparticipant(self):
        """Test non-participant cannot leave room"""
        success = participant_leave_room.func(self.user1, self.public_room.id)
        self.assertFalse(success)
        

    def test_remove_participant_by_owner(self):
        """Test owner can remove participant"""
        self.public_room.participants.add(self.user1)
        success = remove_participant.func(self.owner, self.public_room.id, self.user1.id)
        self.assertTrue(success)
        
        # Verify user was removed
        self.public_room.refresh_from_db()
        self.assertFalse(self.public_room.participants.filter(id=self.user1.id).exists())
        
    def test_remove_participant_by_non_owner(self):
        """Test non-owner cannot remove participant"""
        self.public_room.participants.add(self.user1, self.user2)
        success = remove_participant.func(self.user1, self.public_room.id, self.user2.id)
        self.assertFalse(success)
        
        # Verify user was not removed
        self.public_room.refresh_from_db()
        self.assertTrue(self.public_room.participants.filter(id=self.user2.id).exists())


    def test_save_message_success(self):
        """Test saving message by participant"""
        self.public_room.participants.add(self.user1)
        message_data = save_message.func(self.user1, self.public_room.id, 'Test message', 'text')
        
        self.assertEqual(message_data['content'], 'Test message')
        self.assertEqual(message_data['type'], 'text')
        self.assertEqual(message_data['sender_username'], 'participant1')
            
        # Verify message was saved to database
        message = Message.objects.get(content='Test message')
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.room, self.public_room)
        
    def test_save_message_by_non_participant(self):
        """Test saving message by non-participant fails"""
        with self.assertRaises(Exception):  # Should raise PermissionDenied
            save_message.func(self.user1, self.public_room.id, 'Test message', 'text')
        
    def test_save_message_inactive_room(self):
        """Test saving message to inactive room fails"""
        with self.assertRaises(Exception):  # Should raise PermissionDenied
            save_message.func(self.owner, self.inactive_room.id, 'Test message', 'text')
        

    def test_save_message_updates_last_message(self):
        """Test saving message updates room's last_message"""
        self.public_room.participants.add(self.user1)
        save_message.func(self.user1, self.public_room.id, 'Latest message', 'text')
        
        # Verify room's last_message was updated
        self.public_room.refresh_from_db()
        self.assertEqual(self.public_room.last_message.content, 'Latest message')
        