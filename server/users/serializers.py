from rest_framework import serializers
from django.contrib.auth import get_user_model
from .validators import validate_username, validate_email, validate_password
from .services import create_user
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
        }

        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])
    password = serializers.CharField(write_only=True, validators=[validate_password])
    email = serializers.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = create_user(validated_data)
        return user
    

# using in: RoomOwnerDetailSerializer, PublicRoomSerializer
class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
