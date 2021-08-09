#-*- coding: cp949 -*-
import os, datetime, uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django_filters.utils import verbose_field_name
from apps.category.models import *
from apps.account.models import *
from typing import TYPE_CHECKING
from ckeditor_uploader.fields import RichTextUploadingField
from hashids import Hashids
from django.core.validators import MaxValueValidator
#시간 관련 함수
from django.utils import timezone
from datetime import date

import boto3

def project_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "project/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = filename
    return os.path.join(path, format)

def request_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "request/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
    format = filename
    return os.path.join(path, format)

def requestInfo_update_filename(instance, filename):
    ext = filename.split('.')[-1]
    now = datetime.datetime.now()
    path = "requestinfo/" + str(now.year) + "/" + str(now.month) + "/" + str(now.day)
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
# Description : 프로젝트 상태 모델 : 프로젝트의 현재 상태(계약 중 등)을 체크하기 위한 모델로 admin 관리를 위해 사용됨 
# ------------------------------------------------------------------

class ProjectStatus(models.Model):
    name = models.CharField('상황',max_length =256)

    class Meta:
        verbose_name = '     프로젝트진행상황'
        verbose_name_plural = '     프로젝트진행상황'

    def __str__(self):
        return str(self.name)
        
# ------------------------------------------------------------------
# Model   : Manager
# Description : 프로젝트 담당자 모델 : 프로젝트의 담당자를 체크하기 위한 모델로 admin 관리를 위해 사용됨 
# ------------------------------------------------------------------

class Manager(models.Model):
    name = models.CharField('매니저',max_length=150,null=True,blank=True)

    class Meta:
        verbose_name = '     프로젝트담당자'
        verbose_name_plural = '     프로젝트담당자'

    def __str__(self):
        return str(self.name)
        
# ------------------------------------------------------------------
# Model   : Project
# Description : 프로젝트 모델 : 프로젝트에 관련된 정보들을 담고 있고 하위 모델로 request(의뢰서)와 answer(제안서)를 사용하고 있음
# ------------------------------------------------------------------
class Project(models.Model):

    PROGRESS = [
    ('모집중', "모집중"),
    ('모집종료' ,"모집종료"),
    ]

    TRANSFER = [
    ('아니오', '아니오'),
    ('선금', '선금'),
    ('중도금', '중도금'),
    ('완납', '완납'),
    ]

    STEP = [
        ('정보입력', '고객의뢰'),

        ('1', '유선상담1'),
        ('10', '유선상담2'),

        ('업체 수배', '업체수배'),

        ('2', '업체견적문의'),
        ('3', '업체요구정보추가'),


        ('4', '견적검토중'),
        
        ('5', '타업체견적요청'),

        ('6', '미팅'),
        ('7', '직접연결(매칭)'),


        ('거래완료', '계약체결'),

        ('거래 보류', '거래 보류'),

        ('DROP-기획부족', 'DROP-기획부족'),
        ('DROP-예산부족', 'DROP-예산부족'),
        ('DROP-MOQ부족', 'DROP-MOQ부족'),
        ('DROP-납기촉박', 'DROP-납기촉박'),
        ('DROP', 'DROP'),
    ]

    createdAt = models.DateTimeField('등록일자', default=timezone.now)
    status = models.CharField('프로젝트 상태', max_length=10, default="모집중", blank=True, choices=PROGRESS, null=True)
    title = models.CharField('프로젝트 제목', max_length = 150, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='작성클라이언트',null=True) # 작성한 클라이언트 FK

    memo = models.TextField('상담 내용', blank=True, null=True)
    manager = models.ForeignKey(Manager, on_delete = models.CASCADE, verbose_name='담당자',related_name='project', null=True,blank=True)
    #project_status = models.ForeignKey(ProjectStatus, on_delete = models.CASCADE, verbose_name='상황',related_name='project', null=True)
    progressStep = models.CharField('고객 진행 단계', max_length=10, default='', choices=STEP)
    explain = models.TextField('중요 사항', blank=True, null=True)
    reason = models.CharField('담당자 코멘트', max_length=256, blank=True, null=True)

    text = RichTextUploadingField(blank=True, null=True)

    estimate = models.IntegerField('계약 금액', blank=True, null=True, default=0) 
    hope_estimate = models.IntegerField('예상 금액', blank=True, null=True, default=0)
    partner_estimate = models.IntegerField('파트너 견적 금액', blank=True, null=True, default=0)
    transferMoney = models.CharField('입금 여부', max_length=10, default='아니오', choices=TRANSFER)

    client_email = models.CharField('클라이언트 이메일', max_length=256, blank=True, null=True)
    client_phone = models.CharField('클라이언트 핸드폰', max_length=256, null=True)

    class Meta:
        verbose_name = '     프로젝트'
        verbose_name_plural = '     프로젝트'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : ProjectFile
# Description : 프로젝트 파일 모델 : 매니저가 첨부한 모델
# ------------------------------------------------------------------
class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE, verbose_name= '의뢰서')
    name = models.CharField('파일 메모', max_length=256, null=True, blank=True)
    file = models.FileField('매니저 파일', upload_to=project_update_filename, blank=False, null=False, max_length=255)
    share_inform = models.BooleanField('민감정보 포함 여부', default=False)

    class Meta:
        verbose_name = '매니저 첨부파일'
        verbose_name_plural = '매니저 첨부파일'
    def __str__ (self):
        return str(self.project) + ' 매니저 첨부'


    def delete(self, *args, **kwargs):
        s3_client = boto3.client('s3',aws_access_key_id='AKIATYAEQEY5RQM64SEC',aws_secret_access_key='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')
        s3_client.delete_object(Bucket='boltnnutplatform', Key='media/'+self.file.name)
        super(ProjectFile, self).delete(*args, **kwargs)



# ------------------------------------------------------------------
# Model   : Request
# Description : 의뢰서 모델 
# ------------------------------------------------------------------
class Request(models.Model):

    request_states = [
        (0, '상담요청'),
        (1, '견적문의'),
        (2, '업체수배'),
    ]

    deadline_states = [
        (0, '납기일미정'),
        (1, '납기일협의가능'),
    ]

    prices = [
        ( 1, "100만원 이하" ),
        ( 2, "100만원 - 300만원" ),
        ( 3, "300만원 - 500만원" ),
        ( 4, "500만원 - 1000만원"),
        ( 5, "1000만원 - 2000만원"),
        ( 6, "2000만원 - 3000만원"),
        ( 7, "3000만원 - 5000만원"),
        ( 8, "5000만원 - 1억원"),
        ( 9, "1억원이상"),
    ]

    regionAry= [
      (1, "서울" ),
      (2, "경기도" ),
      (3, "인천" ),
      (4, "충청도" ),
      (5, "경상북도" ),
      (6, "경상남도" ),
      (7, "전라도" ),
      (8, "제주도" ),

    ]

    region_states = [
        (0, '미정'),
        (1, '협의가능'),

    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='작성클라이언트')
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='제조사 찾기로 들어온 파트너',blank=True,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='프로젝트')
    request_state = models.CharField('문의 목적', max_length=10, default='', choices=request_states)
    name = models.CharField('상담명', max_length=256, blank=True, null=True)
    deadline = models.DateTimeField('납기일', default=timezone.now)
    deadline_state = models.CharField('납기일 상태', max_length=10, default='', choices=deadline_states)
    contents = models.CharField('공개 발주 요청사항', max_length=5000, blank=True, null=True)
    order_request_close = models.CharField('비공개 발주 요청사항', max_length=5000, blank=True, null=True)
    price = models.CharField('희망비용', blank=True, max_length=256,null=True, default='1', choices=prices) 
    createdAt = models.DateTimeField('등록일자', default=timezone.now)
    category = models.ForeignKey(Mainbusiness, on_delete=models.CASCADE, verbose_name="카테고리", blank=True, null=True)
    region = models.CharField('시/도', max_length=10, default=0,choices=regionAry, blank=True, null=True)
    region_state = models.CharField('시/도 협의', max_length=10, default=0, choices=region_states, blank=True, null=True)

    class Meta:
        verbose_name = '     요청된 의뢰'
        verbose_name_plural = '     요청된 의뢰'

    def __str__(self):
        return str(self.name)

# ------------------------------------------------------------------
# Model   : RequestFile
# Description : 의뢰서 파일 모델 : 의뢰서에 첨부한 파일 모델인데 중복이 되어서 정돈이 필요함
# ------------------------------------------------------------------
class RequestFile(models.Model):
    request = models.ForeignKey(Request, on_delete = models.CASCADE, verbose_name= '의뢰서')
    file = models.FileField('의뢰파일', upload_to=request_update_filename, blank=False, null=False, max_length=255)
    share_inform = models.BooleanField('정보 공개 체크', default=False)

    class Meta:
        verbose_name = '     제품 기본정보 첨부파일'
        verbose_name_plural = '     제품 기본정보 첨부파일'
    def __str__ (self):
        return str(self.request) + ' 의뢰서'


# ------------------------------------------------------------------
# Model   : RequestInfo
# Description : 상세 의뢰서 모델 
# ------------------------------------------------------------------
class RequestInfo(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='작성클라이언트')
    category_big = models.CharField('대분류', max_length=256, blank=True, null=True)
    category_small = models.CharField('소분류', max_length=256, blank=True, null=True)
    city = models.CharField('지역', max_length=256, blank=True, null=True)
    price = models.CharField('희망비용',max_length=256, blank=True, null=True) 
    category_middle = models.ManyToManyField(Develop, verbose_name='의뢰가능분야', related_name='category_request')
    title = models.CharField('제목', max_length=256, blank=True, null=True)
    content = models.TextField('피드백', blank=True, null=True)
    email = models.CharField('이메일', max_length=256, blank=True, null=True)
    phone = models.CharField('핸드폰', max_length=256, blank=True, null=True)
    classified = models.IntegerField('공개 희망', blank=True, null=True) 

    class Meta:
        verbose_name = '업체 수배 요청'
        verbose_name_plural = '업체 수배 요청'

    def __str__(self):
        return str(self.title) 


# ------------------------------------------------------------------
# Model   : RequestInfoFile
# Description : 의뢰서 파일 모델 : 의뢰서에 첨부한 파일 모델인데 중복이 되어서 정돈이 필요함
# ------------------------------------------------------------------
class RequestInfoFile(models.Model):
    requestInfo = models.ForeignKey(RequestInfo, on_delete = models.CASCADE)
    file = models.FileField('의뢰파일', upload_to=requestInfo_update_filename, blank=False, null=False, max_length=255)
    share_inform = models.BooleanField('정보 공개 체크', default=False)

    class Meta:
        verbose_name = '상세 의뢰 첨부파일'
        verbose_name_plural = '상세 의뢰 첨부파일'
    def __str__ (self):
        return str(self.requestInfo)


# ------------------------------------------------------------------
# Model   : Select_save
# Description : 의로서에 저장되는 선택질문/답변 모델 : 객관식 질문에 대한 답변을 위한 내용인데 이 내용은 서비스 고도화가 되기 전에는 사용하지 않을 예정이나 추후 가능성 보임
# ------------------------------------------------------------------
class Select_save(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name='의뢰서')
    category = models.ForeignKey(Develop, on_delete=models.CASCADE, verbose_name='개발분야')
    question = models.CharField('선택질문', max_length=256, blank=True, null=True)
    answer = models.CharField('선택질문답변', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '     의뢰서에 저장되는 선택질문/답변'
        verbose_name_plural = '     의뢰서에 저장되는 선택질문/답변'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Select
# Description : 선택질문 모델 : 왜 위에꺼랑 두 개를 만들었는 지 이해되지는 않음... 삭제 예정. 위에꺼가 제안서랑도 연결되어 있어서 추후 사용될 가능성이 보임.
# ------------------------------------------------------------------
class Select(models.Model):
    # 선택질문
    category = models.ForeignKey(Develop, on_delete=models.CASCADE, verbose_name='개발분야중분류')
    request = models.TextField('선택질문', blank=True, null=True)


    class Meta:
        verbose_name = '     선택질문'
        verbose_name_plural = '     선택질문'

    def __str__(self):
        return str(self.request)
        
# ------------------------------------------------------------------
# Model   : Content
# Description : 선택질문내용 모델 : 선택 질문에 대한 답변을 저장한 모델 마찬가지로 추후에 시스템 고도화 시에 사용 가능성 있음
# ------------------------------------------------------------------
class Content(models.Model):
    # 선택질문
    request = models.ForeignKey(Select, on_delete=models.CASCADE, verbose_name='선택질문')
    content1 = models.CharField('컨텐츠1', max_length=256, blank=True, null=True)
    content2 = models.CharField('컨텐츠2', max_length=256, blank=True, null=True)
    content3 = models.CharField('컨텐츠3', max_length=256, blank=True, null=True)
    content4 = models.CharField('컨텐츠4', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = '     선택질문컨텐츠'
        verbose_name_plural = '     선택질문컨텐츠'

    def __str__(self):
        return str(self.request)

# ------------------------------------------------------------------
# Model   : Answer
# Description : 제안서 모델 : 파트너가 의뢰서를 확인하고 제안한 제안서를 저장하는 모델임. 현재는 너무 복잡하게 진행되어 있어 단순화할 계획임
# ------------------------------------------------------------------

INFO = [
    (0, "정보 미확인"),
    (1, "파트너사 정보 확인"),
    (2, "파트너사 연락"),
]

MEETING_STATE = [
    (0, "NOTSUBMIT"), # 선택되지 않음
    (1, "YES"),
    (2, "NO"),
]
class Answer(models.Model):

    content1 = models.TextField('컨텐츠1', max_length=256, blank=True, null=True)
    content2 = models.TextField('컨텐츠2', max_length=256, blank=True, null=True)
    content3 = models.TextField('컨텐츠3', max_length=256, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="프로젝트", null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="파트너",)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name="의뢰서 모델", null=True)
    check_time_client = models.DateTimeField('클라이언트 확인 시간', default = timezone.now, blank=True, null=True)
    check_time_partner = models.DateTimeField('파트너 확인 시간', default = timezone.now, blank=True, null=True)
    share_inform = models.BooleanField('정보 공개 체크', default=False)
    createdAt = models.DateTimeField('작성일', default = timezone.now)

    class Meta:
        verbose_name = '     제안서'
        verbose_name_plural = '     제안서'

    def __str__(self):
        return str(self.id)

# ------------------------------------------------------------------
# Model   : Review
# Description : 리뷰 모델 : 클라이언트의 리뷰 모델로 추후 내용에 대해서 추가될 가능성이 높다.
# ------------------------------------------------------------------
class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="프로젝트", null = True)
    isMain = models.BooleanField('메인 페이지 노출 여부', default = False)
    title = models.CharField('제목', max_length=256, blank=True, null=True)
    content = models.TextField('내용',null = True)
    createdAt = models.DateTimeField('작성일', default = timezone.now)

    class Meta:
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰'

    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    client = models.ForeignKey(Client, on_delete= models.CASCADE, verbose_name = "작성클라이언트")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name = "댓글이달린프로젝트")
    content = models.TextField('댓글 내용')
    createdAt = models.DateTimeField('등록일자', default=timezone.now)

    class Meta:
        verbose_name = '     요청사항'
        verbose_name_plural = '     요청사항'

class KakaoToken(models.Model):
    token = models.TextField()
    
