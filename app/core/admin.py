from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    '''Define admin pages for user'''
    ordering=['id']
    list_display=['email','name']

#'UserAdmin' should mention to take the changes done above
admin.site.register(models.User,UserAdmin)