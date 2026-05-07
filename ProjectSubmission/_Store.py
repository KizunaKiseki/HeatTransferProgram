# -*- coding: utf-8 -*-
"""
TITLE = Store Functions
DATE  = 2026.05.15
_____________________________________________________________________
DESCRIPTION:
1. Functions for reading, writing, and printing mesh data.
2. A function for extracting node coordinates from the mesh data.
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
import pandas as pd

# * VARIABLES *
# ? ================================================================ ?
N1 = ['n0','n1']
N2 = ['n0','n1','n2']

# * FUNCTION *
# ? ================================================================ ?

def read_mesh(file_name : str) -> dict:
    """
    This function reads a mesh from an Excel file and returns it as a dictionary.
    
    Args:
        file_name (str): The name of the Excel file containing the mesh data.
    
    Returns:
        mesh (dict): A dictionary containing the mesh data.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: For any I/O errors or issues while reading the file.
    """
    # Types for all columns in short form
    types = {
        str: 'name color',
        int: 'id material n0 n1 n2',
        float: 'x y T q ρ k Cₚ',
    }
    
    # Invert types dictionary for pandas format
    conv = {
        column: dtype
        for dtype, columns in types.items()
        for column in columns.split()
    }

    # Read all sheets in file as dataframes
    mesh = pd.read_excel(file_name, None, converters=conv)
    
    
    return mesh


def write_mesh(mesh : dict, file_name : str) -> None:
    """
    This function writes a mesh dictionary to an Excel file.
    
    Args:
        mesh (dict): A dictionary containing the mesh data.
        file_name (str): The name of the Excel file.
    
    Returns:
        None
    """
    with pd.ExcelWriter(file_name) as excel:
        for (sheet, data) in mesh.items():
            data.to_excel(excel, sheet_name=sheet, index=False)


def print_mesh(mesh : dict) -> None:
    """
    This function prints the contents of a mesh dictionary in a readable format.
    
    Args:
        mesh (dict): A dictionary containing the mesh data.
    
    Returns:
        None
    """
    for (k, (sheet, data)) in enumerate(mesh.items()):
        if k != 0:
            print()
        
        print(f'= {sheet} ='.center(46, '='))
        print(data)


def get_nodes(mesh : dict) -> tuple:
    """
    This function gets the x and y coordinates of the nodes from the mesh dictionary.
    
    Args:
        mesh (dict): A dictionary containing the mesh data.
    
    Returns:
        x_coordinate (tuple): A tuple containing the x coordinates of the nodes.
        y_coordinate (tuple): A tuple containing the y coordinates of the nodes.
    """
    x_coordinate = mesh['XY']['x'].values
    y_coordinate = mesh['XY']['y'].values
    
    
    return x_coordinate, y_coordinate

