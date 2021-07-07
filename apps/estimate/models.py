#-*- coding: cp949 -*-
import os, datetime, uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from apps.project.models import *

from django.core.validators import MaxValueValidator
from django.db.models import Avg
from hashids import Hashids

#시간 관련 함수
from django.utils import timezone
from datetime import date


# id 해쉬화를 위한 함수
def get_default_hash_id():
    hashids = Hashids(salt=settings.SECRET_KEY, min_length=6)
    try:
        user_id = User.objects.latest('id').id + 1
    except:
        user_id = 1
    return hashids.encode(user_id)

# 파일 이름 자동 저장을 위한 함수

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
# Description : 자동 견적 모델 : 자동 견적에서 나온 데이터를 저장하는 모델로 추후 attribute 수정이 필요함
# ------------------------------------------------------------------
class Estimate(models.Model):
    ###  filed
    # client정보 
    #client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='작성클라이언트')
    
    # 가견적 파일에 대한 정보
    request = models.ForeignKey(Request, verbose_name = '의뢰서', on_delete=models.CASCADE, default = None, null = True)
    stp_file = models.FileField('stp파일', upload_to=stp_update_filename)
    stl_file = models.FileField('stl파일', upload_to=stl_update_filename)
    volume = models.FloatField('부피')
    x_length = models.FloatField('x축 길이')
    y_length = models.FloatField('y축 길이')
    z_length = models.FloatField('z축 길이')
    process = models.CharField('프로세스', max_length=256, null=True, blank=True)
    category = models.CharField('종류', max_length=256, null=True, blank=True)
    material = models.CharField('재질', max_length=256, null=True, blank=True)
    minPrice = models.FloatField('사출최소가격', default=0)
    maxPrice = models.FloatField('서출최대가격', default=0)
    totalMinPrice = models.FloatField('금형 사출 최소 가격 ', default=0)
    totalMaxPrice = models.FloatField('금형 사출 최대 가격', default=0)
    number = models.IntegerField('수량', null=True, blank=True)
    
    created_at = models.DateTimeField('등록일자', default=time)
    class Meta:
        verbose_name = '     가견적 내역'
        verbose_name_plural = '     가견적 내역'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : EstimateList
# Description : 도면 정보
# ------------------------------------------------------------------
class Estimate_list(models.Model):
    product_img = models.ImageField('도면 형상 이미지', upload_to=request_update_filename, null=True)
    price = models.CharField('가격정보', max_length=256, null=True)
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, verbose_name='도면 정보')

    class Meta:
        verbose_name = '     선택한 도면 정보'
        verbose_name_plural = '     선택한 도면 정보'

    def __str__ (self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : manufactureProcess
# Description : 공정 대분류 모델 : 자동 견적을 내기 위해 공정에 따른 정보를 저장하고 있는 모델
# ------------------------------------------------------------------

class manufactureProcess (models.Model):
    name = models.CharField('공정명', max_length=256, blank=True, null=True)
    
    class Meta:
        verbose_name = '     공정 대분류'
        verbose_name_plural = '     공정 대분류'
    
    def __str__(self):
        return str(self.name)

# ------------------------------------------------------------------
# Model   : detailManufactureProcess
# Description : 공정 소분류 모델 : 자동 견적을 내기 위해 공정에 소분류에 따라 자동 견적 관련 정보를 저장하고 있는 모델
# ------------------------------------------------------------------


class detailManufactureProcess (models.Model):
    process = models.ForeignKey(manufactureProcess, verbose_name = '공정 대분류', on_delete=models.CASCADE, null = False)
    name = models.CharField('공정명', max_length=256, blank=True, null=True)
    minShoot = models.IntegerField('쇼트 최소값')
    maxShoot = models.IntegerField('쇼트 최대값')
    minPostProcessing = models.IntegerField('후가공게이트사상 최소값')
    maxPostProcessing = models.IntegerField('후가공게이트사상 최대값')
    
    class Meta:
        verbose_name = '     세부 공정'
        verbose_name_plural = '     세부 공정'
    
    def __str__(self):
        return str(self.name)
    
# ------------------------------------------------------------------
# Model   : material
# Description : 소재 모델 : 자동 견적을 내기 위한 소재에 대한 정보를 가지고 있는 모델
# ------------------------------------------------------------------


class material (models.Model):
    detailProcess = models.ForeignKey(detailManufactureProcess, verbose_name = '세부공정', on_delete=models.CASCADE)
    name = models.CharField("재료명", max_length=256)
    price = models.FloatField("가격")
    
    class Meta:
        verbose_name = '     재료'
        verbose_name_plural = '     재료'
    
    def __str__(self):
        return str(self.name)

