from django.urls import path
from django.conf import settings
from chatapp.views import *
from chatapp import views

urlpatterns = [
    path('privatechat/', Privatechat.as_view(template_name = 'pages/chat/privatechat.html'), name='chat'),
    # path('directhat/<username>', views.Directs , name="direct"),
    path('directchat/<username>', Direct.as_view(template_name = 'pages/chat/privatechat.html') , name="direct"),
    path('send/', views.sendDirect , name='send-direct'),
]
