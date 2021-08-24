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

# filename 자동 변경
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
# Description : 회원 모델
# ------------------------------------------------------------------
USER_TYPE = [
    (0, "CLIENT"),
    (1, "PARTNER")
]
class User(AbstractUser):

    # 공통 부분
    username = models.CharField('이메일', max_length=256, default=get_default_hash_id, unique=True)
    type = models.IntegerField('유저타입', default=0, choices=USER_TYPE)
    password = models.CharField(max_length=256)
    phone = models.CharField('휴대폰 번호', max_length=100, blank=True)
    marketing = models.BooleanField('마케팅동의여부', default=True, null=True)
    last_activity = models.DateTimeField('최근 활동', default = None, blank = True, null = True)

    class Meta:
        verbose_name = '가입자'
        verbose_name_plural = '가입자'
        
    @property
    def is_update(self):
        if self.username and self.type and self.password:
            return True
        else:
            return False

# ------------------------------------------------------------------
# Model   : Client
# Description : 클라이언트 모델
# ------------------------------------------------------------------

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='유저')
    name = models.CharField('업체명', max_length=256, null=True)
    title = models.CharField('직급', max_length=256, null=True)
    realName = models.CharField('이름', max_length=256, null=True)
    department = models.CharField('부서', max_length=256, null=True)
    path = models.CharField('방문경로', max_length=256, null=True)
    business = models.CharField('업종', max_length=256, null=True)
    email = models.CharField('이메일', max_length=256, null=True)
    
    class Meta:
        verbose_name = '클라이언트'
        verbose_name_plural = '클라이언트'

    def __str__(self):
        return str(self.user.username)

# ------------------------------------------------------------------
# Model   : Partner
# Description : 파트너 모델
# ------------------------------------------------------------------

class Partner(models.Model):
    sales_state = [
        ('0','5천만원 미만'),
        ('1','5천~1억원 미만'),
        ('2','1억~5억원 미만'),
        ('3','5억~10억원 미만'),
        ('4','10억원~50억원 미만'),
        ('5','50억~100억원 미만'),
        ('6','100억~200억원 미만'),
        ('7','200억~400억원 미만'),
        ('8','400억~600억원 미만'),
        ('9','600억~800억원 미만'),
        ('10','800억~1,000억원 미만'),
        ('11','1,000억~1,500억원 미만'),
        ('12','1,500억원 이상'),
    ]
    staff_state = [
        ('0', '1~4인'),
        ('1', '5~9인'),
        ('2', '10~29인'),
        ('3', '30~49인'),
        ('4', '50~99인'),
        ('5', '100~199인'),
        ('6', '200~299인'),
        ('7', '300~499인'),
        ('8', '500~999인'),
        ('9', '1000인이상'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='유저')
    name = models.CharField('업체명', max_length=256, null=True)
    title = models.CharField('직급', max_length=256, null=True,blank=True)
    realName = models.CharField('이름', max_length=256, null=True,blank=True)
    logo = models.ImageField('로고', upload_to=partner_update_filename, blank=True, null=True)
    info_company = models.TextField('회사소개', blank=True, null=True)
    history = models.TextField('진행한 제품들', blank=True, null=True)
    deal = models.TextField('주요거래처', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="시/도", null=True)
    region = models.CharField('상세 주소', max_length=256, null=True)
    business = models.ManyToManyField(Business, verbose_name="업체중분류", blank=True)
    category = models.ManyToManyField(Category, verbose_name='만들제품분류', blank=True)
    subcategory = models.ManyToManyField(Subcategory, verbose_name='만들제품분류(소)', blank=True)
    material = models.ManyToManyField(Material, verbose_name='소재 분류', blank=True)
    develop = models.ManyToManyField(Develop, verbose_name='공정분류', blank=True)
    file = models.FileField('회사소개 및 포토폴리오파일', upload_to=partner_update_filename, blank=True, null=True)
    resume = models.FileField('이력서', upload_to=partner_update_filename, blank=True, null=True)
    avg_score = models.DecimalField('평균점수', default=0, max_digits=5, decimal_places=2, null=True)
    real_phone = models.CharField('실제 휴대폰 번호', max_length=255, blank=True, null=True)
    idenfication_state = models.BooleanField('확인 기업', default=False)
    chat_state = models.BooleanField('채팅 가능', default=False)
    Certification = models.FileField('인증서', upload_to=certification_update_filename, null=True,blank=True)
    CEO = models.CharField('대표자', max_length=256,blank=True, null=True)
    sales = models.CharField('매출액', max_length=10,choices=sales_state, blank=True, null=True)
    staff = models.CharField('직원수', max_length=10, choices=staff_state, blank=True, null=True)
    year = models.CharField('설립연도', max_length=10,blank=True, null=True, default='0000')
    certification_list = models.CharField('인증서 목록', max_length=512,blank=True, null=True)
    view = models.IntegerField('조회수', default=0)


    class Meta:
        verbose_name = '파트너'
        verbose_name_plural = '파트너'

    def __str__(self):
        return str(self.name)

# ------------------------------------------------------------------
# Model   : SNS 로그인 모델
# Description : 회원 모델
# ------------------------------------------------------------------
SNS_TYPE = [
    (0, "NAVER"),
    (1, "KAKAO")
]
class Snsuser(models.Model):

    # 공통 부분
    token = models.CharField('토큰', max_length=256, unique=True)
    username = models.CharField('이메일', max_length=256, unique=True)
    sns = models.IntegerField('SNS타입', default=0, choices=SNS_TYPE)

    class Meta:
        verbose_name = 'SNS 연동 유저'
        verbose_name_plural = 'SNS 연동 유저'
        
    def __str__(self):
        return str(self.username)


# ------------------------------------------------------------------
# Model   : Portfolio
# Description : 포트폴리오 모델
# ------------------------------------------------------------------
class Portfolio(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="파트너", null=True)
    name = models.CharField('이미지 명', max_length=256, null=True)
    img_portfolio = models.ImageField('포토폴리오 이미지', upload_to=portfolio_update_filename, null=True)
    is_main = models.BooleanField('메인 여부', default=False)

    class Meta:
        verbose_name = '파트너 제작 제품'
        verbose_name_plural = '파트너 제작 제품'

    def __str__(self):
        return str(self.partner.name) + " 파트너 제작 제품"

# ------------------------------------------------------------------
# Model   : Label
# Description : 포트폴리오 모델
# ------------------------------------------------------------------
class Label(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, verbose_name="파트너 제작 제품 라벨",related_name='라벨', null=True)
    label = models.CharField('이미지 명', max_length=256, null=True)
    score = models.FloatField('유사도', default=0,null=True )

    class Meta:
        verbose_name = '라벨'
        verbose_name_plural = '라벨'

    def __str__(self):
        return str(self.label)
        

# ------------------------------------------------------------------
# Model   : Path
# Description : 방문경로 저장 모델
# ------------------------------------------------------------------
class Path(models.Model):
    path = models.CharField('방문경로', max_length=256, null=True)


    class Meta:
        verbose_name = '방문경로'
        verbose_name_plural = '방문경로'

    def __str__(self):
        return str(self.path)

# ------------------------------------------------------------------
# Model   : Busincess
# Description : 업종 로그 저장 모델
# ------------------------------------------------------------------
class Business_client(models.Model):
    business = models.CharField('업종', max_length=256, null=True)


    class Meta:
        verbose_name = '업종'
        verbose_name_plural = '업종'

    def __str__(self):
        return str(self.business)


# ------------------------------------------------------------------
# Model   : Partner Review
# Description : 파트너 리뷰 테이블
# ------------------------------------------------------------------
# REVIEW_TYPE = [
#     (1, "매우 불만족"),
#     (2, "불만족"),
#     (3, "보통"),
#     (4, "만족"),
#     (5, "매우 만족"),
# ]
# class PartnerReview(models.Model):

#     partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="파트너", null=True)
#     client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="클라이언트", null=True)
#     score = models.IntegerField('점수', default=0, choices=REVIEW_TYPE)
#     content = models.CharField('컨텐츠', max_length=256, null=True)

#     class Meta:
#         verbose_name = '파트너 리뷰'
#         verbose_name_plural = '파트너 리뷰'

#     def __str__(self):
#         return str(self.score)

class PartnerReview(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name="파트너", null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="클라이언트", null=True)
    projectname = models.CharField('프로젝트 이름', max_length=256, null=True)
    consult_score = models.IntegerField('상담 점수', default=0)
    kindness_score = models.IntegerField('친절 점수', default=0)
    communication_score = models.IntegerField('소통 점수', default=0)
    profession_score = models.IntegerField('전문성 점수', default=0)
    content = models.TextField('리뷰내용', blank=True, null=True)
    new_partner = models.IntegerField('새로운 제조사', null=True)
    partner_name = models.CharField('새로운 제조사 이름', max_length=256, null=True)
    date = models.CharField('리뷰 작성 시간', max_length=256, null=True)

    class Meta:
        verbose_name = '파트너 리뷰'
        verbose_name_plural = '파트너 리뷰'





# ------------------------------------------------------------------
# Model   : Partner Review_temp
# Description : 파트너 임시 리뷰 테이블 : 리뷰 받기를 위한 임시 내용
# ------------------------------------------------------------------
REVIEW_TYPE = [
    (1, "매우 불만족"),
    (2, "불만족"),
    (3, "보통"),
    (4, "만족"),
    (5, "매우 만족"),
]
class PartnerReviewTemp(models.Model):

    partnername = models.CharField('업체명', max_length=256, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="클라이언트", null=True)
    score = models.IntegerField('점수', default=0, choices=REVIEW_TYPE)
    content = models.CharField('컨텐츠', max_length=256, null=True)

    class Meta:
        verbose_name = '파트너 임시 리뷰'
        verbose_name_plural = '파트너 임시 리뷰'

    def __str__(self):
        return str(self.score)

class CsvFileUpload(models.Model):
    filename = models.CharField("파일이름", max_length=256, null=True)
    partner_info_file = models.FileField('파트너정보 파일',upload_to=partner_update_filename,max_length=255, blank=True, null=True)
    portfolio_file = models.FileField('포트폴리오 파일',upload_to=partner_update_filename,max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = '파일이름'
        verbose_name_plural = '파일이름'

    def __str__(self):
        return str(self.filename)

#본섭 추가
# ------------------------------------------------------------------
# Model   : Bookmark
# Description : 클라이언트 관심파트너 저장
# ------------------------------------------------------------------
class Bookmark(models.Model):
    client =  models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='클라이언트')
    bookmark_partner = models.ForeignKey(Partner, on_delete=models.CASCADE, verbose_name='관심 기업')


    class Meta:
        verbose_name = '관심 파트너 북마크'
        verbose_name_plural = '관심 파트너 북마크'

    def __str__(self):
        return str(self.bookmark_partner)