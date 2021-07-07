# from rest_framework import (
#     viewsets,
#     status,
#     mixins,
# )

# import random

# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

# #pagenation
# from .paginations import *

# #django-filter
# from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend
# from apps.account.filters import *

# import enum
# from apps.utils import *

# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema

# from django.contrib.auth import authenticate
# from apps.account.models import *
# from apps.category.models import *
# from apps.kakaotalk.models import *
# from .serializers import *
# from django.utils import timezone


# class KakaotalkViewSet(viewsets.GenericViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer

#     @action(detail=False, methods=('POST',), url_path='chat', http_method_names=('post',))
#     def chat(self, request, *args, **kawrgs):
#         url = 'https://api.bizppurio.com/v1/token'
#         headers = {
#             'Content-type': 'application/json;charset=utf-8', 
#             'Accept': 'text/plain', 
#             'Authorization':'Basic Ym9sdG5udXRfa29yZWE6QGJvbHQxMjM='
#         }
#         response = requests.post(url, headers=headers)
#         response = json.loads(response.content)
#         token = response['accesstoken']
#         tokenType = response['type']
#         basicAccessToken = tokenType + " " + token
#         data = KakaoToken.objects.get()
#         data.token = basicAccessToken
#         data.save()
        
        
        
#         token = KakaoToken.objects.get(id=1)
#         Authorization = token.token
#         url = 'https://api.bizppurio.com/v3/message'
#         data = {
#             'account': 'boltnnut_korea',
#             'refkey': 'bolt123',
#             'type': 'at',
#             'from': '01028741248',
#             'to': '01066057996',
#             'content': {
#                 'at': {
#                     'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98',
#                     'templatecode': 'send_chat_text',
#                     'message': 'test' + ' 상담에 매칭된 ' + 'test' + '이 다음과 같이 답변을 주셨습니다.\n\n' + 'test',
#                     'button': [
#                         {
#                             'name': '답변하러 가기',
#                             'type': 'WL',
#                             'url_mobile': 'https://www.boltnnut.com',
#                             'url_pc': 'https://www.boltnnut.com',
#                         }
#                     ]
#                 }
#             }
#         }
#         headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
#         response = requests.post(url, data=json.dumps(data), headers=headers)
#         # return response

#         return Response(data={
#                                 'code': ResponseCode.SUCCESS.value,
#                                 'message': '로그인에 성공하였습니다.',
#                         }})