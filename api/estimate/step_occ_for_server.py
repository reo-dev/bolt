from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopAbs import TopAbs_SHELL, TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
# from OCC.Core.StepRepr import Handle_StepRepr_RepresentationItem
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeShape
from OCC.Core.BRepAlgo import BRepAlgo_BooleanOperation
from OCC.Core.TopoDS import topods, TopoDS_Iterator
from OCC.Core.TObj import TObj_Model
from OCC.Core.ShapeAnalysis import shapeanalysis_GetFaceUVBounds, shapeanalysis_OuterWire, shapeanalysis_ContourArea
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties, brepgprop_LinearProperties, brepgprop_VolumeProperties
from OCC.Core.GProp import GProp_GProps
from pprint import pprint
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus, \
    GeomAbs_BezierSurface, GeomAbs_BSplineSurface, GeomAbs_SurfaceOfRevolution, GeomAbs_SurfaceOfExtrusion, \
    GeomAbs_OffsetSurface, GeomAbs_OtherSurface
from OCC.Core.GeomAbs import GeomAbs_Line, GeomAbs_Circle, GeomAbs_Ellipse, GeomAbs_Hyperbola, GeomAbs_Parabola, \
    GeomAbs_BezierCurve, GeomAbs_BSplineCurve, GeomAbs_OffsetCurve, GeomAbs_OtherCurve
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.TopTools import TopTools_ListOfShape
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepBndLib import brepbndlib_Add
import trimesh
import numpy as np
import csv
import os
import math

# 알루미늄,Steel/합금강, 황동, 아크릴/나일론, 테프론, 플라스틱, SUS304/316
# material_ratio = [0.022, 0.05, 0.05, 0.0115, 0.05, 0.01, 0.06]
material_ratio = {7:0.022, 8:0.05, 9:0.05, 10:0.0115, 11:0.05, 12:0.01, 15:0.06}


def test(filename, material, stlname):
    # Face 구분. Face의 type에 따라 position, direction, radius 등 Face의 기하학 관련 정보를 가져온다.
    def _face_get_props(face):
        # face에 대한  분석을 위해 BRepAdaptor_Surface로 surface를 만들어 기하학적으로 접근하게 한다.
        face_adaptor = BRepAdaptor_Surface(face, False)
        # face의 종류 가져오기
        face_type = face_adaptor.GetType()

        # face의 종류는 Plane, Cylinder, Cone, Sphere, Torus, BezierSurface, BSplineSurface, SurfaceOfRevolution,
        # SurfaceOfExtrusion, OffsetSurface, OtherSurface 등이 있으며, 이 중 Plane, Cylinder, Cone, Sphere, Torus를 다룬다.
        # 평면

        if face_type == GeomAbs_Plane:
            # 중복 예외처리.
            if face in plane_list:
                return 0
            plane = face_adaptor.Plane()
            entity_face['type'] = 'plane'
            entity_face['position'] = plane.Axis().Location().Coord()
            direction = plane.Axis().Direction().Coord()
            # face.Orientation()이 1이면 평면의 normal vector가 물체의 바깥쪽이 아닌 안쪽을 향하고 있다는 걸 의미한다. 바깥쪽을 향하게 바꿔준다
            if face.Orientation() == 1:
                direction = (-direction[0], -direction[1], -direction[2])
            entity_face['direction'] = direction
            entity_face['coefficients'] = plane.Coefficients()
            entity_face['X axis'] = plane.XAxis().Direction().Coord()
            entity_face['Y axis'] = plane.YAxis().Direction().Coord()

            # 중복 체크를 위해 plane_list에 추가해준다.
            plane_list.append(face)
            typelist_num[0] += 1

        # 원기둥
        elif face_type == GeomAbs_Cylinder:
            # 중복 예외처리
            if face in cylinder_list:
                return 0
            cylinder = face_adaptor.Cylinder()
            entity_face['type'] = 'cylinder'
            entity_face['position'] = cylinder.Position().Location().Coord()
            entity_face['direction'] = cylinder.Axis().Direction().Coord()
            entity_face['coefficients'] = cylinder.Coefficients()
            entity_face['X axis'] = cylinder.XAxis().Direction().Coord()
            entity_face['Y axis'] = cylinder.YAxis().Direction().Coord()
            entity_face['radius'] = cylinder.Radius()
            cylinder_list.append(face)
            typelist_num[1] += 1


        # 원뿔
        elif face_type == GeomAbs_Cone:
            # 중복 예외처리
            if face in cone_list:
                return 0
            cone = face_adaptor.Cone()
            entity_face['type'] = 'cone'
            entity_face['position'] = cone.Position().Location().Coord()
            entity_face['direction'] = cone.Axis().Direction().Coord()
            entity_face['coefficients'] = cone.Coefficients()
            entity_face['X axis'] = cone.XAxis().Direction().Coord()
            entity_face['Y axis'] = cone.YAxis().Direction().Coord()
            entity_face['radius'] = 0
            entity_face['sub radius'] = 0
            entity_face['apex'] = cone.Apex().Coord()
            cone_list.append(face)
            typelist_num[2] += 1

        # 구
        elif face_type == GeomAbs_Sphere:
            if face in sphere_list:
                return 0
            sphere = face_adaptor.Sphere()
            entity_face['type'] = 'sphere'
            entity_face['position'] = sphere.Position().Location().Coord()
            entity_face['coefficients'] = sphere.Coefficients()
            entity_face['X axis'] = sphere.XAxis().Direction().Coord()
            entity_face['Y axis'] = sphere.YAxis().Direction().Coord()
            entity_face['radius'] = sphere.Radius()
            entity_face['volume'] = sphere.Volume()

            sphere_list.append(face)
            typelist_num[3] += 1
        # 원환면
        elif face_type == GeomAbs_Torus:
            if face in torus_list:
                return 0
            torus = face_adaptor.Torus()
            entity_face['type'] = 'torus'
            entity_face['position'] = torus.Position().Location().Coord()
            entity_face['direction'] = torus.Axis().Direction().Coord()
            entity_face['X axis'] = torus.XAxis().Direction().Coord()
            entity_face['Y axis'] = torus.YAxis().Direction().Coord()
            entity_face['major radius'] = torus.MajorRadius()
            entity_face['minor radius'] = torus.MinorRadius()
            entity_face['radius'] = entity_face['major radius'] + entity_face['minor radius'] / 2

            torus_list.append(face)
            typelist_num[4] += 1
        # 베지어 표면
        elif face_type == GeomAbs_BezierSurface:
            beziersurface = face_adaptor.Bezier()
            entity_face['type'] = 'beziersurface'

            typelist_num[5] += 1

        elif face_type == GeomAbs_BSplineSurface:
            bsplinesurface = face_adaptor.BSpline()
            entity_face['type'] = 'bsplinesurface'
            a = bsplinesurface.Poles()
            #             print('Poles', bsplinesurface.Poles(a))
            #             print('UKnots', bsplinesurface.UKnots())
            #             print('Umultiplicity', bsplinesurface.UMultiplicities())
            #             print('Uiso', bsplinesurface.UIso(1))
            typelist_num[6] += 1
            nbu = bsplinesurface.NbUPoles()
            nbv = bsplinesurface.NbVPoles()
            #             print('number of u',nbu)
            #             print('number of v',nbv)
            #             for nb in range(nbu):
            #                 print('Uiso', bsplinesurface.UIso(nb))
            #             for nb in range(nbv):
            #                 print('Viso', bsplinesurface.VIso(nb))
        elif face_type == GeomAbs_SurfaceOfRevolution:
            basiscurve = face_adaptor.BasisCurve()
            entity_face['type'] = 'basiscurve'
            typelist_num[7] += 1

        elif face_type == GeomAbs_SurfaceOfExtrusion:
            basiscurve = face_adaptor.BasisCurve()
            # #         print(basiscurve)
            typelist_num[8] += 1

        elif face_type == GeomAbs_OffsetSurface:
            offsetsurface = face_adaptor.OffsetSurface()
            # #         print(offsetsurface)
            typelist_num[9] += 1

        elif face_type == GeomAbs_OtherSurface:
            others = face_adaptor.OtherSurface()
            # #         print(others)
            typelist_num[10] += 1

        # 기본적으로 surface는 물체의 내부를 나타낸다. 그 부분이 물체의 내부인지 외부인지 확인하기 위해서는 face.Orientation()을 확인하면 된다.
        # 기본이 되는 surface를 토대로 만들어진 face의 direction은 face를 감싸는 wire에 의해 정해진다. face.Orientation()은 surface의
        # direction과 face의 direction이 일치하는 지 확인하는 함수이며, face.Orientation()이 0일 경우 물체의 내부를 나타내고, 1일 경우
        # 물체의 외부를 나타낸다.
        if face.Orientation() == 0:
            entity_face['inside'] = True
        else:
            entity_face['inside'] = False

    # Edge 구분. Edge의 type에 따라 position, direction, radius 등 Edge의 properties를 가져온다.
    def _edge_get_props(edge):
        curve_adaptor = BRepAdaptor_Curve(edge)
        curve_type = curve_adaptor.GetType()
        gprop = GProp_GProps()
        brepgprop_LinearProperties(edge, gprop)

        edge_len = gprop.Mass()

        if curve_type == GeomAbs_Line:
            line = curve_adaptor.Line()
            entity_edge['type'] = 'line'
            entity_edge['position'] = line.Location().Coord()
            direction = line.Direction().Coord()
            if edge.Orientation() == 1:
                direction = (-direction[0], -direction[1], -direction[2])
            entity_edge['direction'] = direction
            #             print('line :', entity)
            edgelist_num[0] += 1
        elif curve_type == GeomAbs_Circle:
            circle = curve_adaptor.Circle()
            entity_edge['type'] = 'circle'
            entity_edge['position'] = circle.Axis().Location().Coord()
            direction = circle.Axis().Direction().Coord()
            if edge.Orientation() == 1:
                direction = (-direction[0], -direction[1], -direction[2])
            entity_edge['direction'] = direction
            entity_edge['radius'] = circle.Radius()
            entity_edge['X axis'] = circle.XAxis().Direction().Coord()
            entity_edge['Y axis'] = circle.YAxis().Direction().Coord()
            #             print('circle :', entity)
            edgelist_num[1] += 1
        elif curve_type == GeomAbs_Ellipse:
            ellipse = curve_adaptor.Ellipse()
            entity_edge['type'] = 'ellipse'
            entity_edge['position'] = ellipse.Axis().Location().Coord()
            direction = ellipse.Axis().Direction().Coord()
            if edge.Orientation() == 1:
                direction = (-direction[0], -direction[1], -direction[2])
            entity_edge['direction'] = direction
            entity_edge['focus_1'] = ellipse.Focus1().Coord()
            entity_edge['focus_2'] = ellipse.Focus2().Coord()
            entity_edge['major radius'] = ellipse.MajorRadius()
            entity_edge['minor radius'] = ellipse.MinorRadius()
            entity_edge['X axis'] = ellipse.XAxis().Direction().Coord()
            entity_edge['Y axis'] = ellipse.YAxis().Direction().Coord()
            edgelist_num[2] += 1
        #             print('ellipse :', entity)
        elif curve_type == GeomAbs_Hyperbola:
            hyperbola = curve_adaptor.Hyperbola()
            entity_edge['type'] = 'hyperbola'
            entity_edge['position'] = hyperbola.Location().Coord()
            direction = hyperbola.Axis().Direction().Coord()
            if edge.Orientation() == 1:
                direction = (-direction[0], -direction[1], -direction[2])
            entity_edge['direction'] = direction
            #             print('hyperbola :', entity)
            edgelist_num[3] += 1
        elif curve_type == GeomAbs_Parabola:
            parabola = curve_adaptor.Parabola()
            entity_edge['type'] = 'parabola'
            entity_edge['position'] = parabola.Location().Coord()
            direction = parabola.Direction().Coord()
            if edge.Orientation() == 1:
                direction = (-direction[0], -direction[1], -direction[2])
            entity_edge['direction'] = parabola.Direction().Coord()
            #             print('parabola :', entity)
            edgelist_num[4] += 1
        elif curve_type == GeomAbs_BezierCurve:
            entity_edge['type'] = 'beziercurve'
            #             print('BezierCurve')
            edgelist_num[5] += 1
        elif curve_type == GeomAbs_BSplineCurve:
            bsplinecurve = curve_adaptor.BSpline()
            entity_edge['type'] = 'bsplinecurve'
            edgelist_num[6] += 1
        elif curve_type == GeomAbs_OffsetCurve:
            entity_edge['type'] = 'offsetcurve'
            #             print('OffsetCurve')
            edgelist_num[7] += 1
        else:
            entity_edge['type'] = 'other type'
            #             print('other types')
            edgelist_num[8] += 1


        entity_edge['len'] = edge_len

    def _cylinder_combining(surface):
        idx = surface_list.index(surface)
        # print('*' * 15, 'cylinder', '*' * 15)
        # pprint(wire_list[idx])

        dummyDic_wire = {}
        dummyDic_wire['edges'] = []
        dummyDic_edge = {}
        dummyDic_edge['type'] = 'blank'

        while True:
            wire_len = len(wire_list[idx])

            for i in range(len(wire_list[idx]) - 1):
                for j in range(1, len(wire_list[idx]) - i):
                    new_wire = {}
                    new_wire['edges'] = []
                    new_wire['area'] = 0
                    new_wire['height'] = 0
                    # print('wire_list[idx]', wire_list[idx])
                    # print('wire_list[idx][i]',wire_list[idx][i])
                    # print('wire_list[idx][i+j]', wire_list[idx][i+j])

                    wire_1 = wire_list[idx][i]['edges']
                    wire_2 = wire_list[idx][i + j]['edges']
                    check, pnt_1, pnt_2 = _check_overlapping(wire_1, wire_2)

                    if check:
                        pre_wire_1 = 0
                        pre_wire_2 = 0
                        while wire_1 != pre_wire_1 and wire_2 != pre_wire_2:
                            pre_wire_1 = wire_1
                            pre_wire_2 = wire_2
                            for circle_1 in wire_1:
                                for circle_2 in wire_2:

                                    #                         CircleCombining(circle_1, circle_2, pnt_1, pnt_2)
                                    if circle_1['type'] != 'circle' or circle_2['type'] != 'circle':
                                        continue
                                    if pnt_1 in circle_1['points'] and pnt_1 in circle_2['points']:
                                        pnt = pnt_1
                                    elif pnt_2 in circle_1['points'] and pnt_2 in circle_2['points']:
                                        pnt = pnt_2
                                    else:

                                        continue

                                    if circle_1['position'] == circle_2['position'] and circle_1['direction'] == circle_2[
                                        'direction'] and circle_1['radius'] == circle_2['radius'] and circle_1['X axis'] == \
                                            circle_2['X axis'] and circle_1['Y axis'] == circle_2['Y axis']:

                                        if circle_1['points'][0] == pnt:
                                            new_point = [circle_2['points'][0], circle_1['points'][1]]
                                        else:
                                            new_point = [circle_1['points'][0], circle_2['points'][1]]

                                        new_circle = {}
                                        new_circle['type'] = 'circle'
                                        new_circle['position'] = circle_1['position']
                                        new_circle['direction'] = circle_1['direction']
                                        new_circle['radius'] = circle_1['radius']
                                        new_circle['X axis'] = circle_1['X axis']
                                        new_circle['Y axis'] = circle_1['Y axis']
                                        new_circle['len'] = circle_1['len'] + circle_2['len']

                                        new_circle['points'] = new_point

                                        n = wire_1.index(circle_1)
                                        del wire_1[n]
                                        wire_1.insert(n, dummyDic_edge)

                                        n = wire_2.index(circle_2)

                                        del wire_2[n]
                                        wire_2.insert(n, dummyDic_edge)


                                        new_wire['edges'].append(new_circle)
                        for e in wire_1:
                            if e['type'] == 'blank':
                                continue
                            new_wire['edges'].append(e)
                        for e in wire_2:
                            if e['type'] == 'blank':
                                continue
                            new_wire['edges'].append(e)
                        new_area = wire_list[idx][i]['area'] + wire_list[idx][i+j]['area']
                        new_wire['area'] = new_area
                        new_wire['height'] = max(wire_list[idx][i]['height'], wire_list[idx][i+j]['height'])
                        del wire_list[idx][i]
                        wire_list[idx].insert(i, dummyDic_wire)

                        del wire_list[idx][i + j]
                        wire_list[idx].insert(i + j, dummyDic_wire)

                        wire_list[idx].append(new_wire)
                    else:
                        continue

            if wire_len == len(wire_list[idx]):
                break

        while dummyDic_wire in wire_list[idx]:
            wire_list[idx].remove(dummyDic_wire)
        # print('\n')
        # print('*' * 15, 'after', '*' * 15)
        # print('\n')
        # pprint(wire_list[idx])

    def _cone_combining(surface):
        idx = surface_list.index(surface)
        # print('*' * 15, 'cone', '*' * 15)
        # pprint(wire_list[idx])
        dummyDic_wire = {}
        dummyDic_wire['edges'] = []
        dummyDic_edge = {}
        dummyDic_edge['type'] = 'blank'

        for i in range(len(wire_list[idx]) - 1):
            for j in range(1, len(wire_list[idx]) - i):
                new_wire = {}
                new_wire['edges'] = []
                new_wire['area'] = []
                wire_1 = wire_list[idx][i]['edges']
                wire_2 = wire_list[idx][i + j]['edges']
                check, pnt_1, pnt_2 = _check_overlapping(wire_1, wire_2)

                if check:
                    for circle_1 in wire_1:
                        for circle_2 in wire_2:

                            if circle_1['type'] != 'circle' or circle_2['type'] != 'circle':
                                continue
                            if pnt_1 in circle_1['points'] and pnt_1 in circle_2['points']:
                                pnt = pnt_1
                            elif pnt_2 in circle_1['points'] and pnt_2 in circle_2['points']:
                                pnt = pnt_2
                            else:
                                continue

                            if circle_1['position'] == circle_2['position'] and circle_1['direction'] == circle_2[
                                'direction'] and circle_1['radius'] == circle_2['radius'] and circle_1['X axis'] == \
                                    circle_2['X axis'] and circle_1['Y axis'] == circle_2['Y axis']:

                                if circle_1['points'][0] == pnt:
                                    new_point = [circle_2['points'][0], circle_1['points'][1]]
                                else:
                                    new_point = [circle_1['points'][0], circle_2['points'][1]]

                                new_circle = {}
                                new_circle['type'] = 'circle'
                                new_circle['position'] = circle_1['position']
                                new_circle['direction'] = circle_1['direction']
                                new_circle['radius'] = circle_1['radius']
                                new_circle['X axis'] = circle_1['X axis']
                                new_circle['Y axis'] = circle_1['Y axis']
                                new_circle['len'] = circle_1['len'] + circle_2['len']

                                new_circle['points'] = new_point


                                n = wire_1.index(circle_1)
                                del wire_1[n]
                                wire_1.insert(n, dummyDic_edge)

                                n = wire_2.index(circle_2)

                                del wire_2[n]
                                wire_2.insert(n, dummyDic_edge)

                                new_wire['edges'].append(new_circle)

                    for e in wire_1:
                        if e['type'] == 'blank':
                            continue
                        new_wire['edges'].append(e)
                    for e in wire_2:
                        if e['type'] == 'blank':
                            continue

                        new_wire['edges'].append(e)


                    new_area = wire_list[idx][i]['area'] + wire_list[idx][i+j]['area']
                    new_wire['area'] = new_area
                    new_wire['height'] = max(wire_list[idx][i]['height'], wire_list[idx][i]['height'])
                    del wire_list[idx][i]
                    wire_list[idx].insert(i, dummyDic_wire)

                    del wire_list[idx][i + j]
                    wire_list[idx].insert(i + j, dummyDic_wire)
                    wire_list[idx].append(new_wire)

                else:
                    continue

        while dummyDic_wire in wire_list[idx]:
            wire_list[idx].remove(dummyDic_wire)
        # print('\n')
        # print('*' * 15, 'after', '*' * 15)
        # print('\n')
        # pprint(wire_list[idx])

    def _sphere_combining(surface):
        idx = surface_list.index(surface)
        # print('*' * 15, 'sphere', '*' * 15)
        # pprint(wire_list[idx])

        for i in range(len(wire_list[idx]) - 1):
            for j in range(1, len(wire_list[idx]) - i):
                new_wire = {}
                new_wire['edges'] = []
                new_wire['area'] = []
                wire_1 = wire_list[idx][i]['edges']
                wire_2 = wire_list[idx][i + j]['edges']

                check, pnt_list = _check_overlapping_sphere(wire_1, wire_2)
                _bsplinecurve_to_circle(surface, wire_1)
                _bsplinecurve_to_circle(surface, wire_2)
                if check:
                    for pnt_pair in pnt_list:
                        for circle_1 in wire_1:
                            for circle_2 in wire_2:
                                if circle_1['type'] != 'circle' or circle_2['type'] != 'circle':
                                    continue
                                pnt_1, pnt_2 = pnt_pair[0], pnt_pair[1]
                                if pnt_1 in circle_1['points'] and pnt_1 in circle_2['points']:
                                    pnt = pnt_1
                                elif pnt_2 in circle_1['points'] and pnt_2 in circle_2['points']:
                                    pnt = pnt_2
                                else:
                                    continue

                                # if circle_1['position'] == circle_2['position'] and circle_1['direction'] == circle_2[
                                #     'direction'] and circle_1['radius'] == circle_2['radius'] and circle_1['X axis'] == \
                                #         circle_2['X axis'] and circle_1['Y axis'] == circle_2['Y axis']:
                                if circle_1['position'] == circle_2['position'] and circle_1['direction'] == circle_2[
                                    'direction'] and circle_1['radius'] == circle_2['radius']:
                                    if circle_1['points'][0] == pnt:
                                        new_point = [circle_2['points'][0], circle_1['points'][1]]
                                    else:
                                        new_point = [circle_1['points'][0], circle_2['points'][1]]

                                    new_circle = {}
                                    new_circle['type'] = 'circle'
                                    new_circle['position'] = circle_1['position']
                                    new_circle['direction'] = circle_1['direction']
                                    new_circle['radius'] = circle_1['radius']
                                    # new_circle['X axis'] = circle_1['X axis']
                                    # new_circle['Y axis'] = circle_1['Y axis']
                                    new_circle['len'] = circle_1['len'] + circle_2['len']

                                    new_circle['points'] = new_point
                                    dummyDic = {}
                                    dummyDic['type'] = 'blank'

                                    n = wire_1.index(circle_1)
                                    del wire_1[n]
                                    wire_1.insert(n, dummyDic)

                                    n = wire_2.index(circle_2)

                                    del wire_2[n]
                                    wire_2.insert(n, dummyDic)

                                    new_wire['edges'].append(new_circle)

                                # else:
                                #     if circle_1['position'] != circle_2['position']:
                                #         print('position is different')
                                #
                                #     elif circle_1['direction'] != circle_2['direction']:
                                #
                                #         print('direction is different')
                                #     else:
                                #         print('radius is different')
                                #     print('########################################')
                                #     pprint(circle_1)
                                #     pprint(circle_2)
                    for e in wire_1:
                        if e['type'] == 'blank':
                            continue
                        new_wire['edges'].append(e)
                    for e in wire_2:
                        if e['type'] == 'blank':
                            continue

                        new_wire['edges'].append(e)

                    dummyList = []
                    new_area = wire_list[idx][i]['area'] + wire_list[idx][i + j]['area']
                    new_wire['area'] = new_area
                    del wire_list[idx][i]
                    wire_list[idx].insert(i, dummyList)

                    del wire_list[idx][i + j]
                    wire_list[idx].insert(i + j, dummyList)
                    wire_list[idx].append(new_wire)

                else:
                    continue

        while [] in wire_list[idx]:
            wire_list[idx].remove([])
        # print('*' * 15, 'after sphere', '*' * 15)
        # pprint(wire_list[idx])

    def _circle_combining(wire):
        pnt_lst = []
        dummyDic_edge = {}
        dummyDic_edge['type'] = 'blank'

        for i in range(len(wire['edges'])):
            if wire['edges'][i]['type'] == 'line':
                pnt_lst.append(wire['edges'][i]['points'][1])

        for i in range(len(wire['edges'])):
            for j in range(len(wire['edges'])):
                if i == j:
                    continue
                if wire['edges'][i]['type'] != 'circle' or wire['edges'][j]['type'] != 'circle':
                    continue
                if wire['edges'][i]['points'][0] not in pnt_lst and wire['edges'][j]['points'][0] not in pnt_lst:
                    continue
                new_circle = {}
                new_point = []
                if wire['edges'][i]['points'][1] == wire['edges'][j]['points'][0]:
                    new_point = [wire['edges'][i]['points'][0], wire['edges'][j]['points'][1]]
                elif wire['edges'][i]['points'][0] == wire['edges'][j]['points'][1]:
                    new_point = [wire['edges'][j]['points'][0], wire['edges'][i]['points'][1]]
                if not new_point:
                    continue
                new_circle['type'] = 'circle'
                new_circle['position'] = wire['edges'][i]['position']
                new_circle['direction'] = wire['edges'][i]['direction']
                new_circle['radius'] = wire['edges'][i]['radius']
                new_circle['X axis'] = wire['edges'][i]['X axis']
                new_circle['Y axis'] = wire['edges'][i]['Y axis']
                new_circle['len'] = wire['edges'][i]['len'] + wire['edges'][j]['len']
                new_circle['points'] = new_point
                del wire['edges'][i]
                wire['edges'].insert(i, dummyDic_edge)
                del wire['edges'][j]
                wire['edges'].insert(j, dummyDic_edge)
                wire['edges'].append(new_circle)

        while dummyDic_edge in wire['edges']:
            wire['edges'].remove(dummyDic_edge)

    def _check_overlapping(wire_1, wire_2):
        pnt_1, pnt_2 = 0, 0
        check = False
        for edge_1 in wire_1:
            for edge_2 in wire_2:
                if edge_1['type'] != edge_2['type'] or edge_1['type'] == 'bsplinecurve':
                    continue
                if edge_1['position'] == edge_2['position'] and edge_1['len'] == edge_2['len'] and edge_1['points'][0] == \
                        edge_2['points'][1] and edge_1['points'][1] == edge_2['points'][0]:
                    dir_2 = edge_2['direction']
                    if edge_1['direction'] == (-dir_2[0], -dir_2[1], -dir_2[2]):

                        pnt_1 = edge_1['points'][0]
                        pnt_2 = edge_1['points'][1]
                        del wire_1[wire_1.index(edge_1)]
                        del wire_2[wire_2.index(edge_2)]
                        check = True
                        break
            if check:
                break

        return check, pnt_1, pnt_2

    def _check_overlapping_sphere(wire_1, wire_2):
        pnt_list = []
        check = False

        for edge_1 in wire_1:
            if edge_1['type'] != 'circle':
                continue
            for edge_2 in wire_2:
                if edge_2['type'] != 'circle':
                    continue
                if edge_1['position'] == edge_2['position'] and edge_1['len'] == edge_2['len'] and edge_1['points'][0] == \
                        edge_2['points'][1] and edge_1['points'][1] == edge_2['points'][0]:
                    dir_2 = edge_2['direction']
                    if edge_1['direction'] == (-dir_2[0], -dir_2[1], -dir_2[2]):
                        pnt_1 = edge_1['points'][0]
                        pnt_2 = edge_1['points'][1]
                        pnt_list.append((pnt_1, pnt_2))

                        del wire_1[wire_1.index(edge_1)]
                        del wire_2[wire_2.index(edge_2)]

                        check = True

        return check, pnt_list

    def _bsplinecurve_to_circle(surface, wire):
        for bsplinecurve in wire:
            if bsplinecurve['type'] != 'bsplinecurve':
                continue
            if wire.count(bsplinecurve) == 2:
                new_circle = {}
                new_circle['type'] = 'circle'
                new_circle['position'] = surface['position']
                pnt_1, pnt_2 = bsplinecurve['points'][0], bsplinecurve['points'][1]
                vec_1 = [0, 0,0]
                vec_2 = [0, 0, 0]
                for i in range(3):
                    vec_1[i] = pnt_1[i] - surface['position'][i]
                    vec_2[i] = pnt_2[i] - surface['position'][i]

                vec_1 = np.array(vec_1)
                vec_2 = np.array(vec_2)

                cross = np.cross(vec_1, vec_2)
                cross = cross / pow((pow(cross[0], 2) + pow(cross[1], 2) + pow(cross[2], 2)) , (1/2))
                new_circle['direction'] = tuple(cross)
                new_circle['radius'] = surface['radius']
                # new_circle['X axis'] =
                # new_circle['Y axis'] =
                new_circle['len'] = bsplinecurve['len']
                new_circle['points'] = bsplinecurve['points']
                wire.append(new_circle)

                new_circle = {}
                new_circle['type'] = 'circle'
                new_circle['position'] = surface['position']
                cross = -cross
                new_circle['direction'] = tuple(cross)
                new_circle['radius'] = surface['radius']
                new_circle['len'] = bsplinecurve['len']
                new_circle['points'] = [bsplinecurve['points'][1], bsplinecurve['points'][0]]
                wire.append(new_circle)

                while bsplinecurve in wire:
                    wire.remove(bsplinecurve)
                break


    def _circular_segment(r, height):
        cos = height/r
        rad = math.acos(cos)
        segment = r**2 * rad/2-math.sin(2*rad)*r*r/2
        return segment

    def _lathe_processing(mesh):
        circle_bottom_enum = ['cylinder', 'cone', 'torus', 'sphere']

        lathe_surface_list = []
        lathe_wire_list = []
        bounding_cylinder_axis = mesh.bounding_cylinder.direction.copy()
        for i in range(len(bounding_cylinder_axis)):
            bounding_cylinder_axis[i] = abs(round(bounding_cylinder_axis[i], 1))

        center = (mesh.bounds[1] + mesh.bounds[0]) / 2
        for i in range(len(center)):
            center[i] = round(center[i], 1)

        cylinder_ax = 3

        for i in range(3):
            if bounding_cylinder_axis[i] == 1:
                cylinder_ax = i
                break

        if cylinder_ax == 3:
            return 0, 0

        for surface in surface_list:
            if surface['type'] in circle_bottom_enum:
                surface_axis = []
                check = True
                cnt = 0
                if 'direction' in surface:
                    for i in range(3):
                        surface_axis.append(abs(surface['direction'][i]))
                        if surface_axis[i] != bounding_cylinder_axis[i]:
                            check = False
                            break

                for i in range(3):
                    if i == cylinder_ax:
                        continue
                    if round(surface['position'][i]) == round(center[i]):
                        cnt += 1
                if cnt != 2:
                    check = False

                if check:
                    if surface not in lathe_surface_list:
                        lathe_surface_list.append(surface)
                    if len(lathe_wire_list) == lathe_surface_list.index(surface):
                        lathe_wire_list.append([])
                    for wire in wire_list[surface_list.index(surface)]:
                        lathe_wire_list[lathe_surface_list.index(surface)].append(wire)

        if not lathe_surface_list:
            print(11111111111)
            return 0, 0

        lathe_check = False

        max_radius = 0
        for lathe_surface in lathe_surface_list:
            if max_radius<lathe_surface['radius']:
                max_radius = lathe_surface['radius']
                inside_check = lathe_surface['inside']
                max_surface = lathe_surface

        if not inside_check:
            return 0, 0

        for i in range(3):
            if i == cylinder_ax:
                continue
            if mesh.extents[i]*0.9 <= 2*max_radius:
                lathe_check = True
                break

        # 가공품의 끝부분 확인. 이것도 생각해봐야 됨
        if not lathe_check:
            cylinder_ax_min = mesh.bounds[1][cylinder_ax]
            cylinder_ax_max = mesh.bounds[0][cylinder_ax]

            for lathe_surface in lathe_surface_list:
                idx = lathe_surface_list.index(lathe_surface)
                for wire in lathe_wire_list[idx]:
                    for edge in wire['edges']:
                        if edge['type'] == 'circle' or edge['type'] == 'other type' or edge['type'] == 'bsplinecurve':
                            if edge['type'] == 'other type' and edge['points'][0] == edge['points'][1]:
                                edge['position'] = edge['points'][0]
                            elif edge['type'] == 'bsplinecurve':
                                if edge['points'][0][cylinder_ax]> edge['points'][1][cylinder_ax]:
                                    if mesh.bounds[1][cylinder_ax] - edge['points'][0][cylinder_ax] < edge['points'][1][
                                       cylinder_ax] - mesh.bounds[0][cylinder_ax]:
                                        edge['position'] = edge['points'][0]
                                    else:
                                        edge['position'] = edge['points'][1]
                                else:
                                    if mesh.bounds[1][cylinder_ax] - edge['points'][1][cylinder_ax] < edge['points'][0][
                                       cylinder_ax] - mesh.bounds[0][cylinder_ax]:
                                        edge['position'] = edge['points'][1]
                                    else:
                                        edge['position'] = edge['points'][0]
                            if cylinder_ax_min > edge['position'][cylinder_ax]:
                                cylinder_ax_min = edge['position'][cylinder_ax]
                                min_edge = edge

                            if cylinder_ax_max < edge['position'][cylinder_ax]:
                                cylinder_ax_max = edge['position'][cylinder_ax]
                                max_edge = edge

            for surface in surface_list:
                if surface['type'] in circle_bottom_enum and (surface['type'] == 'torus' or surface['inside']):
                    for wire in wire_list[surface_list.index(surface)]:
                        if min_edge in wire['edges'] or max_edge in wire['edges']:
                            lathe_check = True
                            break
        print(lathe_check)
        print('lathe_check')
        if lathe_check:
            lathe_min_position = mesh.bounds[1][cylinder_ax]
            lathe_max_position = mesh.bounds[0][cylinder_ax]
            for lathe_wire in lathe_wire_list[lathe_surface_list.index(max_surface)]:
                for lathe_edge in lathe_wire['edges']:
                    if lathe_edge['type'] == 'other type':
                        lathe_edge['position'] = lathe_edge['points'][0]

                    elif lathe_edge['type'] == 'bsplinecurve':
                        if lathe_edge['points'][0][cylinder_ax] > lathe_edge['points'][1][cylinder_ax]:
                            if mesh.bounds[1][cylinder_ax] - lathe_edge['points'][0][cylinder_ax] < lathe_edge['points'][1][
                                cylinder_ax] - mesh.bounds[0][cylinder_ax]:
                                lathe_edge['position'] = lathe_edge['points'][0]
                            else:
                                lathe_edge['position'] = lathe_edge['points'][1]
                        else:
                            if mesh.bounds[1][cylinder_ax] - lathe_edge['points'][1][cylinder_ax] < lathe_edge['points'][0][
                                cylinder_ax] - mesh.bounds[0][cylinder_ax]:
                                lathe_edge['position'] = lathe_edge['points'][1]
                            else:
                                lathe_edge['position'] = lathe_edge['points'][0]

                    lathe_min_position = min(lathe_min_position, lathe_edge['position'][cylinder_ax])
                    lathe_max_position = max(lathe_max_position, lathe_edge['position'][cylinder_ax])
            for i in range(len(surface_list)):
                if surface_list[i] == max_surface:
                    continue
                for wire in wire_list[i]:
                    outer_wire = False
                    min_position = mesh.bounds[1][cylinder_ax]
                    max_position = mesh.bounds[0][cylinder_ax]
                    for edge in wire['edges']:
                        if edge['type'] == 'other type':
                            edge['position'] = edge['points'][0]
                        elif edge['type'] == 'bsplinecurve':
                            if edge['points'][0][cylinder_ax] > edge['points'][1][cylinder_ax]:
                                if mesh.bounds[1][cylinder_ax] - edge['points'][0][cylinder_ax] < edge['points'][1][
                                   cylinder_ax] - mesh.bounds[0][cylinder_ax]:
                                    edge['position'] = edge['points'][0]
                                else:
                                    edge['position'] = edge['points'][1]
                            else:
                                if mesh.bounds[1][cylinder_ax] - edge['points'][1][cylinder_ax] < edge['points'][0][
                                   cylinder_ax] - mesh.bounds[0][cylinder_ax]:
                                    edge['position'] = edge['points'][1]
                                else:
                                    edge['position'] = edge['points'][0]

                        min_position = min(min_position, edge['position'][cylinder_ax])
                        max_position = max(max_position, edge['position'][cylinder_ax])

                        edge_center_len = 0
                        if not outer_wire:
                            for j in range(3):
                                if j == cylinder_ax:
                                    continue

                                edge_center_len += (edge['position'][j] - center[j]) ** 2
                            edge_center_len = edge_center_len ** (1 / 2)
                            if edge_center_len > max_surface['radius']:
                                outer_wire = True
                        if not outer_wire:
                            continue

                    if not outer_wire:
                        continue

                    if lathe_min_position>=min_position and lathe_max_position<=max_position:
                        lathe_check = False
                        break
                if not lathe_check:

                    break




        # 자재 구분
        # if mesh.bounding_cylinder.volume < mesh.bounding_box.volume:
            # bounding_cylinder_height = mesh.extents[cylinder_ax]
            # bounding_cylinder_radius = round(
            #     pow(mesh.bounding_cylinder.volume / (bounding_cylinder_height * math.pi), (1 / 2)),
            #     1)
            # min_edge = 0
            # max_edge = 0
            #
            # for lathe_surface in lathe_surface_list:
            #     if lathe_surface['type'] == 'plane':
            #         min_edge = lathe_wire_list[0][0]['edges'][0]
            #         max_edge = lathe_wire_list[0][0]['edges'][0]
            #         break
            # if min_edge == 0:
            #     lathe_check = True
            #
            # cylinder_ax_min = mesh.bounds[1][cylinder_ax]
            # cylinder_ax_max = mesh.bounds[0][cylinder_ax]
            #
            # for surface in lathe_surface_list:
            #     if lathe_check:
            #         break
            #     idx = lathe_surface_list.index(surface)
            #     for wire in lathe_wire_list[idx]:
            #
            #         for edge in wire['edges']:
            #             if edge['type'] == 'circle' and edge['radius'] == bounding_cylinder_radius:
            #                 lathe_check = True
            #                 break
            #             else:
            #                 if edge['type'] == 'circle' or edge['type'] == 'other type':
            #                     if edge['type'] == 'other type' and edge['points'][0] == edge['points'][1]:
            #                         edge['position'] = edge['points'][0]
            #                     if cylinder_ax_min > edge['position'][cylinder_ax]:
            #                         cylinder_ax_min = edge['position'][cylinder_ax]
            #                         # min_end_type = surface['type']
            #                     if cylinder_ax_max < edge['position'][cylinder_ax]:
            #                         cylinder_ax_max = edge['position'][cylinder_ax]
            #                         # max_end_type = surface['type']
            #
            #                 if edge['type'] == 'circle' or edge['type'] == 'other type' or edge['type'] == 'bsplincurve':
            #                     if edge['type'] == 'other type' and edge['points'][0] == edge['points'][1]:
            #                         edge['position'] = edge['points'][0]
            #                     elif edge['type'] == 'bsplinecurve':
            #                         if edge['points'][0][cylinder_ax]> edge['points'][1][cylinder_ax]:
            #                             if mesh.bounds[1][cylinder_ax] - edge['points'][0][cylinder_ax] < edge['points'][1][
            #                                cylinder_ax] - mesh.bounds[0][cylinder_ax]:
            #                                 edge['position'] = edge['points'][0]
            #                             else:
            #                                 edge['position'] = edge['points'][1]
            #                         else:
            #                             if mesh.bounds[1][cylinder_ax] - edge['points'][1][cylinder_ax] < edge['points'][0][
            #                                cylinder_ax] - mesh.bounds[0][cylinder_ax]:
            #                                 edge['position'] = edge['points'][1]
            #                             else:
            #                                 edge['position'] = edge['points'][0]
            #                     if cylinder_ax_min > edge['position'][cylinder_ax]:
            #                         cylinder_ax_min = edge['position'][cylinder_ax]
            #                         min_edge = edge
            #
            #                     if cylinder_ax_max < edge['position'][cylinder_ax]:
            #                         cylinder_ax_max = edge['position'][cylinder_ax]
            #                         max_edge = edge
            #         if lathe_check:
            #             break
            #     if lathe_check:
            #         break
            # for surface in surface_list:
            #     if surface['type'] in circle_bottom_enum and (surface['type'] == 'torus' or surface['inside']):
            #         for wire in wire_list[surface_list.index(surface)]:
            #             if min_edge in wire or max_edge in wire:
            #                 lathe_check = True
            #                 break

        # else:
        #     if lathe_surface_list:
        #         pass

        if not lathe_check:

            return 0, 0

        lathe_processing_volume = mesh.bounding_cylinder.volume

        # surface는 무한하지 않다는 가정
        for i in range(len(lathe_surface_list)):
            surface_type = lathe_surface_list[i]['type']
            height = lathe_wire_list[i][0]['height']
            for wire in lathe_wire_list[i]:
                height = max(height, wire['height'])
            cylinder_position_lst = []
            cone_position_lst = []
            sphere_position_lst = []
            torus_position_lst = []
            if surface_type == 'cylinder':
                radius = lathe_surface_list[i]['radius']
                volume = height * radius * radius * math.pi
                # print('height, radius, volume', height, radius, volume)
            elif surface_type == 'cone':
                radius = lathe_surface_list[i]['radius']
                sub_radius = lathe_surface_list[i]['sub radius']
                oh = height + (sub_radius * height) / (radius - sub_radius)
                volume = (radius * radius * oh - sub_radius * sub_radius * (oh - height)) * math.pi / 3
                # print('height, radius, sub_radius, volume', height, radius, sub_radius, volume)
            elif surface_type == 'sphere':
                radius = lathe_surface_list[i]['radius']
                if 'upper radius' in lathe_surface_list[i]:
                    upper_radius = lathe_surface_list[i]['upper radius']
                else:
                    upper_radius = 0
                if 'lower radius' in lathe_surface_list[i]:
                    lower_radius = lathe_surface_list[i]['lower radius']
                else:
                    lower_radius = 0
                volume = math.pi * height * (
                        3 * (lower_radius ** 2) + 3 * (upper_radius ** 2) + (height ** 2)) / 6
            elif surface_type == 'torus':
                if lathe_surface_list[i]['inside']:
                    radius = lathe_surface_list[i]['major radius'] + lathe_surface_list[i]['minor radius'] / 2
                    volume = height * radius * radius * math.pi
                else:
                    radius = lathe_surface_list[i]['major radius'] - lathe_surface_list[i]['minor radius'] / 2
                    volume = height * radius * radius * math.pi
                    lathe_processing_volume -= volume
                    continue

            # surface가 무한하다는 가정

            # for wire in lathe_wire_list[i]:
            #     if surface_type == 'cylinder':
            #         # cylinder_check = True
            #         # for edge in wire['edges']:
            #         #     if edge['type'] == 'circle':
            #         #         if edge['position'] in cylinder_position_lst:
            #         #             cylinder_check = False
            #         #             break
            #         # if not cylinder_check:
            #         #     continue
            #         # for edge in wire['edges']:
            #         #     if edge['type'] == 'circle':
            #         #         cylinder_position_lst.append(edge['position'])
            #
            #         height = wire['height']
            #         radius = lathe_surface_list[i]['radius']
            #         beforeround = height * radius * radius * math.pi
            #         volume = height * radius * radius * math.pi
            #         print('height, radius, volume', height, radius, volume)
            #     elif surface_type == 'cone':
            #         height = wire['height']
            #         radius = lathe_surface_list[i]['radius']
            #         sub_radius = lathe_surface_list[i]['sub radius']
            #         beforeround = math.pi * height * (pow(2 * radius, 2) + radius * sub_radius + pow(2 * sub_radius, 2)) / 12
            #         oh = height + (sub_radius * height) / (radius - sub_radius)
            #         volume = (radius * radius * oh - sub_radius * sub_radius * (oh - height)) * math.pi / 3
            #         print('height, radius, sub_radius, volume', height, radius,sub_radius, volume)
            #     elif surface_type == 'sphere':
            #         min_pnt, max_pnt = mesh.bounds[1][cylinder_ax], mesh.bounds[0][cylinder_ax]
            #         lower_radius, upper_radius = 0, 0
            #
            #         for edge in wire['edges']:
            #             if edge['type'] != 'circle':
            #                 continue
            #             if min_pnt > edge['position'][cylinder_ax]:
            #                 lower_radius = edge['radius']
            #                 min_pnt = edge['position'][cylinder_ax]
            #             if max_pnt < edge['position'][cylinder_ax]:
            #                 upper_radius = edge['radius']
            #                 max_pnt = edge['position'][cylinder_ax]
            #
            #         if min_pnt == mesh.bounds[1][cylinder_ax]:
            #             min_pnt = mesh.bounds[0][cylinder_ax]
            #         if max_pnt == mesh.bounds[0][cylinder_ax]:
            #             max_pnt = mesh.bounds[1][cylinder_ax]
            #         height = max_pnt - min_pnt
            #
            #         volume = math.pi * height * (
            #                     3 * pow(lower_radius, 2) + 3 * pow(upper_radius, 2) + pow(height, 2)) / 6
            #
            #
            #     elif surface_type == 'torus':
            #         # height = 2 * lathe_surface_list[i]['minor radius']
            #         height = wire['height']
            #         if lathe_surface_list[i]['inside']:
            #             radius = lathe_surface_list[i]['major radius']+lathe_surface_list[i]['minor radius']/2
            #             volume = height * radius * radius * math.pi
            #         else:
            #             radius = lathe_surface_list[i]['major radius'] - lathe_surface_list[i]['minor radius']/2
            #             volume = height * radius * radius * math.pi
            #             lathe_processing_volume -= volume
            #             continue

                    # Torus 조건 설정. 미완.

                    # min_pnt, max_pnt = mesh.bounds[1][cylinder_ax], mesh.bounds[0][cylinder_ax]
                    # lower_radius = 0
                    # upper_radius = 0
                    #
                    # for edge in wire['edges']:
                    #     if edge['type'] != 'circle':
                    #         continue
                    #     if abs(edge['direction'][cylinder_ax]) != 1:
                    #         continue
                    #     if min_pnt > edge['position'][cylinder_ax]:
                    #         lower_radius = edge['radius']
                    #         min_pnt = edge['position'][cylinder_ax]
                    #     if max_pnt < edge['position'][cylinder_ax]:
                    #         upper_radius = edge['radius']
                    #         max_pnt = edge['position'][cylinder_ax]
                    #
                    #     # torus의 형태에 따라 구분 필요
                    #     # if edge['radius'] >= surface['major radius']:
                    #
                    #     # else:
                    #
                    # if min_pnt == mesh.bounds[1][cylinder_ax]:
                    #     min_pnt = mesh.bounds[0][cylinder_ax]
                    # if max_pnt == mesh.bounds[0][cylinder_ax]:
                    #     max_pnt = mesh.bounds[1][cylinder_ax]
                    # upper_height = max_pnt - lathe_surface_list[i]['position'][cylinder_ax]
                    # lower_height = lathe_surface_list[i]['position'][cylinder_ax] - min_pnt
                    # print(lathe_surface_list[i])
                    # r = lathe_surface_list[i]['minor radius']
                    #
                    # if upper_height >= 0 and lower_height >= 0:
                    #     upper_segment = CircularSegment(r, upper_height)
                    #     lower_segment = CircularSegment(r, lower_height)
                    #
                    # elif upper_height < 0:
                    #     cos = abs(upper_height) / r
                    #     sin = pow(1 - cos * cos, (1 / 2))
                    #     upper_segment = abs(upper_height) * r * sin
                    #     lower_segment = CircularSegment(r, lower_height)
                    # elif lower_height < 0:
                    #     cos = abs(lower_height) / r
                    #     sin = pow(1 - cos * cos, (1 / 2))
                    #     upper_segment = CircularSegment(r, upper_height)
                    #     lower_segment = abs(lower_height) * r * sin
                    # minorcirlce_area = math.pi * r * r - upper_segment - lower_segment
                    # volume = lathe_surface_list[i]['major radius'] * 2 * math.pi * minorcirlce_area

            if lathe_surface_list[i]['inside']:
                lathe_processing_volume -= volume
                print('inside')
                print(volume)
            else:
                lathe_processing_volume += volume
                print('outside')
                print(volume)

        lathe_cnt = len(lathe_surface_list)

        for lathe_surface in lathe_surface_list:
            if lathe_surface in surface_list:
                idx = surface_list.index(lathe_surface)
                surface_list.remove(lathe_surface)
                del wire_list[idx]

        return round(lathe_processing_volume, 1), lathe_cnt

    def _drilling_processing():
        drilling_surface_list = []
        drilling_wire_list = []

        for surface in surface_list:
            if surface['type'] == 'cylinder' or surface['type'] == 'cone':
                if surface['inside']:
                    continue
                drilling_check = True

                for wire in wire_list[surface_list.index(surface)]:
                    for edge in wire['edges']:
                        if edge['type'] == 'circle' and (edge['points'][0] != edge['points'][1] or edge['len'] <= round(2 * surface['radius'] * math.pi / 4, 1)):
                            drilling_check = False
                            break
                    if drilling_check:
                        if surface not in drilling_surface_list:
                            drilling_surface_list.append(surface)
                        idx = drilling_surface_list.index(surface)

                        if len(drilling_wire_list) == idx:
                            drilling_wire_list.append([])
                        drilling_wire_list[idx].append(wire)



        # 드릴링 부피 및 횟수
        drilling_volume = 0
        drilling_count = 0
        drilling_rhratio_volume = 0
        for i in range(len(drilling_surface_list)):
            surface_type = drilling_surface_list[i]['type']
            for wire in drilling_wire_list[i]:
                if surface_type == 'cylinder':
                    height = wire['height']
                    radius = drilling_surface_list[i]['radius']
                    volume = round(height * radius * radius * math.pi, 1)
                    beforeround = height * radius * radius * math.pi
                    # print('height, radius, volume', height, radius, volume)
                elif surface_type == 'cone':
                    height = wire['height']
                    radius = drilling_surface_list[i]['radius']
                    sub_radius = drilling_surface_list[i]['sub radius']
                    volume = round(
                        math.pi * height * (pow(2 * radius, 2) + radius * sub_radius + pow(2 * sub_radius, 2)) / 12, 1)
                    beforeround = math.pi * height * (pow(2 * radius, 2) + radius * sub_radius + pow(2 * sub_radius, 2)) / 12
                    # print('height, radius, sub_radius, volume', height, radius, sub_radius, volume)
                drilling_volume += volume
                drilling_count += 1
                drilling_rhratio_volume += volume * height / radius


        drilling_volume = round(drilling_volume, 1)
        print('드릴링:',drilling_volume, drilling_count, drilling_rhratio_volume)

        # 드릴링의 정삭, 황삭 조건.

        # for drilling_surface in drilling_surface_list:
        #     if drilling_surface['type'] == 'cylinder': # 3mm 이하일 경우 황삭만, 3mm 초과일 경우 황삭 + 정삭
        #         if drilling_surface['radius'] >3:
        #             if not drilling_surface in finishing_surface_list:
        #                 finishing_surface_list.append(drilling_surface)
        #             idx = finishing_surface_list.index(drilling_surface)
        #             if len(finishing_wire_list) == idx:
        #                 finishing_wire_list.append([])
        #             for wire in wire_list[surface_list.index(drilling_surface)]:
        #                 finishing_wire_list[idx].append(wire)

        for drilling_surface in drilling_surface_list:
            if drilling_surface in surface_list:
                idx = surface_list.index(drilling_surface)
                drilling_idx = drilling_surface_list.index(drilling_surface)
                for drilling_wire in drilling_wire_list[drilling_idx]:
                    while drilling_wire in wire_list[idx]:
                        wire_list[idx].remove(drilling_wire)
                if not wire_list[idx]:
                    wire_list.remove(wire_list[idx])
                    surface_list.remove(drilling_surface)

        return drilling_volume, drilling_count, drilling_rhratio_volume

    def _finishing_processing(mesh):
        finishing_processing_area = 0
        rectangle_processing_1 = []
        rectangle_processing_2 = []
        rectangle_cylinder_processing = 0
        rectangle_cylinder_shallow_processing=0
        rectangle_cylinder_deep_processing=0
        rectangle_processing_edge_list = []
        rectangle_processing_surface = []
        rectangle_processing_point_list = []
        processing_axis = _processing_axis(mesh)
        processing_axis_list = []
        processing_axis_list.append(processing_axis)
        finishing_processing_wire = []
        finishing_processing_edge = []
        finishing_cylinder = 0

        inner_line = 0
        for i in range(len(surface_list)):
            for wire in wire_list[i]:
                finishing_processing_area += wire['area']
        for wires in finishing_wire_list:
            for wire in wires:
                finishing_processing_area += wire['area']

        print('겉면 빼기 전 정삭가공:', finishing_processing_area)
        finishing_processing_area = 0

        for i in range(len(surface_list)):
            finishing_check = True
            surface = surface_list[i]

            if surface['type'] == 'plane':
                norm_vector = 3
                for j in range(3):
                    if abs(round(surface['direction'][j], 1)) == 1:
                        norm_vector = j
                        break
                if norm_vector != 3:
                    if round(mesh.bounds[0][norm_vector], 1) in surface['position'] or round(mesh.bounds[1][norm_vector], 1) in surface['position']:
                        finishing_check = False
            if finishing_check:
                if surface not in finishing_surface_list:
                    finishing_surface_list.append(surface)
                    if surface['type'] == 'cylinder':
                        for j in range(3):
                            if abs(surface['direction'][j]) == 1:
                                if processing_axis != i:
                                    for wire in wire_list[surface_list.index(surface)]:
                                        finishing_cylinder += wire['height']
                                if j not in processing_axis_list:
                                    processing_axis_list.append(j)


                idx = finishing_surface_list.index(surface)
                if len(finishing_wire_list) == idx:
                    finishing_wire_list.append([])
                for wire in wire_list[surface_list.index(surface)]:
                    finishing_wire_list[idx].append(wire)
        for n in range(len(finishing_surface_list)):
            finishing_surface = finishing_surface_list[n]
            if finishing_surface['type'] != 'plane':   # 기준이 되는 평면
                continue
            rectangle_processing_surface.append(finishing_surface)

            norm_vector_xyz = 3
            for i in range(3):
                if abs(round(finishing_surface['direction'][i], 1)) == 1:
                    norm_vector_xyz = i
                    break

            if norm_vector_xyz == 3:
                continue

            for m in range(len(finishing_surface_list)):
                sub_finishing_surface = finishing_surface_list[m]

                if sub_finishing_surface in rectangle_processing_surface:
                    continue
                if sub_finishing_surface['type'] == 'plane' and abs(round(finishing_surface['direction'][norm_vector_xyz], 1)) == abs(round(sub_finishing_surface['direction'][norm_vector_xyz], 1)):
                    continue

                for wire in finishing_wire_list[n]:
                    for subwire in finishing_wire_list[m]:
                        # print('subwire', subwire)

                        for subedge in subwire['edges']:
                            if subedge in rectangle_processing_edge_list:
                                # print('subedge already')
                                continue
                            temp_edge = _temp_edge(subedge)
                            if temp_edge in wire['edges']:
                                subedge_vector = subedge['direction']
                                norm_vector = finishing_surface['direction']
                                if sub_finishing_surface['type'] == 'plane':
                                    sub_norm_vector = [round(sub_finishing_surface['direction'][0], 1),
                                                       round(sub_finishing_surface['direction'][1], 1),
                                                       round(sub_finishing_surface['direction'][2], 1)]
                                    cross = np.cross(subedge_vector, norm_vector)
                                    cross = [round(cross[0], 1), round(cross[1], 1), round(cross[2], 1)]

                                    if sub_norm_vector == cross:
                                        if abs(subedge_vector[processing_axis]) == 1:
                                            len_1 = _plane_height(wire, sub_norm_vector, subedge)
                                            len_2 = _plane_height(subwire, norm_vector, subedge)
                                            if len_1*4<subedge['len'] or len_2*4<subedge['len']:
                                                # print('가공 깊이가 너무 깊습니다.')
                                                pass
                                            if len_1<10 or len_2<10:
                                                pass
                                                # print('rectangle_processing_1')
                                                # print('폭이 좁음')
                                                # print(subedge['len'], len_1, len_2)

                                            rectangle_processing_1.append(round(subedge['len'], 1))
                                        else:
                                            if abs(sub_norm_vector[processing_axis]) == 1:
                                                processing_axis_wire = wire
                                                processing_axis_vector = sub_norm_vector
                                                width_axis_wire = subwire
                                                width_axis_vector = norm_vector
                                            elif abs(norm_vector[processing_axis]) == 1:
                                                processing_axis_wire = subwire
                                                processing_axis_vector = norm_vector
                                                width_axis_wire = wire
                                                width_axis_vector = sub_norm_vector
                                            else:
                                                continue
                                            # pnt_list = []
                                            # for processing_axis_edge in processing_axis_wire['edges']:
                                            #     if processing_axis_edge['type'] == 'circle':
                                            #         pnt_list.append(list(processing_axis_edge['position']))
                                            #         pnt_list.append(list(processing_axis_edge['points'][0]))
                                            #         pnt_list.append(list(processing_axis_edge['points'][1]))
                                            #     elif processing_axis_edge['type'] == 'bsplinecurve' or processing_axis_edge['type'] == 'line':
                                            #         pnt_list.append(list(processing_axis_edge['points'][0]))
                                            #         pnt_list.append(list(processing_axis_edge['points'][1]))
                                            # for i in range(len(pnt_list)):
                                            #     pnt_list[i] = AxisFitting(pnt_list[i], processing_axis_vector)
                                            # max_pnt = pnt_list[0][2]
                                            # for pnt in pnt_list:
                                            #     max_pnt = max(max_pnt, pnt[2])
                                            # min_pnt = AxisFitting(list(subedge['position']), processing_axis_vector)[2]
                                            # face_height = round(max_pnt - min_pnt, 1)
                                            face_height = _plane_height(processing_axis_wire, processing_axis_vector, subedge)
                                            width_height = _plane_height(width_axis_wire, width_axis_vector, subedge)
                                            if face_height > 4 * width_height:
                                                pass
                                                # print('가공 깊이가 너무 깊습니다.')
                                            if width_height < 10 or subedge['len'] < 10:
                                                pass
                                                # print('rectangle_processing_2')
                                                # print('폭이 좁음')
                                                # print(subedge['len'], face_height, width_height)
                                            rectangle_processing_2.append(round(subedge['len'], 1))

                                        if wire not in finishing_processing_wire:
                                            finishing_processing_wire.append(wire)
                                        if len(finishing_processing_edge) == finishing_processing_wire.index(wire):
                                            finishing_processing_edge.append([])
                                        finishing_processing_edge[finishing_processing_wire.index(wire)].append(temp_edge)

                                        if subwire not in finishing_processing_wire:
                                            finishing_processing_wire.append(subwire)
                                        if len(finishing_processing_edge) == finishing_processing_wire.index(subwire):
                                            finishing_processing_edge.append([])
                                        finishing_processing_edge[finishing_processing_wire.index(subwire)].append(subedge)

                                        rectangle_processing_edge_list.append(subedge)

                                        if subedge['type'] == 'line':
                                            for point in rectangle_processing_point_list:
                                                if (subedge['points'][1] == point[0] and sub_norm_vector == list(point[2])) or \
                                                   (subedge['points'][0] == point[1] and sub_norm_vector == [-point[2][0], -point[2][1], -point[2][2]]):
                                                    inner_line += 1
                                            rectangle_processing_point_list.append((subedge['points'][0], subedge['points'][1], subedge_vector))
                                        break

                                    else:
                                        cos = _angle_between_vectors(norm_vector, sub_norm_vector)

                                        if cos<0:
                                            # print('예각')
                                            pass
                                        elif cos == 0:
                                            # print('90도')
                                            pass
                                        else:
                                            # print('둔각')
                                            pass

                                elif sub_finishing_surface['type'] == 'cylinder':
                                    if subedge['type'] != 'circle':
                                        continue
                                    if (sub_finishing_surface['inside'] and subedge_vector == norm_vector) or (
                                       not sub_finishing_surface['inside'] and subedge_vector == (-norm_vector[0],
                                                                                                  -norm_vector[1],
                                                                                                  -norm_vector[2])):
                                        if subwire['height'] < 5:  # 부분 원기둥 가공의 깊이 구분
                                            rectangle_cylinder_shallow_processing += subwire['height']
                                            if not sub_finishing_surface['inside'] and subwire['area']<=2*sub_finishing_surface['radius']*math.pi*wire['height']:
                                                inner_line += 1

                                        else:
                                            rectangle_cylinder_deep_processing += subwire['height']

                                        temp_sub_edge = _temp_edge(subedge)

                                        # if not sub_finishing_surface['inside']:

                                    else:
                                        # print('failed')
                                        # print(sub_finishing_surface['inside'], subedge_vector, norm_vector)
                                        # if not sub_finishing_surface['inside']:
                                        #     norm_vector = (-norm_vector[0], -norm_vector[1], -norm_vector[2])
                                        #
                                        # print(subedge_vector, norm_vector)
                                        # print(subedge_vector == norm_vector)
                                        pass
                            else:
                                # print('no temp edge')
                                pass
        t_processing_surface_list = []
        t_processing_wire_list = []
        t_processing_edge_list = []

        for edges in finishing_processing_edge:
            if len(edges)<2:
                continue
            for i in range(len(edges)):
                for j in range(i+1, len(edges)):
                    edge_1 = edges[i]
                    edge_2 = edges[j]
                    if edge_1['len'] == edge_2['len'] and edge_1['direction'] == (-edge_2['direction'][0], -edge_2['direction'][1], -edge_2['direction'][2]):
                        wire = finishing_processing_wire[finishing_processing_edge.index(edges)]
                        for k in range(len(finishing_processing_edge)):
                            if k == finishing_processing_edge.index(edges):
                                continue
                            for edge in finishing_processing_edge[k]:
                                if (edge_1['len'] == edge['len'] and edge_1['direction'] == (-edge['direction'][0], -edge[
                                   'direction'][1], -edge['direction'][2]) and edge_1['position'] == edge['position']) or (
                                   edge['len'] == edge_2['len'] and edge['direction'] == (-edge_2['direction'][0], -edge_2[
                                   'direction'][1], -edge_2['direction'][2]) and edge['position'] == edge_2['position']):
                                    if finishing_processing_wire[k] not in t_processing_wire_list:
                                        t_processing_wire_list.append(finishing_processing_wire[k])
                                    if t_processing_wire_list.index(finishing_processing_wire[k]) == len(t_processing_edge_list):
                                        t_processing_edge_list.append([])
                                    if edge not in t_processing_edge_list[t_processing_wire_list.index(finishing_processing_wire[k])]:
                                        t_processing_edge_list[t_processing_wire_list.index(finishing_processing_wire[k])].append(edge)

                        if wire not in t_processing_wire_list:
                            t_processing_wire_list.append(wire)
                        if t_processing_wire_list.index(wire) == len(t_processing_edge_list):
                            t_processing_edge_list.append([])
                        if edge_1 not in t_processing_edge_list[t_processing_wire_list.index(wire)]:
                            t_processing_edge_list[t_processing_wire_list.index(wire)].append(edge_1)
                        if edge_2 not in t_processing_edge_list[t_processing_wire_list.index(wire)]:
                            t_processing_edge_list[t_processing_wire_list.index(wire)].append(edge_2)

        t_processing_wire_list_2 = []
        t_processing_edge_list_2 = []

        t_processing_check = False

        for i in range(len(t_processing_wire_list)):
            # T자 가공의 밑바닥 면
            t_processing_bottom = 0
            if len(t_processing_edge_list[i])<2:
                continue
            t_processing_bottom = t_processing_wire_list[i]
            direction_check = True
            for e in t_processing_edge_list[i]:
                if 'direction' in e and e['direction'][processing_axis] == 1:
                    direction_check = False
                    break
            if not direction_check:
                continue


            side_check = False
            for j in range(len(t_processing_wire_list)):
                if i == j:
                    continue
                for k in range(j+1, len(t_processing_wire_list)):
                    if i == k:
                        continue

                    if len(t_processing_edge_list[j])<2 or len(t_processing_edge_list[k])<2:
                        continue

                    # T자 가공의 밑바닥 위 옆면
                    t_processing_side_1 = 0
                    t_processing_side_2 = 0
                    t_processing_side_edge_1 = 0
                    t_processing_side_edge_2 = 0
                    for t_processing_edge in t_processing_edge_list[i]:
                        temp_edge = _temp_edge(t_processing_edge)
                        if temp_edge in t_processing_edge_list[j]:
                            t_processing_side_1 = t_processing_wire_list[j]
                            t_processing_side_edge_1 = temp_edge
                        elif temp_edge in t_processing_edge_list[k]:
                            t_processing_side_2 = t_processing_wire_list[k]
                            t_processing_side_edge_2 = temp_edge

                    if t_processing_side_1 == 0 or t_processing_side_2 == 0:
                        continue
                    if t_processing_side_edge_1['len'] == t_processing_side_edge_2['len'] and t_processing_side_edge_1['direction'] == (-t_processing_side_edge_2['direction'][0], -t_processing_side_edge_2['direction'][1], -t_processing_side_edge_2['direction'][2]):
                        side_check = True
                        break
                if side_check:
                    break
            if not side_check:
                continue

            # T자 가공의 옆면 위의 면
            t_processing_upper_1 = 0
            t_processing_upper_edge_1 = 0
            t_processing_upper_2 = 0
            t_processing_upper_edge_2 = 0

            temp_edge = _temp_edge(t_processing_side_edge_1)
            for upper_edge_1 in t_processing_edge_list[t_processing_wire_list.index(t_processing_side_1)]:
                if temp_edge['direction'] == upper_edge_1['direction'] and temp_edge['len'] == upper_edge_1['len']:
                    t_processing_upper_edge_1 = upper_edge_1

            temp_edge = _temp_edge(t_processing_side_edge_2)
            for upper_edge_2 in t_processing_edge_list[t_processing_wire_list.index(t_processing_side_2)]:
                if temp_edge['direction'] == upper_edge_2['direction'] and temp_edge['len'] == upper_edge_2['len']:
                    t_processing_upper_edge_2 = upper_edge_2

            if t_processing_upper_edge_1 == 0 or t_processing_upper_edge_2 == 0:
                continue

            for j in range(len(t_processing_wire_list)):
                temp_edge_1 = _temp_edge(t_processing_upper_edge_1)
                temp_edge_2 = _temp_edge(t_processing_upper_edge_2)
                if temp_edge_1 in t_processing_edge_list[j]:
                    t_processing_upper_1 = t_processing_wire_list[j]
                elif temp_edge_2 in t_processing_edge_list[j]:
                    t_processing_upper_2 = t_processing_wire_list[j]
            if t_processing_upper_1 == 0 or t_processing_upper_2 == 0 or t_processing_upper_1 == t_processing_upper_2:
                continue

            t_processing_check = True
            break

        t_processing_len = 0

        if t_processing_check:
            t_processing_len = t_processing_upper_edge_1['len']
            for i in range(4):
                rectangle_processing_2.remove(t_processing_len)

        for wires in finishing_wire_list:
            for wire in wires:
                finishing_processing_area += wire['area']
        if lathe_processing_volume != 0:
            pass

        print('정삭 가공:', round(finishing_processing_area, 1))
        print('- cylinder:', round(finishing_cylinder, 1))
        print('- 직각 가공 1:', rectangle_processing_1)
        print('- 직각 가공 2:', rectangle_processing_2)
        print('- 꼭지점 가공:', inner_line)
        print('- 부분 원기둥 얕은 가공:', rectangle_cylinder_shallow_processing)
        print('- 부분 원기둥 깊은 가공:', rectangle_cylinder_deep_processing)
        print('- T자 가공:', t_processing_check)
        return round(finishing_processing_area,1), round(finishing_cylinder, 1), rectangle_processing_1, rectangle_processing_2, \
               round(rectangle_cylinder_shallow_processing, 1), round(rectangle_cylinder_deep_processing, 1), inner_line, \
               t_processing_len

    def _axis_fitting(pnt, standard_axis):
        axis = []
        new_pnt = pnt.copy()
        for ax in standard_axis:
            axis.append(round(ax, 1))
        # axis_len = pow(pow(axis[0], 2) + pow(axis[1], 2) + pow(axis[2], 2), (1 / 2))
        for i in range(3):
            if axis[i] == 0:
                new_pnt[i] = 0
        # print('pnt', pnt)
        # print('axis', axis)

        axis_len_xy = (axis[0]** 2 + axis[1]** 2)** (1/2)
        if axis_len_xy == 0:
            axis_len_xy = 1
        rot_cos1 = axis[1] / axis_len_xy
        rot_sin1 = axis[0] / axis_len_xy
        new_axis = [rot_cos1 * axis[0] - rot_sin1 * axis[1], rot_sin1 * axis[0] + rot_cos1 * axis[1], axis[2]]

        new_pnt = [rot_cos1 * new_pnt[0] - rot_sin1 * new_pnt[1], rot_sin1 * new_pnt[0] + rot_cos1 * new_pnt[1], new_pnt[2]]
        axis_len_xyz = (new_axis[0]** 2 + new_axis[1] ** 2 + new_axis[2] ** 2) ** (1 / 2)
        rot_cos2 = new_axis[2] / axis_len_xyz
        rot_sin2 = new_axis[1] / axis_len_xyz
        new_axis = [new_axis[0], rot_cos2 * new_axis[1] - rot_sin2 * new_axis[2],
                    rot_sin2 * new_axis[1] + rot_cos2 * new_axis[2]]
        new_pnt = [new_pnt[0], rot_cos2*new_pnt[1]-rot_sin2*new_pnt[2],rot_sin2*new_pnt[1] + rot_cos2*new_pnt[2]]
        # print('new_pnt', new_pnt)
        return new_pnt

    def _processing_axis(mesh):
        processing_axis = 0
        min_extent = mesh.extents[0]
        for i in range(len(mesh.extents)):
            if min_extent>mesh.extents[i]:
                processing_axis = i
                min_extent = mesh.extents[i]
        return processing_axis

    def _angle_between_vectors(vector_1, vector_2):
        inner = np.dot(vector_1, vector_2)
        vector_1_size = (vector_1[0] ** 2 + vector_1[1] ** 2 + vector_1[2] ** 2) ** (1/2)
        vector_2_size = (vector_2[0] ** 2 + vector_2[1] ** 2 + vector_2[2] ** 2) ** (1/2)
        cos = inner / (vector_1_size * vector_2_size)

        return cos

    def _temp_edge(edge): # 기존 edge와 방향이 다른 temp_edge 생성
        tempedge = {}
        tempedge['type'] = edge['type']
        tempedge['position'] = edge['position']
        tempedge['direction'] = (-edge['direction'][0], -edge['direction'][1], -edge['direction'][2])
        tempedge['len'] = edge['len']
        tempedge['points'] = [edge['points'][1], edge['points'][0]]
        if edge['type'] == 'circle':
            tempedge['radius'] = edge['radius']
            tempedge['X axis'] = edge['X axis']
            tempedge['Y axis'] = edge['Y axis']
        return tempedge

    def _plane_height(wire, vector, sub_edge = 0):  # plane의 높이를 구하는 함수. vector는 높이의 기준, sub_edge는 출발선이 없을 경우 0, 있을 경우 해당 edge
        pnt_list = []
        for edge in wire['edges']:
            if edge['type'] == 'circle':
                pnt_list.append(list(edge['position']))
                pnt_list.append(list(edge['points'][0]))
                pnt_list.append(list(edge['points'][1]))
            elif edge['type'] == 'bsplinecurve' or edge['type'] == 'line':
                pnt_list.append(list(edge['points'][0]))
                pnt_list.append(list(edge['points'][1]))
        for i in range(len(pnt_list)):
            pnt_list[i] = _axis_fitting(pnt_list[i], vector)
        max_pnt = pnt_list[0][2]
        min_pnt = pnt_list[0][2]
        for pnt in pnt_list:
            max_pnt = max(max_pnt, pnt[2])
            min_pnt = min(min_pnt, pnt[2])
        if sub_edge != 0:
            min_pnt = _axis_fitting(list(sub_edge['position']), vector)[2]
        plane_height = round(max_pnt - min_pnt, 1)
        return plane_height

    # Read the file and get the shape
    reader = STEPControl_Reader()
    print('지뢰15',filename)
    reader.ReadFile(filename)
    print('지뢰16')
    reader.TransferRoots()
    shape = reader.OneShape()


    # typelist_num = [0, 0, 0, 0, 0,]
    typelist_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    edgelist_num = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    plane_list = []
    cylinder_list = []
    cone_list = []
    sphere_list = []
    torus_list = []
    entity_list = []

    plane_area = 0
    cylinder_area = 0
    cone_area = 0
    sphere_area = 0
    torus_area = 0
    bsplinesurface_area = 0
    circle_bottom_enum = ['cylinder', 'cone', 'torus', 'sphere']


    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        s = exp.Current()
        exp.Next()
        # Converting TopoDS_Shape to TopoDS_Face
        face = topods.Face(s)
        entity = {}
        entity_face = {}

        # Getting Properties of face
        _face_get_props(face)

        entity['face'] = []
        entity['wire'] = {}
        entity['wire']['edges'] = []
        gprop = GProp_GProps()
        brepgprop_SurfaceProperties(face, gprop)
        entity['wire']['area'] = gprop.Mass()
        entity['wire']['height'] = 0

        exp2 = TopExp_Explorer(face, TopAbs_EDGE)

        while exp2.More():
            edge = exp2.Current()
            exp2.Next()
            entity_edge = {}

            # Getting Properties of edge
            _edge_get_props(edge)

            exp3 = TopExp_Explorer(edge, TopAbs_VERTEX)

            entity_point = []
            while exp3.More():
                vertex = exp3.Current()
                exp3.Next()
                entity_point.append(BRep_Tool.Pnt(vertex).Coord())
            if edge.Orientation() == 1:
                temp = entity_point[0]
                entity_point[0] = entity_point[1]
                entity_point[1] = temp

            entity_edge['points'] = entity_point

            if entity_edge['type'] == 'bsplinecurve':
                entity_edge['position'] = entity_point[0]

                entity_edge['direction'] = (entity_point[1][0] - entity_point[0][0],entity_point[1][1] - entity_point[0][1],entity_point[1][2] - entity_point[0][2])
                d = entity_edge['direction']
                b = pow(pow(d[0], 2) + pow(d[1], 2) + pow(d[2], 2), (1 / 2))
                d = (d[0]/b, d[1]/b, d[2]/b)
                entity_edge['direction'] = d

            entity['wire']['edges'].append(entity_edge)

        _circle_combining(entity['wire'])



        if entity_face['type'] in circle_bottom_enum and 'direction' in entity_face:
            pnt_list = []
            for e in entity['wire']['edges']:
                if e['type'] == 'circle':
                    pnt_list.append(list(e['position']))
                    pnt_list.append(list(e['points'][0]))
                    pnt_list.append(list(e['points'][1]))
                elif e['type'] == 'bsplinecurve' or e['type'] == 'line':
                    pnt_list.append(list(e['points'][0]))
                    pnt_list.append(list(e['points'][1]))

            for i in range(len(pnt_list)):
                pnt_list[i] = _axis_fitting(pnt_list[i], entity_face['direction'])

            min_pnt = pnt_list[0][2]
            max_pnt = pnt_list[0][2]

            for pnt in pnt_list:
                min_pnt = min(min_pnt, pnt[2])
                max_pnt = max(max_pnt, pnt[2])
            entity['wire']['height'] = max_pnt - min_pnt


            if entity_face['type'] == 'cone':
                cone_position = list(entity_face['position'])
                cone_position = _axis_fitting(cone_position, entity_face['direction'])
                original_height = pow(pow(entity_face['apex'][0] - entity_face['position'][0], 2) +
                                      pow(entity_face['apex'][1] - entity_face['position'][1], 2) +
                                      pow(entity_face['apex'][2] - entity_face['position'][2], 2), (1 / 2))
                face_adaptor = BRepAdaptor_Surface(face, False)
                cone = face_adaptor.Cone()

                if cone_position[2] == max_pnt:
                    entity_face['radius'] = cone.RefRadius()
                    entity_face['sub radius'] = (original_height - entity['wire']['height'])*entity_face['radius']/original_height

                else:
                    entity_face['sub radius'] = cone.RefRadius()
                    if original_height != 0:
                        entity_face['radius'] = entity_face['sub radius'] * (entity['wire']['height']+original_height) / original_height
                    else:
                        entity_face['radius'] = entity['wire']['height'] * math.tan(cone.SemiAngle())
            elif entity_face['type'] == 'sphere':
                for edge in entity['wire']['edges']:
                    if edge['type'] != 'circle':
                        continue
                    edge_position = list(edge['position'])
                    edge_position = _axis_fitting(edge_position, entity_face['direction'])

                    if edge_position[2] == min_pnt:
                        entity_face['lower radius'] = edge['radius']
                    elif edge_position[2] == max_pnt:
                        entity_face['upper radius'] = edge['radius']

        entity['face'] = entity_face
        entity_list.append(entity)

    surface_list = []
    wire_list = []

    for ent in entity_list:
        for key in ent['face']:
            if 'radius' in key:
                continue
            if type(ent['face'][key]) == bool or type(ent['face'][key]) == str:
                continue
            elif type(ent['face'][key]) == float:
                rounding = round(ent['face'][key], 1)
                ent['face'][key] = rounding
                continue
            pnt_list = []
            for t in ent['face'][key]:
                if type(t) == float:
                    rounding = round(t, 1)
                    pnt_list.append(rounding)
            ent['face'][key] = tuple(pnt_list)

        for edge in ent['wire']['edges']:
            for key in edge:
                if type(edge[key]) == str:
                    continue
                elif type(edge[key]) == float:
                    edge[key] = round(edge[key], 1)
                    continue
                pnt_list = []
                for t in edge[key]:
                    if type(t) == float:
                        pnt_list.append(round(t, 1))

                    else:
                        pnt_list_2 = []
                        for tt in t:
                            if type(tt) == float:
                                pnt_list_2.append(round(tt, 1))
                        pnt_list.append(tuple(pnt_list_2))

                if len(pnt_list) == 3:
                    pnt_list = tuple(pnt_list)
                edge[key] = pnt_list
        ent['wire']['area'] = round(ent['wire']['area'], 1)

        if ent['face'] not in surface_list:
            surface_list.append(ent['face'])
            # if ent['face']['type'] == 'cylinder':
            #     pprint(ent)
        idx = surface_list.index(ent['face'])
        if len(wire_list) == idx:
            wire_list.append([])
        wire_list[idx].append(ent['wire'])


    for surface in surface_list:
        # pprint(surface)
        if surface['type'] == 'cylinder':
            # print('\n\n')
            # print('*' * 15, 'cylinder', '*' * 15)
            _cylinder_combining(surface)
            # print('*' * 15, 'cylinder end', '*' * 15)
            # print('\n\n')
        elif surface['type'] == 'cone':
            # print('\n\n')
            # print('*' * 15, 'cone', '*' * 15)
            _cone_combining(surface)
            # print('*' * 15, 'cone end', '*' * 15)
            # print('\n\n')
        elif surface['type'] == 'sphere':
            _sphere_combining(surface)
        elif surface['type'] == 'torus':
            # print('\n\n')
            # print('*' * 15, 'torus', '*' * 15)
            _cylinder_combining(surface)
            # print('*' * 15, 'torus end', '*' * 15)
            # print('\n\n')

        else:
            pass
            # pprint(wire_list[surface_list.index(surface)])

    # for i in range(len(surface_list)):
    #     print('surface_list')
    #     pprint(surface_list[i])
    #     for j in range(len(wire_list[i])):
    #         print('wire_list')
    #         pprint(wire_list[i][j])

    # Convert from stp to stl
    mesh = trimesh.load_mesh(stlname)

    ###################################################################################################################
    ############################################                  #####################################################
    ############################################   선반 가공 판별   #####################################################
    ############################################                  #####################################################
    ###################################################################################################################

    lathe_processing_volume, lathe_cnt = _lathe_processing(mesh)
    print('선반 가공:', lathe_processing_volume, lathe_cnt)


    ###################################################################################################################
    ############################################                  #####################################################
    ############################################      드릴링       #####################################################
    ############################################                  #####################################################
    ###################################################################################################################

    finishing_surface_list = []
    finishing_wire_list = []

    drilling_volume, drilling_count, drilling_rhratio_volume = _drilling_processing()

    ###################################################################################################################
    ############################################                  #####################################################
    ############################################       정삭        #####################################################
    ############################################                  #####################################################
    ###################################################################################################################

    finishing_processing_area, finishing_cylinder, rectangle_processing_1, rectangle_processing_2, rectangle_cylinder_shallow_processing, rectangle_cylinder_deep_processing, inner_line, t_processing_len = _finishing_processing(mesh)


    ###################################################################################################################
    ############################################                  #####################################################
    ############################################        황삭       #####################################################
    ############################################                  #####################################################
    ###################################################################################################################
    stlname = os.path.splitext(filename)[0] + '.stl'

    if lathe_processing_volume != 0:
        bounding_volume = mesh.bounding_cylinder.volume
    else:
        bounding_volume = mesh.bounding_box.volume
        len_list = list(mesh.extents)
        len_list.remove(min(mesh.extents))
        # 가공면은 3mm를 여유를 둔다?
        # bounding_volume += len_list[0] * len_list[1] * 3


    gprop = GProp_GProps()
    brepgprop_VolumeProperties(shape, gprop)
    print('원래 부피:', round(gprop.Mass(), 1))
    roughing_processing_volume = round(bounding_volume - gprop.Mass() - lathe_processing_volume - drilling_volume, 1)
    if roughing_processing_volume <= finishing_processing_area * 1.5:
        print('정삭만 존재')
        finishing_processing_area = max(roughing_processing_volume, finishing_processing_area)
        roughing_processing_volume = 0
    print('bound 부피:', bounding_volume)
    print('황삭 가공:', roughing_processing_volume)
    print('가공 부피:', round(bounding_volume - gprop.Mass(), 1))

    result = lathe_processing_volume/3+drilling_volume+finishing_processing_area
    RectangleProcessing1 = 0
    RectangleProcessing2 = 0
    for i in rectangle_processing_1:
        RectangleProcessing1 += i ** 3.53
    for i in rectangle_processing_2:
        RectangleProcessing2 += i ** 1.6
    result += (RectangleProcessing1 + RectangleProcessing2+rectangle_cylinder_shallow_processing+rectangle_cylinder_deep_processing)
    result += (inner_line+t_processing_len*50 +roughing_processing_volume/5)
    commodity = mesh.volume * material_ratio[material]
    if max(mesh.extents)>400:
        result *= 1.4
    if min(mesh.extents)<10:
        commodity *= 10

    result += 40000 + commodity
    print('견적가:', result)

    return result
