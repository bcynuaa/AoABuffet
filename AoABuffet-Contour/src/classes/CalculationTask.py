'''
 # @ project: AoABuffet-PressureContour
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-10-11 23:43:27
 # @ description: calculation task class
 '''
 
import os
import subprocess
import numpy as np
from src.config.PyvistaSettings import pyvista

import src.config.CalculationSettings as CalculationSettings
import src.config.FluentSettings as FluentSettings
import src.config.PyvistaSettings as PyvistaSettings

class CalculationTask:
    
    # ---------------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.reset()
        pass
    
    def reset(self) -> None:
        self.mesh_filename: str = ""
        self.mach: float = 0.00
        self.attack_angle: float = 0.00
        self.iterations: int = 2500
        self.__projectAttackAngle()
        # directory or file
        self.working_directory: str = ""
        self.read_case_filename: str = ""
        self.write_case_filename: str = ""
        self.cd_report_filename: str = ""
        self.cl_report_filename: str = ""
        self.tui_commands_filename: str = ""
        # data
        self.lift_coeff: float = 0.00
        self.drag_coeff: float = 0.00
        # tui commands
        self.tui_commands_list: list = list()
        self.tui_commands_str: str = ""
        # cmd
        self.cmd_list: list = list()
        self.return_code: int = 0
        # scalar list
        self.scalar_min_array: np.ndarray = np.zeros(PyvistaSettings.n_scalars)
        self.scalar_max_array: np.ndarray = np.zeros(PyvistaSettings.n_scalars)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def setMeshFilename(self, mesh_filename: str) -> None:
        self.mesh_filename = mesh_filename
        pass
    
    def setMach(self, mach: float) -> None:
        self.mach = mach
        pass
    
    def setAttackAngle(self, attack_angle: float) -> None:
        self.attack_angle = attack_angle
        self.__projectAttackAngle()
        pass
    
    def setIterations(self, iterations: int) -> None:
        self.iterations = iterations
        pass
    
    def __projectAttackAngle(self) -> None:
        self.cos_attack_angle: float = np.cos(self.attack_angle * np.pi / 180.0)
        self.sin_attack_angle: float = np.sin(self.attack_angle * np.pi / 180.0)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __makeWorkingDirectory(self) -> None:
        self.working_directory = \
            CalculationSettings.getWorkingDirectory(self.mesh_filename, self.mach)
        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)
            pass
        pass
    
    def __getReadCaseFilename(self) -> None:
        self.read_case_filename: str = \
            CalculationSettings.getAbsPathReadCaseFilename(self.mesh_filename)
        pass
    
    def __getWriteCaseFilename(self) -> None:
        self.write_case_filename: str = \
            FluentSettings.getAbsPathWriteCaseFilename(self.working_directory)
        pass
    
    def __getCdReportFilename(self) -> None:
        self.cd_report_filename: str = \
            FluentSettings.getAbsPathCdReportFilename(self.working_directory)
        pass
    
    def __getClReportFilename(self) -> None:
        self.cl_report_filename: str = \
            FluentSettings.getAbsPathClReportFilename(self.working_directory)
        pass
    
    def __getTuiCommandsFilename(self) -> None:
        self.tui_commands_filename: str = \
            FluentSettings.getAbsPathTuiCommandsFilename(self.working_directory)
        pass
    
    def __makeCmdList(self) -> None:
        self.cmd_list = [FluentSettings.fluent_exe, \
            "-t%d" % FluentSettings.thread_number, "%dd" % FluentSettings.dim, \
                "-i", self.tui_commands_filename]
        pass
    
    def getFilename(self) -> None:
        self.__makeWorkingDirectory()
        self.__getReadCaseFilename()
        self.__getWriteCaseFilename()
        self.__getCdReportFilename()
        self.__getClReportFilename()
        self.__getTuiCommandsFilename()
        self.__makeCmdList()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def isCalculated(self) -> bool:
        return os.path.exists(self.cd_report_filename) and os.path.exists(self.cl_report_filename)
        pass
    
    def __readLiftCoeff(self) -> None:
        with open(self.cl_report_filename, "r", encoding="utf-8") as report_file:
            line: str = report_file.readlines()[-1]
            pass
        self.lift_coeff = float(line.split()[-1])
        pass
    
    def __readDragCoeff(self) -> None:
        with open(self.cd_report_filename, "r", encoding="utf-8") as report_file:
            line: str = report_file.readlines()[-1]
            pass
        self.drag_coeff = float(line.split()[-1])
        pass
    
    def __readScalars(self) -> None:
        unstructured_grid: pyvista.UnstructuredGrid = \
            pyvista.read(self.write_case_filename).combine().cell_data_to_point_data()
        for i_scalar in range(PyvistaSettings.n_scalars):
            scalar_range: tuple = unstructured_grid.get_data_range(PyvistaSettings.scalar_name_list[i_scalar])
            self.scalar_min_array[i_scalar] = scalar_range[0]
            self.scalar_max_array[i_scalar] = scalar_range[1]
            pass
        pass
    
    def readResult(self) -> None:
        if self.isCalculated() == True:
            self.__readDragCoeff()
            self.__readLiftCoeff()
            self.__readScalars()
            pass
        else:
            print("error: CalculationTask.py: readResult(): not calculated")
            pass
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __generateTuiCommands(self) -> None:
        self.tui_commands_list = FluentSettings.tui_commands_template.copy()
        custom_list: list = [
            self.read_case_filename,
            (self.mach, self.cos_attack_angle, self.sin_attack_angle),
            self.iterations,
            self.write_case_filename,
            (self.cos_attack_angle, self.sin_attack_angle, self.cd_report_filename),
            (-self.sin_attack_angle, self.cos_attack_angle, self.cl_report_filename)
        ]
        for i in range(len(FluentSettings.tui_commands_custom_lines_index)):
            self.tui_commands_list[FluentSettings.tui_commands_custom_lines_index[i]] = \
                self.tui_commands_list[ \
                    FluentSettings.tui_commands_custom_lines_index[i]] % custom_list[i]
            pass
        self.tui_commands_str = "\n".join(self.tui_commands_list)
        pass
    
    def writeTuiCommands(self) -> None:
        self.__generateTuiCommands()
        with open(self.tui_commands_filename, "w", encoding="utf-8") as tui_commands_file:
            tui_commands_file.write(self.tui_commands_str)
            pass
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def run(self) -> None:
        self.return_code: int = subprocess.run(self.cmd_list, cwd=self.working_directory, \
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
        pass
    
    def autoCalculate(self) -> None:
        self.getFilename()
        if self.isCalculated() == False:
            self.writeTuiCommands()
            self.run()
            pass
        self.readResult()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    pass

print("classes: CalculationTask.py loaded")