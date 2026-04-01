# -*- coding: utf-8 -*-
"""
TITLE = Solving Functions
DATE  = 2026.05.15
_____________________________________________________________________
DESCRIPTION:
1. [Insert Description Here]
2. ...
_____________________________________________________________________
DISCLAIMER:
- Portions of this code were developed with AI autocomplete tools.
- These tools were used to improve coding efficiency and syntax accuracy.
_____________________________________________________________________
AUTHOR : Nicholas Heling
"""

# * IMPORTS *
# ? ================================================================ ?

# ! PYTHON TEMPLATES & LIBRARIES !
import numpy as np
import scipy.sparse as sp

import matplotlib.pyplot as pl

# ! PROJECT MODULES !
from lib._Store import N1,N2
from lib._Store import get_nodes
import lib._Plot as _plot

# * VARIABLES *
# ? ================================================================ ?
DELTA_Z = 0.01      # m

# * FUNCTION *
# ? ================================================================ ?

def build_dual_mesh_matrix(x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> np.ndarray:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def build_shape_matrix(x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> np.ndarray:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def build_capacity_matrix(mesh : dict) -> sp.dok_array:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def build_conduction_matrix(mesh : dict) -> sp.dok_array:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def build_generation_vector(mesh : dict) -> np.ndarray:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def steady_BCs(mesh : dict, conduction_matrix : sp.dok_array, generation_matrix : np.ndarray) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def transient_BCs(mesh : dict, capacity_matrix : sp.dok_array, conduction_matrix : sp.dok_array, 
                  generation_vector : np.ndarray, temperature_vector : np.ndarray) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass
