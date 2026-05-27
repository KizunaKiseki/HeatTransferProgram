# -*- coding: utf-8 -*-
"""
TITLE = Plot Functions
DATE  = 2026.05.15
_____________________________________________________________________
DESCRIPTION:
1. Functions for plotting the mesh, sparsity pattern of the conduction matrix, and temperature distributions.
2. A function for plotting the evolution of temperature over time for different methods and time steps.s
_____________________________________________________________________
DISCLAIMER:
- Portions of this code were developed with AI autocomplete tools.
- These tools were used to improve coding efficiency and syntax accuracy.
_____________________________________________________________________
AUTHOR : KizunaKiseki
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
import _Store as _store
import _Solve as _solve


# * FUNCTION *
# ? ================================================================ ?

def plot_evolution_figure(solution_array : list[np.ndarray], method_types : list[str], time_steps : list[float]) -> pl.figure:
    """
    Plots the evolution of temperature over time for different methods and time steps.
    The different methods are:
        ➀ Explicit
        ➁ Implicit 
        ➂ Semi-Implicit
    
    ! Figure 7 !
    
    Args:
        solution_array (list[np.ndarray]): A list of solution arrays. 
        method_types (list[str]): A list of strings indicating the method type.
        time_steps (list[float]): A list of floats indicating the time step values corresponding to each solution/method.
    
    Returns:
        figure (pl.figure): A Matplotlib figure object containing the plot of temperature evolution.
    """
    plot_evolution_figure = pl.figure()
    
    # Axes & Line Styles
    plot_evolution_axes = plot_evolution_figure.add_subplot(1,1,1)
    plot_evolution_axes.set_xlabel('Time, $t$ [hr]')
    plot_evolution_axes.set_ylabel('Temperature, $T$ [K]')
    line_styles = ['-','--',':']
    
    # Plot each solution array with corresponding method and time step
    for(k, (solution, method, time_step)) in enumerate(zip(solution_array, method_types, time_steps)):
        time_values, temperature_values = solution.T
        plot_evolution_axes.plot(time_values/3600, temperature_values, f'{line_styles[k]}C{k}', label=f'β={method}; Δt={time_step}')
    
    plot_evolution_axes.legend()
    
    
    return plot_evolution_figure


def draw_mesh_figure(mesh: dict) -> pl.figure:
    """
    Graphical depiction of the mesh used to approximate the solution to the problem.
    Triangular elements were used to fill the two-dimensional space of the domain.
    
    ! Figure 4 !
    
    Args:
        mesh (dict): A dictionary containing the mesh information.
    
    Returns:
        mesh_figure (pl.figure): A Matplotlib figure object containing the plot of the mesh.
    """
    # Retrieve x & y coordinates from mesh
    x_coordinates, y_coordinates = _store.get_nodes(mesh)
    
    # Setup Figure & Axes
    mesh_figure, mesh_axes = setup_figure()
    
    # Draw Interior, Exterior, and Nodes
    draw_interior(mesh_axes, mesh, x_coordinates, y_coordinates)
    draw_exterior(mesh_axes, mesh, x_coordinates, y_coordinates)
    draw_nodes(mesh_axes, mesh, x_coordinates, y_coordinates)
    
    
    return mesh_figure
    

def draw_temperature_field_figure(mesh: dict, temperature_vector : np.ndarray) -> pl.figure:
    """
    Graphical depiction of the steady-state temperature field.
    Polyhedral cells were used to assert conservation of energy using the finite volume method.
    
    ! Figure 6 !
    
    Args:
        mesh (dict): A dictionary containing the mesh information.
        temperature_vector (np.ndarray): A vector containing the temperature values at each node.
    
    Returns:
        temperature_field_figure (pl.figure): A Matplotlib figure object containing the plot of the temperature field.
    """
    # Retrieve x & y coordinates from mesh
    x_coordinates, y_coordinates = _store.get_nodes(mesh)
    
    # Setup Figure & Axes
    temperature_field_figure, temperature_field_axes = setup_figure()
    
    # Draw Field, Cells, Exterior, and Nodes
    draw_field(temperature_field_axes, mesh, x_coordinates, y_coordinates, temperature_vector, 'Temperature, $T$ [K]')
    draw_cells(temperature_field_axes, mesh, x_coordinates, y_coordinates)
    draw_exterior(temperature_field_axes, mesh, x_coordinates, y_coordinates)
    draw_nodes(temperature_field_axes, mesh, x_coordinates, y_coordinates)
    
    
    return temperature_field_figure


def setup_figure() -> tuple[pl.figure, pl.axes]:
    """
    General function to set up a Matplotlib figure and axes with consistent formatting for all plots.

    Args:
        None
    
    Returns:
        figure (pl.figure): A Matplotlib figure object.
        axes (pl.axes): A Matplotlib axes object with specific formatting applied.
    """
    # Create figure
    figure = pl.figure()
    
    # Create axes
    axes = figure.add_subplot(1,1,1)
    axes.set_aspect(1.0)
    axes.set_adjustable('datalim')
    axes.set_frame_on(False)
    axes.set_xticks([])
    axes.set_yticks([])
    
    
    return figure, axes


def draw_nodes(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> None:
    """
    Draws the nodes of the mesh on the given axes.
    
    Args:
        axes (pl.axes): A Matplotlib axes object on which to draw the nodes.
        mesh (dict): A dictionary containing the mesh information.
        x_coordinate (np.ndarray): An array containing the x-coordinates of the nodes.
        y_coordinate (np.ndarray): An array containing the y-coordinates of the nodes.
    
    Returns:
        None    
    """
    axes.plot(x_coordinate, y_coordinate, 'ko', ms=1, zorder=7)
    

def draw_field(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, 
               y_coordinate : np.ndarray, field : np.ndarray, name : str) -> None:
    """
    Draws the field values on the given axes.
    
    Args:
        axes (pl.axes): A Matplotlib axes object on which to draw the field.
        mesh (dict): A dictionary containing the mesh information.
        x_coordinate (np.ndarray): An array containing the x-coordinates of the nodes.
        y_coordinate (np.ndarray): An array containing the y-coordinates of the nodes.
        field (np.ndarray): An array containing the field values at each node.
        name (str): The name of the field to be displayed in the color bar.
    
    Returns:
        None
    """
    # Triangulate the field values using the connectivity information from the mesh
    triangles = mesh['IE'][_store.N2].values
    
    # Plot the field and add a color bar
    axes.tricontour(x_coordinate, y_coordinate, triangles, field, levels=25, zorder=4, linewidths=0.5)
    contour_filled = axes.tricontourf(x_coordinate, y_coordinate, triangles, field, levels=25)
    axes.get_figure().colorbar(contour_filled, ax=axes, label=name)


def draw_cells(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> None:
    """
    Draws the cells of the mesh on the given axes.
    
    Args:
        axes (pl.axes): A Matplotlib axes object on which to draw the cells.
        mesh (dict): A dictionary containing the mesh information.
        x_coordinate (np.ndarray): An array containing the x-coordinates of the nodes.
        y_coordinate (np.ndarray): An array containing the y-coordinates of the nodes.
    
    Returns:
        None
    """
    # Define the matrix M for cell centroids
    matrix_M = np.array([
        [1/3, 1/3, 1/3],
        [1/2, 1/2, 0],
        [1/3, 1/3, 1/3],
        [0, 1/2, 1/2],
        [1/3, 1/3, 1/3],
        [1/2, 0, 1/2]
        ])
    
    # Compute the cell centroids using the connectivity information from the mesh
    connectivity = mesh['IE'][_store.N2].values
    function = lambda x: (matrix_M@x[connectivity].T).T.flatten()
    vertices = np.column_stack([function(x_coordinate), function(y_coordinate)])
    
    # Create a PathPatch for the cells and add it to the axes
    codes = [path.Path.MOVETO, path.Path.LINETO] * (vertices.shape[0] // 2)
    cell_path_data = path.Path(vertices, codes)
    cell_path_patch = patches.PathPatch(cell_path_data, lw=0.3, alpha=0.5, zorder=5)
    axes.add_patch(cell_path_patch)


def draw_interior(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> None:
    """
    Draws the interior of the mesh on the given axes, coloring the cells based on their types.
    
    Args:
        axes (pl.axes): A Matplotlib axes object on which to draw the interior.
        mesh (dict): A dictionary containing the mesh information.
        x_coordinate (np.ndarray): An array containing the x-coordinates of the nodes.
        y_coordinate (np.ndarray): An array containing the y-coordinates of the nodes.
    
    Returns:
        None
    """
    # Triangulate the interior using the connectivity information from the mesh
    triangles = mesh['IE'][_store.N2].values
    connectivity = mesh['IE']['cid'].values
    
    # Create a color map based on the interior cell types
    colors = [matplotlib.colors.to_rgba(color) for color in mesh['IC']['color'].values]
    color_map = matplotlib.colors.ListedColormap(colors)
    axes.tripcolor(x_coordinate, y_coordinate, triangles, connectivity, cmap=color_map, edgecolor='k', lw=0.1)


def draw_exterior(axes : pl.axes, mesh: dict, x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> None:
    """
    Draws the exterior of the mesh on the given axes, coloring the cells based on their types.
    
    Args:
        axes (pl.axes): A Matplotlib axes object on which to draw the exterior.
        mesh (dict): A dictionary containing the mesh information.
        x_coordinate (np.ndarray): An array containing the x-coordinates of the nodes.
        y_coordinate (np.ndarray): An array containing the y-coordinates of the nodes.
    
    Returns:
        None
    """
    # Triangulate the exterior using the connectivity information from the mesh
    edge = mesh['BE'][_store.N1].values
    connectivity = mesh['BE']['cid'].values
    
    # Create a color map based on the exterior cell types
    colors = mesh['BC']['color'][connectivity]
    for edge_index, color_index in zip(edge, colors):
        axes.plot(x_coordinate[edge_index], y_coordinate[edge_index], color=color_index, lw=4, zorder=6)


def plot_sparse_figure(sparse_matrix : sp.spmatrix, label : str = 'Coefficient Magnitude, $A_{ij} [-]$', partition : list[int] = None) -> pl.figure:
    """
    Graphical depiction of the sparsity pattern for the conduction matrix.
    
    ! Figure 5 !
    
    Args:
        sparse_matrix (sp.spmatrix): A sparse matrix representing the conduction coefficients.
        label (str): The label for the color bar. Defaults to 'Coefficient Magnitude, $A_{ij} [-]$'.
        partition (list[int]): A list of integers indicating the partitioning of the matrix for visualization. Defaults to None.
    
    Returns:
        sparse_figure (pl.figure): A Matplotlib figure object containing the plot of the sparsity pattern.
    """
    # Setup Figure & Axes
    sparse_figure = pl.figure(figsize=(7.5, 4))
    sparse_axes = sparse_figure.subplots(1, 1)
    
    # Set axes labels and formatting
    sparse_axes.set_xlabel('Column, $j$ [$\\#$]')
    sparse_axes.set_ylabel('Row, $i$ [$\\#$]')
    sparse_axes.set_xticks([])
    sparse_axes.set_yticks([])
    sparse_axes.xaxis.tick_top()
    sparse_axes.xaxis.set_label_position('top')
    
    # Draw the sparsity pattern of the matrix
    keys = np.array(list(sparse_matrix.keys()))
    values = np.array(list(sparse_matrix.values()))
    row_indices = keys.shape[0] - keys[:, 0] - 1
    column_indices = keys[:, 1]
    scale = max(abs(values.min()), abs(values.max()))
    
    # Calculate marker size based on the number of rows and the figure size
    height = sparse_axes.get_window_extent().transformed(sparse_axes.get_figure().dpi_scale_trans.inverted()).height
    row_spacing = height / row_indices.size
    fudge_factor = 25
    size = (fudge_factor * row_spacing * 72)**2
    
    # Create a color map and scatter plot for the non-zero entries of the matrix
    color_map = cm.get_cmap('viridis', 9)
    scatter = sparse_axes.scatter(column_indices, row_indices, marker='o', linewidths=0, s=size, c=values, vmin=-scale, vmax=scale, cmap=color_map)
    
    # Draw partition lines if specified
    if partition:
        sparse_axes.axhline(keys.shape[0] - partition - 1 + 0.5, linestyle='-', color='k', linewidth=0.5)
        sparse_axes.axvline(partition - 1 + 0.5, linestyle='-', color='k', linewidth=0.5)
    
    # Set axes limits to ensure all points are visible
    sparse_axes.set_xlim(column_indices.min() - 0.5, column_indices.max() + 0.5)
    sparse_axes.set_ylim(row_indices.min() - 0.5, row_indices.max() + 0.5)
    
    # Create a color bar for the scatter plot
    sparse_figure = sparse_axes.get_figure()
    sparse_figure.colorbar(scatter, ax=sparse_axes, label=label)
    
    # Set aspect ratio and anchor for the axes
    sparse_axes.set_aspect(1.0)
    sparse_axes.set_anchor('C')
    
    
    return sparse_figure


def plot_element_figure(mesh: dict, element_conduction : sp.dok_array) -> pl.figure:
    """
    Graphical depiction of the element conduction matrix for a specific element in the mesh.
    
    ! Figure 2 !
        
    Args:
        mesh (dict): A dictionary containing the mesh information.
        element_conduction (sp.dok_array): A sparse matrix representing the conduction coefficients for the element.
    
    Returns:
        element_figure (pl.figure): A Matplotlib figure object containing the plot of the element conduction matrix.
    """
    # Extract the number of nodes and elements from the mesh
    mesh_nodes = mesh['XY'].shape[0]
    mesh_elements = mesh['IE'].shape[0]
    sparse_matrix = sp.dok_array((mesh_nodes, mesh_nodes))
    
    # Define the matrices for the element conduction calculation
    shift_matrix = np.array([[0, 1, 0], [0, 0, 1]])
    edge_matrix = np.array([[1, 1, 0], [0, 1, 1], [1, 0, 1]]) / 2
    centroid_matrix = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 3
    rotation_matrix = np.array([[0, 1], [-1, 0]])
    difference_matrix = np.array([[1, 0, -1], [-1, 1, 0], [0, -1, 1]])
    
    # Retrieve x and y coordinates of the nodes and nodes for each element from the mesh
    x_nodes, y_nodes = _store.get_nodes(mesh)
    element_nodes = mesh['IE'][_store.N2].values
    
    # Compute the x and y coordinates for the nodes of the specified element
    node_indices = element_nodes[element_conduction]
    x_element = x_nodes[node_indices]
    y_element = y_nodes[node_indices]

    # Compute the cell ID and conductivity for the specified element
    cell_id = mesh['IE']['cid'][element_conduction]
    cell_conductivity = mesh['IC']['k'][cell_id]
    
    # Compute dual mesh matrix and shape matrix for the specified element
    dual_mesh_matrix = _solve.build_dual_mesh_matrix(x_element, y_element)
    shape_matrix = _solve.build_shape_matrix(x_element, y_element)
    
    # Figure and Axes Setup
    element_figure = pl.figure()
    element_axes = element_figure.add_subplot(1, 1, 1)
    element_axes.set_aspect('equal')
    
    # Plot the dual mesh matrix for the specified element
    element_axes.plot(dual_mesh_matrix[:, 0], dual_mesh_matrix[:, 1], 'ks')
    element_axes.fill(dual_mesh_matrix[:, 0], dual_mesh_matrix[:, 1], color='C1', alpha=0.2)
    
    # Compute the edge points and centroid points for the specified element and plot
    edge_points = edge_matrix @ dual_mesh_matrix
    centroid_points = centroid_matrix @ dual_mesh_matrix
    
    element_axes.plot(edge_points[:, 0], edge_points[:, 1], 'ko')
    element_axes.plot(centroid_points[:, 0], centroid_points[:, 1], 'kh')
    
    # Compute the shape function values for the specified element and plot the corresponding vectors
    shape_function_values = (edge_matrix - centroid_matrix) @ dual_mesh_matrix
    
    element_axes.quiver(centroid_points[:, 0], centroid_points[:, 1], shape_function_values[:, 0], shape_function_values[:, 1], scale=1.0, scale_units='xy', color='C0')
    
    # Compute the face points and corresponding vectors for the specified element and plot the vectors
    face_points = (edge_matrix + centroid_matrix) @ dual_mesh_matrix / 2
    face_vectors = shape_function_values @ rotation_matrix
    
    element_axes.plot(face_points[:, 0], face_points[:, 1], 'kd')
    element_axes.quiver(face_points[:, 0], face_points[:, 1], face_vectors[:, 0], face_vectors[:, 1], scale=1.0, scale_units='xy', color='C3')
    
    # Compute the flux points and corresponding vectors for the specified element and plot the vectors
    flux_points = - difference_matrix @ face_points
    midpoints = np.abs(difference_matrix) @ edge_points / 2
    
    element_axes.plot(midpoints[:, 0], midpoints[:, 1], 'kv')
    element_axes.quiver(midpoints[:, 0], midpoints[:, 1], flux_points[:, 0] / 2, flux_points[:, 1] / 2, scale=1.0, scale_units='xy', color='C4')
    
    
    return element_figure

