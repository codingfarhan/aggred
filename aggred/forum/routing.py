from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/interact_with_post/(?P<post_id_>[\w\-]+)/$', consumers.interact_with_post_consumer.as_asgi()),
]