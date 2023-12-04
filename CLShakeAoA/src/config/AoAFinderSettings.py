'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-06 16:37:47
 # @ Description: contains the AoA finder settings
 '''

import json

aoa_finder_settings_json_filename: str = "config//aoa_finder_settings.json"
aoa_finder_settings_json_data: dict = json.load(open(aoa_finder_settings_json_filename, 'r'))

AoA_begin: float = aoa_finder_settings_json_data["AoA begin"]

converge_AoA_begin: float = aoa_finder_settings_json_data["converge AoA"]["AoA begin"]["value"]
converge_AoA_end: float = aoa_finder_settings_json_data["converge AoA"]["AoA end"]["value"]
converge_tolerance: float = aoa_finder_settings_json_data["converge AoA"]["tolerance"]
converge_devide: int = aoa_finder_settings_json_data["converge AoA"]["devide"]
converge_extend_percentage: float = aoa_finder_settings_json_data["converge AoA"]["extend percentage"]["value"]
converge_min_AoA_span: float = aoa_finder_settings_json_data["converge AoA"]["min AoA span"]["value"]

linear_sample_number: int = aoa_finder_settings_json_data["linear part"]["sample number"]
linear_percentage: float = aoa_finder_settings_json_data["linear part"]["AoA span percentage"]

fluctuate_sample_number: int = aoa_finder_settings_json_data["fluctuate part"]["sample number"]
fluctuate_percentage: float = aoa_finder_settings_json_data["fluctuate part"]["AoA span percentage"]

diverge_sample_number: int = aoa_finder_settings_json_data["diverge part"]["sample number"]
diverge_percentage: float = aoa_finder_settings_json_data["diverge part"]["AoA span percentage"]

CLalpha0_sample_number: int = aoa_finder_settings_json_data["CLalpha 0"]["sample number"]
CLalpha0_first_AoA_index: int = aoa_finder_settings_json_data["CLalpha 0"]["first AoA index"]

interpolation_sample_number: int = aoa_finder_settings_json_data["interpolation"]["sample number"]

CLalpha_shift_buffet: float = aoa_finder_settings_json_data["AoA buffet"]["CLalpha shift"]
CLalpha_AoA_span_percentage: float = aoa_finder_settings_json_data["AoA buffet"]["AoA span percentage"]["value"]

print("config: AoAFinderSettings.py is imported.")