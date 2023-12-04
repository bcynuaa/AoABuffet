'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-04 16:52:36
 # @ Description: contains the calculation task class
 '''

import shutil
import numpy as np
import pandas as pd
from cfdpost.cfdresult import cfl3d
from cfdpost.section.physical import PhysicalSec

from src.config.Cfl3d import exe_path, exe_filename, exe_pure_filename, inp_filename
from src.config.InpFileSettings import *
from src.config.CalculationSettings import *
from src.config.Meshes import j0, j1

from src.utils.Path import assurePath, getPureFilename
from src.utils.RunExe import runExecutableFile
from src.utils.Decorator import clock

def numberListToStringList(number_list: list) -> None:
    for i in range(len(number_list)):
        if isinstance(number_list[i], int):
            number_list[i] = str(number_list[i])
            pass
        else:
            number_list[i] = number_format % number_list[i]
            pass
        pass
    pass

class CalculationTask:
    
    # ---------------------------------------------------------------------------------------------
    
    def __init__(self, mesh_filename: str, Minf: float) -> None:
        self.mesh_filename: str = mesh_filename
        self.Minf: float = Minf
        pass
    
    def setTask(self, AoA: float, dt: float = default_dt, CL: float = np.nan) -> None:
        self.AoA: float = AoA
        self.dt: float = dt
        self.CL: float = CL
        self.dataframe: pd.DataFrame = pd.DataFrame(columns=dataframe_columns)
        self.__createTaskFolder()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __createTaskFolder(self) -> None:
        mesh_info: str = getPureFilename(self.mesh_filename)
        Minf_info: str = folder_number_format % self.Minf
        AoA_info: str = folder_number_format % self.AoA
        self.task_folder: str = os.path.join(calculation_data_path, \
            mesh_info, connection_character.join([Minf_folder_hint, Minf_info]), \
                    connection_character.join([AoA_folder_hint, AoA_info]))
        assurePath(self.task_folder)
        print("Task folder created: %s" % self.task_folder)
        pass
    
    def __backupFilesFromExePath(self) -> None:
        files_list: list = os.listdir(exe_path)
        if exe_pure_filename in files_list:
            files_list.remove(exe_pure_filename)
            pass
        for file in files_list:
            shutil.copy(os.path.join(exe_path, file), self.task_folder)
            pass
        print("Files copied from exe path to task folder: %s" % self.task_folder)
        pass
    
    # ! this function is copied from origin writer's code
    # ! i didn't check the package `cfl3d` to see its function
    # ! i'm not responsible for this function
    def __extractFeatures(self) -> None:
        # * Load plot3d format results
        xy, qq, mach, alfa, reyn = cfl3d.readPlot2d(self.task_folder, binary=True)
        X = xy[: ,: ,0]
        Y = xy[: ,: ,1]
        # * Calculate fluid properties
        data = cfl3d.analysePlot3d(mach, qq, iVar=[2 ,3 ,7 ,11])
        U = data[: ,: ,0]         # U [ni,nj]
        V = data[: ,: ,1]         # V [ni,nj]
        T = data[: ,: ,2]         # T [ni,nj]
        Cp =  data[: ,: ,3]       # Cp[ni,nj]
        # * Extract wall data and boundary layer properties
        x  = cfl3d.foildata(X, j0, j1)  # x [j1-j0]
        y  = cfl3d.foildata(Y, j0, j1)  # y [j1-j0]
        cp = cfl3d.foildata(Cp, j0, j1)  # cp[j1-j0]
        Hi, Hc, info = PhysicalSec.getHi(X, Y, U, V, T, j0=j0, j1=j1, nHi=40, neglect_error=True)
        (Tw, dudy) = info               # Tw[j1-j0], dudy[j1-j0]
        self.flow_field: PhysicalSec = PhysicalSec(mach, alfa, reyn)
        self.flow_field.setdata(x, y, cp, Tw, Hi, Hc, dudy)
        self.flow_field.extract_features()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def makeInpString(self) -> None:
        inp_lines: list = []
        inp_lines += [header]
        inp_lines += [self.mesh_filename]
        
        io_files: list = \
            [os.path.join(self.task_folder, io_file) for io_file in io_files_needed]
        inp_lines += io_files
        
        if np.isnan(self.CL) == False:
            inp_lines += [cltarg_lines["line before"]]
            inp_lines += [cltarg_lines["line"] + number_format % self.CL]
            inp_lines += [cltarg_lines["line after"]]
            pass
        
        inp_lines += [setup_comment]
        
        inp_lines += [condition_data[title_line]]
        condition_data_dict: dict = condition_data[default_values].copy()
        condition_data_dict["XMACH"] = self.Minf
        condition_data_dict["ALPHA"] = self.AoA
        condition_data_list: list = list(condition_data_dict.values())
        numberListToStringList(condition_data_list)
        condition_data_list = [delimiter] + condition_data_list
        inp_lines += [delimiter.join(condition_data_list)]
        
        inp_lines += [reference_data[title_line]]
        reference_data_list: list = list(reference_data[default_values].values())
        numberListToStringList(reference_data_list)
        reference_data_list = [delimiter] + reference_data_list
        inp_lines += [delimiter.join(reference_data_list)]
        
        inp_lines += [cycling_data[title_line]]
        cycling_data_dict: dict = cycling_data[default_values].copy()
        cycling_data_dict["DT"] = self.dt
        cycling_data_list: list = list(cycling_data_dict.values())
        numberListToStringList(cycling_data_list)
        cycling_data_list = [delimiter] + cycling_data_list
        inp_lines += [delimiter.join(cycling_data_list)]
        
        inp_lines += shared_lines
        self.inp_lines: list = inp_lines
        self.inp_string: str = line_break.join(inp_lines)
        pass
    
    def writeInpFile(self) -> None:
        with open(inp_filename, 'w') as inp_file:
            inp_file.write(self.inp_string)
            pass
        print("Inp file overwritten: %s" % inp_filename)
        pass
    
    def run(self) -> None:
        print("Running calculation task for \nmesh: %s, Minf: %f, AoA: %f, dt: %f" % \
            (self.mesh_filename, self.Minf, self.AoA, self.dt))
        runExecutableFile(exe_filename)
        self.__backupFilesFromExePath() # backup files from exe path
        print("Calculation task finished")
        pass
    
    def readResults(self) -> None:
        _, Minf, _, _, _ = cfl3d.readinput(self.task_folder)
        if self.Minf != Minf:
            print("Error: Minf not match")
            pass
        converge, CL, CD, Cm, CDp, CDf, errs = cfl3d.readCoef( \
            self.task_folder, n=100, output_error=True)
        success_AoA, AoA_output, err = cfl3d.readAoA(self.task_folder, n=100, output_error=True)
        # ? actrually i have no idea why the AoA_output is not the same as self.AoA
        # ? but the origin code's writer did this
        # ? thus i will record it in the dataframe
        if success_AoA == True:
            err = 0.0
            pass
        errs += [err]
        self.__extractFeatures()
        dudy_min: float = self.flow_field.getValue("mUy","dudy")
        # generate a new row of dataframe
        # ! the order of the columns is important
        # ! if you change the order, you should change the order in the dataframe_columns
        # ! converge is a bool value, so its conversion to str is encouraged
        self.dataframe.loc[self.dataframe.shape[0]] = \
            [getPureFilename(self.mesh_filename), \
                self.Minf, self.AoA, self.dt, self.CL, \
                    str(converge), CL, CD, Cm, CDp, CDf, AoA_output, dudy_min] \
                        + errs + [self.task_folder]
        print("Converge: %s" % str(converge))
        print("Results readed")
        pass
    
    @clock
    def autoCalculate(self) -> None:
        self.makeInpString()
        self.writeInpFile()
        self.run()
        self.readResults()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    pass

print("classes: CalculationTask imported")