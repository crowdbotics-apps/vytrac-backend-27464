from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.routing import ProtocolTypeRouter, URLRouter
from django.contrib.auth.models import AnonymousUser
from django.core.asgi import get_asgi_application
# from jwt import decode
from rest_framework_simplejwt.tokens import UntypedToken

from Alerts.routing import websocket_urlpatterns
from Functions.debuging import Debugging
from users.models import User


# TODO encode and decode the jwt_token


@database_sync_to_async
def get_user(querys):
    Debugging('xxxxxxxx', color='yellow')
    token = parse_qs(querys.decode("utf8"))['token'][0]
    token_data = UntypedToken(token)
    user_id = token_data["user_id"]
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class QueryAuthMiddleware:
    def __init__(self, app):
        self.app = app
    async def __call__(self, scope, receive, send):
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
