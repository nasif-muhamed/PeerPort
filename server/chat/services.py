import logging
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Room, Message
from .serializers import MiniMessageSerializer

User = get_user_model()
logger = logging.getLogger(__name__)


# websocket services:
@database_sync_to_async
def permission_to_join_room(user, room_id):
    logger.debug(user, room_id)
    try:
        room = Room.objects.get(id=room_id, status=Room.ACTIVE)
        print('join room count:', room.participants.count())
        if room.participants.filter(id=user.id).exists():
            return True, False
        if room.limit <= room.participants.count():
            return False, False
        if room.access == Room.PUBLIC:
            room.participants.add(user)
            room.save(update_fields=[])
            print('join inside room count:', room.participants.count())
            return True, True
        else:
            return False, False
    except Room.DoesNotExist:
        return False, False
    except Exception as e:
        logger.error(f"Error adding user to room: {e}")
        return False, False


@database_sync_to_async
def participant_leave_room(user, room_id):
    """
    Allow a participant to voluntarily leave a room.
    """
    try:
        room = Room.objects.get(id=room_id, status=Room.ACTIVE)
        logger.debug('room:', room)
        print('leave count:', room.participants.count())
        print(room.owner == user)
        if room.owner == user:
            return False
        if room.participants.filter(id=user.id).exists():
            print('inside')
            room.participants.remove(user)
            room.save(update_fields=[])
            print('count:', room.participants.count())
            return True
        return False

    except Room.DoesNotExist:
        return False
    except Exception as e:
        logger.error(f"Error leaving room: {e}")
        return False


@database_sync_to_async
def remove_participant(owner, room_id, target_user_id):
    """
    Allow the room owner to remove a participant from the room.
    """
    try:
        room = Room.objects.get(id=room_id, status=Room.ACTIVE)

        if room.owner_id != owner.id:
            return False  # only the owner can remove participants

        target_user = User.objects.get(id=target_user_id)

        if room.participants.filter(id=target_user.id).exists():
            room.participants.remove(target_user)
            room.save(update_fields=[])
            return True
        return False  # target not in room

    except Room.DoesNotExist:
        return False
    except User.DoesNotExist:
        return False
    except Exception as e:
        logger.error(f"Error removing participant from room: {e}")
        return False

@database_sync_to_async
def save_message(user, room_id, message, message_type):
    room = Room.objects.get(id=room_id)
    msg = Message(
        sender=user,
        room=room,
        content=message,
        type=message_type,
    )
    msg.save()
    return MiniMessageSerializer(msg).data
