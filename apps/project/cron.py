from django.utils import timezone

from .models import KakaoToken
from .models import Request

from ..utils import kakaotalk_send_meeting_confirm,kakaotalk_send_request_rerequest

import requests
import json
from datetime import datetime, timedelta, time
import ast

def getToken():
    url = 'https://api.bizppurio.com/v1/token'
    headers = {
        'Content-type': 'application/json;charset=utf-8', 
        'Accept': 'text/plain', 
        'Authorization':'Basic Ym9sdG5udXRfa29yZWE6QGJvbHQxMjM='
    }
    response = requests.post(url, headers=headers)
    response = json.loads(response.content)
    token = response['accesstoken']
    tokenType = response['type']
    basicAccessToken = tokenType + " " + token
    data = KakaoToken.objects.get()
    data.token = basicAccessToken
    data.save()

def sendKakaotalkAfterMeetingConfirmX():
    try:
        currentDate = timezone.localtime().date()
        yesterDate = currentDate + timedelta(days=-1)
        standardTime = time(9,0)
        currentDatetime = datetime.combine(currentDate, standardTime )
        yesterDatetime = datetime.combine(yesterDate, standardTime )
        print("--------------sendKakaotalkAfterMeetingConfirmX-----------------------")
        print("현재시각",timezone.localtime())
        print("currentDatetime : ", currentDatetime)
        print("yesterDatetime : ", yesterDatetime)
        print("--------------------------------------------")
        qs = Request.objects.filter(createdAt__gte = yesterDatetime , createdAt__lt = currentDatetime).exclude(proposal__proposalType = 17)
        print(qs)
        for obj in qs:
            print("----------------의뢰----------------------")
            print("클라이언트 : ",obj.client)
            print("오브젝트 시간 : ", obj.createdAt)
            print("클라이언트 유저 : ",obj.client.user)
            print("클라이언트 전화번호 : ",obj.client.user.phone)
            print("의뢰분야 카테고리 : ",obj.product.category)
            print("의뢰 제목 : ",obj.name)
            result = kakaotalk_send_meeting_confirm.send(obj.client.user.phone, obj.product.category, obj.name)
            print("메세지 리스폰스 : ",result.content)
    except Exception as e:
        print('=' * 10)
        print('함수 실행 중 Exception 에러 발생')
        print( timezone.localtime().now() )
        print(e)

def sendKakaotalkAfterMeetingConfirmXBasicInfo():
    try:
        currentDate = timezone.localtime().date()
        yesterDate = currentDate + timedelta(days=-1)
        standardTime = time(9,0)
        currentDatetime = datetime.combine(currentDate, standardTime )
        yesterDatetime = datetime.combine(yesterDate, standardTime )
        print("--------------sendKakaotalkAfterMeetingConfirmXBasicInfo-----------------------")
        print("현재시각",timezone.localtime())
        print("currentDatetime : ", currentDatetime)
        print("yesterDatetime : ", yesterDatetime)
        qs = Request.objects.filter(createdAt__gte = yesterDatetime , createdAt__lt = currentDatetime).filter(proposal__proposalType = 17)
        print(qs)
        for obj in qs:
            print("---------------의뢰----------------------")
            print(obj)
            print("클라이언트 : ",obj.client)
            print("클라이언트 유저 : ",obj.client.user)
            print("오브젝트 시간 : ", obj.createdAt)
            print("클라이언트 전화번호 : ",obj.client.user.phone)
            print("의뢰 제목 : ",obj.name)
            response = kakaotalk_send_request_rerequest.send(obj.client.user.phone, obj.name)
            print("메세지 리스폰스 : ",response.content)
    except Exception as e:
        print('=' * 10)
        print('함수 실행 중 Exception 에러 발생')
        print( timezone.localtime().now() )
        print(e)
