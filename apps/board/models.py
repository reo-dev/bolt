#-*- coding: cp949 -*-
import os, datetime, uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

# �Խ���
from ckeditor_uploader.fields import RichTextUploadingField

def magazine_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "magazine/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_magazine" + "." + ext
    return os.path.join(path, format)

# ------------------------------------------------------------------
# Model   : Magazine_Category
# Description : �Ű��� ī�װ� �� : �Ű��� ī�װ��� �����ϴ� �� 
# ------------------------------------------------------------------
class Magazine_Category(models.Model):

    category = models.CharField('�Ű��� �з�', max_length=40, default="�⺻")
    class Meta:
        verbose_name = '   �Ű��� ī�װ�'
        verbose_name_plural = '   �Ű��� ī�װ�'

    def __str__(self):
        return str(self.category)


# ------------------------------------------------------------------
# Model   : Magazine
# Description : �Ű��� �� : �������� �����ϴ� �Խ��ǿ� �����. 
# ------------------------------------------------------------------
class Magazine(models.Model):

    title = models.CharField('����', max_length=40)
    content = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField('�Ű��� �̹���', upload_to=magazine_update_filename, null=True)
    is_top = models.BooleanField('��ܰ�������', default=False)
    created_at = models.DateTimeField('�������', auto_now_add=True)
    summary = models.TextField('���', null=True)
    category = models.ForeignKey(Magazine_Category, on_delete=models.CASCADE, verbose_name='�Ű��� ī�װ�', null=True)
    class Meta:
        verbose_name = '   �Ű���'
        verbose_name_plural = '   �Ű���'

    def __str__(self):
        return str(self.title) + " : �Ű���"