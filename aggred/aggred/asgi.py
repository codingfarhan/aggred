"""
ASGI config for aggred project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import django
from channels.auth import AuthMiddlewareStack

from forum.routing import websocket_urlpatterns as url_pattern1



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggred.settings')

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "https": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(url_pattern1)
    )
})
