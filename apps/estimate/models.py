#-*- coding: cp949 -*-
import os, datetime, uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from apps.project.models import *

from django.core.validators import MaxValueValidator
from django.db.models import Avg
from hashids import Hashids

#�ð� ���� �Լ�
from django.utils import timezone
from datetime import date


# id �ؽ�ȭ�� ���� �Լ�
def get_default_hash_id():
    hashids = Hashids(salt=settings.SECRET_KEY, min_length=6)
    try:
        user_id = User.objects.latest('id').id + 1
    except:
        user_id = 1
    return hashids.encode(user_id)

# ���� �̸� �ڵ� ������ ���� �Լ�

def stp_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "stp/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = filename
    return os.path.join(path, format)

def stl_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "stl/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = filename
    return os.path.join(path, format)

def time():
    time = timezone.now()
    return time

# ------------------------------------------------------------------
# Model   : Estimate
# Description : �ڵ� ���� �� : �ڵ� �������� ���� �����͸� �����ϴ� �𵨷� ���� attribute ������ �ʿ���
# ------------------------------------------------------------------
class Estimate(models.Model):
    ###  filed
    # client���� 
    #client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='�ۼ�Ŭ���̾�Ʈ')
    
    # ������ ���Ͽ� ���� ����
    request = models.ForeignKey(Request, verbose_name = '�Ƿڼ�', on_delete=models.CASCADE, default = None, null = True)
    stp_file = models.FileField('stp����', upload_to=stp_update_filename)
    stl_file = models.FileField('stl����', upload_to=stl_update_filename)
    volume = models.FloatField('����')
    x_length = models.FloatField('x�� ����')
    y_length = models.FloatField('y�� ����')
    z_length = models.FloatField('z�� ����')
    process = models.CharField('���μ���', max_length=256, null=True, blank=True)
    category = models.CharField('����', max_length=256, null=True, blank=True)
    material = models.CharField('����', max_length=256, null=True, blank=True)
    minPrice = models.FloatField('�����ּҰ���', default=0)
    maxPrice = models.FloatField('�����ִ밡��', default=0)
    totalMinPrice = models.FloatField('���� ���� �ּ� ���� ', default=0)
    totalMaxPrice = models.FloatField('���� ���� �ִ� ����', default=0)
    number = models.IntegerField('����', null=True, blank=True)
    
    created_at = models.DateTimeField('�������', default=time)
    class Meta:
        verbose_name = '     ������ ����'
        verbose_name_plural = '     ������ ����'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : EstimateList
# Description : ���� ����
# ------------------------------------------------------------------
class Estimate_list(models.Model):
    product_img = models.ImageField('���� ���� �̹���', upload_to=request_update_filename, null=True)
    price = models.CharField('��������', max_length=256, null=True)
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, verbose_name='���� ����')

    class Meta:
        verbose_name = '     ������ ���� ����'
        verbose_name_plural = '     ������ ���� ����'

    def __str__ (self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : manufactureProcess
# Description : ���� ��з� �� : �ڵ� ������ ���� ���� ������ ���� ������ �����ϰ� �ִ� ��
# ------------------------------------------------------------------

class manufactureProcess (models.Model):
    name = models.CharField('������', max_length=256, blank=True, null=True)
    
    class Meta:
        verbose_name = '     ���� ��з�'
        verbose_name_plural = '     ���� ��з�'
    
    def __str__(self):
        return str(self.name)

# ------------------------------------------------------------------
# Model   : detailManufactureProcess
# Description : ���� �Һз� �� : �ڵ� ������ ���� ���� ������ �Һз��� ���� �ڵ� ���� ���� ������ �����ϰ� �ִ� ��
# ------------------------------------------------------------------


class detailManufactureProcess (models.Model):
    process = models.ForeignKey(manufactureProcess, verbose_name = '���� ��з�', on_delete=models.CASCADE, null = False)
    name = models.CharField('������', max_length=256, blank=True, null=True)
    minShoot = models.IntegerField('��Ʈ �ּҰ�')
    maxShoot = models.IntegerField('��Ʈ �ִ밪')
    minPostProcessing = models.IntegerField('�İ�������Ʈ��� �ּҰ�')
    maxPostProcessing = models.IntegerField('�İ�������Ʈ��� �ִ밪')
    
    class Meta:
        verbose_name = '     ���� ����'
        verbose_name_plural = '     ���� ����'
    
    def __str__(self):
        return str(self.name)
    
# ------------------------------------------------------------------
# Model   : material
# Description : ���� �� : �ڵ� ������ ���� ���� ���翡 ���� ������ ������ �ִ� ��
# ------------------------------------------------------------------


class material (models.Model):
    detailProcess = models.ForeignKey(detailManufactureProcess, verbose_name = '���ΰ���', on_delete=models.CASCADE)
    name = models.CharField("����", max_length=256)
    price = models.FloatField("����")
    
    class Meta:
        verbose_name = '     ���'
        verbose_name_plural = '     ���'
    
    def __str__(self):
        return str(self.name)

