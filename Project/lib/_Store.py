# -*- coding: utf-8 -*-
"""
TITLE = Store Functions
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
import pandas

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
        Exception: If any other error occurs during the reading process.
    """
    try:
        types = {
            str: 'name color',
            int: 'id material n0 n1 n2',
            float: 'x y T q rho k C',
        }
        
        conv = {
            column: dtype
            for dtype, columns in types.items()
            for column in columns.split()
        }

        mesh = pandas.read_excel(file_name, None, converters=conv)
        
        return mesh
    
    except FileNotFoundError:
        raise
    except Exception as e:
        raise e


def write_mesh(mesh : dict, file_name : str) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def print_mesh(mesh : dict) -> None:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def get_nodes(mesh : dict) -> tuple:
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass
