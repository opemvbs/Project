import customtkinter as ctk
from tkinter import ttk, messagebox
from molmass import Formula

ctk.set_appearance_mode("dark")

# Default constants
DEFAULT_CYL_VOLUME = 40  # L
DEFAULT_FILL_PRESSURE = 150  # bar
DEFAULT_GAS_CONSTANT = 0.08314  # L.Bar/mol.g.K
DEFAULT_TEMPERATURE = 295  # K
DEFAULT_Z_MIX = 0.995

# Available gases
COMPONENTS = {
    "OXYGEN": 'O2',  # Chemical formula for Oxygen
    "NITROGEN": 'N2',  # Chemical formula for Nitrogen
}

# Function to calculate molar mass
def get_molar_mass(component):
    formula = COMPONENTS.get(component)
    if formula:
        return Formula(formula).mass
    else:
        raise ValueError(f"Unknown component: {component}")

# Function to calculate weight
def calculated_weight(component, percent_mol, volume, pressure, constant, temperature, z_mix):
    molar_mass = get_molar_mass(component)
    weight = pressure * volume * percent_mol * molar_mass / (z_mix * constant * temperature * 100)
    return weight

# Calculate the weights of gases and show results
def calculate():
    try:
        # Get user inputs
        oxygen_percent = float(entry_oxygen.get())
        nitrogen_percent = float(entry_nitrogen.get())
        volume = float(entry_volume.get())
        pressure = float(entry_pressure.get())
        temperature = float(entry_temperature.get())
        gas_constant = float(entry_gas_constant.get())
        z_mix = float(entry_z_mix.get())
        
        if oxygen_percent + nitrogen_percent != 100.0:
            raise ValueError("Oxygen and Nitrogen percentages must sum to 100.")
        
        # Get the selected components
        oxygen_component = component_oxygen.get()
        nitrogen_component = component_nitrogen.get()
        
        # Calculate the weight of oxygen and nitrogen
        oxygen_weight = calculated_weight(oxygen_component, oxygen_percent , volume, pressure, gas_constant, temperature, z_mix)
        nitrogen_weight = calculated_weight(nitrogen_component, nitrogen_percent , volume, pressure, gas_constant, temperature, z_mix)
        
        # Display results
        label_oxygen_weight.configure(text=f"Oxygen Weight: {oxygen_weight:.4f} g")
        label_nitrogen_weight.configure(text=f"Nitrogen Weight: {nitrogen_weight:.4f} g")
        label_total_weight.configure(text=f"Total Weight: {oxygen_weight + nitrogen_weight:.4f} g")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Set up the GUI window
root = ctk.CTk()
root.title("Gas Weight Calculator")

# Create and place widgets for constants
label_volume = ctk.CTkLabel(root, text="Cylinder Volume (L):")
label_volume.grid(row=0, column=0, padx=10, pady=5)
entry_volume = ctk.CTkEntry(root)
entry_volume.insert(0, DEFAULT_CYL_VOLUME)
entry_volume.grid(row=0, column=1, padx=10, pady=5)

label_pressure = ctk.CTkLabel(root, text="Pressure (bar):")
label_pressure.grid(row=1, column=0, padx=10, pady=5)
entry_pressure = ctk.CTkEntry(root)
entry_pressure.insert(0, DEFAULT_FILL_PRESSURE)
entry_pressure.grid(row=1, column=1, padx=10, pady=5)

label_temperature = ctk.CTkLabel(root, text="Temperature (K):")
label_temperature.grid(row=2, column=0, padx=10, pady=5)
entry_temperature = ctk.CTkEntry(root)
entry_temperature.insert(0, DEFAULT_TEMPERATURE)
entry_temperature.grid(row=2, column=1, padx=10, pady=5)

label_gas_constant = ctk.CTkLabel(root, text="Gas Constant (L.Bar/mol.g.K):")
label_gas_constant.grid(row=3, column=0, padx=10, pady=5)
entry_gas_constant = ctk.CTkEntry(root)
entry_gas_constant.insert(0, DEFAULT_GAS_CONSTANT)
entry_gas_constant.grid(row=3, column=1, padx=10, pady=5)

label_z_mix = ctk.CTkLabel(root, text="Z Mix (Compression Factor):")
label_z_mix.grid(row=4, column=0, padx=10, pady=5)
entry_z_mix = ctk.CTkEntry(root)
entry_z_mix.insert(0, DEFAULT_Z_MIX)
entry_z_mix.grid(row=4, column=1, padx=10, pady=5)

# Create and place widgets for gas components and percentages
label_oxygen_percent = ctk.CTkLabel(root, text="Oxygen Percentage (%):")
label_oxygen_percent.grid(row=5, column=0, padx=10, pady=5)
entry_oxygen = ctk.CTkEntry(root)
entry_oxygen.insert(0, "0.0008")
entry_oxygen.grid(row=5, column=1, padx=10, pady=5)

label_nitrogen_percent = ctk.CTkLabel(root, text="Nitrogen Percentage (%):")
label_nitrogen_percent.grid(row=6, column=0, padx=10, pady=5)
entry_nitrogen = ctk.CTkEntry(root)
entry_nitrogen.insert(0, "99.9992")
entry_nitrogen.grid(row=6, column=1, padx=10, pady=5)

# Create combobox for selecting gas components
label_oxygen_component = ctk.CTkLabel(root, text="Oxygen Component:")
label_oxygen_component.grid(row=7, column=0, padx=10, pady=5)
component_oxygen = ctk.CTkComboBox(root, values=list(COMPONENTS.keys()))
component_oxygen.set("OXYGEN")
component_oxygen.grid(row=7, column=1, padx=10, pady=5)

label_nitrogen_component = ctk.CTkLabel(root, text="Nitrogen Component:")
label_nitrogen_component.grid(row=8, column=0, padx=10, pady=5)
component_nitrogen = ctk.CTkComboBox(root, values=list(COMPONENTS.keys()))
component_nitrogen.set("NITROGEN")
component_nitrogen.grid(row=8, column=1, padx=10, pady=5)

# Calculate Button
button_calculate = ctk.CTkButton(root, text="Calculate", command=calculate)
button_calculate.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Results Labels
label_oxygen_weight = ctk.CTkLabel(root, text="Oxygen Weight: 0.0000 g")
label_oxygen_weight.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

label_nitrogen_weight = ctk.CTkLabel(root, text="Nitrogen Weight: 0.0000 g")
label_nitrogen_weight.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

label_total_weight = ctk.CTkLabel(root, text="Total Weight: 0.0000 g")
label_total_weight.grid(row=12, column=0, columnspan=2, padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()
