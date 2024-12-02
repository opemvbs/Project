import pandas as pd
import numpy as np
from chemicals import Tc, Pc, omega, CAS_from_any

R = 0.0831446261815324  # Universal gas constant in L·bar/(mol·K)

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

def calculate_Z_2nd_virial(P, T, T_crit, P_crit, omega_value):
    """
    Calculate Z using the 2nd Virial coefficient correlation.
    """
    Tr = T / T_crit
    Pr = P / P_crit

    B0 = 0.083 - 0.422 / (Tr ** 1.6)
    B1 = 0.139 - 0.172 / (Tr ** 4.2)
    B = B0 + omega_value * B1

    return 1 + B * (Pr / Tr)

def calculate_Z_3rd_virial(P, T, T_crit, P_crit, omega_value):
    """
    Calculate Z using the 3rd Virial coefficient correlation.
    """
    Tr = T / T_crit  # Reduced temperature
    Pr = P / P_crit  # Reduced pressure

    # Second virial coefficient B
    B0 = 0.083 - 0.422 / (Tr ** 1.6)
    B1 = 0.139 - 0.172 / (Tr ** 4.2)
    B = B0 + omega_value * B1

    # Third virial coefficient C
    C0 = 0.01407 + 0.02432 / Tr - 0.00313 / Tr**10.5
    C1 = -0.02676 + 0.05539 / Tr**2.7 - 0.00242 / Tr**10.5
    C = C0 + omega_value * C1

    # For the compressibility factor, using ideal gas law V = RT / P
    # The equation Z = 1 + B * (P / RT) + C * (P / RT)^2 can be used.

    # Assuming the equation of state: Z = 1 + B * (Pr / Tr) + C * (Pr / Tr)^2
    Z = 1 + B * (Pr / Tr) + C * (Pr / Tr)**2

    return Z


def calculate_Z_PR(P, T, T_crit, P_crit, omega_value):
    """
    Calculate Z using the Peng-Robinson EOS.
    """
    Tr = T / T_crit
    if omega_value <= 0.49:
        m = 0.37464 + 1.54226 * omega_value - 0.26992 * omega_value**2
    elif omega_value > 0.49:
        m = 0.3796 + 1.485 * omega_value - 0.1644 * omega_value**2 + 0.01667 * omega_value**3
    # m = 0.37464 + 1.54226 * omega_value - 0.26992 * omega_value**2
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

def calculate_Z_SRK(P, T, T_crit, P_crit, omega):
    """
    Calculate Z using the Soave-Redlich-Kwong EOS, given omega.
    """
    # SRK specific parameters
    a = 0.42748 * (R**2 * T_crit**2.5) / P_crit * (1 + omega * (1 - np.sqrt(T / T_crit)))**2
    b = 0.08664 * (R * T_crit) / P_crit

    A = a * P / (R**2 * T**2.5)
    B = b * P / (R * T)

    coeffs = [1, -(1 - B), A - 2 * B - 3 * B**2, -(A * B - B**2 - B**3)]
    roots = np.roots(coeffs)

    real_roots = [np.real(r) for r in roots if np.isreal(r)]
    return max(real_roots)  # Assume gas phase: return largest Z

def generate_mixture_data(P, T, T_crit, P_crit, omega_value):
    """
    Generate a DataFrame of Z values for Pitzer, Peng-Robinson, and Redlich-Kwong for mixtures.
    """
    data = []
    Z_2nd_virial = calculate_Z_2nd_virial(P, T, T_crit, P_crit, omega_value)
    Z_3rd_virial = calculate_Z_3rd_virial(P, T, T_crit, P_crit, omega_value)
    Z_PR = calculate_Z_PR(P, T, T_crit, P_crit, omega_value)
    Z_RK = calculate_Z_RK(P, T, T_crit, P_crit)
    Z_SRK = calculate_Z_SRK(P, T, T_crit, P_crit, omega_value)
    data.append({'Pressure (P)': P, 'Temperature (T)': T,
                    'Z (2nd Virial)': Z_2nd_virial, 'Z (3rd Virial)': Z_3rd_virial, 'Z (PR)': Z_PR, 'Z (RK)': Z_RK, 'Z (SRK)': Z_SRK})
    return pd.DataFrame(data)

def main_mixture():
    # Define components and mole fractions
    components = ["nitrous oxide"]  # Add more components as needed
    mole_fractions = [1]  # Ensure these sum to 1

    # Calculate mixture properties
    T_crit_mix, P_crit_mix, omega_mix = calculate_mixture_properties(components, mole_fractions)

    # Define pressure and temperature ranges
    P = 10
    T = 288.15

    # Generate Z data for the mixture
    df = generate_mixture_data(P, T, T_crit_mix, P_crit_mix, omega_mix)
    print(df.to_string(index=False))
    # Save data to CSV

if __name__ == "__main__":
    main_mixture()
