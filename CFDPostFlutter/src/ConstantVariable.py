'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-06-29 17:37:07
 # @ Description: contain all the const variables
 '''

import json

constvar_json_filename: str = "config//constant_variable.json"
constvar_dict: dict = json.load(open(constvar_json_filename, 'r'))

kSmall_Amount: float = constvar_dict["small amount"]
kDefault_Interpolation_Type: str = constvar_dict["default interpolation type"]
kPrefered_Interpolation_Type: str = constvar_dict["preferred interpolation type"]

print("ConstantVariable.py is imported.")