from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    '''Define admin pages for user.
    Fields are defined to override default user model-to ignore username
    '''
    ordering=['id']
    list_display=['email','name']
    #for modify user page
    fieldsets=(
        (None,{'fields':('email','password')}),
        (
            _('permissions'),
            {
                'fields':(
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'),{'fields':('last_login',)}),
    )
    readonly_fields=['last_login']
    #for add user page
    add_fieldsets=(
        (None,{
            # 'classes':('wide',),
            'fields':(
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )

#'UserAdmin' should mention to take the changes done above
admin.site.register(models.User,UserAdmin)