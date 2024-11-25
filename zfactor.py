# Install the necessary library if not installed already:
# pip install thermo

from thermo import Chemical

def calculate_compressibility_factor(chemical_name, temperature, pressure):
    """
    Calculate the compressibility factor (Z) for a given chemical at a specific temperature and pressure
    using the Peng-Robinson equation of state.
    
    Parameters:
    - chemical_name: Name of the chemical (e.g., 'methane', 'ethanol')
    - temperature: Temperature in Kelvin (K)
    - pressure: Pressure in atmospheres (atm)
    
    Returns:
    - Z: Compressibility factor (dimensionless)
    """
    
    # Create a Chemical object using the given chemical name
    chem = Chemical(chemical_name)
    
    # Using the Peng-Robinson equation of state to calculate the compressibility factor
    Z = chem.Z(T=temperature, P=pressure)
    
    return Z

# Example usage
if __name__ == "__main__":
    # Define the chemical, temperature, and pressure for the calculation
    chemical_name = 'methane'  # You can change this to any supported chemical name
    temperature = 300  # in Kelvin
    pressure = 1  # in atm
    
    # Call the function to calculate compressibility factor
    Z = calculate_compressibility_factor(chemical_name, temperature, pressure)
    
    # Output the result
    print(f"Compressibility factor (Z) for {chemical_name} at {temperature} K and {pressure} atm: {Z}")
