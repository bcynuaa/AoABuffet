'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-06 23:55:32
 # @ Description: # ! consider the root directory is the project directory
 '''

import os

import pandas as pd
import matplotlib.pyplot as plt

from src.utils.Path import *
from src.utils.Decorator import *
from src.classes.AoAFinder import AoAFinder

image_path: str = "C://Project//Image"
mesh_path: str = "C://Project//Mesh"
Minf_list: list = [0.72, 0.74, 0.76]

assurePath(image_path)
mesh_pure_filename_list: list = os.listdir(mesh_path)
mesh_filename_list = [os.path.join(mesh_path, mesh_filename) for mesh_filename in mesh_pure_filename_list]

@clock
def runAoAFinder(mesh_filename: str, Minf: float) -> float:
    folder: str = os.path.join(image_path, getPureFilename(mesh_filename), "%.3f" % Minf)
    # if "AoA_buffet.dat" exists, return AoA_buffet directly
    if os.path.exists(os.path.join(folder, "AoA_buffet.dat")):
        with open(os.path.join(folder, "AoA_buffet.dat"), "r") as f:
            AoA_buffet: float = float(f.read())
            return AoA_buffet
        pass
    aoa_finder: AoAFinder = AoAFinder(mesh_filename, Minf)
    aoa_finder.findConvergeAoA()
    aoa_finder.refineAoA()
    aoa_finder.findAoABuffet()
    assurePath(folder)
    # CL-AoA
    plt.figure(figsize=(10, 6), facecolor="white", dpi=200)
    plt.plot(aoa_finder.AoA_interpolation, aoa_finder.CL_interpolation)
    plt.scatter(aoa_finder.AoA_converge, aoa_finder.CL_converge, c="red", zorder=10)
    plt.xlabel("AoA", fontsize=20)
    plt.ylabel("CL", fontsize=20)
    plt.savefig(os.path.join(folder, "CL-AoA.png"), bbox_inches="tight")
    plt.close()
    # CLalpha-AoA
    plt.figure(figsize=(10, 6), facecolor="white", dpi=200)
    plt.plot(aoa_finder.AoA_interpolation, aoa_finder.CLalpha_interpolation)
    plt.scatter(aoa_finder.AoA_converge, aoa_finder.CLalpha_converge, c="red", zorder=10)
    plt.hlines([aoa_finder.CLalpha0, aoa_finder.CLalpha0-0.1], aoa_finder.AoA_begin, aoa_finder.AoA_end, colors="k", linestyles="dashed")
    plt.xlabel("AoA", fontsize=20)
    plt.ylabel("CLalpha", fontsize=20)
    plt.title("CLalpha-AoA, AoA_buffet=%0.4f" % aoa_finder.AoA_buffet, fontsize=20)
    plt.savefig(os.path.join(folder, "CLalpha-AoA.png"), bbox_inches="tight")
    # dudy_min-AoA
    df: pd.DataFrame = aoa_finder.dataframe[aoa_finder.dataframe["converge"] == "True"].copy()
    plt.figure(figsize=(10, 6), facecolor="white", dpi=200)
    plt.plot(df["AoA"], df["dudy min"], "-o")
    plt.xlabel("AoA", fontsize=20)
    plt.ylabel("dudy min", fontsize=20)
    plt.savefig(os.path.join(folder, "dudy_min-AoA.png"), bbox_inches="tight")
    plt.close()
    # end
    aoa_finder.dataframe.to_csv(os.path.join(folder, "data.csv"), index=True)
    # write AoA_buffet to "AoA_buffet.dat"
    with open(os.path.join(folder, "AoA_buffet.dat"), "w") as f:
        f.write("%.4f" % aoa_finder.AoA_buffet)
        pass
    return aoa_finder.AoA_buffet
    pass

if __name__ == "__main__":
    df: pd.DataFrame = pd.DataFrame(columns=Minf_list, index=mesh_pure_filename_list)
    for i_mesh in range(len(mesh_filename_list)):
        mesh_filename: str = mesh_filename_list[i_mesh]
        mesh_pure_filename: str = mesh_pure_filename_list[i_mesh]
        for Minf in Minf_list:
            df.loc[mesh_pure_filename, Minf] = runAoAFinder(mesh_filename, Minf)
            print("AoA_buffet of %s, Minf=%.2f is %.4f" % (mesh_pure_filename, Minf, df.loc[mesh_pure_filename, Minf]))
            pass
        df.to_csv(os.path.join(image_path, "AoA.csv"), index=True)
        pass
    pass