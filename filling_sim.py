import numpy as np

def simulate_filling_with_heat_loss():
    """
    Simulates the gas cylinder filling process over time, including heat
    transfer from the gas to the cylinder wall.

    Assumptions:
    1. Nitrogen behaves as an ideal gas.
    2. Gas is added at a constant molar flow rate.
    3. The cylinder wall temperature is uniform (lumped-capacitance model).
    4. Heat loss from the cylinder to the outside air is neglected for simplicity,
       as the primary heat transfer in the short filling time is from gas to cylinder.
    """

    # --- Input Parameters ---
    V = 10.0  # Volume of the cylinder in Liters
    P_i = 1.0  # Initial pressure in bar
    P_f = 150.0 # Target final pressure in bar
    T_initial_celsius = 25.0  # Initial temperature of gas and cylinder in Celsius

    # --- Filling Process Parameters ---
    filling_time_seconds = 5 * 60  # 10 minutes
    time_step_seconds = 1.0         # Simulation time step in seconds

    # --- Cylinder Physical Properties (Estimated for a 10L steel cylinder) ---
    cylinder_mass_kg = 14.0 # Estimated mass of the steel cylinder
    specific_heat_steel_J_kgK = 450.0 # Specific heat capacity of steel
    # Estimated surface area of the inside of the cylinder
    surface_area_m2 = 0.4
    # Overall heat transfer coefficient (gas to cylinder wall).
    # This is a critical assumption. Higher values mean faster cooling.
    U_heat_transfer_coeff_W_m2K = 150.0

    # --- Constants for Nitrogen (as an ideal diatomic gas) ---
    R = 8.314  # Ideal gas constant in J/(mol*K)
    Cv_molar = 5/2 * R  # Molar specific heat at constant volume
    Cp_molar = 7/2 * R  # Molar specific heat at constant pressure

    # --- Initialization ---
    # Convert units
    V_m3 = V / 1000
    P_i_pa = P_i * 1e5
    P_f_pa = P_f * 1e5
    T_gas_K = T_initial_celsius + 273.15
    T_cylinder_K = T_initial_celsius + 273.15
    T_inlet_gas_K = T_initial_celsius + 273.15 # Assume inlet gas is at ambient temp

    # Calculate initial moles and target final moles (for flow rate)
    n_initial = (P_i_pa * V_m3) / (R * T_gas_K)
    # Estimate target moles assuming final temp is close to initial temp
    n_target_final = (P_f_pa * V_m3) / (R * T_gas_K)
    
    # Calculate required constant molar flow rate
    molar_flow_rate = (n_target_final - n_initial) / filling_time_seconds
    
    n_current = n_initial
    
    num_steps = int(filling_time_seconds / time_step_seconds)
    
    print("--- Simulation Started ---")
    print(f"Cylinder Mass: {cylinder_mass_kg} kg, Surface Area: {surface_area_m2} m^2")
    print(f"Heat Transfer Coefficient (U): {U_heat_transfer_coeff_W_m2K} W/m^2K")
    print("-" * 30)

    # --- Simulation Loop ---
    for i in range(num_steps):
        # Moles added in this time step
        moles_added = molar_flow_rate * time_step_seconds
        n_previous = n_current
        n_current = n_previous + moles_added

        # 1. Calculate temperature rise from adding new gas (adiabatic compression)
        # Energy balance: n_new * Cv * T_intermediate = n_old * Cv * T_old + dn * Cp * T_inlet
        T_intermediate_gas_K = (n_previous * Cv_molar * T_gas_K + moles_added * Cp_molar * T_inlet_gas_K) / (n_current * Cv_molar)

        # 2. Calculate heat loss from gas to cylinder wall in this time step
        # Q = U * A * (T_gas - T_cylinder) * dt
        heat_lost_from_gas_J = U_heat_transfer_coeff_W_m2K * surface_area_m2 * (T_intermediate_gas_K - T_cylinder_K) * time_step_seconds
        
        # 3. Update temperatures based on heat transfer
        # Temperature drop in gas due to heat loss
        delta_T_gas_cooling = heat_lost_from_gas_J / (n_current * Cv_molar)
        T_gas_K = T_intermediate_gas_K - delta_T_gas_cooling
        
        # Temperature rise in cylinder due to heat gain
        delta_T_cylinder_heating = heat_lost_from_gas_J / (cylinder_mass_kg * specific_heat_steel_J_kgK)
        T_cylinder_K = T_cylinder_K + delta_T_cylinder_heating

    # --- Final Results ---
    final_pressure_pa = (n_current * R * T_gas_K) / V_m3
    final_pressure_bar = final_pressure_pa / 1e5
    
    T_gas_celsius = T_gas_K - 273.15
    T_cylinder_celsius = T_cylinder_K - 273.15
    
    print("--- Simulation Finished ---")
    print(f"Filling Time: {filling_time_seconds / 60:.0f} minutes")
    print("-" * 30)
    print(f"Final Calculated Pressure: {final_pressure_bar:.2f} bar")
    print(f"Final Gas Temperature: {T_gas_celsius:.2f} °C")
    print(f"Final Cylinder Wall Temperature: {T_cylinder_celsius:.2f} °C")
    print("-" * 30)

simulate_filling_with_heat_loss()