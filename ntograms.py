# Given values
P = 150  # bar
V = 40   # L
Z = 0.9093
R = 0.08314  # L·bar/mol·K
T = 300  # K
M_Ar = 39.948  # g/mol (molar mass of Argon)

# Calculate the number of moles of argon (n)
n = (P * V) / (Z * R * T)

# Convert moles to grams
mass_grams = n * M_Ar

# Print the result
print(f"Mass of argon: {mass_grams:.2f} grams")
