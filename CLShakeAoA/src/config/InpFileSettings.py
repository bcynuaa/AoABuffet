'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-04 18:35:21
 # @ Description: values from inp file settings json
 '''

import os
import json

inp_file_settings_json_filename: str = "config//inp_file_settings.json"
inp_file_settings_json_data: dict = json.load(open(inp_file_settings_json_filename, 'r'))

file_digits: int = inp_file_settings_json_data["file digits"]
delimiter: str = inp_file_settings_json_data["delimiter"]
shared_lines_filename: str = inp_file_settings_json_data["shared lines filename"]

header: str = inp_file_settings_json_data["header"]
io_files_needed: list = inp_file_settings_json_data["io files needed"]

cltarg_lines: dict = inp_file_settings_json_data["cltarg lines"]

setup_comment: str = inp_file_settings_json_data["setup comment"]

title_line: str = "title line"
default_values: str = "default values"
condition_data: dict = inp_file_settings_json_data["condition data"]
reference_data: dict = inp_file_settings_json_data["reference data"]
cycling_data: dict = inp_file_settings_json_data["cycling data"]

number_format: str = "%0." + str(file_digits) + "f"
default_dt: float = cycling_data[default_values]["DT"]

shared_lines_filename = os.path.abspath(shared_lines_filename)
shared_lines: list = open(shared_lines_filename, 'r').readlines()
shared_lines = [line[:-1] for line in shared_lines]

line_break: str = "\n"

print("config: InpFileSettings.py is imported.")