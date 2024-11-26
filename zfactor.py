from chemicals import Tc, Pc, Vc, omega
from chemicals import CAS_from_any
from chemicals import MW
import pandas as pd

H2S = CAS_from_any("methane")
CH4 = CAS_from_any("methane")
N2_MW = MW("methane")
Ar_MW = MW("methane")
N2_pct = 0.1
Ar_pct = 0.9
P = 150
T = 293

T_crit_H2S = Tc(H2S)
P_crit_H2S = Pc(H2S) / 101300
V_crit_H2S = Vc(H2S) * 10**6
Omega_H2S = omega(H2S)


Pr_H2S = P/P_crit_H2S
Tr_H2S = T/T_crit_H2S

B0 = 0.083-(0.422/(Tr_H2S**1.6))
B1 = 0.139-(0.172/(Tr_H2S**4.2))
B_up = B0 + (Omega_H2S * B1)

Z = 1 + (B0*(Pr_H2S/Tr_H2S)) + (Omega_H2S * B1 * (Pr_H2S/Tr_H2S))

# def calculate_Z(P):
#     T = 293

#     T_crit_N2 = Tc(N2)
#     P_crit_N2 = Pc(N2) / 101300
#     V_crit_N2 = Vc(N2) * 10**6
#     Omega_N2 = omega(N2)
#     rho_c_N2 = N2_MW / V_crit_N2

#     Pr_N2 = P/P_crit_N2
#     Tr_N2 = T/T_crit_N2

#     B0 = 0.083-(0.422/(Tr_N2**1.6))
#     B1 = 0.139-(0.172/(Tr_N2**4.2))
#     B_up = B0 + (Omega_N2 * B1)

#     Z = 1 + (B0*(Pr_N2/Tr_N2)) + (Omega_N2 * B1 * (Pr_N2/Tr_N2))

#     return Z

# # for P in range(10, 150, 10):
# #     for T in range(293, 313, 1):
# #         Z = calculate_Z(P, T)
# #         print(f"{Z}")

# # Create an empty list to store results
# results = []

# # Loop over the range of P and T values
# for P in range(10, 160, 10):
#     # for T in range(293, 313, 1):
#     Z = calculate_Z(P)
#     results.append({'Pressure (P)': P, 'Z': Z})

# # Convert the results list to a pandas DataFrame
# df = pd.DataFrame(results)
# # df.to_csv('hydrogen.csv', index=False)

# # Display the table
# print(df)

print(f"Tc: {T_crit_H2S}")
print(f"Pc: {P_crit_H2S}")
print(f"Vc: {V_crit_H2S}")
# print(f"Rhoc: {rho_c_N2}")
print(f"Omega: {Omega_H2S}")

# print(f"Pr: {Pr_N2}")
# print(f"Tr: {Tr_N2}")
# print(f"B0: {B0}")
# print(f"B1: {B1}")
# print(f"B_up: {B_up}")
# print(f"Z: {Z}")
# # print(f"Tr: {}")