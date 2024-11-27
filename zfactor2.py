import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting
from chemicals import Tc, Pc, Vc, omega, CAS_from_any, MW

# Constants and component details
COMPONENT = "argon"
P_MIN, P_MAX, P_STEP = 10, 160, 10  # Pressure range in bar
T_MIN, T_MAX, T_STEP = 294, 314, 1  # Temperature range in Kelvin

# Retrieve component properties
CAS = CAS_from_any(COMPONENT)
MW_component = MW(COMPONENT)
T_crit = Tc(CAS)
P_crit = Pc(CAS) / 101325  # Convert Pa to bar
V_crit = Vc(CAS) * 1e6  # Convert m^3/mol to cm^3/mol
omega_value = omega(CAS)

def calculate_Z(P, T, T_crit, P_crit, omega_value):
    """
    Calculate the compressibility factor (Z) using the virial equation of state.
    Parameters:
        P (float): Pressure in bar.
        T (float): Temperature in Kelvin.
        T_crit (float): Critical temperature in Kelvin.
        P_crit (float): Critical pressure in bar.
        omega_value (float): Acentric factor of the component.
    Returns:
        float: Compressibility factor Z.
    """
    Tr = T / T_crit  # Reduced temperature
    Pr = P / P_crit  # Reduced pressure

    B0 = 0.083 - 0.422 / (Tr ** 1.6)
    B1 = 0.139 - 0.172 / (Tr ** 4.2)
    B = B0 + omega_value * B1

    return 1 + B * (Pr / Tr)

def generate_data(P_range, T_range, T_crit, P_crit, omega_value):
    """
    Generate a DataFrame of Z values for given pressure and temperature ranges.
    Parameters:
        P_range (list): List of pressures in bar.
        T_range (list): List of temperatures in Kelvin.
        T_crit (float): Critical temperature in Kelvin.
        P_crit (float): Critical pressure in bar.
        omega_value (float): Acentric factor of the component.
    Returns:
        pd.DataFrame: DataFrame containing P, T, and Z values.
    """
    data = []
    for P in P_range:
        for T in T_range:
            Z = calculate_Z(P, T, T_crit, P_crit, omega_value)
            data.append({'Pressure (P)': P, 'Temperature (T)': T, 'Z': Z})
    return pd.DataFrame(data)

def plot_3d(data):
    """
    Create a 3D scatter plot of Z vs Pressure and Temperature.
    Parameters:
        data (pd.DataFrame): DataFrame containing 'Pressure (P)', 'Temperature (T)', and 'Z' columns.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data['Pressure (P)'], data['Temperature (T)'], data['Z'], c=data['Z'], cmap='viridis')

    # Adding labels and title
    ax.set_xlabel('Pressure (P) [bar]')
    ax.set_ylabel('Temperature (T) [K]')
    ax.set_zlabel('Compressibility Factor (Z)')
    ax.set_title('3D Plot of Z vs P and T')

    plt.show()

def main():
    # Define pressure and temperature ranges
    P_range = range(P_MIN, P_MAX, P_STEP)
    T_range = range(T_MIN, T_MAX, T_STEP)

    # Generate Z data
    df = generate_data(P_range, T_range, T_crit, P_crit, omega_value)

    # Save data to CSV
    # df.to_csv('output.csv', index=False)
    # print("Data saved to 'output.csv'.")

    # Plot 3D graph
    plot_3d(df)

if __name__ == "__main__":
    main()
