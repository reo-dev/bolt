from rest_framework import serializers
from apps.log.models import *

class ClickLogSerializer (serializers.ModelSerializer):
    class Meta:
        model = clickLog
        fields = ['id', 'client', 'search','partner','created_at']



class ChatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Chat
        fields = '__all__'


class LoginLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = ['id']

class SearchTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchText
        fields = ['id','text','created_at'] 