from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import serializers
from .serializers import UserSerializer
from drf_spectacular.utils import inline_serializer


def doc_login_schema():
    return extend_schema(
        summary="Login to obtain access and refresh tokens",
        examples=[
            OpenApiExample(
                name="Valid Login Request",
                description="Example credentials for login",
                value={
                    "username": "test_user",
                    "password": "TestPass123!"
                },
                request_only=True
            )
        ],
        responses={
            200: OpenApiResponse(description="Successful login with tokens and user details"),
            401: OpenApiResponse(description="Unauthorized (invalid credentials)")
        }
    )


def doc_register_schema():
    return extend_schema(
        summary="Register a new user",
        request=UserSerializer,
        examples=[
            OpenApiExample(
                name="Valid Registration Request",
                description="Example data for registering a new user",
                value={
                    "username": "test_user",
                    "email": "test@example.com",
                    "password": "TestPass123!"
                },
                request_only=True
            )
        ],
        responses={
            201: OpenApiResponse(description="User registered successfully"),
            400: OpenApiResponse(description="Bad request (validation errors)")
        }
    )


def doc_profile_schema():
    return extend_schema(
        summary="Retrieve the authenticated user's profile",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="Unauthorized (authentication required)")
        }
    )


def doc_logout_schema():
    return extend_schema(
        summary="Logout by blacklisting the refresh token",
        request=inline_serializer(
            name='LogoutRequest',
            fields={
                'refresh': serializers.CharField(help_text="The refresh token to blacklist")
            }
        ),
        examples=[
            OpenApiExample(
                name="Valid Logout Request",
                description="Example refresh token for logout",
                value={
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                },
                request_only=True
            )
        ],
        responses={
            200: OpenApiResponse(description="Logout successful"),
            400: OpenApiResponse(description="Bad request (invalid token)"),
            401: OpenApiResponse(description="Unauthorized (authentication required)")
        }
    )