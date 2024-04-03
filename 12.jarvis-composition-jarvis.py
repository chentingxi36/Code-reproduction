import os
import pandas as pd
from jarvis.core.atoms import Atoms
from jarvis.ai.descriptors.cfid import CFID, feat_names
from pymatgen.io.cif import CifParser
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

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

# 处理单个 CIF 文件的函数
def process_cif_file(cif_path):
    cif_parser = CifParser(cif_path)
    structure = cif_parser.get_structures(primitive=True)[0]
    cif_filename = os.path.basename(cif_path)  # 获取文件的基本名称
    return cif_filename, get_jarvis_features(structure)  # 返回基本名称和 Jarvis 描述符

# 创建一个空列表来保存 Jarvis 描述符
jarvis_features = []

# 获取 CIF 文件夹中的所有 CIF 文件路径
cif_folder = 'cif_files2'
cif_files = [os.path.join(cif_folder, filename) for filename in os.listdir(cif_folder) if filename.endswith('.cif')]

# 获取描述符的名称列表
jarvis_feature_names = feat_names()

# 创建一个进度条
with tqdm(total=len(cif_files), desc='Processing CIF files') as pbar:
    # 使用进度条包装并行任务
    with ProcessPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(process_cif_file, cif_path) for cif_path in cif_files]
        # 使用as_completed获取已完成的任务并更新进度条
        for future in as_completed(futures):
            cif_filename, jarvis_feature = future.result()  # 获取任务结果
            jarvis_features.append({'CIF filename': cif_filename, **jarvis_feature})  # 将描述符值添加到字典中
            pbar.update(1)  # 更新进度条

# 将 Jarvis 描述符列表添加到 DataFrame 中
jarvis_df = pd.DataFrame(jarvis_features)

# 将结果保存到 CSV 文件中
jarvis_df.to_csv('structure_features_with_jarvis.csv', index=False)

