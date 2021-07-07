#-*- coding: cp949 -*-
from django.db import models
from apps.account.models import *
from apps.project.models import *

def time():
    time = timezone.now()
    return time

def chat_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "chat/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = filename
    return os.path.join(path, format)


class clickLog (models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Ŭ���̾�Ʈ')
    search = models.CharField("�˻���", max_length=256, null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='��Ʈ��')
    created_at = models.DateTimeField('�������', default=time)

    class Meta:
        verbose_name = '��ȭ��ȣ �α�'
        verbose_name_plural = '��ȭ��ȣ �α�'

    def __str__(self):
        return str(self.search)


class Chat(models.Model):
    USERTYPE = [
        (0, "Ŭ���̾�Ʈ"),
        (1, "��Ʈ��"),
    ]

    CHATTYPE = [
        (0, "�ؽ�Ʈ"),
        (1, "�̹���"),
        (2, "����"),
    ]

    text_content = models.TextField('ä�� ����', null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='���ȼ�', null=True)
    user_type = models.IntegerField('�۾��� Ÿ��', default=0, blank=True, choices=USERTYPE, null=True)
    createdAt = models.DateTimeField('�ۼ�����', default=timezone.now)
    chat_type = models.IntegerField('ä�� Ÿ��',choices=CHATTYPE, null=True)
    file = models.FileField('ä������', upload_to=chat_update_filename, blank=True, null=True, max_length=255)

    class Meta:
        verbose_name = 'ä�� �α�'
        verbose_name_plural = 'ä�� �α�'

    def __str__(self):
        return str(self.id)


# ------------------------------------------------------------------
# Model   : LoginLog
# Description : �α��� �α� ���� ��
# ------------------------------------------------------------------
class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'User', null=True)
    created_at = models.DateTimeField('�α�������', auto_now_add=True)
    type = models.IntegerField('����Ÿ��', default=0, choices=USER_TYPE)

    class Meta:
        verbose_name = '�α��� �α�'
        verbose_name_plural = '�α��� �α�'
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.user)

# ------------------------------------------------------------------
# Model   : Search_text
# Description : ������ ã�⿡�� �˻��� Ű����
# ------------------------------------------------------------------
class SearchText(models.Model):
    ip = models.GenericIPAddressField(default = "0.0.0.0")
    text = models.CharField('�˻���', max_length=256, null=True)
    created_at = models.DateTimeField('�˻�����', auto_now_add=True)


    class Meta:
        verbose_name = '�˻��� �α�'
        verbose_name_plural = '�˻��� �α�'

    def __str__(self):
        return str(self.text)