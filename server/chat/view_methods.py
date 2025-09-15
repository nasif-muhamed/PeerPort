from .spectacular_schemas import (
    doc_owner_room_list_schema,
    doc_owner_room_create_schema,
    doc_owner_single_room_retrieve_schema,
    doc_owner_single_room_update_schema,
    doc_owner_single_room_delete_schema,
    doc_public_all_room_list_schema,
    doc_public_room_detail_schema,
    doc_room_message_list_schema
)


class OwnerRoomMethodsMixin:
    @doc_owner_room_list_schema()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @doc_owner_room_create_schema()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OwnerSingleRoomMethodsMixin:
    @doc_owner_single_room_retrieve_schema()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @doc_owner_single_room_update_schema()
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @doc_owner_single_room_update_schema()
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @doc_owner_single_room_delete_schema()
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class PublicAllRoomMethodsMixin:
    @doc_public_all_room_list_schema()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PublicRoomDetailMethodsMixin:
    @doc_public_room_detail_schema()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RoomMessageMethodsMixin:
    @doc_room_message_list_schema()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)