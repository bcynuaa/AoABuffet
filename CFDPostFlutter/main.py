'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-06-29 20:24:08
 # @ Description: the main entrance of the program
 '''

from src.CaseManager import CaseManager

if __name__ == "__main__":
    input_info_json_filename: str = "config/input_info.json"
    case_manager: CaseManager = CaseManager(input_info_json_filename)
    pass