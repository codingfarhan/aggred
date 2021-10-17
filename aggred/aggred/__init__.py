import os
from django.core.asgi import get_asgi_application



django_asgi_app = get_asgi_application()

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aggred.settings")