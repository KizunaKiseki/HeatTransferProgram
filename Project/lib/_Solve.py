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
from threading import local

import numpy as np
import scipy.sparse as sp

import matplotlib.pyplot as pl

# ! PROJECT MODULES !
import lib._Store as _store
import lib._Plot as _plot

# * VARIABLES *
# ? ================================================================ ?
DELTA_Z = 0.01      # m

# * FUNCTION *
# ? ================================================================ ?

def build_dual_mesh_matrix(x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> np.ndarray:
    """
    Builds the dual mesh matrix from the given x and y coordinates.
    
    Args:
        x_coordinate (np.ndarray): An array containing the x-coordinates of the nodes.
        y_coordinate (np.ndarray): An array containing the y-coordinates of the nodes.
    
    Returns:
        dual_mesh_matrix (np.ndarray): A matrix containing the dual mesh coordinates.
    """
    dual_mesh_matrix = np.array([x_coordinate,y_coordinate]).T
    
    
    return dual_mesh_matrix


def build_shape_matrix(x_coordinate : np.ndarray, y_coordinate : np.ndarray) -> np.ndarray:
    """
    Build the shape matrix from the given x and y coordinates.
    
    Args:
        x_coordinate (np.ndarray): An array containing the x-coordinates of the nodes.
        y_coordinate (np.ndarray): An array containing the y-coordinates of the nodes.
    
    Returns:
        shape_matrix (np.ndarray): A matrix containing the shape function values.
    """
    shape_matrix = np.array([[1,1,1], x_coordinate-x_coordinate.mean(), y_coordinate-y_coordinate.mean()]).T
    
    
    return shape_matrix


def build_capacity_matrix(mesh : dict) -> sp.dok_array:
    """
    Builds the capacity matrix for the given mesh.

    Args:
        mesh (dict): A dictionary containing the mesh information.
    
    Returns:
        capacity_matrix (sp.dok_array): A sparse matrix representing the capacity coefficients.
    """
    # Extract the number of nodes and elements from the mesh dictionary
    mesh_nodes = mesh['XY'].shape[0]
    mesh_elements = mesh['IE'].shape[0]
    capacity_matrix = sp.dok_array((mesh_nodes, mesh_nodes))
    
    # Define the necessary matrices for the capacity coefficient calculation
    identity_matrix = np.eye(3)
    
    # Retrieve x and y coordinates for the nodes and the element from mesh dictionary
    x_nodes, y_nodes = _store.get_nodes(mesh)
    element_nodes = mesh['IE'][_store.N2].values
    
    # Loop through each element in the mesh and compute the capacity coefficients
    for element_index in range(mesh_elements):
        # Get the node indices for the current element
        node_indices = element_nodes[element_index]
        
        # Get the x and y coordinates for the current element
        x_element = x_nodes[node_indices]
        y_element = y_nodes[node_indices]
        
        # ! Equation 22 from Project Handout !
        capacity_element = (mesh['IC']['C'] * mesh['IC']['rho'] * DELTA_Z * 0.5 * 
                          np.abs(np.linalg.det(build_shape_matrix(x_element, y_element))) * identity_matrix)
        
        for local_index, global_index in enumerate(node_indices):
            capacity_matrix[global_index, global_index] += capacity_element[local_index, local_index]
  
            
    return capacity_matrix


def build_conduction_matrix(mesh : dict) -> sp.dok_array:
    """
    Builds the conduction matrix for the given mesh.

    Args:
        mesh (dict): A dictionary containing the mesh information.
    
    Returns:
        conduction_matrix (sp.dok_array): A sparse matrix representing the conduction coefficients.
    """
    # Extract the number of nodes and elements from the mesh dictionary
    mesh_nodes = mesh['XY'].shape[0]
    mesh_elements = mesh['IE'].shape[0]
    conduction_matrix = sp.dok_array((mesh_nodes, mesh_nodes))
    
    # Define the necessary matrices for the conduction coefficient calculation
    difference_matrix = np.array([[1,0,-1],[-1,1,0],[0,-1,1]])
    edge_matrix = np.array([[1,1,0],[0,1,1],[1,0,1]])/2
    midpoint_matrix = np.array([[1,1,1],[1,1,1],[1,1,1]])/3
    rotation_matrix = np.array([[0,1],[-1,0]])
    span_matrix = np.array([[0,1,0],[0,0,1]])
    
    # Retrieve x and y coordinates for the nodes and the element from mesh dictionary
    x_nodes, y_nodes = _store.get_nodes(mesh)
    element_nodes = mesh['IE'][_store.N2].values
    
    # Loop through each element in the mesh and compute the conduction coefficients
    for element_index in range(mesh_elements):
        # Get the node indices for the current element
        node_indices = element_nodes[element_index]
        
        # Get the x and y coordinates for the current element
        x_element = x_nodes[node_indices]
        y_element = y_nodes[node_indices]
        
        # ! Equation 18 from Project Handout !
        conduction_element = (mesh['IE']['k'] * DELTA_Z * difference_matrix @ (edge_matrix - midpoint_matrix) 
                              @ build_dual_mesh_matrix(x_element, y_element) @ rotation_matrix @ span_matrix 
                              @ np.linalg.inv(build_shape_matrix(x_element, y_element)))
        
        I = node_indices.reshape(3,1)
        J = node_indices.reshape(1,3)
        
        conduction_matrix[I, J] += conduction_element
        
    
    return conduction_matrix


def build_generation_vector(mesh : dict) -> np.ndarray:
    """
    Builds the generation vector for the given mesh.

    Args:
        mesh (dict): A dictionary containing the mesh information.
    
    Returns:
        generation_vector (np.ndarray): An array representing the generation values at each node.
    """
    # Extract the number of nodes and elements from the mesh dictionary
    mesh_nodes = mesh['XY'].shape[0]
    mesh_elements = mesh['IE'].shape[0]
    generation_vector = np.zeros(mesh_nodes)
    
    # Retrieve x and y coordinates for the nodes and the element from mesh dictionary
    x_nodes, y_nodes = _store.get_nodes(mesh)
    element_nodes = mesh['IE'][_store.N2].values
    
    # Loop through each element in the mesh and compute the generation values
    for element_index in range(mesh_elements):
        # Get the node indices for the current element
        node_indices = element_nodes[element_index]
        
        # Get x and y coordinates for the current element
        x_element = x_nodes[node_indices]
        y_element = y_nodes[node_indices]
        
    
    return generation_vector
    
    

def steady_BCs(mesh : dict, conduction_matrix : sp.dok_array, generation_matrix : np.ndarray) -> None:
    """
    Applies the steady-state boundary conditions to the conduction matrix and generation vector.
    The boundary conditions are fixed temperature and fixed heat flux.
    
    Args:
        mesh (dict): A dictionary containing the mesh information.
        conduction_matrix (sp.dok_array): A sparse matrix representing the conduction coefficients.
        generation_matrix (np.ndarray): An array representing the generation values at each node.
    
    Returns:
        None
    """
    # Extract the boundary element from the mesh dictionary
    mesh_elements = mesh['BE'].shape[0]
    
    # Retrieve x and y coordinates for the nodes and the boundary element from mesh dictionary
    x_nodes, y_nodes = _store.get_nodes(mesh)
    element_nodes = mesh['BE'][_store.N1].values
    
    # Loop through each element in the mesh and compute the generation values
    for element_index in range(mesh_elements):
        # Get the node indices for the current boundary element
        node_indices = element_nodes[element_index]
        
        # Get the boundary condition index for the current boundary element
        boundary_index = mesh['BE']['cid'][element_index]
        boundary_heat_flux = mesh['BC']['q'][boundary_index]
    
        if np.isfinite(boundary_heat_flux):

            pass
        
    # Loop through each element in the mesh and compute the generation values
    for element_index in range(mesh_elements):
        # Get the node indices for the current boundary element
        node_indices = element_nodes[element_index]
        
        # Get the boundary condition index for the current boundary element
        boundary_index = mesh['BE']['cid'][element_index]
        boundary_temperature = mesh['BC']['T'][boundary_index]
    
        if np.isfinite(boundary_temperature):

            pass
        
    

def transient_BCs(mesh : dict, capacity_matrix : sp.dok_array, conduction_matrix : sp.dok_array, 
                  generation_vector : np.ndarray, temperature_vector : np.ndarray) -> None:
    """
    Applies the transient boundary conditions to the capacity matrix, conduction matrix, generation vector, and temperature vector.
    The boundary conditions are fixed temperature and fixed heat flux.
    
    Args:
        mesh (dict): A dictionary containing the mesh information.
        capacity_matrix (sp.dok_array): A sparse matrix representing the capacity coefficients.
        conduction_matrix (sp.dok_array): A sparse matrix representing the conduction coefficients.
        generation_vector (np.ndarray): An array representing the generation values at each node.
        temperature_vector (np.ndarray): An array representing the temperature values at each node.
    
    Returns:
        None
    """
    # Extract the boundary element from the mesh dictionary
    mesh_elements = mesh['BE'].shape[0]
    
    # Retrieve x and y coordinates for the nodes and the boundary element from mesh dictionary
    x_nodes, y_nodes = _store.get_nodes(mesh)
    element_nodes = mesh['BE'][_store.N1].values
    
    # Loop through each element in the mesh and compute the generation values
    for element_index in range(mesh_elements):
        # Get the node indices for the current boundary element
        node_indices = element_nodes[element_index]
        
        # Get the boundary condition index for the current boundary element
        boundary_index = mesh['BE']['cid'][element_index]
        boundary_heat_flux = mesh['BC']['q'][boundary_index]
        boundary_temperature = mesh['BC']['T'][boundary_index]
        
        if np.isfinite(boundary_heat_flux):

            pass
        
        if np.isfinite(boundary_temperature):
            
            pass
    
    

