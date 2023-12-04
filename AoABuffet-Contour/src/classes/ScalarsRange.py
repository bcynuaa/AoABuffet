'''
 # @ project: AoABuffet-PressureContour
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-10-12 20:05:39
 # @ description: scalars range class
 '''

import tqdm
import pandas as pd

import src.config.ScalarsRangeSettings as ScalarsRangeSettings
import src.config.PyvistaSettings as PyvistaSettings

from src.classes.CalculationTask import CalculationTask

class ScalarsRange:
    
    # ---------------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.buffet_aoa_df: pd.DataFrame = \
            pd.read_csv(ScalarsRangeSettings.buffet_aoa_csv_filename, index_col=None)
        self.calculation_task: CalculationTask = CalculationTask()
        self.__addColumns()
        pass
    
    def __addColumns(self) -> None:
        self.buffet_aoa_df[ScalarsRangeSettings.drag_coeff_name] = 0.00
        self.buffet_aoa_df[ScalarsRangeSettings.lift_coeff_name] = 0.00
        self.buffet_aoa_df[ScalarsRangeSettings.working_directory_name] = ""
        self.buffet_aoa_df[ScalarsRangeSettings.flow_field_file_name] = ""
        self.scalar_min_name_list: list = list()
        self.scalar_max_name_list: list = list()
        for i_scalar in range(PyvistaSettings.n_scalars):
            self.scalar_min_name_list.append( \
                PyvistaSettings.scalar_name_list[i_scalar] \
                    + ScalarsRangeSettings.scalar_min_addition)
            self.scalar_max_name_list.append( \
                PyvistaSettings.scalar_name_list[i_scalar] \
                    + ScalarsRangeSettings.scalar_max_addition)
            pass
        for i_scalar in range(PyvistaSettings.n_scalars):
            self.buffet_aoa_df[self.scalar_min_name_list[i_scalar]] = 0.00
            self.buffet_aoa_df[self.scalar_max_name_list[i_scalar]] = 0.00
            pass
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def __addCalculationTaskDataToBuffetAoADf(self, i_row: int) -> None:
        self.buffet_aoa_df.iloc[i_row, \
            self.buffet_aoa_df.columns.get_loc(ScalarsRangeSettings.drag_coeff_name)] = \
                self.calculation_task.drag_coeff
        self.buffet_aoa_df.iloc[i_row, \
            self.buffet_aoa_df.columns.get_loc(ScalarsRangeSettings.lift_coeff_name)] = \
                self.calculation_task.lift_coeff
        self.buffet_aoa_df.iloc[i_row, \
            self.buffet_aoa_df.columns.get_loc(ScalarsRangeSettings.working_directory_name)] = \
                self.calculation_task.working_directory
        self.buffet_aoa_df.iloc[i_row, \
            self.buffet_aoa_df.columns.get_loc(ScalarsRangeSettings.flow_field_file_name)] = \
                self.calculation_task.write_case_filename
        for i_scalar in range(PyvistaSettings.n_scalars):
            self.buffet_aoa_df.iloc[i_row, \
                self.buffet_aoa_df.columns.get_loc(self.scalar_min_name_list[i_scalar])] = \
                    self.calculation_task.scalar_min_array[i_scalar]
            self.buffet_aoa_df.iloc[i_row, \
                self.buffet_aoa_df.columns.get_loc(self.scalar_max_name_list[i_scalar])] = \
                    self.calculation_task.scalar_max_array[i_scalar]
            pass
        pass
    
    def __runRow(self, i_row: int) -> None:
        i_series: pd.Series = self.buffet_aoa_df.iloc[i_row, :]
        self.calculation_task.setMeshFilename(i_series[ScalarsRangeSettings.mesh_file_name])
        self.calculation_task.setMach(i_series[ScalarsRangeSettings.mach_name])
        self.calculation_task.setAttackAngle(i_series[ScalarsRangeSettings.attack_angle_name])
        self.calculation_task.autoCalculate()
        pass
    
    def __getMinAndMax(self) -> None:
        self.scalar_min_series: pd.Series = self.buffet_aoa_df[self.scalar_min_name_list].min()
        self.scalar_max_series: pd.Series = self.buffet_aoa_df[self.scalar_max_name_list].max()
        self.min_max_series: pd.Series = pd.concat( \
            [self.scalar_min_series, self.scalar_max_series])
        self.min_max_series.sort_index(inplace=True)
        pass
    
    def __savePandasData(self) -> None:
        self.buffet_aoa_df.to_csv(ScalarsRangeSettings.output_csv_filename, index=False)
        self.min_max_series.to_csv(ScalarsRangeSettings.min_max_csv_filename, index=True)
        pass
    
    def runAll(self) -> None:
        for i_row in tqdm.tqdm(range(len(self.buffet_aoa_df))):
            tqdm.tqdm.write(f"Fluent processing mesh: %s with mach: %.2f at row: %d" % \
                (self.buffet_aoa_df.iloc[i_row, \
                    self.buffet_aoa_df.columns.get_loc(ScalarsRangeSettings.mesh_file_name)], \
                        self.buffet_aoa_df.iloc[i_row, \
                            self.buffet_aoa_df.columns.get_loc(ScalarsRangeSettings.mach_name)], \
                                i_row))
            self.__runRow(i_row)
            self.__addCalculationTaskDataToBuffetAoADf(i_row)
            pass
        self.__getMinAndMax()
        self.__savePandasData()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    pass

print("classes: ScalarsRange.py loaded")