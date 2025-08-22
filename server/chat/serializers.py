from rest_framework import serializers
from .models import Room, Message
from .validators import validate_name, validate_access, validate_status, validate_limit

class RoomOwnerSerializer(serializers.ModelSerializer):
    participant_count = serializers.SerializerMethodField()
    name = serializers.CharField(validators=[validate_name])
    access = serializers.CharField(validators=[validate_access], required=False)
    status = serializers.CharField(validators=[validate_status], required=False)
    limit = serializers.IntegerField(validators=[validate_limit], required=False)

    class Meta:
        model = Room
        fields = ['id', 'name', 'access', 'status', 'limit', 'participant_count', 'last_message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'participant_count', 'last_message', 'created_at', 'updated_at']

    def get_participant_count(self, obj):
        return getattr(obj, "participant_count", obj.participants.count())
