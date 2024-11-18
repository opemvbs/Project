# Filling record

from molmass import Formula

# Component
COMPONENT = {
    "SULPHUR_DIOXIDE": Formula('SO2'),
    "CARBON_MONOXIDE": Formula('CO'),
    "CARBON_DIOXIDE" : Formula('CO2'),
    "NITROGEN"       : Formula('N2'),
}

molar_masses = {component: formula.mass for component, formula in COMPONENT.items()}
# for component, formula in COMPONENT.items():
#     print(f"{component:<20s}: {formula.mass:} g/mol")
print(molar_masses)

WEIGHTS = {
    "SULPHUR_DIOXIDE": 2.521,
    "CARBON_MONOXIDE": 1.261,
    "CARBON_DIOXIDE" : 923.067,
    "NITROGEN"       : 3082.226,
}

moles = {component: WEIGHTS[component] / COMPONENT[component].mass for component in WEIGHTS}
print(moles)

total_moles = sum(moles.values())

percent_moles = {component: moles[component] / total_moles * 100 for component in moles}
print(percent_moles)

ppm_moles = {component: percent_moles[component] * 10000 for component in percent_moles}
print(ppm_moles)
