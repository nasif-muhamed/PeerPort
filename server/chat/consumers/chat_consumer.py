import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

from ..services import permission_to_join_room, participant_leave_room, remove_participant, save_message


logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close(code=4000, reason="Anonymous users are not allowed")
            return
        
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_name = f"room_{self.room_id}"

        allowed, _ = await permission_to_join_room(self.user, self.room_id)
        if allowed:
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "group_notification",
                    "room_id": self.room_id,
                    "sub_type": 'joined',
                    "payload": {
                        "message": f"{self.user.username} joined the room",
                        "sender": "system",
                        "sender_id": self.user.id,
                    },
                },
            )

        else:
            await self.close(code=4002, reason="You are not authorized to join this room")
            

    async def disconnect(self, close_code):
        if not self.user.is_anonymous:
            try:
                await participant_leave_room(self.user, self.room_id)
                await self.channel_layer.group_discard(
                    self.room_name,
                    self.channel_name
                )
                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        "type": "group_notification",
                        "room_id": self.room_id,
                        "sub_type": 'left',
                        "payload": {
                            "message": f"{self.user.username} left the room",
                            "sender": "system",
                            "sender_id": self.user.id,
                        },
                    },
                )
            except Exception as e:
                logger.error(f"Error in disconnect: {e}", exc_info=True)
                # Continue with group discard and notification even if participant_leave_room fails
                await self.channel_layer.group_discard(
                    self.room_name,
                    self.channel_name
                )
            
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data["type"]
        payload = data.get("payload")
        logger.info(f'In recieve: {message_type}')

        if message_type == "send_chat":
            message = payload.get('message')
            if not message.strip():
                return
            msg_type = data.get('message_type', 'text')
            serialized_message = await save_message(self.user, self.room_id, message, msg_type)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "payload": {
                        "message": serialized_message,
                        "sender": self.user.id,
                    },
                },
            )

        elif message_type == "typing":
            pass


    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_recieved",
                    "payload": event["payload"],
                }
            )
        )

    async def group_notification(self, event):
        try:
            logger.debug(f"group_notification: {event}")
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "group_notification",
                        "sub_type": event.get("sub_type"),
                        "room_id": event.get("room_id"),
                        "payload": event["payload"],
                    }
                )
            )
        except Exception as e:
            logger.error(f"Error sending group_notification: {e}", exc_info=True)
