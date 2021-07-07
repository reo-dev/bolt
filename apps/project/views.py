#-- coding: cp949 --
from django.shortcuts import render
from apps.account.models import *
from apps.project.models import *
from apps.category.models import *
from django.db.models import Subquery
from django.db.models import Count
from django.db.models import Sum
# Create your views here.

# 클라이언트 정보 반환
def getClient(queryPath, queryTitle, queryBusiness):
    obj = {}
    client = Client.objects
    
    if queryPath != None:
        client = client.filter(path=queryPath)
    if queryTitle != None:
        client = client.filter(title=queryTitle)
    if queryBusiness != None:
        client = client.filter(business=queryBusiness) 
        
    originClientPath     = Client.objects.values('path').annotate(path_count=Count('path')).order_by('-path_count')[:5]
    originClientTitle    = Client.objects.values('title').annotate(title_count=Count('title')).order_by('-title_count')[:5]
    originClientBusiness = Client.objects.values('business').annotate(business_count=Count('business')).order_by('-business_count')[:5]
    clientPath           = client.values('path').annotate(path_count=Count('path')).order_by('-path_count')[:5]
    clientTitle          = client.values('title').annotate(title_count=Count('title')).order_by('-title_count')[:5]
    clientBusiness       = client.values('business').annotate(business_count=Count('business')).order_by('-business_count')[:5]

    obj['originClientPath']     = originClientPath
    obj['originClientTitle']    = originClientTitle
    obj['originClientBusiness'] = originClientBusiness
    obj['clientPath']           = clientPath
    obj['clientTitle']          = clientTitle
    obj['clientBusiness']       = clientBusiness
    
    return obj



# 의뢰서를 작성한 클라이언트 정보 반환
def getRequestClient(queryRequestPath, queryRequestTitle, queryRequestBusiness):
    obj = {}
    requestClient       = Client.objects.filter(id__in=Subquery(Request.objects.values('client_id'))).values()
    originRequestClient = requestClient
    
    if queryRequestPath != None:
        requestClient = requestClient.filter(path=queryRequestPath)
    if queryRequestTitle != None:
        requestClient = requestClient.filter(title=queryRequestTitle)
    if queryRequestBusiness != None:
        requestClient = requestClient.filter(business=queryRequestBusiness)
    
    originRequestClientPath     = originRequestClient.values('path').annotate(path_count=Count('path')).order_by('-path_count')[:5]
    originRequestClientTitle    = originRequestClient.values('title').annotate(title_count=Count('title')).order_by('-title_count')[:5]
    originRequestClientBusiness = originRequestClient.values('business').annotate(business_count=Count('business')).order_by('-business_count')[:5]
    requestClientPath           = requestClient.values('path').annotate(path_count=Count('path')).order_by('-path_count')[:5]
    requestClientTitle          = requestClient.values('title').annotate(title_count=Count('title')).order_by('-title_count')[:5]
    requestClientBusiness       = requestClient.values('business').annotate(business_count=Count('business')).order_by('-business_count')[:5]
    
    obj['originRequestClientPath']     = originRequestClientPath
    obj['originRequestClientTitle']    = originRequestClientTitle
    obj['originRequestClientBusiness'] = originRequestClientBusiness
    obj['requestClientPath']           = requestClientPath
    obj['requestClientTitle']          = requestClientTitle
    obj['requestClientBusiness']       = requestClientBusiness
    
    return obj



# 의뢰서에 대한 정보 반환
def getProgressStatus(queryProgressStatus, queryRequestGte, queryRequestLte):
    obj = {}
    if (queryRequestGte == None) and (queryRequestLte == None):
        requestObj = Request.objects
        today      = datetime.datetime.today()
        dayFilter  = datetime.datetime(today.year, today.month, today.day) - datetime.timedelta(6)
        requestObj = requestObj.filter(created_at__gte=dayFilter)
    else:
        requestObj = Request.objects
    
    if queryRequestGte != None:
        queryRequestGte = list(map(int, queryRequestGte.split('-')))
        requestObj      = requestObj.filter(created_at__gte=datetime.datetime(queryRequestGte[0], queryRequestGte[1], queryRequestGte[2], 0, 0))
    if queryRequestLte != None:
        queryRequestLte = list(map(int, queryRequestLte.split('-')))
        requestObj      = requestObj.filter(created_at__lte=datetime.datetime(queryRequestLte[0], queryRequestLte[1], queryRequestLte[2], 23, 59))
    
    requestObj = requestObj.values('created_at').annotate(created_at_count=Count('created_at')).order_by('created_at')

    progressStatus = Request.objects
    if queryProgressStatus != None:
        progressStatus = progressStatus.filter(progress_status=queryProgressStatus)
    if queryRequestGte != None:
        progressStatus = progressStatus.filter(created_at__gte=datetime.datetime(queryRequestGte[0], queryRequestGte[1], queryRequestGte[2], 0, 0))
    if queryRequestLte != None:
        progressStatus = progressStatus.filter(created_at__lte=datetime.datetime(queryRequestLte[0], queryRequestLte[1], queryRequestLte[2], 23, 59))

    originProgress = Request.objects.values('progress_status').annotate(progress_status_count=Count('progress_status'))
    progressStatus = progressStatus.values('progress_status').annotate(progress_status_count=Count('progress_status'))

    obj['requestObj']     = requestObj
    obj['originProgress'] = originProgress
    obj['progressStatus'] = progressStatus
    
    return obj
    
    
    
def getEstimate(queryEstimateGte, queryEstimateLte):
    estimateObj = Request.objects.all()
    
    if queryEstimateGte != None:
        queryEstimateGte = list(map(int, queryEstimateGte.split('-')))
        estimateObj = estimateObj.filter(created_at__gte=datetime.datetime(queryEstimateGte[0], queryEstimateGte[1], queryEstimateGte[2], 0, 0))
    if queryEstimateLte != None:
        queryEstimateLte = list(map(int, queryEstimateLte.split('-')))
        estimateObj = estimateObj.filter(created_at__lte=datetime.datetime(queryEstimateLte[0], queryEstimateLte[1], queryEstimateLte[2], 23, 59)) 
    
    progress0Sum = estimateObj.filter(progress_status='미정').aggregate(Sum('estimate'))['estimate__sum']
    if progress0Sum == None:
        progress0Sum = 0
    progress1Sum = estimateObj.filter(progress_status='드랍').aggregate(Sum('estimate'))['estimate__sum']
    if progress1Sum == None:
        progress1Sum = 0
    progress2Sum = estimateObj.filter(progress_status='진행중').aggregate(Sum('estimate'))['estimate__sum']
    if progress2Sum == None:
        progress2Sum = 0
    progress3Sum = estimateObj.filter(progress_status='전환').aggregate(Sum('estimate'))['estimate__sum']
    if progress3Sum == None:
        progress3Sum = 0
    
    estimateList = {'progress0':'미정',   'progress0Sum':progress0Sum,
                    'progress1':'드랍',   'progress1Sum':progress1Sum,
                    'progress2':'진행중', 'progress2Sum':progress2Sum, 
                    'progress3':'전환',   'progress3Sum':progress3Sum}

    return estimateList



def getMaincategory(queryMaincategory, queryMaincategoryGte, queryMaincategoryLte):
    obj = {}
    maincategoryObj        = Maincategory.objects.values('id', 'maincategory')
    subclassObj            = Subclass.objects.values()
    requestMaincategoryObj = Request.objects.filter(created_at__gte=datetime.datetime(2020, 9, 1, 0, 0))
    
    if queryMaincategoryGte != None:
        queryMaincategoryGte = list(map(int, queryMaincategoryGte.split('-')))
        requestMaincategoryObj = requestMaincategoryObj.filter(created_at__gte=datetime.datetime(queryMaincategoryGte[0], queryMaincategoryGte[1], queryMaincategoryGte[2], 0, 0))
    if queryMaincategoryLte != None:
        queryMaincategoryLte = list(map(int, queryMaincategoryLte.split('-')))
        requestMaincategoryObj = requestMaincategoryObj.filter(created_at__lte=datetime.datetime(queryMaincategoryLte[0], queryMaincategoryLte[1], queryMaincategoryLte[2], 23, 59))   
    
    requestMaincategoryObj = requestMaincategoryObj.values('product').annotate(cnt=Count('product')).order_by('-cnt')
    
    maincategoryLength = 0
    
    linkDic              = {}
    maincategoryCountDic = {}
    maincategoryList     = []
    
    # subclass -> maincategory 연결
    for i in subclassObj:
        linkDic[i['id']] = i['maincategory_id']
    
    # reset maincategoryCountDic -> 0
    for i in maincategoryObj:
        maincategoryCountDic[i['id']] = 0
    
    if queryMaincategory != None:
        queryMaincategory = maincategoryObj.filter(maincategory=queryMaincategory)[0]['id']
    
    for i in requestMaincategoryObj:
        if queryMaincategory != None:
            if queryMaincategory == linkDic[i['product']]:
                maincategoryCountDic[linkDic[i['product']]] += i['cnt']
                maincategoryLength += i['cnt']
            else:
                maincategoryLength += i['cnt']
        else:
            maincategoryCountDic[linkDic[i['product']]] += i['cnt']
            maincategoryLength += i['cnt']

    for i in maincategoryCountDic:
        maincategoryName = maincategoryObj.filter(id=i)[0]['maincategory']
        maincategoryList.append({ 'maincategory':maincategoryName, 'count':maincategoryCountDic[i], 'percentage':round(maincategoryCountDic[i]/maincategoryLength*100,2) })

    obj['originMaincategory'] = maincategoryObj
    obj['maincategoryList']   = maincategoryList
    obj['maincategoryLength'] = maincategoryLength
    
    return obj




def chart(request):
    context = {}    
    
    ######################
    #클라이언트
    ######################
    queryPath     = request.GET.get('path')
    queryTitle    = request.GET.get('title')
    queryBusiness = request.GET.get('business')
    
    clientObj = getClient(queryPath, queryTitle, queryBusiness)
    
    context['originClientPath']     = clientObj['originClientPath']
    context['originClientTitle']    = clientObj['originClientTitle']
    context['originClientBusiness'] = clientObj['originClientBusiness']
    context['clientPath']           = clientObj['clientPath']
    context['clientTitle']          = clientObj['clientTitle']
    context['clientBusiness']       = clientObj['clientBusiness']
    
    
    
    #############################
    #의뢰서를 작성한 클라이언트
    #############################
    queryRequestPath     = request.GET.get('requestPath')
    queryRequestTitle    = request.GET.get('requestTitle')
    queryRequestBusiness = request.GET.get('requestBusiness')
    
    requestClientObj = getRequestClient(queryRequestPath, queryRequestTitle, queryRequestBusiness)
    
    context['originRequestClientPath']     = requestClientObj['originRequestClientPath']
    context['originRequestClientTitle']    = requestClientObj['originRequestClientTitle']
    context['originRequestClientBusiness'] = requestClientObj['originRequestClientBusiness']
    context['requestClientPath']           = requestClientObj['requestClientPath']
    context['requestClientTitle']          = requestClientObj['requestClientTitle']
    context['requestClientBusiness']       = requestClientObj['requestClientBusiness']
    
    
    
    ##############
    #진행사항
    ##############
    queryProgressStatus = request.GET.get('progressStatus')
    queryRequestGte     = request.GET.get('requestGte')
    queryRequestLte     = request.GET.get('requestLte')
    
    requestObj = getProgressStatus(queryProgressStatus, queryRequestGte, queryRequestLte)
        
    context['requestObj']     = requestObj['requestObj']
    context['originProgress'] = requestObj['originProgress']
    context['progressStatus'] = requestObj['progressStatus']
    
    
    
    ###########
    #가견적
    ###########
    queryEstimateGte = request.GET.get('estimateGte')
    queryEstimateLte = request.GET.get('estimateLte')
    
    estimateList = getEstimate(queryEstimateGte, queryEstimateLte)

    context['estimateList'] = estimateList



    #############
    # 제품 대분류
    #############
    queryMaincategory    = request.GET.get('maincategory')
    queryMaincategoryGte = request.GET.get('maincategoryGte')
    queryMaincategoryLte = request.GET.get('maincategoryLte')
    
    maincategoryObj = getMaincategory(queryMaincategory, queryMaincategoryGte, queryMaincategoryLte)
    
    context['originMaincategory'] = maincategoryObj['originMaincategory']
    context['maincategoryList']   = maincategoryObj['maincategoryList']
    context['maincategoryLength'] = maincategoryObj['maincategoryLength']
    
    
    

    return render(request, 'chart_render.html', context)
    
    