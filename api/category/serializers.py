from django.contrib.auth.models import Group
from rest_framework import serializers
from apps.category.models import *
from apps.project.models import *
from api.project.serializers import *

class SubclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subclass
        fields = ['maincategory','category','id']

class CategorySerializer(serializers.ModelSerializer):
    subclass_set = SubclassSerializer(many=True)
    class Meta:
        model = Category
        fields = ['maincategory', 'id','category', 'middle_img','subclass_set']

class MaincategorySerializer(serializers.ModelSerializer):
    category_set = CategorySerializer(many=True)
    class Meta:
        model = Maincategory
        fields = ['id', 'maincategory', 'big_img', 'category_set']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city']

class DevelopSerializer(serializers.ModelSerializer):
    select_set = SelectSerializer(many=True)
    class Meta:
        model = Develop
        fields = ['id','maincategory', 'category', 'coin', 'select_set']

class DevelopbigSerializer(serializers.ModelSerializer):
    develop_set = DevelopSerializer(many=True)
    class Meta:
        model = Developbig
        fields = ['id','maincategory', 'maincategory_img', 'develop_set']
        
class justDevelopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Develop
        fields = ['category']

class justSubclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subclass
        fields = ['subclass']