'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-06-30 21:43:19
 # @ Description: contain utils
 '''

import os
import subprocess

def runExecutableFile(filename: str) -> None:
    """
    
    # run the executable file from absolute path
    
    ## Arguments
    
    - `filename`: the executable filename
    
    ## Return
    
    - `None`
    
    """
    file_absdir: str = os.path.dirname(filename)
    subprocess.call([filename], cwd=file_absdir)
    pass

print("Utils.py is imported.")