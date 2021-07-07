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

    # RequestViewset�� �⺻ url�� post��û�� ���� �� ���� ���� ȣ��Ǵ� �Լ�
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # ��� �Ƿڼ� �ۼ� �� ����Ǿ�� �ϴ� ����
    # ���� ���� �� : ���� ���� | ���� ���� | ������ | ������ ����(���� | ���� ����) | ����(FK) ���̺� ���� - �ڵ� ���� ���� | ���� ���� | ����� ���� | ���� �ڷ� | ����� �ڷ�
    # ���� ���� �� : ���� ���� | ���� ���� | ������ | ������ ����(���� | ���� ����) | ����(FK) ���̺� ���� - ���� ���� ���� | ���� ���� | ����� ���� | ���� �ڷ� | ����� �ڷ�
    @action(detail=False, methods=('POST',), http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def perform_create(self, serializer, request):
        # Token �ҷ��ͼ� ���� ������ ����
        #rint(request.headers['Token'])
        #Token = request.headers['Authorization']
        users = request.user
        # �Ƿڼ� �� �����ϱ�
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
        # ����Ʈȭ
        process = list(process.replace(',',''))
        detailprocess = list(detailprocess.replace(',',''))
        # number �ޱ� - �� �ڸ� �̻����� process�� detailprocess�� �� �ڸ� �̻�Ǹ� numberó�� ���� �ʿ���
        number = list(number.split(','))
        # project �����ϱ� : request ������ ����
        projects = Project.objects.create(
            client=client,
        )
        # jandi_webhook_project.send(name,client.user.username)
        # requst �����ϱ�
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
        # ���� �ִ� �� ���� �� Ȯ��
        blueprint_exist = request.data.get('blueprint_exist')
        # ������ �ִٸ�
        if int(blueprint_exist) == 1:
            index = 0
            for blueprint_element in blueprint:
                print(blueprint_element)
                EstimateViewSet.create(self, request, requests.id, blueprint_element, process[index], detailprocess[index], number[index])
                index = index + 1

        return Response(status = status.HTTP_200_OK,
                        data={   'code': ResponseCode.SUCCESS.value,
                                  'message': "�Ƿڼ��� ����������ϴ�."
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
    def find_select(self, request, *args, **kwargs):  # ���õ� ���� �о߿� ���� �������� ����

        category = request.data.get('category')
        # product id

        develop_instances = Develop.objects.filter(id__in=category)
       # select = Select.objects.filter(range__in=product_instances)
    #    select = Select.objects.filter(range=product) # �� �� �� ����..?

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

        #��Ʈ�ʰ� �̹� �������� ���
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


        #�������� �ʾҴٸ� ������ ���� �� īī������ Ŭ���̾�Ʈ���� ������
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
        
        #ä�� �α� ����
        chat = Chat.objects.create(
            text_content = serializer.data['content1'],
            answer = Answer.objects.get(id=serializer.data['id']),
            user_type = 1
        )

        #ä�� �α� ����
        chat = Chat.objects.create(
            text_content = serializer.data['content1'],
            answer = Answer.objects.get(id=serializer.data['id']),
            user_type = 1
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #ä�� īī���� ������
    @action(detail=False, methods=('POST',), url_path='chat', http_method_names=('post',))
    def chat(self, request, *args, **kawrgs):
        return Response(data=kakaotalk_chat_text.send(request.data["phoneNum"],request.data["requestTitle"],request.data["name"],request.data["text"]))
    
    #���� īī���� ������
    @action(detail=False, methods=('POST',), url_path='file', http_method_names=('post',))
    def file(self, request, *args, **kawrgs):
        
        return Response(data=kakaotalk_chat_file.send('01066057996','requestTitle','partner_name','file'))
        
# ----------------------------------------------------- ������� �ʴ� API ---------------------------------------------------#

    @swagger_auto_schema(request_body=AnswerSerializer)
    @action(detail=False, methods=('POST',), url_path='first-active', http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def first_active(self, request, *args, **kwargs):  # ���� ���� ���� ��Ʈ�� Ȱ��ȭ > ������Ʈ���� �Ǿ����.
            project__id = request.data.get('project__id')
            answer_qs = Answer.objects.filter(project = project__id)
            if answer_qs.exists():
                instance=answer_qs.first()
                instance.active = True
                instance.save()
                return Response(data={'code': ResponseCode.SUCCESS.value,
                                      'message' : "������ ���� ���� ��Ʈ�ʰ� Ȱ��ȭ�Ǿ����ϴ�.",
                                      'data': AnswerSerializer(answer_qs, many=True).data
                                    })
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "������Ʈ�� ���� ���ȼ��� �����ϴ�"
                            })

    @swagger_auto_schema(request_body=AnswerSerializer)
    @action(detail=False, methods=('PATCH',), url_path='active', http_method_names=('patch',))
    def change_active(self, request, *args, **kwargs):  # ��Ʈ���� id�� �޾Ƽ� �ش� id�� ��Ʈ�ʰ� ���� ���ȼ��� active ���� True�� ������ִ� API
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
                                  'message': "�ش� ��Ʈ���� ���ȼ��� Ȱ��ȭ�Ǿ����ϴ�."
                                  })
        return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "������Ʈ�� ���� ���ȼ��� �����ϴ�"
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
                                  'message': 'answer ���� �ٲ�����',
                                  'data': AnswerSerializer(answer).data
                                  }
                            )

        elif answer_click == 2:
            answer.info_check = 2
            answer.save()

            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message': 'answer ���� �ٲ�����',
                                  'data': AnswerSerializer(answer).data
                                  }
                            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "Error 404"
                                  })
# ----------------------------------------------------- ������� �ʴ� API �� ---------------------------------------------------#

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



# ----------------------------------------------------- ������� �ʴ� API ---------------------------------------------------#

    @swagger_auto_schema(request_body=ProjectSerializer)
    @action(detail=False, methods=['PATCH', ], url_path='state', http_method_names=('patch',))
    def change_state(self, request, *args, **kwargs):  # ��ư Ŭ���� ���� ������Ʈ state ���¸� �ٲٴ� api

        project_id = request.data.get('project_id')
        state = request.data.get('state')
        # project id

        #filter�� �˻� �� Queryset�� ��, get�� ���� �������� ������ ���ܸ� �߻���Ŵ
        update_project = Project.objects.get(id=project_id)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        serializer = ProjectSerializer(update_project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'data': ProjectSerializer(update_project).data
                              })
    
    # �ش� Ŭ���̾�Ʈ�� ������Ʈ����Ʈ�� ��ȯ���ִ� api
    @action(detail=False, methods=('POST',), url_path='client', http_method_names=('post',), permission_classes=(ProjectIsAuthorOrReadonly,))
    def getProjectListByClient(self, request, *args, **kwargs):
        clientId = request.data.get('clientId')
        requestClient = Client.objects.get(id = clientId)
        qs = Project.objects.filter(client = requestClient)
        # �������� ���������̼� �ؼ� �ް������ŭ ������.
        page = self.paginate_queryset(qs)
        if page is not None:
            # ���������� �ø���������� �޾ƿ´�
            serializer = self.get_serializer(page,many=True)
            response = self.get_paginated_response(serializer.data)
            # ���������� ���������� �����ش�.
            return response
        serializer = self.get_serializer(page,many=True)
        response = self.get_paginated_response(serializer.data)
        return response

# ----------------------------------------------------- ������� �ʴ� API �� ---------------------------------------------------#

class CommentViewSet(viewsets.ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # ��ū �Ƽ���̼� �ɾ����
    authentication_classes = [TokenAuthentication]
    # �ڱ��� ��ۿ� ���ؼ��� �۹̼��� �ɾ���� Ŀ���� �۹̼� �ɾ����
    permission_classes = [CommentIsAuthorOrReadonly]

class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # ��ū �Ƽ���̼�
    authentication_classes = [TokenAuthentication]
    # �ڽ��� ������Ʈ�� ���信 ���ؼ��� �۹̼��� ������ ����
    permission_classes = [ReveiwIsAuthorOrReadonly]
