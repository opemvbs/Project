import numpy as np
from scipy.optimize import fsolve

# Given constants
a = 1.355  # L^2·bar/mol^2 (argon)
b = 0.03201  # L/mol (argon)
R = 0.08314  # L·bar/mol·K (gas constant)
T = 300  # K (temperature)
P = 150  # bar (pressure)

# Define the function for the van der Waals equation
def van_der_waals_eq(V):
    return (P + a / V**2) * (V - b) - R * T

# Initial guess for the molar volume (V)
V_initial_guess = 1.0

# Solve for V (molar volume) using fsolve
V_solution = fsolve(van_der_waals_eq, V_initial_guess)

# Calculate the compressibility factor Z
Z = P * V_solution[0] / (R * T)

# Print the results
print(f"Molar volume (V) = {V_solution[0]:.4f} L/mol")
print(f"Compressibility factor (Z) = {Z:.4f}")
