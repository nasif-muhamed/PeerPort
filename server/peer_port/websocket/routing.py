from django.urls import re_path
from chat.consumers import chat_consumer

websocket_urlpatterns = [
    re_path(r'^ws/room/(?P<room_id>\d+)/$', chat_consumer.ChatConsumer.as_asgi()),
]