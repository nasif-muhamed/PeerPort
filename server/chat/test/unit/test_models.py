from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from chat.models import Room, Message

User = get_user_model()


class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username="owner_user",
            email="owner@example.com",
            password="TestPass123!",
        )
        cls.user2 = User.objects.create_user(
            username="participant_user",
            email="participant@example.com",
            password="TestPass123!",
        )
        cls.base_room = Room.objects.create(
            owner=cls.user1,
            name="Base Room",
            access=Room.PUBLIC,
            status=Room.ACTIVE,
            limit=10,
        )

    def test_create_room(self):
        """Test creating a room with valid data"""
        self.assertEqual(self.base_room.name, "Base Room")
        self.assertEqual(self.base_room.owner, self.user1)
        self.assertEqual(self.base_room.access, Room.PUBLIC)
        self.assertEqual(self.base_room.status, Room.ACTIVE)
        self.assertEqual(self.base_room.limit, 10)
        self.assertTrue(self.base_room.participants.filter(id=self.user1.id).exists())

    def test_room_string_representation(self):
        """Test the string representation of room model"""
        self.assertEqual(str(self.base_room), "Base Room (Public)")

    def test_unique_room_name_constraint(self):
        """Test that room names must be unique"""
        with self.assertRaises(IntegrityError):
            Room.objects.create(owner=self.user2, name="Base Room")

    def test_can_add_participant_with_space(self):
        """Test can_add_participant when room has space"""
        self.assertTrue(self.base_room.can_add_participant())

    def test_can_add_participant_when_full(self):
        """Test can_add_participant when room is full"""
        room = Room.objects.create(owner=self.user1, name="Full Room", limit=1)
        self.assertFalse(room.can_add_participant())  # owner is already a participant

    def test_owner_automatically_added_as_participant(self):
        """Test that owner is automatically added as participant"""
        self.assertTrue(self.base_room.participants.filter(id=self.user1.id).exists())

    def test_room_ordering(self):
        """Test that rooms are ordered by created_at descending"""
        room2 = Room.objects.create(owner=self.user1, name="Second Room")
        rooms = Room.objects.all()
        self.assertEqual(rooms.first(), room2)
        self.assertEqual(rooms.last(), self.base_room)

    def test_room_default_values(self):
        """Test default values for room fields"""
        self.assertEqual(self.base_room.access, Room.PUBLIC)
        self.assertEqual(self.base_room.status, Room.ACTIVE)
        self.assertEqual(self.base_room.limit, 10)


class MessageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username="sender_user",
            email="sender@example.com",
            password="TestPass123!",
        )
        cls.room = Room.objects.create(owner=cls.user1, name="Message Room")
        cls.message = Message.objects.create(
            sender=cls.user1, room=cls.room, content="Hello, World!"
        )

    def test_create_message(self):
        """Test creating a message with valid data"""
        self.assertEqual(self.message.sender, self.user1)
        self.assertEqual(self.message.room, self.room)
        self.assertEqual(self.message.content, "Hello, World!")
        self.assertEqual(self.message.type, "text")

    def test_message_string_representation(self):
        """Test the string representation of message model"""
        self.assertEqual(str(self.message), f"{self.user1.username} in {self.room.name}")

    def test_message_updates_room_last_message(self):
        """Test that saving a message updates room's last_message"""
        message = Message.objects.create(sender=self.user1, room=self.room, content="Latest message")
        self.room.refresh_from_db()
        self.assertEqual(self.room.last_message, message)

    def test_message_ordering(self):
        """Test that messages are ordered by timestamp descending"""
        msg2 = Message.objects.create(sender=self.user1, room=self.room, content="Second message")
        messages = Message.objects.all()
        self.assertEqual(messages.first(), msg2)
        self.assertEqual(messages.last(), self.message)

    def test_message_default_type(self):
        """Test default message type is text"""
        self.assertEqual(self.message.type, "text")
