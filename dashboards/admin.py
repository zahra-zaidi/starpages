from django.contrib import admin
from .models import *
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    model=Profile
    list_display=('id', 'token', 'user', 'verify')


admin.site.register(Profile , ProfileAdmin)
