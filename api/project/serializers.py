from rest_framework import serializers
from apps.project.models import *
from apps.estimate.models import *
from api.estimate.serializers import *

import json
from django.forms.models import model_to_dict

from django.utils import timezone
from datetime import date

now = timezone.localtime()

class RequestFileSerializer(serializers.ModelSerializer): 

    class Meta:
        model = RequestFile
        fields = ['id', 'request', 'file', 'share_inform']

class RequestSerializer(serializers.ModelSerializer):
    estimate_set = EstimateSerializer(many=True, read_only=True)
    requestfile_set = RequestFileSerializer(many=True, read_only=True)
    class Meta:
        model = Request
        fields = ['id', 'client','request_state', 'name', 'deadline', 'deadline_state', 'order_request_open', 'order_request_close','price', 'createdAt','estimate_set','requestfile_set']
        read_only_fields = ['client','project']

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
