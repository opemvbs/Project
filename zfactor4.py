import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting
from chemicals import Tc, Pc, omega, CAS_from_any, MW

# Constants and range definitions
P_MIN, P_MAX, P_STEP = 10, 200, 10  # Pressure range in bar
T_MIN, T_MAX, T_STEP = 273, 323, 1  # Temperature range in Kelvin
R = 0.08314  # Universal gas constant in L·bar/(mol·K)

def calculate_mixture_properties(components, mole_fractions):
    """
    Calculate mixture properties (Tc, Pc, omega) using mixing rules.
    
    Parameters:
        components (list of str): List of component names.
        mole_fractions (list of float): List of mole fractions corresponding to each component.
    
    Returns:
        tuple: Mixture critical temperature (Tc), pressure (Pc), and acentric factor (omega).
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

def calculate_Z_pitzer(P, T, T_crit, P_crit, omega_value):
    """
    Calculate Z using the Pitzer correlation.
    """
    Tr = T / T_crit
    Pr = P / P_crit

    B0 = 0.083 - 0.422 / (Tr ** 1.6)
    B1 = 0.139 - 0.172 / (Tr ** 4.2)
    B = B0 + omega_value * B1

    return 1 + B * (Pr / Tr)

def calculate_Z_PR(P, T, T_crit, P_crit, omega_value):
    """
    Calculate Z using the Peng-Robinson EOS.
    """
    Tr = T / T_crit
    m = 0.37464 + 1.54226 * omega_value - 0.26992 * omega_value**2
    alpha = (1 + m * (1 - np.sqrt(Tr)))**2
    a = 0.45724 * (R**2 * T_crit**2 / P_crit) * alpha
    b = 0.07780 * (R * T_crit / P_crit)

    A = a * P / (R**2 * T**2)
    B = b * P / (R * T)

    coeffs = [1, B - 1, A - 3 * B**2 - 2 * B, B**3 + B**2 - A * B]
    roots = np.roots(coeffs)

    real_roots = [np.real(r) for r in roots if np.isreal(r)]
    return max(real_roots)  # Assume gas phase: return largest Z

def calculate_Z_RK(P, T, T_crit, P_crit):
    """
    Calculate Z using the Redlich-Kwong EOS.
    """
    a = 0.42748 * (R**2 * T_crit**2.5) / P_crit
    b = 0.08664 * (R * T_crit) / P_crit

    A = a * P / (R**2 * T**2.5)
    B = b * P / (R * T)

    coeffs = [1, -1, A - B - B**2, -A * B]
    roots = np.roots(coeffs)

    real_roots = [np.real(r) for r in roots if np.isreal(r)]
    return max(real_roots)  # Assume gas phase: return largest Z

def generate_mixture_data(P_range, T_range, T_crit, P_crit, omega_value):
    """
    Generate a DataFrame of Z values for Pitzer, Peng-Robinson, and Redlich-Kwong for mixtures.
    """
    data = []
    for P in P_range:
        for T in T_range:
            Z_pitzer = calculate_Z_pitzer(P, T, T_crit, P_crit, omega_value)
            Z_PR = calculate_Z_PR(P, T, T_crit, P_crit, omega_value)
            Z_RK = calculate_Z_RK(P, T, T_crit, P_crit)
            data.append({'Pressure (P)': P, 'Temperature (T)': T,
                         'Z (Pitzer)': Z_pitzer, 'Z (PR)': Z_PR, 'Z (RK)': Z_RK})
    return pd.DataFrame(data)

def plot_3d_comparison(data):
    """
    Create 3D scatter plots to compare Pitzer, PR-EOS, and RK results.
    """
    fig = plt.figure(figsize=(15, 6))

    ax1 = fig.add_subplot(131, projection='3d')
    ax1.scatter(data['Pressure (P)'], data['Temperature (T)'], data['Z (Pitzer)'],
                c=data['Z (Pitzer)'], cmap='viridis')
    ax1.set_title('Pitzer Correlation')
    ax1.set_xlabel('Pressure (P) [bar]')
    ax1.set_ylabel('Temperature (T) [K]')
    ax1.set_zlabel('Compressibility Factor (Z)')

    ax2 = fig.add_subplot(132, projection='3d')
    ax2.scatter(data['Pressure (P)'], data['Temperature (T)'], data['Z (PR)'],
                c=data['Z (PR)'], cmap='plasma')
    ax2.set_title('Peng-Robinson EOS')
    ax2.set_xlabel('Pressure (P) [bar]')
    ax2.set_ylabel('Temperature (T) [K]')
    ax2.set_zlabel('Compressibility Factor (Z)')

    ax3 = fig.add_subplot(133, projection='3d')
    ax3.scatter(data['Pressure (P)'], data['Temperature (T)'], data['Z (RK)'],
                c=data['Z (RK)'], cmap='cividis')
    ax3.set_title('Redlich-Kwong EOS')
    ax3.set_xlabel('Pressure (P) [bar]')
    ax3.set_ylabel('Temperature (T) [K]')
    ax3.set_zlabel('Compressibility Factor (Z)')

    plt.tight_layout()
    plt.show()

def main_mixture():
    # Define components and mole fractions
    components = ["methane"]  # Add more components as needed
    mole_fractions = [1]  # Ensure these sum to 1

    # Calculate mixture properties
    T_crit_mix, P_crit_mix, omega_mix = calculate_mixture_properties(components, mole_fractions)

    # Define pressure and temperature ranges
    P_range = range(P_MIN, P_MAX, P_STEP)
    T_range = range(T_MIN, T_MAX, T_STEP)

    # Generate Z data for the mixture
    df = generate_mixture_data(P_range, T_range, T_crit_mix, P_crit_mix, omega_mix)

    # Save data to CSV
    df.to_csv('output_mixture_comparison2.csv', index=False)
    print("Data saved to 'output_mixture_comparison2.csv'.")

    # Plot 3D graph for comparison
    plot_3d_comparison(df)

if __name__ == "__main__":
    main_mixture()
