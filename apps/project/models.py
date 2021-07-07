#-*- coding: cp949 -*-
import os, datetime, uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from apps.category.models import *
from apps.account.models import *
from typing import TYPE_CHECKING

from ckeditor_uploader.fields import RichTextUploadingField

from hashids import Hashids
from django.core.validators import MaxValueValidator

#�ð� ���� �Լ�
from django.utils import timezone
from datetime import date

def project_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "project/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_project" + "." + ext
    return os.path.join(path, format)

def request_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "request/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = filename
    return os.path.join(path, format)

def answer_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "answer/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_answer" + "." + ext
    return os.path.join(path, format)

def chat_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "chat/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = filename
    return os.path.join(path, format)

def time():
    time = timezone.now()
    return time


# ------------------------------------------------------------------
# Model   : ProjectStatus
# Description : ������Ʈ ���� �� : ������Ʈ�� ���� ����(��� �� ��)�� üũ�ϱ� ���� �𵨷� admin ������ ���� ���� 
# ------------------------------------------------------------------

class ProjectStatus(models.Model):
    name = models.CharField('��Ȳ',max_length =256)

    class Meta:
        verbose_name = '     ������Ʈ�����Ȳ'
        verbose_name_plural = '     ������Ʈ�����Ȳ'

    def __str__(self):
        return str(self.name)
        
# ------------------------------------------------------------------
# Model   : Manager
# Description : ������Ʈ ����� �� : ������Ʈ�� ����ڸ� üũ�ϱ� ���� �𵨷� admin ������ ���� ���� 
# ------------------------------------------------------------------

class Manager(models.Model):
    name = models.CharField('�Ŵ���',max_length=150)

    class Meta:
        verbose_name = '     ������Ʈ�����'
        verbose_name_plural = '     ������Ʈ�����'

    def __str__(self):
        return str(self.name)
        
# ------------------------------------------------------------------
# Model   : Project
# Description : ������Ʈ �� : ������Ʈ�� ���õ� �������� ��� �ְ� ���� �𵨷� request(�Ƿڼ�)�� answer(���ȼ�)�� ����ϰ� ����
# ------------------------------------------------------------------
class Project(models.Model):

    PROGRESS = [
    ('������', "������"),
    ('��������' ,"��������"),
    ]

    TRANSFER = [
    ('�ƴϿ�', '�ƴϿ�'),
    ('�����Ա�', '�����Ա�'),
    ('�ϳ�', '�ϳ�'),
    ]

    STEP = [
        ('�����Է�', '�����Է�'),
        ('��������', '��������'),
        ('����û', '����û'),
    ]

    createdAt = models.DateTimeField('�������', default=timezone.now)
    status = models.CharField('������Ʈ ����', max_length=10, default="������", blank=True, choices=PROGRESS, null=True)
    title = models.CharField('������Ʈ ����', max_length = 150, blank=True, null=True)
    transferMoney = models.CharField('�Ա� ����', max_length=10, default='�ƴϿ�', choices=TRANSFER)
    memo = models.TextField('�ǵ��', blank=True, null=True)
    manager = models.ForeignKey(Manager, on_delete = models.CASCADE, verbose_name='�����',related_name='project', null=True)
    #project_status = models.ForeignKey(ProjectStatus, on_delete = models.CASCADE, verbose_name='��Ȳ',related_name='project', null=True)
    progressStep = models.CharField('�� ���� �ܰ�', max_length=10, default='', choices=STEP)
    estimate = models.IntegerField('����', blank=True, null=True, default=0) 
    explain = models.TextField('����', blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='�ۼ�Ŭ���̾�Ʈ',null=True) # �ۼ��� Ŭ���̾�Ʈ FK
    reason = models.CharField('�� �Ƿ� ����', max_length=256, blank=True, null=True)


    class Meta:
        verbose_name = '     ������Ʈ'
        verbose_name_plural = '     ������Ʈ'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Request
# Description : �Ƿڼ� �� 
# ------------------------------------------------------------------
class Request(models.Model):

    request_state = [
        ('����û', '����û'),
        ('��������', '��������'),
        ('��ü����', '��ü����'),
    ]

    deadline_state = [
        ('�����Ϲ���', '�����Ϲ���'),
        ('���������ǰ���', '���������ǰ���'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='�ۼ�Ŭ���̾�Ʈ')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='������Ʈ')
    request_state = models.CharField('���� ����', max_length=10, default='', choices=request_state)
    name = models.CharField('����', max_length=256, blank=True, null=True)
    deadline = models.DateTimeField('������', default=timezone.now, null=True)
    deadline_state = models.CharField('������ ����', max_length=10, default='', choices=deadline_state)
    order_request_open = models.CharField('���� ���� ��û����', max_length=5000, blank=True, null=True)
    order_request_close = models.CharField('����� ���� ��û����', max_length=5000, blank=True, null=True)
    createdAt = models.DateTimeField('�������', default=timezone.now)
    price = models.IntegerField('������', blank=True, null=True) # ���� ������ ������Ʈ�� ���� ����� ������ ������

    class Meta:
        verbose_name = '     ��û�� �Ƿ�'
        verbose_name_plural = '     ��û�� �Ƿ�'

    def __str__(self):
        return str(self.name)

# ------------------------------------------------------------------
# Model   : RequestFile
# Description : �Ƿڼ� ���� �� : �Ƿڼ��� ÷���� ���� ���ε� �ߺ��� �Ǿ ������ �ʿ���
# ------------------------------------------------------------------
class RequestFile(models.Model):
    request = models.ForeignKey(Request, on_delete = models.CASCADE, verbose_name= '�Ƿڼ�')
    file = models.FileField('�Ƿ�����', upload_to=request_update_filename, blank=False, null=False, max_length=255)
    share_inform = models.BooleanField('���� ���� üũ', default=False)

    class Meta:
        verbose_name = '     ��ǰ �⺻���� ÷������'
        verbose_name_plural = '     ��ǰ �⺻���� ÷������'
    def __str__ (self):
        return str(self.request) + ' �Ƿڼ�'


# ------------------------------------------------------------------
# Model   : Select_save
# Description : �Ƿμ��� ����Ǵ� ��������/�亯 �� : ������ ������ ���� �亯�� ���� �����ε� �� ������ ���� ��ȭ�� �Ǳ� ������ ������� ���� �����̳� ���� ���ɼ� ����
# ------------------------------------------------------------------
class Select_save(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name='�Ƿڼ�')
    category = models.ForeignKey(Develop, on_delete=models.CASCADE, verbose_name='���ߺо�')
    question = models.CharField('��������', max_length=256, blank=True, null=True)
    answer = models.CharField('���������亯', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '     �Ƿڼ��� ����Ǵ� ��������/�亯'
        verbose_name_plural = '     �Ƿڼ��� ����Ǵ� ��������/�亯'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Select
# Description : �������� �� : �� �������� �� ���� ������� �� ���ص����� ����... ���� ����. �������� ���ȼ����� ����Ǿ� �־ ���� ���� ���ɼ��� ����.
# ------------------------------------------------------------------
class Select(models.Model):
    # ��������
    category = models.ForeignKey(Develop, on_delete=models.CASCADE, verbose_name='���ߺо��ߺз�')
    request = models.TextField('��������', blank=True, null=True)


    class Meta:
        verbose_name = '     ��������'
        verbose_name_plural = '     ��������'

    def __str__(self):
        return str(self.request)
        
# ------------------------------------------------------------------
# Model   : Content
# Description : ������������ �� : ���� ������ ���� �亯�� ������ �� ���������� ���Ŀ� �ý��� ��ȭ �ÿ� ��� ���ɼ� ����
# ------------------------------------------------------------------
class Content(models.Model):
    # ��������
    request = models.ForeignKey(Select, on_delete=models.CASCADE, verbose_name='��������')
    content1 = models.CharField('������1', max_length=256, blank=True, null=True)
    content2 = models.CharField('������2', max_length=256, blank=True, null=True)
    content3 = models.CharField('������3', max_length=256, blank=True, null=True)
    content4 = models.CharField('������4', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '     ��������������'
        verbose_name_plural = '     ��������������'

    def __str__(self):
        return str(self.request)

# ------------------------------------------------------------------
# Model   : Answer
# Description : ���ȼ� �� : ��Ʈ�ʰ� �Ƿڼ��� Ȯ���ϰ� ������ ���ȼ��� �����ϴ� ����. ����� �ʹ� �����ϰ� ����Ǿ� �־� �ܼ�ȭ�� ��ȹ��
# ------------------------------------------------------------------

INFO = [
(0, "���� ��Ȯ��"),
(1, "��Ʈ�ʻ� ���� Ȯ��"),
(2, "��Ʈ�ʻ� ����"),
]

MEETING_STATE = [
    (0, "NOTSUBMIT"), # ���õ��� ����
    (1, "YES"),
    (2, "NO"),
]
class Answer(models.Model):

    content1 = models.TextField('������1', max_length=256, blank=True, null=True)
    content2 = models.TextField('������2', max_length=256, blank=True, null=True)
    content3 = models.TextField('������3', max_length=256, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="������Ʈ", null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="��Ʈ��",)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name="�Ƿڼ� ��", null=True)
    check_time_client = models.DateTimeField('Ŭ���̾�Ʈ Ȯ�� �ð�', default = timezone.now, blank=True, null=True)
    check_time_partner = models.DateTimeField('��Ʈ�� Ȯ�� �ð�', default = timezone.now, blank=True, null=True)
    share_inform = models.BooleanField('���� ���� üũ', default=False)
    createdAt = models.DateTimeField('�ۼ���', default = timezone.now)

    class Meta:
        verbose_name = '     ���ȼ�'
        verbose_name_plural = '     ���ȼ�'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Review
# Description : ���� �� : Ŭ���̾�Ʈ�� ���� �𵨷� ���� ���뿡 ���ؼ� �߰��� ���ɼ��� ����.
# ------------------------------------------------------------------
class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="������Ʈ", null = True)
    isMain = models.BooleanField('���� ������ ���� ����', default = False)
    title = models.CharField('����', max_length=256, blank=True, null=True)
    content = models.TextField('����',null = True)
    createdAt = models.DateTimeField('�ۼ���', default = timezone.now)

    class Meta:
        verbose_name = '����'
        verbose_name_plural = '����'

    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    client = models.ForeignKey(Client, on_delete= models.CASCADE, verbose_name = "�ۼ�Ŭ���̾�Ʈ")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name = "����̴޸�������Ʈ")
    content = models.TextField('��� ����')
    createdAt = models.DateTimeField('�������', default=timezone.now)

    class Meta:
        verbose_name = '     ��û����'
        verbose_name_plural = '     ��û����'

class KakaoToken(models.Model):
    token = models.TextField()
    
