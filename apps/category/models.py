#-*- coding: cp949 -*-
import os, datetime, uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

#���� ���ε� �Լ�
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
# Description : ��ǰ ��з� �� : ���� �Ƿ��ϴ� ��ǰ�� �з��� ���� ��Ī�� �Ϸ��� ������ ����� ����ϰ� ���� ����
# ------------------------------------------------------------------
class Maincategory(models.Model):
    maincategory = models.CharField('��ǰ��з�', max_length=256)
    big_img = models.ImageField('��ǰ��з��̹���', upload_to=maincategory_update_filename)

    class Meta:
        verbose_name = '  ��ǰ��з�'
        verbose_name_plural = '  ��ǰ��з�'

    def __str__(self):
        return str(self.maincategory)



# ------------------------------------------------------------------
# Model   : Category
# Description : ��ǰ �ߺз� �� : ���� �Ƿ��ϴ� ��ǰ�� �з��� ���� ��Ī�� �Ϸ��� ������ ����� ����ϰ� ���� ����
# ------------------------------------------------------------------
class Category(models.Model):
    maincategory = models.ForeignKey(Maincategory, on_delete=models.CASCADE, verbose_name='��ǰ��з�')
    category = models.CharField('��ǰ�ߺз�', max_length=256)
    middle_img = models.ImageField('�ߺз��̹���', upload_to=category_update_filename)
    price = models.CharField('��������', max_length=256,default = '0')
    period = models.CharField('�Ⱓ����', max_length=256,default = '0')
    additionalPrice = models.CharField('�߰��ݾ�',max_length = 256, default ='0',null = True)    
    
    class Meta:
        verbose_name = '  ��ǰ�ߺз�'
        verbose_name_plural = '  ��ǰ�ߺз�'

    def __str__(self):
        return str(self.category)



# ------------------------------------------------------------------
# Model   : Subclass
# Description : ��ǰ �Һз� �� : ���� �Ƿ��ϴ� ��ǰ�� �з��� ���� ��Ī�� �Ϸ��� ������ ����� ����ϰ� ���� ����
# ------------------------------------------------------------------
class Subclass(models.Model):
    maincategory = models.ForeignKey(Maincategory, on_delete=models.CASCADE, verbose_name='��ǰ��з�')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='��ǰ�ߺз�')
    subclass = models.CharField('��ǰ�Һз�', max_length=256, blank=True)
    small_img = models.ImageField('��ǰ�Һз��̹���', upload_to=subclass_update_filename)

    class Meta:
        verbose_name = '  ��ǰ�Һз�'
        verbose_name_plural = '  ��ǰ�Һз�'

    def __str__(self):
        return str(self.subclass)



# ------------------------------------------------------------------
# Model   : City
# Description : ��/�� �� : ��Ʈ���� ��/���� ��ġ�� �����ϱ� ���� ���̳� ���� ����ϰ� ���� ����
# ------------------------------------------------------------------
class City(models.Model):
    city = models.CharField('��/��', max_length=256)

    class Meta:
        verbose_name = '��/��'
        verbose_name_plural = '��/��'

    def __str__(self):
        return str(self.city)

# ------------------------------------------------------------------
# Model   : Developbig
# Description : ���ߺо� ��з� : ��Ʈ���� ���ߺо߸� �����ϱ� ���� ���̳� ���� ����ϰ� ���� ����
# ------------------------------------------------------------------
class Developbig(models.Model):
    maincategory = models.CharField('���ߴ�з�', max_length=256)
    maincategory_img = models.ImageField('���ߴ�о� �̹���', upload_to=developbig_update_filename, null=True)

    class Meta:
        verbose_name = '���ߺо� ��з�'
        verbose_name_plural = '���ߺо� ��з�'

    def __str__(self):
        return str(self.maincategory)



# ------------------------------------------------------------------
# Model   : Develop
# Description : ���ߺо� �ߺз� : ��Ʈ���� ���ߺо߸� �����ϱ� ���� ���̳� ���� ����ϰ� ���� ����
# ------------------------------------------------------------------
class Develop(models.Model):
    maincategory = models.ForeignKey(Developbig, on_delete=models.CASCADE, verbose_name='���ߴ�з�')
    category = models.CharField('�����ߺз�', max_length=256)
  #  category_img = models.ImageField('���ߺо� �̹���', upload_to=develop_update_filename, null=True)
    coin =models.IntegerField('ī�װ��� ����', default=0, null=True)

    class Meta:
        verbose_name = '���ߺо� �ߺз�'
        verbose_name_plural = '���ߺо� �ߺз�'

    def __str__(self):
        return str(self.category)