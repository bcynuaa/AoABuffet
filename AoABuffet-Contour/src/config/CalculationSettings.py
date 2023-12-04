'''
 # @ project: AoABuffet-PressureContour
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-10-12 14:20:07
 # @ description: calculation settings
 '''

import os
import json

calculation_settings_json_filename: str = "config//calculation_task_settings.json"
calculation_settings_json_data: dict = \
    json.load(open(calculation_settings_json_filename, "r", encoding="utf-8"))

mesh_data_path: str = calculation_settings_json_data["mesh data path"]
calculation_data_path: str = calculation_settings_json_data["calculation data path"]
connection_character: str = calculation_settings_json_data["connection character"]
mach_folder_hint: str = calculation_settings_json_data["mach folder hint"]

def getAbsPathReadCaseFilename(mesh_filename: str) -> str:
    return os.path.join(mesh_data_path, mesh_filename)
    pass

def getWorkingDirectory(mesh_filename: str, mach: float) -> str:
    # suppose mesh_filename is "xxxtxxx.cas"
    # mach is a 2 digit float number like "0.72"
    # return "calculation_data_path//xxxtxxx_mach_0.72"
    pure_mesh_filename: str = mesh_filename.split(".")[0]
    foler_name: str = pure_mesh_filename + connection_character + mach_folder_hint + str(mach)
    return os.path.join(calculation_data_path, foler_name)
    pass

print("config: CalculationSettings.py loaded")