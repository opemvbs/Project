import customtkinter as ctk
from tkinter import ttk, messagebox
from molmass import Formula

# Default constants
DEFAULT_CYL_VOLUME = 40  # L
DEFAULT_FILL_PRESSURE = 150  # bar
DEFAULT_GAS_CONSTANT = 0.08314  # L.Bar/mol.g.K
DEFAULT_TEMPERATURE = 293  # K
DEFAULT_Z_MIX = 0.995

# Available gases (can be expanded dynamically)
COMPONENTS = {
    "OXYGEN": 'O2',
    "NITROGEN": 'N2',
}

class GasCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.row = 6
        self.entry_percent_widgets = {}
        self.component_combobox_widgets = {}

        # Set up the GUI window
        self.root.title("Gas Weight Calculator")
        self.root.iconbitmap('images/SII.ico')
        self.setup_ui()

    def setup_ui(self):
        # Create and place widgets for constants
        self.entry_volume = self.create_label_entry("Cylinder Volume (L):", DEFAULT_CYL_VOLUME, 0, 0)
        self.entry_pressure = self.create_label_entry("Pressure (bar):", DEFAULT_FILL_PRESSURE, 1, 0)
        self.entry_temperature = self.create_label_entry("Temperature (K):", DEFAULT_TEMPERATURE, 2, 0)
        self.entry_gas_constant = self.create_label_entry("Gas Constant (L.Bar/mol.g.K):", DEFAULT_GAS_CONSTANT, 3, 0)
        self.entry_z_mix = self.create_label_entry("Z Mix (Compression Factor):", DEFAULT_Z_MIX, 4, 0)

        # Component and weight headers
        self.create_component_headers()

        # Dynamically add initial components (can be expanded)
        for component in COMPONENTS:
            self.add_component_widgets(component)

        # Buttons
        self.add_buttons()

    def create_label_entry(self, label_text, default_value, row, col):
        label = ctk.CTkLabel(self.root, text=label_text)
        label.grid(row=row, column=col, padx=10, pady=5)
        entry = ctk.CTkEntry(self.root)
        entry.insert(0, default_value)
        entry.grid(row=row, column=col + 1, padx=10, pady=5)
        return entry

    def create_component_headers(self):
        ctk.CTkLabel(self.root, text="Component").grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        ctk.CTkLabel(self.root, text="Percentage (%)").grid(row=5, column=3, padx=10, pady=5)
        ctk.CTkLabel(self.root, text="Molar Mass").grid(row=5, column=4, columnspan=1, padx=10, pady=5)
        ctk.CTkLabel(self.root, text="Weight").grid(row=5, column=6, columnspan=2, padx=10, pady=5)
        

    def add_buttons(self):
        # Add new component button
        button_add_component = ctk.CTkButton(self.root, text="Add Component", command=self.add_new_component)
        button_add_component.grid(row=4, column=8, columnspan=2, padx=10, pady=10)

        # Calculate button
        button_calculate = ctk.CTkButton(self.root, text="Calculate", command=self.calculate)
        button_calculate.grid(row=5, column=8, columnspan=2, padx=10, pady=10)

        # Total weight label
        self.label_total_weight = ctk.CTkLabel(self.root, text="Total Weight: 0.0000 g")
        self.label_total_weight.grid(row=6, column=8, columnspan=1, padx=10, pady=5)

    def add_component_widgets(self, component_name):
        """Add the dynamic widgets for each component."""
        entry_percent = ctk.CTkEntry(self.root)
        entry_percent.insert(0, "0.0")
        entry_percent.grid(row=self.row, column=3, padx=10, pady=5)
        self.entry_percent_widgets[component_name] = entry_percent

        # label_component = ctk.CTkLabel(self.root, text=f"{component_name} :")
        # label_component.grid(row=self.row, column=0, padx=10, pady=5)

        component_combobox = ctk.CTkComboBox(self.root, values=list(COMPONENTS.keys()), width=300)
        component_combobox.set(component_name)
        component_combobox.grid(row=self.row, column=0, columnspan=2, padx=10, pady=5)
        self.component_combobox_widgets[component_name] = component_combobox

        label_molarmass = ctk.CTkLabel(self.root, text=f"0.0000 g/mol")
        label_molarmass.grid(row=self.row, column=4, columnspan=2, padx=10, pady=5)
        setattr(self, f"label_{component_name.lower()}_molarmass", label_molarmass)

        label_weight = ctk.CTkLabel(self.root, text=f"0.0000 g")
        label_weight.grid(row=self.row, column=6, columnspan=2, padx=10, pady=5)
        setattr(self, f"label_{component_name.lower()}_weight", label_weight)

        self.row += 3

    def add_new_component(self):
        """Add a new component dynamically."""
        def submit_new_component():
            component_name = entry_new_component_name.get().strip().upper()
            component_formula = entry_new_component_formula.get().strip()

            if not component_name or not component_formula:
                messagebox.showerror("Input Error", "Both name and formula are required!")
                return

            # Add new component to the COMPONENTS dictionary
            COMPONENTS[component_name] = component_formula

            # Update the ComboBox values for all components
            self.update_combobox_values()

            # Add component widgets for the new component
            self.add_component_widgets(component_name)

            # Clear entry fields
            entry_new_component_name.delete(0, ctk.END)
            entry_new_component_formula.delete(0, ctk.END)

            messagebox.showinfo("Success", f"Component {component_name} added successfully!")

        popup = ctk.CTkToplevel(self.root)
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

    def update_combobox_values(self):
        """Update the ComboBox values with the latest components."""
        # Get the updated list of component names
        component_names = list(COMPONENTS.keys())
        
        # Update each ComboBox with the new values
        for combobox in self.component_combobox_widgets.values():
            combobox.configure(values=component_names)


    def calculate(self):
        """Calculate the weights of all components and show results."""
        try:
            # Get user inputs for constants
            volume = float(self.entry_volume.get())
            pressure = float(self.entry_pressure.get())
            temperature = float(self.entry_temperature.get())
            gas_constant = float(self.entry_gas_constant.get())
            z_mix = float(self.entry_z_mix.get())

            total_percent = 0
            component_weights = {}

            for component_name in self.entry_percent_widgets.keys():
                percent = float(self.entry_percent_widgets[component_name].get())
                if not 0 <= percent <= 100:
                    raise ValueError(f"{component_name} percentage must be between 0 and 100.")

                total_percent += percent
                if total_percent > 100:
                    raise ValueError("Total percentage of all components cannot exceed 100.")

                # Get the selected component for this entry
                selected_component = self.component_combobox_widgets[component_name].get()

                # Calculate the weight of the component
                weight, molarmass = self.calculated_weight(selected_component, percent, volume, pressure, gas_constant, temperature, z_mix)
                component_weights[component_name] = weight, molarmass

            # Display results
            # self.label_total_weight.configure(text=f"Total Weight: {sum(component_weights.values()):.4f} g")
            self.label_total_weight.configure(text=f"Total Weight: {sum(weight for weight, _ in component_weights.values()):.4f} g")


            # Update the weight and molar mass labels for each component
            for component_name, (weight, molarmass) in component_weights.items():
                mass_label = getattr(self, f"label_{component_name.lower()}_molarmass")
                mass_label.configure(text=f"{molarmass:.4f} g/mol")
                weight_label = getattr(self, f"label_{component_name.lower()}_weight")
                weight_label.configure(text=f"{weight:.4f} g")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def calculated_weight(self, component, percent_mol, volume, pressure, constant, temperature, z_mix):
        """Calculate the weight of a given component."""
        formula = COMPONENTS.get(component)
        if not formula:
            raise ValueError(f"Unknown component: {component}")
        molar_mass = Formula(formula).mass
        return pressure * volume * percent_mol * molar_mass / (z_mix * constant * temperature * 100), molar_mass

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    app = GasCalculatorApp(root)
    root.mainloop()
