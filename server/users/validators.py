import re
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()
USERNAME_PATTERN = r'^[a-z0-9_]+$'
PASSWORD_SPECIAL_CHARS = r'[!@#$%^&*(),.?":{}|<>]'
UPPER_CASE = r'[A-Z]'
LOWER_CASE = r'[a-z]'
DIGITS = r'[0-9]'
SPACE = r'\s'


def validate_username(value):
    if len(value) < 4:
        raise ValidationError("Username must be at least 4 characters long.")
    if len(value) > 20:
        raise ValidationError("Username cannot be longer than 20 characters.")
    if sum(c.isalpha() for c in value) < 3:
        raise ValidationError("Username must contain at least three letters.")
    if not re.match(USERNAME_PATTERN, value):
        raise ValidationError("Username must only contain lowercase letters, numbers and underscores.")
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError("This username is already taken.")
    return value


def validate_email(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError("This email is already registered.")
    return value


def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')            
    if not re.search(PASSWORD_SPECIAL_CHARS, value):
        raise ValidationError('Password must contain at least one special character.')
    if not re.search(UPPER_CASE, value):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not re.search(LOWER_CASE, value):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.search(DIGITS, value):
        raise ValidationError('Password must contain at least one digit.')
    if re.search(SPACE, value):
        raise ValidationError('Password must not contain empty space.')
    return value
