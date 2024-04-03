import os
import pandas as pd
from tqdm import tqdm  # 导入tqdm模块
from jarvis.core.atoms import Atoms
from jarvis.ai.descriptors.cfid import CFID
from pymatgen.io.cif import CifParser

# 使用 Jarvis 包来获取结构描述符
def get_jarvis_features(structure):
    # 将 pymatgen 的结构对象转换为 Jarvis 的 Atoms 对象
    lattice_mat = structure.lattice.matrix
    elements = [site.specie.symbol for site in structure]
    coords = [site.frac_coords for site in structure]

    jarvis_atoms = Atoms(
        lattice_mat=lattice_mat,
        coords=coords,
        elements=elements,
        cartesian=False
    )

    # 获取 Jarvis 描述符
    desc_cfid = CFID(jarvis_atoms).get_comp_descp(jcell=True, jmean_chem=True, jmean_chg=True, jrdf=False, jrdf_adf=True, print_names=False)

    return desc_cfid

# 创建一个空列表来保存 Jarvis 描述符和 CIF 文件名
jarvis_features = []
cif_filenames = []

# 遍历 CIF 文件夹中的每一个文件，并显示进度条
cif_folder = 'cif_files2'
file_list = os.listdir(cif_folder)
for filename in tqdm(file_list, desc='Processing CIF files', unit='file'):
    if filename.endswith('.cif'):
        cif_path = os.path.join(cif_folder, filename)
        cif_parser = CifParser(cif_path)
        structure = cif_parser.get_structures(primitive=True)[0]

        # 获取 Jarvis 描述符
        jarvis_feature = get_jarvis_features(structure)
        jarvis_features.append(jarvis_feature)
        
        # 保存 CIF 文件名
        cif_filenames.append(filename)

# 创建 DataFrame，将 Jarvis 描述符和 CIF 文件名添加到其中
jarvis_df = pd.DataFrame({'CIF Filename': cif_filenames, 'Jarvis features': jarvis_features})

# 将结果保存到 CSV 文件中
jarvis_df.to_csv('structure_features_with_jarvis.csv', index=False)

