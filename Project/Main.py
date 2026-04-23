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

# Time Conversion Constants
CONVERT_HOURS_TO_SECONDS = 3600
CONVERT_MINUTES_TO_SECONDS = 60

# TOTAL Simulation Time for Transient Solvers (in seconds)
TOTAL_TIME = CONVERT_HOURS_TO_SECONDS * 700                 # 700 hours

# Time Step for Transient Solvers (in seconds)
EXPLICIT_TIME_STEP = CONVERT_MINUTES_TO_SECONDS * 3         # 3 minutes
IMPLICIT_TIME_STEP = CONVERT_HOURS_TO_SECONDS * 20          # 20 hours
SEMI_IMPLICIT_TIME_STEP = CONVERT_HOURS_TO_SECONDS * 20     # 20 hours

# Time Steps Names for Plotting
EXPLICIT_TIME_NAME = '3 min'
IMPLICIT_TIME_NAME = '20 hr'
SEMI_IMPLICIT_TIME_NAME = '20 hr'

# Method Parameters for Transient Solvers
EXPLICIT_METHOD = 0.0
SEMI_IMPLICIT_METHOD = 0.5
IMPLICIT_METHOD = 1.0

# Method Names for Plotting
EXPLICIT_METHOD_NAME = '0/2'
SEMI_IMPLICIT_METHOD_NAME = '1/2'
IMPLICIT_METHOD_NAME = '2/2'

# * FUNCTION *
# ? ================================================================ ?

def steady_solver(mesh_data : dict) -> np.ndarray:
    """
    Computes the steady-state temperature distribution for a given mesh.
    
    Args:
        mesh_data (dict): A dictionary containing the mesh data.

    
    Returns:
        steady_solution (np.ndarray): The steady-state temperature distribution.
    """
    
    
    
    
    pass



def transient_solver(mesh_data : dict) -> list[np.ndarray]:
    """
    Computes the temperature distribution at the next time step using the explicit method for transient heat conduction problems.
    
    Args:
        mesh_data (dict): A dictionary containing the mesh data.

    
    Returns:
        transient_solution (list[np.ndarray]): A list containing the temperature distributions at each time step for different methods.
    """
    # Build Conduction Matrix, Generation Vector, and Capacity Matrix
    conduction_matrix = _solve.build_conduction(mesh_data)
    generation_vector = _solve.build_generation(mesh_data)
    capacity_matrix = _solve.build_capacity(mesh_data)
    
    
    # Extract the number of nodes from the mesh data dictionary
    mesh_nodes = mesh_data['XY'].shape[0]
    
    # Retrieve x and y coordinates for nodes
    x_nodes, y_nodes = _store.get_nodes(mesh_data)
        
    # Identify the node closest to the center of the domain 
    temperature_min = np.argmin((x_nodes - 0.5)**2 + (y_nodes - 0.5)**2)
    
    # Initialize Transient Arrays
    transient_solution = []
    method_type = [EXPLICIT_METHOD, SEMI_IMPLICIT_METHOD, IMPLICIT_METHOD]
    time_steps = [EXPLICIT_TIME_STEP, SEMI_IMPLICIT_TIME_STEP, IMPLICIT_TIME_STEP]
    
    for time_index in range(len(method_type)):
        
        # Initialize initial temperature distribution
        initial_temperature = time_steps[time_index] * np.ones(mesh_nodes)
        
        # ! Generalized Format from Project Handout !
        temperature_new = (capacity_matrix - method_type[time_index] * time_steps[time_index] * conduction_matrix).tocsc()
        temperature_old = (capacity_matrix + (1 - method_type[time_index]) * time_steps[time_index] * conduction_matrix).tocsc()
        generation_time = time_steps[time_index] * generation_vector
        
        # Initialize initial time for each method
        initial_time = 0.0
        
        for time in range(initial_time, TOTAL_TIME, time_steps[time_index]):
            pass

    
    # Iterate over time steps until total simulation time is reached
    while time < TOTAL_TIME:
        explicit_solution = np.linalg.solve(temperature_new, temperature_old @ initial_temperature + generation_time)
        
        
    
    
    return transient_solution



# * MAIN *
# ? ================================================================ ?

def main():
    """
    Summary of what the main does
    
    Args:
    
    
    Returns:
    
    
    Raises:
    """
    # Initialize figure_path & figure_names for saving figures
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
    
    # ! Steady State Assembly from Project Handout ! 
    # Build Conduction Matrix & Generation Vector 
    conduction_matrix = _solve.build_conduction_matrix(mesh_data)
    generation_vector = _solve.build_generation_vector(mesh_data)
    
    # Apply Steady-State Boundary Conditions
    _solve.steady_BCs(mesh_data, conduction_matrix, generation_vector)
    
    # Solve for Steady-State Temperature Distribution
    temperature_distribution = _solve.sp.linalg.spsolve(conduction_matrix.tocsc(), generation_vector)
    
    # ! Transient State Assembly from Project Handout ! 
    
    
    
    
    # ! Create Figure 4 ⇒ Graphical Depiction of the Mesh !
    mesh_figure = _plot.draw_mesh_figure(mesh_data)
    figure_path.append(mesh_figure)
    figure_names.append('mesh_figure')
    
    # ! Create Figure 5 ⇒ Sparsity Pattern of Conduction Matrix !
    sparsity_figure = _plot.plot_sparse_figure(conduction_matrix)
    figure_path.append(sparsity_figure)
    figure_names.append('sparsity_figure')

    # ! Create Figure 6 ⇒ Steady-State Temperature Distribution !
    temperature_figure = _plot.draw_temperature_field_figure(mesh_data, -temperature_distribution)
    figure_path.append(temperature_figure)
    figure_names.append('temperature_figure')
    
    # ! Create Figure 7 ⇒ Transient Temperature Distribution for Each Method !
    evolution_figure = _plot.plot_evolution(None, None, None)
    figure_path.append(evolution_figure)
    figure_names.append('evolution_figure')
    
    # Create Figures Dictionary to save figures
    figures_dictionary = os.path.join(os.path.dirname(__file__), 'Figures')
    os.makedirs(figures_dictionary, exist_ok=True)
    
    # Save Figures to Figures Directory as PDF
    for figure, name in zip(figure_path, figure_names):
        figure_file_path = os.path.join(figures_dictionary, f'{name}.pdf')
        figure.savefig(figure_file_path, dpi=300)
        
        # Success Message for Saving Figure
        print(f"✅ {name} saved to {figure_file_path}")
    
   
# * EXECUTE *
# ? ================================================================ ?
if __name__ == "__main__":
    main()