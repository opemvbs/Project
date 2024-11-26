import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting
from chemicals import Tc, Pc, Vc, omega
from chemicals import CAS_from_any
from chemicals import MW
import pandas as pd

N2 = CAS_from_any("oxygen")
Ar = CAS_from_any("argon")
N2_MW = MW("nitrogen")
Ar_MW = MW("argon")
N2_pct = 0.1
Ar_pct = 0.9

def calculate_Z(P, T):
    T = T

    T_crit_N2 = Tc(N2)
    P_crit_N2 = Pc(N2) / 101300
    V_crit_N2 = Vc(N2) * 10**6
    Omega_N2 = omega(N2)
    rho_c_N2 = N2_MW / V_crit_N2

    Pr_N2 = P/P_crit_N2
    Tr_N2 = T/T_crit_N2

    B0 = 0.083-(0.422/(Tr_N2**1.6))
    B1 = 0.139-(0.172/(Tr_N2**4.2))
    B_up = B0 + (Omega_N2 * B1)

    Z = 1 + (B0*(Pr_N2/Tr_N2)) + (Omega_N2 * B1 * (Pr_N2/Tr_N2))

    return Z

# Create an empty list to store results
results = []

# Loop over the range of P and T values
for P in range(10, 160, 10):
    for T in range(294, 314, 1):
        Z = calculate_Z(P, T)
        results.append({'Pressure (P)': P, 'Temperature (T)': T, 'Z': Z})

# Convert the results list to a pandas DataFrame
df = pd.DataFrame(results)

# Save the DataFrame to a CSV file
df.to_csv('output.csv', index=False)

# Create a 3D plot of Pressure (P), Temperature (T), and Z
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extracting values for plotting
P_values = df['Pressure (P)']
T_values = df['Temperature (T)']
Z_values = df['Z']

# Plotting the 3D surface
ax.scatter(P_values, T_values, Z_values, c=Z_values, cmap='viridis')

# Adding labels and title
ax.set_xlabel('Pressure (P)')
ax.set_ylabel('Temperature (T)')
ax.set_zlabel('Z')
ax.set_title('3D Plot of Z vs P and T')

# Show the plot
plt.show()

print("Data saved to 'output.csv' and graph displayed.")
