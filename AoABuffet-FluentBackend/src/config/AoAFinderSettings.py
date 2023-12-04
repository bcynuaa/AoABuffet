'''
 # @ project: AoABuffet-FluentBackend
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-07-19 20:52:51
 # @ description: AoAFinder related settings
 '''

import json

aoa_finder_settings_filename: str = "config//aoa_finder_settings.json"
aoa_finder_settings_data: dict = \
    json.load(open(aoa_finder_settings_filename, "r", encoding="utf-8"))

aoa_finder_dataframe_columns: list = aoa_finder_settings_data["dataframe"]["columns"]
Clalpha_shift: float = aoa_finder_settings_data["Clalpha shift"]    
Clalpha0_sample_points: list = aoa_finder_settings_data["Clalpha 0"]["sample points"]

where_buffet_AoA_begin: float = aoa_finder_settings_data["where buffet"]["AoA begin"]
where_buffet_delta_AoA: float = aoa_finder_settings_data["where buffet"]["delta AoA"]

tolerance: float = aoa_finder_settings_data["tolerance"]

interpolation_sample_number: int = aoa_finder_settings_data["interpolation sample number"]

print("config: AoAFinderSettings.py loaded")