from django.db import models
from django.contrib.auth.models import User 
from django.db.models import Model , Max , Count , Sum
# Create your models here.

class Chat(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    user1=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='User1')
    user2=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='User2')
    seen1=models.BooleanField(default=True)
    seen2=models.BooleanField(default=True)

class ChatModel(models.Model):
    chat_id=models.ForeignKey('Chat',on_delete=models.DO_NOTHING,related_name='chat_id')
    sender=models.CharField(max_length=100 , default=None)
    message= models.TextField(null=True , blank=True )
    thread_name= models.CharField(null=True , blank=True ,max_length=50)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.message


