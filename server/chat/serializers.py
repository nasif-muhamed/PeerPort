from rest_framework import serializers
from .models import Room, Message
from .validators import validate_name, validate_access, validate_status, validate_limit
from users.serializers import MiniUserSerializer


class MiniMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "room", "sender", "sender_username", "type", "content", "timestamp"]
        read_only_fields = ["id", "timestamp", "sender", "room"]


class RoomOwnerSerializer(serializers.ModelSerializer):
    participant_count = serializers.SerializerMethodField()
    name = serializers.CharField(validators=[validate_name])
    access = serializers.CharField(validators=[validate_access], required=False)
    status = serializers.CharField(validators=[validate_status], required=False)
    limit = serializers.IntegerField(validators=[validate_limit], required=False)
    last_message = MiniMessageSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'access', 'status', 'limit', 'participant_count', 'last_message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'participant_count', 'last_message', 'created_at', 'updated_at']

    def get_participant_count(self, obj):
        return getattr(obj, "participant_count", obj.participants.count())


class PublicRoomSerializer(serializers.ModelSerializer):
    participant_count = serializers.IntegerField(read_only=True)
    is_participant = serializers.BooleanField(read_only=True)
    owner = MiniUserSerializer(read_only=True)
    last_message = MiniMessageSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'owner', 'access', 'limit', 'participant_count', 'is_participant', 'last_message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'participant_count', 'is_participant', 'last_message', 'created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(read_only=True)
    msg_type = serializers.CharField(read_only=True)
  
    class Meta:
        model = Message
        fields = ["id", "sender", "sender_username", "room", "type", "content", "timestamp", "msg_type"]
        read_only_fields = ["id", "timestamp", "sender", "room"]
