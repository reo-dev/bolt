#-*- coding: cp949 -*-
import os, datetime, uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

#파일 업로드 함수
def maincategory_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "maincategory/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_maincategory" + "." + ext
    return os.path.join(path, format)

def category_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "category/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_category" + "." + ext
    return os.path.join(path, format)

def subclass_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "subclass/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_subclass" + "." + ext
    return os.path.join(path, format)

def developbig_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "developbig/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_developbig" + "." + ext
    return os.path.join(path, format)

def develop_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "develop/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_develop" + "." + ext
    return os.path.join(path, format)



# ------------------------------------------------------------------
# Model   : Maincategory
# Description : 제품 대분류 모델 : 원래 의뢰하는 제품의 분류에 따라 매칭을 하려고 했으나 현재는 사용하고 있지 않음
# ------------------------------------------------------------------
class Maincategory(models.Model):
    maincategory = models.CharField('제품대분류', max_length=256)
    big_img = models.ImageField('제품대분류이미지', upload_to=maincategory_update_filename)

    class Meta:
        verbose_name = '  제품대분류'
        verbose_name_plural = '  제품대분류'

    def __str__(self):
        return str(self.maincategory)



# ------------------------------------------------------------------
# Model   : Category
# Description : 제품 중분류 모델 : 원래 의뢰하는 제품의 분류에 따라 매칭을 하려고 했으나 현재는 사용하고 있지 않음
# ------------------------------------------------------------------
class Category(models.Model):
    maincategory = models.ForeignKey(Maincategory, on_delete=models.CASCADE, verbose_name='제품대분류')
    category = models.CharField('제품중분류', max_length=256)
    middle_img = models.ImageField('중분류이미지', upload_to=category_update_filename)
    price = models.CharField('가격정보', max_length=256,default = '0')
    period = models.CharField('기간정보', max_length=256,default = '0')
    additionalPrice = models.CharField('추가금액',max_length = 256, default ='0',null = True)    
    
    class Meta:
        verbose_name = '  제품중분류'
        verbose_name_plural = '  제품중분류'

    def __str__(self):
        return str(self.category)



# ------------------------------------------------------------------
# Model   : Subclass
# Description : 제품 소분류 모델 : 원래 의뢰하는 제품의 분류에 따라 매칭을 하려고 했으나 현재는 사용하고 있지 않음
# ------------------------------------------------------------------
class Subclass(models.Model):
    maincategory = models.ForeignKey(Maincategory, on_delete=models.CASCADE, verbose_name='제품대분류')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='제품중분류')
    subclass = models.CharField('제품소분류', max_length=256, blank=True)
    small_img = models.ImageField('제품소분류이미지', upload_to=subclass_update_filename)

    class Meta:
        verbose_name = '  제품소분류'
        verbose_name_plural = '  제품소분류'

    def __str__(self):
        return str(self.subclass)



# ------------------------------------------------------------------
# Model   : City
# Description : 시/도 모델 : 파트너의 시/도의 위치를 저장하기 위한 모델이나 현재 사용하고 있지 않음
# ------------------------------------------------------------------
class City(models.Model):
    city = models.CharField('시/도', max_length=256)

    class Meta:
        verbose_name = '시/도'
        verbose_name_plural = '시/도'

    def __str__(self):
        return str(self.city)

# ------------------------------------------------------------------
# Model   : Developbig
# Description : 개발분야 대분류 : 파트너의 개발분야를 저장하기 위한 모델이나 현재 사용하고 있지 않음
# ------------------------------------------------------------------
class Developbig(models.Model):
    maincategory = models.CharField('개발대분류', max_length=256)
    maincategory_img = models.ImageField('개발대분야 이미지', upload_to=developbig_update_filename, null=True)

    class Meta:
        verbose_name = '개발분야 대분류'
        verbose_name_plural = '개발분야 대분류'

    def __str__(self):
        return str(self.maincategory)



# ------------------------------------------------------------------
# Model   : Develop
# Description : 개발분야 중분류 : 파트너의 개발분야를 저장하기 위한 모델이나 현재 사용하고 있지 않음
# ------------------------------------------------------------------
class Develop(models.Model):
    maincategory = models.ForeignKey(Developbig, on_delete=models.CASCADE, verbose_name='개발대분류')
    category = models.CharField('개발중분류', max_length=256)
  #  category_img = models.ImageField('개발분야 이미지', upload_to=develop_update_filename, null=True)
    coin =models.IntegerField('카테고리당 가격', default=0, null=True)

    class Meta:
        verbose_name = '개발분야 중분류'
        verbose_name_plural = '개발분야 중분류'

    def __str__(self):
        return str(self.category)