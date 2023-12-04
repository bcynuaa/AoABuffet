'''
 # @ project: AoABuffet-FluentBackend
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-07-19 16:10:13
 # @ description: path related utils
 '''

import os

def assurePathExists(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
        pass
    pass

def getPureFilename(filename: str) -> str:
    return os.path.splitext(os.path.split(filename)[1])[0]
    pass

print("utils: Path.py loaded")