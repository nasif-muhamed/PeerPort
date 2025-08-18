from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username
