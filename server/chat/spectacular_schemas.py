from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import RoomOwnerSerializer, RoomOwnerDetailSerializer, PublicRoomSerializer, MessageSerializer


def doc_owner_room_list_schema():
    return extend_schema(
        summary="List rooms owned by the authenticated user",
        responses={
            200: OpenApiResponse(description="List of rooms owned by the user, paginated", response=RoomOwnerSerializer(many=True)),
            401: OpenApiResponse(description="Unauthorized (authentication required)")
        }
    )


def doc_owner_room_create_schema():
    return extend_schema(
        summary="Create a new room owned by the authenticated user",
        request=RoomOwnerSerializer,
        examples=[
            OpenApiExample(
                name="Valid Room Creation Request",
                description="Example data for creating a new room",
                value={
                    "name": "Test Room",
                    "access": "public",
                    "status": "active",
                    "limit": 3
                },
                request_only=True
            )
        ],
        responses={
            201: OpenApiResponse(description="Room created successfully"),
            400: OpenApiResponse(description="Bad request (validation errors)"),
            401: OpenApiResponse(description="Unauthorized (authentication required)")
        }
    )


def doc_owner_single_room_retrieve_schema():
    return extend_schema(
        summary="Retrieve details of a room owned by the authenticated user",
        responses={
            200: OpenApiResponse(description="Room details retrieved successfully", response=RoomOwnerDetailSerializer),
            401: OpenApiResponse(description="Unauthorized (authentication required)"),
            404: OpenApiResponse(description="Room not found or user is not the owner")
        }
    )


def doc_owner_single_room_update_schema():
    return extend_schema(
        summary="Update a room owned by the authenticated user",
        request=RoomOwnerDetailSerializer,
        examples=[
            OpenApiExample(
                name="Valid Room Update Request",
                description="Example data for updating a room",
                value={
                    "name": "Updated Room",
                    "access": "private",
                    "status": "active",
                    "limit": 5
                },
                request_only=True
            )
        ],
        responses={
            200: OpenApiResponse(description="Room updated successfully"),
            400: OpenApiResponse(description="Bad request (validation errors)"),
            401: OpenApiResponse(description="Unauthorized (authentication required)"),
            404: OpenApiResponse(description="Room not found or user is not the owner")
        }
    )


def doc_owner_single_room_delete_schema():
    return extend_schema(
        summary="Delete a room owned by the authenticated user",
        responses={
            204: OpenApiResponse(description="Room deleted successfully"),
            401: OpenApiResponse(description="Unauthorized (authentication required)"),
            404: OpenApiResponse(description="Room not found or user is not the owner")
        }
    )


def doc_public_all_room_list_schema():
    return extend_schema(
        summary="List all active public rooms with search capability",
        responses={
            200: OpenApiResponse(description="List of active public rooms, paginated", response=PublicRoomSerializer(many=True)),
            401: OpenApiResponse(description="Unauthorized (authentication required)")
        }
    )


def doc_public_room_detail_schema():
    return extend_schema(
        summary="Retrieve details of an active public room",
        responses={
            200: OpenApiResponse(description="Details of the public room", response=PublicRoomSerializer),
            401: OpenApiResponse(description="Unauthorized (authentication required)"),
            404: OpenApiResponse(description="Room not found or not active")
        }
    )


def doc_room_message_list_schema():
    return extend_schema(
        summary="List messages in a specific room",
        responses={
            200: OpenApiResponse(description="List of messages in the room, paginated", response=MessageSerializer(many=True)),
            401: OpenApiResponse(description="Unauthorized (authentication required)"),
            403: OpenApiResponse(description="Forbidden (user is not the owner or a participant)"),
            404: OpenApiResponse(description="Room not found")
        }
    )