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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='클라이언트')
    search = models.CharField("검색어", max_length=256, null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='파트너')
    created_at = models.DateTimeField('등록일자', default=time)

    class Meta:
        verbose_name = '전화번호 로그'
        verbose_name_plural = '전화번호 로그'

    def __str__(self):
        return str(self.search)


class Chat(models.Model):
    USERTYPE = [
        (0, "클라이언트"),
        (1, "파트너"),
    ]

    CHATTYPE = [
        (0, "텍스트"),
        (1, "이미지"),
        (2, "파일"),
    ]

    text_content = models.TextField('채팅 내용', null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='제안서', null=True)
    user_type = models.IntegerField('글쓴이 타입', default=0, blank=True, choices=USERTYPE, null=True)
    createdAt = models.DateTimeField('작성일자', default=timezone.now)
    chat_type = models.IntegerField('채팅 타입',choices=CHATTYPE, null=True)
    file = models.FileField('채팅파일', upload_to=chat_update_filename, blank=True, null=True, max_length=255)

    class Meta:
        verbose_name = '채팅 로그'
        verbose_name_plural = '채팅 로그'

    def __str__(self):
        return str(self.id)


# ------------------------------------------------------------------
# Model   : LoginLog
# Description : 로그인 로그 저장 모델
# ------------------------------------------------------------------
class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'User', null=True)
    created_at = models.DateTimeField('로그인일자', auto_now_add=True)
    type = models.IntegerField('유저타입', default=0, choices=USER_TYPE)

    class Meta:
        verbose_name = '로그인 로그'
        verbose_name_plural = '로그인 로그'
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.user)

# ------------------------------------------------------------------
# Model   : Search_text
# Description : 제조사 찾기에서 검색된 키워드
# ------------------------------------------------------------------
class SearchText(models.Model):
    ip = models.GenericIPAddressField(default = "0.0.0.0")
    text = models.CharField('검색어', max_length=256, null=True)
    created_at = models.DateTimeField('검색일자', auto_now_add=True)


    class Meta:
        verbose_name = '검색어 로그'
        verbose_name_plural = '검색어 로그'

    def __str__(self):
        return str(self.text)