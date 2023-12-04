'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-04 17:47:15
 # @ Description: path related
 '''
 
import os

def assurePath(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
        pass
    pass

def getPureFilename(filepath: str) -> str:
    return os.path.splitext(os.path.basename(filepath))[0]
    pass

print("utils: Path is imported.")