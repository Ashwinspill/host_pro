from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('message_page/', consumers.ChatConsumer.as_asgi()),
]