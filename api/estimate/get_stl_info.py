from stl import mesh

def get_stl_info(argv):
    stl_file = mesh.Mesh.from_file('api/estimate/'+argv+'.stl')
    print(stl_file)
    
    return {
              # x�� ����
              "x_length" : stl_file.x.max() - stl_file.x.min(), 
              # y�� ����
              "y_length" : stl_file.y.max() - stl_file.y.min(),
              # z�� ����
              "z_length" : stl_file.z.max() - stl_file.z.min(),
               # �𵨿� ���� ���� return, ������� Volume, Center of gravity, Inertia
              "volume" :  stl_file.get_mass_properties()[0]
    }