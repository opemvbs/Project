import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from molmass import Formula
from chemicals import MW

# Default constants
DEFAULT_CONSTANTS = {
    "cyl_volume": 40,  # L
    "fill_pressure": 150,  # bar
    "gas_constant": 0.08314,  # L.Bar/mol.g.K
    "temperature": 293,  # K
    "z_mix": 0.995,
}

# Available components
COMPONENTS = {
    "OXYGEN": "O2",
    "NITROGEN": "N2",
    "WATER": "H2O"
}

class GasCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.row = 6
        self.entries = {}
        self.component_widgets = {}
        self.component_combobox_widgets = {}
        
        # Set up the GUI
        self.root.title("Gas Weight Calculator")
        self.root.iconbitmap("images/SII.ico")
        self.setup_ui()

    def setup_ui(self):
        """Initialize the main UI elements."""
        self.setup_constants_section()
        self.setup_component_section()
        self.setup_buttons()
        self.add_initial_components()

    def setup_constants_section(self):
        """Create input fields for constants."""
        self.entries["constants"] = {}
        for idx, (label, value) in enumerate(DEFAULT_CONSTANTS.items()):
            entry = self.create_label_entry(
                label.replace("_", " ").title() + ":", value, idx, 0
            )
            self.entries["constants"][label] = entry

    def setup_component_section(self):
        """Set up the header row for component-related inputs."""
        headers = ["Component", "Percentage (%)", "Molar Mass (g/mol)", "Weight (g)"]
        for col, text in enumerate(headers):
            ctk.CTkLabel(self.root, text=text).grid(
                row=5, column=col, padx=10, pady=5
            )

    def setup_buttons(self):
        """Add buttons for various actions."""
        ctk.CTkButton(
            self.root, text="Add Component", command=self.add_new_component
        ).grid(row=4, column=4, padx=10, pady=10)
        
        ctk.CTkButton(
            self.root, text="Calculate", command=self.calculate
        ).grid(row=5, column=4, padx=10, pady=10)

        self.total_weight_label = ctk.CTkLabel(self.root, text="Total Weight: 0.0000 g")
        self.total_weight_label.grid(row=6, column=4, padx=10, pady=5)

    def create_label_entry(self, label_text, default_value, row, col):
        """Helper to create a labeled entry."""
        ctk.CTkLabel(self.root, text=label_text).grid(row=row, column=col, padx=10, pady=5)
        entry = ctk.CTkEntry(self.root)
        entry.insert(0, default_value)
        entry.grid(row=row, column=col + 1, padx=10, pady=5)
        return entry

    def add_initial_components(self):
        """Add initial components to the UI."""
        for component in COMPONENTS:
            self.add_component_widgets(component)

    def add_component_widgets(self, component_name):
        """Add widgets for a single gas component."""
        row = self.row

        # Component selection (ComboBox)
        component_selector = ctk.CTkComboBox(
            self.root, values=list(COMPONENTS.keys()), width=150
        )
        component_selector.set(component_name)
        component_selector.grid(row=row, column=0, padx=10, pady=5)

        # Percentage input
        percentage_entry = ctk.CTkEntry(self.root)
        percentage_entry.insert(0, "0.0")
        percentage_entry.grid(row=row, column=1, padx=10, pady=5)

        # Molar Mass and Weight
        molar_mass_label = ctk.CTkLabel(self.root, text="0.0000 g/mol")
        molar_mass_label.grid(row=row, column=2, padx=10, pady=5)

        weight_label = ctk.CTkLabel(self.root, text="0.0000 g")
        weight_label.grid(row=row, column=3, padx=10, pady=5)

        # Store component widgets
        self.component_widgets[component_name] = {
            "selector": component_selector,
            "percentage": percentage_entry,
            "molar_mass": molar_mass_label,
            "weight": weight_label,
        }

        # Add ComboBox to the dedicated dictionary for updating
        self.component_combobox_widgets[component_name] = component_selector

        self.row += 1

    def add_new_component(self):
        """Add a new component dynamically through a popup."""
        def submit_new_component():
            name = new_name_entry.get().strip().upper()
            formula = new_formula_entry.get().strip()

            if not name or not formula:
                CTkMessagebox(title="Input Error",
                              message="Both name and formula are required!",
                              icon="cancel")
                return

            COMPONENTS[name] = formula
            self.update_combobox_values()
            self.add_component_widgets(name)
            popup.destroy()
            
            CTkMessagebox(title="Success",
                          message=f"Component '{name}' added successfully!",
                          icon="check")

        popup = ctk.CTkToplevel(self.root)
        popup.title("Add New Component")
        popup.attributes('-topmost', 'true')

        ctk.CTkLabel(popup, text="Component Name:").grid(row=0, column=0, padx=10, pady=5)
        new_name_entry = ctk.CTkEntry(popup)
        new_name_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(popup, text="Component Formula:").grid(row=1, column=0, padx=10, pady=5)
        new_formula_entry = ctk.CTkEntry(popup)
        new_formula_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(popup, text="Submit", command=submit_new_component).grid(
            row=2, column=0, columnspan=2, pady=10
        )
        
    def update_combobox_values(self):
        """Update the ComboBox values with the latest components."""
        # Get the updated list of component names
        component_names = list(COMPONENTS.keys())
        
        # Update each ComboBox with the new values
        for combobox in self.component_combobox_widgets.values():
            combobox.configure(values=component_names)

    def calculate(self):
        """Calculate weights for all components and display the results."""
        try:
            constants = {
                key: float(entry.get())
                for key, entry in self.entries["constants"].items()
            }
            total_percentage = 0
            total_weight = 0

            for component_name, widgets in self.component_widgets.items():
                selector = widgets["selector"]
                percentage = float(widgets["percentage"].get())
                gas = selector.get()

                if gas not in COMPONENTS or not (0 <= percentage <= 100):
                    raise ValueError(f"Invalid input for {component_name}")

                total_percentage += percentage

                formula = Formula(COMPONENTS[gas])
                molar_mass = formula.mass
                weight = (
                    constants["fill_pressure"]
                    * constants["cyl_volume"]
                    * percentage
                    * molar_mass
                    / (constants["z_mix"] * constants["gas_constant"] * constants["temperature"] * 100)
                )

                # Update labels
                widgets["molar_mass"].configure(text=f"{molar_mass:.4f} g/mol")
                widgets["weight"].configure(text=f"{weight:.4f} g")
                total_weight += weight

            if total_percentage > 0 and total_percentage != 100:
                raise ValueError("Total percentage of all components must equal 100.")
            
            if total_percentage == 0:
                return

            self.total_weight_label.configure(text=f"Total Weight: {total_weight:.4f} g")

        except ValueError as e:
            CTkMessagebox(title="Calculation Error",
                          message="str(e)",
                          icon="cancel")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    app = GasCalculatorApp(root)
    root.mainloop()
