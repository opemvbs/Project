import customtkinter as ctk
import numpy as np
from CTkMessagebox import CTkMessagebox
from molmass import Formula
from chemicals import Tc, Pc, omega, CAS_from_any

# Default constants
DEFAULT_CONSTANTS = {
    "cyl_volume": 40,  # L
    "fill_pressure": 150,  # bar
    "gas_constant": 0.08314,  # L.Bar/mol.g.K
    "temperature": 293,  # K
    "z_mix": 1,  # This will be replaced with calculated Z later
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
        self.row = 6  # Initial row
        self.col = 0  # Initial column for headers or labels
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
                label.replace("_", " ").title() + ":", value
            )
            self.entries["constants"][label] = entry

    def setup_component_section(self):
        """Set up the header row for component-related inputs."""
        headers = ["Component", "Z", "Percentage (%)", "Z x comp", "Molar Mass (g/mol)", "Weight (g)"]
        for col, text in enumerate(headers):
            ctk.CTkLabel(self.root, text=text).grid(
                row=self.row, column=self.col + col, padx=10, pady=5
            )
        self.row += 1  # Move to the next row after headers

    def setup_buttons(self):
        """Add buttons for various actions."""
        ctk.CTkButton(
            self.root, text="Add Component", command=self.add_new_component
        ).grid(row=self.row, column=self.col + 6, padx=10, pady=10)

        ctk.CTkButton(
            self.root, text="Calculate", command=self.calculate
        ).grid(row=self.row, column=self.col + 6, padx=10, pady=10)

        self.row += 1  # Move to the next row for total weight label

        self.total_weight_label = ctk.CTkLabel(self.root, text="Total Weight: 0.0000 g")
        self.total_weight_label.grid(row=self.row, column=self.col + 6, padx=10, pady=5)

    def create_label_entry(self, label_text, default_value):
        """Helper to create a labeled entry.""" 
        ctk.CTkLabel(self.root, text=label_text).grid(row=self.row, column=self.col, padx=10, pady=5)
        entry = ctk.CTkEntry(self.root)
        entry.insert(0, default_value)
        entry.grid(row=self.row, column=self.col + 1, padx=10, pady=5)
        self.row += 1  # Move to the next row after each entry
        return entry

    def add_initial_components(self):
        """Add initial components to the UI."""
        for component in COMPONENTS:
            self.add_component_widgets(component)

    def add_component_widgets(self, component_name):
        """Add widgets for a single gas component."""
        row = self.row  # Store current row

        # Component selection (ComboBox)
        component_selector = ctk.CTkComboBox(
            self.root, values=list(COMPONENTS.keys()), width=150
        )
        component_selector.set(component_name)
        component_selector.grid(row=row, column=self.col, padx=10, pady=5)

        # Percentage input
        percentage_entry = ctk.CTkEntry(self.root)
        percentage_entry.insert(0, "0.0")
        percentage_entry.grid(row=row, column=self.col + 2, padx=10, pady=5)

        # Z compressibility
        z_comp_factor = ctk.CTkLabel(self.root, text="0.0000")
        z_comp_factor.grid(row=row, column=self.col + 1, padx=10, pady=5)

        # Molar Mass and Weight
        molar_mass_label = ctk.CTkLabel(self.root, text="0.0000 g/mol")
        molar_mass_label.grid(row=row, column=self.col + 4, padx=10, pady=5)

        weight_label = ctk.CTkLabel(self.root, text="0.0000 g")
        weight_label.grid(row=row, column=self.col + 5, padx=10, pady=5)

        # Store component widgets
        self.component_widgets[component_name] = {
            "selector": component_selector,
            "percentage": percentage_entry,
            "molar_mass": molar_mass_label,
            "weight": weight_label,
        }

        # Add ComboBox to the dedicated dictionary for updating
        self.component_combobox_widgets[component_name] = component_selector

        self.row += 1  # Move to the next row after adding a component widget

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
        component_names = list(COMPONENTS.keys())
        for combobox in self.component_combobox_widgets.values():
            combobox.configure(values=component_names)

    def calculate_mixture_props(self, components, mole_fractions):
        """Calculate mixture properties (Tc, Pc, omega) using mixing rules."""
        if len(components) != len(mole_fractions):
            raise ValueError("Number of components must match number of mole fractions.")
        if not np.isclose(sum(mole_fractions), 1.0, atol=1e-6):
            raise ValueError("Mole fractions must sum to 1.")

        # Calculate mixture critical temperature (Tc) using linear rule
        T_crit_mix = sum(x * Tc(CAS_from_any(c)) for c, x in zip(components, mole_fractions))

        # Calculate mixture critical pressure (Pc) using geometric mean for binary interactions
        P_crit_mix = 0
        for i, (c1, x_i) in enumerate(zip(components, mole_fractions)):
            for j, (c2, x_j) in enumerate(zip(components, mole_fractions)):
                if i <= j:  # Avoid redundant calculations
                    P_crit_mix += 2 * x_i * x_j * np.sqrt(Pc(CAS_from_any(c1)) * Pc(CAS_from_any(c2)))
        P_crit_mix /= 2  # Final averaging
        P_crit_mix /= 100000  # Convert from Pa to bar

        # Calculate mixture acentric factor (omega) using linear rule
        omega_mix = sum(x * omega(CAS_from_any(c)) for c, x in zip(components, mole_fractions))

        return T_crit_mix, P_crit_mix, omega_mix

    def calculate(self):
        """Perform the gas weight calculation."""
        components = []
        mole_fractions = []

        # Collect components and mole fractions
        for component_name, widget_set in self.component_widgets.items():
            selected_component = widget_set["selector"].get()
            try:
                mole_fraction = float(widget_set["percentage"].get()) / 100
            except ValueError:
                mole_fraction = 0.0  # Handle invalid input

            # Add the correct component formula to the components list
            components.append(COMPONENTS.get(selected_component, selected_component))
            mole_fractions.append(mole_fraction)

        # Ensure mole fractions sum to 1
        if not np.isclose(sum(mole_fractions), 1.0, atol=1e-6):
            CTkMessagebox(
                title="Input Error",
                message="Mole fractions must sum to 1.",
                icon="cancel"
            )
            return

        # Retrieve constants
        R = float(self.entries["constants"]["gas_constant"].get())  # Gas constant
        T = float(self.entries["constants"]["temperature"].get())  # Temperature (K)
        P = float(self.entries["constants"]["fill_pressure"].get())  # Pressure (bar)
        V = float(self.entries["constants"]["cyl_volume"].get())  # Volume (L)

        # Calculate total number of moles using the ideal gas law
        total_moles = (P * V) / (R * T)

        # Calculate mixture properties (Tc, Pc, omega)
        T_crit_mix, P_crit_mix, omega_mix = self.calculate_mixture_props(components, mole_fractions)

        # Calculate Z mix using the Pitzer correlation
        def calculate_Z_pitzer(P, T, T_crit, P_crit, omega_value):
            Tr = T / T_crit
            Pr = P / P_crit

            B0 = 0.083 - 0.422 / (Tr ** 1.6)
            B1 = 0.139 - 0.172 / (Tr ** 4.2)
            B = B0 + omega_value * B1

            return 1 + B * (Pr / Tr)

        Z_mix = calculate_Z_pitzer(P, T, T_crit_mix, P_crit_mix, omega_mix)
        self.entries["constants"]["z_mix"].delete(0, ctk.END)
        self.entries["constants"]["z_mix"].insert(0, f"{Z_mix:.4f}")

        # Adjust total moles for compressibility factor
        total_moles /= Z_mix

        # Update weight labels for each component
        total_weight = 0.0
        for component_name, widget_set in self.component_widgets.items():
            selected_component = widget_set["selector"].get()
            component_formula = COMPONENTS.get(selected_component, selected_component)  # Get the formula
            molar_mass = Formula(component_formula).mass
            widget_set["molar_mass"].configure(text=f"{molar_mass:.4f} g/mol")

            # Calculate the weight of the component
            moles_component = total_moles * mole_fractions[components.index(component_formula)]
            weight = moles_component * molar_mass
            widget_set["weight"].configure(text=f"{weight:.4f} g")
            total_weight += weight

        # Update the total weight display
        self.total_weight_label.configure(text=f"Total Weight: {total_weight:.4f} g")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    app = GasCalculatorApp(root)
    root.mainloop()
