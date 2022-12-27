from django.urls import path
from user import views

#this name will be used by reverse lookup
app_name='user'

urlpatterns = [
    #name is used by reverse lookup
    path('create/',views.CreateUserView.as_view(),name='create'),
]
