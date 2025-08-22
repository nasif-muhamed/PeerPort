import logging
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Room, Message
from .serializers import RoomOwnerSerializer, PublicRoomSerializer
from peer_port.pagination import CommonPagination

logger = logging.getLogger(__name__)


class OwnerRoomListCreateAPIView(ListCreateAPIView):
    serializer_class = RoomOwnerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_queryset(self):
        return (
            Room.objects.filter(owner=self.request.user)
            .annotate(participant_count=Count("participants"))
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PublicAllRoomListView(ListAPIView):
    serializer_class = PublicRoomSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_queryset(self):
        return (
            Room.objects.filter(status=Room.ACTIVE).select_related('owner').all()
            .annotate(participant_count=Count("participants"))
            .order_by("-created_at")
        )
