#-*- coding: cp949 -*-
from rest_framework import (
    viewsets,
    status,
    mixins,
)

from rest_framework.decorators import action
from rest_framework.response import Response

#django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.utils import *

from .serializers import *

# models
from apps.schedule.models import *
from datetime import datetime, timedelta
import ast

class ScheduleViewSet (viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    
    @action(detail=False, methods=['GET'], url_path='getScheduleByPeriod')
    def getScheduleByPeriod (self, request, *args, **kwargs):
        startAt = request.GET['startAt']
        endAt = request.GET['endAt']
        timeWindow = float(request.GET['timeWindow'])
        startAt = datetime.strptime(startAt, '%Y-%m-%d %H:%M:%S.%f')
        endAt = datetime.strptime(endAt, '%Y-%m-%d %H:%M:%S.%f')
        
        if startAt > endAt:
            return Response(
                data = {'message': '올바르지 않은 기간입니다.'},
                status = status.HTTP_400_BAD_REQUEST 
            )
        if timeWindow < 1:
            return Response(
                data = {'message': '시간 단위는 1시간 이상 부터 가능합니다.'},
                status = status.HTTP_400_BAD_REQUEST 
            )
        timeWindow = timedelta( hours = int(timeWindow) )
        

        timeCache = set()
        result = []
        
        
        scheduleCache = Schedule.objects.filter(startAt__gte = startAt, endAt__lte = endAt)
        for schedule in scheduleCache:
            scheduleSerialized = ScheduleSerializer(schedule).data 
            
            startAtCache = datetime.strptime(scheduleSerialized['startAt'][:-6], '%Y-%m-%dT%H:%M:%S')
            endAtCache = datetime.strptime(scheduleSerialized['endAt'][:-6], '%Y-%m-%dT%H:%M:%S')
            
            period = (endAtCache - startAtCache).total_seconds()/3600

            for hourCount in range(int(period)):
                timeCache.add(startAtCache + timedelta(hours = hourCount))


        return Response(
            data = { 'data': timeCache},
            status = status.HTTP_200_OK
            
        )

    def create(self, request, *args, **kwargs):
        requestId = request.data.get('request')
        startAt = request.data.get('startAt')
        endAt = request.data.get('endAt')
        note = request.data.get('note')
        email = request.data.get('email')
        isOnline = request.data.get('isOnline')
        marketing = request.data.get('marketing')

        flag = False
        clientCache = None

        requestCache = None
        scheduleCache = None    

        startAt = datetime.strptime(startAt, '%Y-%m-%d %H:%M:%S.%f')
        endAt = datetime.strptime(endAt, '%Y-%m-%d %H:%M:%S.%f')

        try:
            if requestId:
                requestCache = Request.objects.get(id = requestId)

            if startAt > endAt:
                return Response(
                    data = {'message': '올바르지 않은 기간입니다.'},
                    status = status.HTTP_400_BAD_REQUEST
                )

            if datetime.now() > startAt:
                return Response(
                    data = {'message': '이미 지나간 시각입니다.'},
                    status = status.HTTP_400_BAD_REQUEST
                )

            scheduleCache = Schedule.objects.filter(startAt__gte = startAt, endAt__lte = endAt)
            if scheduleCache:
                return Response(
                    data = {'message': '해당 기간에 스케쥴이 존재합니다.'},
                    status = status.HTTP_400_BAD_REQUEST
                )

            schedule = Schedule.objects.create(
                request = requestCache if requestCache else None,
                startAt = startAt,
                endAt = endAt,
                note = note,
                status = flag,
                isOnline = isOnline
            )
            requestCache.project.progressStep = '상담신청'
            requestCache.project.save()
            
            if email:
                clientCache = Client.objects.get(id = requestCache.client_id)
                if marketing == False:
                  clientCache.user.marketing = False
                  clientCache.user.save()
                clientCache.email = email
                clientCache.save()     
        
        except Request.DoesNotExist: 
            return Response(
                data = {
                    'message': "의뢰서가 존재하지 않습니다."    
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        except Client.DoesNotExist: 
            return Response(
                data = {
                    'message': "client를 찾을 수 없습니다."    
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                data = {
                    'message': '올바르지 않은 request입니다.'
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        if request:
            clientCache = Client.objects.get(id = requestCache.client_id)
            meetAt = str(startAt.year) + '년 ' + str(startAt.month) + '월 ' + str(startAt.day) + '일 ' + str(startAt.hour) + '시 ' + str(startAt.minute) + '분' 
            result = kakaotalk_send_meetin_content.send(requestCache.name, meetAt, isOnline, clientCache.user.phone)
            result_data = ast.literal_eval( result.content.decode('utf-8') )
            
            if result_data['code'] != 1000:
                return Response(
                    data = { 
                        'message': '카톡전송에 실패했습니다. ' + '코드: ' + str(result_data['code']) + ' 원인: ' + result_data['description'],
                        'data': ScheduleSerializer(schedule).data
                     },
                    status = status.HTTP_503_SERVICE_UNAVAILABLE
                )
        

        return Response(
            data = { 'data': ScheduleSerializer(schedule).data },
            status =status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['GET'], url_path='getNotAvailableDays')
    def getNotAvailableDays (self, request, *args, **kwargs):
        try:
            startAt = request.GET['startAt']
            endAt = request.GET['endAt']
            startAt = datetime.strptime(startAt, '%Y-%m-%d %H:%M:%S.%f')
            endAt = datetime.strptime(endAt, '%Y-%m-%d %H:%M:%S.%f')
            days = (endAt - startAt).days
            notAvailableDays = []


            # 해당 영업시간에 스케쥴이 꽉찼는지 확인
            for day in range (days + 1): #한달 중 하루하루 씩 확인
                date = startAt + timedelta(days = day)
                
                startAtCache = "{year}-{month}-{date} 10:00:00.000000".format(year = date.year, month = date.month, date = date.day)
                endAtCache = "{year}-{month}-{date} 19:00:00.000000".format(year = date.year, month = date.month, date = date.day)

                scheduleCache = Schedule.objects.filter(startAt__gte = startAtCache, endAt__lte = endAtCache)
                
                timeCache = set()
                
                for schedule in scheduleCache:#해당 날짜 스케쥴 모두 반복
                    scheduleSerialized = ScheduleSerializer(schedule).data 

                    tempStartAt = datetime.strptime(scheduleSerialized['startAt'][:-6], '%Y-%m-%dT%H:%M:%S')#스케쥴 시작 시각
                    tempEndAt = datetime.strptime(scheduleSerialized['endAt'][:-6], '%Y-%m-%dT%H:%M:%S')#스케쥴 끝나는 시각

                    period = (tempEndAt - tempStartAt).total_seconds()/3600 #스케쥴 몇시간인지 구함
                    
                    for hourCount in range(int(period)): #10시부터 19시 까지 확인 
                        tempSchedule = tempStartAt + timedelta(hours = hourCount)
                        if not (int(tempSchedule.hour) >= 12 and int(tempSchedule.hour) < 13): #점심시간 제외
                            timeCache.add(tempSchedule)
                
                if len(timeCache) >= 8:
                    notAvailableDays.append( (startAt + timedelta(days = day)).date())
            return Response(
                data = { 'data': notAvailableDays},
                status = status.HTTP_200_OK
            )    
        except ValueError as e:
            return Response(
                data = { 'message': e },
                status = status.HTTP_400_BAD_REQUEST 
            )
        except Exception as e:
            return Response(
                data = { 'message': e },
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            






        



