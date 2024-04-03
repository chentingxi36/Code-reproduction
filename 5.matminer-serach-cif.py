import pandas as pd
import os
import pymatgen as mp

from matminer.featurizers.structure import JarvisCFID
from pymatgen.core.structure import Structure

jarvis = JarvisCFID()
cif_path = 'cif_files2/'
cif_files = os.listdir(cif_path)

jarvis_features = []
for cif in cif_files:
	cif_struc = Structure.from_file(cif_path + cif)
	cif_feature = jarvis.featurize(cif_struc)
	jarvis_features.append(cif_feature)

df = pd.DataFrame(jarvis_features, index = cif_files)

df['target'] = [0]*len(cif_path)

df.to_csv('featurized_cif_file.csv', index_label='cif_file')
