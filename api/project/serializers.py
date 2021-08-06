#-*- coding: cp949 -*-
from rest_framework import serializers
from rest_framework.fields import ChoiceField
from apps.project.models import *
from apps.estimate.models import *
from api.estimate.serializers import *

from apps.category.models import *
from api.category.serializers import *

import json


from django.utils import timezone
from datetime import date

from django.contrib.auth import get_user_model


# choices 필드의 value를 출력해주는 함수, 
# #만약 choise필드의 key가 string이였다면 예외처리포함
User = get_user_model()
class ChoicesField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        try : 
            re = self._choices[int(obj)]

        except Exception as e: 
            re =  obj
        return re

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)

class Field(serializers.ModelSerializer):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return '전체'
                
        return obj

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


now = timezone.localtime()

class RequestFileSerializer(serializers.ModelSerializer): 

    class Meta:
        model = RequestFile
        fields = ['id', 'request', 'file', 'share_inform']

class RequestInfoSerializer(serializers.ModelSerializer): 

    class Meta:
        model = RequestInfo
        fields = ['id', 'client','email','phone','price','title','classified','category_middle']


class RequestSerializer(serializers.ModelSerializer):
    #serializer
    estimate_set = EstimateSerializer(many=True, read_only=True)
    requestfile_set = RequestFileSerializer(many=True, read_only=True)
    

    #choices set 
    price = ChoicesField(choices = Request.prices)
    deadline_state = ChoicesField(choices = Request.deadline_states)
    request_state = ChoicesField(choices = Request.request_states)
    

    class Meta:
        model = Request
        fields = ['id', 'client','request_state', 'name', 'deadline', 'deadline_state', 'contents','price', 'createdAt','category','region','estimate_set','requestfile_set']
        read_only_fields = ['client','project']

    #ForeignKey가 NULL일때 예외처리
    def to_representation(self, obj):
        # get representation from ModelSerializer
        ret = super(RequestSerializer, self).to_representation(obj)
        # if parent is None, overwrite
        if not ret.get("category", None):
            ret["category"] = '전체'
        else : 
            ret["category"] = str(obj.category)

        if not ret.get("region", None):
            ret["region"] = '전국'
        else : 
            ret["region"] = str(obj.region)
        

        return ret



class ContentSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Content
        fields = ['id', 'request', 'content1', 'content2', 'content3', 'content4']

class SelectSerializer(serializers.ModelSerializer):
    content_set = ContentSerializer(many=True)
    class Meta:
        model = Select
        fields = ['id', 'category', 'request', 'content_set']

class Select_saveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Select_save
        fields = ['id', 'category', 'request', 'question', 'answer']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['createdAt', 'id', 'project', 'partner', 'request','content1','content2','content3','check_time_client','check_time_partner','share_inform']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'project','isMain','title','content','createdAt']
        read_only_fields = ['isMain','createdAt']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'client','project','content','createdAt']

class ProjectSerializer(serializers.ModelSerializer):
    request_set = RequestSerializer(many=True, read_only=True)
    answer_set = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id','title','status','request_set','answer_set','progressStep']
        read_only_fields = ['review_set']
