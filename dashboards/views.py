from django.views.generic import TemplateView ,View ,RedirectView
from django.views import generic
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import resolve
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from .form import SignUpForm , SignInForm
from .models import Profile
import uuid
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import re
"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""

class DashboardsView(LoginRequiredMixin, TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'pages/dashboards/index.html'
   


    # Predefined function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        """
        # Example to get page name. Refer to dashboards/urls.py file.
        url_name = resolve(self.request.path_info).url_name

        if url_name == 'dashboard-2':
            # Example to override settings at the runtime
            settings.KT_THEME_DIRECTION = 'rtl'
        else:
            settings.KT_THEME_DIRECTION = 'ltr'
        """

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])

        return context

class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)
    

class AuthNewPasswordView(TemplateView):
    template_name = 'pages/auth/new-password.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/reset-password/new-password.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context



class AuthResetPasswordView(TemplateView):
    template_name = 'pages/auth/reset-password.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/reset-password/reset-password.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context

class AuthSigninView(TemplateView):
    template_name = 'pages/auth/signin.html'

    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        fm= SignInForm()
        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')
        
        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
            'form': fm
        })

        return context


    

    def post(self,request):
        fm= SignInForm(request , data=request.POST)
  
        if fm.is_valid():
            username=fm.cleaned_data['username']
            password=fm.cleaned_data['password']
            user=authenticate(username=username , password=password)
            try:
                pro_user=Profile.objects.get(user=user)
                if pro_user.verify:
                    print('ok')
                    login(request, user)
                    return redirect('/')
                else:
                    messages.info(request , "Please Check your email to verify your Account")
                    return redirect('/signin')
            except:
                messages.info(request,"Your Account is not Verified")
                return redirect('/signin')
        else:
             return render(request, self.template_name, { 'layout': KTTheme.setLayout('auth.html'),'form':fm})
            # for field,errors in fm.errors.items():
            #     messages.success(request,errors,extra_tags='danger')
            # return redirect('/signin')
        
        

            

        



def send_email_after_registration(email ,  token):
    subject="Verify Email"
    message= f"Hy Click on the link to verify http://127.0.0.1:8080/verify-account/{token}"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]

    send_mail(subject=subject , message=message , from_email=from_email, recipient_list=recipient_list)



class AuthSignupView(TemplateView):

    template_name = 'pages/auth/signup.html'

    def get_context_data(self, **kwargs):

        fm= SignUpForm()
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/sign-up/general.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
            'form': fm ,
           

        })

        return context
    





    def post(self,request,*args,**kwargs ):
       
        fm= SignUpForm(request.POST)
        # form=SignUpForm()
        if request.method == 'POST':

            PostData=request.POST.copy()
            username=PostData['username']
            email=PostData['email']
            password=PostData['password1']
            # confirmPassword=PostData['confirmpassword']

            if fm.is_valid():

                    new_user=User.objects.create_user(username=username , email=email , password=password)
                    new_user.save() 
                    uid=uuid.uuid4()
                    pro_obj=Profile(user=new_user, token=uid)
                    pro_obj.save()
                    send_email_after_registration(new_user.email , uid)
                    messages.success(request , "Check your mail to verify your account")
                    return redirect ("/signup")
            
            else:
                # for field,errors in fm.errors.items():
                #     messages.success(request,errors,extra_tags='danger')
                return render(request, self.template_name, { 'layout': KTTheme.setLayout('auth.html'),'form':fm})
                # for field,errors in fm.errors.items():
                #     messages.success(request,errors,extra_tags='danger')
                # return redirect('/signup')
            


def account_verify(request , token):
    pro_token=Profile.objects.filter(token=token).first()
    print(pro_token)
    pro_token.verify = True
    pro_token.save()
    messages.success(request , " Now you Can Login")
    return redirect('/signup')


