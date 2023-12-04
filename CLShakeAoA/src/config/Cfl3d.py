'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-04 17:11:20
 # @ Description: values from cfl3d.json
 '''
 
import os
import json

cfl3d_json_filename: str = "config//cfl3d.json"
cfl3d_json_data: dict = json.load(open(cfl3d_json_filename, 'r'))

exe_path: str = cfl3d_json_data["exe path"]
exe_pure_filename: str = cfl3d_json_data["exe filename"]
inp_pure_filename: str = cfl3d_json_data["inp filename"]

exe_path = os.path.abspath(exe_path)
exe_filename = os.path.join(exe_path, exe_pure_filename)
inp_filename = os.path.join(exe_path, inp_pure_filename)

print("config: Cfl3d.py is imported.")