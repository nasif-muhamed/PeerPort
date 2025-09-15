from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from chat.models import Room, Message
from chat.consumers.chat_consumer import ChatConsumer
import json
import asyncio
from django.db import connections

User = get_user_model()


class ChatConsumerTest(TransactionTestCase):
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
            name='Test Chat Room'
        )
        self.room.participants.add(self.participant)

    def tearDown(self):
        # Close all database connections after each test to prevent "connection already closed" errors
        for conn in connections.all():
            conn.close()
        super().tearDown()

    async def test_authenticated_user_can_connect(self):
        """Test authenticated participant can connect to websocket"""
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/room/{self.room.id}/"
        )
        communicator.scope["user"] = self.participant
        communicator.scope['url_route'] = {'kwargs': {'room_id': str(self.room.id)}}
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        # Should receive join notification
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "group_notification")
        self.assertEqual(response["sub_type"], "joined")
        
        await communicator.disconnect()

    async def test_anonymous_user_cannot_connect(self):
        """Test anonymous user cannot connect to websocket"""
        from django.contrib.auth.models import AnonymousUser
        
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/room/{self.room.id}/"
        )
        communicator.scope["user"] = AnonymousUser()
        communicator.scope['url_route'] = {'kwargs': {'room_id': str(self.room.id)}}
        
        connected, subprotocol = await communicator.connect()
        self.assertFalse(connected)

    async def test_non_participant_can_connect_to_public_room(self):
        """Test non-participant cannot connect to websocket"""
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/room/{self.room.id}/"
        )
        communicator.scope["user"] = self.non_participant
        communicator.scope['url_route'] = {'kwargs': {'room_id': str(self.room.id)}}
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

    async def test_send_message_workflow(self):
        """Test sending message through websocket"""
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/room/{self.room.id}/"
        )
        communicator.scope["user"] = self.participant
        communicator.scope['url_route'] = {'kwargs': {'room_id': str(self.room.id)}}
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        # Clear join notification
        await communicator.receive_json_from()
        
        # Send message
        await communicator.send_json_to({
            "type": "send_chat",
            "message_type": "text",
            "payload": {
                "message": "Hello, World!"
            }
        })
        
        # Should receive message back
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "chat_recieved")
        self.assertEqual(response["payload"]["message"]["content"], "Hello, World!")
        
        # Verify message was saved to database
        message_exists = await database_sync_to_async(
            lambda: Message.objects.filter(
                content="Hello, World!",
                sender=self.participant,
                room=self.room
            ).exists()
        )()
        self.assertTrue(message_exists)
        
        await communicator.disconnect()

    async def test_empty_message_ignored(self):
        """Test empty messages are ignored"""
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/room/{self.room.id}/"
        )
        communicator.scope["user"] = self.participant
        communicator.scope['url_route'] = {'kwargs': {'room_id': str(self.room.id)}}
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        # Clear join notification
        await communicator.receive_json_from()
        
        # Send empty message
        await communicator.send_json_to({
            "type": "send_chat",
            "message_type": "text",
            "payload": {
                "message": "   "  # Only whitespace
            }
        })
        
        # Should not receive anything back (with timeout)
        try:
            response = await asyncio.wait_for(
                communicator.receive_json_from(),
                timeout=1.0
            )
            self.fail("Should not receive response for empty message")
        except asyncio.TimeoutError:
            pass  # Expected
        
        # Ensure disconnection completes
        try:
            await communicator.disconnect()
            await asyncio.sleep(0.1)  # Small delay to allow cleanup
        except asyncio.CancelledError:
            pass  # Ignore CancelledError during cleanup

    async def test_disconnect_sends_leave_notification(self):
        """Test disconnect sends leave notification"""
        communicator1 = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/room/{self.room.id}/"
        )
        communicator1.scope["user"] = self.participant
        communicator1.scope['url_route'] = {'kwargs': {'room_id': str(self.room.id)}}
        
        communicator2 = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/room/{self.room.id}/"
        )
        communicator2.scope["user"] = self.owner
        communicator2.scope['url_route'] = {'kwargs': {'room_id': str(self.room.id)}}
        
        # Connect both
        await communicator1.connect()
        await communicator2.connect()
        
        # Clear join notifications
        await communicator1.receive_json_from()  # participant joined
        await communicator2.receive_json_from()  # owner joined
        await communicator1.receive_json_from()  # owner joined (received by participant)
        
        # Disconnect participant
        await communicator1.disconnect()
        
        # Owner should receive leave notification
        response = await communicator2.receive_json_from()
        self.assertEqual(response["type"], "group_notification")
        self.assertEqual(response["sub_type"], "left")
        self.assertIn("left the room", response["payload"]["message"])
        
        await communicator2.disconnect()

    def test_connect_authenticated_user(self):
        """Test wrapper for authenticated connection"""
        async def test():
            await self.test_authenticated_user_can_connect()
        
        asyncio.run(test())

    def test_connect_anonymous_user(self):
        """Test wrapper for anonymous connection"""
        async def test():
            await self.test_anonymous_user_cannot_connect()
        
        asyncio.run(test())

    def test_connect_non_participant_to_public_room(self):
        """Test wrapper for non-participant connection"""
        async def test():
            await self.test_non_participant_can_connect_to_public_room()
        
        asyncio.run(test())

    def test_send_message(self):
        """Test wrapper for message sending"""
        async def test():
            await self.test_send_message_workflow()
        
        asyncio.run(test())

    def test_empty_message(self):
        """Test wrapper for empty message handling"""
        async def test():
            await self.test_empty_message_ignored()
        
        asyncio.run(test())

    def test_disconnect_notification(self):
        """Test wrapper for disconnect notification"""
        async def test():
            await self.test_disconnect_sends_leave_notification()
        
        asyncio.run(test())