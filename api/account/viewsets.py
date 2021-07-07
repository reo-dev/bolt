#-*- coding: cp949 -*-
from rest_framework import (
    viewsets,
    status,
    mixins,
)

import random
import pandas as pd

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

# ��� ���� ����
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

import pandas as pd


# ����Ż��� �ڵ��� ��ȣ null�� ���� �� ��� �ؽ�ȭ

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
    

    @action(detail=False, methods=('POST',), url_path='login', http_method_names=('post',))
    def login(self, request, *args, **kawrgs):
        '''
        �Ϲ� �α���
        '''

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            
            LoginLog.objects.create(
                   user=user,
                   type=user.type,
            )
            
            if user.type == 0:
                client = Client.objects.filter(user=user)
                return Response(data={
                                    'code': ResponseCode.SUCCESS.value,
                                    'message': '�α��ο� �����Ͽ����ϴ�.',
                                    'data': {
                                        'token': user.auth_token.key,
                                        'User': PatchUserSerializer(user).data,
                                        'Client' : ClientSerializer(client, many=True).data,
                                    }})
            partner = Partner.objects.filter(user=user)
            return Response(data={
                                    'code': ResponseCode.SUCCESS.value,
                                    'message': '�α��ο� �����Ͽ����ϴ�.',
                                    'data': {
                                        'token': user.auth_token.key,
                                        'User': PatchUserSerializer(user).data,
                                        'Partner' : PartnerSerializer(partner, many=True).data,
                                    }})

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': '���̵� Ȥ�� ��й�ȣ�� Ʋ�Ƚ��ϴ�.'},
        )

    @action(detail=False, methods=('POST',), url_path='data', http_method_names=('post',), permission_classes=(IsAuthenticated,),)
    def Token_data(self, request, *args, **kawrgs):
        '''
        ���ΰ�ħ�� ��, ��ū ������ ������ ������ ����
        '''
        user = request.user
        if user.type == 0:
            client = Client.objects.filter(user=user)
            return Response(data={
                'code': ResponseCode.SUCCESS.value,
                'message': 'Ŭ���̾�Ʈ �����͸� �����帳�ϴ�.',
                'data': {
                    'token': user.auth_token.key,
                    'User': PatchUserSerializer(user).data,
                    'Client': ClientSerializer(client, many=True).data,
                }})
        partner = Partner.objects.filter(user=user)
        return Response(data={
            'code': ResponseCode.SUCCESS.value,
            'message': '��Ʈ�� �����͸� �����帳�ϴ�.',
            'data': {
                'token': user.auth_token.key,
                'User': PatchUserSerializer(user).data,
                'Partner': PartnerSerializer(partner, many=True).data,
            }})


    @action(detail=False, methods=('PATCH',), url_path='deactivate', http_method_names=('patch',),  permission_classes=[IsAuthenticated], )
    def deactivate(self, request, *args, **kwargs):
        """
        ȸ�� Ż��
        """
        user = request.user
        password = request.data.get('password')
        if not authenticate(username=user.username, password=password):
            return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={'message': '��й�ȣ�� ���� �ʽ��ϴ�.'},
                    )
        user.is_active = False
        user.username = user.username + '(deactivate_user_{})'.format(timezone.now())
        user.phone = get_default_hash_id()
        user.save()

        return Response()

    @action(detail=False, methods=['PATCH', ], url_path='password',
            http_method_names=('patch',), permission_classes=(IsAuthenticated,), )
    def change_password(self, request, *args, **kwargs):
        '''
        ��й�ȣ ����
        '''
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        user = request.user
        if user.check_password(password):
            if password == new_password:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'message': '������ ���� ��й�ȣ�� �Է��ϼ̽��ϴ�.'}
                )
            user.set_password(new_password)
            user.save()
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message': '���������� ��й�ȣ�� �����Ͽ����ϴ�.'})
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': '������ ��й�ȣ�� ���� �ʽ��ϴ�.', })

    @action(detail=False, methods=('POST',), url_path='password/phone', http_method_names=('post',))
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
            # email = EmailMessage('[��Ʈ�س�Ʈ]ȸ������ �ӽ� ��й�ȣ�� �̸��Ϸ� �����帳�ϴ�.', 'ȸ������ �ӽ� ��й�ȣ��\n\n' + password + '\n\n�Դϴ�.', to=[user.username])
            # email.send()
            return Response(data={'code': ResponseCode.SUCCESS.value,
                                  'message' : '�ӽ� ��й�ȣ�� ȸ������ ��ȭ��ȣ�� �߼۵Ǿ����ϴ�.',
                                  })
        return Response( status=status.HTTP_400_BAD_REQUEST,
                         data={'message': 'ȸ�������� �ùٸ��� �ʽ��ϴ�.'}
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
                                  'message': '�Է��Ͻ� �޴��� ��ȣ�� ���Ե� �̸��� ����Դϴ�.',
                                  'data': list_username,
                                  })
        return Response(status=status.HTTP_400_BAD_REQUEST,
                         data={'message': '�Է��Ͻ� ��ȣ�� ���� �� ������ �����ϴ�. �����Ϳ� ������ �ּ���.'}
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

    @swagger_auto_schema(request_body=ClientSerializer)
    @action(detail=False, methods=('POST',), url_path='signup', http_method_names=('post',))
    def client_signup(self, request, *args, **kwargs):
        '''
        ȸ������
        '''
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        title = request.data.get('title')
        path = request.data.get('path')
        business = request.data.get('business')
        phone = request.data.get('phone')
        type = request.data.get('type')
        marketing = request.data.get('marketing')
        # type�� ���� def(partner / client)�� api�� ���� ����
        if not username or not password:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�̸��� �̳� ��й�ȣ ���� �����ϴ�.'})

        if not phone:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '��ȭ��ȣ ���� �����ϴ�.'})

        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�ش� ���̵� �̹� �����մϴ�.'})

        if User.objects.filter(phone=phone).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�ش� ��ȭ��ȣ�� �̹� �����մϴ�.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            type=type,
            phone=phone,
            marketing=marketing,
        )

        client = Client.objects.create(
            user=user,
            name=name,
            title=title,
            path=path,
            business=business,
        )
        token, _ = Token.objects.get_or_create(user=user)

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': 'ȸ�������� ���������� �Ϸ�Ǿ����ϴ�.\n�ٽ� �α����� ���ּ���.',
                              'data': {
                                     'token': user.auth_token.key,
                                     'client': ClientSerializer(client).data,
                                     'user': PatchUserSerializer(user).data,
                                     # password�� ���� �����͸� ���������
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
    #     # ����Ʈȭ
    #     #client_phone_list = list(client_phone_list)
    #     partner_phone_list = list(partner_phone_list)
    #     # ��������
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
    #             'message': '�߼ۿ� �����Ͽ����ϴ�.',
    #             'data': {
    #                 'status_code': response2.status_code,
    #                 'response': response2.json(),
    #             }
    #         })

# ----------------------------------------------------- ������� �ʴ� API ---------------------------------------------------#
    #@action(detail=False, methods=('POST',), url_path='kakaotalk', http_method_names=('post',), )
    #def kakao_client(self, request, *args, **kwargs):  # Ŭ���̾�Ʈ���� ���ȼ� ��ϵ� �� īī���� ������
    #    client = request.data.get('client')
    #    client_qs = Client.objects.filter(id=client)
    #    client_phone_list = client_qs.values_list('user__phone', flat=True)
    #    print(client_qs)
    #    print(client_phone_list)
    # ����Ʈȭ
    #   client_phone_list = list(client_phone_list)
    # ��������
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
        #    'message': '�߼ۿ� �����Ͽ����ϴ�.',
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
    #    # ����Ʈȭ
    #    client_phone_list = list(client_phone_list)
    #    # ��������
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
    #            'message': '�߼ۿ� �����Ͽ����ϴ�.',
    #            'data': {
    #                'status_code': response.status_code,
    #                'response': response.json(),
    #            }})

    # Ư�� Atribute�� �������� �������� ��, signal�� ���ؼ� Kakaotalk�� ������ API 

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
    #    # ����Ʈȭ
    #    client_phone_list = list(client_phone_list)
    #    partner_phone_list = list(partner_phone_list)
    #    # ��������
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
    #            'message': '�߼ۿ� �����Ͽ����ϴ�.',
    #        #    'data': {
    #        #        'status_code': response1.status_code,
    #        #        'response': response1.json(),
    #        #    }
    #        })

# ----------------------------------------------------- ������� �ʴ� API �� ---------------------------------------------------#

class PartnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    #orderbyList = ['-avg_score', '-id']
    queryset = Partner.objects.filter(user__is_active=True).order_by('-id')
    serializer_class = PartnerSerializer
    pagination_class = PartnerPageNumberPagination
    filter_backends = [filters.SearchFilter,PartnerFilter, filters.OrderingFilter]
    filterset_fields = ['history','history_set', 'city', 'category_middle__id', 'history_set__id', 'answer_set__id']
    search_fields = ['name','history','category_middle__category','info_company']
    ordering_fields = '__all__'
    # x=Partner.objects.filter(name='�ڷ�')
    # print(x.values())

    @action(detail=False, methods=('POST',), url_path='signup',http_method_names=('post',))
    def partner_signup(self, request, *args, **kwargs):
        '''
        ��Ʈ�� ȸ������
        '''
        username = request.data.get('username')
        password = request.data.get('password')
        phone = request.data.get('phone')
        type = request.data.get('type')
        marketing = request.data.get('marketing')
        name = request.data.get('name')
        logo = request.data.get('logo')
        city = request.data.get('city')
        info_company = request.data.get('info_company')
        history = request.data.get('history')
        deal = request.data.get('deal')
        category_middle = request.data.get('category_middle')

        # ����Ʈ ���·� �ޱ� ���ؼ�
        category_middle = category_middle.split(',')
        #possible_set = possible_set.split(',')
        #history_set = history_set.split(',')


        file = request.data.get('file')
        resume = request.data.get('resume')

        # type�� ���� def(partner / client)�� api�� ���� ����
        #if not name:
        #    return Response(
        #        status=status.HTTP_400_BAD_REQUEST,
        #        data={'message': '��ȣ�� ���� �����ϴ�.'})

        if not phone:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '����ó ���� �����ϴ�.'})

        #if not logo:
        #     return Response(
        #         status=status.HTTP_400_BAD_REQUEST,
        #         data={'message': '�ΰ� ������ �����ϴ�.'})

        
        #if not career:
        #    return Response(
        #        status=status.HTTP_400_BAD_REQUEST,
        #        data={'message': '��� ����� �����ϴ�.'})

        #if not employee:
        #    return Response(
        #        status=status.HTTP_400_BAD_REQUEST,
        #        data={'message': '������ ���� �����ϴ�.'})

        #if not revenue:
        #    return Response(
        #        status=status.HTTP_400_BAD_REQUEST,
        #        data={'message': '���� ���� �����ϴ�.'})

        if not info_company:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'ȸ��Ұ� ���� �����ϴ�.'})

        #if not info_biz:
        #    return Response(
        #        status=status.HTTP_400_BAD_REQUEST,
        #        data={'message': '�ֿ��� ���� �����ϴ�.'})
        
        if not resume:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�̷¼� ������ �����ϴ�.'})

     #   if not history:
     #       return Response(
     #           status=status.HTTP_400_BAD_REQUEST,
     #           data={'message': '���� ���� �����ϴ�.'})

        if not deal:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�ֿ�ŷ�ó ���� �����ϴ�.'})

        if User.objects.filter(username=username).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�ش� �̸����� �̹� �����մϴ�.'})

        if User.objects.filter(phone=phone).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': '�ش� ��ȭ��ȣ�� �̹� �����մϴ�.'})

        user = User.objects.create_user(
            username=username,
            password=password,
            type=type,
            phone=phone,
            marketing=marketing,
        )

        partner = Partner.objects.create(
            user=user,
            name=name,
            info_company=info_company,
            history=history,
            deal=deal,
            logo=logo,
            file=file,
            resume=resume,
        )
        city = City.objects.filter(id=city)

        partner.city = city.first()

        category_elements = Develop.objects.filter(id__in=category_middle)
        #history_elements = Subclass.objects.filter(id__in=history_set)
        #possible_elements = Subclass.objects.filter(id__in=possible_set)
        partner.category_middle.add(*category_elements)
        #partner.history_set.add(*history_elements)
        #partner.possible_set.add(*possible_elements)
        partner.save()
        #form-data�� �ڵ����� �ּ� �ڵ带 ���� ������
        #serializer = PartnerSerializer(partner, data=request.data, partial=True)
        #serializer.is_valid(raise_exception=True)
        #instance = serializer.save()
        #instance.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': 'ȸ�������� ���������� �Ϸ�Ǿ����ϴ�.\n�ٽ� �α����� ���ּ���.',
                              'data': {
                                  'token': user.auth_token.key,
                                  'partner': PartnerSerializer(partner).data,
                                  'user': PatchUserSerializer(user).data,
                              }})

    @action(detail=False, methods=('POST',), url_path='category', http_method_names=('post',))
    # ��Ʈ�� ������ �ΰ� �����ϴ� API
    def partnerListByCategory(self, request, *args, **kwargs):
        
        # category = request.data.get('category')
        count = request.data.get('count')
        qs = Partner.objects.filter(user__is_active=True).exclude(logo ="null")
        # qs = PartnerCategory.objects.select_related('partner').exclude(partner__logo ="null")
        partnerList = PartnerCategorySerializer(qs,many=True).data
        partnerListSize = len(partnerList)
        if partnerListSize == 0:
            partnerList = random.sample(partnerList,partnerListSize)
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message' : "have no category",
                }
            )
        try:
            partnerList = random.sample(partnerList,count)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'count' : count,
                    'data' : partnerList
                }
            )
        except ValueError:
            partnerList = random.sample(partnerList,partnerListSize)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    'count' : partnerListSize,
                    'data' : partnerList
                }
            )

# ----------------------------------------------------- ������� �ʴ� API ---------------------------------------------------#

    @action(detail=False, methods=('GET',), url_path='request', http_method_names=('get',))
    def find_partner(self, request, *args, **kwargs):  # �Ƿڼ� �ϼ� �ÿ� ������ ��Ʈ�� ����Ʈ ��õ
        subclass = request.GET['subclass']

       # partner1_qs = Partner.objects.filter(possible_set__id = subclass)
       # print(partner1_qs)
        partner2_qs = Partner.objects.filter(history_set__id = subclass)
       # print(partner2_qs)
        #query_set ��ġ��
       # partner_qs = partner1_qs.union(partner2_qs)

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '�ش� �Ƿڼ��� ������ ��Ʈ�� ����Ʈ�Դϴ�.',
                              'data': PartnerSerializer(partner2_qs, many=True).data
                              }
                        )

    @action(detail=False, methods=['PATCH', ], url_path='coin', http_method_names=('patch',), permission_classes=(IsAuthenticated,),)
    def update_coin(self, request, *args, **kwargs):  # ������ �������� �� ���� �߰�
        # ���� ���� �ø����� �޾Ƽ� ������Ʈ�� ��û.
        partner_id = request.user.partner.id
        #partner_id = request.data.get('partner_id')
        coin = request.data.get('coin')  # ����Ʈ���� Partner coin���� �ҷ��ͼ� ���ϱ� Ȥ�� ���� ����

        # filter�� �˻� �� Queryset�� ��, get�� ���� �������� ������ ���ܸ� �߻���Ŵ
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        partner_data.coin += coin
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '������ ������Ʈ�� ��Ʈ�� �����Դϴ�.',
                              'data': PartnerSerializer(partner_data).data
                              }
                        )

    @action(detail=False, methods=['PATCH', ], url_path='minus-coin', http_method_names=('patch',),
            permission_classes=(IsAuthenticated,), )
    def minus_coin(self, request, *args, **kwargs):  # ���� �ÿ� ������ ���ִ� API
        # ���� ���� �ø����� �޾Ƽ� ������Ʈ�� ��û.
        partner_id = request.user.partner.id
        coin = request.data.get('coin')  # ����Ʈ���� Partner coin���� �ҷ��ͼ� ���ϱ� Ȥ�� ���� ����

        # filter�� �˻� �� Queryset�� ��, get�� ���� �������� ������ ���ܸ� �߻���Ŵ
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        partner_data.coin -= coin
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '������ ������Ʈ�� ��Ʈ�� �����Դϴ�.',
                              'data': PartnerSerializer(partner_data).data
                              }
                        )

    #@receiver(post_save, sender=Request)
    #def request_kakaotalk(sender, instance, *args, **kwargs):  # �˼� �� ������ ��Ʈ�ʿ��� īī���� �˸�
    #    client = instance.client
    #    subject = instance.name
    #    subclass = instance.product
    #    category = instance.category.values_list('category')
    #    category_list = list(category)
    #    # ����Ʈȭ
    #    for i in range(len(category_list)):
    #        category_list[i] = category_list[i][0]
    #    # print(category_list)
    #    # str ȭ
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
    #        # query_set value ��������
    #        partner_phone_list = partner_qs_all.values_list('user__phone', flat=True)
    #        # ����Ʈȭ
    #        partner_phone_list = list(partner_phone_list)
    #        # ��������
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
            ##    'message': '�߼ۿ� �����Ͽ����ϴ�.',
            ##    'data': {
            ##        'status_code': response.status_code,
            ##        'response': response.json(),
            ##    }})
    #        return True
    #    return False

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('PATCH',), url_path='success', http_method_names=('patch',))
    def meeting_success(self, request, *args, **kwargs):
        partner_id = request.data.get('partner_id')
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        partner_data.success += 1
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '��Ʈ�� ���� ���� Ƚ���� �߰��Ǿ����ϴ�.',
                              'data': PartnerSerializer(partner_data).data,
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('PATCH',), url_path='fail', http_method_names=('patch',))
    def meeting_fail(self, request, *args, **kwargs):
        partner_id = request.data.get('partner_id')
        partner_data = Partner.objects.get(id=partner_id)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        partner_data.fail += 1
        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '��Ʈ�� ���� ���� Ƚ���� �߰��Ǿ����ϴ�.',
                              'data': PartnerSerializer(partner_data).data,
                              }
                        )

    @swagger_auto_schema(request_body=PartnerSerializer)
    @action(detail=False, methods=('GET',), url_path='meeting', http_method_names=('get',))
    def meeting_percent(self, request, *args, **kwargs):
        partner_id = request.data.get('partner_id')
        partner_data = Partner.objects.get(id=partner_id)
        meeting_count = (partner_data.success + partner_data.fail)
        # Serializer�� ó�� �Ķ���Ϳ��� model(row)�� �;���.
        if meeting_count == 0:
           if not partner_data.success == 0: # ���� ������ 1ȸ �̻��� ���
                partner_data.meeting = 100
           else:                            # ���� ������ 0ȸ�� ���
                partner_data.meeting = 0
        else:
            partner_data.meeting = partner_data.success / meeting_count

        partner_data.save()

        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'message': '��Ʈ���� ���� ��ȯ ������ �Դϴ�.',
                              'data': PartnerSerializer(partner_data).data,
                              }
                        )


    @action(detail=False, methods=('GET',), url_path='find-partner-name', http_method_names=('get',))
    def findpartnername(self, request, *args, **kwargs):
        request_name = request.GET.dict()['name']

        partner_info = Partner.objects.all().filter(name__contains = request_name)

        return Response(
                status=status.HTTP_200_OK,
                data={
                    'data': PartnerSerializer(partner_info, many=True).data,
                }
            )

# ----------------------------------------------------- ������� �ʴ� API �� ---------------------------------------------------#

class PortfolioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'is_main', 'partner']
    
class PathViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Path.objects.all()
    serializer_class = PathSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'path']

class BusinessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'business']

class PartnerReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = PartnerReview.objects.all()
    serializer_class = PartnerReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'score','client','partner']

class PartnerReviewTempViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = PartnerReviewTemp.objects.all()
    serializer_class = PartnerReviewTempSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'score','client','partnername']


class CsvFileuploadViewSet(viewsets.ModelViewSet):
    queryset = CsvFileUpload.objects.all()
    serializer_class = CsvFileuploadSerializer

    @action(detail=False, methods=('POST',), url_path='csvfile_upload', http_method_names=('post',))

    def fileupload(self, request, *args, **kwargs):

        partner_info_file = request.data.get('partner_info_file') # ������ ���� ��������
        portfolio_file = request.data.getlist('portfolio_file') # ȸ��Ұ��� ����(ppt or pdf)
        logo = request.data.get('logo')
        
        csv_file = pd.read_csv(partner_info_file, error_bad_lines=False)
        csv_file_values = csv_file.values
        count = 16550
        
        for row in csv_file_values:
            print(row)
            count += 1
            print('���� ��',row[7])
            city_name = City.objects.get(city = row[7])
            category_middle_list = row[9].split(',')

            
            # init
            partner_file = []
            # file exist
            for pf in portfolio_file:
                if str(pf) == f'{row[4]}.pptx' or str(pf) == f'{row[4]}.pdf':
                    partner_file = pf

            if partner_file != []:
                user = User.objects.create(
                    username = f'boltnnut{count}' + '@boltnnut.com',
                    password = '1234',
                    phone = row[1],
                    type = 1,
                )
                
                partner = Partner.objects.create(
                    user = user,
                    name = row[4],
                    city = city_name,
                    info_company = row[0],
                    history = row[3],
                    file = partner_file,
                    logo = logo
                )
                
                for el in category_middle_list:
                    develop_name = Develop.objects.filter(category = el)
                    partner.category_middle.add(*develop_name)
                    partner.save()

        # # return Response(data={'message': "Successfully"})
            
        # return Response(data={'message': "Successfully saving {0} partner information.".format(len(csv_file_values))})