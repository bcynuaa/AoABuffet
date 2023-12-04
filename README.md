# AoABuffet

A repository to find buffet attack angle using fluent automatically.

# Introduction

This repository aims to help my leader's wife's students to build a model to find the buffet attack angle in machine learning.

My work is to make a dataset for them to train their model.

# Folders

1. `CLShakeAoA`: Original method using `CFL3D` as backend inspired from Runze Lee. However, `CFL3D` seems not a good choice for this problem.
2. `AoABuffet-Fluentbackend`: A new method using `Fluent` as backend. `Fluent` is quite stable and easy to use. This method using bin-search and cubic spline interpolation to quickly locate the buffet attack angle.
3. `AoABuffet-Contour`: For graphic network, we need to generate contour images. This folder contains the code to generate contour images using `pyvista`.