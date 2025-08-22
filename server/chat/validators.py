from django.core.exceptions import ValidationError
from .models import Room


def validate_name(value):
    if len(value) < 3:
        raise ValidationError("Room name must be at least 3 characters.")
    if len(value) > 255:
        raise ValidationError("Room name should not be more than 255 characters.")
    if not value.replace(" ", "").isalnum():
        raise ValidationError("Room name should only contain letters, numbers, and spaces.")
    if Room.objects.filter(name=value).exists():
        raise ValidationError(f"A room with the name '{value}' already exists.")
    return value


def validate_access(value):
    if value not in [Room.PUBLIC, Room.PRIVATE]:
        raise ValidationError("Invalid access type.")
    return value


def validate_status(value):
    if value not in [Room.ACTIVE, Room.INACTIVE]:
        raise ValidationError("Invalid status type.")
    return value


def validate_limit(value):
    if value < 1 or value > 50:
        raise ValidationError("Limit must be between 1 and 50.")
    return value
