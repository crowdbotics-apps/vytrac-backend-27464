
from .consumers import Alerts
from django.urls import path

websocket_urlpatterns = [
    path('alerts/', Alerts.as_asgi()),
    # path('chat/', Chat.as_asgi())
]
