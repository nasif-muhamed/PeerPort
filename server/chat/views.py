import logging
from django.db.models import Count, Case, When, Value, CharField, F, Exists, OuterRef
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Room, Message
from .serializers import RoomOwnerSerializer, RoomOwnerDetailSerializer, PublicRoomSerializer, MessageSerializer
from peer_port.pagination import CommonPagination
from .view_methods import (
    OwnerRoomMethodsMixin,
    OwnerSingleRoomMethodsMixin,
    PublicAllRoomMethodsMixin,
    PublicRoomDetailMethodsMixin,
    RoomMessageMethodsMixin
)


logger = logging.getLogger(__name__)


class OwnerRoomListCreateAPIView(OwnerRoomMethodsMixin, ListCreateAPIView):
    serializer_class = RoomOwnerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_queryset(self):
        return (
            Room.objects.filter(owner=self.request.user)
            .annotate(participant_count=Count("participants"))
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OwnerSingleRoomAPIView(OwnerSingleRoomMethodsMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = RoomOwnerDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return (
            Room.objects.filter(owner=self.request.user)
            .prefetch_related('participants')
        )


class PublicAllRoomListView(PublicAllRoomMethodsMixin, ListAPIView):
    serializer_class = PublicRoomSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_queryset(self):
        user = self.request.user
        search_term = self.request.query_params.get('search', None)
        queryset = Room.objects.filter(status=Room.ACTIVE).select_related("owner").annotate(
            participant_count=Count("participants"),
            is_participant=Exists(
                Room.participants.through.objects.filter(
                    room_id=OuterRef("pk"), user_id=user.id
                )
            )
        )
        if search_term:
            queryset = queryset.filter(
                name__icontains=search_term
            )

        return queryset.order_by("-created_at")


class PublicRoomDetailView(PublicRoomDetailMethodsMixin, RetrieveAPIView):
    serializer_class = PublicRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Room.objects.filter(status=Room.ACTIVE).select_related("owner").annotate(
            participant_count=Count("participants")
        )


class RoomMessageListView(RoomMessageMethodsMixin, ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        user = self.request.user

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise PermissionDenied("Room does not exist.")

        if room.owner != user and not room.participants.filter(id=user.id).exists():
            raise PermissionDenied("You are not a participant of this room.")

        return (
            room.messages
            .select_related("sender")
            .annotate(
                sender_username=F("sender__username"),
                msg_type=Case(
                    When(sender=user, then=Value("sent")),
                    default=Value("received"),
                    output_field=CharField(),
                )
            )
        )
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # reversing the list for the UI purpose: oldest - newest
        response.data["results"].reverse()
        return response
