'''
 # @ project: AoABuffet-PressureContour
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-10-12 20:01:48
 # @ description: check mesh file
 '''

import os
import pandas as pd

csv_filename: str = r"C:\Users\bcynuaa\Desktop\LocalProject\Help\BuffetPressure\Data\BuffetAoAData\BuffetAoA.csv"

df = pd.read_csv(csv_filename, index_col=None)

mesh_path: str = r"C:\Users\bcynuaa\Desktop\LocalProject\Help\BuffetPressure\Data\Mesh"
mesh_file_list: list = os.listdir(mesh_path)

file_exists_list: list = []
for mesh_file in mesh_file_list:
    file_exists_list.append(mesh_file in df["mesh file"].values)
    pass
all_files_exist: bool = False not in file_exists_list

print("All files exist: ", all_files_exist)