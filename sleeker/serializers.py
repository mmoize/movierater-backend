from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Sleeker
from rest_framework.authtoken.models import Token




class SleekerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sleeker
        fields = '__all__'
    

