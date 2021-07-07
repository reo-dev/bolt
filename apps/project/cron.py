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
        print("����ð�",timezone.localtime())
        print("currentDatetime : ", currentDatetime)
        print("yesterDatetime : ", yesterDatetime)
        print("--------------------------------------------")
        qs = Request.objects.filter(createdAt__gte = yesterDatetime , createdAt__lt = currentDatetime).exclude(proposal__proposalType = 17)
        print(qs)
        for obj in qs:
            print("----------------�Ƿ�----------------------")
            print("Ŭ���̾�Ʈ : ",obj.client)
            print("������Ʈ �ð� : ", obj.createdAt)
            print("Ŭ���̾�Ʈ ���� : ",obj.client.user)
            print("Ŭ���̾�Ʈ ��ȭ��ȣ : ",obj.client.user.phone)
            print("�Ƿںо� ī�װ� : ",obj.product.category)
            print("�Ƿ� ���� : ",obj.name)
            result = kakaotalk_send_meeting_confirm.send(obj.client.user.phone, obj.product.category, obj.name)
            print("�޼��� �������� : ",result.content)
    except Exception as e:
        print('=' * 10)
        print('�Լ� ���� �� Exception ���� �߻�')
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
        print("����ð�",timezone.localtime())
        print("currentDatetime : ", currentDatetime)
        print("yesterDatetime : ", yesterDatetime)
        qs = Request.objects.filter(createdAt__gte = yesterDatetime , createdAt__lt = currentDatetime).filter(proposal__proposalType = 17)
        print(qs)
        for obj in qs:
            print("---------------�Ƿ�----------------------")
            print(obj)
            print("Ŭ���̾�Ʈ : ",obj.client)
            print("Ŭ���̾�Ʈ ���� : ",obj.client.user)
            print("������Ʈ �ð� : ", obj.createdAt)
            print("Ŭ���̾�Ʈ ��ȭ��ȣ : ",obj.client.user.phone)
            print("�Ƿ� ���� : ",obj.name)
            response = kakaotalk_send_request_rerequest.send(obj.client.user.phone, obj.name)
            print("�޼��� �������� : ",response.content)
    except Exception as e:
        print('=' * 10)
        print('�Լ� ���� �� Exception ���� �߻�')
        print( timezone.localtime().now() )
        print(e)
