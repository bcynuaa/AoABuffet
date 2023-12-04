'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-04 17:20:18
 # @ Description: run exe file
 '''

import os
import subprocess

def runExecutableFile(filename: str) -> None:
    file_absdir: str = os.path.dirname(filename)
    subprocess.call([filename], cwd=file_absdir)
    pass

print("utils: RunExe is imported.")