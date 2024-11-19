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
print(molar_masses)

PERCENT_MOL_TARGET = {
    "SULPHUR_DIOXIDE": 0.03002,
    "CARBON_MONOXIDE": 0.03433,
    "CARBON_DIOXIDE" : 16,
    "NITROGEN"       : 83.93565,
}

WEIGHTS = {
    "SULPHUR_DIOXIDE": 2.641,
    "CARBON_MONOXIDE": 1.315,
    "CARBON_DIOXIDE" : 923.0,
    "NITROGEN"       : 3053.944,
}

actual_moles = {component: WEIGHTS[component] / COMPONENT[component].mass for component in WEIGHTS}
# print(actual_moles)

total_moles = sum(actual_moles.values())

percent_moles = {component: actual_moles[component] / total_moles * 100 for component in actual_moles}
print(percent_moles)

ppm_moles = {component: percent_moles[component] * 10000 for component in percent_moles}
# print(ppm_moles)

blending_tolerance = {component: round((percent_moles[component] / PERCENT_MOL_TARGET[component] - 1) * 100, 5) for component in PERCENT_MOL_TARGET}
print(blending_tolerance)

print(Formula('C2H4O').mass)

# TODO
# Make premix database