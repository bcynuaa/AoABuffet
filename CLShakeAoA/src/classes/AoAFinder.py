'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-05 19:48:15
 # @ Description: contains the AoA finder class
 '''

import numpy as np
import pandas as pd
from scipy import interpolate

from src.config.CalculationSettings import dataframe_columns
from src.config.InpFileSettings import default_dt
from src.config.AoAFinderSettings import *

from src.utils.Decorator import clock

from src.classes.CalculationTask import CalculationTask

class AoAFinder:
    
    # ---------------------------------------------------------------------------------------------
    
    def __init__(self, mesh_filename: str, Minf: float) -> None:
        self.mesh_filename: str = mesh_filename
        self.Minf: float = Minf
        self.AoA_begin: float = AoA_begin
        self.calculation_task: CalculationTask = CalculationTask(mesh_filename, Minf)
        self.dataframe: pd.DataFrame = pd.DataFrame(columns=dataframe_columns)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def runTask(self, AoA: float, dt: float = default_dt, CL: float = np.nan) -> None:
        self.calculation_task.setTask(AoA, dt, CL)
        self.calculation_task.autoCalculate()
        self.dataframe = pd.concat( \
            [self.dataframe, self.calculation_task.dataframe], ignore_index=True)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __findAoAConvergeBound(self) -> tuple:
        AoA_converge_max: float = \
            self.dataframe[self.dataframe["converge"] == "True"]["AoA"].max()
        AoA_not_converge_min: float = \
            self.dataframe[self.dataframe["converge"] == "False"]["AoA"].min()
        return AoA_converge_max, AoA_not_converge_min
        pass
    
    def __assureConvergeDivergeBothExist(self) -> None:
        self.runTask(converge_AoA_begin)
        self.runTask(converge_AoA_end)
        AoA_converge_max, AoA_not_converge_min = self.__findAoAConvergeBound()
        if np.isnan(AoA_converge_max) == False and np.isnan(AoA_not_converge_min) == False:
            return
            pass
        if np.isnan(AoA_converge_max) == True:
            while np.isnan(AoA_converge_max) == True:
                AoA_converge_max: float = self.dataframe["AoA"].min() \
                    - converge_extend_percentage * \
                        (self.dataframe["AoA"].max() - self.dataframe["AoA"].min())
                self.runTask(AoA_converge_max)
                AoA_converge_max, AoA_not_converge_min = self.__findAoAConvergeBound()
                pass
            pass
        if np.isnan(AoA_not_converge_min) == True:
            while np.isnan(AoA_not_converge_min) == True:
                AoA_not_converge_min: float = self.dataframe["AoA"].max() \
                    + converge_extend_percentage * \
                        (self.dataframe["AoA"].max() - self.dataframe["AoA"].min())
                self.runTask(AoA_not_converge_min)
                AoA_converge_max, AoA_not_converge_min = self.__findAoAConvergeBound()
                pass
            pass
        pass
    
    @clock
    def findConvergeAoA(self) -> None:   
        self.__assureConvergeDivergeBothExist()   
        AoA_converge_max, AoA_not_converge_min = self.__findAoAConvergeBound()
        while AoA_not_converge_min - AoA_converge_max > converge_tolerance:
            delta_AoA: float = (AoA_not_converge_min - AoA_converge_max) / converge_devide
            for i in range(1, converge_devide):
                self.runTask(AoA_converge_max + delta_AoA * i)
                pass
            AoA_converge_max, AoA_not_converge_min = self.__findAoAConvergeBound()
            pass
        self.dataframe.sort_values(by="AoA", inplace=True, ignore_index=True)
        self.AoA_end: float = self.dataframe[self.dataframe["converge"] == "True"]["AoA"].max()
        self.AoA_begin: float = min( \
            self.dataframe[self.dataframe["converge"] == "True"]["AoA"].min(), self.AoA_begin)
        self.AoA_span: float = self.AoA_end - self.AoA_begin
        # issue found in 013-t012-0.76
        if self.AoA_span < converge_min_AoA_span:
            self.AoA_begin = self.AoA_begin - converge_min_AoA_span
            self.AoA_span = self.AoA_end - self.AoA_begin
            pass
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __haveDataInAoASpan(self, AoA1: float, AoA2: float) -> bool:
        # check whether self.dataframe has data in AoA span [AoA1, AoA2)
        lager_than_AoA1: pd.DataFrame = self.dataframe[self.dataframe["AoA"] >= AoA1]
        smaller_than_AoA2: pd.DataFrame = lager_than_AoA1[lager_than_AoA1["AoA"] < AoA2]
        return smaller_than_AoA2.empty == False
        pass
    
    def __refinePart(self, AoA_first: float, AoA_last: float, sample_number: int) -> None:
        delta_AoA: float = (AoA_last - AoA_first) / (sample_number-1)
        for i in range(sample_number):
            if self.__haveDataInAoASpan(AoA_first + delta_AoA * i, AoA_first + delta_AoA * (i+1)):
                continue
                pass
            else:
                self.runTask(AoA_first + delta_AoA * i)
                pass
            pass
        pass
    
    def __refineLinearPart(self) -> None:
        AoA_first: float = self.AoA_begin
        AoA_last: float = self.AoA_begin + self.AoA_span * linear_percentage
        self.__refinePart(AoA_first, AoA_last, linear_sample_number)
        pass
    
    def __refineFluctuatePart(self) -> None:
        AoA_first: float = self.AoA_begin + self.AoA_span * linear_percentage
        AoA_last: float = self.AoA_begin + \
            self.AoA_span * (linear_percentage + fluctuate_percentage)
        self.__refinePart(AoA_first, AoA_last, fluctuate_sample_number)
        pass
    
    def __refineDivergePart(self) -> None:
        AoA_first: float = self.AoA_begin + \
            self.AoA_span * (linear_percentage + fluctuate_percentage)
        AoA_last: float = self.AoA_end
        self.__refinePart(AoA_first, AoA_last, diverge_sample_number)
        pass
    
    @clock
    def refineAoA(self) -> None:
        self.__refineLinearPart()
        self.__refineFluctuatePart()
        self.__refineDivergePart()
        self.dataframe.sort_values(by="AoA", inplace=True, ignore_index=True)
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __filterConverge(self) -> None:
        df_converge: pd.DataFrame = self.dataframe[self.dataframe["converge"] == "True"]
        # remove repeated "AoA"
        df_converge.drop_duplicates(subset="AoA", keep="first", inplace=True)
        self.AoA_converge: np.ndarray = df_converge["AoA"].to_numpy(copy=True)
        self.CL_converge: np.ndarray = df_converge["CL"].to_numpy(copy=True)
        self.dudy_min_converge: np.ndarray = df_converge["dudy min"].to_numpy(copy=True)
        self.CLalpha_converge: np.ndarray = np.gradient(self.CL_converge, self.AoA_converge)
        pass
    
    def __linearFitForCLalpha0(self) -> None:
        AoA_linear: np.ndarray = self.AoA_converge[ \
            CLalpha0_first_AoA_index: CLalpha0_first_AoA_index + CLalpha0_sample_number]
        CL_linear: np.ndarray = self.CL_converge[ \
            CLalpha0_first_AoA_index: CLalpha0_first_AoA_index + CLalpha0_sample_number]
        self.CLalpha0: float = np.polyfit(AoA_linear, CL_linear, 1)[0]
        pass
    
    def __interpolateCLAoA(self) -> None:
        # ref:
        # https://docs.scipy.org/doc/scipy/tutorial/interpolate/1D.html#piecewise-linear-interpolation
        # have overshot, PchipInterpolator is encouraged
        # but i think cubic spline also works well so i just '#' it
        # self.function_CL_AoA: interpolate.CubicSpline = \
        #     interpolate.CubicSpline(self.AoA_converge, self.CL_converge)
        self.function_CL_AoA: interpolate.PchipInterpolator = \
            interpolate.PchipInterpolator(self.AoA_converge, self.CL_converge)
        self.AoA_interpolation: np.ndarray = np.linspace( \
            self.AoA_begin, self.AoA_end, interpolation_sample_number)
        self.CL_interpolation: np.ndarray = self.function_CL_AoA(self.AoA_interpolation)
        self.CLalpha_interpolation: np.ndarray = self.function_CL_AoA(self.AoA_interpolation, nu=1)
        pass
    
    @clock
    def findAoABuffet(self) -> None:
        self.__filterConverge()
        self.__linearFitForCLalpha0()
        self.__interpolateCLAoA()
        CLalpha_shift_abs: np.ndarray = np.abs( \
            self.CLalpha_interpolation - (self.CLalpha0 - CLalpha_shift_buffet))
        CLalpha_shift_abs_max: float = CLalpha_shift_abs.max()
        len_CLalpha_shift_abs: int = CLalpha_shift_abs.shape[0]
        # for example when CLalpha_AoA_span_percentage = 0.2
        # only 0.8 to 1.0 of the CLalpha_shift_abs_max is considered
        index_ignore: int = int(len_CLalpha_shift_abs * (1 - CLalpha_AoA_span_percentage))
        CLalpha_shift_abs[0: index_ignore] = CLalpha_shift_abs_max
        self.AoA_buffet_index: int = np.argmin(CLalpha_shift_abs)
        self.AoA_buffet: float = self.AoA_interpolation[self.AoA_buffet_index]
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    pass

print("classes: AoAFinder.py is imported.")