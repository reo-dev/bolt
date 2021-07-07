from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
import os, sys, uuid
from django.conf import settings
import datetime
def stp2stl(argv):
    # input ����argv���� Ȯ���ڸ� ������ �̸��� ���´�.
    input_file  = argv + '.stp'   # input STEP (AP203/AP214 file)
    # ���� ���ÿ� �ӽ÷� ������ stl����
    output_file = "api/estimate/" + argv + '.stl'  # output X3D file
    
    # �� step�� ��ü�� ����
    step_reader = STEPControl_Reader()
    # ���� ���ÿ� �ӽ÷� ������ stp������ ����
    step_reader.ReadFile( 'api/estimate/' + input_file )
    # ���� ������ ���� ����� ����
    step_reader.TransferRoot()
    # ������ ����� myshape�� return
    myshape = step_reader.Shape()
    
    # �⺻ �Ű� ���� �� ASCIIMode�� ����Ͽ� �ۼ��� ��ü�� ����
    stl_writer = StlAPI_Writer()
    stl_writer.SetASCIIMode(False)
    
    # �Ž� ����
    mesh = BRepMesh_IncrementalMesh(myshape, 0.1)
    # ������ ��翡 ���ؼ� ���
    mesh.Perform()
    assert mesh.IsDone()

    # ������ �Ž��� ���� output_file�� ������ �ۼ�
    stl_writer.Write(myshape, output_file)
    return output_file

if __name__ == '__main__':
    asdf(sys.argv[1:])
    