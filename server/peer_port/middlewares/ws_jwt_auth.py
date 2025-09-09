import logging
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async


logger = logging.getLogger(__name__)


@database_sync_to_async
def get_user(user_id):
    User = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        query_params = dict(x.split('=') for x in query_string.split('&') if x)
        token = query_params.get('token')

        if token:
            try:
                validated_token = AccessToken(token)
                user = await get_user(validated_token["user_id"])
                scope['user'] = user

            except InvalidToken as e:
                scope['user'] = AnonymousUser()
                logger.error(f"Invalid Token: {e}")
                
            except TokenError as e:
                scope['user'] = AnonymousUser()
                logger.error(f"Token error: {e}")
                
        else:
            scope['user'] = AnonymousUser()
            logger.warning("WebSocket connection attempt without token")

        return await super().__call__(scope, receive, send)
    
