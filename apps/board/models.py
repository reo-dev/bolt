#-*- coding: cp949 -*-
import os, datetime, uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

# 게시판
from ckeditor_uploader.fields import RichTextUploadingField

def magazine_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "magazine/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_magazine" + "." + ext
    return os.path.join(path, format)

# ------------------------------------------------------------------
# Model   : Magazine_Category
# Description : 매거진 카테고리 모델 : 매거진 카테고리를 저장하는 모델 
# ------------------------------------------------------------------
class Magazine_Category(models.Model):

    category = models.CharField('매거진 분류', max_length=40, default="기본")
    class Meta:
        verbose_name = '   매거진 카테고리'
        verbose_name_plural = '   매거진 카테고리'

    def __str__(self):
        return str(self.category)


# ------------------------------------------------------------------
# Model   : Magazine
# Description : 매거진 모델 : 콘텐츠를 제공하는 게시판에 사용함. 
# ------------------------------------------------------------------
class Magazine(models.Model):

    title = models.CharField('제목', max_length=40)
    content = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField('매거진 이미지', upload_to=magazine_update_filename, null=True)
    is_top = models.BooleanField('상단고정여부', default=False)
    created_at = models.DateTimeField('등록일자', auto_now_add=True)
    summary = models.TextField('요약', null=True)
    category = models.ForeignKey(Magazine_Category, on_delete=models.CASCADE, verbose_name='매거진 카테고리', null=True)
    class Meta:
        verbose_name = '   매거진'
        verbose_name_plural = '   매거진'

    def __str__(self):
        return str(self.title) + " : 매거진"