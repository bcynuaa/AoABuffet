# Get Started

## Working Directory

Before using, a working directory should be built ahead. You'd better need to create 3 folders below:

1. `CFL3D`: Where the `cfl3d_Seq.exe` is located, also `cfl3d.inp` will be written here via this program. This can be modified in `config//cfl3d.json` file.
2. `Mesh`: Where the mesh files are located. Actually the mesh files don't need to be copied to working folder where `exe` file is located. It's specified in `cfl3d.inp` file with absolute path. This can be modified in `config//meshes.json` file.
3. `Data`: Where the calculation results will be saved. This can be modified in `config//calculation_settings.json` file.

Before running, the folder should look like this:

```bash
.
├── CFL3D
│   └── cfl3d_Seq.exe
├── Data
└── Mesh
    ├── 001_t010.x
    ├── 001_t012.x
    ├── 002_t010.x
    ├── 002_t012.x
    ├── 003_t010.x
    ├── 003_t012.x
    ├── 004_t010.x
    ├── 004_t012.x
    ├── 005_t010.x
    ├── 005_t012.x
    ├── 006_t010.x
    ├── 006_t012.x
    ...
```

After running one case at given `Minf` and `AoA` the folder should look like:

```bash
.
├── CFL3D
│   ├── aesurf.dat
│   ├── blockforce.dat
│   ├── cfl3d.alpha
│   ├── cfl3d_avgg.p3d
│   ├── cfl3d_avgq.p3d
│   ├── cfl3d.dynamic_patch
│   ├── cfl3d.inp
│   ├── cfl3d_Seq.exe
│   ├── cfl3d.subit_res
│   ├── cfl3d.subit_turres
│   ├── clcd.dat
│   ├── genforce.dat
│   ├── precfl3d.out
│   └── turb_avg.p3d
├── Data
│   └── 001_t010
│       └── M_0.720
│           └── A_0.500
│               ├── aesurf.dat
│               ├── blockforce.dat
│               ├── cfl3d.2out
│               ├── cfl3d.alpha
│               ├── cfl3d_avgg.p3d
│               ├── cfl3d_avgq.p3d
│               ├── cfl3d.blomax
│               ├── cfl3d.dynamic_patch
│               ├── cfl3d.inp
│               ├── cfl3d.out
│               ├── cfl3d.press
│               ├── cfl3d.prt
│               ├── cfl3d.restart
│               ├── cfl3d.subit_res
│               ├── cfl3d.subit_turres
│               ├── cfl3d.turres
│               ├── clcd.dat
│               ├── genforce.dat
│               ├── ovrlp.bin
│               ├── patch.bin
│               ├── plot3d_grid.xyz
│               ├── plot3d_sol.bin
│               ├── precfl3d.out
│               ├── resid.out
│               └── turb_avg.p3d
└── Mesh
    ├── 001_t010.x
    ├── 001_t012.x
    ├── 002_t010.x
    ├── 002_t012.x
    ├── 003_t010.x
    ├── 003_t012.x
    ├── 004_t010.x
    ├── 004_t012.x
    ├── 005_t010.x
    ├── 005_t012.x
    ├── 006_t010.x
    ├── 006_t012.x
    ...
```

Here's one thing to keep in mind that the directory should not be too deep, otherwise the program may not work properly for the `cfl3d` read lines with old `fortran` which may not allocate enough memory for string of path. I locate the root directory at `C://Project//` and it works well.