from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import Case, When, Value, CharField, F, OuterRef, Count, Exists
from rest_framework.exceptions import ValidationError
from chat.models import Room, Message
from chat.serializers import (
    RoomOwnerSerializer, RoomOwnerDetailSerializer, 
    PublicRoomSerializer, MessageSerializer, MiniMessageSerializer
)

User = get_user_model()


class RoomOwnerSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='owner_user',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.valid_data = {
            'name': 'Test Room',
            'access': Room.PUBLIC,
            'status': Room.ACTIVE,
            'limit': 10
        }

    def test_room_creation_with_valid_data(self):
        """Test creating room through serializer"""
        serializer = RoomOwnerSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
        room = serializer.save(owner=self.user)
        self.assertEqual(room.name, 'Test Room')
        self.assertEqual(room.owner, self.user)
        self.assertEqual(room.access, Room.PUBLIC)

    def test_participant_count_read_only(self):
        """Test participant_count is read-only"""
        room = Room.objects.create(owner=self.user, name='Test Room')
        user2 = User.objects.create_user(
            username='participant',
            email='participant@example.com',
            password='TestPass123!'
        )
        room.participants.add(user2)
        annotated_room = Room.objects.filter(owner=self.user).annotate(participant_count=Count("participants")).first()
        serializer = RoomOwnerSerializer(annotated_room)
        self.assertIn('participant_count', serializer.data)
        self.assertEqual(serializer.data['participant_count'], 2)  # owner + participant

    def test_invalid_name_validation(self):
        """Test name validation in serializer"""
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = 'AB'  # Too short
        
        serializer = RoomOwnerSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_last_message_in_serialization(self):
        """Test last_message is included in serialization"""
        room = Room.objects.create(owner=self.user, name='Test Room')
        message = Message.objects.create(
            sender=self.user,
            room=room,
            content='Latest message'
        )
        
        serializer = RoomOwnerSerializer(room)
        self.assertIn('last_message', serializer.data)
        self.assertEqual(serializer.data['last_message']['content'], 'Latest message')


class RoomOwnerDetailSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='owner_user',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.participant = User.objects.create_user(
            username='participant_user',
            email='participant@example.com',
            password='TestPass123!'
        )

    def test_participants_included(self):
        """Test participants are included in detail serializer"""
        room = Room.objects.create(owner=self.user, name='Test Room')
        room.participants.add(self.participant)
        
        serializer = RoomOwnerDetailSerializer(room)
        self.assertIn('participants', serializer.data)
        self.assertEqual(len(serializer.data['participants']), 2)  # owner + participant

    def test_participant_count_excluded(self):
        """Test participant_count is excluded from detail serializer"""
        room = Room.objects.create(owner=self.user, name='Test Room')
        serializer = RoomOwnerDetailSerializer(room)
        self.assertNotIn('participant_count', serializer.data)

    def test_last_message_excluded(self):
        """Test last_message is excluded from detail serializer"""
        room = Room.objects.create(owner=self.user, name='Test Room')
        Message.objects.create(
            sender=self.user,
            room=room,
            content='Test message'
        )
        
        serializer = RoomOwnerDetailSerializer(room)
        self.assertNotIn('last_message', serializer.data)


class PublicRoomSerializerTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner_user',
            email='owner@example.com',
            password='TestPass123!'
        )
        self.user = User.objects.create_user(
            username='regular_user',
            email='user@example.com',
            password='TestPass123!'
        )
        self.room = Room.objects.create(owner=self.owner, name='Public Room')

    def test_owner_included(self):
        """Test owner information is included"""
        serializer = PublicRoomSerializer(self.room)
        
        self.assertIn('owner', serializer.data)
        self.assertEqual(serializer.data['owner']['username'], 'owner_user')

    def test_is_participant_field_and_read_only_fields(self):
        """Test is_participant field functionality"""
        """Test that specified fields are read-only"""

        room = Room.objects.filter(pk=self.room.pk).select_related("owner").annotate(
            participant_count=Count("participants"),
            is_participant=Exists(
                Room.participants.through.objects.filter(
                    room_id=OuterRef("pk"), user_id=self.user.id
                )
            )
        ).first()

        serializer = PublicRoomSerializer(room)
        self.assertIn('is_participant', serializer.data)
        
        read_only_fields = ['id', 'participant_count', 'is_participant', 'last_message', 'created_at', 'updated_at']
        for field in read_only_fields:
            self.assertIn(field, serializer.data)


class MessageSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='sender_user',
            email='sender@example.com',
            password='TestPass123!'
        )
        self.room = Room.objects.create(owner=self.user, name='Test Room')
        self.message = Message.objects.create(
            sender=self.user,
            room=self.room,
            content='Test message',
            type='text'
        )
        

    def test_message_serialization(self):
        """Test sender_username is properly populated"""
        """Test message serialization includes all fields"""

        message = (self.room.messages
            .select_related("sender")
            .annotate(
                sender_username=F("sender__username"),
                msg_type=Case(
                    When(sender=self.user, then=Value("sent")),
                    default=Value("received"),
                    output_field=CharField(),
                )
            )
        ).first()
        serializer = MessageSerializer(message)

        expected_fields = ['id', 'sender', 'sender_username', 'room', 'type', 'content', 'timestamp', 'msg_type']
        self.assertEqual(serializer.data['sender_username'], 'sender_user')
        for field in expected_fields:
            self.assertIn(field, serializer.data)


    def test_read_only_fields(self):
        """Test read-only fields in message serializer"""
        message = Message.objects.create(
            sender=self.user,
            room=self.room,
            content='Test message'
        )
        
        serializer = MessageSerializer(message)
        read_only_fields = ['id', 'timestamp', 'sender', 'room']
        
        for field in read_only_fields:
            self.assertIn(field, serializer.data)


class MiniMessageSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='sender_user',
            email='sender@example.com',
            password='TestPass123!'
        )
        self.room = Room.objects.create(owner=self.user, name='Test Room')

    def test_mini_message_fields(self):
        """Test MiniMessageSerializer contains expected fields"""
        message = Message.objects.create(
            sender=self.user,
            room=self.room,
            content='Test message',
            type='text'
        )
        
        serializer = MiniMessageSerializer(message)
        expected_fields = ['id', 'room', 'sender', 'sender_username', 'type', 'content', 'timestamp']
        
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))

    def test_sender_username_source(self):
        """Test sender_username is sourced from sender.username"""
        message = Message.objects.create(
            sender=self.user,
            room=self.room,
            content='Test message'
        )
        
        serializer = MiniMessageSerializer(message)
        self.assertEqual(serializer.data['sender_username'], 'sender_user')
