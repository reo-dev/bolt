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
     # Ȳ���� ������ �Ǵ� �ּ� ���� ����
    side_len_1 = 200
    side_len_2 = 100
    side_len_3 = 50
    side_len_4 = 10
    side_len_5 = 5
    # ���� Ȳ���̶�� �����ϴ� �� ���� ������� ����
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
        for p in project_plane:    # ���� �������
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
    # �ڵ� ���� �˰���
    print('��� ����ġ��',processId, detailProcessId, model_info)
    processCache = manufactureProcess.objects.get(id = processId) #���� ��� instance �޾ƿ�
    detailProcessCache =  detailManufactureProcess.objects.get(id = detailProcessId, process = processId) #���� ���� ��� instance
    print('��?',detailProcessCache)
    materialCache = material.objects.filter(detailProcess = detailProcessId)
    #print(materialCache)
    # ã�� �ν��Ͻ��� python���� ��밡���� ���·� ��ȯ
    processData = ManufactureProcessSerializer(processCache).data
    detailProcessData = DetailManufactureProcessSerializer(detailProcessCache).data
    

    for i in materialCache:
        materialData = MaterialSerializer(i).data 
        if processData['name'] == '��������':
            if detailProcessData['name'] == '�ö�ƽ': 
                s_p = 2
                loss = 3
                cavy = 2
                # �ö�ƽ ���� ���� 3.6��/1g
                material_price = materialData['price']
                # ��� �ӷ� 
                machine_price = 70000 

                # �� ���� ���̰� mm �����̹Ƿ� weight�� 1000�� ������� ��.
                weight = model_info['volume']/1000

                # ����� ���� 10��
                packaging_price = 10
                
                # ���� ���� ��� ����
                model_price = (weight + s_p + loss) * material_price
                
                #cube_volume = model_info['x_length']*model_info['y_length']*model_info['z_length']

                volume_list = [model_info['x_length'], model_info['y_length'], model_info['z_length']]
                
                # �ö�ƽ �������� ��� ���� ���̿� m^2 �� 300 ����
                Long_side = max(volume_list)

                # �İ��� ���
                min_post_processing_price = detailProcessData['minPostProcessing']
                max_post_processing_price = detailProcessData['maxPostProcessing']
                
                # �ö�ƽ�� ��� SHOT�� 72 - 100SHOT/H
                min_shoot = detailProcessData['minShoot']
                max_shoot = detailProcessData['maxShoot']
                
                # ������ �ѷ��� Cavity * shot ����
                min_manufacture_quantity = cavy * min_shoot
                max_manufacture_quantity = cavy * max_shoot
                
                # ��� �ӷ��� ���� ���� ����
                min_enjaculation_price = machine_price / max_manufacture_quantity
                max_enjaculation_price = machine_price / min_manufacture_quantity

                # �� ���� ���� = ���� ��� ���� + ��� �ӷ� ���� + ���� ���� + �İ��� ���� 
                min_total_price = model_price + min_enjaculation_price + min_post_processing_price + packaging_price
                max_total_price = model_price + max_enjaculation_price + max_post_processing_price + packaging_price
                
                # ������ m^2 �� 200 - 600���� + �⺻�� 800,000��
                mold_min_price = Long_side/100 * 2000000 + 800000 
                mold_max_price = Long_side/100 * 6000000 + 800000

                # ��Ʈ�س�Ʈ ������ 15%  
                min_bolt_nut_commission = mold_min_price*1.15
                max_bolt_nut_commission = mold_max_price*1.15
                
                
                return (
                    {
                        # ���� ����
                        'minPrice': min_total_price,
                        'maxPrice': max_total_price,
                        # ���� ����
                        'totalMinPrice': min_bolt_nut_commission,
                        'totalMaxPrice': max_bolt_nut_commission,
                        'materialId': materialData['id']
                    }
                )
            elif detailProcessData['name'] == '�Ǹ���':
                cavy = 2
                material_price = materialData['price'] 

                # ���� : �� ���� ���̰� mm �����̹Ƿ� 1000�� ����
                weight =  model_info['volume'] / 1000
                
                # �Ǹ����� ��� 60 - 100 shot ����
                min_shoot = detailProcessData['minShoot']
                max_shoot = detailProcessData['maxShoot']

                # �Ϸ翡 ������ �ѷ��� shot * cavity ����
                min_manufacture_quantity = cavy * min_shoot
                max_manufacture_quantity = cavy * max_shoot

                # ��� �ӷ�
                machine_price_per_day = 250000
                
                #cube_volume = model_info['x_length'] * model_info['y_length'] * model_info['z_length']
                
                # ���� ����
                min_enjaculation_price = (machine_price_per_day / max_manufacture_quantity) + (material_price * weight)
                max_enjaculation_price = (machine_price_per_day / min_manufacture_quantity) + (material_price * weight)
                
                volume_list = [model_info['x_length'], model_info['y_length'], model_info['z_length']]
                
                # �Ǹ��� �������� ��� ���� ���̿� 10cm �� 100����
                Long_side = max(volume_list)
                
                # ������ m^2 �� 100 - 150���� + �⺻�� 400,000��
                mold_min_price = Long_side/100 * 1000000 + 400000 
                mold_max_price = Long_side/100 * 1500000 + 400000  
                
                # ��Ʈ�س�Ʈ ������ 15%
                min_bolt_nut_commission = mold_min_price * 1.15
                max_bolt_nut_commission = mold_max_price * 1.15
                
                return (
                    {
                        # ���� ����
                        'minPrice': min_enjaculation_price,
                        'maxPrice': max_enjaculation_price,
                        # ���� ����
                        'totalMinPrice': min_bolt_nut_commission,
                        'totalMaxPrice': max_bolt_nut_commission,
                        'materialId': materialData['id']
                    }
                )
            else:
                raise UnknownDetailProcess('�������� �ʴ� ���� ���� ���� �Դϴ�.')
        elif processData['name'] == '3D ������':

            # ���� : �� ���� ���̰� mm �����̹Ƿ� 1000�� ����
            weight =  model_info['volume'] / 1000
            
            # ������ü ���� : ���� x ���� x ����
            cube_volume = model_info['x_length'] * model_info['y_length'] * model_info['z_length']
            # �ٴڸ鿡 �����Ͱ� �򸮹Ƿ� ����ϴ� �뷮�� cube_volume�� ���� ������ ���� ������ ������ �� �ִ�. 
            real_volume = (cube_volume + model_info['volume'])/2
            # 3d �������� ��� �ð��� 2000�� - 10cm * 10cm * 10cm ������ ��� �� ��ǰ���� 13 �ð� 15��(795��), ��ǰ���� 35�ð� 18��(2118��) �ɸ���.
            machine_price_per_hour = 2000
            
            # �ɸ��� �ð� : 100(mm) * 100(mm) * 100 (mm) = 1,000,000mm^3�� 795�� ~ 2118�� �ɸ��Ƿ� ���ݰ� ���� real_volume(mm^3) / 1,000,000mm^3 
            minute = (real_volume / 1000000) * 1456
            
            # ���� : �м� / 60 * �ð��� ����
            price = (minute/60) * machine_price_per_hour + 4000
            
            
            #���� ���ϱ�
            volume_list = [model_info['x_length'], model_info['y_length'], model_info['z_length']]
            max_length = max(volume_list)
            # ������ 18cm�� ������ ��谡 �ٲ�Ƿ� ���� x 2
            if(max_length > 180):
                price = price * 2


            return (
                {
                    # ���� ���� : 3d �����ʹ� ���������� ����

                    # �⺻ ǰ�� - ���� ����
                    'minPrice': price,
                    'materialId': materialData['id'],
                    'maxPrice': price,
                    'totalMinPrice': price,
                    'totalMaxPrice': price

                }
            )

        elif processData['name'] == '���谡��':
            
            # ���� ���ϱ�
            volume_list = [model_info['x_length'], model_info['y_length'], model_info['z_length']]
            min_length = min(volume_list)
            # ���� ���ϱ�
            max_length = max(volume_list)

            # ��¥ ����    
            real_volume = model_info['x_length']*model_info['y_length']*model_info['z_length']
            # ���� ���� / cm �����Ƿ� 100�� ��������.
            model_square = (real_volume/min_length)/1000     
            
            if max_length < 50:
                # ���� = Square(�������/cm^2)/2 * 10000�� + 50,000(�⺻��)
                model_price = model_square*10000 + 50000
            
            # ũ�Ⱑ Ŀ���� �۾��� ������ �������� ��찡 ����.
            elif max_length < 100:
                model_price = model_square*15000 + 70000
            
            # ũ�Ⱑ Ŀ���� �۾��� ������ �������� ��찡 ����.
            elif max_length < 150:
                model_price = model_square*17500 + 90000

            # ũ�Ⱑ Ŀ���� �۾��� ������ �������� ��찡 ����.
            elif max_length < 400:
                model_price = model_square*20000 + 120000

            # 40cm�� �Ѿ�� ��谡 �޶���
            elif max_length > 400:
                model_price = model_square*40000 + 150000      

            return (
                {
                    # ���� ���� : CNC�� ���������� ��   
                    #�⺻ ǰ�� - ���� ����
                    'minPrice': model_price,
                    'maxPrice': model_price,
                    'totalMinPrice': model_price,
                    'totalMaxPrice': model_price,
                    'materialId': materialData['id']
                }
            )
        else:
            raise UnknownProcess('�������� �ʴ� ���� ���� �Դϴ�.')

            


class ResponseCode(enum.Enum):
    SUCCESS = 0
    FAIL = 1

class EstimateViewSet(viewsets.ModelViewSet):
    serializer_class = EstimateSerializer
    queryset = Estimate.objects.all()
    
    def create(self, request, *args, **kwargs):
        # get stp_file
        blueprintFile = request.FILES.get('blueprint','') #���� ����
        fileType = str(blueprintFile).split('.')[-1] #���� ���Ͽ��� ���� Ȯ���� slicing
        processId = request.data.get('process') #���� id��
        detailProcessId = request.data.get('detailprocess')# ���� ���� id ��
        print(detailProcessId,args[3])
        number = request.data.get('number') # ����
        if args:
            print('args ����')
            requestId = args[0] #request instance
            blueprintFile = args[1]
            processId = args[2] #���� id��
            detailProcessId = args[3]# ���� ���� id ��
            number = args[4] # ���� ��
        else:
            print('args �������� ����')
            requestId = 2105
        stlCache = None

        try:
            requestCache = Request.objects.get(id = requestId) #�Ƿڼ� �ִ��� Ȯ��, �Ƿڼ��� ���� ��� execption �߻�
            
            #proposalId = requestCache.proposal.id
            # estimateCache = Estimate.objects.filter(request_id = requestId) #�ش� �Ƿڼ��� �������� �̹� �����ϴ��� Ȯ��
            
            # if estimateCache: #�ش� �Ƿڼ��� �������� ���� �ϴ� ��� execption �߻�
            #     raise duplicatedEstimate
                

        except Request.DoesNotExist: 
            return Response(
                data = {
                    'message': "�Ƿڼ��� �������� �ʽ��ϴ�."    
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        except duplicatedEstimate:
            return Response(
                        data = {
                            'message': "�̹� �ش� �Ƿڿ� ������ �����մϴ�."    
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )

        # serializer�� python���� ����ϴ� datatype���� ��ȯ
        requestData = RequestSerializer(requestCache).data
        #print(requestData)
        if fileType != 'stl' and fileType != 'stp':
            return Response(
                data = {
                    'message': "������ stl�� stp ���ϸ� ÷�� �����մϴ�."    
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        # ���ÿ� ���� �̸��� ��ġ�� ���� �����Ͽ� uuid�� ����Ͽ� �������� �̸� ����
        fileName =  uuid.uuid4().hex

        try:
            if fileType == 'stp':
                # �������Ͽ� ���� ������ ����
                stpFileCache = str(blueprintFile.read())
                # ���ʿ��� �κ� ����
                stpArr = stpFileCache[2:-1].split('\\r\\n')
                # stp������ ISO 10303-21������ ���� ���̳ʸ��� �ۼ���  �ʿ� ����
                f = open('api/estimate/' + fileName + '.stp', mode = 'wt', encoding = 'utf-8')
                for i in stpArr:
                    f.write(i+'\n')
                f.close()

                # �ӽ÷� ������ stp������ stl�� ��ȯ�Ͽ� �ӽ÷� ����
                # TODO: �Ϻ� stp���� ó���� ����ó�� ���� ������ ���ߴ� ���� �߻�, BRepMesh_IncrementalMesh �κ� Ȯ��
                stp2stl(fileName)
            else:
                # stl���Ͽ� ���� ������ �޾ƿ��� ���� ���̳ʸ� ���� ������ ����.
                stlCache = open('api/estimate/'+fileName + '.stl', mode = 'wb')
                stlCache.write(blueprintFile.read())
                stlCache.close()
            
        except Exception as e: #�� �� ���� ���� �߻��� ����ó��
            return Response(
                data = {'message': '���� ������ �д� �� ������ �߻��Ͽ����ϴ�.'},
                status = status.HTTP_400_BAD_REQUEST
            )
            


            

        stlCache = open('api/estimate/' + fileName + '.stl', 'rb') #stl ���� �Ǵ� stp�� stl�� ��ȯ�� ���� ����
        # CNC ���� ���� �˰��� ���� #
        if processId=="3":
            # Ȳ���� ������ �Ǵ� �ּ� ���� ����
            side_len_1 = 200
            side_len_2 = 100
            side_len_3 = 50
            side_len_4 = 10
            side_len_5 = 5
            # ���� Ȳ���̶�� �����ϴ� �� ���� ������� ����
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
            print('�ɸ� �ð�:', int((time.time() - start) / 60), '��', int((time.time() - start) % 60), '��')
            results = ans
            

            




        # s3�� �����ϱ� ���� ��� ����
        now = datetime.datetime.now()
        stlSavePath = 'stl/' + str(now.year) + '/' + str(now.month) + '/' + str(now.day) + '/'       

        try:    
            print('����1')
            #���� ���� �޾ƿ�
            model_info = get_stl_info(fileName)
            #���鿡�� ������ ���
            result = calculatePriceFormModelInfo(processId, detailProcessId, model_info)
            print('����1�� ���',result)
        except manufactureProcess.DoesNotExist: #���� ����� �������� �ʴ°��
            print('����2')
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 
            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')
            return Response(
                data = { 'message': '�ùٸ� ���� ������ �ƴմϴ�.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except detailManufactureProcess.DoesNotExist: #���� ������ �������� �ʴ� ���
            print('����3')
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 
            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')                       
            return Response(
                data={ 'message': '�ùٸ� ���� ���� ������ �ƴմϴ�.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except material.DoesNotExist:
            print('����4')
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 
            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')          
            return Response(
                data = {'message': '�ùٸ� ��ᰡ �ƴմϴ�.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except UnknownDetailProcess: #�������� �ʴ� ���� ���� ��û�� �߻�, 2021�� 2�� 9�� ���� �������� (�ö�ƽ, �Ǹ���)�� ����
            print('����5')
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 
            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')           
            return Response(
                data = {'message': '���� �������� �ʴ� ���� �����Դϴ�.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except UnknownProcess: #�������� �ʴ� ���� ���� ��û�� �߻�, 2021�� 2�� 9�� ���� �������� (�ö�ƽ, �Ǹ���)�� ����
            print('����6')
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 
            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')            
            return Response(
                data = {'message': '���� �������� �ʴ� ���� �����Դϴ�.'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except Exception as e: #�� �� ���� ���� �߻��� ����ó��
            print('����7',e)
            stlCache.close()
            os.remove('api/estimate/' + fileName + '.stl') 

            if fileType == 'stp':
                os.remove('api/estimate/' + fileName + '.stp')            
            return Response(
                data = {'message': '������ ������ �д� �� ������ �߻��Ͽ����ϴ�.\n' + str(e)},
                status = status.HTTP_400_BAD_REQUEST
            )

        if processId=="3":
            result['minPrice'] = results * 0.5
            result['maxPrice'] = results * 1.5
        print('estimate ����',requestCache)
        estimate = Estimate.objects.create( # ����� ������ ������ db�� insert
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
        print('������ estimate ����',estimate)
        
        # �ӽ÷� ������ ���� ����
        stlCache.close()
        fileName_=fileName+'.stl'
        loc = 'api/estimate/'
        path = os.path.join(loc,fileName_)
        os.remove(path)
        if fileType == 'stp':
            os.remove('api/estimate/' + fileName + '.stp')


        # ��� return
        return Response(
            data={ 
                'data': EstimateSerializer(estimate).data,
                #'proposalId': proposalId,
                'message': "�����Է�"
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

        # ������ list�� ���ΰ��� ���� �־ ������
        for process in processCache:
            #�ش� ������ �´� ���� ������ �޾ƿͼ� serializer�� ó��, id �� name�� ������
            detailProcess = detailManufactureProcess.objects.filter(process_id = process.id)
            detailProcessCache = DetailManufactureProcessSerializer_ID_Name_Process(detailProcess, many = True).data
            
            #������ ���ΰ��� list�� �߰����ְ�, ������ ��ü ��� list�� �߰�����
            processData = ManufactureProcessSerializer(process).data
            processData['detailManufactureProcess'] = detailProcessCache 
            result.append(processData)

        return Response(    
            data = {
                'count': len(processData),
                'data': result
            }
        )
