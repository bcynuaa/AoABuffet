'''
 # @ project: AoABuffet-FluentBackend
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-07-19 15:56:18
 # @ description: calculation related settings
 '''

import json

calculation_settings_json_filename: str = "config//calculation_settings.json"
calculation_settings_json_data: dict = \
    json.load(open(calculation_settings_json_filename, "r", encoding="utf-8"))

calculation_data_path: str = calculation_settings_json_data["calculation data path"]
folder_digits: int = calculation_settings_json_data["folder digits"]
connection_character: str = calculation_settings_json_data["connection character"]
mach_folder_hint: str = calculation_settings_json_data["mach folder hint"]
AoA_folder_hint: str = calculation_settings_json_data["AoA folder hint"]

dataframe_columns: list = calculation_settings_json_data["dataframe config"]["columns"]

mach_folder_pattern: str = mach_folder_hint + \
    connection_character + "%." + str(folder_digits) + "f"
AoA_folder_pattern: str = AoA_folder_hint + \
    connection_character + "%." + str(folder_digits) + "f"

print("config: CalculationSettings.py loaded")