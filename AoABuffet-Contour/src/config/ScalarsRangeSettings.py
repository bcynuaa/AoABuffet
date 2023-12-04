'''
 # @ project: AoABuffet-PressureContour
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-10-12 20:16:51
 # @ description: scalars range settings
 '''

import json
import pandas as pd

scalars_range_settings_json_filename: str = "config//scalars_range_settings.json"
scalars_range_settings_json_data: dict = \
    json.load(open(scalars_range_settings_json_filename, "r", encoding="utf-8"))

buffet_aoa_csv_filename: str = scalars_range_settings_json_data["buffet aoa csv filename"]
csv_filename_addition: str = scalars_range_settings_json_data["csv filename addition"]
min_max_csv_filename_addition: str = scalars_range_settings_json_data["min max csv filename addition"]
output_csv_filename: str = buffet_aoa_csv_filename.split(".")[0] + csv_filename_addition + ".csv"
min_max_csv_filename: str = buffet_aoa_csv_filename.split(".")[0] + min_max_csv_filename_addition + ".csv"

mesh_file_name: str = scalars_range_settings_json_data["mesh file name"]
mach_name: str = scalars_range_settings_json_data["mach name"]
attack_angle_name: str = scalars_range_settings_json_data["attack angle name"]
drag_coeff_name: str = scalars_range_settings_json_data["drag coeff name"]
lift_coeff_name: str = scalars_range_settings_json_data["lift coeff name"]
working_directory_name: str = scalars_range_settings_json_data["working directory name"]
flow_field_file_name: str = scalars_range_settings_json_data["flow field file name"]

scalar_min_addition: str = scalars_range_settings_json_data["scalar min addition"]
scalar_max_addition: str = scalars_range_settings_json_data["scalar max addition"]

print("config: ScalarsRangeSettings.py loaded")