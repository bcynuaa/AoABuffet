'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-04 21:05:14
 # @ Description: values from calculation settings json
 '''

import os
import json

calculation_settings_json_filename: str = "config//calculation_settings.json"
calculation_settings_json_data: dict = json.load(open(calculation_settings_json_filename, 'r'))

calculation_data_path: str = calculation_settings_json_data["calculation data path"]
folder_digits: int = calculation_settings_json_data["folder digits"]
connection_character: str = calculation_settings_json_data["connection character"]
Minf_folder_hint: str = calculation_settings_json_data["Minf folder hint"]
AoA_folder_hint: str = calculation_settings_json_data["AoA folder hint"]

dataframe_columns: list = calculation_settings_json_data["dataframe config"]["columns"]

calculation_data_path = os.path.abspath(calculation_data_path)
folder_number_format: str = "%0." + str(folder_digits) + "f"

print("config: CalculationSettings.py is imported.")