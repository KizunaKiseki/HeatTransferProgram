# --- coding: utf-8 -*-
"""
TITLE = Chapter 5 - Numerical Methods - Problem 5
DATE  = 2026.03.04
_____________________________________________________________________
DESCRIPTION:
1. Calculate the temperature distribution in a 3x3 grid after 10 minutes with convection boundaries
2. Plot the temperature distribution as a contour plot
_____________________________________________________________________
AUTHOR : [Nicholas Heling]
"""

# * IMPORTS *
# ? ================================================================ ?

# ! PYTHON TEMPLATES & LIBRARIES !
import numpy as np
import matplotlib.pyplot as plt

# * GLOBAL VARIABLES *
# ? ================================================================ ?
# HEAT TRANSFER PROPERTIES
THERMAL_CONDUCTIVITY = 120                  # W/m-K
CONVECTION_COEFFICIENT_WATER = 100          # W/m^2-K
CONVECTION_COEFFICIENT_AIR = 10             # W/m^2-K
ALPHA = 3.91e-6                             # m^2/s

# GEOMETRIC PROPERTIES
AREA = 0.80                                 # m^2
DELTA_X = DELTA_Y = 0.1                     # m
NX, NY = 3, 3                               # 3x3 half-grid  

# THERMAL PROPERTIES
INITIAL_TEMPERATURE = 800                   # °C
TEMPERATURE_INFINITY = 15                   # °C

# SIMULATION PROPERTIES
DELTA_T = 10                                # seconds


# * FUNCTION *
# ? ================================================================ ?

def ghost_convection(Tp: float, Bi: float, T_inf: float) -> float:
    """
    Ghost node temperature for convection boundary condition
    Args:
        Tp (float): Temperature at the boundary node
        Bi (float): Biot number
        T_inf (float): Temperature at infinity
    
    Returns:
        float: Ghost node temperature
    """
    return Tp - 2.0 * Bi * (Tp - T_inf)


def update_node(T: np.ndarray, j: int, i: int, fourier_number: float, bi_water: float, bi_air: float, T_inf: float) -> float:
    """
    Update a single node (j, i) using the finite difference method
    
    Grid Indexing:
      1   2   3
      4   5   6
      7   8   9
    
    Args:
        T (np.ndarray): Temperature array
        j (int): Row index
        i (int): Column index
        fourier_number (float): Fourier number
        bi_water (float): Biot number for water convection
        bi_air (float): Biot number for air convection
        T_inf (float): Temperature at infinity
    
    Returns:
        float: Updated temperature at node (j, i)
    """
    Tp = T[j, i]
    
    # West Neighbor
    if i - 1 >= 0:
        T_west = T[j, i - 1]
    else:
        # Left Boundary: Water Convection
        T_west = ghost_convection(Tp, bi_water, T_inf)
        
    # East Neighbor
    if i + 1 < T.shape[1]:
        T_east = T[j, i + 1]
    else:
        # Right Boundary: Symmetry 
        T_east = T_west
    
    # North Neighbor
    if j - 1 >= 0:
        T_north = T[j - 1, i]
    else:
        # Top Boundary: Air Convection
        T_north = ghost_convection(Tp, bi_air, T_inf)
    
    # South Neighbor
    if j + 1 < T.shape[0]:
        T_south = T[j + 1, i]
    else:
        # Bottom Boundary: Water Convection
        T_south = ghost_convection(Tp, bi_water, T_inf)
        
    # Explicit 2D Finite Difference Update
    return (1.0 -4.0 * fourier_number) * Tp + fourier_number * (T_west + T_east + T_north + T_south)
    
def plot_temperature(T: np.ndarray, dx: float) -> None:
    """
    Plot the temperature distribution as a contour plot
    
    Args:
        T (np.ndarray): Temperature array
        dx (float): Grid spacing in x and y directions
    """
    # Grid Dimensions
    ny, nx = T.shape
    
    # Create coordinate arrays for plotting
    x = np.linspace(0, (nx - 1) * dx, nx)
    y = np.linspace(0, (ny - 1) * dx, ny)
    X, Y = np.meshgrid(x, y)
    
    # Create contour plot
    plt.figure(figsize=(6, 5))
    contour = plt.contourf(X, Y, T, levels=20, cmap='inferno')
    plt.colorbar(contour, label='Temperature (°C)')
    
    # Plot Labels and Title
    plt.title('Temperature Distribution After 10 Minutes')
    plt.xlabel('Position X (m)')
    plt.ylabel('Position Y (m)')
    
    # Figure Settings
    plt.gca().set_aspect('equal')    
    plt.show()


# * MAIN *
# ? ================================================================ ?

def main():
    """
    Main function to execute the finite difference simulation for the 3x3 grid with convection boundaries
    """
    
    # Calculate the number of time steps
    time_minutes = 10                                  
    n_steps = int((time_minutes * 60) / DELTA_T) + 1
    
    # Calculate the Fourier number and Biot numbers
    fourier_number = (ALPHA * DELTA_T) / (DELTA_X ** 2)
    bi_water = (CONVECTION_COEFFICIENT_WATER * DELTA_X) / THERMAL_CONDUCTIVITY
    bi_air = (CONVECTION_COEFFICIENT_AIR * DELTA_X) / THERMAL_CONDUCTIVITY
    
    # Initial Conditions
    T = np.full((NY, NX), INITIAL_TEMPERATURE)
    
    # Time-stepping loop
    for _ in range(n_steps):
        T_new = T.copy()
        for j in range (NY):
            for i in range(NX):
                T_new[j, i] = update_node(T, j, i, fourier_number, bi_water, bi_air, TEMPERATURE_INFINITY)
        T = T_new
    
    
    print ("Final Temperature Distribution (°C):")
    print (T)
    
    # Node Mapping:
    # 1   2   3
    # 4   5   6
    # 7   8   9
    print("\nNode Temperatures:")
    print(f"Node 1: {T[0, 0]:.2f} °C, Node 2: {T[0, 1]:.2f} °C, Node 3: {T[0, 2]:.2f} °C")
    print(f"Node 4: {T[1, 0]:.2f} °C, Node 5: {T[1, 1]:.2f} °C, Node 6: {T[1, 2]:.2f} °C")
    print(f"Node 7: {T[2, 0]:.2f} °C, Node 8: {T[2, 1]:.2f} °C, Node 9: {T[2, 2]:.2f} °C")
    
    # Plot the temperature distribution
    plot_temperature(T, DELTA_X)

        
        
# * EXECUTE *
# ? ================================================================ ?
if __name__ == "__main__":
    main()