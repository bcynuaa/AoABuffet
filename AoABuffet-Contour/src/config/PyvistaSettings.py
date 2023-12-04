'''
 # @ project: AoABuffet-PressureContour
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-10-12 16:16:19
 # @ description: pyvista settings
 '''

import json
import pyvista

pyvista_settings_json_filename: str = "config//pyvista_settings.json"
pyvista_settings_json_data: dict = \
    json.load(open(pyvista_settings_json_filename, "r", encoding="utf-8"))
    
plot_theme: str = pyvista_settings_json_data["plot theme"]
pyvista.set_plot_theme(plot_theme)

plotter_window_size: list = pyvista_settings_json_data["plotter"]["window size"]
plotter_off_screen: bool = pyvista_settings_json_data["plotter"]["off screen"]
plotter_show_edges: bool = pyvista_settings_json_data["plotter"]["show edges"]
plotter_show_scalar_bar: bool = pyvista_settings_json_data["plotter"]["show scalar bar"]
plotter_cmap: str = pyvista_settings_json_data["plotter"]["cmap"]
plotter_n_colors: int = pyvista_settings_json_data["plotter"]["n colors"]
plotter_camera_position: list = pyvista_settings_json_data["plotter"]["camera position"]
plotter_camera_zoom: float = pyvista_settings_json_data["plotter"]["camera zoom"]

scalar_name_list: list = pyvista_settings_json_data["scalar name list"]
n_scalars: int = len(scalar_name_list)
screen_shot_filename_list: list = pyvista_settings_json_data["screen shot filename list"]

delta_x: float = pyvista_settings_json_data["delta x"]
delta_y: float = pyvista_settings_json_data["delta y"]

print("config: PyvistaSettings.py loaded")