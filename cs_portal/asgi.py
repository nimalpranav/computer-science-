import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs_portal.settings")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import classroom.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(classroom.routing.websocket_urlpatterns)
    ),
})