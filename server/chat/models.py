from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Room(models.Model):
    PUBLIC = "public"
    PRIVATE = "private"
    ACCESS_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    )

    ACTIVE = "active"
    INACTIVE = "inactive"
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_rooms')
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    participants = models.ManyToManyField(User, related_name='participating_rooms', blank=True)
    last_message = models.ForeignKey("Message", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    access = models.CharField(max_length=10, choices=ACCESS_CHOICES, default=PUBLIC)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    limit = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(50)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_access_display()})"

    def can_add_participant(self):
        """Check if room is full or not"""
        return self.participants.count() < self.limit

    # Add the owner to participants on creation of a new room.
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.participants.filter(id=self.owner.id).exists():
            self.participants.add(self.owner)


class Message(models.Model):
    TYPE_CHOICES = (
        ('text', 'Text'),
        ('image', 'Image'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')
    content = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.sender.username} in {self.room.name}"

    def save(self, *args, **kwargs):
        """Update last_message field in room whenever a message is saved"""
        super().save(*args, **kwargs)
        self.room.last_message = self
        self.room.save(update_fields=["last_message"])
