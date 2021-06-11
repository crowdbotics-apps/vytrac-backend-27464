from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from backend.get_user import get_user
from Alerts.routing import websocket_urlpatterns


# from jwt import decode


# TODO encode and decode the jwt_token


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
