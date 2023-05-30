import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from school_app import routing  # импортируем файл routing из нашего приложения
from channels.layers import get_channel_layer
from CONFIG import ENVIROMENTALPATH

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.'+ENVIROMENTALPATH)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

channel_layer = get_channel_layer()
