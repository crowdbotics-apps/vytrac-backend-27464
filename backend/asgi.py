import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from notifications.routing import websocket_urlpatterns
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import RefreshToken
from channels.db import database_sync_to_async
from users.models import User
# from jwt import decode
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from urllib.parse import parse_qs

# TODO encode and decode the jwt_token
from jwt import decode as jwt_decode


@database_sync_to_async
def get_user(querys):
    token = parse_qs(querys.decode("utf8"))['token'][0]
    token_data = UntypedToken(token)
    user_id = token_data["user_id"]
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class QueryAuthMiddleware:
    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        scope['user'] = await get_user(scope["query_string"])

        return await self.app(scope, receive, send)


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": QueryAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
