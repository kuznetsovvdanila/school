from django.urls import path
import consumers

websocket_urlpatterns = [
    path('lk', consumers.UserConsumer.as_asgi()),
]
