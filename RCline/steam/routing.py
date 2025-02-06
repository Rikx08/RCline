from django.urls import path
from .consumers import GameConsumer

websocket_urlpatterns = [
    path("ws/steam/", GameConsumer.as_asgi()),
]
