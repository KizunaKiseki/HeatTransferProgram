# -*- coding: utf-8 -*-
"""
TITLE = Main Execution File
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
import argparse as ap

# ! PROJECT MODULES !
import Project.Store as _Store
import Project.Solve as _Solve
import Project.Plot as _Plot

# * VARIABLES *
# ? ================================================================ ?


# * FUNCTION *
# ? ================================================================ ?

def function_name():
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass


# * MAIN *
# ? ================================================================ ?

def main():
    """
    Summary of what the main does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    # Parse Commands
    parser = ap.ArgumentParser(description="Description of the program")
    parser.add_argument('mesh_xlsx', type = str, help='The name of the Excel file containing the mesh data.')
    
    # Parse Argument Command
    # ! python (file_path)Main.py (file_path)mesh.xlsx !
    args = parser.parse_args()
    
    try:
        mesh_data = _Store.read_mesh(args.mesh_xlsx)
        
        print("✅ Mesh data successfully read from file.")
    
    except FileNotFoundError:
        print(f"❎ The file {args.mesh_xlsx} was not found.")
    except Exception as e:
        print(f"❎ An error occurred while reading the mesh: {e}")
        
        
# * EXECUTE *
# ? ================================================================ ?
if __name__ == "__main__":
    main()