from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(data):
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    return user