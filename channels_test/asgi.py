"""
ASGI config for channels_test project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import chat.routing
from chat.middlewares import JWTTokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channels_test.settings')

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # "websocket": JWTTokenAuthMiddleware(URLRouter(chat.routing.websocket_urlpatterns)),
    "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))),
})
