# chat/routing.py
from django.urls import re_path,path
from chatapp import consumers
from . import consumers

websocket_urlpatterns = [
      path('ws/<int:id>/', consumers.ChatConsumer.as_asgi()),
]