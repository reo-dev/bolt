from stl import mesh

def get_stl_info(argv):
    stl_file = mesh.Mesh.from_file('api/estimate/'+argv+'.stl')
    print(stl_file)
    
    return {
              # x축 길이
              "x_length" : stl_file.x.max() - stl_file.x.min(), 
              # y축 길이
              "y_length" : stl_file.y.max() - stl_file.y.min(),
              # z축 길이
              "z_length" : stl_file.z.max() - stl_file.z.min(),
               # 모델에 대한 정보 return, 순서대로 Volume, Center of gravity, Inertia
              "volume" :  stl_file.get_mass_properties()[0]
    }