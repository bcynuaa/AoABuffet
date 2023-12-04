'''
 # @ project: AoABuffet-FluentBackend
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-07-19 20:16:52
 # @ description: AoAFinder class
 '''

import os
import numpy as np
import pandas as pd
import scipy.interpolate as interpolate
import matplotlib.pyplot as plt

from src.config.FluentSettings import *
from src.config.CalculationSettings import *
from src.config.AoAFinderSettings import *

from src.utils.Path import *

from src.decorator.Clock import clock

from src.classes.CalculationTask import CalculationTask

class AoAFinder:
    
    # ---------------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.mesh_filename: str = ""
        self.mach: float = 0.0
        self.working_directory: str = ""
        self.Clalphha0: float = 0.0
        self.calculation_task: CalculationTask = CalculationTask()
        self.dataframe: pd.DataFrame = pd.DataFrame(columns=aoa_finder_dataframe_columns)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __createWorkingDirectory(self) -> None:
        self.working_directory = os.path.join(calculation_data_path, \
            getPureFilename(self.mesh_filename))
        assurePathExists(self.working_directory)
        pass
    
    def setMeshFilename(self, mesh_filename: str) -> None:
        self.mesh_filename = os.path.abspath(mesh_filename)
        self.__createWorkingDirectory()
        pass
    
    def setMach(self, mach: float) -> None:
        self.mach = mach
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def runCalculationTask(self, \
        read_case_filename: str, AoA : float, iterations: int = 2500) -> None:
        self.calculation_task.setWorkingDirectory(self.working_directory)
        self.calculation_task.setMach(self.mach)
        self.calculation_task.setReadCaseFilename(read_case_filename)
        self.calculation_task.setAoA(AoA)
        self.calculation_task.setIterations(iterations)
        self.calculation_task.autoCalculate()
        self.dataframe = pd.concat( \
            [self.dataframe, self.calculation_task.dataframe], ignore_index=True)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __filterDataFrame(self) -> None:
        # drop duplicated AoA
        self.dataframe.drop_duplicates(subset=["AoA"], keep="first", inplace=True)
        # sort by AoA
        self.dataframe.sort_values(by=["AoA"], inplace=True)
        pass
    
    def __getAoACLArray(self) -> tuple:
        self.__filterDataFrame()
        AoA_array: np.ndarray = self.dataframe["AoA"].to_numpy()
        CL_array: np.ndarray = self.dataframe["CL"].to_numpy()
        return (AoA_array, CL_array)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    @clock
    def calculateClalpha0(self) -> None:
        for AoA in Clalpha0_sample_points:
            self.runCalculationTask(self.mesh_filename, AoA)
            pass
        AoA_array, CL_array = self.__getAoACLArray()
        self.Clalphha0 = np.polyfit(AoA_array, CL_array, 1)[0]
        print("Clalpha0: %.4f" % self.Clalphha0)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __calculateClalpha(self) -> float:
        AoA_array, CL_array = self.__getAoACLArray()
        Clalpha_array: np.ndarray = np.gradient(CL_array, AoA_array)
        self.dataframe["Clalpha"] = Clalpha_array
        pass
    
    @clock
    def locateWhereBuffet(self) -> None:
        current_AoA: float = where_buffet_AoA_begin
        delta_AoA: float = where_buffet_delta_AoA
        self.__calculateClalpha()
        current_min_Clalpha: float = self.dataframe["Clalpha"].min()
        while current_min_Clalpha > self.Clalphha0 - Clalpha_shift:
            self.runCalculationTask(self.mesh_filename, current_AoA)
            self.__calculateClalpha()
            current_min_Clalpha = self.dataframe["Clalpha"].min()
            current_AoA += delta_AoA
            print("Clalpha0: %.4f" % self.Clalphha0)
            print("current min Clalpha: %.4f" % current_min_Clalpha)
            pass
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __cloestAoA(self) -> tuple:
        df: pd.DataFrame = self.dataframe.copy()
        df["Clalpha err"] = df["Clalpha"] - (self.Clalphha0 - Clalpha_shift)
        AoA_lhs: float = df[df["Clalpha err"] > 0]["AoA"].max()
        AoA_rhs: float = df[df["Clalpha err"] < 0]["AoA"].min()
        return (AoA_lhs, AoA_rhs)
        pass
    
    @clock
    def refineWhereBuffet(self) -> None:
        AoA_lhs, AoA_rhs = self.__cloestAoA()
        while np.abs(AoA_lhs - AoA_rhs) > tolerance:
            print("AoA lhs: %.4f, AoA rhs: %.4f" % (AoA_lhs, AoA_rhs))
            self.runCalculationTask(self.mesh_filename, (AoA_lhs+AoA_rhs)/2)
            self.__calculateClalpha()
            AoA_lhs, AoA_rhs = self.__cloestAoA()
            pass
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def interpolate(self) -> None:
        self.function_AoA_to_CL: interpolate.CubicSpline = \
            interpolate.CubicSpline(self.dataframe["AoA"], self.dataframe["CL"], \
                bc_type="natural", extrapolate=True)
        self.function_AoA_to_Clalpha: interpolate.CubicSpline = \
            interpolate.CubicSpline(self.dataframe["AoA"], self.dataframe["Clalpha"], \
                bc_type="natural", extrapolate=True)
        self.AoA_interpolate: np.array = np.linspace( \
            self.dataframe["AoA"].min(), self.dataframe["AoA"].max(), \
                interpolation_sample_number)
        self.CL_interpolate: np.array = self.function_AoA_to_CL(self.AoA_interpolate)
        self.Clalpha_interpolate: np.array = self.function_AoA_to_Clalpha(self.AoA_interpolate)
        pass
    
    def getAoABuffet(self) -> float:
        err: np.ndarray = np.abs(self.Clalpha_interpolate - (self.Clalphha0 - Clalpha_shift))
        self.buffet_index: int = np.argmin(err)
        self.AoA_buffet: float = self.AoA_interpolate[self.buffet_index]
        self.CL_buffet: float = self.CL_interpolate[self.buffet_index]
        self.Clalpha_buffet: float = self.Clalpha_interpolate[self.buffet_index]
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    @clock
    def autoCalculate(self) -> None:
        self.calculateClalpha0()
        self.locateWhereBuffet()
        self.refineWhereBuffet()
        self.interpolate()
        self.getAoABuffet()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def drawAoACL(self) -> None:
        self.figure_AoACL: plt.Figure = plt.figure(figsize=(8, 4), dpi=100, facecolor="white")
        self.axes_AoACL: plt.Axes = self.figure_AoACL.add_subplot(111)
        self.axes_AoACL.plot(self.AoA_interpolate, self.CL_interpolate, \
            label="interpolate", color="blue", linewidth=1.0, linestyle="-")
        self.axes_AoACL.scatter(self.dataframe["AoA"], self.dataframe["CL"], \
            label="data", color="red", s=20, zorder=5)
        self.axes_AoACL.scatter(self.AoA_buffet, self.CL_buffet, \
            label="buffet", color="green", s=100, zorder=20, alpha=0.5)
        self.axes_AoACL.set_xlabel("AoA", fontsize=15)
        self.axes_AoACL.set_ylabel("CL", fontsize=15)
        self.axes_AoACL.set_title("AoA-CL", fontsize=20)
        self.axes_AoACL.legend(loc="best", fontsize=10)
        self.axes_AoACL.text(1.1*self.AoA_buffet, 0.9*self.CL_buffet, \
            "AoA: %.4f\nCL: %.4f" % (self.AoA_buffet, self.CL_buffet), \
                fontsize=10, horizontalalignment="center", verticalalignment="center")
        pass
    
    def drawAoAClalpha(self) -> None:
        self.figure_AoAClalpha: plt.Figure = plt.figure(figsize=(8, 4), dpi=100, facecolor="white")
        self.axes_AoAClalpha: plt.Axes = self.figure_AoAClalpha.add_subplot(111)
        self.axes_AoAClalpha.plot(self.AoA_interpolate, self.Clalpha_interpolate, \
            label="interpolate", color="blue", linewidth=1.0, linestyle="-")
        self.axes_AoAClalpha.scatter(self.dataframe["AoA"], self.dataframe["Clalpha"], \
            label="data", color="red", s=20, zorder=5)
        self.axes_AoAClalpha.scatter(self.AoA_buffet, self.Clalpha_buffet, \
            label="buffet", color="green", s=100, zorder=20, alpha=0.5)
        self.axes_AoAClalpha.hlines(self.Clalphha0, \
            self.dataframe["AoA"].min(), self.dataframe["AoA"].max(), \
                colors="black", linestyles="dashed", \
                    linewidth=0.5, label="Clalpha0=%.4f" % self.Clalphha0)
        self.axes_AoAClalpha.hlines(self.Clalphha0 - Clalpha_shift, \
            self.dataframe["AoA"].min(), self.dataframe["AoA"].max(), \
                colors="black", linestyles="dashed", \
                    linewidth=0.5, label="Clalpha0-%.2f" % Clalpha_shift)
        self.axes_AoAClalpha.set_xlabel("AoA", fontsize=15)
        self.axes_AoAClalpha.set_ylabel("Clalpha", fontsize=15)
        self.axes_AoAClalpha.set_title("AoA-Clalpha", fontsize=20)
        self.axes_AoAClalpha.legend(loc="best", fontsize=10)
        self.axes_AoAClalpha.text(0.9*self.AoA_buffet, 0.85*self.Clalpha_buffet, \
            "AoA: %.4f\nClalpha: %.4f" % (self.AoA_buffet, self.Clalpha_buffet), \
                fontsize=10, horizontalalignment="center", verticalalignment="center")
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    pass

print("classes: AoAFinder.py loaded")