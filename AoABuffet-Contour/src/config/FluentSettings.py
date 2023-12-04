'''
 # @ project: AoABuffet-PressureContour
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-10-11 23:34:12
 # @ description: fluent settings
 '''

import os
import json

fluent_settings_json_filename: str = "config//fluent_settings.json"
fluent_settings_json_data: dict = \
    json.load(open(fluent_settings_json_filename, "r", encoding="utf-8"))
    
fluent_exe: str = fluent_settings_json_data["fluent exe"]
dim: int = fluent_settings_json_data["dim"]
thread_number: int = fluent_settings_json_data["thread number"]

tui_commands_template: list = fluent_settings_json_data["tui commands template"]
tui_commands_custom_lines_index: list = list()
for key in fluent_settings_json_data["tui commands custom"]:
    tui_commands_custom_lines_index.append( \
        fluent_settings_json_data["tui commands custom"][key]["line number"] - 1)
    pass

read_case_default_filename: str = fluent_settings_json_data["tui commands custom"]["read case"]["default filename"]
write_case_default_filename: str = fluent_settings_json_data["tui commands custom"]["write case"]["default filename"]

cd_report_default_filename: str = fluent_settings_json_data["tui commands custom"]["cd report"]["default filename"]
cl_report_default_filename: str = fluent_settings_json_data["tui commands custom"]["cl report"]["default filename"]

tui_commands_filename: str = fluent_settings_json_data["tui commands filename"]

def getAbsPathWriteCaseFilename(working_directory: str) -> str:
    return os.path.join(working_directory, write_case_default_filename)
    pass

def getAbsPathCdReportFilename(working_directory: str) -> str:
    return os.path.join(working_directory, cd_report_default_filename)
    pass

def getAbsPathClReportFilename(working_directory: str) -> str:
    return os.path.join(working_directory, cl_report_default_filename)
    pass

def getAbsPathTuiCommandsFilename(working_directory: str) -> str:
    return os.path.join(working_directory, tui_commands_filename)
    pass

print("config: FluentSettings.py loaded")