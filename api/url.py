from django.urls import include, path
from rest_framework import routers
from django.conf.urls import url
from api.account import viewsets as view_account
from api.board import viewsets as view_board
from api.category import viewsets as view_category
from api.detailQuestion import viewsets as view_detailQuestion
from api.payment import viewsets as view_payment
from api.project import viewsets as view_project    
from api.estimate import viewsets as view_estimate
from api.schedule import viewsets as view_schedule
from api.shop import viewsets as view_shop
from api.chat import viewsets as view_chat
from api.log import viewsets as view_log
# from api.kakaotalk import viewsets as view_kakao


from typing import TYPE_CHECKING
app_name = 'api'

router = routers.DefaultRouter()
#account
router.register('users', view_account.UserViewSet)
router.register('client', view_account.ClientViewSet)
router.register('partner', view_account.PartnerViewSet)
router.register('portfolio', view_account.PortfolioViewSet)
router.register('path', view_account.PathViewSet)
router.register('business', view_account.BusinessViewSet)
router.register('partnerreview', view_account.PartnerReviewViewSet)
router.register('partnerreviewtemp', view_account.PartnerReviewTempViewSet)
router.register('csvfileupload', view_account.CsvFileuploadViewSet)

#board
router.register('magazine', view_board.MagazineViewSet)
router.register('magazine_category', view_board.MagazineCategoryViewSet)
#category
router.register('maincategory', view_category.MaincategoryViewSet)
router.register('category', view_category.CategoryViewSet)
router.register('subclass', view_category.SubclassViewSet)
router.register('city', view_category.CityViewSet)
router.register('develop', view_category.DevelopViewSet)
router.register('developbig', view_category.DevelopbigViewSet)

#payment
router.register('paylist', view_payment.PaylistViewSet)

#project
router.register('project', view_project.ProjectViewSet)
router.register('requests', view_project.RequestViewSet)
router.register('requestfile', view_project.RequestFileViewSet)
router.register('answer', view_project.AnswerViewSet)
router.register('review', view_project.ReviewViewSet)

#estimate
router.register('estimate', view_estimate.EstimateViewSet)
router.register('manufactureProcess', view_estimate.ManufactureProcessViewSet)


#schedule
router.register('schedule', view_schedule.ScheduleViewSet)

#shop
router.register('shop', view_shop.OrderViewSet)

#log
router.register('clicklog', view_log.ClickLogViewSet)
router.register('chatlog', view_log.ChatViewSet)
router.register('searchtextlog', view_log.SearchTextViewSet)



urlpatterns = [
    path('', include(router.urls))
]
