from django.urls import path
from django.conf import settings
from dashboards.views import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
app_name = 'dashboards'

urlpatterns = [
    path('', DashboardsView.as_view(template_name = 'pages/dashboards/index.html'), name='index'),
    path('verify-account/<slug:token>', account_verify , name="account_verify" ),
    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
    
    path('signin', AuthSigninView.as_view(template_name = 'pages/auth/signin.html'), name='signin'),
    path('signup', AuthSignupView.as_view(template_name = 'pages/auth/signup.html'), name='signup'),
    path('reset-password', AuthResetPasswordView.as_view(template_name = 'pages/auth/reset-password.html'), name='reset-password'),
    path('new-password', AuthNewPasswordView.as_view(template_name = 'pages/auth/new-password.html'), name='new-password'),
    path('logout', LogoutView.as_view(), name='logout'),
]