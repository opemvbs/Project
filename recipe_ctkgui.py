import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from molmass import Formula
# from chemicals import Z

# Default constants
DEFAULT_CONSTANTS = {
    "cyl_volume": 40,  # L
    "fill_pressure": 150,  # bar
    "gas_constant": 0.08314,  # L.Bar/mol.g.K
    "temperature": 293,  # K
    "z_mix": 1,
}

# Available components
# COMPONENTS = {'acetaldehyde': '75-07-0', 'acetone': '67-64-1', 'acetylene': '74-86-2', 'ethyl-acetylene': '107-00-6', 'allyl alcohol': '107-18-6', 'ammonia': '7664-41-7', 'argon': '7440-37-1', 'benzene': '71-43-2', 'ethyl-benzene': '100-41-4', 'propyl-benzene': '103-65-1', '1,3-butadiene': '106-99-0', '1,2-butadiene': '590-19-2', 'n-butane': '106-97-8', 'iso-butane': '75-28-5', 'iso-butylene': '7756-94-7', '1-butanol': '71-36-3', '2-butanol': '78-92-2', '1-butene': '106-98-9', '1-butanethiol': '109-79-5', '2-butanethiol': '513-53-1', 'isobutyl mercaptan': '513-44-0', 'tert-butyl mercaptan': '75-66-1', 'cis-2-butene': '590-18-1', 'trans-2-butene': '624-64-6', 'isobutyraldehyde': '78-84-2', 'butyraldehyde': '123-72-8', 'carbon dioxide': '124-38-9', 'carbon disulphide': '75-15-0', 'carbon monoxide': '630-08-0', 'carbonyl sulphide': '463-58-1', 'cumene': '98-82-8', 'chloroethane': '75-00-3', 'chloroform': '67-66-3', '2-chloropropene': '557-98-2', '1-decanethiol': '143-10-2', 'decane': '124-18-5', '1,1-dichloroethane': '75-34-3', '1,2-dichloroethane': '107-06-2', 'diethylamine': '109-89-7', '1,4-diethylbenzene': '105-05-5', 'diethyl sulphide': '352-93-2', 'dimethyl sulphide': '75-18-3', 'dimethyl disulphide': '624-92-0', 'dimethyl ether': '115-10-6', 'diethyl ether': '60-29-7', 'diisobutylene': '107-39-1', 'cis-1,2-dichloroethylene': '156-59-2', 'trans-1,2-dichloroethylene': '156-60-5', '1,4-dioxane': '123-91-1', '2,2-dimethylbutane': '75-83-2', '2,3-dimethylbutane': '79-29-8', 'dodecane': '112-40-3', 'ethane': '74-84-0', 'ethanol': '64-17-5', 'ethanethiol': '75-08-1', 'ethylcyclohexane': '1678-91-7', 'ethylcyclopentane': '1640-89-7', 'ethylene': '74-85-1', 'ethyl formate': '109-94-4', 'methyl ethyl ketone': '78-93-3', 'helium': '7440-59-7', 'heptane': '142-82-5', 'hexane': '110-54-3', 'iso-hexane': '107-83-5', 'cyclo-hexane': '110-82-7', '1-hexanethiol': '111-31-9', '1-hexene': '592-41-6', '2-hexene': '4050-45-7', 'trans-2-hexene': '592-43-8', '1-heptanethiol': '1639-09-4', 'hydrogen': '1333-74-0', 'hydrogen sulphide': '7783-06-4', 'isoprene': '78-79-5', 'methane': '74-82-8', 'methanethiol': '74-93-1', 'methanol': '67-56-1', 'methyl acetate': '79-20-9', '2-methyl-1-butene': '563-46-2', '2-methyl-2-butene': '513-35-9', '3-methyl-1-butene': '563-45-1', 'methyl-cyclo-hexane': '108-87-2', 'methyl chloride': '74-87-3', 'methyl formate': '107-31-3', '2-methylhexane': '591-76-4', '3-methylpentane': '96-14-0', 'nitric oxide': '10102-43-9', 'nitrogen': '7727-37-9', 'nitrogen dioxide': '10102-44-0', 'nitrous oxide': '10024-97-2', 'nonane': '111-84-2', '1-nonanethiol': '1455-21-6', 'octane': '111-65-9', '1-octanethiol': '111-88-6', 'oxygen': '7782-44-7', 'n-pentane': '109-66-0', 'iso-pentane': '78-78-4', 'neo-pentane': '463-82-1', 'cyclo-pentane': '287-92-3', 'methyl-cyclo-pentane': '96-37-7', '2 -propanol': '67-63-0', '1 -propanol': '71-23-8', '1,4-pentadiene': '591-93-5', '1-pentene': '109-67-1', '1-propanethiol': '107-03-9', '2-propanethiol': '75-33-2', 'cis-2-pentene': '627-20-3', 'trans-2-pentene': '646-04-8', '1-pentanethiol': '110-66-7', '2-methyl-1-propanethiol': '513-44-0', '2-methyl-2-propanethiol': '75-66-1', 'propane': '74-98-6', 'cyclo-propane': '75-19-4', 'propylene': '115-07-1', 'propadiene': '463-49-0', 'propyne': '74-99-7', 'propyl ether': '111-43-3', 'diisopropyl ether': '108-20-3', 'propionaldehyde': '123-38-6', 'sulphur dioxide': '7446-09-5', 'sulphur hexafluoride': '2551-62-4', 'sulfolane': '126-33-0', 'styrene': '100-42-5', 'ethyl methyl sulphide': '624-89-5', 'tetradecane': '629-59-4', 'toluene': '108-88-3', 'tridecane': '629-50-5', 'trichloroethylene': '79-01-6', '1,2,4-trichlorobenzene': '120-82-1', '1,2,4-trimethylbenzene': '95-63-6', '2,2,4-trimethylpentane': '540-84-1', '2,4,4-trimethyl-1-pentene': '107-39-1', 'undecane': '1120-21-4', 'valeraldehyde': '110-62-3', 'isovaleraldehyde': '590-86-3', 'vinyl chloride': '75-01-4', 'vinyl acetylene': '689-97-4', 'water': '7732-18-5', 'ortho-xylene': '95-47-6', 'meta-xylene': '108-38-3', 'para-xylene': '106-42-3', 'tert-butyl methyl ether': '1634-04-4', 'tert-butyl ethyl ether': '637-92-3', 'sec-butyl methyl ether': '6795-87-5', 'sec-butyl sulfide': '626-26-6', 'tert-butyl alcohol': '75-65-0', 'isobutanol': '78-83-1', 'tert-amyl methyl ether': '994-05-8', 'thiophene': '110-02-1', 'tetrahydrothiophene': '110-01-0', '2-Ethylthiophene': '872-55-9', '2-Methylthiophene': '554-14-3', '3-Methylthiophene': '616-44-4', '2,5-Dimethylthiophene': '638-02-8', 'difluoromethane': '75-10-5', 'pentafluoroethane': '354-33-6', '1,1,1,2-tetrafluoroethane': '811-97-2'
#               }

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
        headers = ["Component", "Z" , "Percentage (%)", "Z x comp", "Molar Mass (g/mol)", "Weight (g)"]
        for col, text in enumerate(headers):
            ctk.CTkLabel(self.root, text=text).grid(
                row=self.row, column=self.col + col, padx=10, pady=5
            )
        # self.row += 1  # Move to the next row after headers

    def setup_buttons(self):
        """Add buttons for various actions."""
        ctk.CTkButton(
            self.root, text="Add Component", command=self.add_new_component
        ).grid(row=self.row - 1, column=self.col + 6, padx=10, pady=10)

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
                    constants["fill_pressure"] * constants["cyl_volume"] * percentage * molar_mass / (constants["z_mix"] * constants["gas_constant"] * constants["temperature"] * 100)
                )

                

                mole = weight / molar_mass
                density = mole * molar_mass / constants["cyl_volume"] # g/L
                if percentage == 0:
                    return
                molar_volume = (1e3 * molar_mass) / density
                print(f"{component_name} {mole}")
                print(f"{component_name} {density}")
                print(f"{component_name} {molar_volume}")

                
                
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
                          message=str(e),
                          icon="cancel")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    app = GasCalculatorApp(root)
    root.mainloop()
