# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import  AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatModel ,Chat
from django.contrib.auth.models import User
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        my_id= self.scope['user'].id
        other_user_id=self.scope['url_route']['kwargs']['id']
        await self.chatid(my_id , other_user_id)

        if int(my_id) > int(other_user_id):
            self.room_name=f'{my_id}-{other_user_id}'
        else:
            self.room_name=f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None , bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username=text_data_json['username']



        # this line is saving mesages in db
        # await self.save_message(username,self.room_group_name ,message)



        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message ,
                'username':username,
                
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        _message = event['message']
        _username=event['username']


        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": _message,
                    "username": _username,
                    'timestamp': timezone.now().isoformat()
                }
            )
        )


        
    @database_sync_to_async
    def save_message(self, username , thread_name, message):
        ChatModel.objects.create(sender=username,message=message, thread_name=thread_name)
    

    @database_sync_to_async
    def chatid(self, username , otherusername):
        _user1=User.objects.get(id=username)
        _user2=User.objects.get(id=otherusername)
        Chat.objects.create(user1=_user1,user2=_user2)