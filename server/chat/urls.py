from django.urls import path
from .views import OwnerRoomListCreateAPIView, PublicAllRoomListView, PublicRoomDetailView, RoomMessageListView

urlpatterns = [
    path('rooms/', OwnerRoomListCreateAPIView.as_view(), name='create-room'),
    path('all-rooms/', PublicAllRoomListView.as_view(), name='all-room'),
    path('rooms/<int:pk>/', PublicRoomDetailView.as_view(), name='single-room'),
    path("rooms/<int:room_id>/messages/", RoomMessageListView.as_view(), name="room-messages"),
]
