
from .consumers import WSConsumer
from django.urls import path

websocket_urlpatterns = [
    path('test/', WSConsumer.as_asgi()),
    # path('notifcation/', WSConsumer.as_asgi())
]
