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


# �ش� ������ Version 3.0���� ���� ������ 4.0������ ������ ���� �����Դϴ�.

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
                    'message': '�ش� ������ �������� �ʽ��ϴ�.'
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
                            'message': '�̹� �亯������ �����մϴ�'
                        }
                    )
                
                if len(selectCacheList) > 0 and selectSerialized['nextTitle']: 
                    
                    previousSelectSerialized =  selectCacheList[ len(selectCacheList) - 1 ]
                    if previousSelectSerialized['nextTitle'] != selectSerialized['title']:
                        return Response(
                            status = status.HTTP_400_BAD_REQUEST,
                            data = {
                                'message': '�߸��� �亯 �����Դϴ�.'
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
                    if selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ �״�� ����" and selectCacheList[4]['select']=="��" and selectCacheList[5]['select'] !="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=1)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ ������ ���� ����" and selectCacheList[4]['select']=="��" and selectCacheList[5]['select'] !="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=2)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ�� ��� ���� ����" and selectCacheList[4]['select']=="��" and selectCacheList[5]['select'] !="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=3)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���� ��ǰ�� ���� ����ǰ ����" and selectCacheList[4]['select']=="��" and selectCacheList[5]['select'] !="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=4)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ �״�� ����" and selectCacheList[4]['select']=="��" and selectCacheList[5]['select'] =="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=5)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ ������ ���� ����" and selectCacheList[4]['select']=="��" and selectCacheList[5]['select'] =="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=6)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ�� ��� ���� ����" and selectCacheList[4]['select']=="��" and selectCacheList[5]['select'] =="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=7)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���� ��ǰ�� ���� ����ǰ ����" and selectCacheList[4]['select']=="��" and selectCacheList[5]['select'] =="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=8)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ �״�� ����" and selectCacheList[4]['select']=="�ƴϿ�" and selectCacheList[5]['select'] =="��":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=9)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ ������ ���� ����" and selectCacheList[4]['select']=="�ƴϿ�" and selectCacheList[5]['select'] =="��":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=10)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ�� ��� ���� ����" and selectCacheList[4]['select']=="�ƴϿ�" and selectCacheList[5]['select'] =="��":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=11)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ �״�� ����" and selectCacheList[4]['select']=="�ƴϿ�" and selectCacheList[5]['select'] =="�ƴϿ�":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=12)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ ������ ���� ����" and selectCacheList[4]['select']=="�ƴϿ�" and selectCacheList[5]['select'] =="�ƴϿ�":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=13)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���� ��ǰ�� ���� ����ǰ ����" and selectCacheList[4]['select']=="�ƴϿ�" and selectCacheList[5]['select'] =="�ƴϿ�":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=14)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���� ��ǰ�� ���� ����ǰ ����" and selectCacheList[4]['select']=="�ƴϿ�" and selectCacheList[5]['select'] =="��":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=15)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ�� ��� ���� ����" and selectCacheList[4]['select']=="�ƴϿ�" and selectCacheList[5]['select'] =="�ƴϿ�":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=16)
                        requestCache.proposal.save()
                    else :
                        return Response(
                            status = status.HTTP_400_BAD_REQUEST,
                            data = {
                                'message': '���Ŀ� ���� �ʽ��ϴ�'
                            }
                        )
                elif len(selectCacheList) == 5:
                    if selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ �״�� ����" and selectCacheList[3]['select']=="��" and selectCacheList[4]['select'] !="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=1)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ ������ ���� ����" and selectCacheList[3]['select']=="��" and selectCacheList[4]['select'] !="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=2)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ�� ��� ���� ����" and selectCacheList[3]['select']=="��" and selectCacheList[4]['select'] !="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=3)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���� ��ǰ�� ���� ����ǰ ����" and selectCacheList[3]['select']=="��" and selectCacheList[4]['select'] !="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=4)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ �״�� ����" and selectCacheList[3]['select']=="��" and selectCacheList[4]['select'] =="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=5)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ ������ ���� ����" and selectCacheList[3]['select']=="��" and selectCacheList[4]['select'] =="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=6)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ�� ��� ���� ����" and selectCacheList[3]['select']=="��" and selectCacheList[4]['select'] =="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=7)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���� ��ǰ�� ���� ����ǰ ����" and selectCacheList[3]['select']=="��" and selectCacheList[4]['select'] =="���ʿ���":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=8)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ �״�� ����" and selectCacheList[3]['select']=="�ƴϿ�" and selectCacheList[4]['select'] =="��":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=9)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ ������ ���� ����" and selectCacheList[3]['select']=="�ƴϿ�" and selectCacheList[4]['select'] =="��":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=10)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ�� ��� ���� ����" and selectCacheList[3]['select']=="�ƴϿ�" and selectCacheList[4]['select'] =="��":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=11)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ �״�� ����" and selectCacheList[3]['select']=="�ƴϿ�" and selectCacheList[4]['select'] =="�ƴϿ�":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=12)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ ������ ���� ����" and selectCacheList[3]['select']=="�ƴϿ�" and selectCacheList[4]['select'] =="�ƴϿ�":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=13)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���� ��ǰ�� ���� ����ǰ ����" and selectCacheList[3]['select']=="�ƴϿ�" and selectCacheList[4]['select'] =="�ƴϿ�":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=14)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���� ��ǰ�� ���� ����ǰ ����" and selectCacheList[3]['select']=="�ƴϿ�" and selectCacheList[4]['select'] =="��":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=15)
                        requestCache.proposal.save()
                    elif selectCacheList[0]['select'] == "���߿� �ǸŵǴ� ��ǰ�� ��� ���� ����" and selectCacheList[3]['select']=="�ƴϿ�" and selectCacheList[4]['select'] =="�ƴϿ�":
                        requestCache.proposal.proposalType = ProposalType.objects.get(id=16)
                        requestCache.proposal.save()
                    else :
                        return Response(
                            status = status.HTTP_400_BAD_REQUEST,
                            data = {
                                'message': '���Ŀ� ���� �ʽ��ϴ�'
                            }
                        )
                else:
                    return Response(
                            status = status.HTTP_400_BAD_REQUEST,
                            data = {
                                'message': '������ ������ �ùٸ��� �ʽ��ϴ�.'
                            }
                        )

            else :
                for save in saveCacheList:
                    tempData = DetailQuestionSave.objects.create(request = save['request'], question = save['question'], select = save['select'])
                
                requestCache.project.progressStep = '��������'
                requestCache.project.save()
                requestCache.proposal.proposalType = ProposalType.objects.get(name="�����Է�Ÿ��")
                requestCache.proposal.save()
                return Response(
                    status = status.HTTP_201_CREATED,
                    data = {
                        'message': '�亯 ������ �����Ͽ����ϴ�(�����Է�)',
                        'proposalId' : requestCache.proposal.id
                    }
                )   

            for save in saveCacheList:
                tempData = DetailQuestionSave.objects.create(request = save['request'], question = save['question'], select = save['select'])
            print("ī�װ�����?",type(requestCache.product.maincategory.maincategory))
            print("ī�װ�����?",requestCache.product.maincategory.maincategory)
            
            if requestCache.product.maincategory.maincategory != "��ǰ �� ��ǰ":

                requestCache.project.progressStep = '��������'
                requestCache.project.save()
                requestCache.proposal.proposalType = ProposalType.objects.get(name='������Ȯ�δܰ����������������Ȯ�θ���Ÿ��')
                requestCache.proposal.save()

                return Response(
                    status = status.HTTP_201_CREATED,
                    data = {
                        'message': '�亯 ������ �����Ͽ����ϴٸ� ��ǰ�������� �ƴ϶� �������� Ȯ������ ���մϴ�.',
                        'proposalId' : requestCache.proposal.id
                    }
                )

            requestCache.project.progressStep = '��������'
            requestCache.project.save()

            return Response(
                status = status.HTTP_201_CREATED,
                data = {
                    'message': '�亯 ������ �����Ͽ����ϴ�',
                    'proposalId' : requestCache.proposal.id
                }
            )
        
        except DetailQuestionTitle.DoesNotExist:
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
                data = {
                    'message': '�亯�� �������� �ʽ��ϴ�'
                }
            )
        
        except DetailQuestionSelect.DoesNotExist:
            return Response(
                     status = status.HTTP_400_BAD_REQUEST,
                     data = {
                        'message': '������ �������� �ʽ��ϴ�'
                    }
            )
        except Request.DoesNotExist:
            return Response(
                    status = status.HTTP_400_BAD_REQUEST,
                    data = {
                        'message': '�Ƿڼ��� �������� �ʽ��ϴ�'
                    }
            )
