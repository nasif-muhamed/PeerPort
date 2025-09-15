import pytest
from rest_framework.test import APIClient
from channels.testing import WebsocketCommunicator
from peer_port.asgi import application
from django.db import connections


@pytest.fixture
def api_client():
    """DRF APIClient for HTTP requests"""
    return APIClient()


@pytest.fixture
async def ws_communicator():
    """Factory to create WebSocket communicator"""
    async def _create(room_id, token):
        return WebsocketCommunicator(
            application,
            f"/ws/room/{room_id}/?token={token}"
        )
    return _create


@pytest.fixture(autouse=True)
def close_connections():
    yield
    for conn in connections.all():
        conn.close()

