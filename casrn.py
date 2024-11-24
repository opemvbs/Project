import pandas as pd
from chemicals.identifiers import CAS_from_any

def get_CAS(chemical_name):
    """
    Retrieve CAS RN for a given chemical name using the chemicals library.
    """
    try:
        cas_rn = CAS_from_any(chemical_name)
        if cas_rn:
            return cas_rn
        return "CAS RN not found"
    except Exception as e:
        return f"Error: {e}"

# Load the CSV file
input_file = "material.csv"  # Replace with your file name
output_file = "material_with_cas.csv"  # Output file name
df = pd.read_csv(input_file)

# Ensure the input file has the correct column
if "component_name" not in df.columns:
    raise ValueError("The input CSV must have a column named 'component_name'.")

# Process each component and fetch CAS RN
df["CAS RN"] = df["component_name"].apply(get_CAS)

# Save the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False)

print(f"Processed data saved to {output_file}")
print(df.head())  # Display the first few rows of the updated DataFrame
