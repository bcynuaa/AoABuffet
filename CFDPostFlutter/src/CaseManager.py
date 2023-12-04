'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-06-30 15:12:56
 # @ Description: the case manager
 '''

import os
import json
import shutil
from cfdpost.cfdresult import cfl3d

from src.Utils import runExecutableFile

class CaseManager:
    
    # ---------------------------------------------------------------------------------------------
    
    def __init__(self, json_filename: str) -> None:
        try:
            self.__initialize(json_filename)
            pass
        except:
            print("Error: CaseManager.__initialize() failed, please check the json file.")
            pass
        pass
    
    def __initialize(self, json_filename) -> None:
        json_data: dict = json.load(open(json_filename, 'r'))
        self.__initializeCFL3DDirectory(json_data)
        self.__initializeWorkingDirectory(json_data)
        self.__initializeWorkingCondition(json_data)
        self.__initializeAirfoilGeometryAndGrid(json_data)
        self.__initializeInpFileConfig(json_data)
        # save the json filename
        self.json_filename: str = json_filename
        # initialize the current variables
        self.__initializeCurrentVariables()
        pass
    
    def __initializeCFL3DDirectory(self, json_data: dict) -> None:
        cfl3d_directory: str = "cfl3d directory"
        self.cfl3d_directory: str = json_data[cfl3d_directory]["value"]
        self.cfl3d_Seq_exe_filename: str = json_data[cfl3d_directory]["exe filename"]
        self.cfl3d_inp_filename: str = json_data[cfl3d_directory]["inp filename"]
        self.cfl3d_x_filename: str = json_data[cfl3d_directory]["x filename"]
        self.cfl3d_Sep_exe_pure_filename: str = self.cfl3d_Seq_exe_filename
        self.cfl3d_inp_pure_filename: str = self.cfl3d_inp_filename
        self.__joinCFL3DPath()
        pass
    
    def __initializeWorkingDirectory(self, json_data: dict) -> None:
        working_directory: str = "working directory"
        self.working_directory: str = json_data[working_directory]["value"]
        self.folder_digits: int = json_data[working_directory]["folder digits"]
        self.folder_name: str = json_data[working_directory]["folder name"]
        self.folder_pattern: str = self.folder_name + "%0." + str(self.folder_digits) + "f"
        pass
    
    def __initializeWorkingCondition(self, json_data: dict) -> None:
        working_condition: str = "working condition"
        self.CL_cruise: float = json_data[working_condition]["CL_cruise"]
        self.AoA_min: float = json_data[working_condition]["AoA_min"]
        self.AoA_max: float = json_data[working_condition]["AoA_max"]
        self.dAoA: list = json_data[working_condition]["dAoA"]
        self.Minf: float = json_data[working_condition]["Minf"]
        self.Re: float = json_data[working_condition]["Re"]
        self.t_max: float = json_data[working_condition]["t_max"]
        pass
    
    def __initializeAirfoilGeometryAndGrid(self, json_data: dict) -> None:
        airfoil_geometry_and_grid: str = "airfoil geometry and grid"
        self.nn: int = json_data[airfoil_geometry_and_grid]["nn"]
        self.n_cst: int = json_data[airfoil_geometry_and_grid]["n_cst"]
        self.j0: int = json_data[airfoil_geometry_and_grid]["j0"]
        self.j1: int = json_data[airfoil_geometry_and_grid]["j1"]
        self.G_Tail: int = json_data[airfoil_geometry_and_grid]["G_Tail"]
        pass
    
    def __initializeInpFileConfig(self, json_data: dict) -> None:
        cfl3d_inp_file_config: str = "cfl3d inp file config"
        self.file_digits: int = json_data[cfl3d_inp_file_config]["file digits"]
        self.inp_header: str = json_data[cfl3d_inp_file_config]["inp header"]
        self.io_files_needed: list = json_data[cfl3d_inp_file_config]["io files needed"]
        self.before_cltarg: str = json_data[cfl3d_inp_file_config]["before cltarg"]
        self.cltarg: str = json_data[cfl3d_inp_file_config]["cltarg"]
        self.after_cltarg: str = json_data[cfl3d_inp_file_config]["after cltarg"]
        self.inp_file_comment: str = json_data[cfl3d_inp_file_config]["inp file comment"]
        self.inp_config_vars_header: str = \
            json_data[cfl3d_inp_file_config]["inp config vars header"]
        self.inp_shared_things_from_line: int = \
            json_data[cfl3d_inp_file_config]["shared things in inp file from this line number"]
        self.cltarg_pattern: str = self.cltarg + "%0." + str(self.file_digits) + "f\n"
        with open(self.cfl3d_inp_filename, 'r') as f:
            self.shared_lines_from_inp: list = f.readlines()[self.inp_shared_things_from_line-1:]
            pass
        self.io_files_needed = [io_file + "\n" for io_file in self.io_files_needed]
        self.beta: float = json_data[cfl3d_inp_file_config]["BETA"]
        self.tinf_dr: float = json_data[cfl3d_inp_file_config]["TINF,DR"]
        self.ialph: int = json_data[cfl3d_inp_file_config]["IALPH"]
        self.ihstry: int = json_data[cfl3d_inp_file_config]["IHSTRY"]
        self.delim: str = json_data[cfl3d_inp_file_config]["delim"]
        form: str = "%0." + str(self.file_digits) + "f"
        inp_vars_list: list = [self.delim+form, self.delim+form, self.delim+str(self.beta), \
            self.delim+form, self.delim+str(self.tinf_dr), self.delim+str(self.ialph), \
                self.delim+str(self.ihstry), " \n"]
        self.inp_vars_pattern: str = "".join(inp_vars_list)
        pass
    
    def __joinCFL3DPath(self) -> None:
        self.cfl3d_Seq_exe_filename = os.path.join( \
            self.cfl3d_directory, self.cfl3d_Seq_exe_filename)
        self.cfl3d_inp_filename = os.path.join(self.cfl3d_directory, self.cfl3d_inp_filename)
        self.cfl3d_x_filename = os.path.join(self.cfl3d_directory, self.cfl3d_x_filename)
        pass
    
    def __initializeCurrentVariables(self) -> None:
        self.current_AoA: float = self.AoA_min
        self.current_data_folder: str = self.__currentDataFolder()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __currentDataFolder(self) -> str:
        return os.path.join(self.working_directory, self.folder_pattern % self.current_AoA)
        pass
    
    def __assureDataFolder(self) -> None:
        if os.path.exists(self.current_data_folder) == False:
            os.mkdir(self.current_data_folder)
        pass
    
    def __makeCurrentInpFile(self, use_CL_cruise: bool = False) -> None:
        inp_vars_line: str = self.inp_vars_pattern % (self.Minf, self.current_AoA, self.Re)
        if use_CL_cruise == False:
            cltarg: list = []
            pass
        else:
            cltarg: list = \
                [self.before_cltarg, self.cltarg_pattern % self.CL_cruise, self.after_cltarg]
            pass
        inp_config_lines_list: list = [self.inp_header] + self.io_files_needed + cltarg + \
            [self.inp_file_comment, self.inp_config_vars_header, inp_vars_line] + \
                self.shared_lines_from_inp
        inp_config: str = "".join(inp_config_lines_list)
        inp_config_filename: str = os.path.join( \
            self.current_data_folder, self.cfl3d_inp_pure_filename)
        with open(inp_config_filename, 'w') as config_file:
            config_file.write(inp_config)
            pass
        pass
    
    def __runCFL3DEXE(self) -> None:
        executable_filename: str = os.path.join( \
            self.current_data_folder, self.cfl3d_Sep_exe_pure_filename)
        runExecutableFile(executable_filename)
        pass
    
    def __checkCalculationOutput(self) -> None:
        succeed, Minf, _, Re, _ = cfl3d.readinput(self.current_data_folder)
        print(succeed, Minf, Re)
        if Minf != self.Minf or Re != self.Re:
            raise Exception("Error: Minf or Re is not correct.")
            pass
        converge_flag, CL, CD, Cm, CDp, CDf, errs = cfl3d.readCoef( \
            self.current_data_folder, n=100, output_error=True)
        succeed_flag, AoA, err = cfl3d.readAoA(self.current_data_folder, output_error=True)
        if succeed_flag == True:
            self.current_AoA = AoA
            err = 0.0
            pass
        errs += [err]
        print(converge_flag, CL, CD, Cm, CDp, CDf, errs)
        pass
    
    def __extractFeature(self) -> None:
        
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __copyCFL3DFilesToCurrentDataFolder(self) -> None:
        shutil.copy(self.cfl3d_Seq_exe_filename, self.current_data_folder)
        shutil.copy(self.cfl3d_x_filename, self.current_data_folder)
        pass
    
    def calculateCurrentAoA(self) -> None:
        self.current_data_folder: str = self.__currentDataFolder()
        self.__assureDataFolder()
        self.__copyCFL3DFilesToCurrentDataFolder()
        self.__makeCurrentInpFile()
        print("begin this calculation")
        self.__runCFL3DEXE()
        print("finish this calculation")
        self.__checkCalculationOutput()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    pass