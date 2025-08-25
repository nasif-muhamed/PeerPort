import json
from channels.generic.websocket import AsyncWebsocketConsumer

from ..services import permission_to_join_room, participant_leave_room, remove_participant, save_message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        self.room_groups = {}
        await self.accept()

    async def disconnect(self, close_code):
        # Leave all rooms on disconnect
        for room_id in self.room_groups.values():
            await participant_leave_room(self.user, room_id)
            await self.channel_layer.group_discard(
                f"chat_{room_id}", self.channel_name
            )
            
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data["type"]
        room_id = data.get("room_id")
        payload = data.get("payload")

        if message_type == "join_room":
            allowed, created = await permission_to_join_room(self.user, room_id)
            if allowed:
                await self.join_room(room_id)
                await self.channel_layer.group_send(
                    f"chat_{room_id}",
                    {
                        "type": "group_notification",
                        "room_id": room_id,
                        "sub_type": 'joined',
                        "payload": {
                            "message": f"{self.user.username} {"joined the room" if created else "is online"}",
                            "sender": "system",
                            "sender_id": self.user.id,
                        },
                    },
                )
            else:
                await self.send(text_data=json.dumps({
                    "type": "join_denied",
                    "room_id": room_id,
                    "payload": {"reason": "Access denied or room is full."}
                }))
                
        # elif message_type == "leave_room":
        #     await self.leave_room(room_id)
        #     await self.channel_layer.group_send(
        #         f"chat_{room_id}",
        #         {
        #             "type": "group_notification",
        #             "room_id": room_id,
        #             "sub_type": 'left',
        #             "payload": {
        #                 "message": f"{self.user.username} is offline",
        #                 "sender": "system",
        #             },
        #         },
        #     )


        elif message_type == "left_room":
            left = await participant_leave_room(self.user, room_id)
            print('left:', left)
            if left:
                await self.channel_layer.group_send(
                    f"chat_{room_id}",
                    {
                        "type": "group_notification",
                        "room_id": room_id,
                        "sub_type": 'left',
                        "payload": {
                            "message": f"{self.user.username} left the room",
                            "sender": "system",
                            "sender_id": self.user.id,
                        },
                    },
                )
                await self.leave_room(room_id)
            else:
                await self.send(text_data=json.dumps({
                    "type": "leave_denied",
                    "room_id": room_id,
                    "payload": {"reason": "Unable to leave the room. You may not be a participant or the room does not exist."}
                }))

        elif message_type == "send_chat":
            message = payload.get('message')
            msg_type = data.get('message_type', 'text')
            serialized_message = await save_message(self.user, room_id, message, msg_type)
            await self.channel_layer.group_send(
                f"chat_{room_id}",
                {
                    "type": "chat_message",
                    "room_id": room_id,
                    "payload": {
                        "message": serialized_message,
                        "sender": self.user.id,
                    },
                },
            )

        elif message_type == "notification":
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "notification",
                        "payload": payload,
                    }
                )
            )
    
    async def chat_message(self, event):
        # Forward chat messages to the client
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_recieved",
                    "room_id": event.get("room_id"),
                    "payload": event["payload"],
                }
            )
        )

    async def join_room(self, room_id):
        self.room_groups[room_id] = f"chat_{room_id}"
        await self.channel_layer.group_add(f"chat_{room_id}", self.channel_name)

    async def leave_room(self, room_id):
        if room_id in self.room_groups:
            await self.channel_layer.group_discard(
                f"chat_{room_id}", self.channel_name
            )

    async def group_notification(self, event):
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
