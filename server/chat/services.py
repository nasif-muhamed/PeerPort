import logging
from channels.db import database_sync_to_async

from .models import Room

logger = logging.getLogger(__name__)


# websocket services:
@database_sync_to_async
def permission_to_join_room(user, room_id):
    logger.debug(user, room_id)
    try:
        room = Room.objects.get(id=room_id, status=Room.ACTIVE)
        print(room.participants.count())
        if room.limit < room.participants.count():
            return False
        if room.access == Room.PUBLIC:
            if not room.participants.filter(id=user.id).exists():
                room.participants.add(user)
                room.save(update_fields=[])
            return True
        else:
            return False
    except Room.DoesNotExist:
        return False
    except Exception as e:
        logger.error(f"Error adding user to room: {e}")
        return False
