# -*- coding: utf-8 -*-
"""
TITLE = Solving Functions
DATE  = 2026.05.15
_____________________________________________________________________
DESCRIPTION:
1. Functions for solving steady and transient heat conduction problems.
2. Builds the dual mesh matrix, shape matrix, capacity matrix, conduction matrix, and generation vector.
3. Functions to solve for steady-state and transient boundary conditions.
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
import _Store as _store
import _Plot as _plot

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
        
        # Get the Interior Index for the current element
        interior_index = mesh['IE']['cid'][element_index]
        
        # ! Equation 22 from Project Handout !
        capacity_element = (DELTA_Z * mesh['IC']['C'][interior_index] * mesh['IC']['rho'][interior_index] *
                          np.abs(np.linalg.det(build_shape_matrix(x_element, y_element))) * identity_matrix) / 6
        
        I = node_indices.reshape(3,1)
        J = node_indices.reshape(1,3)
        
        capacity_matrix[I, J] += capacity_element
            
            
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
        
        # Get the Interior Index for the current element
        interior_index = mesh['IE']['cid'][element_index]
        
        # ! Equation 18 from Project Handout !
        conduction_element = (DELTA_Z * mesh['IC']['k'][interior_index] * difference_matrix @ (edge_matrix - midpoint_matrix) 
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
    
    # Define the necessary matrices for the generation calculation
    identity_matrix = np.eye(3)
    
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

        # Get the Interior Index for the current element
        interior_index = mesh['IE']['cid'][element_index]

        # ! Equation 26 from Project Handout !
        generation_element = mesh['IC']['e'][interior_index]
        
        # ! Equation 22 from Project Handout !
        volume_element = (DELTA_Z * np.abs(np.linalg.det(build_shape_matrix(x_element, y_element))) * identity_matrix) / 6
        
        generation_vector[node_indices] += generation_element * volume_element.sum()
    
    
    return generation_vector
    

def steady_BCs(mesh : dict, conduction_matrix : sp.dok_array, generation_vector : np.ndarray) -> None:
    """
    Applies the steady-state boundary conditions to the conduction matrix and generation vector.
    The boundary conditions are fixed temperature and fixed heat flux.
    
    Args:
        mesh (dict): A dictionary containing the mesh information.
        conduction_matrix (sp.dok_array): A sparse matrix representing the conduction coefficients.
        generation_vector (np.ndarray): An array representing the generation values at each node.
    
    Returns:
        None
    """
    # Extract the boundary element from the mesh dictionary
    mesh_elements = mesh['BE'].shape[0]
    
    # Define the necessary matrices for the boundary condition application
    distribution_vector = np.array([1, 1])
    
    # Retrieve x and y coordinates for the nodes and the boundary element from mesh dictionary
    x_nodes, y_nodes = _store.get_nodes(mesh)
    element_nodes = mesh['BE'][_store.N1].values
    
    # Loop through each element in the mesh and compute the generation values
    for element_index in range(mesh_elements):
        # Get the node indices for the current boundary element
        node_indices = element_nodes[element_index]
        
        # Get the Boundary Index for the current boundary element
        boundary_index = mesh['BE']['cid'][element_index]
        heat_flux_element = mesh['BC']['q'][boundary_index]
    
        if np.isfinite(heat_flux_element):
            
            # Get x and y coordinates for the current element
            x_element = x_nodes[node_indices]
            y_element = y_nodes[node_indices]
            
            # Calculate the distance between the two nodes of the boundary element
            euclidean_distance = np.sqrt((x_element[1] - x_element[0])**2 + (y_element[1] - y_element[0])**2)
            
            # ! Equation 39 from Project Handout !
            generation_vector[node_indices] += (0.5 * DELTA_Z * heat_flux_element * euclidean_distance * distribution_vector)
        
    # Loop through each element in the mesh and compute the generation values
    for element_index in range(mesh_elements):
        # Get the node indices for the current boundary element
        node_indices = element_nodes[element_index]
        
        # Get the Boundary Index for the current boundary element
        boundary_index = mesh['BE']['cid'][element_index]
        temperature_element = mesh['BC']['T'][boundary_index]
    
        if np.isfinite(temperature_element):
            
            for temperature_node in node_indices:
            
                # ? All coefficients in the row corresponding to the target temperature,
                # ? must be set to zero except for the diagonal elements, which must be set to 1.
                conduction_matrix[temperature_node, :] = 0
                conduction_matrix[temperature_node, temperature_node] = 1
                
                # ! Equation 39 from Project Handout !
                generation_vector[temperature_node] = -temperature_element

            
def transient_BCs(mesh : dict, conduction_matrix : sp.dok_array, generation_vector : np.ndarray, 
                  temperature_vector : np.ndarray) -> None:
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
    
    # Define the necessary matrices for the boundary condition application
    distribution_vector = np.array([1, 1])
    
    # Retrieve x and y coordinates for the nodes and the boundary element from mesh dictionary
    x_nodes, y_nodes = _store.get_nodes(mesh)
    element_nodes = mesh['BE'][_store.N1].values
    
    # Loop through each element in the mesh and compute the generation values
    for element_index in range(mesh_elements):
        # Get the node indices for the current boundary element
        node_indices = element_nodes[element_index]
        
        # Get the boundary condition index for the current boundary element
        boundary_index = mesh['BE']['cid'][element_index]
        heat_flux_element = mesh['BC']['q'][boundary_index]
        temperature_element = mesh['BC']['T'][boundary_index]
        
        if np.isfinite(heat_flux_element):
            
            # Get x and y coordinates for the current element
            x_element = x_nodes[node_indices]
            y_element = y_nodes[node_indices]
            
            # Calculate the distance between the two nodes of the boundary element
            euclidean_distance = np.sqrt((x_element[1] - x_element[0])**2 + (y_element[1] - y_element[0])**2)
            
            # ! Equation 39 from Project Handout !
            generation_vector[node_indices] += (0.5 * DELTA_Z * heat_flux_element * euclidean_distance * distribution_vector)
        
        
        if np.isfinite(temperature_element):
            
            for temperature_node in node_indices:
                
                # ? All terms in the conduction matrix for the impacted rows should be set to zero.
                # ? All terms in the generation vector for the impacted rows should be set to zero.
                conduction_matrix[temperature_node, :] = 0
                generation_vector[temperature_node] = 0
                
                # ? Set initial temperature to ensure it does not change. 
                temperature_vector[temperature_node] = temperature_element
            
    

