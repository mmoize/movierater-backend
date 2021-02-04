  
from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Profile
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # user_info = user
        # print('this is user', user_info)
        # userToken = Token.objects.get_or_create(user=user)
        
        # data ={}
        # data['user'] = user
        # data['userToken'] = userToken

        # print('from serializer', data)
        return user




class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'