#-- coding: cp949 --
import os, datetime, uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from apps.category.models import *
from django.core.validators import MaxValueValidator
from django.db.models import Avg
from hashids import Hashids

# Create your models here.
def get_default_hash_id():
    hashids = Hashids(salt=settings.SECRET_KEY, min_length=6)
    try:
        user_id = User.objects.latest('id').id + 1
    except:
        user_id = 1
    return hashids.encode(user_id)

# filename �ڵ� ����
def partner_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "partner/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_partner" + "." + ext
    return os.path.join(path, format)


def portfolio_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "portfolio/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_portfolio" + "." + ext
    return os.path.join(path, format)

def machine_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "machine/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_machine" + "." + ext
    return os.path.join(path, format)

def certification_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "certification/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_certification" + "." + ext
    return os.path.join(path, format)

def process_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "process/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_process" + "." + ext
    return os.path.join(path, format)

def structure_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "structure/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = uuid.uuid4().hex + "_structure" + "." + ext
    return os.path.join(path, format)
    
# ------------------------------------------------------------------
# Model   : User
# Description : ȸ�� ��
# ------------------------------------------------------------------
USER_TYPE = [
    (0, "CLIENT"),
    (1, "PARTNER")
]
class User(AbstractUser):

    # ���� �κ�
    username = models.CharField('�̸���', max_length=256, default=get_default_hash_id, unique=True)
    type = models.IntegerField('����Ÿ��', default=0, choices=USER_TYPE)
    password = models.CharField(max_length=256)
    phone = models.CharField('�޴��� ��ȣ', max_length=100, blank=True)
    marketing = models.BooleanField('�����õ��ǿ���', default=True, null=True)
    last_activity = models.DateTimeField('�ֱ� Ȱ��', default = None, blank = True, null = True)

    class Meta:
        verbose_name = '������'
        verbose_name_plural = '������'
        
    @property
    def is_update(self):
        if self.username and self.type and self.password:
            return True
        else:
            return False

# ------------------------------------------------------------------
# Model   : Client
# Description : Ŭ���̾�Ʈ ��
# ------------------------------------------------------------------

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='����')
    name = models.CharField('��ü��', max_length=256, null=True)
    title = models.CharField('����', max_length=256, null=True)
    realName = models.CharField('�̸�', max_length=256, null=True)
    department = models.CharField('�μ�', max_length=256, null=True)
    path = models.CharField('�湮���', max_length=256, null=True)
    business = models.CharField('����', max_length=256, null=True)
    email = models.CharField('�̸���', max_length=256, null=True)
    
    class Meta:
        verbose_name = 'Ŭ���̾�Ʈ'
        verbose_name_plural = 'Ŭ���̾�Ʈ'

    def __str__(self):
        return str(self.user.username)

# ------------------------------------------------------------------
# Model   : Partner
# Description : ��Ʈ�� ��
# ------------------------------------------------------------------

class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='����')
    name = models.CharField('��ü��', max_length=256, null=True)
    logo = models.ImageField('�ΰ�', upload_to=partner_update_filename, blank=True, null=True)
    #����
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="��/��", null=True)
    info_company = models.TextField('ȸ��Ұ�', blank=True, null=True)
    history = models.TextField('������ ��ǰ��', blank=True, null=True)
    deal = models.TextField('�ֿ�ŷ�ó', blank=True, null=True)
    category_middle = models.ManyToManyField(Develop, verbose_name='�Ƿڰ��ɺо�', related_name='category_middle')
    #ȸ������ �� ����
    file = models.FileField('ȸ��Ұ� �� ��������������', upload_to=partner_update_filename, blank=True, null=True)
    resume = models.FileField('�̷¼�', upload_to=partner_update_filename, blank=True, null=True)
    avg_score = models.DecimalField('�������', default=0, max_digits=5, decimal_places=2, null=True)
    # �Ƚɹ�ȣ�� �ƴ� ���� ��ȭ��ȣ
    real_phone = models.CharField('���� �޴��� ��ȣ', max_length=255, blank=True, null=True)


    class Meta:
        verbose_name = '��Ʈ��'
        verbose_name_plural = '��Ʈ��'

    def __str__(self):
        return str(self.user.username)

# ------------------------------------------------------------------
# Model   : Portfolio
# Description : ��Ʈ������ ��
# ------------------------------------------------------------------
class Portfolio(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="��Ʈ��", null=True)
    img_portfolio = models.ImageField('���������� �̹���', upload_to=portfolio_update_filename, null=True)
    is_main = models.BooleanField('���� ����', default=False)

    class Meta:
        verbose_name = '     ��Ʈ������'
        verbose_name_plural = '     ��Ʈ������'

    def __str__(self):
        return str(self.partner.name) + " ��Ʈ������"
        

# ------------------------------------------------------------------
# Model   : Path
# Description : �湮��� ���� ��
# ------------------------------------------------------------------
class Path(models.Model):
    path = models.CharField('�湮���', max_length=256, null=True)


    class Meta:
        verbose_name = '�湮���'
        verbose_name_plural = '�湮���'

    def __str__(self):
        return str(self.path)

# ------------------------------------------------------------------
# Model   : Busincess
# Description : ���� �α� ���� ��
# ------------------------------------------------------------------
class Business(models.Model):
    business = models.CharField('����', max_length=256, null=True)


    class Meta:
        verbose_name = '����'
        verbose_name_plural = '����'

    def __str__(self):
        return str(self.business)


# ------------------------------------------------------------------
# Model   : Partner Review
# Description : ��Ʈ�� ���� ���̺�
# ------------------------------------------------------------------
REVIEW_TYPE = [
    (1, "�ſ� �Ҹ���"),
    (2, "�Ҹ���"),
    (3, "����"),
    (4, "����"),
    (5, "�ſ� ����"),
]
class PartnerReview(models.Model):

    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="��Ʈ��", null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Ŭ���̾�Ʈ", null=True)
    score = models.IntegerField('����', default=0, choices=REVIEW_TYPE)
    content = models.CharField('������', max_length=256, null=True)

    class Meta:
        verbose_name = '��Ʈ�� ����'
        verbose_name_plural = '��Ʈ�� ����'

    def __str__(self):
        return str(self.score)

# ------------------------------------------------------------------
# Model   : Partner Review_temp
# Description : ��Ʈ�� �ӽ� ���� ���̺� : ���� �ޱ⸦ ���� �ӽ� ����
# ------------------------------------------------------------------
REVIEW_TYPE = [
    (1, "�ſ� �Ҹ���"),
    (2, "�Ҹ���"),
    (3, "����"),
    (4, "����"),
    (5, "�ſ� ����"),
]
class PartnerReviewTemp(models.Model):

    partnername = models.CharField('��ü��', max_length=256, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Ŭ���̾�Ʈ", null=True)
    score = models.IntegerField('����', default=0, choices=REVIEW_TYPE)
    content = models.CharField('������', max_length=256, null=True)

    class Meta:
        verbose_name = '��Ʈ�� �ӽ� ����'
        verbose_name_plural = '��Ʈ�� �ӽ� ����'

    def __str__(self):
        return str(self.score)

class CsvFileUpload(models.Model):
    filename = models.CharField("�����̸�", max_length=256, null=True)
    partner_info_file = models.FileField('��Ʈ������ ����',upload_to=partner_update_filename,max_length=255, blank=True, null=True)
    portfolio_file = models.FileField('��Ʈ������ ����',upload_to=partner_update_filename,max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = '�����̸�'
        verbose_name_plural = '�����̸�'

    def __str__(self):
        return str(self.filename)
