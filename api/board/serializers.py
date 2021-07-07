from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.board.models import *

class MagazineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazine
        fields = ['id', 'title', 'content','category', 'image', 'is_top', 'created_at', 'summary']

class MagazineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazine_Category
        fields = ['id', 'category']