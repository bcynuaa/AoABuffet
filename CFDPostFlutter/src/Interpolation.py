'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-06-29 17:40:34
 # @ Description: interpolations
 '''

import numpy as np
import scipy.interpolate as interpolate

from src.ConstantVariable import kDefault_Interpolation_Type, kPrefered_Interpolation_Type, kSmall_Amount

def removeZeroElements(x_origin: np.ndarray, y_origin: np.ndarray, \
    also_remove_x: bool=False, track_index: bool=False) -> tuple:
    '''
    # remove zero elements in x_origin and y_origin
    
    ## Arguments
    
    - `x_origin`: np.ndarray, shape=(N,)
    - `y_origin`: np.ndarray, shape=(N,)
    - `also_remove_x`: bool, if True, also remove zero elements in x_origin
    - `track_index`: bool, if True, return the index of nonzero elements
    
    ## Returns
    
    - `x`: np.ndarray, shape=(M,), M <= N
    - `y`: np.ndarray, shape=(M,), M <= N
    - `nonzero_index`: np.ndarray, shape=(M,), M <= N, only if track_index == True
    '''
    nonzero_index: np.ndarray = np.where(np.abs(y_origin) > kSmall_Amount)[0]
    if also_remove_x == True:
        nonzero_index_x: np.ndarray = np.where(np.abs(x_origin) > kSmall_Amount)[0]
        nonzero_index = np.intersect1d(nonzero_index, nonzero_index_x)
        pass
    if track_index == False:
        return x_origin[nonzero_index], y_origin[nonzero_index]
        pass
    else:
        return x_origin[nonzero_index], y_origin[nonzero_index], nonzero_index
        pass
    pass

def getInterpolationFunction(x_origin: np.ndarray, y_origin: np.ndarray, method_flag: int) -> tuple:
    '''
    # cubic interpolation
    
    ## Arguments
    
    - `x_origin`: np.ndarray, shape=(N,)
    - `y_origin`: np.ndarray, shape=(N,)
    - `method_flag`: int, 0 for interp1d, 1 for PchipInterpolator, others for interp1d
    
    ## Returns
    
    - `interpolation`: function, the interpolation function
    - `x_min`: float, the minimum of x_origin
    - `x_max`: float, the maximum of x_origin
    '''
    x, y = removeZeroElements(x_origin, y_origin, also_remove_x=True)
    if x.shape[0] < 4:
        return np.zeros_like, 0.0, 0.0
        pass
    elif method_flag == 0:
        return interpolate.interp1d(x, y, kind=kPrefered_Interpolation_Type), x[0], x[-1]
        pass
    elif method_flag == 1:
        return interpolate.PchipInterpolator(x, y), x[0], x[-1]
        pass
    else:
        return interpolate.interp1d(x, y, kind=kDefault_Interpolation_Type), x[0], x[-1]
        pass
    pass

print("Interpolation.py is imported.")