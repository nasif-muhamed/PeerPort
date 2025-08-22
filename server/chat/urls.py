from django.urls import path
from .views import OwnerRoomListCreateAPIView

urlpatterns = [
    path('rooms/', OwnerRoomListCreateAPIView.as_view(), name='create-room'),
]
