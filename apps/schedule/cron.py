from django.utils import timezone

from .models import *
from apps.project.models import *

from ..utils import kakaotalk_send_request_review, kakaotalk_send_meetin_content, kakaotalk_send_appreciate

import requests
import json
from api.schedule.serializers import *
from datetime import datetime, timedelta, time
import ast

def sendKakaotalkSendAppreciate():
    try:
        currentDate = timezone.localtime().date()
        beforeTwoWeekDate = currentDate + timedelta(days=-14)
        beforeTwoWeekDate2 = currentDate + timedelta(days=-13)
        standardTime = time(9,0)
        beforeTwoWeekDatetime = datetime.combine(beforeTwoWeekDate, standardTime )
        beforeTwoWeekDatetime2 = datetime.combine(beforeTwoWeekDate2, standardTime )
        print("-------------------sendKakaotalkSendAppreciate------------------------")
        print("����ð�",timezone.localtime())
        print("beforeTwoWeekDate : ", beforeTwoWeekDatetime)
        print("beforeTwoWeekDate2 : ", beforeTwoWeekDatetime2)
        qs = Schedule.objects.filter(endAt__gte = beforeTwoWeekDatetime , endAt__lt = beforeTwoWeekDatetime2).exclude(status = False)
        print(qs)
        for obj in qs:
            print("------------------�Ƿ�----------------------")
            print("�����ð������� : ",obj.endAt)
            print("Ŭ���̾�Ʈ��������",obj.request.client)
            print("Ŭ���̾�Ʈ : ",obj.request.client.user)
            print("Ŭ���̾�Ʈ ��ȭ��ȣ : ",obj.request.client.user.phone)
            print("�Ƿ� ���� : ",obj.request.name)
            response = kakaotalk_send_appreciate.send(obj.request.client.user.phone, obj.request.name)
            print("�޼��� �������� : ",response.content)

    except Exception as e:
        print('=' * 10)
        print('�Լ� ���� �� Exception ���� �߻�')
        print( timezone.localtime().now() )
        print(e)


def sendKakaotalkRequestReview():
    try:
        currentDate = timezone.localtime().date()
        yesterDate = currentDate + timedelta(days=-1)
        standardTime = time(9,0)
        currentDatetime = datetime.combine(currentDate, standardTime )
        yesterDatetime = datetime.combine(yesterDate, standardTime )
        print("-------------------sendKakaotalkRequestReview------------------------")
        print("����ð�",timezone.localtime())
        print("currentDatetime : ", currentDatetime)
        print("yesterDatetime : ", yesterDatetime)
        qs = Schedule.objects.filter(endAt__gte = yesterDatetime , endAt__lt = currentDatetime).exclude(status = False)
        print(qs)
        for obj in qs:
            print("------------obj----------------------")
            print(obj)
            print(type(obj))
            print("�����ð������� : ",obj.endAt)
            print("Ŭ���̾�Ʈ : ",obj.request.client)
            print("Ŭ���̾�Ʈ ���� : ",obj.request.client.user)
            print("Ŭ���̾�Ʈ ��ȭ��ȣ : ",obj.request.client.user.phone)
            print("�Ƿ� ���� : ",obj.request.name)
            print("��Ī ������Ʈ : ",obj.request.proposal.consultant.name)
            response = kakaotalk_send_request_review.send(obj.request.client.user.phone, obj.request.proposal.consultant.name, obj.request.name)
            print("�������� �޼��� : ",response.content) 
    except Exception as e:
        print('=' * 10)
        print('�Լ� ���� �� Exception ���� �߻�')
        print( timezone.localtime().now() )
        print(e)

def send_meeting_content_daybefore ():
    try:
        currentDate = timezone.localtime().date()
        tomorrowDate = currentDate + timedelta(days = 1)
        standardTime = time(9,0)
        tomorrowStartAt = datetime.combine(tomorrowDate, time(0,0) )
        tomorrowEndAt = datetime.combine(tomorrowDate, time(23,59) )     
        ScehduleCache = Schedule.objects.filter(startAt__gte = tomorrowStartAt, endAt__lte = tomorrowEndAt, request__isnull = False)
        scheduleSerialized = ScheduleSerializer(ScehduleCache, many = True).data
        print("-------------------send_meeting_content_daybefore------------------------")
        print("����ð� : ",timezone.localtime())
        print(ScehduleCache)
        for schedule in scheduleSerialized:
            print("-----------------������------------")
            requestCache = Request.objects.get(id = schedule['request'])
            clientCache =requestCache.client
            print(clientCache.user.phone)
            # clientCache = Client.objects.get(id = requestCache.client_id)
            
            
            startAtDate = schedule['startAt'].split('T')[0]
            startAtTime = schedule['startAt'].split('T')[1]
            meetAt = startAtDate.split('-')[0] + '�� ' + startAtDate.split('-')[1] + '�� ' + startAtDate.split('-')[2] + '�� ' + startAtTime.split(':')[0] + '�� ' + startAtTime.split(':')[1] + '��' 
            result = kakaotalk_send_meetin_content.send(requestCache.name, meetAt, schedule['isOnline'], clientCache.user.phone)
            result_data = ast.literal_eval( result.content.decode('utf-8') )
            if result_data['code'] != 1000:
                print('='*10)
                print( timezone.localtime().now() )
                print('ī������ ���� ' + '�ڵ�: ' + str(result_data['code']) + ' ����: ' + result_data['description'])
                print("������Ʈ: {title}, ���� ��ȣ: {phone}, ���ýð�: {startAt}".format(title = requestCache.name, phone = clientCache.user.phone, startAt = meetAt))
                
            else:
                print('='*10)
                print( timezone.localtime().now() )
                print('ī������ ��û �Ϸ� ' + '�ڵ�: ' + str(result_data['code']) + ' ���: ' + result_data['description'])
                print("������Ʈ: {title}, ���� ��ȣ: {phone}, ���ýð�: {startAt}".format(title = requestCache.name, phone = clientCache.user.phone, startAt = meetAt))

    except Exception as e:
        print('=' * 10)
        print('�Լ� ���� �� Exception ���� �߻�')
        print( timezone.localtime().now() )
        print(e)
