#-*- coding: cp949 -*-
from rest_framework import (
    viewsets,
    status,
    mixins,
)
from rest_framework.decorators import action
from rest_framework.response import Response
#pagenation
from .paginations import *

#django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.utils import *

from .serializers import *

# models
from apps.detailQuestion.models import *
from apps.project.models import Request


# 해당 로직은 Version 3.0에서 사용된 것으로 4.0에서는 사용되지 않을 예정입니다.

class DetailQuestionTitleViewSet(viewsets.ModelViewSet):
    """
    DetailQuestionTitle
    """
    queryset = DetailQuestionTitle.objects.order_by('id')
    serializer_class = DetailQuestionTitleSerializer
    @action(detail=False, methods=['POST',], url_path='detailQuestionSelect', http_method_names=('post',))
    def get_select(self, request, *args, **kwargs):
        title_id = request.data.get("title_id")
        title = DetailQuestionTitle.objects.filter(id = int(title_id))
        select_list = DetailQuestionSelect.objects.filter(title = title_id)
        
        
        return Response(data={'code': ResponseCode.SUCCESS.value,
                              'title': DetailQuestionTitleSerializer(title, many=True).data,
                              'data': DetailQuestionSelectSerializer(select_list, many=True).data
                              })
    
class DetailQuestionSelectViewSet (viewsets.ModelViewSet):
    """
    DetailQuestionSelect
    """
    queryset = DetailQuestionSelect.objects.all()
    serializer_class = DetailQuestionSelectSerializer

    @action (detail = False, methods = ['GET'], url_path = 'detailQuestionTitle') 
    def selectFromTitleId (self, request, *args, **kwargs):
        titleId = request.GET['titleId']
        try:
            titleCache = DetailQuestionTitle.objects.get(id = titleId)
        except DetailQuestionTitle.DoesNotExist:
            return Response(
                data = {
                    'message': '해당 질문이 존재하지 않습니다.'
                },
                status = status.HTTP_400_BAD_REQUEST,
            )
        
        select_list = DetailQuestionSelect.objects.filter(title = titleId)
        count = len(select_list)

        return Response(
            data = {
                'title': titleId,
                'count': count,
                'data': DetailQuestionSelectSerializer(select_list, many = True).data
            },
            status = status.HTTP_200_OK
        )
    
class DetailQuestionSaveViewSet (viewsets.ModelViewSet):
    """
    DetailQuestionSave
    """
    queryset = DetailQuestionSave.objects.all()
    serializer_class = DetailQuestionSaveSerializer

    #@action (detail = False, methods = ['POST'], url_path = 'saveByList')
    def create (self, request, *args, **kwargs):
        requestId = request.data.get('request')
        saveDatas = request.data.get('data')
        
        saveCacheList = []
        selectCacheList = []
        try:
            requestCache = Request.objects.get(id = requestId)
            for save in saveDatas:
                titleId = save['title_id']
                selectId = save['title_select']
                titleCache = DetailQuestionTitle.objects.get(id = titleId)
                selectCache = DetailQuestionSelect.objects.get(id = selectId, title = titleId)
                selectSerialized = DetailQuestionSelectSerializer(selectCache).data
                duplicateChcek = DetailQuestionSave.objects.filter( request_id = requestId, question_id = titleId)

                if duplicateChcek:
                    return Response(
                        status = status.HTTP_400_BAD_REQUEST,
                        data = {
                            'message': '이미 답변내용이 존재합니다'
                        }
                    )
                
                if len(selectCacheList) > 0 and selectSerialized['nextTitle']: 
                    
                    previousSelectSerialized =  selectCacheList[ len(selectCacheList) - 1 ]
                    if previousSelectSerialized['nextTitle'] != selectSerialized['title']:
                        return Response(
                            status = status.HTTP_400_BAD_REQUEST,
                            data = {
                                'message': '잘못된 답변 조합입니다.'
                            }
                        )   
                        
                saveCacheList.append({
                    'request': requestCache,
                    'question': titleCache,
                    'select': selectCache,
                })

                selectCacheList.append(selectSerialized)
            for i in selectCacheList:
                print(i)   
        
            if len(selectCacheList) != 3:
                if len(selectCacheList) == 6: 
                    if selectCacheList[0]['select'] == "시중에 판매되는 제품 그대로 개발" and selectCacheList[4]['select']=="예" and selectCacheList[5]['select'] !="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=1)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 디자인 변경 개발" and selectCacheList[4]['select']=="예" and selectCacheList[5]['select'] !="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=2)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품의 기능 변경 개발" and selectCacheList[4]['select']=="예" and selectCacheList[5]['select'] !="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=3)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "기존 제품이 없는 신제품 개발" and selectCacheList[4]['select']=="예" and selectCacheList[5]['select'] !="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=4)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 그대로 개발" and selectCacheList[4]['select']=="예" and selectCacheList[5]['select'] =="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=5)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 디자인 변경 개발" and selectCacheList[4]['select']=="예" and selectCacheList[5]['select'] =="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=6)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품의 기능 변경 개발" and selectCacheList[4]['select']=="예" and selectCacheList[5]['select'] =="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=7)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "기존 제품이 없는 신제품 개발" and selectCacheList[4]['select']=="예" and selectCacheList[5]['select'] =="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=8)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 그대로 개발" and selectCacheList[4]['select']=="아니요" and selectCacheList[5]['select'] =="예":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=9)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 디자인 변경 개발" and selectCacheList[4]['select']=="아니요" and selectCacheList[5]['select'] =="예":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=10)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품의 기능 변경 개발" and selectCacheList[4]['select']=="아니요" and selectCacheList[5]['select'] =="예":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=11)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 그대로 개발" and selectCacheList[4]['select']=="아니요" and selectCacheList[5]['select'] =="아니요":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=12)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 디자인 변경 개발" and selectCacheList[4]['select']=="아니요" and selectCacheList[5]['select'] =="아니요":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=13)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "기존 제품이 없는 신제품 개발" and selectCacheList[4]['select']=="아니요" and selectCacheList[5]['select'] =="아니요":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=14)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "기존 제품이 없는 신제품 개발" and selectCacheList[4]['select']=="아니요" and selectCacheList[5]['select'] =="예":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=15)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품의 기능 변경 개발" and selectCacheList[4]['select']=="아니요" and selectCacheList[5]['select'] =="아니요":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=16)
                        requestCache.proposal.save()
                    else :
                        return Response(
                            status = status.HTTP_400_BAD_REQUEST,
                            data = {
                                'message': '형식에 맞지 않습니다'
                            }
                        )
                elif len(selectCacheList) == 5:
                    if selectCacheList[0]['select'] == "시중에 판매되는 제품 그대로 개발" and selectCacheList[3]['select']=="예" and selectCacheList[4]['select'] !="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=1)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 디자인 변경 개발" and selectCacheList[3]['select']=="예" and selectCacheList[4]['select'] !="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=2)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품의 기능 변경 개발" and selectCacheList[3]['select']=="예" and selectCacheList[4]['select'] !="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=3)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "기존 제품이 없는 신제품 개발" and selectCacheList[3]['select']=="예" and selectCacheList[4]['select'] !="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=4)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 그대로 개발" and selectCacheList[3]['select']=="예" and selectCacheList[4]['select'] =="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=5)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 디자인 변경 개발" and selectCacheList[3]['select']=="예" and selectCacheList[4]['select'] =="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=6)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품의 기능 변경 개발" and selectCacheList[3]['select']=="예" and selectCacheList[4]['select'] =="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=7)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "기존 제품이 없는 신제품 개발" and selectCacheList[3]['select']=="예" and selectCacheList[4]['select'] =="불필요함":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=8)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 그대로 개발" and selectCacheList[3]['select']=="아니요" and selectCacheList[4]['select'] =="예":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=9)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 디자인 변경 개발" and selectCacheList[3]['select']=="아니요" and selectCacheList[4]['select'] =="예":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=10)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품의 기능 변경 개발" and selectCacheList[3]['select']=="아니요" and selectCacheList[4]['select'] =="예":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=11)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 그대로 개발" and selectCacheList[3]['select']=="아니요" and selectCacheList[4]['select'] =="아니요":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=12)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품 디자인 변경 개발" and selectCacheList[3]['select']=="아니요" and selectCacheList[4]['select'] =="아니요":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=13)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "기존 제품이 없는 신제품 개발" and selectCacheList[3]['select']=="아니요" and selectCacheList[4]['select'] =="아니요":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=14)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "기존 제품이 없는 신제품 개발" and selectCacheList[3]['select']=="아니요" and selectCacheList[4]['select'] =="예":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=15)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "시중에 판매되는 제품의 기능 변경 개발" and selectCacheList[3]['select']=="아니요" and selectCacheList[4]['select'] =="아니요":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=16)
                        requestCache.proposal.save()
                    else :
                        return Response(
                            status = status.HTTP_400_BAD_REQUEST,
                            data = {
                                'message': '형식에 맞지 않습니다'
                            }
                        )
                else:
                    return Response(
                            status = status.HTTP_400_BAD_REQUEST,
                            data = {
                                'message': '선택지 개수가 올바르지 않습니다.'
                            }
                        )

            else :
                for save in saveCacheList:
                    tempData = DetailQuestionSave.objects.create(request = save['request'], question = save['question'], select = save['select'])
                
                requestCache.project.progressStep = '세부질문'
                requestCache.project.save()
                requestCache.proposal.proposalType = ProposalType.objects.get(name="도면입력타입")
                requestCache.proposal.save()
                return Response(
                    status = status.HTTP_201_CREATED,
                    data = {
                        'message': '답변 내용을 저장하였습니다(도면입력)',
                        'proposalId' : requestCache.proposal.id
                    }
                )   

            for save in saveCacheList:
                tempData = DetailQuestionSave.objects.create(request = save['request'], question = save['question'], select = save['select'])
            print("카테고리뭔데?",type(requestCache.product.maincategory.maincategory))
            print("카테고리뭔데?",requestCache.product.maincategory.maincategory)
            
            if requestCache.product.maincategory.maincategory != "제품 및 용품":

                requestCache.project.progressStep = '세부질문'
                requestCache.project.save()
                requestCache.proposal.proposalType = ProposalType.objects.get(name='견적서확인단계까지왔지만견적서확인못한타입')
                requestCache.proposal.save()

                return Response(
                    status = status.HTTP_201_CREATED,
                    data = {
                        'message': '답변 내용을 저장하였습니다만 제품및응용이 아니라서 견적서를 확인하지 못합니다.',
                        'proposalId' : requestCache.proposal.id
                    }
                )

            requestCache.project.progressStep = '세부질문'
            requestCache.project.save()

            return Response(
                status = status.HTTP_201_CREATED,
                data = {
                    'message': '답변 내용을 저장하였습니다',
                    'proposalId' : requestCache.proposal.id
                }
            )
        
        except DetailQuestionTitle.DoesNotExist:
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
                data = {
                    'message': '답변이 존재하지 않습니다'
                }
            )
        
        except DetailQuestionSelect.DoesNotExist:
            return Response(
                     status = status.HTTP_400_BAD_REQUEST,
                     data = {
                        'message': '질문이 존재하지 않습니다'
                    }
            )
        except Request.DoesNotExist:
            return Response(
                    status = status.HTTP_400_BAD_REQUEST,
                    data = {
                        'message': '의뢰서가 존재하지 않습니다'
                    }
            )
