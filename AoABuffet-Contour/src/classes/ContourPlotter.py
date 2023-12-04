'''
 # @ project: AoABuffet-PressureContour
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-10-13 01:08:27
 # @ description: contour plotter class
 '''

import os
from src.config.PyvistaSettings import pyvista

import src.config.PyvistaSettings as PyvistaSettings

class ContourPlotter:
    
    # ---------------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        pass
    
    def __resetPlotter(self) -> None:
        self.plotter: pyvista.Plotter = pyvista.Plotter( \
            window_size=PyvistaSettings.plotter_window_size, \
                off_screen=PyvistaSettings.plotter_off_screen)
        pass
    
    def reset(self) -> None:
        self.__resetPlotter()
        self.working_directory: str = ""
        self.flow_field_file_name: str = ""
        self.unstructured_grid: pyvista.UnstructuredGrid = pyvista.UnstructuredGrid()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def setWorkingDirectory(self, working_directory: str) -> None:
        self.working_directory = working_directory
        pass
    
    def setFlowFieldFileName(self, flow_field_file_name: str) -> None:
        self.flow_field_file_name = flow_field_file_name
        pass
    
    def readFlowField(self) -> None:
        self.unstructured_grid = pyvista.read( \
            self.flow_field_file_name).combine().cell_data_to_point_data()
        self.unstructured_grid.points[:, 1] += PyvistaSettings.delta_x
        self.unstructured_grid.points[:, 2] += PyvistaSettings.delta_y
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    def plotScalar(self, i_scalar: int, clim: list) -> None:
        scalar_name: str = PyvistaSettings.scalar_name_list[i_scalar]
        png_filename: str = os.path.join(self.working_directory, \
            PyvistaSettings.screen_shot_filename_list[i_scalar])
        self.plotter.add_mesh(self.unstructured_grid, scalars=scalar_name, \
            show_edges=PyvistaSettings.plotter_show_edges, \
                show_scalar_bar=PyvistaSettings.plotter_show_scalar_bar, \
                    cmap=PyvistaSettings.plotter_cmap, \
                        n_colors=PyvistaSettings.plotter_n_colors, \
                            clim=clim)
        self.plotter.camera_position = PyvistaSettings.plotter_camera_position
        self.plotter.camera.zoom(PyvistaSettings.plotter_camera_zoom)
        self.plotter.show(screenshot=png_filename, auto_close=True)
        self.plotter.close()
        self.__resetPlotter()
        pass
    
    # ---------------------------------------------------------------------------------------------
    
    pass