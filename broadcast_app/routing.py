from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/broadcast/(?P<stream_id>\w+)/$', consumers.BroadcastConsumer.as_asgi()),
]