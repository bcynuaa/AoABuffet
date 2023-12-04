'''
 # @ project: AoABuffet-PressureContour
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-10-13 01:24:56
 # @ description: main entry
 '''

import tqdm

import src.config.ScalarsRangeSettings as ScalarsRangeSettings
import src.config.PyvistaSettings as PyvistaSettings

from src.classes.ScalarsRange import ScalarsRange
from src.classes.ContourPlotter import ContourPlotter

def main() -> None:
    scalar_range: ScalarsRange = ScalarsRange()
    contour_plotter: ContourPlotter = ContourPlotter()
    scalar_range.runAll()
    for i_row in tqdm.tqdm(range(scalar_range.buffet_aoa_df.shape[0])):
        tqdm.tqdm.write(f"Pyvista plotting mesh: %s with mach: %.2f at row: %d" % \
            (scalar_range.buffet_aoa_df.iloc[i_row, \
                scalar_range.buffet_aoa_df.columns.get_loc( \
                    ScalarsRangeSettings.flow_field_file_name)], \
                        scalar_range.buffet_aoa_df.iloc[i_row, \
                            scalar_range.buffet_aoa_df.columns.get_loc( \
                                ScalarsRangeSettings.mach_name)], \
                                    i_row))
        contour_plotter.reset()
        contour_plotter.setWorkingDirectory( \
            scalar_range.buffet_aoa_df.iloc[i_row, \
                scalar_range.buffet_aoa_df.columns.get_loc( \
                    ScalarsRangeSettings.working_directory_name)])
        contour_plotter.setFlowFieldFileName( \
            scalar_range.buffet_aoa_df.iloc[i_row, \
                scalar_range.buffet_aoa_df.columns.get_loc( \
                    ScalarsRangeSettings.flow_field_file_name)])
        contour_plotter.readFlowField()
        for i_scalar in range(PyvistaSettings.n_scalars):
            scalar_min: float = scalar_range.scalar_min_series.iloc[i_scalar]
            scalar_max: float = scalar_range.scalar_max_series.iloc[i_scalar]
            contour_plotter.plotScalar(i_scalar, [scalar_min, scalar_max])
            pass
        pass
    pass

if __name__ == "__main__":
    main()
    pass