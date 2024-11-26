from chemicals import CAS_from_any
from chemicals import Tc, Pc, omega
from chemicals import Lee_Kesler
from chemicals import Ambrose_Walton
from chemicals import Sanjari


def get_parameter(component):
    T_crit = Tc(component)
    P_crit = Pc(component)
    O_comp  = omega(component)
    return T_crit, P_crit, O_comp

def calculate(component, T):
    T_crit, P_crit, O_comp = get_parameter(component)
    vappres_LK = Lee_Kesler(T, T_crit, P_crit, O_comp)
    vappres_AW = Ambrose_Walton(T, T_crit, P_crit, O_comp)
    vappres_S  = Sanjari(T, T_crit, P_crit, O_comp)
    return vappres_LK, vappres_AW, vappres_S

CAS = CAS_from_any('carbon monoxide')
T = 293

Pv_LK, Pv_AW, Pv_S = calculate(CAS, T)
print(Pv_LK * 1.450377e-4)
print(Pv_AW * 1.450377e-4)
print(Pv_S * 1.450377e-4)
# print(Pv_S / 6895)