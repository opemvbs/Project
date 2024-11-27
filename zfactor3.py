import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting
from chemicals import Tc, Pc, omega, CAS_from_any, MW

# Constants and component details
COMPONENT = "argon"
P_MIN, P_MAX, P_STEP = 10, 200, 10  # Pressure range in bar
T_MIN, T_MAX, T_STEP = 273, 323, 1  # Temperature range in Kelvin
R = 0.08314  # Universal gas constant in L·bar/(mol·K)

# Retrieve component properties
CAS = CAS_from_any(COMPONENT)
MW_component = MW(COMPONENT)
T_crit = Tc(CAS)
P_crit = Pc(CAS) / 100000  # Convert Pa to bar
omega_value = omega(CAS)

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
    # Calculate a, b, and alpha
    Tr = T / T_crit
    m = 0.37464 + 1.54226 * omega_value - 0.26992 * omega_value**2
    alpha = (1 + m * (1 - np.sqrt(Tr)))**2
    a = 0.45724 * (R**2 * T_crit**2 / P_crit) * alpha
    b = 0.07780 * (R * T_crit / P_crit)

    # Calculate A and B
    A = a * P / (R**2 * T**2)
    B = b * P / (R * T)

    # Coefficients of the cubic equation
    coeffs = [1, B - 1, A - 3 * B**2 - 2 * B, B**3 + B**2 - A * B]

    # Solve cubic equation for Z
    roots = np.roots(coeffs)

    # Filter real roots
    real_roots = [np.real(r) for r in roots if np.isreal(r)]
    return max(real_roots)  # Assume gas phase: return largest Z

def generate_data(P_range, T_range, T_crit, P_crit, omega_value):
    """
    Generate a DataFrame of Z values for Pitzer and Peng-Robinson.
    """
    data = []
    for P in P_range:
        for T in T_range:
            Z_pitzer = calculate_Z_pitzer(P, T, T_crit, P_crit, omega_value)
            Z_PR = calculate_Z_PR(P, T, T_crit, P_crit, omega_value)
            data.append({'Pressure (P)': P, 'Temperature (T)': T,
                         'Z (Pitzer)': Z_pitzer, 'Z (PR)': Z_PR})
    return pd.DataFrame(data)

def plot_3d_comparison(data):
    """
    Create 3D scatter plots to compare Pitzer and PR-EOS results.
    """
    fig = plt.figure(figsize=(12, 6))

    # Plot Pitzer results
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(data['Pressure (P)'], data['Temperature (T)'], data['Z (Pitzer)'],
                c=data['Z (Pitzer)'], cmap='viridis')
    ax1.set_title('Pitzer Correlation')
    ax1.set_xlabel('Pressure (P) [bar]')
    ax1.set_ylabel('Temperature (T) [K]')
    ax1.set_zlabel('Compressibility Factor (Z)')

    # Plot PR-EOS results
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(data['Pressure (P)'], data['Temperature (T)'], data['Z (PR)'],
                c=data['Z (PR)'], cmap='plasma')
    ax2.set_title('Peng-Robinson EOS')
    ax2.set_xlabel('Pressure (P) [bar]')
    ax2.set_ylabel('Temperature (T) [K]')
    ax2.set_zlabel('Compressibility Factor (Z)')

    plt.tight_layout()
    plt.show()

def main():
    # Define pressure and temperature ranges
    P_range = range(P_MIN, P_MAX, P_STEP)
    T_range = range(T_MIN, T_MAX, T_STEP)

    # Generate Z data
    df = generate_data(P_range, T_range, T_crit, P_crit, omega_value)

    # Save data to CSV
    df.to_csv('output_comparison1.csv', index=False)
    print("Data saved to 'output_comparison.csv1'.")

    # Plot 3D graph for comparison
    plot_3d_comparison(df)

if __name__ == "__main__":
    main()
