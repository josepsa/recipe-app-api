from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    serializer_class=UserSerializer

    