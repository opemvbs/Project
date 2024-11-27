from chemicals import Tc, Pc, Vc, omega
from chemicals import CAS_from_any
from chemicals import MW

COMP = CAS_from_any("nitrogen")
P = 150
T = 293

T_crit = Tc(COMP)
P_crit = Pc(COMP) / 101300

Omega = omega(COMP)

Pr = P/P_crit
Tr = T/T_crit

B0 = 0.083-(0.422/(Tr**1.6))
B1 = 0.139-(0.172/(Tr**4.2))
B_up = B0 + (Omega * B1)

Z = 1 + (B0*(Pr/Tr)) + (Omega * B1 * (Pr/Tr))

print(f"Z: {Z}")