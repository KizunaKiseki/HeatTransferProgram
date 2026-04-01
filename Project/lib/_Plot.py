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
- Portions of this code were developed with AI autocomplete tools.
- These tools were used to improve coding efficiency and syntax accuracy.
_____________________________________________________________________
AUTHOR : Nicholas Heling
"""

# * IMPORTS *
# ? ================================================================ ?

# ! PYTHON TEMPLATES & LIBRARIES !
import numpy as np
import matplotlib.pyplot as pl
import scipy.sparse as sp

import matplotlib
import matplotlib.cm as cm
import matplotlib.patches as patches
import matplotlib.path as path

# ! PROJECT MODULES !
from lib._Store import N1, N2
from lib._Store import get_nodes

# * VARIABLES *
# ? ================================================================ ?


# * FUNCTION *
# ? ================================================================ ?

def plot_evolution(solution_array : list[np.ndarray], method_types : list[str], time_steps : list[float]) -> pl.figure:
    """
    Plots the evolution of temperature over time for different methods and time steps.
    The different methods are:
        ➀ Explicit
        ➁ Implicit 
        ➂ Semi-Implicit
    
    Args:
        solution_array (list[np.ndarray]): A list of solution arrays. 
        method_types (list[str]): A list of strings indicating the method type.
        time_steps (list[float]): A list of time step values corresponding to each solution/method.
    
    Returns:
        figure (pl.figure): A Matplotlib figure object containing the plot of temperature evolution.
    """
    plot_evolution_figure = pl.figure()
    
    # Axes & Line Styles
    plot_evolution_axes = figure.add_subplot(1,1,1)
    plot_evolution_axes.set_xlabel('Time, $t$ [hr]')
    plot_evolution_axes.set_ylabel('Temperature, $T$ [K]')
    line_styles = ['-','--',':']
    
    # Plot each solution array with corresponding method and time step
    for(k, (solution, method, time_step)) in enumerate(zip(solution_array, method_types, time_steps)):
        time_values, temperature_values = solution.T
        plot_evolution_axes.plot(time_values/3600, temperature_values, f'{line_styles[k]}C{k}', label=f'β={method}; Δt={time_step}')
    
    plot_evolution_axes.legend()
    
    
    return plot_evolution_figure


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

def draw_field(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, 
               y_coordinate : np.ndarray, field : np.ndarray, name : str) -> None:
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

def draw_element(mesh: dict, element_conduction_matrix : sp.dok_array, 
                 x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass