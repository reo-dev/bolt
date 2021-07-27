#-*- coding: cp949 -*-
from django.utils.deconstruct import deconstructible

from rest_framework.response import Response
import datetime
import io
import os
import random
import string
import uuid
import enum
import requests
import json
import time
from .project.models import *
from .account.models import *
import sys

from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives

from PIL import Image
import cv2
import glob
import imageio
from io import BytesIO,StringIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import pandas as pd
from pptx import Presentation
import unicodedata
from google.oauth2 import service_account
from google.cloud import vision






class ResponseCode(enum.Enum):

    SUCCESS = 0
    FAIL = 1


@deconstructible
class FilenameChanger(object):

    def __init__(self, base_path):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.base_path = '{}/{}'.format(base_path, str(date))

    def __call__(self, instance, filename, *args, **kwargs):
        ext = filename.split('.')[-1].lower()
        filename = "%s.%s" % (uuid.uuid4(), ext)
        path = os.path.join(self.base_path, filename)
        print('[File] Upload File')
        print('- name : {}'.format(filename))
        print('- format : {}'.format(ext))
        print('- new name : {}'.format(filename))
        print('- path : {}'.format(path))
        return path

    def __eq__(self, other):
        return self.base_path


@deconstructible
class Util():

    @classmethod
    def add_unit(cls, value):
        UNIT = (
            (100000000, 'B'),
            (1000000, 'M'),
            (1000, 'K'),
            (1, ''),
        )
        for count, unit in UNIT:
            if value % count != value:
                number = round(value / count, 1)
                if (number*10)%10 == 0:
                    number = int(number)
                return '{number}{unit}'.format(number=str(number), unit=unit)
        return '{number}{unit}'.format(number=value, unit='')

    @classmethod
    def get_random_digit_letter(cls, length):
        result = ''
        for i in range(length):
            result += random.choice(string.digits)
        return str(result)

    @classmethod
    def get_random_letter(cls, length):
        result = ''
        for i in range(length):
            result += random.choice(string.digits + string.ascii_letters)
        return str(result)

class kakaotalk(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone_list, subject):
            # print(subject)
            # print(phone_list)
            # for phone in phone_list:
            #  print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #        'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'request_to_partner2',
            #                 'message': '파트너님에게 적합한 의뢰서가 도착했습니다.\n의뢰서명 : ' + subject,

            #               'button': [
            #                     {
            #                      'name': '확인하러 가기',
            #                      'type': 'WL',
            #                      'url_mobile': 'http://www.boltnnut.com',
            #                      'url_pc': 'http://www.boltnnut.com'
            #                  }
            #              ]}}}
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return 


class kakaotalk2(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone_list, subject, subclass,category):
            # print(subject)
            # print(phone_list)
            # for phone in phone_list:
            #  print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #        'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'request_to_partner3',
            #                 'message': '파트너님에게 적합한 의뢰서가 도착했습니다.\n의뢰서명 : ' + subject + '\n의뢰제품분야 : ' + str(subclass) + '\n제조의뢰분야 : ' + category,

            #               'button': [
            #                     {
            #                      'name': '확인하러 가기',
            #                      'type': 'WL',
            #                      'url_mobile': 'http://www.boltnnut.com',
            #                      'url_pc': 'http://www.boltnnut.com'
            #                  }
            #              ]}}}
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return


class kakaotalk_request(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone_list):
            # print(phone_list)
            # for phone in phone_list:
            #  #print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #        'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'answer_to_client',
            #                 'message': '고객님의 의뢰에 대한 전문가의 제안서가 도착하였습니다.\n\n* 해당 메시지는 고객님께서 요청하신 의뢰에 대한 제안이 있을 경우 발송됩니다',

            #               'button': [
            #                     {
            #                      'name': '확인하러 가기',
            #                      'type': 'WL',
            #                      'url_mobile': 'http://www.boltnnut.com',
            #                      'url_pc': 'http://www.boltnnut.com'
            #                  }
            #              ]}}}
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return

class kakaotalk_request_edit_end(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone):
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #          'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'request_edit_end',
            #                 'message':'고객님의 의뢰서 검토가 완료되어 파트너 제안서 모집이 시작되었습니다.\n\n제안서가 도착할 때마다 카카오톡 알림메시지를 보내드립니다.\n\n조금만 기다려주세요'}}}
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            #  return response
            return

class kakaotalk_send_information(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone_list, subject, content, price, period, file):
            # print(subject)
            # print(phone_list)
            # for phone in phone_list:
            #  print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #          'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_request_information3',
            #                 'message': '다음 의뢰를 주신 클라이언트에게 파트너님을 추천하고자합니다.\n클라이언트와 소통의사가 있으시면 ‘O’를, 없으시다면 ‘X’를 남겨주시길 바랍니다.\n\n해당 프로젝트를 진행할 의사가 있는 업체만 추천될 예정입니다.\n추천 후 클라이언트분께서 파트너님의 정보를 확인한 후 전화드릴 수 있습니다.\n\n의뢰제품 : ' + subject + '\n\n상담내용 : ' + content + '\n\n희망예산 : ' + price + '\n\n희망기간 : ' + period +  '\n\n의뢰파일 : ' + file
            #                 }
            #             }
            #          }
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return

class kakaotalk_send_IDPassword(object):
    def send(phoneNumber, username,title, password):
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message'
        data = {
            'account': 'boltnnut_korea', 
            'refkey': 'bolt123', 
            'type': 'at', 
            'from': '01028741248',
            'to': phoneNumber, 
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 
                    'templatecode': 'send_user_id_password',
                    'message': '안녕하세요. 볼트앤너트입니다.\n의뢰주신 ' + title + '의 가견적을 다시 확인할 수 있는\n의뢰 아이디와 비밀번호 안내드립니다.\n\n의뢰아이디 : '+ username + '\n비밀번호 : ' + password +'\n\n볼트앤너트 홈페이지에서 해당 아이디와 비밀번호로 로그인하신 후\n상단 메뉴창에서 기존 의뢰에서 의뢰 주신 '+title +'의 가견적을 재확인할 수 있습니다.'
                    }
                }
            }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response
        return

class kakaotalk_send_ID_ExistUser(object):
    def send(phoneNumber, username,title):
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message'
        data = {
            'account': 'boltnnut_korea', 
            'refkey': 'bolt123', 
            'type': 'at', 
            'from': '01028741248',
            'to': phoneNumber, 
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 
                    'templatecode': 'send_id_exist_user',
                    'message': '안녕하세요. 볼트앤너트입니다.\n의뢰주신 ' + title + '의 가견적을 다시 확인할 수 있는\n의뢰 아이디를 안내드립니다.\n\n의뢰아이디 : '+ username +'\n\n볼트앤너트 홈페이지에서 해당 아이디와 비밀번호로 로그인하신 후\n상단 메뉴창에서 기존 의뢰에서 의뢰 주신 '+title +'의 가견적을 재확인할 수 있습니다.'
                    }
                }
            }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response
        return

class kakaotalk_set_temp_password():
    def send(phoneNumber,tempPassword):
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message'
        data = {
            'account': 'boltnnut_korea', 
            'refkey': 'bolt123', 
            'type': 'at', 
            'from': '01028741248',
            'to': phoneNumber, 
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 
                    'templatecode': 'set_temp_password',
                    'message': '[볼트앤너트] 회원님의 임시비밀번호를 카카오톡으로 보내드립니다.\n회원님의 임시비밀번호는 ' +  tempPassword + ' 입니다.\n\n회원님이 비밀번호를 변경하지 않았는데, 해당메세지를 받았을 시 볼트앤너트로 문의해주십시오.'
                    }
                }
            }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response
        return

class kakaotalk_send_meeting_confirm():
        def send(phoneNumber,requestCategory,requestTitle):
            # token = KakaoToken.objects.get(id=1)
            # Authorization = token.token
            
            # consultant1 = "노현수 기술팀장"
            # consultant2 = "최진영 기술이사"
            # consultant3 = Consultant.objects.order_by("?").filter(id__lt=9).first().name
            # print("랜덤 컨설턴트 : ",consultant3)
            # url = 'https://api.bizppurio.com/v3/message'
            # data = {
            #     'account': 'boltnnut_korea', 
            #     'refkey': 'bolt123', 
            #     'type': 'at', 
            #     'from': '01028741248',
            #     'to': phoneNumber, 
            #     'content': {
            #         'at': {
            #             'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_meeting_confirm',
            #             'message': '안녕하세요. 볼트앤너트입니다.\n\n의뢰주신 ' + requestTitle + '의 가견적은 잘 받아보셨나요?\n\n'+requestTitle +' 의뢰에는 '+requestCategory+'의 전문 컨설턴트인 ' + consultant1 +',' + consultant2 + ',' + consultant3 +'님이 배정되어 있습니다.\n\n볼트앤너트는 전문 컨설턴트의 상담을 통한 정확한 견적 서비스를 무료로 제공하고 있으니\n\n상담을 통해 '+requestTitle +'의 정확한 견적과 전문 지식을 알아보세요\n\n상담은 볼트앤너트 홈페이지에서 로그인하신 후 작성하신 의뢰 페이지에서 요청하실 수 있습니다.\n\n지금 바로 상담을 원하시면 볼트앤너트 상담 전화인 02-926-6637로 바로 전화주세요.',
            #             'button': [
            #                 {
            #                     'name': '무료 상담 받으러 가기',
            #                     'type': 'WL',
            #                     'url_mobile': 'https://www.boltnnut.com/',
            #                     'url_pc': 'https://www.boltnnut.com/'
            #                 }
            #             ]
            #         }
            #     }
            # }
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
            # response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return
          
class kakaotalk_send_meetin_content(object):
    def send(title, startAt, isOnline, phone):
        # try:
        #     message = "안녕하세요. 볼트앤너트입니다.\n의뢰주신 {title}에 전문 컨설턴트가 배정되어 상담을 진행할 예정입니다.\n{startAt}에 {place}에서 뵙겠습니다.\n{online}\n정확한 상담을 위해서 첨부된 링크에 포함된 상담 의뢰서를 작성해주시면\n담당 컨설턴트님께서 더욱 적합한 상담을 드릴 수 있습니다.\n추가적으로 궁금하신 사항이 있다면 {BnNPhone}, {BnNEmail}로 문의사항을 보내주세요.\n감사합니다.".format(
        #         title = title,
        #         startAt = startAt,
        #         place = '서울특별시 성북구 고려대로27길 3 2층' if not isOnline else 'ZooM 화상회의',
        #         online = 'ZooM 화상회의 주소는 미팅 1시간 전 다시 안내 드리겠습니다.\n' if isOnline else ' ',
        #         BnNPhone = '02-926-6637',
        #         BnNEmail = 'project@boltnnut.com'
        #     )
        #     token = KakaoToken.objects.get(id=1)
        #     Authorization = token.token
        #     url = 'https://api.bizppurio.com/v3/message'
        #     data = {
        #         'account': 'boltnnut_korea', 
        #         'refkey': 'bolt123', 
        #         'type': 'at', 
        #         'from': '01028741248',
        #         'to': phone, 
        #         'content': {
        #             'at': {
        #                 'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 
        #                 'templatecode': 'send_meeting_contentdaybefore2',
        #                 'message': message,
        #                 'button': [
        #                     {
        #                         'name': '상담의뢰서 받기',
        #                         'type': 'WL',
        #                         'url_mobile': 'https://boltnnutplatform.s3.ap-northeast-2.amazonaws.com/media/request/request.docx',
        #                         'url_pc': 'https://boltnnutplatform.s3.ap-northeast-2.amazonaws.com/media/request/request.docx'
        #                     }
        #                 ]
        #             }
        #         }
        #     }
        #     headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        #     response = requests.post(url, data=json.dumps(data), headers=headers)
        #     return response
        # except Exception as e:
        #     return e
        return

class kakaotalk_send_request_review():
        def send(phoneNumber,consultant,requestTitle):
            # token = KakaoToken.objects.get(id=1)
            # Authorization = token.token
            
            # url = 'https://api.bizppurio.com/v3/message'
            # data = {
            #     'account': 'boltnnut_korea', 
            #     'refkey': 'bolt123', 
            #     'type': 'at', 
            #     'from': '01028741248',
            #     'to': phoneNumber, 
            #     'content': {
            #         'at': {
            #             'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_request_review',
            #             'message': '안녕하세요. 볼트앤너트입니다.\n\n의뢰주신 ' + requestTitle + '에 대한 ' +consultant +'님의 상담은 어떠셨나요?\n\n 부족한 점이나 칭찬할만한 점이 있다면 첨부된 링크에서 리뷰를 작성해주세요.\n\n매달 리뷰를 작성해주신 고객분들 중 한 분을 선발하여 무료 모델링 서비스를 제공하고 있습니다.',
            #             'button': [
            #                 {
            #                     'name': '리뷰하러가기',
            #                     'type': 'WL',
            #                     'url_mobile': 'https://www.boltnnut.com/',
            #                     'url_pc': 'https://www.boltnnut.com/'
            #                 }
            #             ]
            #         }
            #     }
            # }
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
            # response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return

class kakaotalk_send_request_rerequest():
        def send(phoneNumber,requestTitle):
            # token = KakaoToken.objects.get(id=1)
            # Authorization = token.token
            # boltnnutPhone = "02-996-6637"
            # boltnnutEmail = "boltnnut@boltnnut.com"
            # url = 'https://api.bizppurio.com/v3/message'
            # data = {
            #     'account': 'boltnnut_korea', 
            #     'refkey': 'bolt123', 
            #     'type': 'at', 
            #     'from': '01028741248',
            #     'to': phoneNumber, 
            #     'content': {
            #         'at': {
            #             'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'bizp_2021020216131026670531311',
            #             'message': '안녕하세요. 볼트앤너트입니다.\n\n요청 주신 의뢰 : ' + requestTitle + '에는 전문가인\n\n최진영 기술이사님이 배정되어 있습니다.\n\n의뢰 기본정보와 5가지 선택질문만 답변해주시면 '+requestTitle+'의 가견적과\n\n전문 컨설턴트 상담을 무료로 받을 수 있으니 확인해보세요.\n\n온라인 의뢰 작성 시에 불편한 사항이 있었다면 '+ boltnnutPhone +' 혹은\n\n' + boltnnutEmail +'로 연락주세요.',
            #             'button': [
            #                 {
            #                     'name': '의뢰작성하러가기',
            #                     'type': 'WL',
            #                     'url_mobile': 'http://www.boltnnut.com/',
            #                     'url_pc': 'http://www.boltnnut.com/'
            #                 }
            #             ]
            #         }
            #     }
            # }
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
            # response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return

class kakaotalk_send_appreciate():
        def send(phoneNumber,requestTitle):
            # token = KakaoToken.objects.get(id=1)
            # Authorization = token.token
            # boltnnutPhone = "02-996-6637"
            # boltnnutEmail = "boltnnut@boltnnut.com"
            # url = 'https://api.bizppurio.com/v3/message'
            # data = {
            #     'account': 'boltnnut_korea', 
            #     'refkey': 'bolt123', 
            #     'type': 'at', 
            #     'from': '01028741248',
            #     'to': phoneNumber, 
            #     'content': {
            #         'at': {
            #             'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_appreciate',
            #             'message': '안녕하세요. 볼트앤너트입니다.\n\n볼트앤너트에 '+requestTitle +'의뢰를 주셔서 감사합니다.\n\n저희 볼트앤너트 서비스가 부족한 점이나 칭찬할만한 점이 있다면 첨부된 링크에서 리뷰를 작성해주세요.\n\n고객님께서 주신 소중한 의견 하나하나 귀기울여 듣고 부족한 점을 개선하도록 하겠습니다.\n\n매달 리뷰를 작성해주신 고객분들 중 한 분을 선발하여 무료 모델링 서비스를 제공하고 있습니다.\n\n볼트앤너트는 고객 분들의 의뢰 물품을 최적의 가격에 제대로 만들어드릴 수 있도록 노력하겠습니다.',
            #             'button': [
            #                 {
            #                     'name': '리뷰하러가기',
            #                     'type': 'WL',
            #                     'url_mobile': 'https://www.boltnnut.com/',
            #                     'url_pc': 'https://www.boltnnut.com/'
            #                 }
            #             ]
            #         }
            #     }
            # }
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
            # response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return

class kakaotalk_archiving_after_meeting():
        def send(phoneNumber,requestTitle):
            # token = KakaoToken.objects.get(id=1)
            # Authorization = token.token
            # boltnnutPhone = "02-996-6637"
            # boltnnutEmail = "boltnnut@boltnnut.com"
            # url = 'https://api.bizppurio.com/v3/message'
            # data = {
            #     'account': 'boltnnut_korea', 
            #     'refkey': 'bolt123', 
            #     'type': 'at', 
            #     'from': '01028741248',
            #     'to': phoneNumber, 
            #     'content': {
            #         'at': {
            #             'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_appreciate',
            #             'message': '안녕하세요. 볼트앤너트입니다.\n\n볼트앤너트에 '+requestTitle +'의뢰를 주셔서 감사합니다.\n\n저희 볼트앤너트 서비스가 부족한 점이나 칭찬할만한 점이 있다면 첨부된 링크에서 리뷰를 작성해주세요.\n\n고객님께서 주신 소중한 의견 하나하나 귀기울여 듣고 부족한 점을 개선하도록 하겠습니다.\n\n매달 리뷰를 작성해주신 고객분들 중 한 분을 선발하여 무료 모델링 서비스를 제공하고 있습니다.\n\n볼트앤너트는 고객 분들의 의뢰 물품을 최적의 가격에 제대로 만들어드릴 수 있도록 노력하겠습니다.',
            #             'button': [
            #                 {
            #                     'name': '의뢰작성하러가기',
            #                     'type': 'WL',
            #                     'url_mobile': 'https://www.boltnnut.com/',
            #                     'url_pc': 'https://www.boltnnut.com/'
            #                 }
            #             ]
            #         }
            #     }
            # }
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
            # response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return
            
# #-----------------------------------------------------------------------------------------------------------------#

class kakaotalk_send_response_msg():
        def send(phone_list, requestTitle):
            for phone in phone_list:
                token = KakaoToken.objects.get(id=1)
                Authorization = token.token
                boltnnutPhone = "02-996-6637"
                boltnnutEmail = "boltnnut@boltnnut.com"
                url = 'https://api.bizppurio.com/v3/message'
                data = {
                    'account': 'boltnnut_korea',
                    'refkey': 'bolt123', 
                    'type': 'at', 
                    'from': '01028741248',
                    'to': '01041376379',
                    'content': {
                        'at': {
                            'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'template_code': 'send_response_message',
                            'message': "안녕하세요 {phone.username}님.\n\n 상담 요청하신 "+requestTitle +"의뢰에 적합한 제조사가 문의 사항에 대한 댓글을 달아주셨어요.\n\n 댓글 내용을 확인해보시고 추가로 궁금하신 사항이 있다면 해당 제조사와의 소통을 통해 문의해주세요.",
                            'button': [
                                    {
                                    'name': '댓글 확인하기',
                                    'type': 'WL',
                                    'url_mobile': 'http://www.boltnnut.com',
                                    'url_pc': 'http://www.boltnnut.com'
                                }
                            ]
                        }
                    }
                }
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
                response = requests.post(url, data=json.dumps(data), headers=headers)
                return response

class kakaotalk_send_msg_request_week():
        def send(phone_list, requestTitle):
            for phone in phone_list:
                token = KakaoToken.objects.get(id=1)
                Authorization = token.token
                boltnnutPhone = "02-996-6637"
                boltnnutEmail = "boltnnut@boltnnut.com"
                url = 'https://api.bizppurio.com/v3/message'
                data = {
                    'account': 'boltnnut_korea',
                    'refkey': 'bolt123',
                    'type': 'at', 
                    'from': '01028741248',
                    'to': '01041376379',
                    'content': {
                        'at': {
                            'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'template_code': 'send_message_after_week',
                            'message': "안녕하세요 {phone.username}님.\n\n요청하신 "+requestTitle+" 상담에 문의 사항은 충분히 해결되셨나요?\n\n제조사와의 소통 과정을 통해 충분히 해소되지 않았다면 볼트앤너트 전문 컨설턴트에게 상담을 요청해보세요.\n\n컨설턴트께서 문의 사항을 확인하고 적합한 답변을 드릴 수 있습니다.",
                            'button': [
                                    {
                                    'name': '상담하기',
                                    'type': 'WL',
                                    'url_mobile': 'https://www.boltnnut.com/',
                                }
                            ]
                        }
                    }
                }
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
                response = requests.post(url, data=json.dumps(data), headers=headers)
                return response

# class kakaotalk_send_detail_inform():
#         def send(phone_list, requestTitle):
#             token = KakaoToken.objects.get(id=1)
#             Authorization = token.token
#             boltnnutPhone = "02-996-6637"
#             boltnnutEmail = "boltnnut@boltnnut.com"
#             url = 'https://api.bizppurio.com/v3/message'
#             data = {
#                 'account': 'boltnnut_korea',
#                 'refkey': 'bolt123', 
#                 'type': 'at', 
#                 'from': '01028741248',
#                 'to': phone_list,
#                 'content': {
#                     'at': {
#                         'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'template_code': 'notice_partner',
#                         'message': "안녕하세요. 볼트앤너트입니다.\n"+requestTitle +"의뢰에 대한 채팅이 시작되었습니다.\n준비가 되셨으면 시작해주세요.",
#                     }
#                 }
#             }
#             headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
#             response = requests.post(url, data=json.dumps(data), headers=headers)
#             return response

# class kakaotalk_send_chat_alarm():
#         def send(phone):
#             url = 'https://api.bizppurio.com/v3/message'
#             data = {
#                 'account': 'boltnnut_korea',
#                 'refkey': 'bolt123', 
#                 'type': 'at', 
#                 'from': '01028741248',
#                 'to': phone,
#                 'content': {
#                     'at': {
#                         'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'template_code': 'send_chat_alarm',
#                         'message': "안녕하세요. 볼트앤너트입니다.\n채팅에 대한 답변이 도착했습니다.",
#                     }
#                 }
#             }
            
class kakaotalk_send_msg_response():
        # 제조사의 채팅에 답변을 하지 않고 2일이 지난 경우 (의뢰당 1번만)
        def send(phone_list, requestTitle, partner_name):
            for phone in phone_list:
                token = KakaoToken.objects.get(id=1)
                Authorization = token.token
                boltnnutPhone = "02-996-6637"
                boltnnutEmail = "boltnnut@boltnnut.com"
                url = 'https://api.bizppurio.com/v3/message'
                data = {
                    'account': 'boltnnut_korea',
                    'refkey': 'bolt123',
                    'type': 'at', 
                    'from': '01028741248',
                    'to': '01041376379',
                    'content': {
                        'at': {
                            'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'template_code': 'send_message_about_response',
                            'message': "안녕하세요 {phone.username}님.\n\n"+requestTitle+" 상담에 매칭된 "+partner_name+"분께서 답변을 기다리고 있습니다.\n\n상담을 종료하고 싶으시다면 "+partner_name+"분께 안내해주세요.",
                            'button': [
                                    {
                                    'name': '답변하러 가기',
                                    'type': 'WL',
                                    'url_mobile': 'https://www.boltnnut.com/',
                                    'url_pc': 'https://www.boltnnut.com/'
                                }
                            ]
                        }
                    }
                }

# 수정 후
# class kakaotalk_request_answer():
#         def send(phone,requestTitle):
#             token = KakaoToken.objects.get(id=1)
#             Authorization = token.token
#             boltnnutPhone = "02-996-6637"
#             boltnnutEmail = "boltnnut@boltnnut.com"
#             url = 'https://api.bizppurio.com/v3/message'
#              data = {
#                 'account': 'boltnnut_korea',
#                 'refkey': 'bolt123',
#                 'type': 'at',
#                 'from': '01028741248',
#                 'to': phone,
#                 'content': {
#                     'at': {
#                         'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98',
#                         'templatecode': 'request',
#                         'message': '안녕하세요.' + phone.username + '님 상담 요청하신' + requestTitle + '에 적합한 제조사가 문의 사항에 대한 댓글을 달아 주셨어요\n\n 댓글 내용을 확인해보시고 추가로 궁금하신 사항이 있다면 해당 제조사와의 소통을 통해 문의해주세요',
#                         'button': [
#                             {
#                                 'name': '댓글 확인하기',
#                                 'type': 'WL',
#                                 'url_mobile': 'https://www.boltnnut.com/'',
#                                 'url_pc': 'https://www.boltnnut.com/'
#                             }
#                         ]
#                     }
#                 }
#             }
#             headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
#             response = requests.post(url, data=json.dumps(data), headers=headers)
#             return response





class kakaotalk_send_answer_to_client():
    def send(phone, username, requestTitle):
        #토큰 요청하고 저장
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

        #토큰 가져와서 api 보내기
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message/'
        data = {
            'account': 'boltnnut_korea',
            'refkey': 'bolt123',
            'type': 'at',
            'from': '01028741248',
            'to': phone,
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98',
                    'templatecode': 'send_answer_to_client',
                    'message': '안녕하세요 '+username+'님.\n요청하신 '+requestTitle+' 상담에 적합한 제조사가 문의주신 사항에 대한 답변을 제안주셨어요.\n답변 내용을 확인해보시고 추가로 궁금하신 사항은 해당 제조사와의 소통을 통해 문의해주세요.',
                    'button': [
                        {
                            'name': '제안서 확인하기',
                            'type': 'WL',
                            'url_mobile': 'https://www.boltnnut.com',
                            'url_pc': 'https://www.boltnnut.com' ,
                        }
                    ]
                }
            }
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(response.json())
        return response







class kakaotalk_chat_text():
    def send(phone, requestTitle, partner_name, chat_content):
        
        #토큰 요청하고 저장
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
        
        #토큰 가져와서 api 보내기
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message'
        data = {
            'account': 'boltnnut_korea',
            'refkey': 'bolt123',
            'type': 'at',
            'from': '01028741248',
            'to': phone,
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98',
                    'templatecode': 'send_chat_text',
                    'message': requestTitle + ' 상담에 매칭된 ' + partner_name + '님이 다음과 같이 답변을 주셨습니다.\n\n' + chat_content,
                    'button': [
                        {
                            'name': '답변하러 가기',
                            'type': 'WL',
                            'url_mobile': 'https://www.boltnnut.com',
                            'url_pc': 'https://www.boltnnut.com',
                        }
                    ]
                }
            }
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response

class kakaotalk_chat_file():
    def send(phone, requestTitle, partner_name, file):
        
        #토큰 요청하고 저장
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

        #토큰 가져와서 api 보내기
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message'
        data = {
            'account': 'boltnnut_korea',
            'refkey': 'bolt123',
            'type': 'at',
            'from': '01028741248',
            'to': phone,
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98',
                    'templatecode': 'send_chat_file',
                    'message': requestTitle + ' 상담에 매칭된 ' + partner_name + '님이 ' + file + ' 파일을 전달주셨습니다.',
                    'button': [
                        {
                            'name': '확인하러 가기',
                            'type': 'WL',
                            'url_mobile': 'https://www.boltnnut.com',
                            'url_pc': 'https://www.boltnnut.com',
                        }
                    ]
                }
            }
        }
        headers = {'Content-type': 'application/json', 'Accept': 'file/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response



class jandi_webhook_answer():
    def send(title,clinetName):
        url = 'https://wh.jandi.com/connect-api/webhook/18069463/bf7dce120b1a85f9478b8460db6d07ad'
        headers = {
            'Accept': 'application/vnd.tosslab.jandi-v2+json',
            'Content-Type': 'application/json'
        }
        data = {
            "body" : "[볼트앤너트] "+clinetName+"님이 "+"<"+title+">"+"에 대한 제안서를 생성하였습니다.",
            }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response

class jandi_webhook_project():
    def send(title,clinetName):
        url = 'https://wh.jandi.com/connect-api/webhook/18069463/bf7dce120b1a85f9478b8460db6d07ad'
        headers = {
            'Accept': 'application/vnd.tosslab.jandi-v2+json',
            'Content-Type': 'application/json'
        }
        data = {
            "body" : "[볼트앤너트] " +clinetName+"님이 "+"<"+title+">"+" 프로젝트를 생성하였습니다.",
            }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response

    def send_requestInfo(title,clinetName):
        url = 'https://wh.jandi.com/connect-api/webhook/18069463/bf7dce120b1a85f9478b8460db6d07ad' 

        headers = {
            'Accept': 'application/vnd.tosslab.jandi-v2+json',
            'Content-Type': 'application/json'
        }
        data = {
            "body" : "[볼트앤너트] " +clinetName+"님이 "+"<"+title+">"+"  업체 수배 견적이 생성하였습니다.",
            }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response


class getIp():
    def get(a,b):
        x_forwarded_for = a
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = b

        if ip == '211.196.18.140' or ip == '211.216.28.238' or ip =='211.196.18.225' or ip =='59.5.24.185' or ip =='39.125.32.19' or ip =='220.116.11.139' or ip =='46.165.250.77' or ip=='54.86.50.139' or ip=='218.155.155.121':
            ip = '0.0.0.0'
        
        return ip



class sendEmail():
    def send(username):
        recipient = [username]
        sender = "boltnnut@boltnnut.com" # 
        image_path = '/home/ubuntu/staging/boltnnut_platform/media/account/signUpGreeting.jpg'
        image_name = Path(image_path).name
        subject = "[온라인 제조 플랫폼] 전국 제조사 정보 다 있다, 볼트앤너트에 회원 가입이 완료되었습니다."
        text_message = f"{image_name}"
        html_message = f"""
        <!doctype html>
            <html lang=en>
                <head>
                    <meta charset=utf-8>
                    <title>Some title.</title>
                </head>
                <body>
                    <h3>{subject}</h1>
                    <p>
                    {username}님, 볼트앤너트에 가입해 주셔서 감사합니다.<br>
                    <img style="width: 800px;" src='cid:{image_name}'/>
                    </p>
                </body>
            </html>
        """
        email = EmailMultiAlternatives(subject=subject, body=text_message, from_email=sender, to=recipient)
        if all([html_message,image_path,image_name]):
            email.attach_alternative(html_message, "text/html")
            email.content_subtype = 'html' 
            email.mixed_subtype = 'related' 
            with open(image_path, mode='rb') as f:
                image = MIMEImage(f.read(),_subtype="jpg")
                email.attach(image)
                image.add_header('Content-ID', f"<{image_name}>")
        email.send()


class imgUpload():
    def save():
        path = '/Users/iyuchang/Downloads/오솔찬/'
        file_list = os.listdir(path)
        for i in file_list:
            print(i)
            if i != '.DS_Store':
                uni1 = unicodedata.normalize('NFC',i)
                partner = Partner.objects.filter(name=uni1)
                if partner:
                    newpath = path+i
                    file_list = os.listdir(newpath)
                    for j in file_list:
                        j = unicodedata.normalize('NFC',j)
                        if j != '.DS_Store':
                            buffer = BytesIO()
                            j_=j.split('.')
                            if j_[-1] !='html' and j_[-1] !='PDF' and j_[-1]!='JFIF' and j_[-1]!='jfif':
                                if j_[-1]=='pptx':
                                    #pptx
                                    pr=Presentation(newpath+'/'+j)
                                    pr.save(buffer)
                                    pptx_file = InMemoryUploadedFile(buffer, None, j, 'application/vnd.openxmlformats-officedocument.presentationml.presentation', sys.getsizeof(pr), None)
                                    partner[0].file.save(j,pptx_file)

                                elif j_[-1]=='pdf':
                                    #pdf
                                    file = open(newpath+'/'+j, 'rb')
                                    pdf_file = InMemoryUploadedFile(file, None, j, 'application/pdf', sys.getsizeof(file), None)
                                    partner[0].file.save(j,pdf_file)

                                else:
                                    #이미지
                                    im=Image.open(newpath+'/'+j)
                                    if j_[-1] == 'jpg' or j_[-1]=='JPG':
                                        im=im.convert('RGB')
                                        j_[-1]='jpeg'
                                    im.save(buffer, j_[-1])
                                    image_file = InMemoryUploadedFile(buffer, None, j, 'image/'+j_[-1], im.size, None)

                                    Portfolio.objects.create(
                                        partner = partner[0],
                                        img_portfolio = image_file,
                                        name = j_[0]
                                    )


    def fileupload():
        path = '/Users/iyuchang/Downloads/본사분배.csv'
        csv_file = pd.read_csv(path, error_bad_lines=False)
        csv_file_values = csv_file.values
        count = 600352

        for row in csv_file_values:
            if Partner.objects.filter(name=row[4]):
                continue
            else:
                count += 1
                city_name = City.objects.get(city = row[7])
                category_middle_list = row[9].split(',')

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
                    logo='null'
                )
                
                for el in category_middle_list:
                    develop_name = Develop.objects.filter(category = el)
                    partner.category_middle.add(*develop_name)
                    partner.save()

    def vision_api_test():
        # 구글비전
        credential_path = '/Users/iyuchang/Downloads/decent-destiny-319206-20c01e01bd7c.json'
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
        client = vision.ImageAnnotatorClient()

        # 경로
        path = '/Users/iyuchang/Downloads/오솔찬/'
        file_list = os.listdir(path)
        for i in file_list:
            if i !='.DS_Store':
                uni1 = unicodedata.normalize('NFC',i)
                x =Partner.objects.filter(name=uni1)
                if x:
                    newPath = path+i+'/'
                    new_file_list = os.listdir(newPath)

                    for j in new_file_list:
                        j2 = j.split('.')[-1]
                        if j !='.DS_Store' and j2!='pptx' and j2!='pdf' and j2!='PDF'and j2!='html'and j2!='JFIF'and j2!='jfif':
                            with io.open(f'{newPath}{j}', 'rb') as f:
                                content = f.read()
                            image = vision.Image(content=content)
                            response = client.label_detection(image=image)
                            labels = response.label_annotations

                            label_list = []
                            label_score_list = []
                            for label in labels:
                                label_list.append(label.description)
                                label_score_list.append(label.score)


                            uni2 = unicodedata.normalize('NFC',j)
                            j_ = uni2.split('.')
                            if x[0].portfolio_set.filter(name=j_[0]):
                                pf=x[0].portfolio_set.filter(name=j_[0])[0]
                                for k in range(len(label_list)):
                                    Label.objects.create(
                                        portfolio = pf,
                                        label=label_list[k],
                                        score = label_score_list[k]
                                    )




class test():
    def test():
        # input_file = '/Users/iyuchang/Downloads/전국제조업체다알아버리기/hrefs_factory'
        # output_file = '/Users/iyuchang/Downloads/전국제조업체다알아버리기/hrefs_factory/result.csv' 
        input_file = '/Users/iyuchang/Downloads/전국제조업체다알아버리기/hrefs_rnd'
        output_file = '/Users/iyuchang/Downloads/전국제조업체다알아버리기/hrefs_rnd/result.csv' 
        allFile_list = glob.glob(os.path.join(input_file, 'href_*')) 
        allData = [] 
        for file in allFile_list:
            df = pd.read_csv(file,index_col = 0, encoding='CP949') 
            x = df['href'].str.split('/').str[2]
            df['href']=x
            x = df['href'].str.contains('kbank|industryland|seniormaeil|medicaltimes|koreanair|lotte|ujnews|jobplanet|chungbuk|www.donga.com|hankookilbo|jbtp|dcinside|incruit|jbcc|twitter|google|jobkorea|linkedin|cafe24|partsgo|life114|sentry|www.xn--hy1b74g2uem0k.xn--3e0b707e|tachyonnews|daiso|okkorea|slideshare|musinsa|icpart|data.go.kr|hangame|vymaps|coupang|fishinggroup|thingoolmarket|hotels|etoday|scourt|indeed|m.post.naver.comjhealthmedia|ecomedia| music.bugs.co.kr|reportshop|cscamera|michelin|joongang|apps.apple.com|incheon|pikicast|recruittimes|dailymedi|dobong|costco|susansijang|busaninnews|mail.kldc.co.kr|metroseoul|.png|rockwellautomation|wikipedia|post.naver.com|koreamg|jmagazine|cine21|earticle|foodb2b|coffeebann|rocketpunch|paxnetnews|softpowerup|pinterest|korean.dict.naver.com|hyundaicard|sisamagazine|jbroot|facebook|ebn.co.kr|melon|fashionn.com|coffeejob|shopping|lotterentacar|daangn|weeklytrade|kreport|bizkorea|fisheco|kaist|theteams|www.jeju.go.kr|youtub|techbiz|ticketlink|nett.kr|bizinfo|busan|band.us|presidentmedia|boardlife|airbnb|Infostockdaily|coolenjoy|ulsankyocharo|dorojuso|trello|www.wowtv.co.kr|femiwiki|instagram|wikitree|auction|chosun|shinailbo|bithumb|shop.cables.co.kr|happycampus|shopma|alldream|print.or.kr|g2b|gamejob|korea724|www.quest.comwww.cj.net|ommall|najuwork|danawa|opensalary|saramin|gongjangbang|hankyung|hancommds|tourbiz|career|worker.co.kr|yeogie|kosha|cctoday|kisreport|sportsseoul|wadiz|aladin|mss.go.kr|navimro|samsung|anjunj|krmcia|misumi|aving|thethegangsa|kakamuka|businesskoreadiscover-jeju|bizk.co.kr|boannews.com|bmw-motorrad|yes24|lfmall|ssg.com|daara|coupongil|edaily|hmgjournal|mangoplate|ssg|weeklypeople|tumblbug|store114|make24|lottecinema|fpost|www.seoul.co.krbusinesspost|tmon|wemakeprice|todayhumor|law.go.kr|bizno|pharmnews|ulsanpress|samcheok|broofa|dgeplus|gsshop|e-name|coupang.com|namu.wiki|somemap|apt4|forum.38.co.kr| kr.hotels.com|wanted|ebooth|blog.daum.net|seouljobs|collector|headlinejejuthefirstmedia|www.jejusori.net|11st|netflix|jobaba|happycampus|booking|the114|guyweb|yna.co.kr|cosinkorea|lotteon|allthatcompany|kakao.com|blog|cunews|ksilbbrunch|honam|hansolhomedeco|juso.app|moneypie|gmarket|sandan114|place.naver|news|dailian.co.kr|wix|reportworld|glowpick|tistory|kovwa|storefarm|catch|Wikipedia|megastudy|bizok.incheon.go.kr|kosis|myrealtrip|soco.seoul.go.kr|babosarang|interpark|hmall|114.co.kr|sedaily|newswire|jroot|databasesets|findjob|jejulavawater|sisanewstime|job.seoul.go.kr|weather.com|kookje|hanryeotoday|m.cafe.daum.net|campustown|yeogienews|redcross|anewsa|cafeshow|thesegye|e-jlmaeil|ymdaily|naver|daum|apple|dictionary|go.kr|.gov|amazon|.org|.edu|.or.kr|hackers|.ac.kr')
            allData.append(df[~x].drop_duplicates(['href']))

        dataCombine = pd.concat(allData, axis=0, ignore_index=True) 
        dataCombine.to_csv(output_file,encoding='CP949', index=True) 


        input_file = '/Users/iyuchang/Downloads/전국제조업체다알아버리기' 
        output_file = '/Users/iyuchang/Downloads/전국제조업체다알아버리기/email_result1.csv'
        input_file = '/Users/iyuchang/Downloads/전국제조업체다알아버리기/hrefs_rnd'
        output_file = '/Users/iyuchang/Downloads/전국제조업체다알아버리기/hrefs_rnd/result1.csv' 
        input_file = '/Users/iyuchang/Downloads/전국제조업체다알아버리기/hrefs_factory'
        output_file = '/Users/iyuchang/Downloads/전국제조업체다알아버리기/hrefs_factory/result12.csv' 
        allFile_list = glob.glob(os.path.join(input_file, 'factory_result_95746.csv')) 
        allData = [] 
        for file in allFile_list:
            df = pd.read_csv(file,index_col = 0) 
            x = df['name'].str.contains('건설|컨설팅|공단|협회|여행|캠핑|일보|물류')
            allData.append(df[~x])

        dataCombine = pd.concat(allData, axis=0, ignore_index=True) 
        print(len(dataCombine.index))
        dataCombine.to_csv(output_file,index=True) 

                                    

#-*- coding: cp949 -*-
from django.utils.deconstruct import deconstructible

from rest_framework.response import Response
import datetime
import os
import random
import string
import uuid
import enum
import requests
import json
import time
from .project.models import *

from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives


from google.cloud import vision
from base64 import b64encode
from google.protobuf import field_mask_pb2 as field_mask


class ResponseCode(enum.Enum):

    SUCCESS = 0
    FAIL = 1


@deconstructible
class FilenameChanger(object):

    def __init__(self, base_path):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.base_path = '{}/{}'.format(base_path, str(date))

    def __call__(self, instance, filename, *args, **kwargs):
        ext = filename.split('.')[-1].lower()
        filename = "%s.%s" % (uuid.uuid4(), ext)
        path = os.path.join(self.base_path, filename)
        print('[File] Upload File')
        print('- name : {}'.format(filename))
        print('- format : {}'.format(ext))
        print('- new name : {}'.format(filename))
        print('- path : {}'.format(path))
        return path

    def __eq__(self, other):
        return self.base_path


@deconstructible
class Util():

    @classmethod
    def add_unit(cls, value):
        UNIT = (
            (100000000, 'B'),
            (1000000, 'M'),
            (1000, 'K'),
            (1, ''),
        )
        for count, unit in UNIT:
            if value % count != value:
                number = round(value / count, 1)
                if (number*10)%10 == 0:
                    number = int(number)
                return '{number}{unit}'.format(number=str(number), unit=unit)
        return '{number}{unit}'.format(number=value, unit='')

    @classmethod
    def get_random_digit_letter(cls, length):
        result = ''
        for i in range(length):
            result += random.choice(string.digits)
        return str(result)

    @classmethod
    def get_random_letter(cls, length):
        result = ''
        for i in range(length):
            result += random.choice(string.digits + string.ascii_letters)
        return str(result)

class kakaotalk(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone_list, subject):
            # print(subject)
            # print(phone_list)
            # for phone in phone_list:
            #  print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #        'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'request_to_partner2',
            #                 'message': '파트너님에게 적합한 의뢰서가 도착했습니다.\n의뢰서명 : ' + subject,

            #               'button': [
            #                     {
            #                      'name': '확인하러 가기',
            #                      'type': 'WL',
            #                      'url_mobile': 'http://www.boltnnut.com',
            #                      'url_pc': 'http://www.boltnnut.com'
            #                  }
            #              ]}}}
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return 


class kakaotalk2(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone_list, subject, subclass,category):
            # print(subject)
            # print(phone_list)
            # for phone in phone_list:
            #  print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #        'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'request_to_partner3',
            #                 'message': '파트너님에게 적합한 의뢰서가 도착했습니다.\n의뢰서명 : ' + subject + '\n의뢰제품분야 : ' + str(subclass) + '\n제조의뢰분야 : ' + category,

            #               'button': [
            #                     {
            #                      'name': '확인하러 가기',
            #                      'type': 'WL',
            #                      'url_mobile': 'http://www.boltnnut.com',
            #                      'url_pc': 'http://www.boltnnut.com'
            #                  }
            #              ]}}}
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return


class kakaotalk_request(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone_list):
            # print(phone_list)
            # for phone in phone_list:
            #  #print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #        'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'answer_to_client',
            #                 'message': '고객님의 의뢰에 대한 전문가의 제안서가 도착하였습니다.\n\n* 해당 메시지는 고객님께서 요청하신 의뢰에 대한 제안이 있을 경우 발송됩니다',

            #               'button': [
            #                     {
            #                      'name': '확인하러 가기',
            #                      'type': 'WL',
            #                      'url_mobile': 'http://www.boltnnut.com',
            #                      'url_pc': 'http://www.boltnnut.com'
            #                  }
            #              ]}}}
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return

class kakaotalk_request_edit_end(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone):
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #          'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'request_edit_end',
            #                 'message':'고객님의 의뢰서 검토가 완료되어 파트너 제안서 모집이 시작되었습니다.\n\n제안서가 도착할 때마다 카카오톡 알림메시지를 보내드립니다.\n\n조금만 기다려주세요'}}}
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            #  return response
            return

class kakaotalk_send_information(object):
# 빈 전화번호 / 이상한 전화번호는 에러뜹니다.
        def send(phone_list, subject, content, price, period, file):
            # print(subject)
            # print(phone_list)
            # for phone in phone_list:
            #  print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #          'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_request_information3',
            #                 'message': '다음 의뢰를 주신 클라이언트에게 파트너님을 추천하고자합니다.\n클라이언트와 소통의사가 있으시면 ‘O’를, 없으시다면 ‘X’를 남겨주시길 바랍니다.\n\n해당 프로젝트를 진행할 의사가 있는 업체만 추천될 예정입니다.\n추천 후 클라이언트분께서 파트너님의 정보를 확인한 후 전화드릴 수 있습니다.\n\n의뢰제품 : ' + subject + '\n\n상담내용 : ' + content + '\n\n희망예산 : ' + price + '\n\n희망기간 : ' + period +  '\n\n의뢰파일 : ' + file
            #                 }
            #             }
            #          }
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return

class kakaotalk_send_IDPassword(object):
    def send(phoneNumber, username,title, password):
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message'
        data = {
            'account': 'boltnnut_korea', 
            'refkey': 'bolt123', 
            'type': 'at', 
            'from': '01028741248',
            'to': phoneNumber, 
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 
                    'templatecode': 'send_user_id_password',
                    'message': '안녕하세요. 볼트앤너트입니다.\n의뢰주신 ' + title + '의 가견적을 다시 확인할 수 있는\n의뢰 아이디와 비밀번호 안내드립니다.\n\n의뢰아이디 : '+ username + '\n비밀번호 : ' + password +'\n\n볼트앤너트 홈페이지에서 해당 아이디와 비밀번호로 로그인하신 후\n상단 메뉴창에서 기존 의뢰에서 의뢰 주신 '+title +'의 가견적을 재확인할 수 있습니다.'
                    }
                }
            }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response
        return

class kakaotalk_send_ID_ExistUser(object):
    def send(phoneNumber, username,title):
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message'
        data = {
            'account': 'boltnnut_korea', 
            'refkey': 'bolt123', 
            'type': 'at', 
            'from': '01028741248',
            'to': phoneNumber, 
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 
                    'templatecode': 'send_id_exist_user',
                    'message': '안녕하세요. 볼트앤너트입니다.\n의뢰주신 ' + title + '의 가견적을 다시 확인할 수 있는\n의뢰 아이디를 안내드립니다.\n\n의뢰아이디 : '+ username +'\n\n볼트앤너트 홈페이지에서 해당 아이디와 비밀번호로 로그인하신 후\n상단 메뉴창에서 기존 의뢰에서 의뢰 주신 '+title +'의 가견적을 재확인할 수 있습니다.'
                    }
                }
            }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response
        return

class kakaotalk_set_temp_password():
    def send(phoneNumber,tempPassword):
        #토큰 요청하고 저장
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

        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message'
        data = {
            'account': 'boltnnut_korea', 
            'refkey': 'bolt123', 
            'type': 'at', 
            'from': '01028741248',
            'to': phoneNumber, 
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 
                    'templatecode': 'set_temp_password',
                    'message': '[볼트앤너트] 회원님의 임시비밀번호를 카카오톡으로 보내드립니다.\n회원님의 임시비밀번호는 ' +  tempPassword + ' 입니다.\n\n회원님이 비밀번호를 변경하지 않았는데, 해당메세지를 받았을 시 볼트앤너트로 문의해주십시오.'
                    }
                }
            }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response
        return

class kakaotalk_send_meeting_confirm():
        def send(phoneNumber,requestCategory,requestTitle):
            # token = KakaoToken.objects.get(id=1)
            # Authorization = token.token
            
            # consultant1 = "노현수 기술팀장"
            # consultant2 = "최진영 기술이사"
            # consultant3 = Consultant.objects.order_by("?").filter(id__lt=9).first().name
            # print("랜덤 컨설턴트 : ",consultant3)
            # url = 'https://api.bizppurio.com/v3/message'
            # data = {
            #     'account': 'boltnnut_korea', 
            #     'refkey': 'bolt123', 
            #     'type': 'at', 
            #     'from': '01028741248',
            #     'to': phoneNumber, 
            #     'content': {
            #         'at': {
            #             'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_meeting_confirm',
            #             'message': '안녕하세요. 볼트앤너트입니다.\n\n의뢰주신 ' + requestTitle + '의 가견적은 잘 받아보셨나요?\n\n'+requestTitle +' 의뢰에는 '+requestCategory+'의 전문 컨설턴트인 ' + consultant1 +',' + consultant2 + ',' + consultant3 +'님이 배정되어 있습니다.\n\n볼트앤너트는 전문 컨설턴트의 상담을 통한 정확한 견적 서비스를 무료로 제공하고 있으니\n\n상담을 통해 '+requestTitle +'의 정확한 견적과 전문 지식을 알아보세요\n\n상담은 볼트앤너트 홈페이지에서 로그인하신 후 작성하신 의뢰 페이지에서 요청하실 수 있습니다.\n\n지금 바로 상담을 원하시면 볼트앤너트 상담 전화인 02-926-6637로 바로 전화주세요.',
            #             'button': [
            #                 {
            #                     'name': '무료 상담 받으러 가기',
            #                     'type': 'WL',
            #                     'url_mobile': 'https://www.boltnnut.com/',
            #                     'url_pc': 'https://www.boltnnut.com/'
            #                 }
            #             ]
            #         }
            #     }
            # }
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
            # response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return
          
class kakaotalk_send_meetin_content(object):
    def send(title, startAt, isOnline, phone):
        # try:
        #     message = "안녕하세요. 볼트앤너트입니다.\n의뢰주신 {title}에 전문 컨설턴트가 배정되어 상담을 진행할 예정입니다.\n{startAt}에 {place}에서 뵙겠습니다.\n{online}\n정확한 상담을 위해서 첨부된 링크에 포함된 상담 의뢰서를 작성해주시면\n담당 컨설턴트님께서 더욱 적합한 상담을 드릴 수 있습니다.\n추가적으로 궁금하신 사항이 있다면 {BnNPhone}, {BnNEmail}로 문의사항을 보내주세요.\n감사합니다.".format(
        #         title = title,
        #         startAt = startAt,
        #         place = '서울특별시 성북구 고려대로27길 3 2층' if not isOnline else 'ZooM 화상회의',
        #         online = 'ZooM 화상회의 주소는 미팅 1시간 전 다시 안내 드리겠습니다.\n' if isOnline else ' ',
        #         BnNPhone = '02-926-6637',
        #         BnNEmail = 'project@boltnnut.com'
        #     )
        #     token = KakaoToken.objects.get(id=1)
        #     Authorization = token.token
        #     url = 'https://api.bizppurio.com/v3/message'
        #     data = {
        #         'account': 'boltnnut_korea', 
        #         'refkey': 'bolt123', 
        #         'type': 'at', 
        #         'from': '01028741248',
        #         'to': phone, 
        #         'content': {
        #             'at': {
        #                 'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 
        #                 'templatecode': 'send_meeting_contentdaybefore2',
        #                 'message': message,
        #                 'button': [
        #                     {
        #                         'name': '상담의뢰서 받기',
        #                         'type': 'WL',
        #                         'url_mobile': 'https://boltnnutplatform.s3.ap-northeast-2.amazonaws.com/media/request/request.docx',
        #                         'url_pc': 'https://boltnnutplatform.s3.ap-northeast-2.amazonaws.com/media/request/request.docx'
        #                     }
        #                 ]
        #             }
        #         }
        #     }
        #     headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        #     response = requests.post(url, data=json.dumps(data), headers=headers)
        #     return response
        # except Exception as e:
        #     return e
        return

class kakaotalk_send_request_review():
        def send(phoneNumber,consultant,requestTitle):
            # token = KakaoToken.objects.get(id=1)
            # Authorization = token.token
            
            # url = 'https://api.bizppurio.com/v3/message'
            # data = {
            #     'account': 'boltnnut_korea', 
            #     'refkey': 'bolt123', 
            #     'type': 'at', 
            #     'from': '01028741248',
            #     'to': phoneNumber, 
            #     'content': {
            #         'at': {
            #             'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_request_review',
            #             'message': '안녕하세요. 볼트앤너트입니다.\n\n의뢰주신 ' + requestTitle + '에 대한 ' +consultant +'님의 상담은 어떠셨나요?\n\n 부족한 점이나 칭찬할만한 점이 있다면 첨부된 링크에서 리뷰를 작성해주세요.\n\n매달 리뷰를 작성해주신 고객분들 중 한 분을 선발하여 무료 모델링 서비스를 제공하고 있습니다.',
            #             'button': [
            #                 {
            #                     'name': '리뷰하러가기',
            #                     'type': 'WL',
            #                     'url_mobile': 'https://www.boltnnut.com/',
            #                     'url_pc': 'https://www.boltnnut.com/'
            #                 }
            #             ]
            #         }
            #     }
            # }
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
            # response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return

class kakaotalk_send_request_rerequest():
        def send(phoneNumber,requestTitle):
            # token = KakaoToken.objects.get(id=1)
            # Authorization = token.token
            # boltnnutPhone = "02-996-6637"
            # boltnnutEmail = "boltnnut@boltnnut.com"
            # url = 'https://api.bizppurio.com/v3/message'
            # data = {
            #     'account': 'boltnnut_korea', 
            #     'refkey': 'bolt123', 
            #     'type': 'at', 
            #     'from': '01028741248',
            #     'to': phoneNumber, 
            #     'content': {
            #         'at': {
            #             'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'bizp_2021020216131026670531311',
            #             'message': '안녕하세요. 볼트앤너트입니다.\n\n요청 주신 의뢰 : ' + requestTitle + '에는 전문가인\n\n최진영 기술이사님이 배정되어 있습니다.\n\n의뢰 기본정보와 5가지 선택질문만 답변해주시면 '+requestTitle+'의 가견적과\n\n전문 컨설턴트 상담을 무료로 받을 수 있으니 확인해보세요.\n\n온라인 의뢰 작성 시에 불편한 사항이 있었다면 '+ boltnnutPhone +' 혹은\n\n' + boltnnutEmail +'로 연락주세요.',
            #             'button': [
            #                 {
            #                     'name': '의뢰작성하러가기',
            #                     'type': 'WL',
            #                     'url_mobile': 'http://www.boltnnut.com/',
            #                     'url_pc': 'http://www.boltnnut.com/'
            #                 }
            #             ]
            #         }
            #     }
            # }
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
            # response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return

class kakaotalk_send_appreciate():
        def send(phoneNumber,requestTitle):
            # token = KakaoToken.objects.get(id=1)
            # Authorization = token.token
            # boltnnutPhone = "02-996-6637"
            # boltnnutEmail = "boltnnut@boltnnut.com"
            # url = 'https://api.bizppurio.com/v3/message'
            # data = {
            #     'account': 'boltnnut_korea', 
            #     'refkey': 'bolt123', 
            #     'type': 'at', 
            #     'from': '01028741248',
            #     'to': phoneNumber, 
            #     'content': {
            #         'at': {
            #             'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_appreciate',
            #             'message': '안녕하세요. 볼트앤너트입니다.\n\n볼트앤너트에 '+requestTitle +'의뢰를 주셔서 감사합니다.\n\n저희 볼트앤너트 서비스가 부족한 점이나 칭찬할만한 점이 있다면 첨부된 링크에서 리뷰를 작성해주세요.\n\n고객님께서 주신 소중한 의견 하나하나 귀기울여 듣고 부족한 점을 개선하도록 하겠습니다.\n\n매달 리뷰를 작성해주신 고객분들 중 한 분을 선발하여 무료 모델링 서비스를 제공하고 있습니다.\n\n볼트앤너트는 고객 분들의 의뢰 물품을 최적의 가격에 제대로 만들어드릴 수 있도록 노력하겠습니다.',
            #             'button': [
            #                 {
            #                     'name': '리뷰하러가기',
            #                     'type': 'WL',
            #                     'url_mobile': 'https://www.boltnnut.com/',
            #                     'url_pc': 'https://www.boltnnut.com/'
            #                 }
            #             ]
            #         }
            #     }
            # }
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
            # response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return

class kakaotalk_archiving_after_meeting():
        def send(phoneNumber,requestTitle):
            # token = KakaoToken.objects.get(id=1)
            # Authorization = token.token
            # boltnnutPhone = "02-996-6637"
            # boltnnutEmail = "boltnnut@boltnnut.com"
            # url = 'https://api.bizppurio.com/v3/message'
            # data = {
            #     'account': 'boltnnut_korea', 
            #     'refkey': 'bolt123', 
            #     'type': 'at', 
            #     'from': '01028741248',
            #     'to': phoneNumber, 
            #     'content': {
            #         'at': {
            #             'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_appreciate',
            #             'message': '안녕하세요. 볼트앤너트입니다.\n\n볼트앤너트에 '+requestTitle +'의뢰를 주셔서 감사합니다.\n\n저희 볼트앤너트 서비스가 부족한 점이나 칭찬할만한 점이 있다면 첨부된 링크에서 리뷰를 작성해주세요.\n\n고객님께서 주신 소중한 의견 하나하나 귀기울여 듣고 부족한 점을 개선하도록 하겠습니다.\n\n매달 리뷰를 작성해주신 고객분들 중 한 분을 선발하여 무료 모델링 서비스를 제공하고 있습니다.\n\n볼트앤너트는 고객 분들의 의뢰 물품을 최적의 가격에 제대로 만들어드릴 수 있도록 노력하겠습니다.',
            #             'button': [
            #                 {
            #                     'name': '의뢰작성하러가기',
            #                     'type': 'WL',
            #                     'url_mobile': 'https://www.boltnnut.com/',
            #                     'url_pc': 'https://www.boltnnut.com/'
            #                 }
            #             ]
            #         }
            #     }
            # }
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
            # response = requests.post(url, data=json.dumps(data), headers=headers)
            # return response
            return
            
# #-----------------------------------------------------------------------------------------------------------------#

class kakaotalk_send_response_msg():
        def send(phone_list, requestTitle):
            for phone in phone_list:
                token = KakaoToken.objects.get(id=1)
                Authorization = token.token
                boltnnutPhone = "02-996-6637"
                boltnnutEmail = "boltnnut@boltnnut.com"
                url = 'https://api.bizppurio.com/v3/message'
                data = {
                    'account': 'boltnnut_korea',
                    'refkey': 'bolt123', 
                    'type': 'at', 
                    'from': '01028741248',
                    'to': '01041376379',
                    'content': {
                        'at': {
                            'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'template_code': 'send_response_message',
                            'message': "안녕하세요 {phone.username}님.\n\n 상담 요청하신 "+requestTitle +"의뢰에 적합한 제조사가 문의 사항에 대한 댓글을 달아주셨어요.\n\n 댓글 내용을 확인해보시고 추가로 궁금하신 사항이 있다면 해당 제조사와의 소통을 통해 문의해주세요.",
                            'button': [
                                    {
                                    'name': '댓글 확인하기',
                                    'type': 'WL',
                                    'url_mobile': 'http://www.boltnnut.com',
                                    'url_pc': 'http://www.boltnnut.com'
                                }
                            ]
                        }
                    }
                }
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
                response = requests.post(url, data=json.dumps(data), headers=headers)
                return response

class kakaotalk_send_msg_request_week():
        def send(phone_list, requestTitle):
            for phone in phone_list:
                token = KakaoToken.objects.get(id=1)
                Authorization = token.token
                boltnnutPhone = "02-996-6637"
                boltnnutEmail = "boltnnut@boltnnut.com"
                url = 'https://api.bizppurio.com/v3/message'
                data = {
                    'account': 'boltnnut_korea',
                    'refkey': 'bolt123',
                    'type': 'at', 
                    'from': '01028741248',
                    'to': '01041376379',
                    'content': {
                        'at': {
                            'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'template_code': 'send_message_after_week',
                            'message': "안녕하세요 {phone.username}님.\n\n요청하신 "+requestTitle+" 상담에 문의 사항은 충분히 해결되셨나요?\n\n제조사와의 소통 과정을 통해 충분히 해소되지 않았다면 볼트앤너트 전문 컨설턴트에게 상담을 요청해보세요.\n\n컨설턴트께서 문의 사항을 확인하고 적합한 답변을 드릴 수 있습니다.",
                            'button': [
                                    {
                                    'name': '상담하기',
                                    'type': 'WL',
                                    'url_mobile': 'https://www.boltnnut.com/',
                                }
                            ]
                        }
                    }
                }
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
                response = requests.post(url, data=json.dumps(data), headers=headers)
                return response

# class kakaotalk_send_detail_inform():
#         def send(phone_list, requestTitle):
#             token = KakaoToken.objects.get(id=1)
#             Authorization = token.token
#             boltnnutPhone = "02-996-6637"
#             boltnnutEmail = "boltnnut@boltnnut.com"
#             url = 'https://api.bizppurio.com/v3/message'
#             data = {
#                 'account': 'boltnnut_korea',
#                 'refkey': 'bolt123', 
#                 'type': 'at', 
#                 'from': '01028741248',
#                 'to': phone_list,
#                 'content': {
#                     'at': {
#                         'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'template_code': 'notice_partner',
#                         'message': "안녕하세요. 볼트앤너트입니다.\n"+requestTitle +"의뢰에 대한 채팅이 시작되었습니다.\n준비가 되셨으면 시작해주세요.",
#                     }
#                 }
#             }
#             headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
#             response = requests.post(url, data=json.dumps(data), headers=headers)
#             return response

# class kakaotalk_send_chat_alarm():
#         def send(phone):
#             url = 'https://api.bizppurio.com/v3/message'
#             data = {
#                 'account': 'boltnnut_korea',
#                 'refkey': 'bolt123', 
#                 'type': 'at', 
#                 'from': '01028741248',
#                 'to': phone,
#                 'content': {
#                     'at': {
#                         'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'template_code': 'send_chat_alarm',
#                         'message': "안녕하세요. 볼트앤너트입니다.\n채팅에 대한 답변이 도착했습니다.",
#                     }
#                 }
#             }
            
class kakaotalk_send_msg_response():
        # 제조사의 채팅에 답변을 하지 않고 2일이 지난 경우 (의뢰당 1번만)
        def send(phone_list, requestTitle, partner_name):
            for phone in phone_list:
                token = KakaoToken.objects.get(id=1)
                Authorization = token.token
                boltnnutPhone = "02-996-6637"
                boltnnutEmail = "boltnnut@boltnnut.com"
                url = 'https://api.bizppurio.com/v3/message'
                data = {
                    'account': 'boltnnut_korea',
                    'refkey': 'bolt123',
                    'type': 'at', 
                    'from': '01028741248',
                    'to': '01041376379',
                    'content': {
                        'at': {
                            'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'template_code': 'send_message_about_response',
                            'message': "안녕하세요 {phone.username}님.\n\n"+requestTitle+" 상담에 매칭된 "+partner_name+"분께서 답변을 기다리고 있습니다.\n\n상담을 종료하고 싶으시다면 "+partner_name+"분께 안내해주세요.",
                            'button': [
                                    {
                                    'name': '답변하러 가기',
                                    'type': 'WL',
                                    'url_mobile': 'https://www.boltnnut.com/',
                                    'url_pc': 'https://www.boltnnut.com/'
                                }
                            ]
                        }
                    }
                }

# 수정 후
# class kakaotalk_request_answer():
#         def send(phone,requestTitle):
#             token = KakaoToken.objects.get(id=1)
#             Authorization = token.token
#             boltnnutPhone = "02-996-6637"
#             boltnnutEmail = "boltnnut@boltnnut.com"
#             url = 'https://api.bizppurio.com/v3/message'
#              data = {
#                 'account': 'boltnnut_korea',
#                 'refkey': 'bolt123',
#                 'type': 'at',
#                 'from': '01028741248',
#                 'to': phone,
#                 'content': {
#                     'at': {
#                         'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98',
#                         'templatecode': 'request',
#                         'message': '안녕하세요.' + phone.username + '님 상담 요청하신' + requestTitle + '에 적합한 제조사가 문의 사항에 대한 댓글을 달아 주셨어요\n\n 댓글 내용을 확인해보시고 추가로 궁금하신 사항이 있다면 해당 제조사와의 소통을 통해 문의해주세요',
#                         'button': [
#                             {
#                                 'name': '댓글 확인하기',
#                                 'type': 'WL',
#                                 'url_mobile': 'https://www.boltnnut.com/'',
#                                 'url_pc': 'https://www.boltnnut.com/'
#                             }
#                         ]
#                     }
#                 }
#             }
#             headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
#             response = requests.post(url, data=json.dumps(data), headers=headers)
#             return response





class kakaotalk_send_answer_to_client():
    def send(phone, username, requestTitle):
        #토큰 요청하고 저장
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

        #토큰 가져와서 api 보내기
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message/'
        data = {
            'account': 'boltnnut_korea',
            'refkey': 'bolt123',
            'type': 'at',
            'from': '01028741248',
            'to': phone,
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98',
                    'templatecode': 'send_answer_to_client',
                    'message': '안녕하세요 '+username+'님.\n요청하신 '+requestTitle+' 상담에 적합한 제조사가 문의주신 사항에 대한 답변을 제안주셨어요.\n답변 내용을 확인해보시고 추가로 궁금하신 사항은 해당 제조사와의 소통을 통해 문의해주세요.',
                    'button': [
                        {
                            'name': '제안서 확인하기',
                            'type': 'WL',
                            'url_mobile': 'https://www.boltnnut.com',
                            'url_pc': 'https://www.boltnnut.com' ,
                        }
                    ]
                }
            }
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(response.json())
        return response







class kakaotalk_chat_text():
    def send(phone, requestTitle, partner_name, chat_content):
        
        #토큰 요청하고 저장
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
        
        #토큰 가져와서 api 보내기
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message'
        data = {
            'account': 'boltnnut_korea',
            'refkey': 'bolt123',
            'type': 'at',
            'from': '01028741248',
            'to': phone,
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98',
                    'templatecode': 'send_chat_text',
                    'message': requestTitle + ' 상담에 매칭된 ' + partner_name + '님이 다음과 같이 답변을 주셨습니다.\n\n' + chat_content,
                    'button': [
                        {
                            'name': '답변하러 가기',
                            'type': 'WL',
                            'url_mobile': 'https://www.boltnnut.com',
                            'url_pc': 'https://www.boltnnut.com',
                        }
                    ]
                }
            }
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response

class kakaotalk_chat_file():
    def send(phone, requestTitle, partner_name, file):
        
        #토큰 요청하고 저장
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

        #토큰 가져와서 api 보내기
        token = KakaoToken.objects.get(id=1)
        Authorization = token.token
        url = 'https://api.bizppurio.com/v3/message'
        data = {
            'account': 'boltnnut_korea',
            'refkey': 'bolt123',
            'type': 'at',
            'from': '01028741248',
            'to': phone,
            'content': {
                'at': {
                    'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98',
                    'templatecode': 'send_chat_file',
                    'message': requestTitle + ' 상담에 매칭된 ' + partner_name + '님이 ' + file + ' 파일을 전달주셨습니다.',
                    'button': [
                        {
                            'name': '확인하러 가기',
                            'type': 'WL',
                            'url_mobile': 'https://www.boltnnut.com',
                            'url_pc': 'https://www.boltnnut.com',
                        }
                    ]
                }
            }
        }
        headers = {'Content-type': 'application/json', 'Accept': 'file/plain', 'Authorization': Authorization}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response



class jandi_webhook_answer():
    def send(title,clinetName):
        url = 'https://wh.jandi.com/connect-api/webhook/18069463/bf7dce120b1a85f9478b8460db6d07ad'
        headers = {
            'Accept': 'application/vnd.tosslab.jandi-v2+json',
            'Content-Type': 'application/json'
        }
        data = {
            "body" : "[볼트앤너트] "+clinetName+"님이 "+"<"+title+">"+"에 대한 제안서를 생성하였습니다.",
            }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response

class jandi_webhook_project():
    def send(title,clinetName):
        url = 'https://wh.jandi.com/connect-api/webhook/18069463/bf7dce120b1a85f9478b8460db6d07ad'
        headers = {
            'Accept': 'application/vnd.tosslab.jandi-v2+json',
            'Content-Type': 'application/json'
        }
        data = {
            "body" : "[볼트앤너트] " +clinetName+"님이 "+"<"+title+">"+" 프로젝트를 생성하였습니다.",
            }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response

    def send_requestInfo(title,clinetName):
        url = 'https://wh.jandi.com/connect-api/webhook/18069463/bf7dce120b1a85f9478b8460db6d07ad' 

        headers = {
            'Accept': 'application/vnd.tosslab.jandi-v2+json',
            'Content-Type': 'application/json'
        }
        data = {
            "body" : "[볼트앤너트] " +clinetName+"님이 "+"<"+title+">"+"  업체 수배 견적이 생성하였습니다.",
            }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response


class getIp():
    def get(a,b):
        x_forwarded_for = a
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = b

        if ip == '211.196.18.140' or ip == '211.216.28.238' or ip =='211.196.18.225' or ip =='59.5.24.185' or ip =='39.125.32.19' or ip =='220.116.11.139' or ip =='46.165.250.77' or ip=='54.86.50.139' or ip=='218.155.155.121' or ip=='218.155.155.121'or ip=='0.0.0.0' or ip=='211.196.18.166':
            ip = '0.0.0.0'
        
        
        return ip



class sendEmail():
    def send(username):
        recipient = [username]
        sender = "boltnnut@boltnnut.com"
        image_path = '/home/ubuntu/staging/boltnnut_platform/media/account/signUpGreeting.jpg'
        image_name = Path(image_path).name
        subject = "[온라인 제조 플랫폼] 전국 제조사 정보 다 있다, 볼트앤너트에 회원 가입이 완료되었습니다."
        text_message = f"{image_name}"
        html_message = f"""
        <!doctype html>
            <html lang=en>
                <head>
                    <meta charset=utf-8>
                    <title>Some title.</title>
                </head>
                <body>
                    <h3>{subject}</h1>
                    <p>
                    {username}님, 볼트앤너트에 가입해 주셔서 감사합니다.<br>
                    <img style="width: 800px;" src='cid:{image_name}'/>
                    </p>
                </body>
            </html>
        """
        email = EmailMultiAlternatives(subject=subject, body=text_message, from_email=sender, to=recipient)
        if all([html_message,image_path,image_name]):
            email.attach_alternative(html_message, "text/html")
            email.content_subtype = 'html' 
            email.mixed_subtype = 'related' 
            with open(image_path, mode='rb') as f:
                image = MIMEImage(f.read(),_subtype="jpg")
                email.attach(image)
                image.add_header('Content-ID', f"<{image_name}>")
        email.send()





class ImgSearch():
    def url(image_uri):            
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/ubuntu/staging/boltnnut_platform/.config/google/bolt-nut-289101-3be9837f46a7.json"
        project_id = 'bolt-nut-289101'
        location = 'asia-east1'
        product_set_id = 'product_set1'
        product_category = 'general-v1'
        filter = ""

        product_search_client = vision.ProductSearchClient()
        image_annotator_client = vision.ImageAnnotatorClient()

        # Create annotate image request along with product search feature.
        image_source = vision.ImageSource(image_uri=image_uri)
        image = vision.Image(source=image_source)

        # product search specific parameters
        product_set_path = product_search_client.product_set_path(
            project=project_id, location=location,
            product_set=product_set_id)
        product_search_params = vision.ProductSearchParams(
            product_set=product_set_path,
            product_categories=[product_category],
            filter=filter)
        image_context = vision.ImageContext(
            product_search_params=product_search_params)

        # Search products similar to the image.
        response = image_annotator_client.product_search(
            image, image_context=image_context)

        index_time = response.product_search_results.index_time

        results = response.product_search_results.results

        product_id= []
        product_score=[]
        for result in results:
        
            sc = str(result.score)
            SCORE = round (float(sc.rpartition(':')[-1]),3)

            uri = str(result.image)
            ID = int(uri.rpartition('/')[-1])
            
            product_id.append(ID)
            product_score.append(SCORE)

            
        return (product_id,product_score)

    def file(file):            
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/ubuntu/staging/boltnnut_platform/.config/google/bolt-nut-289101-3be9837f46a7.json"
        project_id = 'bolt-nut-289101'
        location = 'asia-east1'
        product_set_id = 'product_set1'
        product_category = 'general-v1'
        filter = ""

        # product_search_client is needed only for its helper methods.
        product_search_client = vision.ProductSearchClient()
        image_annotator_client = vision.ImageAnnotatorClient()

        content = file.read()

        # # Read the image as a stream of bytes.
        # with open(file_path, 'rb') as image_file:
        #     content = image_file.read()

        # Create annotate image request along with product search feature.
        image = vision.Image(content=content)

        # product search specific parameters
        product_set_path = product_search_client.product_set_path(
            project=project_id, location=location,
            product_set=product_set_id)
        product_search_params = vision.ProductSearchParams(
            product_set=product_set_path,
            product_categories=[product_category],
            filter=filter)
        image_context = vision.ImageContext(
            product_search_params=product_search_params)

        # Search products similar to the image.
        response = image_annotator_client.product_search(
            image, image_context=image_context)

        index_time = response.product_search_results.index_time
        print('Product set index time: ')
        print(index_time)

        results = response.product_search_results.results

        product_id= []
        product_score=[]
        for result in results:
        
            sc = str(result.score)
            SCORE = round (float(sc.rpartition(':')[-1]),3)

            uri = str(result.image)
            ID = int(uri.rpartition('/')[-1])
            
            product_id.append(ID)
            product_score.append(SCORE)

            
        return (product_id,product_score)


