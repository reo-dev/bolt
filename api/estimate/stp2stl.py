from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
import os, sys, uuid
from django.conf import settings
import datetime
def stp2stl(argv):
    # input 파일argv에는 확장자를 제외한 이름이 들어온다.
    input_file  = argv + '.stp'   # input STEP (AP203/AP214 file)
    # 서버 로컬에 임시로 저장할 stl파일
    output_file = "api/estimate/" + argv + '.stl'  # output X3D file
    
    # 빈 step모델 객체를 생성
    step_reader = STEPControl_Reader()
    # 서버 로컬에 임시로 저장한 stp파일을 읽음
    step_reader.ReadFile( 'api/estimate/' + input_file )
    # 읽은 파일은 토대로 모양을 생성
    step_reader.TransferRoot()
    # 생성된 모양을 myshape에 return
    myshape = step_reader.Shape()
    
    # 기본 매개 변수 인 ASCIIMode를 사용하여 작성기 객체를 생성
    stl_writer = StlAPI_Writer()
    stl_writer.SetASCIIMode(False)
    
    # 매쉬 생성
    mesh = BRepMesh_IncrementalMesh(myshape, 0.1)
    # 설정된 모양에 대해서 계산
    mesh.Perform()
    assert mesh.IsDone()

    # 생성한 매쉬를 토대로 output_file에 내용을 작성
    stl_writer.Write(myshape, output_file)
    return output_file

if __name__ == '__main__':
    asdf(sys.argv[1:])
    