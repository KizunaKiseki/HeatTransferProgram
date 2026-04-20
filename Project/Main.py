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
- Portions of this code were developed with AI autocomplete tools.
- These tools were used to improve coding efficiency and syntax accuracy.
_____________________________________________________________________
AUTHOR : Nicholas Heling
"""

# * IMPORTS *
# ? ================================================================ ?

# ! PYTHON TEMPLATES & LIBRARIES !
import os
import argparse as ap

# ! PROJECT MODULES !
import lib._Store as _store
import lib._Solve as _solve
import lib._Plot as _plot

# * VARIABLES *
# ? ================================================================ ?


# * FUNCTION *
# ? ================================================================ ?

def steady_state():
    """
    Summary of what the function does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    
    
    
    pass

def transient_state():
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
    # Initialize Figure_Path & Figure_Names for saving figures
    figure_path = []
    figure_names = []
    
    # Parse Commands
    parser = ap.ArgumentParser(description="Description of the program")
    parser.add_argument('mesh_xlsx', type = str, help='The name of the Excel file containing the mesh data.')
    
    # Parse Argument Command
    # ! python (file_path)Main.py (file_path)mesh.xlsx !
    args = parser.parse_args()
    
    try:
        mesh_data = _store.read_mesh(args.mesh_xlsx)

        # Output success message and prints the mesh data
        print("✅ Mesh data successfully read from the file.")
        _store.print_mesh(mesh_data)
 
    except FileNotFoundError:
        print(f"❎ The file {args.mesh_xlsx} was not found.")
    except Exception as e:
        print(f"❎ An error occurred while reading the mesh: {e}")
    
    
    # Create Figure 4 ⇒ Graphical Depiction of the Mesh
    mesh_figure = _plot.draw_mesh_figure(mesh_data)
    figure_path.append(mesh_figure)
    figure_names.append('mesh_figure')
    
    # Build Sparse Matrix
    sparse_matrix = _solve.build_conduction_matrix(mesh_data)

    # Create Figure 5 ⇒ Sparsity Pattern of Conduction Matrix
    sparsity_figure = _plot.plot_sparse_figure(sparse_matrix)
    figure_path.append(sparsity_figure)
    figure_names.append('sparsity_figure')
    
    
    
    # Create Figures Dictionary to save figures
    figures_dictionary = os.path.join(os.path.dirname(__file__), 'Figures')
    os.makedirs(figures_dictionary, exist_ok=True)
 
    for figure, name in zip(figure_path, figure_names):
        figure_file_path = os.path.join(figures_dictionary, f'{name}.png')
        figure.savefig(figure_file_path, dpi=300)
        print(f"✅ {name} saved to {figure_file_path}")
    
   
# * EXECUTE *
# ? ================================================================ ?
if __name__ == "__main__":
    main()