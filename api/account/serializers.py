#-*- coding: cp949 -*-
from rest_framework import serializers
from apps.account.models import *
from apps.project.models import *
from apps.log.models import *
from api.project.serializers import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'type', 'password', 'is_update','phone','marketing']

class PatchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'type','phone','marketing']

class ClientSerializer(serializers.ModelSerializer):

    user = PatchUserSerializer()
    class Meta:
        model = Client
        fields = ['user','id','title','name','realName','department']

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id','partner','img_portfolio','is_main']


class PathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        fields = ['id','path']

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id','business']
        
class PartnerSerializer(serializers.ModelSerializer):
    # 사용하는 method들 | def 순서대로 안하면 error 발생함
    count_loginlog = serializers.SerializerMethodField()

    # User 객체를 가지고 오는 방법
    user = PatchUserSerializer()
    answer_set = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Partner
        fields = ['user','id', 'name', 'logo','city', 'info_company', 'deal' , 'history', 'category_middle','file','resume', 'count_loginlog','real_phone','answer_set']

    def get_count_loginlog(self, obj):
        loginlog_qs = LoginLog.objects.filter(user=obj.user)
        if loginlog_qs.exists():
            return loginlog_qs.count()
        return 0   

class PartnerReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartnerReview
        fields = ['id','partner','client','score','content'] 
        
class PartnerReviewTempSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartnerReviewTemp
        fields = ['id','partnername','client','score','content'] 


class CsvFileuploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvFileUpload
        fields = '__all__'
