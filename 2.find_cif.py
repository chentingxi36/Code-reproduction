from mp_api.client import MPRester
import os
import pandas as pd

# 将您的API密钥放在此处
API_KEY = 'd5fJczu2HWTt1HySXFQMgXAWJHXCiM3F'

# 创建一个 MPRester 实例
with MPRester(API_KEY) as mpr:
    # 读取您的 CSV 文件到 DataFrame
    df = pd.read_csv('your_data.csv')

    # 创建一个目录来保存 CIF 文件
    if not os.path.exists('cif_files2'):
        os.makedirs('cif_files2')

    # 遍历 DataFrame 中的每一行
    for index, row in df.iterrows():
        fm = row['Formula']
        sn = row['Space group number']
        De = row['Debye T (K)']
        Gap = row['Band Gap (eV)']

        # 根据化学式和空间群号搜索材料
        materials = mpr.materials.search(formula=fm, spacegroup_number=sn, fields=["structure"])
        
        # 如果找到匹配的材料，则将 CIF 数据写入到以化学式命名的 CIF 文件中
        if materials:
            structure = materials[0].structure
            cif = structure.to(fmt="cif")  # 将结构对象转换为 CIF 格式字符
            cif_filename = os.path.join('cif_files2', f'{fm}_{sn}_{Gap}_{De}.cif')
            with open(cif_filename, 'w') as f:
                f.write(cif)

