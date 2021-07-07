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
# from .project.cron import *

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
# �� ��ȭ��ȣ / �̻��� ��ȭ��ȣ�� ������ϴ�.
        def send(phone_list, subject):
            # print(subject)
            # print(phone_list)
            # for phone in phone_list:
            #  print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #        'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'request_to_partner2',
            #                 'message': '��Ʈ�ʴԿ��� ������ �Ƿڼ��� �����߽��ϴ�.\n�Ƿڼ��� : ' + subject,

            #               'button': [
            #                     {
            #                      'name': 'Ȯ���Ϸ� ����',
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
# �� ��ȭ��ȣ / �̻��� ��ȭ��ȣ�� ������ϴ�.
        def send(phone_list, subject, subclass,category):
            # print(subject)
            # print(phone_list)
            # for phone in phone_list:
            #  print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #        'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'request_to_partner3',
            #                 'message': '��Ʈ�ʴԿ��� ������ �Ƿڼ��� �����߽��ϴ�.\n�Ƿڼ��� : ' + subject + '\n�Ƿ���ǰ�о� : ' + str(subclass) + '\n�����Ƿںо� : ' + category,

            #               'button': [
            #                     {
            #                      'name': 'Ȯ���Ϸ� ����',
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
# �� ��ȭ��ȣ / �̻��� ��ȭ��ȣ�� ������ϴ�.
        def send(phone_list):
            # print(phone_list)
            # for phone in phone_list:
            #  #print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #        'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'answer_to_client',
            #                 'message': '������ �Ƿڿ� ���� �������� ���ȼ��� �����Ͽ����ϴ�.\n\n* �ش� �޽����� ���Բ��� ��û�Ͻ� �Ƿڿ� ���� ������ ���� ��� �߼۵˴ϴ�',

            #               'button': [
            #                     {
            #                      'name': 'Ȯ���Ϸ� ����',
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
# �� ��ȭ��ȣ / �̻��� ��ȭ��ȣ�� ������ϴ�.
        def send(phone):
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #          'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'request_edit_end',
            #                 'message':'������ �Ƿڼ� ���䰡 �Ϸ�Ǿ� ��Ʈ�� ���ȼ� ������ ���۵Ǿ����ϴ�.\n\n���ȼ��� ������ ������ īī���� �˸��޽����� �����帳�ϴ�.\n\n���ݸ� ��ٷ��ּ���'}}}
            #  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #  response = requests.post(url, data=json.dumps(data), headers=headers)
            #  return response
            return

class kakaotalk_send_information(object):
# �� ��ȭ��ȣ / �̻��� ��ȭ��ȣ�� ������ϴ�.
        def send(phone_list, subject, content, price, period, file):
            # print(subject)
            # print(phone_list)
            # for phone in phone_list:
            #  print(phone)
            #  url = 'https://api.bizppurio.com/v1/message'
            #  data = {'account': 'boltnnut_korea', 'refkey': 'bolt123', 'type': 'at', 'from': '01028741248',
            #          'to': phone, 'content': {
            #          'at': {'senderkey': '44e4fdc989b12906c82fc46e428dd91dd99f0d98', 'templatecode': 'send_request_information3',
            #                 'message': '���� �Ƿڸ� �ֽ� Ŭ���̾�Ʈ���� ��Ʈ�ʴ��� ��õ�ϰ����մϴ�.\nŬ���̾�Ʈ�� �����ǻ簡 �����ø� ��O����, �����ôٸ� ��X���� �����ֽñ� �ٶ��ϴ�.\n\n�ش� ������Ʈ�� ������ �ǻ簡 �ִ� ��ü�� ��õ�� �����Դϴ�.\n��õ �� Ŭ���̾�Ʈ�в��� ��Ʈ�ʴ��� ������ Ȯ���� �� ��ȭ�帱 �� �ֽ��ϴ�.\n\n�Ƿ���ǰ : ' + subject + '\n\n��㳻�� : ' + content + '\n\n������� : ' + price + '\n\n����Ⱓ : ' + period +  '\n\n�Ƿ����� : ' + file
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
                    'message': '�ȳ��ϼ���. ��Ʈ�س�Ʈ�Դϴ�.\n�Ƿ��ֽ� ' + title + '�� �������� �ٽ� Ȯ���� �� �ִ�\n�Ƿ� ���̵�� ��й�ȣ �ȳ��帳�ϴ�.\n\n�Ƿھ��̵� : '+ username + '\n��й�ȣ : ' + password +'\n\n��Ʈ�س�Ʈ Ȩ���������� �ش� ���̵�� ��й�ȣ�� �α����Ͻ� ��\n��� �޴�â���� ���� �Ƿڿ��� �Ƿ� �ֽ� '+title +'�� �������� ��Ȯ���� �� �ֽ��ϴ�.'
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
                    'message': '�ȳ��ϼ���. ��Ʈ�س�Ʈ�Դϴ�.\n�Ƿ��ֽ� ' + title + '�� �������� �ٽ� Ȯ���� �� �ִ�\n�Ƿ� ���̵� �ȳ��帳�ϴ�.\n\n�Ƿھ��̵� : '+ username +'\n\n��Ʈ�س�Ʈ Ȩ���������� �ش� ���̵�� ��й�ȣ�� �α����Ͻ� ��\n��� �޴�â���� ���� �Ƿڿ��� �Ƿ� �ֽ� '+title +'�� �������� ��Ȯ���� �� �ֽ��ϴ�.'
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
                    'message': '[��Ʈ�س�Ʈ] ȸ������ �ӽú�й�ȣ�� īī�������� �����帳�ϴ�.\nȸ������ �ӽú�й�ȣ�� ' +  tempPassword + ' �Դϴ�.\n\nȸ������ ��й�ȣ�� �������� �ʾҴµ�, �ش�޼����� �޾��� �� ��Ʈ�س�Ʈ�� �������ֽʽÿ�.'
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
            
            # consultant1 = "������ �������"
            # consultant2 = "������ ����̻�"
            # consultant3 = Consultant.objects.order_by("?").filter(id__lt=9).first().name
            # print("���� ������Ʈ : ",consultant3)
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
            #             'message': '�ȳ��ϼ���. ��Ʈ�س�Ʈ�Դϴ�.\n\n�Ƿ��ֽ� ' + requestTitle + '�� �������� �� �޾ƺ��̳���?\n\n'+requestTitle +' �Ƿڿ��� '+requestCategory+'�� ���� ������Ʈ�� ' + consultant1 +',' + consultant2 + ',' + consultant3 +'���� �����Ǿ� �ֽ��ϴ�.\n\n��Ʈ�س�Ʈ�� ���� ������Ʈ�� ����� ���� ��Ȯ�� ���� ���񽺸� ����� �����ϰ� ������\n\n����� ���� '+requestTitle +'�� ��Ȯ�� ������ ���� ������ �˾ƺ�����\n\n����� ��Ʈ�س�Ʈ Ȩ���������� �α����Ͻ� �� �ۼ��Ͻ� �Ƿ� ���������� ��û�Ͻ� �� �ֽ��ϴ�.\n\n���� �ٷ� ����� ���Ͻø� ��Ʈ�س�Ʈ ��� ��ȭ�� 02-926-6637�� �ٷ� ��ȭ�ּ���.',
            #             'button': [
            #                 {
            #                     'name': '���� ��� ������ ����',
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
        #     message = "�ȳ��ϼ���. ��Ʈ�س�Ʈ�Դϴ�.\n�Ƿ��ֽ� {title}�� ���� ������Ʈ�� �����Ǿ� ����� ������ �����Դϴ�.\n{startAt}�� {place}���� �˰ڽ��ϴ�.\n{online}\n��Ȯ�� ����� ���ؼ� ÷�ε� ��ũ�� ���Ե� ��� �Ƿڼ��� �ۼ����ֽø�\n��� ������Ʈ�Բ��� ���� ������ ����� �帱 �� �ֽ��ϴ�.\n�߰������� �ñ��Ͻ� ������ �ִٸ� {BnNPhone}, {BnNEmail}�� ���ǻ����� �����ּ���.\n�����մϴ�.".format(
        #         title = title,
        #         startAt = startAt,
        #         place = '����Ư���� ���ϱ� ������27�� 3 2��' if not isOnline else 'ZooM ȭ��ȸ��',
        #         online = 'ZooM ȭ��ȸ�� �ּҴ� ���� 1�ð� �� �ٽ� �ȳ� �帮�ڽ��ϴ�.\n' if isOnline else ' ',
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
        #                         'name': '����Ƿڼ� �ޱ�',
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
            #             'message': '�ȳ��ϼ���. ��Ʈ�س�Ʈ�Դϴ�.\n\n�Ƿ��ֽ� ' + requestTitle + '�� ���� ' +consultant +'���� ����� ��̳���?\n\n ������ ���̳� Ī���Ҹ��� ���� �ִٸ� ÷�ε� ��ũ���� ���並 �ۼ����ּ���.\n\n�Ŵ� ���並 �ۼ����ֽ� ���е� �� �� ���� �����Ͽ� ���� �𵨸� ���񽺸� �����ϰ� �ֽ��ϴ�.',
            #             'button': [
            #                 {
            #                     'name': '�����Ϸ�����',
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
            #             'message': '�ȳ��ϼ���. ��Ʈ�س�Ʈ�Դϴ�.\n\n��û �ֽ� �Ƿ� : ' + requestTitle + '���� ��������\n\n������ ����̻���� �����Ǿ� �ֽ��ϴ�.\n\n�Ƿ� �⺻������ 5���� ���������� �亯���ֽø� '+requestTitle+'�� ��������\n\n���� ������Ʈ ����� ����� ���� �� ������ Ȯ���غ�����.\n\n�¶��� �Ƿ� �ۼ� �ÿ� ������ ������ �־��ٸ� '+ boltnnutPhone +' Ȥ��\n\n' + boltnnutEmail +'�� �����ּ���.',
            #             'button': [
            #                 {
            #                     'name': '�Ƿ��ۼ��Ϸ�����',
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
            #             'message': '�ȳ��ϼ���. ��Ʈ�س�Ʈ�Դϴ�.\n\n��Ʈ�س�Ʈ�� '+requestTitle +'�Ƿڸ� �ּż� �����մϴ�.\n\n���� ��Ʈ�س�Ʈ ���񽺰� ������ ���̳� Ī���Ҹ��� ���� �ִٸ� ÷�ε� ��ũ���� ���並 �ۼ����ּ���.\n\n���Բ��� �ֽ� ������ �ǰ� �ϳ��ϳ� �ͱ�￩ ��� ������ ���� �����ϵ��� �ϰڽ��ϴ�.\n\n�Ŵ� ���並 �ۼ����ֽ� ���е� �� �� ���� �����Ͽ� ���� �𵨸� ���񽺸� �����ϰ� �ֽ��ϴ�.\n\n��Ʈ�س�Ʈ�� �� �е��� �Ƿ� ��ǰ�� ������ ���ݿ� ����� �����帱 �� �ֵ��� ����ϰڽ��ϴ�.',
            #             'button': [
            #                 {
            #                     'name': '�����Ϸ�����',
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
            #             'message': '�ȳ��ϼ���. ��Ʈ�س�Ʈ�Դϴ�.\n\n��Ʈ�س�Ʈ�� '+requestTitle +'�Ƿڸ� �ּż� �����մϴ�.\n\n���� ��Ʈ�س�Ʈ ���񽺰� ������ ���̳� Ī���Ҹ��� ���� �ִٸ� ÷�ε� ��ũ���� ���並 �ۼ����ּ���.\n\n���Բ��� �ֽ� ������ �ǰ� �ϳ��ϳ� �ͱ�￩ ��� ������ ���� �����ϵ��� �ϰڽ��ϴ�.\n\n�Ŵ� ���並 �ۼ����ֽ� ���е� �� �� ���� �����Ͽ� ���� �𵨸� ���񽺸� �����ϰ� �ֽ��ϴ�.\n\n��Ʈ�س�Ʈ�� �� �е��� �Ƿ� ��ǰ�� ������ ���ݿ� ����� �����帱 �� �ֵ��� ����ϰڽ��ϴ�.',
            #             'button': [
            #                 {
            #                     'name': '�Ƿ��ۼ��Ϸ�����',
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
                            'message': "�ȳ��ϼ��� {phone.username}��.\n\n ��� ��û�Ͻ� "+requestTitle +"�Ƿڿ� ������ �����簡 ���� ���׿� ���� ����� �޾��ּ̾��.\n\n ��� ������ Ȯ���غ��ð� �߰��� �ñ��Ͻ� ������ �ִٸ� �ش� ��������� ������ ���� �������ּ���.",
                            'button': [
                                    {
                                    'name': '��� Ȯ���ϱ�',
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
                            'message': "�ȳ��ϼ��� {phone.username}��.\n\n��û�Ͻ� "+requestTitle+" ��㿡 ���� ������ ����� �ذ�Ǽ̳���?\n\n��������� ���� ������ ���� ����� �ؼҵ��� �ʾҴٸ� ��Ʈ�س�Ʈ ���� ������Ʈ���� ����� ��û�غ�����.\n\n������Ʈ���� ���� ������ Ȯ���ϰ� ������ �亯�� �帱 �� �ֽ��ϴ�.",
                            'button': [
                                    {
                                    'name': '����ϱ�',
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
#                         'message': "�ȳ��ϼ���. ��Ʈ�س�Ʈ�Դϴ�.\n"+requestTitle +"�Ƿڿ� ���� ä���� ���۵Ǿ����ϴ�.\n�غ� �Ǽ����� �������ּ���.",
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
#                         'message': "�ȳ��ϼ���. ��Ʈ�س�Ʈ�Դϴ�.\nä�ÿ� ���� �亯�� �����߽��ϴ�.",
#                     }
#                 }
#             }
            
class kakaotalk_send_msg_response():
        # �������� ä�ÿ� �亯�� ���� �ʰ� 2���� ���� ��� (�Ƿڴ� 1����)
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
                            'message': "�ȳ��ϼ��� {phone.username}��.\n\n"+requestTitle+" ��㿡 ��Ī�� "+partner_name+"�в��� �亯�� ��ٸ��� �ֽ��ϴ�.\n\n����� �����ϰ� �����ôٸ� "+partner_name+"�в� �ȳ����ּ���.",
                            'button': [
                                    {
                                    'name': '�亯�Ϸ� ����',
                                    'type': 'WL',
                                    'url_mobile': 'https://www.boltnnut.com/',
                                    'url_pc': 'https://www.boltnnut.com/'
                                }
                            ]
                        }
                    }
                }

# ���� ��
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
#                         'message': '�ȳ��ϼ���.' + phone.username + '�� ��� ��û�Ͻ�' + requestTitle + '�� ������ �����簡 ���� ���׿� ���� ����� �޾� �ּ̾��\n\n ��� ������ Ȯ���غ��ð� �߰��� �ñ��Ͻ� ������ �ִٸ� �ش� ��������� ������ ���� �������ּ���',
#                         'button': [
#                             {
#                                 'name': '��� Ȯ���ϱ�',
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
        #��ū ��û�ϰ� ����
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

        #��ū �����ͼ� api ������
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
                    'message': '�ȳ��ϼ��� '+username+'��.\n��û�Ͻ� '+requestTitle+' ��㿡 ������ �����簡 �����ֽ� ���׿� ���� �亯�� �����ּ̾��.\n�亯 ������ Ȯ���غ��ð� �߰��� �ñ��Ͻ� ������ �ش� ��������� ������ ���� �������ּ���.',
                    'button': [
                        {
                            'name': '���ȼ� Ȯ���ϱ�',
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
        
        #��ū ��û�ϰ� ����
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
        
        #��ū �����ͼ� api ������
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
                    'message': requestTitle + ' ��㿡 ��Ī�� ' + partner_name + '���� ������ ���� �亯�� �ּ̽��ϴ�.\n\n' + chat_content,
                    'button': [
                        {
                            'name': '�亯�Ϸ� ����',
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
        
        #��ū ��û�ϰ� ����
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

        #��ū �����ͼ� api ������
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
                    'message': requestTitle + ' ��㿡 ��Ī�� ' + partner_name + '���� ' + file + ' ������ �����ּ̽��ϴ�.',
                    'button': [
                        {
                            'name': 'Ȯ���Ϸ� ����',
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
            "body" : "[��Ʈ�س�Ʈ] "+clinetName+"���� "+"<"+title+">"+"�� ���� ���ȼ��� �����Ͽ����ϴ�.",
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
            "body" : "[��Ʈ�س�Ʈ] " +clinetName+"���� "+"<"+title+">"+" ������Ʈ�� �����Ͽ����ϴ�.",
            }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response