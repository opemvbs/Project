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

# Available gases (can be expanded as needed)
COMPONENTS = {
    "OXYGEN": 'O2',
    "NITROGEN": 'N2',
    # You can add more components here
    "ARGON": 'Ar',
    "CARBON_DIOXIDE": 'CO2'
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

# Function to add components dynamically
def add_component_widgets(component_name, row):
    # Label for component percentage
    label_percent = ctk.CTkLabel(root, text=f"{component_name} Percentage (%):")
    label_percent.grid(row=row, column=0, padx=10, pady=5)
    
    entry_percent = ctk.CTkEntry(root)
    entry_percent.insert(0, "0.0")  # Default value
    entry_percent.grid(row=row, column=1, padx=10, pady=5)
    entry_percent_widgets[component_name] = entry_percent
    
    # Combobox for selecting component
    label_component = ctk.CTkLabel(root, text=f"{component_name} Component:")
    label_component.grid(row=row + 1, column=0, padx=10, pady=5)
    
    component_combobox = ctk.CTkComboBox(root, values=list(COMPONENTS.keys()))
    component_combobox.set(component_name)  # Default to the name of the component
    component_combobox.grid(row=row + 1, column=1, padx=10, pady=5)
    component_combobox_widgets[component_name] = component_combobox

# Function to calculate the weights of all components and show results
def calculate():
    try:
        # Get user inputs for the constants
        volume = float(entry_volume.get())
        pressure = float(entry_pressure.get())
        temperature = float(entry_temperature.get())
        gas_constant = float(entry_gas_constant.get())
        z_mix = float(entry_z_mix.get())
        
        total_percent = 0
        component_weights = {}
        
        # Loop through the components and calculate the weight for each one
        for component_name in entry_percent_widgets.keys():
            percent = float(entry_percent_widgets[component_name].get())
            if percent < 0 or percent > 100:
                raise ValueError(f"{component_name} percentage must be between 0 and 100.")
            
            total_percent += percent
            if total_percent > 100:
                raise ValueError("Total percentage of all components cannot exceed 100.")
            
            # Get the selected component for this entry
            selected_component = component_combobox_widgets[component_name].get()
            
            # Calculate the weight of the component
            weight = calculated_weight(selected_component, percent, volume, pressure, gas_constant, temperature, z_mix)
            component_weights[component_name] = weight
        
        # Display results
        label_total_weight.configure(text=f"Total Weight: {sum(component_weights.values()):.4f} g")
        
        # Update the weight labels for each component dynamically
        for component_name, weight in component_weights.items():
            component_label = globals().get(f"label_{component_name.lower()}_weight")
            if component_label:
                component_label.configure(text=f"{component_name} Weight: {weight:.4f} g")
        
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

# Create dictionaries to store dynamic widgets
entry_percent_widgets = {}
component_combobox_widgets = {}

# Dynamically add components (you can add more by modifying COMPONENTS)
row = 5
for component in COMPONENTS:
    add_component_widgets(component, row)
    row += 2  # Move to next available row for the next component

# Calculate Button
button_calculate = ctk.CTkButton(root, text="Calculate", command=calculate)
button_calculate.grid(row=row, column=0, columnspan=2, padx=10, pady=10)

# Results Labels for each component dynamically
for component in COMPONENTS:
    globals()[f"label_{component.lower()}_weight"] = ctk.CTkLabel(root, text=f"{component} Weight: 0.0000 g")
    globals()[f"label_{component.lower()}_weight"].grid(row=row + 1, column=0, columnspan=2, padx=10, pady=5)
    row += 1

label_total_weight = ctk.CTkLabel(root, text="Total Weight: 0.0000 g")
label_total_weight.grid(row=row+1, column=0, columnspan=2, padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()
