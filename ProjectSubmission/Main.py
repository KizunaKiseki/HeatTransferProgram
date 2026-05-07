# -*- coding: utf-8 -*-
"""
TITLE = Main Execution File
DATE  = 2026.05.15
_____________________________________________________________________
DESCRIPTION:
1. A dual-mesh solver for steady and transient heat conduction problems.
2. The code reads a mesh from an Excel file and creates a graphical depiction of the mesh.
3. The graphical depiction of the mesh is saved as a PDF in the Figures directory.
    - Mesh nodes are plotted as points, and elements are plotted as lines connecting the nodes.
    - Sparsity pattern of the conduction matrix is visualized and saved as a PDF in the Figures directory.
    - Steady-state temperature distribution is computed and visualized, then saved as a PDF in the Figures directory.
    - Transient temperature distribution is computed for different time steps and methods, visualized, and saved as a PDF in the Figures directory.
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
import numpy as np
import scipy.sparse as sp

# ! PROJECT MODULES !
import _Store as _store
import _Solve as _solve
import _Plot as _plot

# * VARIABLES *
# ? ================================================================ ?

# Starting Temperature
START_TEMPERATURE = 300   # K

# Time Conversion Constants
CONVERT_HOURS_TO_SECONDS = 3600
CONVERT_MINUTES_TO_SECONDS = 60

# TOTAL Simulation Time for Transient Solvers (in seconds)
TOTAL_TIME = CONVERT_HOURS_TO_SECONDS * 700                 # 700 hours in seconds

# Time Step for Transient Solvers (in seconds)
EXPLICIT_TIME_STEP = CONVERT_MINUTES_TO_SECONDS * 3         # 3 minutes in seconds
IMPLICIT_TIME_STEP = CONVERT_HOURS_TO_SECONDS * 20          # 20 hours in seconds
SEMI_IMPLICIT_TIME_STEP = CONVERT_HOURS_TO_SECONDS * 20     # 20 hours in seconds
TIME_STEPS = [EXPLICIT_TIME_STEP, SEMI_IMPLICIT_TIME_STEP, IMPLICIT_TIME_STEP]

# Time Steps Names for Plotting
EXPLICIT_TIME_NAME = '3 min'
IMPLICIT_TIME_NAME = '20 hr'
SEMI_IMPLICIT_TIME_NAME = '20 hr'
TIME_STEP_NAMES = [EXPLICIT_TIME_NAME, SEMI_IMPLICIT_TIME_NAME, IMPLICIT_TIME_NAME]

# Method Parameters for Transient Solvers
EXPLICIT_METHOD = 0.0
SEMI_IMPLICIT_METHOD = 0.5
IMPLICIT_METHOD = 1.0
METHOD_TYPES = [EXPLICIT_METHOD, SEMI_IMPLICIT_METHOD, IMPLICIT_METHOD]

# Method Names for Plotting
EXPLICIT_METHOD_NAME = '0/2'
SEMI_IMPLICIT_METHOD_NAME = '1/2'
IMPLICIT_METHOD_NAME = '2/2'
METHOD_NAMES = [EXPLICIT_METHOD_NAME, SEMI_IMPLICIT_METHOD_NAME, IMPLICIT_METHOD_NAME]

# * FUNCTION *
# ? ================================================================ ?

def steady_solver(mesh_data : dict) -> np.ndarray:
    """
    Computes the steady-state temperature distribution for a given mesh.
    
    ! Steady State Assembly from Project Handout !
    
    Args:
        mesh_data (dict): A dictionary containing the mesh data.

    Returns:
        steady_solution (np.ndarray): The steady-state temperature distribution.
    """
    # ! Steady State Assembly from Project Handout ! 
    # Build Conduction Matrix & Generation Vector 
    conduction_matrix = _solve.build_conduction_matrix(mesh_data)
    generation_vector = _solve.build_generation_vector(mesh_data)
    
    # Apply Steady-State Boundary Conditions
    _solve.steady_BCs(mesh_data, conduction_matrix, generation_vector)
    
    # Solve for Steady-State Temperature Distribution
    temperature_distribution = _solve.sp.linalg.spsolve(conduction_matrix.tocsc(), generation_vector)
    
    # ! Create Figure 5 ⇒ Sparsity Pattern of Conduction Matrix !
    sparsity_figure = _plot.plot_sparse_figure(conduction_matrix)

    # ! Create Figure 6 ⇒ Steady-State Temperature Distribution !
    temperature_figure = _plot.draw_temperature_field_figure(mesh_data, -temperature_distribution)
    
    
    return sparsity_figure, temperature_figure


def transient_solver(mesh_data : dict) -> list[np.ndarray]:
    """
    Computes the temperature distribution at the next time step using the explicit method for transient heat conduction problems.
    
    ! Transient State Assembly from Project Handout !
    
    Args:
        mesh_data (dict): A dictionary containing the mesh data.

    Returns:
        transient_solution (list[np.ndarray]): A list containing the temperature distributions at each time step for different methods.
    """
    # Initialize Transient Solution List to store temperature distributions for each method
    transient_solution = []
    
    # Extract the number of nodes from the mesh data dictionary
    mesh_nodes = mesh_data['XY'].shape[0]
    
    # Retrieve x and y coordinates for nodes
    x_nodes, y_nodes = _store.get_nodes(mesh_data)
        
    # Identify the node closest to the center of the domain 
    temperature_min = np.argmin((x_nodes - 1)**2 + (y_nodes - 1)**2)

    for time_index in range(len(METHOD_TYPES)):
        
        # Construct Conduction Matrix, Generation Vector, and Capacity Matrix
        # ? The matrix is reset after each method so that each method is independent ?
        conduction_matrix = _solve.build_conduction_matrix(mesh_data)
        generation_vector = _solve.build_generation_vector(mesh_data)
        capacity_matrix = _solve.build_capacity_matrix(mesh_data)
                
        # Initialize initial temperature distribution
        initial_temperature = START_TEMPERATURE * np.ones(mesh_nodes)
        
        # Apply Transient Boundary Conditions
        _solve.transient_BCs(mesh_data, conduction_matrix, generation_vector, initial_temperature)
        
        # ! Generalized Format from Project Handout for Transient Assembly !
        new_matrix = (capacity_matrix - METHOD_TYPES[time_index] * TIME_STEPS[time_index] * conduction_matrix).tocsc()
        old_matrix = (capacity_matrix + (1 - METHOD_TYPES[time_index]) * TIME_STEPS[time_index] * conduction_matrix).tocsc()
        generation_time = TIME_STEPS[time_index] * generation_vector
        
        # Initialize initial time & temperature data for transient solutions
        initial_time = 0
        temperature_data = []
        
        # ! Time-stepping loop for transient solution !
        for time in range(initial_time, TOTAL_TIME, TIME_STEPS[time_index]):
            explicit_solution = sp.linalg.spsolve(new_matrix, old_matrix @ initial_temperature + generation_time)    
            initial_temperature = explicit_solution
            
            temperature_data.append((time, explicit_solution[temperature_min]))

        transient_solution.append(np.array(temperature_data))


    return transient_solution


# * MAIN *
# ? ================================================================ ?

def main():
    """
    Computes steady & transient state solutions for a given mesh and saves the results as figures in the Figures directory.
    Steady State Solution:
        1. Builds the conduction matrix and generation vector from the mesh data.
        2. Applies steady-state boundary conditions to the conduction matrix and generation vector.
        3. Solves for the steady-state temperature distribution.
        4. Plots the sparsity pattern of the conduction matrix and the steady-state temperature
            distribution, and saves the figures as PDFs in the Figures directory.
    
    Transient State Solution:
        1. Builds the conduction matrix, generation vector, and capacity matrix from the mesh data.
        2. Initializes the initial temperature distribution and applies transient boundary conditions.
        3. Uses a time-stepping loop to compute the temperature distribution at each time step for different methods 
            (explicit, semi-implicit, implicit).
        4. Plots the evolution of temperature over time for each method and saves the figure as a PDF in the Figures directory.
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
    
    # ! Steady State Solution ! 
    sparsity_figure, temperature_figure = steady_solver(mesh_data)
    
    # ! Transient State Solution !
    transient_solution = transient_solver(mesh_data)
    
    # ! Create Figure 4 ⇒ Graphical Depiction of the Mesh !
    mesh_figure = _plot.draw_mesh_figure(mesh_data)
    figure_path.append(mesh_figure)
    figure_names.append('mesh_figure')
    
    # ! Create Figure 5 ⇒ Sparsity Pattern of Conduction Matrix !
    figure_path.append(sparsity_figure)
    figure_names.append('sparsity_figure')

    # ! Create Figure 6 ⇒ Steady-State Temperature Distribution !
    figure_path.append(temperature_figure)
    figure_names.append('temperature_figure')
    
    # ! Create Figure 7 ⇒ Transient Temperature Distribution for Each Method !
    evolution_figure = _plot.plot_evolution_figure(transient_solution, METHOD_NAMES, TIME_STEP_NAMES)
    figure_path.append(evolution_figure)
    figure_names.append('evolution_figure')
    
    # Create Figures Dictionary to save figures
    figures_dictionary = os.path.join(os.path.dirname(__file__), 'Figures')
    os.makedirs(figures_dictionary, exist_ok=True)
    
    # Save Figures to Figures Directory as PDF
    for figure, name in zip(figure_path, figure_names):
        figure_file_path = os.path.join(figures_dictionary, f'{name}.pdf')
        figure.savefig(figure_file_path)
        
        # Success Message for Saving Figure
        print(f"✅ {name} saved to {figure_file_path}")
    
   
# * EXECUTE *
# ? ================================================================ ?
if __name__ == "__main__":
    main()