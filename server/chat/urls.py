from django.urls import path
from .views import OwnerRoomListCreateAPIView, PublicAllRoomListView

urlpatterns = [
    path('rooms/', OwnerRoomListCreateAPIView.as_view(), name='create-room'),
    path('all-rooms/', PublicAllRoomListView.as_view(), name='all-room'),
]
