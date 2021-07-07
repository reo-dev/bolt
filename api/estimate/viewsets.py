#-*- coding: cp949 -*-
import os, enum, uuid
from datetime import date

from rest_framework import (
    viewsets,
    status,
    mixins,
)

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

#pagenation
from .paginations import *
#django-filter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
#count
from django.db.models import Count

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import authenticate

from .serializers import *
from ..project.serializers import RequestSerializer
from apps.estimate.models import *
from apps.account.models import *
from apps.project.models import *
from apps.utils import *

from .stp2stl import *
from .get_stl_info import *

import trimesh
import numpy as np
import math
import shapely
from shapely import ops
from shapely.geometry import LineString, MultiLineString, Polygon
import csv
import time
from shapely.geometry import LineString, MultiLineString, Polygon, Point 



class UnknownDetailProcess (Exception):
    pass

class UnknownProcess (Exception):
    pass

class duplicatedEstimate (Exception):
    pass


def Projection(mesh):
    try:
        project_x = trimesh.path.polygons.projected(mesh, normal=[1,0,0])
    except:
        project_x = Polygon([(mesh.bounds[0][2], mesh.bounds[0][1]), (mesh.bounds[1][2], mesh.bounds[0][1]),
                           (mesh.bounds[1][2], mesh.bounds[1][1]), (mesh.bounds[0][2], mesh.bounds[1][1])])

    try:
        project_y = trimesh.path.polygons.projected(mesh, normal=[0,1,0])

    except:
        project_y = Polygon([(mesh.bounds[0][0], mesh.bounds[0][2]), (mesh.bounds[1][0], mesh.bounds[0][2]),
                           (mesh.bounds[1][0], mesh.bounds[1][2]), (mesh.bounds[0][0], mesh.bounds[1][2])])
        
    try:
        project_z = trimesh.path.polygons.projected(mesh, normal=[0,0,1])
    except:
        project_z = Polygon([(mesh.bounds[0][0], mesh.bounds[0][1]), (mesh.bounds[1][0], mesh.bounds[0][1]),
                           (mesh.bounds[1][0], mesh.bounds[1][1]), (mesh.bounds[0][0], mesh.bounds[1][1])])
 
    rectangle_x, area_x, rectangle_list_x, rectangle_rough_x = PlaneProcessing(project_x)
    rectangle_y, area_y, rectangle_list_y, rectangle_rough_y = PlaneProcessing(project_y)
    rectangle_z, area_z, rectangle_list_z, rectangle_rough_z = PlaneProcessing(project_z)
    
    rectangle_volume_max = max(rectangle_x*mesh.extents[0], max(rectangle_y*mesh.extents[1], rectangle_z*mesh.extents[2]))
    
    rectangle_processing_detail = 0
    
    
    if rectangle_volume_max == rectangle_x*mesh.extents[0]:
        plane_volume = area_x*mesh.extents[0]
        rectangle_rough = [mesh.extents[0] * x for x in rectangle_rough_x]
        rectangle_rough_volume = sum(rectangle_rough_x)*mesh.extents[0] 
         
    elif rectangle_volume_max == rectangle_y * mesh.extents[1]:
        plane_volume = area_y*mesh.extents[1]
        rectangle_rough =[mesh.extents[1] * x for x in rectangle_rough_y]
        rectangle_rough_volume  = sum(rectangle_rough_y)*mesh.extents[1] 
 
    else:
        plane_volume = area_z*mesh.extents[2]
        rectangle_rough = [mesh.extents[2] * x for x in rectangle_rough_z]
        rectangle_rough_volume  = sum(rectangle_rough_z)*mesh.extents[2] 
        
    rectangle_detail_volume = rectangle_volume_max - rectangle_rough_volume

    return rectangle_volume_max, plane_volume,rectangle_rough,rectangle_rough_volume, rectangle_detail_volume

def PlaneProcessing(project):
     # 황삭의 기준이 되는 최소 변의 길이
    side_len_1 = 200
    side_len_2 = 100
    side_len_3 = 50
    side_len_4 = 10
    side_len_5 = 5
    # 만약 황삭이라면 가공하는 데 사용될 엔드밀의 직경
    rad_1 = 20
    rad_2 = 15
    rad_3 = 10
    rad_4 = 5
    rad_5 = 5
    rectangle_list = [(project.bounds[0],  project.bounds[1]), (project.bounds[2], project.bounds[1]), 
                      (project.bounds[2], project.bounds[3]), (project.bounds[0], project.bounds[3])]
    project_bounding = Polygon(rectangle_list)
    point_0 = Point(project.bounds[0], project.bounds[1])
    point_1 = Point(project.bounds[2], project.bounds[1])
    point_2 = Point(project.bounds[2], project.bounds[3])
    point_3 = Point(project.bounds[0], project.bounds[3])
    point_list = [point_0, point_1, point_2, point_3]
    project_rectangle = 0
    project_plane = project_bounding - project
    project_plane_processing = 0
    project_plane_allprocessing = 0
    project_plane_processing_list = []
    project_plane_rectangle_list = []
    rectangle_1_in = 0
    rectangle_1_out = 0
    rectangle_2_in = 0
    rectangle_2_out = 0
    rectangle_3_in = 0
    rectangle_3_out = 0
    rectangle_4_in = 0
    rectangle_4_out = 0
    rectangle_5_in = 0
    rectangle_5_out = 0
    
    try:
        for p in project_plane:    # 끝점 상관없이
            project_plane_processing_list.append(p)
    except TypeError:
        try:
            project_plane_processing_list.append(project_plane)
        except:
            pass
    
    for p in project_plane_processing_list:
        vertex_list = []
        
        if not p:
            continue
        if math.floor(p.bounds[3] - p.bounds[1]) == 0 or math.floor(p.bounds[2] - p.bounds[0]) == 0:
            continue

        plane_list = [[1] * math.floor(p.bounds[3] - p.bounds[1]) for i in range(math.floor(p.bounds[2] - p.bounds[0]))]

        for i in range(math.floor(p.bounds[2] - p.bounds[0])):
            for j in range(math.floor(p.bounds[3] - p.bounds[1])):
                if p.exterior.contains(Point(p.bounds[0]+i, p.bounds[1]+j)) or p.contains(Point(p.bounds[0]+i, p.bounds[1]+j)):
                    plane_list[i][j] = 0
                    
        if p.exterior.contains(point_0) or p.contains(point_0):
            if plane_list[0][0] == 0:
                vertex_list.append([0, 0])
        if p.exterior.contains(point_1) or p.contains(point_1):
            if plane_list[0][len(plane_list[0])-1] == 0:
                vertex_list.append([0, len(plane_list[0])-1])
        if p.exterior.contains(point_2) or p.contains(point_2):
            if plane_list[len(plane_list)-1][len(plane_list[0])-1] == 0:
                vertex_list.append([len(plane_list)-1, len(plane_list[0])-1])
        if p.exterior.contains(point_3) or p.contains(point_3):
            if plane_list[len(plane_list)-1][0] == 0:
                vertex_list.append([len(plane_list)-1, 0])

        while 1:
            column, row = MaxRectangle(plane_list)
            size = (column - 1)*(row-1)
            project_rectangle += size
            project_plane_rectangle_list.append((column-1, row-1))
            a = min(column-1, row-1)
            
            check = True
            vertex_check = VertexCheck(plane_list, vertex_list)
            if a>=side_len_1:
                rectangle_1_in += size
            elif a>=rad_1 and vertex_check:
                rectangle_1_out += size
            elif a>=side_len_2:
                rectangle_2_in += size
            elif a>=rad_2 and vertex_check:
                rectangle_2_out += size
            elif a>=side_len_3:
                rectangle_3_in += size
            elif a>=rad_3 and vertex_check:
                rectangle_3_out += size
            elif a>=side_len_4:
                rectangle_4_in += size
            elif a>=rad_4 and vertex_check:
                rectangle_4_out += size
            elif a>=side_len_5:
                rectangle_5_in += size
            elif a>=rad_5 and vertex_check:
                rectangle_5_out += size
            else:
                check = False
                
            if check == False:
                break
                
    rough_rectangle_sum = [rectangle_1_in, rectangle_1_out, rectangle_2_in, rectangle_2_out, rectangle_3_in, 
                           rectangle_3_out, rectangle_4_in, rectangle_4_out,rectangle_5_in, rectangle_5_out]
    project_plane_allprocessing = project_bounding.area - project.area
    
    return project_rectangle, project_plane_allprocessing, project_plane_rectangle_list, rough_rectangle_sum



def VertexCheck(plane_list, vertex_list):
    if vertex_list:
        for vertex in vertex_list:
            if plane_list[vertex[0]][vertex[1]] == 1:
                return True
    return False



def MaxRectangle(twod):
    outer = False
    check = [[0] * len(twod[0]) for i in range(len(twod))]  

    
    minx, miny, maxx, maxy = 0, 0, len(twod)-1, len(twod[0])-1
    pointx, pointy = minx, miny              
    column, row, ans = 1, 1, 1
    
    x, y = minx, miny     
    anslst = []                  

    for a in range(len(twod)):
        if column*row > len(twod[0])*(len(twod)-a):
            break

        stack = []    

        for b in range(len(twod[0])):
            if twod[x + a][y + b] == 1:     
                while stack:                                        
                    if ans < stack[-1][1] * (y + b - stack[-1][0]):    
                        ans = stack[-1][1] * (y + b - stack[-1][0])    
                        column = stack[-1][1]                           
                        row = y + b - stack[-1][0]                      
                        pointx = x + a                                 
                        pointy = stack[-1][0]                          
                    stack.pop()                                        
                continue                                               

            tempx = x + a                                        
            while twod[tempx][y + b] == 0:
                tempx += 1
                if tempx == len(twod):  
                    break
            height = tempx - x - a

            if not stack:                                           
                stack.append((y + b, height))
                continue

            if stack[-1][1] > height:                                  
                while stack[-1][1] > height:                            
                    if ans < stack[-1][1] * (y + b - stack[-1][0]):    
                        ans = stack[-1][1] * (y + b - stack[-1][0])     
                        column = stack[-1][1]                          
                        row = y + b - stack[-1][0]                      
                        pointx = x + a                                  
                        pointy = stack[-1][0]                           
                    storey = stack[-1][0]                              
                    stack.pop()                                       
                    if not stack:                                    
                        break
            elif stack[-1][1] == height:                
                continue                       
            else:                                    
                storey = y + b                        

            stack.append((storey, height))               

        while stack:                                                        
            if ans < stack[-1][1] * (y + maxy - miny + 1 - stack[-1][0]):   
                ans = stack[-1][1] * (y + maxy - miny + 1 - stack[-1][0])   
                column = stack[-1][1]                                       
                row = y + maxy - miny + 1 - stack[-1][0]               
                pointx = x + a                                              
                pointy = stack[-1][0]                                      
            stack.pop()                                                  
        continue

        
    for i in range(len(twod)):
        for j in range(len(twod[0])): 
                if i >= pointx and j>= pointy and i<=column+pointx-1 and j<=row+pointy-1:
                    twod[i][j] = 1
    try:
        return column, row
    except Exception as e:
        return 0, 0



def calculatePriceFormModelInfo (processId, detailProcessId, model_info):
    # 자동 견적 알고리즘
    print('결과 파헤치기',processId, detailProcessId, model_info)
    processCache = manufactureProcess.objects.get(id = processId) #공정 방법 instance 받아옴
    detailProcessCache =  detailManufactureProcess.objects.get(id = detailProcessId, process = processId) #세부 공정 방법 instance
    print('왜?',detailProcessCache)
    materialCache = material.objects.filter(detailProcess = detailProcessId)
    #print(materialCache)
    # 찾은 인스턴스들 python에서 사용가능한 형태로 변환
    processData = ManufactureProcessSerializer(processCache).data
    detailProcessData = DetailManufactureProcessSerializer(detailProcessCache).data
    

    for i in materialCache:
        materialData = MaterialSerializer(i).data 
        if processData['name'] == '금형사출':
            if detailProcessData['name'] == '플라스틱': 
                s_p = 2
                loss = 3
                cavy = 2
                # 플라스틱 개당 가격 3.6원/1g
                material_price = materialData['price']
                # 기계 임률 
                machine_price = 70000 

                # 각 변의 길이가 mm 기준이므로 weight는 1000을 나눠줘야 함.
                weight = model_info['volume']/1000

                # 포장비 개당 10원
                packaging_price = 10
                
                # 개당 사출 재료 가격
                model_price = (weight + s_p + loss) * material_price
                
                #cube_volume = model_info['x_length']*model_info['y_length']*model_info['z_length']

                volume_list = [model_info['x_length'], model_info['y_length'], model_info['z_length']]
                
                # 플라스틱 금형가의 경우 장축 길이에 m^2 당 300 만원
                Long_side = max(volume_list)

                # 후가공 비용
                min_post_processing_price = detailProcessData['minPostProcessing']
                max_post_processing_price = detailProcessData['maxPostProcessing']
                
                # 플라스틱의 경우 SHOT가 72 - 100SHOT/H
                min_shoot = detailProcessData['minShoot']
                max_shoot = detailProcessData['maxShoot']
                
                # 나오는 총량은 Cavity * shot 숫자
                min_manufacture_quantity = cavy * min_shoot
                max_manufacture_quantity = cavy * max_shoot
                
                # 기계 임률에 따른 사출 가격
                min_enjaculation_price = machine_price / max_manufacture_quantity
                max_enjaculation_price = machine_price / min_manufacture_quantity

                # 총 사출 가격 = 사출 재료 가격 + 기계 임률 가격 + 포장 가격 + 후가공 가격 
                min_total_price = model_price + min_enjaculation_price + min_post_processing_price + packaging_price
                max_total_price = model_price + max_enjaculation_price + max_post_processing_price + packaging_price
                
                # 금형가 m^2 당 200 - 600만원 + 기본가 800,000원
                mold_min_price = Long_side/100 * 2000000 + 800000 
                mold_max_price = Long_side/100 * 6000000 + 800000

                # 볼트앤너트 수수료 15%  
                min_bolt_nut_commission = mold_min_price*1.15
                max_bolt_nut_commission = mold_max_price*1.15
                
                
                return (
                    {
                        # 사출 가격
                        'minPrice': min_total_price,
                        'maxPrice': max_total_price,
                        # 금형 가격
                        'totalMinPrice': min_bolt_nut_commission,
                        'totalMaxPrice': max_bolt_nut_commission,
                        'materialId': materialData['id']
                    }
                )
            elif detailProcessData['name'] == '실리콘':
                cavy = 2
                material_price = materialData['price'] 

                # 무게 : 각 변의 길이가 mm 기준이므로 1000을 나눔
                weight =  model_info['volume'] / 1000
                
                # 실리콘의 경우 60 - 100 shot 사이
                min_shoot = detailProcessData['minShoot']
                max_shoot = detailProcessData['maxShoot']

                # 하루에 나오는 총량을 shot * cavity 숫자
                min_manufacture_quantity = cavy * min_shoot
                max_manufacture_quantity = cavy * max_shoot

                # 기계 임률
                machine_price_per_day = 250000
                
                #cube_volume = model_info['x_length'] * model_info['y_length'] * model_info['z_length']
                
                # 사출 가격
                min_enjaculation_price = (machine_price_per_day / max_manufacture_quantity) + (material_price * weight)
                max_enjaculation_price = (machine_price_per_day / min_manufacture_quantity) + (material_price * weight)
                
                volume_list = [model_info['x_length'], model_info['y_length'], model_info['z_length']]
                
                # 실리콘 금형가의 경우 장축 길이에 10cm 당 100만원
                Long_side = max(volume_list)
                
                # 금형가 m^2 당 100 - 150만원 + 기본가 400,000원
                mold_min_price = Long_side/100 * 1000000 + 400000 
                mold_max_price = Long_side/100 * 1500000 + 400000  
                
                # 볼트앤너트 수수료 15%
                min_bolt_nut_commission = mold_min_price * 1.15
                max_bolt_nut_commission = mold_max_price * 1.15
                
                return (
                    {
                        # 사출 가격
                        'minPrice': min_enjaculation_price,
                        'maxPrice': max_enjaculation_price,
                        # 금형 가격
                        'totalMinPrice': min_bolt_nut_commission,
                        'totalMaxPrice': max_bolt_nut_commission,
                        'materialId': materialData['id']
                    }
                )
            else:
                raise UnknownDetailProcess('지원하지 않는 세부 제작 공정 입니다.')
        elif processData['name'] == '3D 프린팅':

            # 무게 : 각 변의 길이가 mm 기준이므로 1000을 나눔
            weight =  model_info['volume'] / 1000
            
            # 정육면체 부피 : 가로 x 세로 x 높이
            cube_volume = model_info['x_length'] * model_info['y_length'] * model_info['z_length']
            # 바닥면에 서포터가 깔리므로 사용하는 용량은 cube_volume과 실제 부피의 절반 정도로 유추할 수 있다. 
            real_volume = (cube_volume + model_info['volume'])/2
            # 3d 프린터의 경우 시간당 2000원 - 10cm * 10cm * 10cm 부피의 출력 시 저품질은 13 시간 15분(795분), 고품질은 35시간 18분(2118분) 걸린다.
            machine_price_per_hour = 2000
            
            # 걸리는 시간 : 100(mm) * 100(mm) * 100 (mm) = 1,000,000mm^3이 795분 ~ 2118분 걸리므로 절반값 산정 real_volume(mm^3) / 1,000,000mm^3 
            minute = (real_volume / 1000000) * 1456
            
            # 가격 : 분수 / 60 * 시간당 가격
            price = (minute/60) * machine_price_per_hour + 4000
            
            
            #장축 구하기
            volume_list = [model_info['x_length'], model_info['y_length'], model_info['z_length']]
            max_length = max(volume_list)
            # 장축이 18cm를 넘으면 기계가 바뀌므로 가격 x 2
            if(max_length > 180):
                price = price * 2


            return (
                {
                    # 생산 가격 : 3d 프린터는 금형가격이 없음

                    # 기본 품질 - 단일 가격
                    'minPrice': price,
                    'materialId': materialData['id'],
                    'maxPrice': price,
                    'totalMinPrice': price,
                    'totalMaxPrice': price

                }
            )

        elif processData['name'] == '절삭가공':
            
            # 단축 구하기
            volume_list = [model_info['x_length'], model_info['y_length'], model_info['z_length']]
            min_length = min(volume_list)
            # 장축 구하기
            max_length = max(volume_list)

            # 진짜 볼륨    
            real_volume = model_info['x_length']*model_info['y_length']*model_info['z_length']
            # 장축 넓이 / cm 단위므로 100을 나눠야함.
            model_square = (real_volume/min_length)/1000     
            
            if max_length < 50:
                # 가격 = Square(장축넓이/cm^2)/2 * 10000원 + 50,000(기본료)
                model_price = model_square*10000 + 50000
            
            # 크기가 커지면 작업할 공간이 많아지는 경우가 많음.
            elif max_length < 100:
                model_price = model_square*15000 + 70000
            
            # 크기가 커지면 작업할 공간이 많아지는 경우가 많음.
            elif max_length < 150:
                model_price = model_square*17500 + 90000

            # 크기가 커지면 작업할 공간이 많아지는 경우가 많음.
            elif max_length < 400:
                model_price = model_square*20000 + 120000

            # 40cm가 넘어가면 기계가 달라짐
            elif max_length > 400:
                model_price = model_square*40000 + 150000      

            return (
                {
                    # 생산 가격 : CNC는 금형가격이 없   
                    #기본 품질 - 단일 가격
                    'minPrice': model_price,
                    'maxPrice': model_price,
                    'totalMinPrice': model_price,
                    'totalMaxPrice': model_price,
                    'materialId': materialData['id']
                }
            )
        else:
            raise UnknownProcess('지원하지 않는 제작 공정 입니다.')

            


class ResponseCode(enum.Enum):
    SUCCESS = 0
    FAIL = 1

class EstimateViewSet(viewsets.ModelViewSet):
    serializer_class = EstimateSerializer
    queryset = Estimate.objects.all()
    
    def create(self, request, *args, **kwargs):
        # get stp_file
        blueprintFile = request.FILES.get('blueprint','') #도면 파일
        fileType = str(blueprintFile).split('.')[-1] #도면 파일에서 파일 확장자 slicing
        processId = request.data.get('process') #공정 id값
        detailProcessId = request.data.get('detailprocess')# 세부 공정 id 값
        print(detailProcessId,args[3])
        number = request.data.get('number') # 개수
        if args:
            print('args 존재')
            requestId = args[0] #request instance
            blueprintFile = args[1]
            processId = args[2] #공정 id값
            detailProcessId = args[3]# 세부 공정 id 값
            number = args[4] # 수량 값
        else:
            print('args 존재하지 않음')
            requestId = 2105
        stlCache = None

        try:
            requestCache = Request.objects.get(id = requestId) #의뢰서 있는지 확인, 의뢰서가 없는 경우 execption 발생
            
            #proposalId = requestCache.proposal.id
            # estimateCache = Estimate.objects.filter(request_id = requestId) #해당 의뢰서에 가견적이 이미 존재하는지 확인
            
            # if estimateCache: #해당 의뢰서에 가견적이 존재 하는 경우 execption 발생
            #     raise duplicatedEstimate
                

        except Request.DoesNotExist: 
            return Response(
                data = {
                    'message': "의뢰서가 존재하지 않습니다."    
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        except duplicatedEstimate:
            return Response(
                        data = {
                            'message': "이미 해당 의뢰에 견적이 존재합니다."    
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )

        # serializer로 python에서 사용하는 datatype으로 변환
        requestData = RequestSerializer(requestCache).data
        #print(requestData)
        if fileType != 'stl' and fileType != 'stp':
            return Response(
                data = {
                    'message': "도면은 stl과 stp 파일만 첨부 가능합니다."    
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        # 동시에 들어와 이름이 겹치는 것을 방지하여 uuid를 사용하여 랜덤으로 이름 지정
        fileName =  uuid.uuid4().hex

        try:
            if fileType == 'stp':
                # 원본파일에 대한 내용을 읽음
                stpFileCache = str(blueprintFile.read())
                # 불필요한 부분 제거
                stpArr = stpFileCache[2:-1].split('\\r\\n')
                # stp파일은 ISO 10303-21형식을 따라서 바이너리로 작성할  필요 없음
                f = open('api/estimate/' + fileName + '.stp', mode = 'wt', encoding = 'utf-8')
                for i in stpArr:
                    f.write(i+'\n')
                f.close()

                # 임시로 저장한 stp파일을 stl로 변환하여 임시로 저장
                # TODO: 일부 stp파일 처리중 예외처리 없이 서버가 멈추는 문제 발생, BRepMesh_IncrementalMesh 부분 확인
                stp2stl(fileName)
            else:
                # stl파일에 대한 정보를 받아오기 위해 바이너리 모드로 파일을 연다.
                stlCache = open('api/estimate/'+fileName + '.stl', mode = 'wb')
                stlCache.write(blueprintFile.read())
                stlCache.close()
            
        except Exception as e: #알 수 없는 오류 발생시 예외처리
            return Response(
                data = {'message': '도면 파일을 읽던 중 오류가 발생하였습니다.'},
                status = status.HTTP_400_BAD_REQUEST
            )
            


            

        stlCache = open('api/estimate/' + fileName + '.stl', 'rb') #stl 파일 또는 stp를 stl로 변환한 파일 열기
        # CNC 절삭 가공 알고리즘 시작 #
        if processId=="3":
            # 황삭의 기준이 되는 최소 변의 길이
            side_len_1 = 200
            side_len_2 = 100
            side_len_3 = 50
            side_len_4 = 10
            side_len_5 = 5
            # 만약 황삭이라면 가공하는 데 사용될 엔드밀의 직경
            rad_1 = 20
            rad_2 = 15
            rad_3 = 10
            rad_4 = 5
            rad_5 = 5
            start = time.time()
            print(stlCache.name)
            mesh = trimesh.load_mesh(stlCache.name)
            rectangle_volume,area_volume,rectangle_rough_volume,rectangle_rough_volume_sum, rectangle_detail_volume = Projection(mesh)    
            plane_detail = area_volume - rectangle_volume
            rectangle_detail = rectangle_volume - rectangle_rough_volume_sum
            total_len = mesh.bounding_box.volume -  mesh.volume 
            remain_len = total_len - area_volume
            ans = (rectangle_rough_volume[0]+rectangle_rough_volume[1])/20+(rectangle_rough_volume[2]+rectangle_rough_volume[3])/15+(rectangle_rough_volume[4]+rectangle_rough_volume[5])/10+(rectangle_rough_volume[6]+rectangle_rough_volume[7])/5+(rectangle_rough_volume[8]+rectangle_rough_volume[9])/5++rectangle_detail/5+plane_detail/2+remain_len/2
            ans = 2*ans + 36024
            ans = round(ans, -3)
            print(ans)
            print('걸린 시간:', int((time.time() - start) / 60), '분', int((time.time() - start) % 60), '초')
            results = ans
            

            




        # s3에 저장하기 위한 경로 설정
        now = datetime.datetime.now()
        stlSavePath = 'stl/' + str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '/'       

        try:    
            print('지뢰1')
            #도면 정보 받아옴
            model_info = get_stl_info(fileName)
            #도면에서 가견적 계산
            result = calculatePriceFormModelInfo(processId, detailProcessId, model_info)
            print('지뢰1의 결과',result)
        except manufactureProcess.DoesNotExist: #공정 방법이 존재하지 않는경우
            print('지뢰2')
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 
            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')
            return Response(
                data = { 'message': '올바른 제조 공정이 아닙니다.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except detailManufactureProcess.DoesNotExist: #세부 공정이 존재하지 않는 경우
            print('지뢰3')
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 
            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')                       
            return Response(
                data={ 'message': '올바른 세부 제조 공정이 아닙니다.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except material.DoesNotExist:
            print('지뢰4')
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 
            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')          
            return Response(
                data = {'message': '올바른 재료가 아닙니다.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except UnknownDetailProcess: #지원되지 않는 세부 공정 요청시 발생, 2021년 2월 9일 기준 금형사출 (플라스틱, 실리콘)만 가능
            print('지뢰5')
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 
            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')           
            return Response(
                data = {'message': '현재 지원되지 않는 제조 공정입니다.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except UnknownProcess: #지원되지 않는 세부 공정 요청시 발생, 2021년 2월 9일 기준 금형사출 (플라스틱, 실리콘)만 가능
            print('지뢰6')
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 
            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')            
            return Response(
                data = {'message': '현재 지원되지 않는 제조 공정입니다.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except Exception as e: #알 수 없는 오류 발생시 예외처리
            print('지뢰7',e)
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 

            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')            
            return Response(
                data = {'message': '파일을 정보를 읽는 중 문제가 발생하였습니다.\n' + str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )

        if processId=="3":
            result['minPrice'] = results * 0.5
            result['maxPrice'] = results * 1.5
        print('estimate 저장',requestCache)
        estimate = Estimate.objects.create( # 계산한 정보로 가견적 db에 insert
            stp_file = blueprintFile if fileType == 'stp' else None,
            stl_file = default_storage.save(stlSavePath + fileName + '_stl.stl', stlCache),
            volume = model_info['volume'],
            x_length = model_info['x_length'],
            y_length = model_info['y_length'],
            z_length = model_info['z_length'],
            process = str(processId),
            category = str(detailProcessId),
            material = result['materialId'],
            minPrice = result['minPrice'],
            maxPrice = result['maxPrice'],
            totalMinPrice = result['totalMinPrice'],
            totalMaxPrice = result['totalMaxPrice'],
            number = number,
            request = requestCache
        )
        print('저장한 estimate 정보',estimate)
        
        # 임시로 저장한 파일 삭제
        stlCache.close()
        fileName_=fileName+'.stl'
        loc = 'api/estimate/'
        path = os.path.join(loc,fileName_)
        os.remove(path)
        if fileType == 'stp':
            os.remove('api/estimate/' + fileName + '.stp')


        # 결과 return
        return Response(
            data={ 
                'data': EstimateSerializer(estimate).data,
                #'proposalId': proposalId,
                'message': "도면입력"
            },
            status = status.HTTP_201_CREATED,
        )


class ManufactureProcessViewSet (viewsets.ModelViewSet):
    serializer_class = ManufactureProcessSerializer
    queryset = manufactureProcess.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['id']
    def list (self, request, *args, **kwargs):
        processCache = manufactureProcess.objects.all()
        detailProcessCache = []
        result = []

        # 공정에 list로 세부공정 내용 넣어서 보내줌
        for process in processCache:
            #해당 공정에 맞는 세부 공정들 받아와서 serializer로 처리, id 와 name만 가져옴
            detailProcess = detailManufactureProcess.objects.filter(process_id = process.id)
            detailProcessCache = DetailManufactureProcessSerializer_ID_Name_Process(detailProcess, many = True).data
            
            #공정에 세부공정 list로 추가해주고, 공정도 전체 결과 list에 추가해줌
            processData = ManufactureProcessSerializer(process).data
            processData['detailManufactureProcess'] = detailProcessCache 
            result.append(processData)

        return Response(    
            data = {
                'count': len(processData),
                'data': result
            }
        )
