from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('lk', consumers.UserConsumer.as_asgi()),
]
