# Warnings!

## Working Directory Should be Short

For `cfl3d` use fortran to read the input file, the length of `inp` file each line should not be too long. Otherwise, the program will read the wrong input file.

I have tried to set the working directory  as something like ` C:\Users\myusr\Desktop\LocalProject\Help\CFDPostFlutter\CODE\AoASEP\data\calculation`, and the program failed for it cut the path as something like `C:\Users\myusr\Desktop\LocalProject\Help\CFDPostFlutt`.

This issue is where the `fortran` program should be to blame, which can not be solved by me.

## Output Files' Location May Not What You Expect

In my trial and error, I find that files used in `cfl3d.readCoef` and `cfl3d.readAoA` are actually located where the `exe` file is. So, if you want to use these two functions, you should copy these files from `exe`'s path to your data path. You may find this operation in `src/classes/CalculationTask.__backupFilesFromExePath` function.