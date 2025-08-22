from django.urls import re_path
from chat.consumers import chat_consumer

websocket_urlpatterns = [
    # re_path(r'ws/notifications/$', notification_websocket_consumer.NotificationConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_id>[a-f0-9]{24})/$', chat_consumer.ChatConsumer.as_asgi()),
]