'''
 # @ project: AoABuffet-FluentBackend
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-07-19 14:06:40
 # @ description: CalculationTask class
 '''

import os
import subprocess
import pandas as pd

from src.config.CalculationSettings import *
from src.config.FluentSettings import *

from src.utils.Path import *

from src.decorator.Clock import clock

import numpy as np

class CalculationTask:
    
    # ---------------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.working_directory: str = ""
        self.read_case_filename: str = read_case_default_filename
        self.mach: float = 0.0
        self.AoA: float = 0.0
        self.CD: float = 0.0
        self.CL: float = 0.0
        self.__projectAoA()
        self.iterations: int = 2500
        self.dataframe: pd.DataFrame = pd.DataFrame(columns=dataframe_columns)
        self.task_folder: str = ""
        self.write_case_filename: str = write_case_default_filename
        self.cd_report_filename: str = cd_report_default_filename
        self.cl_report_filename: str = cl_report_default_filename
        self.tui_commands: list = list()
        self.tui_commands_string: str = ""
        self.tui_commands_filename: str = tui_commands_filename
        self.cmd_list: list = \
            [fluent_exe, "-t%d" % thread_number, "%dd" % dim, "-i", self.tui_commands_filename]
        self.return_code: int = 0
        pass
    
    def __projectAoA(self) -> None:
        self.cos_AoA: float = np.cos(self.AoA * np.pi / 180)
        self.sin_AoA: float = np.sin(self.AoA * np.pi / 180)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def setWorkingDirectory(self, working_directory: str) -> None:
        self.working_directory = working_directory
        pass
    
    def setReadCaseFilename(self, read_case_filename: str) -> None:
        self.read_case_filename = read_case_filename
        pass
    
    def setMach(self, mach: float) -> None:
        self.mach = mach
        pass
    
    def setAoA(self, AoA: float) -> None:
        self.AoA = AoA
        self.__projectAoA()
        pass
    
    def setIterations(self, iterations: int) -> None:
        self.iterations = iterations
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __createTaskFolder(self) -> None:
        self.task_folder = os.path.join(self.working_directory, \
            mach_folder_pattern % self.mach, AoA_folder_pattern % self.AoA)
        self.write_case_filename = os.path.join(self.task_folder, write_case_default_filename)
        self.cd_report_filename = os.path.join(self.task_folder, cd_report_default_filename)
        self.cl_report_filename = os.path.join(self.task_folder, cl_report_default_filename)
        self.tui_commands_filename = os.path.join(self.task_folder, tui_commands_filename)
        self.cmd_list[-1] = self.tui_commands_filename
        assurePathExists(self.task_folder)
        print("task folder created: %s" % self.task_folder)
        pass
    
    def __generateTuiCommands(self) -> None:
        self.tui_commands = tui_commands_template.copy()
        custom_list: list = [
            self.read_case_filename,
            (self.mach, self.cos_AoA, self.sin_AoA),
            self.iterations,
            self.write_case_filename,
            (self.cos_AoA, self.sin_AoA, self.cd_report_filename),
            (-self.sin_AoA, self.cos_AoA, self.cl_report_filename)
        ]
        for i in range(len(tui_commands_custom_lines_index)):
            self.tui_commands[tui_commands_custom_lines_index[i]] = \
                self.tui_commands[tui_commands_custom_lines_index[i]] % custom_list[i]
            pass
        self.tui_commands_string = "\n".join(self.tui_commands)
        pass
    
    def __writeTuiCommands(self) -> None:
        with open(self.tui_commands_filename, "w", encoding="utf-8") as file:
            file.write(self.tui_commands_string)
            pass
        print("tui commands written: %s" % self.tui_commands_filename)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __run(self) -> None:
        if os.path.exists(self.cd_report_filename) and \
            os.path.exists(self.cl_report_filename):
            pass
        else:
            self.return_code = subprocess.run(self.cmd_list, cwd=self.task_folder, \
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
            pass
        print("task finished with return code: %d" % self.return_code)
        pass
    
    def __readCD(self) -> None:
        with open(self.cd_report_filename, "r", encoding="utf-8") as file:
            line: str = file.readlines()[-1]
            pass
        self.CD: float = float(line.split()[-1])
        pass
    
    def __readCL(self) -> None:
        with open(self.cl_report_filename, "r", encoding="utf-8") as file:
            line: str = file.readlines()[-1]
            pass
        self.CL: float = float(line.split()[-1])
        pass
    
    def __addToDataframe(self) -> None:
        self.dataframe.loc[len(self.dataframe)] = \
            [self.mach, self.AoA, self.CL, self.CD, self.iterations, " ".join(self.cmd_list), \
                self.task_folder, self.read_case_filename, self.write_case_filename, \
                    self.cd_report_filename, self.cl_report_filename, \
                        self.tui_commands_filename, self.return_code]
        print("mach: %.2f, AoA: %.2f, CL: %.4f, CD: %.4f" % \
            (self.mach, self.AoA, self.CL, self.CD))
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    @clock
    def autoCalculate(self) -> None:
        self.__createTaskFolder()
        self.__generateTuiCommands()
        self.__writeTuiCommands()
        self.__run()
        self.__readCD()
        self.__readCL()
        self.__addToDataframe()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    pass

print("classes: CalculationTask.py loaded")