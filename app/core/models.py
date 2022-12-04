from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    #contains functionalities for authntication
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
 #inheriting from Baseusermanager class, function name should be correct
class UserManager(BaseUserManager):
    '''Manager for users'''
    #passing kwargs for extra fields during user creation
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        #normalize will convert email id to lower case
        user=self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        # it is used if multiple dbs are used, it is best practice to use it
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    '''Custom user'''
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    #assigning usermanager to custome user model
    objects=UserManager()
    #overriding the default username field to email
    USERNAME_FIELD='email'
