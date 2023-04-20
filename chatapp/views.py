from django.shortcuts import render
from django.views.generic import TemplateView 
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.contrib.auth.models import User 
from django.http import HttpResponse,HttpResponseRedirect
from chatapp.models import ChatModel
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class Privatechat(LoginRequiredMixin , TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'pages/chat/privatechat.html'
    # Predefined function
    def get_context_data(self, **kwargs ):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        # KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        # KTTheme.addJavascriptFile('js/custom/apps/chat/chat.js')

        # Include vendors and javascript files for dashboard widgets
        allusers=User.objects.all()

        context.update({
            'layout': KTTheme.setLayout('default.html'),
            'users': allusers,

        
        })

        return context
    

class room(LoginRequiredMixin , TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'pages/chat/privatechat.html'
    # Predefined function
    def get_context_data(self,username, **kwargs ):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        # KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        # KTTheme.addJavascriptFile('js/custom/apps/chat/chat.js')

        # Include vendors and javascript files for dashboard widgets
        # allusers=User.objects.all()
        user_obj=User.objects.get(username=username)
        users=User.objects.exclude(username=self.request.user.username)

        if self.request.user.id > user_obj.id:
            thread_name= f'chat_{self.request.user.id}-{user_obj.id}'
        else:
            thread_name= f'chat_{user_obj.id}-{self.request.user.id}'

        message_obj=ChatModel.objects.filter(thread_name=thread_name)
        username=self.request.user.username

        context.update({
            'layout': KTTheme.setLayout('default.html'),
            'users': users,
            'user':user_obj,
            'User':username,
            'messages':message_obj
        })

        return context




#  def Directs (request, username): 

#     user=request.user
#     messages = Messages.get_message (user=user)
#     active_directs=username
#     directs=Messages.objects.filter(user=user, reciepient__username=username)
#     directs.update(is_read=True)

#     for message in messages :
#         if message["user"].username == username:
#             message["unread"] = 0

#     context ={
#     "messages" :messages,
#     "directs" :directs,
#     "user" :user,
#     "active_directs" :active_directs,
#     }
#     return render(request,'pages/chat/privatechat.html',context)



# def chats(request):
#         getData=request.Get.get('q')
#         if(getData==None):
#             USER=request.user
#             All=User.objects.all()
#             Chats=Chat.objects.filter(Q(user1=USER) | Q(user2=USER)).order_by('-date')
#             context={"USER":USER,"chats":Chats,"users":All}  
#         else:
#             USER1=request.user
#             USER2=User.objects.get(id=getData)
#             Chats=Chat.objects.filter(Q(user1=USER1) | Q(user2=USER1) and Q(user2=USER2)| Q(user1=USER2)).exists()
#             if(Chats):
#                 Chats=Chat.objects.filter(Q(user1=USER1) | Q(user2=USER1) and Q(user2=USER2)| Q(user1=USER2)).order_by('-date')
#                 chat_id=Chats[0].id
#                 return HttpResponseRedirect('/chat/msgs/?q='+str(chat_id))
#             else:
#                 new=Chat()
#                 new.user1=USER1
#                 new.user2=USER2
#                 new.save()
#                 Chats=Chat.objects.filter(Q(user1=USER1) | Q(user2=USER1) and Q(user2=USER2)| Q(user1=USER2)).order_by('-date')
#                 chat_id=Chats[0].id
#                 return HttpResponseRedirect('/chat/msgs/?q='+str(chat_id))
#         return render(request,'pages/chat/privatechat.html',context)
