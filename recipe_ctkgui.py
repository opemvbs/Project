import customtkinter as ctk
from tkinter import ttk, messagebox
from molmass import Formula

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

# Default constants
DEFAULT_CYL_VOLUME = 40  # L
DEFAULT_FILL_PRESSURE = 150  # bar
DEFAULT_GAS_CONSTANT = 0.08314  # L.Bar/mol.g.K
DEFAULT_TEMPERATURE = 295  # K
DEFAULT_Z_MIX = 0.995

# Available gases (can be expanded dynamically)
COMPONENTS = {
    "OXYGEN": 'O2',
    "NITROGEN": 'N2',
    # More components can be added by the user via the app
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

# Function to add new components dynamically
def add_new_component():
    def submit_new_component():
        component_name = entry_new_component_name.get().strip().upper()
        component_formula = entry_new_component_formula.get().strip().upper()

        if not component_name or not component_formula:
            messagebox.showerror("Input Error", "Both name and formula are required!")
            return

        # Add the new component to the dictionary
        COMPONENTS[component_name] = component_formula

        # Refresh the UI by adding entry fields for this new component
        add_component_widgets(component_name)

        # Clear the entry fields for new component inputs
        entry_new_component_name.delete(0, ctk.END)
        entry_new_component_formula.delete(0, ctk.END)

        messagebox.showinfo("Success", f"Component {component_name} added successfully!")

    # Create the popup window to enter the new component
    popup = ctk.CTkToplevel(root)
    popup.title("Add New Component")

    label_name = ctk.CTkLabel(popup, text="Component Name:")
    label_name.grid(row=0, column=0, padx=10, pady=5)
    entry_new_component_name = ctk.CTkEntry(popup)
    entry_new_component_name.grid(row=0, column=1, padx=10, pady=5)

    label_formula = ctk.CTkLabel(popup, text="Component Formula:")
    label_formula.grid(row=1, column=0, padx=10, pady=5)
    entry_new_component_formula = ctk.CTkEntry(popup)
    entry_new_component_formula.grid(row=1, column=1, padx=10, pady=5)

    button_submit = ctk.CTkButton(popup, text="Submit", command=submit_new_component)
    button_submit.grid(row=1, column=5, columnspan=2, padx=10, pady=10)

# Function to add component widgets dynamically
def add_component_widgets(component_name):
    global row
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

    # Add the weight label dynamically for the new component
    globals()[f"label_{component_name.lower()}_weight"] = ctk.CTkLabel(root, text=f"{component_name} Weight: 0.0000 g")
    globals()[f"label_{component_name.lower()}_weight"].grid(row=row + 2, column=0, columnspan=2, padx=10, pady=5)
    
    row += 3  # Update row for the next component

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
root.iconbitmap('images/SII.ico')

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

# Dynamically add initial components (you can add more by clicking "Add Component")
row = 5
for component in COMPONENTS:
    add_component_widgets(component)

# Button to add new component
button_add_component = ctk.CTkButton(root, text="Add Component", command=add_new_component)
button_add_component.grid(row=row, column=0, columnspan=2, padx=10, pady=10)

# Calculate Button
button_calculate = ctk.CTkButton(root, text="Calculate", command=calculate)
button_calculate.grid(row=row + 1, column=0, columnspan=2, padx=10, pady=10)

# Total weight label
label_total_weight = ctk.CTkLabel(root, text="Total Weight: 0.0000 g")
label_total_weight.grid(row=row + 2, column=0, columnspan=2, padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()
