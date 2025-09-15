import json
import pytest
from django.urls import reverse
from rest_framework import status
from asgiref.sync import sync_to_async


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_full_chat_flow(api_client, ws_communicator):
    """
    Complete flow:
    1. Register user
    2. Login and get JWT
    3. Create room
    4. List rooms
    5. Join an existing room
    6. Connect via WebSocket, receive join notification
    7. List messages
    8. Send a message and receive it back
    9. Leave group (close WS)
    10. Logout
    """
    # 1️ - Register
    register_data = {
        "username": "pytest_user",
        "email": "pytest@example.com",
        "password": "TestPass123!"
    }
    res = await sync_to_async(api_client.post)(reverse("register-user"), register_data)
    assert res.status_code == status.HTTP_201_CREATED

    # 2️ - Login
    login_data = {
        "username": "pytest_user",
        "password": "TestPass123!"
    }
    res = await sync_to_async(api_client.post)(reverse("user-login"), login_data)
    assert res.status_code == status.HTTP_200_OK
    access_token = res.data["access"]
    refresh_token = res.data["refresh"]

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # 3️ - Create room
    room_data = {"name": "pytest room 1", "access": "public"}
    res = await sync_to_async(api_client.post)(reverse("create-room"), room_data)
    assert res.status_code == status.HTTP_201_CREATED
    created_room_id = res.data["id"]

    # 4️ - List all rooms
    res = await sync_to_async(api_client.get)(reverse("all-room"))
    assert res.status_code == status.HTTP_200_OK
    assert any(room["id"] == created_room_id for room in res.data["results"])

    # 5️ - Get detail of the room
    res = await sync_to_async(api_client.get)(reverse("single-room", kwargs={"pk": created_room_id}))
    assert res.status_code == status.HTTP_200_OK
    assert res.data["id"] == created_room_id

    # 6️ - Connect via WebSocket
    communicator = await ws_communicator(created_room_id, access_token)
    connected, _ = await communicator.connect()
    assert connected

    # Expect join group notification
    join_event = await communicator.receive_json_from(timeout=2)
    assert join_event["type"] == "group_notification"
    assert join_event["sub_type"] == "joined"

    # 7 - Get list of messages from the room
    res = await sync_to_async(api_client.get)(reverse("room-messages", kwargs={"room_id": created_room_id}))
    assert res.status_code == status.HTTP_200_OK

    # 8 - Send a message and receive it back
    message_payload = {
        "type": "send_chat",
        "payload": {"message": "Hello from pytest!"}
    }
    await communicator.send_json_to(message_payload)

    chat_response = await communicator.receive_json_from(timeout=2)
    assert chat_response["type"] == "chat_recieved"
    assert chat_response["payload"]["message"]["content"] == "Hello from pytest!"

    # 9 - Leave group (close WS)
    await communicator.disconnect()

    # 10 - Logout
    logout_res = await sync_to_async(api_client.post)(reverse("logout-user"), {"refresh": refresh_token})
    assert logout_res.status_code == status.HTTP_200_OK

    # Verify token blacklisted
    refresh_res = await sync_to_async(api_client.post)(reverse("refresh-token"), {"refresh": refresh_token})
    assert refresh_res.status_code == status.HTTP_401_UNAUTHORIZED
