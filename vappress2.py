import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting
from chemicals import Tc, Pc, omega, CAS_from_any, MW

# Constants and range definitions
T_MIN, T_MAX, T_STEP = 273, 323, 1  # Temperature range in Kelvin
R = 0.08314  # Universal gas constant in L·bar/(mol·K)

def calculate_mixture_properties(components, mole_fractions):
    """
    Calculate mixture properties (Tc, Pc, omega) using mixing rules.
    """
    if len(components) != len(mole_fractions):
        raise ValueError("Number of components must match number of mole fractions.")
    if not np.isclose(sum(mole_fractions), 1.0, atol=1e-6):
        raise ValueError("Mole fractions must sum to 1.")

    # Calculate mixture critical temperature (Tc) using linear rule
    T_crit_mix = sum(x * Tc(CAS_from_any(c)) for c, x in zip(components, mole_fractions))

    # Calculate mixture critical pressure (Pc) using geometric mean for binary interactions
    P_crit_mix = 0
    for i, (c1, x_i) in enumerate(zip(components, mole_fractions)):
        for j, (c2, x_j) in enumerate(zip(components, mole_fractions)):
            if i <= j:  # Avoid redundant calculations
                P_crit_mix += 2 * x_i * x_j * np.sqrt(Pc(CAS_from_any(c1)) * Pc(CAS_from_any(c2)))
    P_crit_mix /= 2  # Final averaging
    P_crit_mix /= 100000  # Convert from Pa to bar

    # Calculate mixture acentric factor (omega) using linear rule
    omega_mix = sum(x * omega(CAS_from_any(c)) for c, x in zip(components, mole_fractions))

    return T_crit_mix, P_crit_mix, omega_mix

def calculate_vapor_pressure_PR(T, T_crit, P_crit, omega_value):
    """
    Calculate vapor pressure using the Peng-Robinson EOS.
    """
    Tr = T / T_crit
    m = 0.37464 + 1.54226 * omega_value - 0.26992 * omega_value**2
    alpha = (1 + m * (1 - np.sqrt(Tr)))**2
    a = 0.45724 * (R**2 * T_crit**2 / P_crit) * alpha
    b = 0.07780 * (R * T_crit / P_crit)

    # Iteratively solve for Psat using Peng-Robinson EOS
    Psat = P_crit * 0.1  # Initial guess
    tolerance = 1e-6
    max_iter = 100

    for _ in range(max_iter):
        A = a * Psat / (R**2 * T**2)
        B = b * Psat / (R * T)

        # Peng-Robinson EOS coefficients
        coeffs = [1, -1 + B, A - 3 * B**2 - 2 * B, -A * B + B**3 + B**2]
        roots = np.roots(coeffs)
        real_roots = [np.real(r) for r in roots if np.isreal(r)]

        if not real_roots:
            break

        Z = max(real_roots)  # Assume liquid phase (smallest Z)
        f = Psat * np.exp(Z - 1 - np.log(Z - B) - (A / (2 * np.sqrt(2) * B)) *
                          np.log((Z + (1 + np.sqrt(2)) * B) / (Z + (1 - np.sqrt(2)) * B)))
        delta = Psat - f
        if abs(delta) < tolerance:
            break
        Psat -= delta

    return Psat

def generate_vapor_pressure_data(T_range, T_crit, P_crit, omega_value):
    """
    Generate a DataFrame of vapor pressures for different temperatures.
    """
    data = []
    for T in T_range:
        Psat_PR = calculate_vapor_pressure_PR(T, T_crit, P_crit, omega_value)
        data.append({'Temperature (T)': T, 'Vapor Pressure (PR) [bar]': Psat_PR})
    return pd.DataFrame(data)

def plot_vapor_pressure(data):
    """
    Plot vapor pressure as a function of temperature.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(data['Temperature (T)'], data['Vapor Pressure (PR) [bar]'], label='PR EOS', color='blue')
    plt.xlabel('Temperature (T) [K]')
    plt.ylabel('Vapor Pressure [bar]')
    plt.title('Vapor Pressure vs. Temperature')
    plt.legend()
    plt.grid(True)
    plt.show()

def main_mixture():
    # Define components and mole fractions
    components = ["nitrogen"]  # Add more components as needed
    mole_fractions = [1]  # Ensure these sum to 1

    # Calculate mixture properties
    T_crit_mix, P_crit_mix, omega_mix = calculate_mixture_properties(components, mole_fractions)

    # Define temperature range
    T_range = range(T_MIN, T_MAX, T_STEP)

    # Generate vapor pressure data for the mixture
    df = generate_vapor_pressure_data(T_range, T_crit_mix, P_crit_mix, omega_mix)

    # Save data to CSV
    df.to_csv('output_vapor_pressure.csv', index=False)
    print("Data saved to 'output_vapor_pressure.csv'.")

    # Plot vapor pressure graph
    plot_vapor_pressure(df)

if __name__ == "__main__":
    main_mixture()
