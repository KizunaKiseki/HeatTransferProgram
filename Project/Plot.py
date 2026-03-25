# -*- coding: utf-8 -*-
"""
TITLE = Plot Functions
DATE  = 2026.05.15
_____________________________________________________________________
DESCRIPTION:
1. [Insert Description Here]
2. ...
_____________________________________________________________________
DISCLAIMER:
- 
_____________________________________________________________________
AUTHOR : Nicholas Heling
"""

# * IMPORTS *
# ? ================================================================ ?

# ! PYTHON TEMPLATES & LIBRARIES !
import numpy as np
import matplotlib.pyplot as pl

import matplotlib
import matplotlib.cm as cm
import matplotlib.patches as patches
import matplotlib.path as path

# ! PROJECT MODULES !
from Project.Store import N1,N2
from Project.Store import get_nodes

# * VARIABLES *
# ? ================================================================ ?


# * FUNCTION *
# ? ================================================================ ?

def plot_evolution(solution_array : list[np.ndarray], method_types : list[str], time_steps : list[float]) -> pl.figure:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def draw_problem(mesh: dict) -> pl.figure:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def draw_solution(mesh: dict, temperature_vector : np.ndarray) -> pl.figure:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def setup_figure() -> tuple[pl.figure, pl.axes]:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def draw_nodes(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def draw_field(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, y_coordinate : np.ndarray, field : np.ndarray, name : str) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def draw_cells(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def draw_interior(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def draw_exterior(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def plot_sparse():
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def draw_element(mesh: dict, element_conduction_matrix : sp.dok_array, x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass