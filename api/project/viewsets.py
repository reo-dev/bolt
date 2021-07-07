#-*- coding: cp949 -*-
from apps.project.models import *
from apps.category.models import *
from apps.account.models import *
from rest_framework import (
    viewsets,
    status,
    mixins,
)

from api.estimate.viewsets import *

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

#pagenation
from .paginations import *

#permission
from .permissions import *

#django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
#count
from django.db.models import Count

import enum
import random

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage

from apps.account.models import *
from apps.category.models import *
from apps.log.models import *

# filter
from apps.project.filters import RequestFilter, ProjectFilter

from .serializers import *
from api.category.serializers import *

from apps.utils import *

from string import ascii_letters, digits
symbols = ascii_letters + digits
secure_random = random.SystemRandom()

import requests
import json

from apps.project.models import *
from apps.account.models import Client,User

#kakao
from apps.utils import *


class UserDoesnotExist (Exception):
    pass
class ResponseCode(enum.Enum):

    SUCCESS = 0
    FAIL = 1


class RequestFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = RequestFile.objects.all()
    serializer_class = RequestFileSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['id', 'request', 'share_inform']


class RequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    pagination_class = RequestPageNumberPagination
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = '__all__'
    filterset_fields = ['id', 'project']

    # RequestViewset의 기본 url로 post요청이 왔을 때 제일 먼저 호출되는 함수
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # 상담 의뢰서 작성 시 저장되어야 하는 정보
    # 도면 있을 때 : 문의 목적 | 문의 제목 | 납기일 | 납기일 상태(미정 | 협의 가능) | 도면(FK) 테이블 저장 - 자동 견적 정보 | 공개 내용 | 비공개 내용 | 공개 자료 | 비공개 자료
    # 도면 없을 때 : 문의 목적 | 문의 제목 | 납기일 | 납기일 상태(미정 | 협의 가능) | 도면(FK) 테이블 저장 - 도면 정보 저장 | 공개 내용 | 비공개 내용 | 공개 자료 | 비공개 자료
    @action(detail=False, methods=('POST',), http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def perform_create(self, serializer, request):
        # Token 불러와서 유저 가지고 오기
        #rint(request.headers['Token'])
        #Token = request.headers['Authorization']
        users = request.user
        # 의뢰서 값 저장하기
        client = Client.objects.get(user=users)
        request_state = request.data.get('request_state')
        name = request.data.get('name')
        deadline = request.data.get('deadline')
        deadline_state = request.data.get('deadline_state')
        order_request_open = request.data.get('order_request_open')
        order_request_close = request.data.get('order_request_close')
        file_open = request.FILES.getlist('file_open')
        file_close = request.FILES.getlist('file_close')
        blueprint = request.FILES.getlist('blueprint')
        process = request.data.get('process')
        detailprocess = request.data.get('detailprocess')
        price = request.data.get('price')
        number = request.data.get('number')
        print('name')
        # 리스트화
        process = list(process.replace(',',''))
        detailprocess = list(detailprocess.replace(',',''))
        # number 받기 - 두 자리 이상으로 process와 detailprocess가 두 자리 이상되면 number처럼 수정 필요함
        number = list(number.split(','))
        # project 생성하기 : request 생성을 위함
        projects = Project.objects.create(
            client=client,
        )
        # jandi_webhook_project.send(name,client.user.username)
        # requst 생성하기
        requests = Request.objects.create(
            client=client,
            project=projects,
            request_state = request_state,
            name = name,
            deadline = deadline,
            deadline_state = deadline_state,
            order_request_open = order_request_open,
            order_request_close = order_request_close,
            price = price,
        )
        #print(file_open)
        for file in file_open:
            requests_file = RequestFile.objects.create(
                    request = requests,
                    file = file,
                    share_inform = True,
                )
        
                
        for file in file_close:
            requests_file = RequestFile.objects.create(
                    request = requests,
                    file = file,
                    share_inform = False,
                )

        print(requests.id)
        # 도면 있는 지 없는 지 확인
        blueprint_exist = request.data.get('blueprint_exist')
        # 도면이 있다면
        if int(blueprint_exist) == 1:
            index = 0
            for blueprint_element in blueprint:
                print(blueprint_element)
                EstimateViewSet.create(self, request, requests.id, blueprint_element, process[index], detailprocess[index], number[index])
                index = index + 1

        return Response(status = status.HTTP_200_OK,
                        data={   'code': ResponseCode.SUCCESS.value,
                                  'message': "의뢰서가 만들어졌습니다."
                                }
                        )    
                        
                        
class SelectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Select.objects.all()
    serializer_class = SelectSerializer
    filter_backends = [DjangoFilterBackend]
    # filters.SearchFilter]
    filterset_fields = ['category__id']

    # search_fields = []

    @swagger_auto_schema(request_body=SelectSerializer)
    @action(detail=False, methods=('POST',), url_path='category', http_method_names=('post',))
    def find_select(self, request, *args, **kwargs):  # 占쏙옙占시듸옙 占쏙옙占쏙옙 占싻야울옙 占쏙옙占쏙옙 占쏙옙占쏙옙占쏙옙占쏙옙 占쏙옙占쏙옙

        category = request.data.get('category')
        # product id

        develop_instances = Develop.objects.filter(id__in=category)
       # select = Select.objects.filter(range__in=product_instances)
    #    select = Select.objects.filter(range=product) # 占쏙옙 占쏙옙 占쏙옙 占쏙옙占쏙옙..?

        return Response(
            status = status.HTTP_200_OK,
            data = {
                'data': DevelopSerializer(develop_instances, many=True).data
            }
        )

class Select_saveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Select_save.objects.all()
    serializer_class = Select_saveSerializer
    filter_backends = [DjangoFilterBackend]
    # filters.SearchFilter]
    filterset_fields = ['request','category']

class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    #orderbyList = ['-partner__avg_score', '-partner__meeting','id']
    queryset = Answer.objects.all()#.order_by(*orderbyList)
    serializer_class = AnswerSerializer
    pagination_class = AnswerPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['project', 'partner']
    ordering_fields = '__all__'


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        project = request.data.get('project')
        partner = request.data.get('partner')
        answer = Project.objects.get(id=project).answer_set.values("partner")

        #파트너가 이미 제안했을 경우
        for i in answer:
            if i['partner'] == request.data.get('partner'):
                return Response(
                    status = status.HTTP_200_OK,
                    data = {
                        'data': {
                            "bExist":True
                        }
                    }
                )


        #제안하지 않았다면 데이터 저장 및 카카오톡을 클라이언트에게 보내기
        clientId = Project.objects.get(id=project).request_set.values("client")[0]['client']
        partner = Partner.objects.get(id=partner)
        userInfo = Client.objects.get(id=clientId).user
        phone = userInfo.phone
        username = userInfo.username
        title = Project.objects.get(id=project).request_set.values("name")[0]['name']

        kakaotalk_send_answer_to_client.send(phone, username, title)
        # jandi_webhook_answer.send(title,partner.user.username)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        #채팅 로그 생성
        chat = Chat.objects.create(
            text_content = serializer.data['content1'],
            answer = Answer.objects.get(id=serializer.data['id']),
            user_type = 1
        )

        #채팅 로그 생성
        chat = Chat.objects.create(
            text_content = serializer.data['content1'],
            answer = Answer.objects.get(id=serializer.data['id']),
            user_type = 1
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #채팅 카카오톡 보내기
    @action(detail=False, methods=('POST',), url_path='chat', http_method_names=('post',))
    def chat(self, request, *args, **kawrgs):
        return Response(data=kakaotalk_chat_text.send(request.data["phoneNum"],request.data["requestTitle"],request.data["name"],request.data["text"]))
    
    #파일 카카오톡 보내기
    @action(detail=False, methods=('POST',), url_path='file', http_method_names=('post',))
    def file(self, request, *args, **kawrgs):
        
        return Response(data=kakaotalk_chat_file.send('01066057996','requestTitle','partner_name','file'))
        
# ----------------------------------------------------- 사용하지 않는 API ---------------------------------------------------#

    @swagger_auto_schema(request_body=AnswerSerializer)
    @action(detail=False, methods=('POST',), url_path='first-active', http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def first_active(self, request, *args, **kwargs):  # 제일 평점 높은 파트너 활성화 > 프로젝트마다 되어야함.
            project__id = request.data.get('project__id')
            answer_qs = Answer.objects.filter(project = project__id)
            if answer_qs.exists():
                instance=answer_qs.first()
                instance.active = True
                instance.save()
                return Response(data={'code': ResponseCode.SUCCESS.value,
                                      'message' : "평점이 제일 높은 파트너가 활성화되었습니다.",
                                      'data': AnswerSerializer(answer_qs, many=True).data
                                    })
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "프로젝트에 들어온 제안서가 없습니다"
                            })

    @swagger_auto_schema(request_body=AnswerSerializer)
    @action(detail=False, methods=('PATCH',), url_path='active', http_method_names=('patch',))
    def change_active(self, request, *args, **kwargs):  # 파트너의 id를 받아서 해당 id의 파트너가 보낸 제안서의 active 값을 True로 만들어주는 API
        partner_id = request.data.get('partner_id')
        project_id = request.data.get('project_id')
        answer_qs = Answer.objects.filter(project = project_id, partner = partner_id)
        print(answer_qs)
        if answer_qs.exists():
            instance = answer_qs.first()
            instance.active = True
            instance.save()
            print(instance)
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message': "해당 파트너의 제안서가 활성화되었습니다."
                                  })
        return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "프로젝트에 들어온 제안서가 없습니다"
                            })

    @action(detail=False, methods=('PATCH',), url_path='answer_check', http_method_names=('patch',))
    def answer_check(self, request, *args, **kwargs):
        answer_click = request.data.get('answer_click')
        answer_id = request.data.get('answer_id')
        answer = Answer.objects.get(id=answer_id)

        if answer_click == 1:
            answer.info_check = 1
            answer.save()

            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message': 'answer 상태 바꿔드렸음',
                                  'data': AnswerSerializer(answer).data
                                  }
                            )

        elif answer_click == 2:
            answer.info_check = 2
            answer.save()

            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message': 'answer 상태 바꿔드렸음',
                                  'data': AnswerSerializer(answer).data
                                  }
                            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "Error 404"
                                  })
# ----------------------------------------------------- 사용하지 않는 API 끝 ---------------------------------------------------#

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    orderbyList = ['-id']
    queryset = Project.objects.all().order_by(*orderbyList)
    serializer_class = ProjectSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [ProjectIsAuthorOrReadonly]
    pagination_class = ProjectPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['request__client','request__request_state']
    ordering_fields = '__all__'
    search_fields = ['title']



# ----------------------------------------------------- 사용하지 않는 API ---------------------------------------------------#

    @swagger_auto_schema(request_body=ProjectSerializer)
    @action(detail=False, methods=['PATCH', ], url_path='state', http_method_names=('patch',))
    def change_state(self, request, *args, **kwargs):  # 버튼 클릭에 따라 프로젝트 state 상태를 바꾸는 api

        project_id = request.data.get('project_id')
        state = request.data.get('state')
        # project id

        #filter로 검색 시 Queryset이 옴, get은 모델을 가져오고 없으면 예외를 발생시킴
        update_project = Project.objects.get(id=project_id)
        # Serializer의 처음 파라미터에는 model(row)이 와야함.
        serializer = ProjectSerializer(update_project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'data': ProjectSerializer(update_project).data
                              })
    
    # 해당 클라이언트의 프로젝트리스트를 반환해주는 api
    @action(detail=False, methods=('POST',), url_path='client', http_method_names=('post',), permission_classes=(ProjectIsAuthorOrReadonly,))
    def getProjectListByClient(self, request, *args, **kwargs):
        clientId = request.data.get('clientId')
        requestClient = Client.objects.get(id = clientId)
        qs = Project.objects.filter(client = requestClient)
        # 쿼리셋을 페이지네이션 해서 받고싶은만큼 나눈다.
        page = self.paginate_queryset(qs)
        if page is not None:
            # 페이지별로 시리얼라이저를 받아온다
            serializer = self.get_serializer(page,many=True)
            response = self.get_paginated_response(serializer.data)
            # 페이지별로 리스폰스를 나눠준다.
            return response
        serializer = self.get_serializer(page,many=True)
        response = self.get_paginated_response(serializer.data)
        return response

# ----------------------------------------------------- 사용하지 않는 API 끝 ---------------------------------------------------#

class CommentViewSet(viewsets.ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # 토큰 어센티케이션 걸어놨음
    authentication_classes = [TokenAuthentication]
    # 자기의 댓글에 대해서만 퍼미션을 걸어놓는 커스텀 퍼미션 걸어놨음
    permission_classes = [CommentIsAuthorOrReadonly]

class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # 토큰 어센티케이션
    authentication_classes = [TokenAuthentication]
    # 자신의 프로젝트의 리뷰에 대해서만 퍼미션을 가지고 있음
    permission_classes = [ReveiwIsAuthorOrReadonly]
