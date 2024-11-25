import numpy as np
import matplotlib.pyplot as plt

# Constants
gamma = 1.4  # Adiabatic index for nitrogen
n = 1.1      # Polytropic index for heat exchange with environment (reasonable estimate)
T_initial = 298  # Initial temperature in Kelvin (25°C)
P_initial = 1  # Initial pressure in bar (atmospheric pressure)
P_final = 150  # Final pressure in bar (cylinder pressure)

# Function to calculate temperature at each pressure for polytropic compression
def temperature_at_pressure_polytropic(T_initial, P_initial, P_final, n):
    # Apply the corrected polytropic process formula
    T_final = T_initial * (P_final / P_initial) ** ((gamma - 1) / (n))
    return T_final

# Generate a range of pressures from 1 bar to 150 bar
pressures = np.linspace(P_initial, P_final, num=500)  # Pressures from 1 to 150 bar
temperatures = [temperature_at_pressure_polytropic(T_initial, P_initial, P, n) for P in pressures]

# Plotting the results
plt.plot(pressures, temperatures)
plt.xlabel('Pressure (bar)')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs Pressure during Polytropic Compression of Nitrogen')
plt.grid(True)
plt.show()

# Print final temperature at 150 bar
final_temperature = temperatures[-1]
print(f"Final temperature at 150 bar with heat exchange: {final_temperature:.2f} K")
