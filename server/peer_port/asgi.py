"""
ASGI config for peer_port project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

"""
I added this before importing JWTAuthMiddleware. Because If we didn't 
setup django initially, imports in the middleware will throw error.
"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peer_port.settings')
django.setup()

from .websocket import routing
from .middlewares.ws_jwt_auth import JWTAuthMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        JWTAuthMiddleware(
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    ),
})
