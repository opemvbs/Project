from molmass import Formula

CYL_VOLUME = 40 # L
FILL_PRESSURE = 150 # bar
GAS_CONSTANT = 0.08314 # L.Bar/mol.g.K
TEMPERATURE = 295 # K
Z_MIX = 0.995

COMPONENT = {
    "OXYGEN"    : Formula('O2'),
    "NITROGEN"  : Formula('N2'),
}

molar_masses = {component: formula.mass for component, formula in COMPONENT.items()}
# print(molar_masses)

PERCENT_MOL_TARGET = {
    "OXYGEN"    : 0.0008,
    "NITROGEN"  : 99.9992,
}

def calculated_weight(component, percent_mol, volume=CYL_VOLUME, pressure=FILL_PRESSURE, constant=GAS_CONSTANT, temperature=TEMPERATURE, z_mix=Z_MIX):
    molar_mass = Formula(component).mass
    
    weight = pressure * volume * percent_mol * molar_mass / (z_mix * constant * temperature * 100)
    return weight

oxygen_weight = calculated_weight("O2", 0.0008)
print(oxygen_weight)
nitrogen_weight = calculated_weight("N2", 99.9992)
print(nitrogen_weight)

# TODO
# Calculate vapor pressure using Clausius-Clapeyron 

