'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-04 17:26:25
 # @ Description: values from meshes json
 '''

import os
import json

meshes_json_filename: str = "config//meshes.json"
meshes_json_data: dict = json.load(open(meshes_json_filename, 'r'))

mesh_files_path: str = meshes_json_data["mesh files path"]
mesh_file_format: str = meshes_json_data["mesh file format"]

nn: int = meshes_json_data["airfoil geometry and grid"]["nn"]
j0: int = meshes_json_data["airfoil geometry and grid"]["j0"]
j1: int = meshes_json_data["airfoil geometry and grid"]["j1"]

mesh_files_path = os.path.abspath(mesh_files_path)

print("config: Meshes.py is imported.")