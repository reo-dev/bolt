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

from apps.project.models import *
from apps.account.models import Portfolio

from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives

#import pandas as pd
import csv
import glob
import urllib.request

#from google.cloud import storage
from google.cloud import vision
from google.cloud import storage
from google.oauth2 import service_account
from base64 import b64encode
from google.protobuf import field_mask_pb2 as field_mask
import boto3
import time
import smtplib

# 이메일 메시지에 다양한 형식을 중첩하여 담기 위한 객체
from email.mime.multipart import MIMEMultipart

# 이메일 메시지를 이진 데이터로 바꿔주는 인코더
from email import encoders

# 텍스트 형식
from email.mime.text import MIMEText
# 이미지 형식
from email.mime.image import MIMEImage
# 오디오 형식
from email.mime.audio import MIMEAudio

# 위의 모든 객체들을 생성할 수 있는 기본 객체
# MIMEBase(_maintype, _subtype)
# MIMEBase(<메인 타입>, <서브 타입>)
from email.mime.base import MIMEBase

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

    
class jandi_webhook_QnA():
    def send_question(partner,client,content):
        url = 'https://wh.jandi.com/connect-api/webhook/18069463/bf7dce120b1a85f9478b8460db6d07ad'
        headers = {
            'Accept': 'application/vnd.tosslab.jandi-v2+json',
            'Content-Type': 'application/json'
        }
        data = {
            "body" : "[볼트앤너트] " +client+"님이 "+"파트너 "+partner+" 상세페이지에"+" 질문을 남겼습니다.. \n 내용 :" + content,
            }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response

    def send_answer_partner(partner,client,question,content):
        url = 'https://wh.jandi.com/connect-api/webhook/18069463/bf7dce120b1a85f9478b8460db6d07ad'
        headers = {
            'Accept': 'application/vnd.tosslab.jandi-v2+json',
            'Content-Type': 'application/json'
        }
        data = {
            "body" : "[볼트앤너트] " +client+"님이 "+"파트너 "+partner+" 상세페이지에 질문:"+question + "  에 대한 재질문을 남겼습니다.. \n 내용 :" + content,
            }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response

    def send_answer_client(partner,question,content):
        url = 'https://wh.jandi.com/connect-api/webhook/18069463/bf7dce120b1a85f9478b8460db6d07ad'
        headers = {
            'Accept': 'application/vnd.tosslab.jandi-v2+json',
            'Content-Type': 'application/json'
        }
        data = {
            "body" : "파트너 "+partner+" 상세페이지에 질문:"+question + "  에 대한 답글을 남겼습니다.. \n 내용 :" + content,
            }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response

class getIp():
    def get(a,b):
        #if문을 통해서 ip가 생김
        x_forwarded_for = a
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = b

        #회사 ip차단
        if ip == '59.5.24.185' or ip == '211.196.18.225' or ip =='211.216.28.238' or ip =='221.155.218.99' or ip =='14.39.62.53' or ip =='211.196.18.166' or ip=='172.30.1.3' or ip=='175.192.216.211' or ip=='211.216.28.238'or ip=='61.72.243.246' or ip=='211.216.20.250' or ip =='218.155.48.170' or ip =='59.5.24.185' or ip == '220.116.11.139'or ip == '59.5.75.76':
            ip = '0.0.0.0' 
        
        return ip



class sendEmail():
    def send(username):
        #이메일 템플릿 만들기
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

        #이메일에 jpg파일 첨부하기
        email = EmailMultiAlternatives(subject=subject, body=text_message, from_email=sender, to=recipient)
        if all([html_message,image_path,image_name]):
            email.attach_alternative(html_message, "text/html")
            email.content_subtype = 'html' 
            email.mixed_subtype = 'related' 
            with open(image_path, mode='rb') as f:
                image = MIMEImage(f.read(),_subtype="jpg",Name='서비스 소개서')
                email.attach(image)
                image.add_header('Content-ID', f"<{image_name}>")
        email.send()



                  
    def send_email(email):
        smtp_info = dict(
                         {"smtp_server" : "smtp.gmail.com",
                          "smtp_user_id" : "boltnnut@boltnnut.com" ,
                          "smtp_user_pw" : "hppsgcaehybluwsr" ,
                          "smtp_port" : 587}
                        )

        msg_dict = {
            'image' : {'maintype' : 'image', 'subtype' :'jpg', 'filename' :'/home/ubuntu/staging/boltnnut_platform/media/account/signUpGreeting.jpg'}, # 이미지 첨부파일
        }

        title = "[온라인 제조 플랫폼] 전국 제조사 정보 다 있다, 볼트앤너트에 회원 가입이 완료되었습니다."
        content = "[온라인 제조 플랫폼] 전국 제조사 정보 다 있다, 볼트앤너트에 회원 가입이 완료되었습니다."
        sender = "boltnnut@boltnnut.com"
        receiver =  email

        # 메일 내용
        msg = MIMEText(_text = content, _charset = "utf-8") 

        # 첨부파일 추가
        multi = sendEmail.make_multimsg(msg_dict,receiver)
        multi['subject'] = title  
        multi['from'] = sender  
        multi['to'] = receiver     
        multi.attach(msg)
       
        with smtplib.SMTP(smtp_info["smtp_server"], smtp_info["smtp_port"]) as server:
            # TLS 보안 연결
            server.starttls() 
            # 로그인
            server.login(smtp_info["smtp_user_id"], smtp_info["smtp_user_pw"])
            # 로그인 된 서버에 이메일 전송
            response = server.sendmail(multi['from'], multi['to'], multi.as_string()) # 메시지를 보낼때는 .as_string() 메소드를 사용해서 문자열로 바꿔줍니다.


    def make_multimsg(msg_dict,username):

        multi = MIMEMultipart(_subtype='mixed')
        image_path = '/home/ubuntu/staging/boltnnut_platform/media/account/signUpGreeting.jpg'
        image_name = Path(image_path).name

        html_message = f"""
        <!doctype html>
            <html lang=en>
                <head>
                    <meta charset=utf-8>
                    <title>Some title.</title>
                </head>
                <body>
                    <h3>"[온라인 제조 플랫폼] 전국 제조사 정보 다 있다, 볼트앤너트에 회원 가입이 완료되었습니다."</h1>
                    <p>
                    {username}님, 볼트앤너트에 가입해 주셔서 감사합니다.<br>
                    <img style="width: 800px;" src='cid:{image_name}'/>
                    </p>
                </body>
            </html>
        """
        html_body = MIMEText(html_message, 'html')
        multi.attach(html_body)

        for key, value in msg_dict.items():
            with open(value['filename'], 'rb') as fp:
                msg = MIMEImage(fp.read(), _subtype=value['subtype'],Name='서비스 소개서')
            msg.add_header('Content-ID', f"<{image_name}>")
            multi.attach(msg)
        
        return multi


class ImgSearch():

    def upload_blob(bucket_name,destination_blob_name, url,id):
        # bucket_name = "your-bucket-name"
        # source_file_name = "local/path/to/file"
        # destination_blob_name = "storage-object-name"
        try :
            s3_path = "https://boltnnutplatform.s3.amazonaws.com/media/"
            source_file_name = os.path.dirname(os.path.abspath(__file__))  + '/temp_img/' + id
            img_url = s3_path + url
            print(img_url +" s3에서 버킷으로 저장시작" +source_file_name)
            urllib.request.urlretrieve(img_url, source_file_name)

            print(id +"s3에서 버킷으로 저장완료")
            time.sleep(0.01)

            print(id +"google 저장시작")
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)

            print(
                "File {} uploaded to {}. \n".format(
                    source_file_name, destination_blob_name
                )
            )
            time.sleep(0.01)
            os.remove(source_file_name)
        except Exception as e :
            print(e)
            ImgSearch.upload_blob(bucket_name,destination_blob_name, url,id)

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


    def dataset(low_ID) :
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/ubuntu/staging/boltnnut_platform/.config/google/bolt-nut-289101-3be9837f46a7.json"
        #vision
        project_id = 'bolt-nut-289101'
        location = 'asia-east1'
        product = 'product_set1'
        product_category = 'general-v1'
        bucket_name = "boltnnut"

        #google storage
        date_str =str(datetime.datetime.today()).split(" ")[0]
        gs_path =  "portfolio_img-"+date_str+"/"
        csv_name = "Portfolio-"+date_str+".csv"
        csv_path_local = os.path.dirname(os.path.abspath(__file__))  + '/temp_img/' + csv_name



        
        # low_Id보다 큰 포트폴리오에 접근
        pf_qs = Portfolio.objects.filter(id__gte = low_ID).order_by("-id")
        

        output_csv = []
        count=0
        for pf in pf_qs :
            #s3에서 google data studio로 이동
            pf_url = str(pf.img_portfolio)
            img_url = gs_path+str(pf.id)
            
            
            ImgSearch.upload_blob(bucket_name, img_url, pf_url, str(pf.id))
            count+= 1



            #make csv
            img_id = str(pf.id)
            product_set_id = "product_set1"
            product_id = "product_id" + str(pf.id)
            category = "general-v1"
            pdn = ""
            label = ""
            bound_box =""

            row_list = [img_url,img_id,product_set_id,product_id,category,pdn,label,bound_box]
            output_csv.append(row_list)
            
        with open(csv_path_local,'w') as file :
            write = csv.writer(file)
            write.writerows(output_csv)

        print(count +'개 업로드\n' '쿼리셋 개수 : '+ count(pf_qs))
        
        
            
        
