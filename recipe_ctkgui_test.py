import customtkinter as ctk
import numpy as np
from CTkMessagebox import CTkMessagebox
from molmass import Formula
from chemicals import Tc, Pc, omega, CAS_from_any
import os
import json
import tkinter.filedialog as fd

# Default constants
DEFAULT_CONSTANTS = {
    "cyl_volume": 40,  # L
    "fill_pressure": 150,  # bar
    "gas_constant": 0.08314,  # L.Bar/mol.g.K
    "temperature": 293,  # K
    "z_mix": 1,  # This will be replaced with calculated Z later
}

CONFIG_FILE = "components_config.json"

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as file:
        COMPONENTS = json.load(file)
else:
    COMPONENTS = {
        "OXYGEN": "O2",
        "NITROGEN": "N2",
        "WATER": "H2O"
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(COMPONENTS, file, indent=4)

def save_components_to_file():
    with open(CONFIG_FILE, "w") as file:
        json.dump(COMPONENTS, file, indent=4)

class GasCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.row = 0
        self.col = 0
        self.entries = {}
        self.component_widgets = {}  # {component_name: {widget_name: widget, ...}}
        self.component_combobox_widgets = {}

        self.root.title("Gas Weight Calculator")
        self.root.iconbitmap("images/SII.ico")
        self.setup_ui()

    def setup_ui(self):
        self.setup_constants_section()
        self.setup_component_section()
        self.setup_buttons()
        self.add_initial_components()

    def setup_constants_section(self):
        self.entries["constants"] = {}
        for idx, (label, value) in enumerate(DEFAULT_CONSTANTS.items()):
            entry = self.create_label_entry(
                label.replace("_", " ").title() + ":", value
            )
            self.entries["constants"][label] = entry

    def setup_component_section(self):
        headers = ["Component", "Z", "Percentage (%)", "Z x comp", "Molar Mass (g/mol)", "Weight (g)"]
        for col, text in enumerate(headers):
            ctk.CTkLabel(self.root, text=text).grid(
                row=self.row, column=self.col + col, padx=10, pady=5
            )
        self.component_table_start_row = self.row + 1  # Save where the table starts
        self.row += 1

    def setup_buttons(self):
        ctk.CTkButton(
            self.root, text="Add Component", command=self.add_new_component
        ).grid(row=self.row - 1, column=self.col + 6, padx=10, pady=10)

        ctk.CTkButton(
            self.root, text="Calculate", command=self.calculate
        ).grid(row=self.row - 1, column=self.col + 7, padx=10, pady=10)

        ctk.CTkButton(
            self.root, text="Save Mixture", command=self.save_mixture
        ).grid(row=self.row - 1, column=self.col + 8, padx=10, pady=10)

        ctk.CTkButton(
            self.root, text="Load Mixture", command=self.load_mixture
        ).grid(row=self.row - 1, column=self.col + 9, padx=10, pady=10)

        self.total_weight_label = ctk.CTkLabel(self.root, text="Total Weight: 0.0000 g")
        self.total_weight_label.grid(row=self.row, column=self.col + 6, padx=10, pady=5)
        self.row += 1

    def create_label_entry(self, label_text, default_value):
        ctk.CTkLabel(self.root, text=label_text).grid(row=self.row, column=self.col, padx=10, pady=5)
        entry = ctk.CTkEntry(self.root)
        entry.insert(0, default_value)
        entry.grid(row=self.row, column=self.col + 1, padx=10, pady=5)
        self.row += 1
        return entry

    def add_initial_components(self):
        # Start adding components at the correct row
        self.next_component_row = self.component_table_start_row
        for component in COMPONENTS:
            self.add_component_widgets(component)

    def add_component_widgets(self, component_name):
        row = self.next_component_row
        self.next_component_row += 1

        component_selector = ctk.CTkComboBox(
            self.root, values=list(COMPONENTS.keys()), width=150
        )
        component_selector.set(component_name)
        component_selector.grid(row=row, column=self.col, padx=10, pady=5)

        z_comp_factor = ctk.CTkLabel(self.root, text="0.0000")
        z_comp_factor.grid(row=row, column=self.col + 1, padx=10, pady=5)

        percentage_entry = ctk.CTkEntry(self.root)
        percentage_entry.insert(0, "0.0")
        percentage_entry.grid(row=row, column=self.col + 2, padx=10, pady=5)

        z_x_comp = ctk.CTkLabel(self.root, text="0.0000")
        z_x_comp.grid(row=row, column=self.col + 3, padx=10, pady=5)

        molar_mass_label = ctk.CTkLabel(self.root, text="0.0000 g/mol")
        molar_mass_label.grid(row=row, column=self.col + 4, padx=10, pady=5)

        weight_label = ctk.CTkLabel(self.root, text="0.0000 g")
        weight_label.grid(row=row, column=self.col + 5, padx=10, pady=5)

        delete_button = ctk.CTkButton(
            self.root, text="Delete", command=lambda: self.delete_component(component_name)
        )
        delete_button.grid(row=row, column=self.col + 7, padx=10, pady=5)

        self.component_widgets[component_name] = {
            "selector": component_selector,
            "z": z_comp_factor,
            "percentage": percentage_entry,
            "z_x_comp": z_x_comp,
            "molar_mass": molar_mass_label,
            "weight": weight_label,
            "delete_button": delete_button,
            "row": row
        }
        self.component_combobox_widgets[component_name] = component_selector

    def delete_component(self, component_name):
        """Delete a component row from the UI only."""
        widgets = self.component_widgets.get(component_name, {})
        for key, widget in widgets.items():
            if key != "row":
                widget.grid_forget()
                widget.destroy()
        # Remove from tracking dicts
        self.component_widgets.pop(component_name, None)
        self.component_combobox_widgets.pop(component_name, None)

    def add_new_component(self):
        def submit_new_component():
            name = new_name_entry.get().strip().upper()
            formula = new_formula_entry.get().strip()
            if not name or not formula:
                CTkMessagebox(title="Input Error",
                              message="Both name and formula are required!",
                              icon="cancel")
                return
            if name in COMPONENTS:
                CTkMessagebox(title="Input Error",
                              message="Component already exists!",
                              icon="cancel")
                return
            COMPONENTS[name] = formula
            save_components_to_file()
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
        component_names = list(COMPONENTS.keys())
        for combobox in self.component_combobox_widgets.values():
            combobox.configure(values=component_names)

    def calculate_mixture_props(self, components, mole_fractions):
        if len(components) != len(mole_fractions):
            raise ValueError("Number of components must match number of mole fractions.")
        if not np.isclose(sum(mole_fractions), 1.0, atol=1e-6):
            raise ValueError("Mole fractions must sum to 1.")

        T_crit_mix = sum(x * Tc(CAS_from_any(c)) for c, x in zip(components, mole_fractions))
        P_crit_mix = 0
        for i, (c1, x_i) in enumerate(zip(components, mole_fractions)):
            for j, (c2, x_j) in enumerate(zip(components, mole_fractions)):
                if i <= j:
                    P_crit_mix += 2 * x_i * x_j * np.sqrt(Pc(CAS_from_any(c1)) * Pc(CAS_from_any(c2)))
        P_crit_mix /= 2
        P_crit_mix /= 100000

        omega_mix = sum(x * omega(CAS_from_any(c)) for c, x in zip(components, mole_fractions))
        return T_crit_mix, P_crit_mix, omega_mix

    def calculate(self):
        components = []
        mole_fractions = []
        for component_name, widget_set in self.component_widgets.items():
            selected_component = widget_set["selector"].get()
            try:
                mole_fraction = float(widget_set["percentage"].get()) / 100
            except ValueError:
                mole_fraction = 0.0
            components.append(COMPONENTS.get(selected_component, selected_component))
            mole_fractions.append(mole_fraction)

        if not np.isclose(sum(mole_fractions), 1.0, atol=1e-6):
            CTkMessagebox(
                title="Input Error",
                message="Mole fractions must sum to 1.",
                icon="cancel"
            )
            return

        R = float(self.entries["constants"]["gas_constant"].get())
        T = float(self.entries["constants"]["temperature"].get())
        P = float(self.entries["constants"]["fill_pressure"].get())
        V = float(self.entries["constants"]["cyl_volume"].get())

        total_moles = (P * V) / (R * T)
        T_crit_mix, P_crit_mix, omega_mix = self.calculate_mixture_props(components, mole_fractions)

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

        total_moles /= Z_mix

        total_weight = 0.0
        for component_name, widget_set in self.component_widgets.items():
            selected_component = widget_set["selector"].get()
            component_formula = COMPONENTS.get(selected_component, selected_component)
            molar_mass = Formula(component_formula).mass
            widget_set["molar_mass"].configure(text=f"{molar_mass:.4f} g/mol")
            moles_component = total_moles * mole_fractions[components.index(component_formula)]
            weight = moles_component * molar_mass
            widget_set["weight"].configure(text=f"{weight:.4f} g")
            total_weight += weight

        self.total_weight_label.configure(text=f"Total Weight: {total_weight:.4f} g")

    def save_mixture(self):
        """Save the current mixture (constants and components) to a JSON file."""
        mixture = {
            "constants": {k: self.entries["constants"][k].get() for k in self.entries["constants"]},
            "components": []
        }
        for component_name, widget_set in self.component_widgets.items():
            mixture["components"].append({
                "name": widget_set["selector"].get(),
                "percentage": widget_set["percentage"].get()
            })
        file_path = fd.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save Gas Mixture"
        )
        if file_path:
            with open(file_path, "w") as f:
                json.dump(mixture, f, indent=4)
            CTkMessagebox(title="Success", message="Mixture saved!", icon="check")

    def load_mixture(self):
        """Load a mixture from a JSON file and update the UI."""
        file_path = fd.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Load Gas Mixture"
        )
        if not file_path:
            return
        with open(file_path, "r") as f:
            mixture = json.load(f)
        # Load constants
        for k, v in mixture.get("constants", {}).items():
            if k in self.entries["constants"]:
                self.entries["constants"][k].delete(0, ctk.END)
                self.entries["constants"][k].insert(0, v)
        # Remove existing component rows
        for comp in list(self.component_widgets.keys()):
            self.delete_component(comp)
        # Add loaded components
        for comp in mixture.get("components", []):
            name = comp["name"]
            if name not in self.component_widgets:
                self.add_component_widgets(name)
            self.component_widgets[name]["selector"].set(name)
            self.component_widgets[name]["percentage"].delete(0, ctk.END)
            self.component_widgets[name]["percentage"].insert(0, comp["percentage"])

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    app = GasCalculatorApp(root)
    root.mainloop()