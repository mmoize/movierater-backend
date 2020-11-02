from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer


# User Login / Sign up the class customAuthToken, receives two fields for password and username
# data get serialized and pass back a user instance which a token is created on 
class CustomAuthTokenSignup(ObtainAuthToken):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
                                           
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data
        user_id = serializer.data['id']
        user_intance = User.objects.get(id=user_id)
        token, created = Token.objects.get_or_create(user=user_intance)
        return Response({
            'token': token.key,
            'user_id': user_intance.id,
        })


# class for Login
class CustomAuthTokenLogin(ObtainAuthToken):
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        print('username', request.data)
        user = User.objects.get(username = request.data['username'])
        profile = Profile.objects.get(user=user)   
        serializer = self.serializer_class(profile) 

        token, created = Token.objects.get_or_create(user=user)
        user_profile = serializer.data
        return Response({
            'token': token.key,
            'user_id': user.id,
            'user': user_profile
        })
