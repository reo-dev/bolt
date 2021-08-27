#-*- coding: cp949 -*-
from rest_framework import (
    viewsets,
    status,
    mixins,
)

import random
import pandas as pd
from .paginations import *
from django.core.paginator import Paginator
import math

import io
import os,uuid

from google.oauth2 import service_account
from google.cloud import vision

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

#pagenation
from .paginations import *

#django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.account.filters import *

import enum
from apps.utils import *

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import authenticate
from apps.account.models import *
from apps.log.models import *
from apps.category.models import *
from apps.kakaotalk.models import *
from .serializers import *

# 장고 메일 서버
from django.core.mail import EmailMessage

# logging
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

# signal
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

from django.db.models import F
from hashids import Hashids
from django.utils import timezone
from django.db.models import *



#elasticsearch
from elasticsearch import Elasticsearch  
import requests
import pprint
import requests
from lxml import etree
from argparse import ArgumentParser
import sys

#mail thread
from threading import Thread
import time

# 계정탈퇴시 핸드폰 번호 null값 넣을 수 없어서 해쉬화

def get_default_hash_id():
    hashids = Hashids(salt=settings.SECRET_KEY, min_length=8)
    return hashids.encode(random.choice(range(0,100)))

class ResponseCode(enum.Enum):

    SUCCESS = 0
    FAIL = 1

class UserViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(detail=False, methods=('get',), url_path='check', http_method_names=('get',))
    def email_check(self, request, *args, **kawrgs):    
        username = request.data.get('username')

        if User.objects.filter(username = username).exists() :
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'message': '이미 중복된 아이디가 있습니다.'},
                )


        


    @action(detail=False, methods=('POST',), url_path='login', http_method_names=('post',))
    def login(self, request, *args, **kawrgs):
        '''
        일반 로그인
        '''

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        ip=getIp.get(self.request.META.get('HTTP_X_FORWARDED_FOR'),self.request.META.get('REMOTE_ADDR'))
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            if ip != '0.0.0.0':
                LoginLog.objects.create(
                    ip=ip,
                    user=user,
                    type=user.type,
                )
            
            if user.type == 0:
                client = Client.objects.filter(user=user)
                return Response(data={
                                    'code': ResponseCode.SUCCESS.value,
                                    'message': '로그인에 성공하였습니다.',
                                    'data': {
                                        'token': user.auth_token.key,
                                        'User': PatchUserSerializer(user).data,
                                        'Client' : ClientSerializer(client, many=True).data,
                                    }})
            partner = Partner.objects.filter(user=user)
            return Response(data={
                                    'code': ResponseCode.SUCCESS.value,
                                    'message': '로그인에 성공하였습니다.',
                                    'data': {
                                        'token': user.auth_token.key,
                                        'User': PatchUserSerializer(user).data,
                                        'Partner' : PartnerSerializer(partner, many=True).data,
                                    }})

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': '아이디 혹은 비밀번호가 틀렸습니다.'},
        )

    @action(detail=False, methods=('POST',), url_path='data', http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def Token_data(self, request, *args, **kawrgs):
        '''
        새로고침할 때, 토큰 보내서 데이터 가지고 오기
        '''
        print(request.data)
        user = request.user
        if user.type == 0:
            client = Client.objects.filter(user=user)
            return Response(data={
                'code': ResponseCode.SUCCESS.value,
                'message': '클라이언트 데이터를 보내드립니다.',
                'data': {
                    'token': user.auth_token.key,
                    'User': PatchUserSerializer(user).data,
                    'Client': ClientSerializer(client, many=True).data,
                }})
        partner = Partner.objects.filter(user=user)
        return Response(data={
            'code': ResponseCode.SUCCESS.value,
            'message': '파트너 데이터를 보내드립니다.',
            'data': {
                'token': user.auth_token.key,
                'User': PatchUserSerializer(user).data,
                'Partner': PartnerSerializer(partner, many=True).data,
            }})


    @action(detail=False, methods=('PATCH',), url_path='deactivate', http_method_names=('patch',),  permission_classes=[IsAuthenticated], )
    def deactivate(self, request, *args, **kwargs):
        """
        회원 탈퇴
        """
        user = request.user
        password = request.data.get('password')
        if not authenticate(username=user.username, password=password):
            return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={'message': '비밀번호가 맞지 않습니다.'},
                    )
        user.is_active = False
        Snsuser.objects.filter(username=user.username).delete()
        user.username = user.username + '(deactivate_user_{})'.format(timezone.now())
        user.phone = get_default_hash_id()
        user.save()

        return Response()

    @action(detail=False, methods=['PATCH', ], url_path='password',http_method_names=('patch',), permission_classes=(IsAuthenticated,), )
    def change_password(self, request, *args, **kwargs):
        '''
        비밀번호 변경
        '''
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        user = request.user
        if user.check_password(password):
            if password == new_password:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'message': '이전과 같은 비밀번호를 입력하셨습니다.'}
                )
            user.set_password(new_password)
            user.save()
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message': '성공적으로 비밀번호를 변경하였습니다.'})
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': '기존의 비밀번호가 맞지 않습니다.', })

    @action(detail=False, methods=('POST',), url_path='password-phone', http_method_names=('post',))
    def send_password(self, request, *args, **kawrgs):
        username = request.data.get('username')
        phone = request.data.get('phone')
        user_qs = User.objects.filter(username=username, phone=phone)
        if user_qs.exists():
            user = User.objects.get(username=username, phone=phone)
            password = Util.get_random_letter(8)
            user.set_password(password)
            user.save()
            response = kakaotalk_set_temp_password.send(phone,password)
            email = EmailMessage('[볼트앤너트]회원님의 임시 비밀번호를 이메일로 보내드립니다.', '회원님의 임시 비밀번호는\n\n' + password + '\n\n입니다.', to=[user.username])
            email.send()
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message' : '임시 비밀번호가 회원님의 전화번호로 발송되었습니다.',
                                  })
        return Response( status=status.HTTP_400_BAD_REQUEST,
                         data={'message': '회원정보가 올바르지 않습니다.'}
                                  )
                                  
    @action(detail=False, methods=('POST',), url_path='findemail', http_method_names=('post',))
    def send_email(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        user_qs = User.objects.filter(phone=phone)
        list_username = []
        if user_qs.exists():
            for i in user_qs:
                list_username.append(i.username)
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message': '입력하신 휴대폰 번호로 가입된 이메일 목록입니다.',
                                  'data': list_username,
                                  })
        return Response(status=status.HTTP_400_BAD_REQUEST,
                         data={'message': '입력하신 번호로 가입 된 정보가 없습니다. 고객센터에 문의해 주세요.'}
                         )

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Client.objects.filter(user__is_active=True)
    #.order_by('-date_joined')
    serializer_class = ClientSerializer
    pagination_class = ClientPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['id']

    # @swagger_auto_schema(request_body=ClientSerializer)
    @action(detail=False, methods=('POST',), url_path='signup', http_method_names=('post',))
    def client_signup(self, request, *args, **kwargs):
        '''
        회원가입
        '''
        username = request.data.get('username')
        realName = request.data.get('realName')
        password = request.data.get('password')
        name = request.data.get('name')
        title = request.data.get('title')
        path = request.data.get('path')
        business = request.data.get('business')
        phone = request.data.get('phone')
        type = request.data.get('type')
        marketing = request.data.get('marketing')
        #type에 따라서 def(partner / client)를 api를 따로 설계
        if not username or not password:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '이메일 이나 비밀번호 값이 없습니다.'})

        if not phone:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '전화번호 값이 없습니다.'})

        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '해당 아이디가 이미 존재합니다.'})

        if User.objects.filter(phone=phone).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '해당 전화번호가 이미 존재합니다.'})

        if marketing == '1': marketing = True
        else :marketing == False

        user = User.objects.create_user(
            username=username,
            password=password,
            type=0,
            phone=phone,
            marketing=marketing,
        )

        client = Client.objects.create(
            user=user,
            realName=realName,
            name=name,
            title=title,
            path=path,
            business=business,
        )
        token, _ = Token.objects.get_or_create(user=user)

        mail_thread = Thread(target = sendEmail.send_email, args=(username,))
        mail_thread.start()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '회원가입이 성공적으로 완료되었습니다.\n다시 로그인을 해주세요.',
                              'data': {
                                     'token': user.auth_token.key,
                                     'client': ClientSerializer(client).data,
                                     'user': PatchUserSerializer(user).data,
                                     # password가 없는 데이터를 보내줘야함
                                }})


    #소셜회원가입
    @swagger_auto_schema(request_body=ClientSerializer)
    @action(detail=False, methods=('POST',), url_path='sns-signup', http_method_names=('post',))
    def sns_client_signup(self, request, *args, **kwargs):
        '''
        회원가입
        '''
        username = request.data.get('username')
        realName = request.data.get('realName')
        password = uuid.uuid4().hex
        name = request.data.get('name')
        title = request.data.get('title')
        path = request.data.get('path')
        business = request.data.get('business')
        phone = request.data.get('phone')
        type = request.data.get('type')
        marketing = request.data.get('marketing')
        # type에 따라서 def(partner / client)를 api를 따로 설계
        if not username or not password:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '이메일 이나 비밀번호 값이 없습니다.'})

        if not phone:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '전화번호 값이 없습니다.'})

        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '해당 아이디가 이미 존재합니다.'})

        if User.objects.filter(phone=phone).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '해당 전화번호가 이미 존재합니다.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            type=0,
            phone=phone,
            marketing=marketing,
        )

        client = Client.objects.create(
            user=user,
            realName=realName,
            name=name,
            title=title,
            path=path,
            business=business,
        )
        token, _ = Token.objects.get_or_create(user=user)

        Snsuser.objects.create(
            token = token,
            username = username,
            sns = 0
        )

        mail_thread = Thread(target = sendEmail.send_email, args=(username,))
        mail_thread.start()


        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '회원가입이 성공적으로 완료되었습니다.\n다시 로그인을 해주세요.',
                              'data': {
                                     'token': user.auth_token.key,
                                     'client': ClientSerializer(client).data,
                                     'user': PatchUserSerializer(user).data,
                                     # password가 없는 데이터를 보내줘야함
                                }})

    # @action(detail=False, methods=('POST',), url_path='kakaotalk_send_information', http_method_names=('post',), )
    # @receiver(post_init, sender=Request)
    # def request_init(sender, instance, **kwargs):
    #     instance._previous_send_information = instance.sendInformation

    # @receiver(post_save, sender=Request)
    # def kakao_send_information(sender, instance, **kwargs):
    #     #client = instance.client.id
    #     project = instance.project.id
    #     #client_qs = Client.objects.filter(id=client)

    #     # answer information
    #     answer_qs = Answer.objects.filter(project=project)
    #     answer_list = answer_qs.values_list('partner',flat=True)
    #     answer_list = list(answer_list)

    #     partner_qs = Partner.objects.filter(id__in=answer_list)

    #     #client_phone_list = client_qs.values_list('user__phone', flat=True)
    #     partner_phone_list = partner_qs.values_list('real_phone', flat=True)
    #     # 리스트화
    #     #client_phone_list = list(client_phone_list)
    #     partner_phone_list = list(partner_phone_list)
    #     # 공백제거
    #     #client_phone_list = list(filter(None, client_phone_list))
    #     partner_phone_list = list(filter(None, partner_phone_list))

    #     # data
    #     subject = instance.name
    #     #print(subject)
    #     # content = instance.content.replace("<p>","").replace("</p>","").replace("<br />","").replace("</br>","").replace("<br>","").replace("&nbsp;","")
    #     #if len(instance.content) != 0:
    #     #    content = instance.content.replace("<p>","").replace("</p>","")

    #     #print(content)
    #     price = instance.price
    #     #print(price)
    #     period = instance.period
    #     #print(period)
    #     file = "https://boltnnutplatform.s3.amazonaws.com/media/" + str(instance.file)
    #     #print(file)

    #     if instance.sendInformation is True and instance._previous_send_information is False:
    #         #print(client_phone_list)
    #         #print(partner_phone_list)
    #     #    response1 = kakaotalk_send_information.send(client_phone_list,subject, content, price, period, file)
    #         response2 = kakaotalk_send_information.send(partner_phone_list,subject, content, price, period, file)

    #         #Sendkakao.objects.create(
    #         #    status_code=response1.status_code,
    #         #    description=response1.json()['description'],
    #         #    refkey=response1.json()['refkey'],
    #         #    messagekey=response1.json()['messagekey'],
    #         #)
    #         Sendkakao.objects.create(
    #             status_code=response2.status_code,
    #             description=response2.json()['description'],
    #             refkey=response2.json()['refkey'],
    #             messagekey=response2.json()['messagekey'],
    #         )

    #         return Response(data={
    #             'code': ResponseCode.SUCCESS.value,
    #             'message': '발송에 성공하였습니다.',
    #             'data': {
    #                 'status_code': response2.status_code,
    #                 'response': response2.json(),
    #             }
    #         })

# ----------------------------------------------------- 사용하지 않는 API ---------------------------------------------------#
    #@action(detail=False, methods=('POST',), url_path='kakaotalk', http_method_names=('post',), )
    #def kakao_client(self, request, *args, **kwargs):  # 클라이언트한테 제안서 등록될 때 카카오톡 보내기
    #    client = request.data.get('client')
    #    client_qs = Client.objects.filter(id=client)
    #    client_phone_list = client_qs.values_list('user__phone', flat=True)
    #    print(client_qs)
    #    print(client_phone_list)
    # 리스트화
    #   client_phone_list = list(client_phone_list)
    # 공백제거
    #   client_phone_list = list(filter(None, client_phone_list))
        #print(client_phone_list)
        #response = kakaotalk_request.send(client_phone_list)
        #print(response)
        #Sendkakao.objects.create(
        #    status_code=response.status_code,
        #    description=response.json()['description'],
        #    refkey=response.json()['refkey'],
        #    messagekey=response.json()['messagekey'],
        #)
    #    return True
        #return Response(data={
        #    'code': ResponseCode.SUCCESS.value,
        #    'message': '발송에 성공하였습니다.',
        #    'data': {
        #        'status_code': response.status_code,
        #        'response': response.json(),
        #    }})


    #@action(detail=False, methods=('POST',), url_path='kakaotalk', http_method_names=('post',), )
    #@receiver(post_init, sender=Request)
    #def request_init(sender, instance, **kwargs):
    #    instance._previous_active_save = instance.active_save


    #@receiver(post_save, sender=Request)
    #def kakao_answer_end(sender, instance, **kwargs):
    #    client = instance.client.id
    #    client_qs = Client.objects.filter(id=client)
    #    client_phone_list = client_qs.values_list('user__phone', flat=True)
    #    # 리스트화
    #    client_phone_list = list(client_phone_list)
    #    # 공백제거
    #    client_phone_list = list(filter(None, client_phone_list))
    #    # print(client_phone_list)

    #    if instance.active_save is False and instance._previous_active_save is True:
    #        response = kakaotalk_request.send(client_phone_list)
    #        print(response)
    #        Sendkakao.objects.create(
    #            status_code=response.status_code,
    #            description=response.json()['description'],
    #            refkey=response.json()['refkey'],
    #            messagekey=response.json()['messagekey'],
    #        )

    #        return Response(data={
    #            'code': ResponseCode.SUCCESS.value,
    #            'message': '발송에 성공하였습니다.',
    #            'data': {
    #                'status_code': response.status_code,
    #                'response': response.json(),
    #            }})

    # 특정 Atribute를 수동으로 수정했을 때, signal을 통해서 Kakaotalk을 보내는 API 

    #@action(detail=False, methods=('POST',), url_path='kakaotalk_meeting', http_method_names=('post',), )
    #@receiver(post_init, sender=Answer)
    #def answer_init(sender, instance, **kwargs):
    #    instance._previous_send_meeting = instance.send_meeting

    #@receiver(post_save, sender=Answer)
    #def kakao_answer_meeting(sender, instance, **kwargs):
    #    client = instance.client.id
    #    partner = instance.partner.id
    #    client_qs = Client.objects.filter(id=client)
    #    partner_qs = Partner.objects.filter(id=partner)

    #    client_phone_list = client_qs.values_list('user__phone', flat=True)
    #    partner_phone_list = partner_qs.values_list('user__phone', flat=True)
    #    # 리스트화
    #    client_phone_list = list(client_phone_list)
    #    partner_phone_list = list(partner_phone_list)
    #    # 공백제거
    #    client_phone_list = list(filter(None, client_phone_list))
    #    partner_phone_list = list(filter(None, partner_phone_list))
    #    # print(client_phone_list)

    #    if instance.send_meeting is True and instance._previous_send_meeting is False:
    #        #response1 = kakaotalk_request.send(client_phone_list)
    #        #response2 = kakaotalk_request.send(partner_phone_list)


    #        #Sendkakao.objects.create(
    #        #    status_code=response1.status_code,
    #        #    description=response1.json()['description'],
    #        #    refkey=response1.json()['refkey'],
    #        #    messagekey=response1.json()['messagekey'],
    #        #)
    #        #Sendkakao.objects.create(
    #        #    status_code=response2.status_code,
    #        #    description=response2.json()['description'],
    #        #    refkey=response2.json()['refkey'],
    #        #    messagekey=response2.json()['messagekey'],
    #        #)

    #        return Response(data={
    #            'code': ResponseCode.SUCCESS.value,
    #            'message': '발송에 성공하였습니다.',
    #        #    'data': {
    #        #        'status_code': response1.status_code,
    #        #        'response': response1.json(),
    #        #    }
    #        })

# ----------------------------------------------------- 사용하지 않는 API 끝 ---------------------------------------------------#

class PartnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Partner.objects.filter(user__is_active=True).annotate(cc=Count('portfolio')).order_by('-cc')
    serializer_class = PartnerSerializer
    pagination_class = PartnerPageNumberPagination
    filter_backends = [PartnerFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'business', 'category','material','develop']
    ordering_fields = '__all__'

    #search filter
    def list(self, request, *args, **kwargs):
        #search 파라미터로 들어온 경우
        try:
            if request.query_params['search']:
                #키워드 제거
                words = ['가공','제작','압출','사출','업체','출력','정밀','제조','조립','생산','장비','영어로']
                searchQ=request.query_params['search']
                for i in words:
                    if i in request.query_params['search']:
                        searchQ=searchQ.replace(i,'')
                #공백제거
                searchQ = searchQ.rstrip().lstrip()

                #키워드 제거시 빈 문자열인 경우 키워드 제거하지 않고 검색
                if not searchQ:
                    searchQ = request.query_params['search']
                print(searchQ)
                    
                #구글 서제스트 쿼리--------------------------
                # params = {'output':'toolbar','q':searchQ}
                # res = requests.get('https://suggestqueries.google.com/complete/search',params=params)
                # root = etree.XML(res.text)
                # sugs = root.xpath('//suggestion')
                # sugstrs = [s.get('data') for s in sugs]
                # sugstring = ' '.join(sugstrs)
                # print(sugstring)

                # #연관 검색어 없는 경우 원래 검색어 사용
                # if not sugstring:
                #     sugstring=request.query_params['search']

                # #키워드 제거
                # words = ['가공','제작','압출','사출','업체','출력','정밀','제조','조립','생산','장비','영어로']
                # for i in words:
                #     if i in sugstring:
                #         sugstring=sugstring.replace(i,'')
                # #공백제거
                # sugstring = sugstring.rstrip().lstrip()
                # print(sugstring)
                #-----------------------------------------

                #엘라스틱 서치 검색
                es = Elasticsearch("http://localhost:9200", timeout=100, max_retries=10, retry_on_timeout=True)
                
                partner = es.search(
                    index='partner-1',
                    body={
                        'size':10000,
                        "query": {
                            "multi_match": {
                                "query": searchQ,
                                "fields": [
                                    "name.english_field",
                                    "name.korean_field",
                                    "info_company.english_field",
                                    "info_company.korean_field",
                                    "history.english_field",
                                    "history.korean_field",
                                    "region.english_field",
                                    "region.korean_field",
                                ]
                            }
                        }
                    })
                portfolio = es.search(
                    index='portfolio-1',
                    body={
                        'size':10000,
                        "query": {
                            "multi_match": {
                                "query": searchQ,
                                "fields": [
                                    "name.english_field",
                                    "name.korean_field"
                                ]
                            }
                        }
                    })
                
                #파트너 데이터
                partner_list = []
                for data in partner['hits']['hits']:
                    partner_list.append(data.get('_source')['id'])
                pt2=Partner.objects.filter(id__in=partner_list).annotate(cc=Count('portfolio')).order_by('-cc')
                
                #포트폴리오 데이터
                partnerId =[]
                for data in portfolio['hits']['hits']:
                    partnerId.append(data.get('_source')["partner_id"])
                pt = Partner.objects.filter(id__in=partnerId).annotate(cc=Count('portfolio')).order_by('-cc')
               
                queryset = pt|pt2

        #search 파라미터로 들어오지 않은 경우
        except:
            queryset = self.filter_queryset(self.get_queryset())

        #페이지네이션
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



    # @action(detail=False, methods=('GET',), url_path='test_file',http_method_names=('get',))
    # def test_file(self, request, *args, **kwargs):
    #     file = request.data.get('file')
    #     partner_name = request.data.get('partner_name')

    #     a = Partner.objects.filter(name=partner_name)

    #     if a.exists():
    #         get_file = Partner.objects.get(id=a[0].id)
    #         get_file.file = file
    #         get_file.save()

    #     return Response(data={'message': '해당 의뢰서에 적합한 파트너 리스트입니다.'})

    @action(detail=False, methods=('POST',), url_path='signup',http_method_names=('post',))
    def partner_signup(self, request, *args, **kwargs):
        '''
        파트너 회원가입
        '''
        username = request.data.get('username')
        realName = request.data.get('realName')
        password = request.data.get('password')
        phone = request.data.get('phone')
        type = request.data.get('type')
        marketing = request.data.get('marketing')
        name = request.data.get('name')
        title = request.data.get('title')
        
        if not phone:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '연락처 값이 없습니다.'})

        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '해당 이메일이 이미 존재합니다.'})

        if User.objects.filter(phone=phone).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '해당 전화번호가 이미 존재합니다.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            type=1,
            phone=phone,
            marketing=marketing,
        )

        partner = Partner.objects.create(
            user=user,
            realName=realName,
            name=name,
            title=title,
            idenfication_state = False,
            chat_state = True,
        )

        partner.save()
        
        mail_thread = Thread(target = sendEmail.send_email, args=(username,))
        mail_thread.start()


        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '회원가입이 성공적으로 완료되었습니다.\n다시 로그인을 해주세요.',
                              'data': {
                                  'token': user.auth_token.key,
                                  'partner': PartnerSerializer(partner).data,
                                  'user': PatchUserSerializer(user).data,
                              }})

    #소셜로그인 회원가입               
    @action(detail=False, methods=('POST',), url_path='sns-signup',http_method_names=('post',))
    def sns_partner_signup(self, request, *args, **kwargs):
        '''
        파트너 회원가입
        '''
        username = request.data.get('username')
        realName = request.data.get('realName')
        password = uuid.uuid4().hex
        phone = request.data.get('phone')
        type = request.data.get('type')
        marketing = request.data.get('marketing')
        name = request.data.get('name')
        title = request.data.get('title')
        
        if not phone:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '연락처 값이 없습니다.'})


        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '해당 이메일이 이미 존재합니다.'})

        if User.objects.filter(phone=phone).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '해당 전화번호가 이미 존재합니다.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            type=1,
            phone=phone,
            marketing=marketing,
        )

        partner = Partner.objects.create(
            user=user,
            name=name,
            title=title,
            realName=realName,
            idenfication_state = True,
            chat_state = True,
        )

        partner.save()
        
        mail_thread = Thread(target = sendEmail.send_email, args=(username,))
        mail_thread.start()


        token, _ = Token.objects.get_or_create(user=user)
        Snsuser.objects.create(
            token = token,
            username = username,
            sns = 0
        )
        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '회원가입이 성공적으로 완료되었습니다.\n다시 로그인을 해주세요.',
                              'data': {
                                  'token': user.auth_token.key,
                                  'partner': PartnerSerializer(partner).data,
                                  'user': PatchUserSerializer(user).data,
                              }})

        
    #파트너 회원가입 2페이지 - 카테고리.. 체크박스 
    @action(detail=False, methods=('POST',), url_path='signup-page2',http_method_names=('post',))
    def signup_page2(self, request, *args, **kwargs):
  
        
        partnerId = request.data.get('partnerId')

        business = request.data.get('business') # 업체 중분류
        category = request.data.get('category') # 만들제품분류
        #---
        develop = request.data.get('develop') # 공정 분류
        material = request.data.get('material') # 소재 대분류
        

        partner = Partner.objects.filter(id = partnerId).first()

 
        if business != None :
            business_elements = Business.objects.filter(id__in=business)
            partner.business.clear()
            partner.business.add(*business_elements)
   


        if category != None :
            category_elements = Category.objects.filter(id__in=category)
            partner.category.clear()
            partner.category.add(*category_elements)


        if develop != None :
            develop_elements = Develop.objects.filter(id__in=develop)
            partner.develop.clear()
            partner.develop.add(*develop_elements)


        if material != None :
            material_elements = Material.objects.filter(id__in=material)
            partner.material.clear()
            partner.material.add(*material_elements)



        partner.save()
        return Response( status=status.HTTP_200_OK, )
        
    #파트너 회원가입 3페이지 - 파트너 정보
    @action(detail=False, methods=('POST',), url_path='signup-page3',http_method_names=('post',))
    def signup_page3(self, request, *args, **kwargs):
  
        
        partnerId = request.data.get('partnerId')
        city = request.data.get('city')
        region = request.data.get('region')
        info_company = request.data.get('info_company')
    
        file = request.data.get('file')
        history = request.data.get('history')

        #portpolo
        portfolio = request.FILES.getlist('portfolio')

        #deal = request.data.get('deal')
        #resume = request.data.get('resume')

        if not partnerId:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '파트너가 없습니다.'})

        if not city:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '대분류 주소값이 없습니다.'})

        if not region:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '세부주소값이 없습니다.'})


        if not info_company:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '회사소개 값이 없습니다.'})
        

        partner = Partner.objects.filter(id = partnerId).first()

        
        #시티 확인 - 값 : 강원,서울,울산,대전,충북,충남 ... 줄임말로 옴 
        if len(city) == 2 :
            char1 = City.objects.filter(maincategory__contains = city[0])
            partner.city = char1.filter(maincategory__contains = city[1]).first()
            print(partner.city)

        partner.region = region

        partner.info_conpany = info_company

        if file :
            partner.file = file


        partner.history = history

        
        for pf in portfolio:
            print(str(pf))
            portfolio_file = Portfolio.objects.create(
                    partner = partner,
                    name = str(pf).split('.')[0],
                    img_portfolio = pf
                )

       
        partner.save()
        return Response( status=status.HTTP_200_OK,)
        
   




    # @action(detail=False, methods=('POST',), url_path='category', http_method_names=('post',))
    # # 파트너 정보와 로고만 제공하는 API
    # def partnerListByCategory(self, request, *args, **kwargs):
        
    #     # category = request.data.get('category')
    #     count = request.data.get('count')
    #     qs = Partner.objects.filter(user__is_active=True).exclude(logo ="null")
    #     # qs = PartnerCategory.objects.select_related('partner').exclude(partner__logo ="null")
    #     partnerList = PartnerCategorySerializer(qs,many=True).data
    #     partnerListSize = len(partnerList)
    #     if partnerListSize == 0:
    #         partnerList = random.sample(partnerList,partnerListSize)
    #         return Response(
    #             status=status.HTTP_406_NOT_ACCEPTABLE,
    #             data={
    #                 'message' : "have no category",
    #             }
    #         )
    #     try:
    #         partnerList = random.sample(partnerList,count)
    #         return Response(
    #             status=status.HTTP_200_OK,
    #             data={
    #                 'count' : count,
    #                 'data' : partnerList
    #             }
    #         )
    #     except ValueError:
    #         partnerList = random.sample(partnerList,partnerListSize)
    #         return Response(
    #             status=status.HTTP_200_OK,
    #             data={
    #                 'count' : partnerListSize,
    #                 'data' : partnerList
    #             }
    #         )

        

        
   

      


  
# ----------------------------------------------------- 사용하지 않는 API ---------------------------------------------------#

    # @action(detail=False, methods=('GET',), url_path='request', http_method_names=('get',))
    # def find_partner(self, request, *args, **kwargs):  # 의뢰서 완성 시에 적합한 파트너 리스트 추천
    #     subclass = request.GET['subclass']

    #    # partner1_qs = Partner.objects.filter(possible_set__id = subclass)
    #    # print(partner1_qs)
    #     partner2_qs = Partner.objects.filter(history_set__id = subclass)
    #    # print(partner2_qs)
    #     #query_set 합치기
    #    # partner_qs = partner1_qs.union(partner2_qs)

    #     return Response(data={'code': ResponseCode.SUCCESS.value,
    #                           'message': '해당 의뢰서에 적합한 파트너 리스트입니다.',
    #                           'data': PartnerSerializer(partner2_qs, many=True).data
    #                           }
    #                     )

    # @action(detail=False, methods=['PATCH', ], url_path='coin', http_method_names=('patch',), permission_classes=(IsAuthenticated,),)
    # def update_coin(self, request, *args, **kwargs):  # 코인을 결제했을 때 코인 추가
    #     # 결제 성공 시리얼을 받아서 아임포트에 요청.
    #     partner_id = request.user.partner.id
    #     #partner_id = request.data.get('partner_id')
    #     coin = request.data.get('coin')  # 프론트에서 Partner coin값을 불러와서 더하기 혹은 빼기 수행

    #     # filter로 검색 시 Queryset이 옴, get은 모델을 가져오고 없으면 예외를 발생시킴
    #     partner_data = Partner.objects.get(id=partner_id)
    #     # Serializer의 처음 파라미터에는 model(row)이 와야함.
    #     partner_data.coin += coin
    #     partner_data.save()

    #     return Response(data={'code': ResponseCode.SUCCESS.value,
    #                           'message': '코인을 업데이트한 파트너 정보입니다.',
    #                           'data': PartnerSerializer(partner_data).data
    #                           }
    #                     )

    # @action(detail=False, methods=['PATCH', ], url_path='minus-coin', http_method_names=('patch',),
    #         permission_classes=(IsAuthenticated,), )
    # def minus_coin(self, request, *args, **kwargs):  # 결제 시에 코인을 빼주는 API
    #     # 결제 성공 시리얼을 받아서 아임포트에 요청.
    #     partner_id = request.user.partner.id
    #     coin = request.data.get('coin')  # 프론트에서 Partner coin값을 불러와서 더하기 혹은 빼기 수행

    #     # filter로 검색 시 Queryset이 옴, get은 모델을 가져오고 없으면 예외를 발생시킴
    #     partner_data = Partner.objects.get(id=partner_id)
    #     # Serializer의 처음 파라미터에는 model(row)이 와야함.
    #     partner_data.coin -= coin
    #     partner_data.save()

    #     return Response(data={'code': ResponseCode.SUCCESS.value,
    #                           'message': '코인을 업데이트한 파트너 정보입니다.',
    #                           'data': PartnerSerializer(partner_data).data
    #                           }
    #                     )

    #@receiver(post_save, sender=Request)
    #def request_kakaotalk(sender, instance, *args, **kwargs):  # 검수 시 적합한 파트너에게 카카오톡 알림
    #    client = instance.client
    #    subject = instance.name
    #    subclass = instance.product
    #    category = instance.category.values_list('category')
    #    category_list = list(category)
    #    # 리스트화
    #    for i in range(len(category_list)):
    #        category_list[i] = category_list[i][0]
    #    # print(category_list)
    #    # str 화
    #    category = "/".join(category_list)
    #    # print(category)
    #    if instance.examine == True and instance._previous_examine == False:
    #        list_partner = []
    #        for i in category_list:
    #            result = Partner.objects.filter(category_middle__category__contains=i)
    #            list_partner.append(result)
    #        partner_qs1 = list_partner[0]
    #        print(list_partner)
    #        for partner in list_partner:
    #            partner_qs_all = partner_qs1.union(partner)
    #        # query_set value 가져오기
    #        partner_phone_list = partner_qs_all.values_list('user__phone', flat=True)
    #        # 리스트화
    #        partner_phone_list = list(partner_phone_list)
    #        # 공백제거
    #        partner_phone_list = list(filter(None, partner_phone_list))
    #        print(partner_phone_list)
    #        ##response = kakaotalk2.send(partner_phone_list,subject, subclass, category)

    #        client_phone = User.objects.get(username = client.user).phone

            ##kakaotalk_request_edit_end.send(client_phone)
            #response = kakaotalk2.send(['010-4112-6637'], subject, subclass, category)
            ##Sendkakao.objects.create(
            ##    status_code=response.status_code,
            ##    description=response.json()['description'],
            ##    refkey=response.json()['refkey'],
            ##    messagekey=response.json()['messagekey'],
            ##)

            ##return Response(data={
            ##    'code': ResponseCode.SUCCESS.value,
            ##    'message': '발송에 성공하였습니다.',
            ##    'data': {
            ##        'status_code': response.status_code,
            ##        'response': response.json(),
            ##    }})
    #        return True
    #    return False

    # @swagger_auto_schema(request_body=PartnerSerializer)
    # @action(detail=False, methods=('PATCH',), url_path='success', http_method_names=('patch',))
    # def meeting_success(self, request, *args, **kwargs):
    #     partner_id = request.data.get('partner_id')
    #     partner_data = Partner.objects.get(id=partner_id)
    #     # Serializer의 처음 파라미터에는 model(row)이 와야함.
    #     partner_data.success += 1
    #     partner_data.save()

    #     return Response(data={'code': ResponseCode.SUCCESS.value,
    #                           'message': '파트너 미팅 성공 횟수가 추가되었습니다.',
    #                           'data': PartnerSerializer(partner_data).data,
    #                           }
    #                     )

    # @swagger_auto_schema(request_body=PartnerSerializer)
    # @action(detail=False, methods=('PATCH',), url_path='fail', http_method_names=('patch',))
    # def meeting_fail(self, request, *args, **kwargs):
    #     partner_id = request.data.get('partner_id')
    #     partner_data = Partner.objects.get(id=partner_id)
    #     # Serializer의 처음 파라미터에는 model(row)이 와야함.
    #     partner_data.fail += 1
    #     partner_data.save()

    #     return Response(data={'code': ResponseCode.SUCCESS.value,
    #                           'message': '파트너 미팅 실패 횟수가 추가되었습니다.',
    #                           'data': PartnerSerializer(partner_data).data,
    #                           }
    #                     )

    # @swagger_auto_schema(request_body=PartnerSerializer)
    # @action(detail=False, methods=('GET',), url_path='meeting', http_method_names=('get',))
    # def meeting_percent(self, request, *args, **kwargs):
    #     partner_id = request.data.get('partner_id')
    #     partner_data = Partner.objects.get(id=partner_id)
    #     meeting_count = (partner_data.success + partner_data.fail)
    #     # Serializer의 처음 파라미터에는 model(row)이 와야함.
    #     if meeting_count == 0:
    #        if not partner_data.success == 0: # 미팅 성공이 1회 이상인 경우
    #             partner_data.meeting = 100
    #        else:                            # 미팅 성공이 0회인 경우
    #             partner_data.meeting = 0
    #     else:
    #         partner_data.meeting = partner_data.success / meeting_count

    #     partner_data.save()

    #     return Response(data={'code': ResponseCode.SUCCESS.value,
    #                           'message': '파트너의 미팅 전환 성공율 입니다.',
    #                           'data': PartnerSerializer(partner_data).data,
    #                           }
    #                     )


    # @action(detail=False, methods=('GET',), url_path='find-partner-name', http_method_names=('get',))
    # def findpartnername(self, request, *args, **kwargs):
    #     request_name = request.GET.dict()['name']
    #     partner_info = Partner.objects.all().filter(name__contains=request_name)
    #     partner_info_len = len(partner_info)

    #     paginator = Paginator(partner_info, 10)
    #     page_number = request.GET.get('page')
    #     int_pagenumber = int(page_number)
    #     page_obj = paginator.get_page(page_number)

    #     next_page_obj = int_pagenumber + 1
    #     prev_page_obj = int_pagenumber - 1

    #     total_pages = math.ceil(len(partner_info) / 10)

    #     if partner_info_len == 0:
    #         return Response(
    #             status=status.HTTP_400_BAD_REQUEST,
    #             data={
    #                 'message': '찾고 싶은 제조사 이름을 입력하세요.',
    #             }
    #         )

    #     if int_pagenumber > total_pages:
    #         return Response(
    #             status=status.HTTP_400_BAD_REQUEST,
    #             data={
    #                 'message': '페이지를 찾을 수 없습니다.',
    #             }
    #         )

    #     return Response(
    #         status=status.HTTP_200_OK,
    #         data={
    #             'count': partner_info_len,
    #             'next': f'http://52.78.182.54:8080/partner/find-partner-name/?name={request_name}&page={next_page_obj}',
    #             'previous': f'http://52.78.182.54:8080/partner/find-partner-name/?name={request_name}&page={prev_page_obj}',
    #             'current': PartnerSerializer(page_obj, many=True).data,
    #         },
    #     )

# ----------------------------------------------------- 사용하지 않는 API 끝 ---------------------------------------------------#

class PortfolioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'is_main', 'partner']

    

    
    @action(detail=False, methods=('POST',), url_path='search_file', http_method_names=('post',))
    def visiontest(self, request, *args, **kwargs):
     
        request_img = request.FILES['file']
     

        (ID_list, Score_list)= ImgSearch.file(request_img)
        

        url_list = []
        partner_list = []
        i = 0
        for img_id in ID_list :
            if(Score_list[i]>0.35):
                if Portfolio.objects.filter(id = img_id).exists() :
                    ps = Portfolio.objects.filter(id = img_id).first()
                    url_list.append("https://boltnnutplatform.s3.amazonaws.com/media/"+str(ps.img_portfolio))
                    partner_list.append(str(ps.partner.id))
                i=i+1
            else :
                del Score_list[i]
        
        

        #중복 파트너 정리
        dic = {}
        i = 0
        for url in url_list :
            dic[url] = partner_list[i]
            i+=1

        seen = []
        url_partner = dict()
        for key, val in dic.items():
            if val not in seen:
                seen.append(val)
                url_partner[key] = val

        del partner_list[:]
        del url_list[:]

        for key,val in url_partner.items() :
            partner_list.append(val)
            url_list.append(key)
        

        res=[]
        for i in partner_list:
            x=Partner.objects.get(id=i)
            res.append(PartnerSerializer(x).data)


     
        
        ip=getIp.get(self.request.META.get('HTTP_X_FORWARDED_FOR'),self.request.META.get('REMOTE_ADDR'))

        SearchImg.objects.create(
            ip = ip,
            img=request_img,
            text = str(request_img),
            count = len(res),

        )
        
    
        return Response(
                status=status.HTTP_200_OK,
                data={'img_url': url_list,
                        'partner' : res,
                },
            )
        

 


    @action(detail=False, methods=('POST',), url_path='search_url', http_method_names=('post',))
    def img(self, request, *args, **kwargs):
        url = request.data.get('url')

        (ID_list, Score_list)= ImgSearch.url(url)
        print(ID_list,Score_list)

    
        url_list = []
        partner_list = []
        i = 0
        for img_id in ID_list :
            if(Score_list[i]>0.35):
                ps = Portfolio.objects.get(id = img_id)
                url_list.append("https://boltnnutplatform.s3.amazonaws.com/media/"+str(ps.img_portfolio))
                partner_list.append(str(ps.partner.id))
                i=i+1
            else :
                del Score_list[i]
        
        
        dic = {}
        i = 0
        for url in url_list :
            dic[url] = partner_list[i]
            i+=1

        seen = []
        url_partner = dict()
        for key, val in dic.items():
            if val not in seen:
                seen.append(val)
                url_partner[key] = val

        del partner_list[:]
        del url_list[:]

        for key,val in url_partner.items() :
            partner_list.append(val)
            url_list.append(key)
        

        res=[]
        for i in partner_list:
            x=Partner.objects.get(id=i)
            res.append(PartnerSerializer(x).data)

        

        return Response(
                status=status.HTTP_200_OK,
                data={'img_url': url_list,
                        'partner' : res,
                },
            )

    
# class PathViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Path.objects.all()
#     serializer_class = PathSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['id', 'path']

class Business_ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Business_client.objects.all()
    serializer_class = Business_ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'business']

# class PartnerReviewViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = PartnerReview.objects.all()
#     serializer_class = PartnerReviewSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['id', 'score','client','partner']

class PartnerReviewViewSet(viewsets.ModelViewSet):
    queryset = PartnerReview.objects.all()
    serializer_class = PartnerReviewSerializer

    class PartnerReviewViewSet(viewsets.ModelViewSet):
        queryset = PartnerReview.objects.all()
    serializer_class = PartnerReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields =  '__all__'

    def create(self, request, *args, **kwargs):
        new_partner = request.data.get('new_partner')
        
        if str(new_partner) == '1':
            request.data._mutable = True
            request.data['partner'] = 1
            request.data._mutable = False 

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PartnerReviewTempViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = PartnerReviewTemp.objects.all()
    serializer_class = PartnerReviewTempSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'score','client','partnername']

class SnsuserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Snsuser.objects.all()
    serializer_class = SnsuserSerializer
    filter_backends = [DjangoFilterBackend]

    @action(detail=False, methods=('GET','POST'), url_path='login',http_method_names=('get','post'))
    def login(self, request, *args, **kwargs):

        sns = request.data.get('sns')
        token = request.data.get('token')
        username = request.data.get('username')
        user = User.objects.filter(username=username)
        snsuser = Snsuser.objects.filter(username=username)

        if snsuser:
            if user[0].type ==0:
                client = Client.objects.get(user=user[0])
                return Response(data={
                                'code': ResponseCode.SUCCESS.value,
                                'message': '아이디가 있습니다. 로그인 합니다.',
                                'data': {
                                    'token': user[0].auth_token.key,
                                    'User': PatchUserSerializer(user[0]).data,
                                    'Client' : ClientSerializer(client).data,
                                }})
            else:
                partner = Partner.objects.get(user=user[0])
                return Response(data={
                                'code': ResponseCode.SUCCESS.value,
                                'message': '아이디가 있습니다. 로그인 합니다.',
                                'data': {
                                    'token': user[0].auth_token.key,
                                    'User': PatchUserSerializer(user[0]).data,
                                    'Partner' : PartnerSerializer(partner).data,
                                }})
        else:
            if user:
                Snsuser.objects.create(
                    token=token,
                    sns=sns,
                    username=username,
                )
                if user[0].type ==0:
                    client = Client.objects.get(user=user[0])
                    return Response(data={
                                    'code': ResponseCode.SUCCESS.value,
                                    'message': '아이디가 있습니다. 로그인 합니다.',
                                    'data': {
                                        'token': user[0].auth_token.key,
                                        'User': PatchUserSerializer(user[0]).data,
                                        'Client' : ClientSerializer(client).data,
                                    }})
                else:
                    partner = Partner.objects.get(user=user[0])
                    print(partner)
                    return Response(data={
                                    'code': ResponseCode.SUCCESS.value,
                                    'message': '아이디가 있습니다. 로그인 합니다.',
                                    'data': {
                                        'token': user[0].auth_token.key,
                                        'User': PatchUserSerializer(user[0]).data,
                                        'Partner' : PartnerSerializer(partner).data,
                                    }})
            else:
                # 에러 메세지 제공
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'message': '아이디가 없습니다. 회원가입 합니다.'}
                )

#본섭 추가
class BookmarkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','client','bookmark_partner']

    @action(detail=False, methods=('POST',), url_path='add', http_method_names=('post',))
    def bookmark_add(self, request, *args, **kwargs):
        clientID = request.data.get('clientID')
        partnerID = request.data.get('partnerID')

        if(clientID != '20') :
            c = Client.objects.get(id = clientID )
            p = Partner.objects.get(id = partnerID)
            
            if Bookmark.objects.filter(client = c, bookmark_partner = p).exists()  :
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'message': '해당 파트너가 이미 관심기업으로 추가 되어있습니다.'},
                )

            else : 
                Bookmark.objects.create(client = c, bookmark_partner = p)
                return Response(
                        status=status.HTTP_201_CREATED,
                        data={'message': '해당 파트너 관심기업 추가 성공'},
                    )
        else : 
            return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'message': '먼저 클라이언트로 로그인 해주세요'},
            )

    
    @action(detail=False, methods=('GET',), url_path='exist', http_method_names=('get',))
    def bookmark_exist(self, request, *args, **kwargs):
        clientID = request.GET['clientID']
        partnerID = request.GET['partnerID']
        if(clientID != '20' ):
            c = Client.objects.filter(id = clientID ).first()
            p = Partner.objects.filter(id = partnerID).first()
            
            if Bookmark.objects.filter(client = c, bookmark_partner = p).exists()  :
                return Response(
                    data={'data': '1'},
                )

            else : 
                return Response(
                        data={'data': '0'},
                    )

        else : 
            return Response(
                    data={'data': '0'},
                )



    @action(detail=False, methods=('GET',), url_path='partner', http_method_names=('get',))
    def bookmark_partner(self, request, *args, **kwargs):
        partnerID = request.GET['partnerID']

        p = Partner.objects.get(id = partnerID)
        
        if Bookmark.objects.filter(bookmark_partner = p).exists()  :
            
            count_client = Bookmark.objects.filter(bookmark_partner = p).count()
            return Response(
                data={'count': count_client},
            )

        else : 
            return Response(
                    data={'count': 0},
                )
    


    @action(detail=False, methods=('DELETE',), url_path='sub', http_method_names=('delete',))
    def bookmark_sub(self, request, *args, **kwargs):
        clientID = request.data.get('clientID')
        partnerID = request.data.get('partnerID')
        
        if(clientID != '20' ):
            c = Client.objects.get(id = clientID )
            p = Partner.objects.get(id = partnerID)
            
            if Bookmark.objects.filter(client = c, bookmark_partner = p).exists() :
                Bookmark.objects.filter(client = c, bookmark_partner = p).delete()
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={'message': '해당 파트너가 관심기업에서 제거되었습니다.'},
                )

            else : 
                return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={'message': '해당 파트너가 이미 관심기업에서 제거되었습니다.'},
                    )
        else : 
            return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'message': '먼저 클라이언트로 로그인 해주세요'},
            )

    @action(detail=False, methods=('GET',), url_path='client', http_method_names=('get',),)
    def getclient_bookmark(self, request, *args, **kwargs):
        clientID = request.GET['clientID']

        if(clientID != '20' ):
            requestClient = Client.objects.get(id = clientID)


            mark = Bookmark.objects.filter(client = requestClient)
            

            # 쿼리셋을 페이지네이션 해서 받고싶은만큼 나눈다.
            page = self.paginate_queryset(mark)
            if page is not None:
                # 페이지별로 시리얼라이저를 받아온다
                serializer = self.get_serializer(page,many=True)
                response = self.get_paginated_response(serializer.data)
                # 페이지별로 리스폰스를 나눠준다.
                return response
            
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return response



# class CsvFileuploadViewSet(viewsets.ModelViewSet):
#     queryset = CsvFileUpload.objects.all()
#     serializer_class = CsvFileuploadSerializer

#     @action(detail=False, methods=('POST',), url_path='csvfile_upload', http_method_names=('post',))
#     def fileupload(self, request, *args, **kwargs):

#         partner_info_file = request.data.get('partner_info_file') # 제조사 정보 엑셀파일
#         portfolio_file = request.data.getlist('portfolio_file') # 회사소개서 파일(ppt or pdf)
#         logo = request.data.get('logo')
        
#         csv_file = pd.read_csv(partner_info_file, error_bad_lines=False)
#         csv_file_values = csv_file.values
#         count = 70000
        
#         for row in csv_file_values:
#             # print(row)
#             count += 1
#             # print('저장 중',row[7])
#             city_name = City.objects.get(city = row[7])
#             category_middle_list = row[9].split(',')

#             # init
#             partner_file = []
#             # file exist
#             for pf in portfolio_file:
#                 if str(pf) == f'{row[4]}.pptx' or str(pf) == f'{row[4]}.pdf':
#                     partner_file = pf
            
#             if partner_file != []:
#                 user = User.objects.create(
#                     username = f'boltnnut{count}' + '@boltnnut.com',
#                     password = '1234',
#                     phone = row[1],
#                     type = 1,
#                 )
                
#                 partner = Partner.objects.create(
#                     user = user,
#                     name = row[4],
#                     city = city_name,
#                     info_company = row[0],
#                     history = row[3],
#                     file = partner_file,
#                     logo = logo
#                 )
                
#                 for el in category_middle_list:
#                     develop_name = Develop.objects.filter(category = el)
#                     partner.category_middle.add(*develop_name)
#                     partner.save()
            
#         return Response(data={'message': "Successfully saving {0} partner information.".format(len(csv_file_values))})