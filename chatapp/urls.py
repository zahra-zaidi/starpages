from django.urls import path
from django.conf import settings
from chatapp.views import *
from chatapp import views

urlpatterns = [
    path('privatechat/', Privatechat.as_view(template_name = 'pages/chat/privatechat.html'), name='chat'),
    path('<str:username>/', room.as_view(template_name = 'pages/chat/privatechat.html'), name='room'),
]
