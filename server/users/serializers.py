from rest_framework import serializers
from django.contrib.auth import get_user_model
from .validators import validate_username, validate_email, validate_password
from .services import create_user


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])
    password = serializers.CharField(write_only=True, validators=[validate_password])
    email = serializers.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = create_user(validated_data)
        return user