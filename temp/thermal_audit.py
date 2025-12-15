"""
Thermal Physics Audit Script
Verifies the bifacial panel thermal equilibrium calculations
"""

import math

# ==========================================
# CONSTANTS
# ==========================================

SIGMA = 5.67e-8  # Stefan-Boltzmann constant (W/m²/K⁴)
EARTH_RADIUS_KM = 6371.0

# Space environment
SOLAR_IRRADIANCE = 1361  # W/m² (AM0)
EARTH_IR_FLUX = 237  # W/m² (global average)
EARTH_ALBEDO = 0.30  # Average reflectivity
T_SPACE = 3  # K (deep space sink temperature)

# Default state
solarAbsorptivity = 0.92  # α_pv
emissivityPV = 0.85  # ε_pv (glass)
emissivityRad = 0.90  # ε_rad (white paint/OSR)
pvEfficiency = 0.22  # 22% efficient cells
betaAngle = 90  # Terminator orbit
orbitalAltitudeKm = 550


def earth_angular_radius(altitude_km):
    """Calculate Earth's angular radius as seen from orbit"""
    r_orbit = EARTH_RADIUS_KM + altitude_km
    theta = math.asin(EARTH_RADIUS_KM / r_orbit)
    return theta  # radians


def nadir_view_factor(altitude_km):
    """Maximum view factor (nadir-pointing plate)"""
    theta = earth_angular_radius(altitude_km)
    return math.sin(theta) ** 2


def tilted_plate_vf(altitude_km, tilt_rad):
    """View factor for plate tilted from nadir"""
    theta = earth_angular_radius(altitude_km)
    vf_nadir = math.sin(theta) ** 2
    
    cos_tilt = math.cos(tilt_rad)
    
    if cos_tilt <= 0:
        # Edge-on or facing away
        return vf_nadir * 0.05  # 5% floor
    
    return vf_nadir * cos_tilt


def tilted_plate_vf_from_cos(altitude_km, cos_tilt):
    """
    Numerically-stable VF calculation when cos(tilt) is already known.
    Mirrors `tiltedPlateViewFactorFromCos` in `static/js/math.js`.
    """
    theta = earth_angular_radius(altitude_km)
    vf_nadir = math.sin(theta) ** 2
    if cos_tilt <= 0:
        return vf_nadir * 0.05
    return vf_nadir * cos_tilt


def sun_tracking_panel_vfs(altitude_km, beta_deg):
    """Calculate orbit-averaged view factors for sun-tracking bifacial panel"""
    beta_rad = beta_deg * math.pi / 180
    n_points = 72  # Integration points
    
    vf_a_sum = 0.0
    vf_b_sum = 0.0
    
    for i in range(n_points):
        nu = 2 * math.pi * i / n_points  # True anomaly
        
        # Angle between panel normal (sun direction) and nadir
        cos_gamma = math.cos(beta_rad) * math.cos(nu)
        
        # Mirrors JS implementation: avoid acos→cos (numerical issues near β=90°)
        vf_a = tilted_plate_vf_from_cos(altitude_km, cos_gamma)
        vf_b = tilted_plate_vf_from_cos(altitude_km, -cos_gamma)
        
        vf_a_sum += vf_a
        vf_b_sum += vf_b
    
    return {
        'vf_side_a': vf_a_sum / n_points,
        'vf_side_b': vf_b_sum / n_points,
        'vf_total': (vf_a_sum + vf_b_sum) / n_points
    }


def audit_thermal():
    """Audit thermal equilibrium calculations"""
    print("="*60)
    print("THERMAL PHYSICS AUDIT")
    print("="*60)
    
    # Use a sample area (10 km²)
    area_m2 = 10e6  # 10 km²
    
    print(f"\nParameters:")
    print(f"  Area: {area_m2/1e6:.0f} km²")
    print(f"  Orbital Altitude: {orbitalAltitudeKm} km")
    print(f"  Beta Angle: {betaAngle}°")
    print(f"  Solar Absorptivity: {solarAbsorptivity}")
    print(f"  PV Emissivity: {emissivityPV}")
    print(f"  Radiator Emissivity: {emissivityRad}")
    print(f"  PV Efficiency: {pvEfficiency*100}%")
    
    # --- VIEW FACTORS ---
    print("\n--- VIEW FACTOR CALCULATIONS ---")
    
    earth_angle_deg = earth_angular_radius(orbitalAltitudeKm) * 180 / math.pi
    vf_nadir = nadir_view_factor(orbitalAltitudeKm)
    
    print(f"Earth angular radius: {earth_angle_deg:.1f}°")
    print(f"Max view factor (nadir): {vf_nadir:.3f}")
    
    vfs = sun_tracking_panel_vfs(orbitalAltitudeKm, betaAngle)
    print(f"\nOrbit-averaged VFs for sun-tracking panel at β={betaAngle}°:")
    print(f"  Side A (sun-facing): {vfs['vf_side_a']:.4f}")
    print(f"  Side B (anti-sun): {vfs['vf_side_b']:.4f}")
    print(f"  Total: {vfs['vf_total']:.4f}")
    
    # --- HEAT LOADS ---
    print("\n--- HEAT LOADS (INPUTS) ---")
    
    # 1. Solar absorbed
    power_generated = SOLAR_IRRADIANCE * pvEfficiency * area_m2
    q_absorbed_total = SOLAR_IRRADIANCE * solarAbsorptivity * area_m2
    q_solar_waste = q_absorbed_total - power_generated
    
    print(f"\n1. Solar:")
    print(f"   Incident: {SOLAR_IRRADIANCE * area_m2 / 1e9:.2f} GW")
    print(f"   Absorbed (α={solarAbsorptivity}): {q_absorbed_total / 1e9:.2f} GW")
    print(f"   Converted to electricity ({pvEfficiency*100}%): {power_generated / 1e9:.2f} GW")
    print(f"   Immediate thermal waste: {q_solar_waste / 1e9:.2f} GW")
    
    # 2. Earth IR
    vf_a = vfs['vf_side_a']
    vf_b = vfs['vf_side_b']
    q_earth_ir_a = EARTH_IR_FLUX * vf_a * emissivityPV * area_m2
    q_earth_ir_b = EARTH_IR_FLUX * vf_b * emissivityRad * area_m2
    q_earth_ir = q_earth_ir_a + q_earth_ir_b
    
    print(f"\n2. Earth IR:")
    print(f"   Side A (VF={vf_a:.4f}, ε={emissivityPV}): {q_earth_ir_a / 1e9:.3f} GW")
    print(f"   Side B (VF={vf_b:.4f}, ε={emissivityRad}): {q_earth_ir_b / 1e9:.3f} GW")
    print(f"   Total Earth IR: {q_earth_ir / 1e9:.3f} GW")
    
    # 3. Albedo
    albedo_scaling = math.cos(betaAngle * math.pi / 180)
    q_albedo = SOLAR_IRRADIANCE * EARTH_ALBEDO * vf_a * albedo_scaling * solarAbsorptivity * area_m2
    
    print(f"\n3. Albedo:")
    print(f"   Albedo scaling at β={betaAngle}°: {albedo_scaling:.3f}")
    print(f"   Albedo load: {q_albedo / 1e9:.3f} GW")
    
    # 4. Heat loop return (compute waste)
    q_heat_loop = power_generated
    print(f"\n4. Heat loop return: {q_heat_loop / 1e9:.2f} GW")
    
    # Total heat in
    total_heat_in = q_solar_waste + q_earth_ir + q_albedo + q_heat_loop
    print(f"\nTOTAL HEAT IN: {total_heat_in / 1e9:.2f} GW")
    
    # --- VERIFY HEAT BALANCE ---
    print("\n--- HEAT BALANCE CHECK ---")
    print(f"Solar waste + Earth IR + Albedo + Loop return:")
    print(f"  {q_solar_waste/1e9:.3f} + {q_earth_ir/1e9:.3f} + {q_albedo/1e9:.3f} + {q_heat_loop/1e9:.3f}")
    print(f"  = {total_heat_in/1e9:.3f} GW")
    
    # Alternative calculation: absorbed solar + Earth IR + Albedo
    alt_total = q_absorbed_total + q_earth_ir + q_albedo
    print(f"\nAlternative: q_absorbed + Earth IR + Albedo:")
    print(f"  {q_absorbed_total/1e9:.3f} + {q_earth_ir/1e9:.3f} + {q_albedo/1e9:.3f}")
    print(f"  = {alt_total/1e9:.3f} GW")
    print(f"Match: {abs(total_heat_in - alt_total) < 1}")  # Within 1W
    
    # --- EQUILIBRIUM TEMPERATURE ---
    print("\n--- EQUILIBRIUM TEMPERATURE ---")
    
    total_emissivity = emissivityPV + emissivityRad
    print(f"Total emissivity (both sides): {total_emissivity:.2f}")
    
    # T = (Q_in / (σ × A × ε_total) + T_space⁴)^0.25
    eq_temp_k = (total_heat_in / (SIGMA * area_m2 * total_emissivity) + T_SPACE**4) ** 0.25
    eq_temp_c = eq_temp_k - 273.15
    
    print(f"Equilibrium Temperature: {eq_temp_k:.1f} K ({eq_temp_c:.1f} °C)")
    
    # Radiative capacity at equilibrium
    delta_t4 = eq_temp_k**4 - T_SPACE**4
    q_rad_a = SIGMA * area_m2 * emissivityPV * delta_t4
    q_rad_b = SIGMA * area_m2 * emissivityRad * delta_t4
    radiative_capacity = q_rad_a + q_rad_b
    
    print(f"\nRadiative capacity at equilibrium:")
    print(f"  Side A: {q_rad_a/1e9:.2f} GW")
    print(f"  Side B: {q_rad_b/1e9:.2f} GW")
    print(f"  Total: {radiative_capacity/1e9:.2f} GW")
    print(f"Heat in: {total_heat_in/1e9:.2f} GW")
    print(f"Balance: {abs(radiative_capacity - total_heat_in)/1e9:.4f} GW difference")
    
    # --- GPU THERMAL MARGIN ---
    print("\n--- GPU THERMAL MARGIN ---")
    max_die_temp_c = 85
    temp_drop_c = 10
    radiator_target_c = max_die_temp_c - temp_drop_c
    
    print(f"Max GPU die temp: {max_die_temp_c}°C")
    print(f"Die-to-radiator drop: {temp_drop_c}°C")
    print(f"Required radiator temp: ≤{radiator_target_c}°C")
    print(f"Actual equilibrium temp: {eq_temp_c:.1f}°C")
    print(f"Margin: {radiator_target_c - eq_temp_c:.1f}°C")
    print(f"Thermal OK: {eq_temp_c <= radiator_target_c}")
    
    # --- ENERGY PARTITION CHECK ---
    print("\n--- ENERGY PARTITION SANITY CHECK ---")
    print(f"Incident solar: 100%")
    absorbed_pct = (solarAbsorptivity) * 100
    electrical_pct = (pvEfficiency / solarAbsorptivity) * absorbed_pct
    thermal_pct = absorbed_pct - electrical_pct
    reflected_pct = 100 - absorbed_pct
    
    print(f"  Reflected (1-α): {reflected_pct:.1f}%")
    print(f"  Absorbed (α): {absorbed_pct:.1f}%")
    print(f"    -> Electrical ({pvEfficiency*100}% eff): {pvEfficiency*100:.1f}%")
    print(f"    -> Immediate thermal: {absorbed_pct - pvEfficiency*100:.1f}%")
    print(f"  Total accounted: {reflected_pct + pvEfficiency*100 + (absorbed_pct - pvEfficiency*100):.1f}%")
    
    return eq_temp_c


def audit_beta_angle_sensitivity():
    """Check how beta angle affects thermal equilibrium"""
    print("\n" + "="*60)
    print("BETA ANGLE SENSITIVITY")
    print("="*60)
    
    area_m2 = 10e6
    
    print(f"\nBeta Angle | VF_A   | VF_B   | Earth IR | Albedo | Eq Temp")
    print("-" * 65)
    
    for beta in [90, 75, 60, 45, 30, 0]:
        vfs = sun_tracking_panel_vfs(orbitalAltitudeKm, beta)
        vf_a = vfs['vf_side_a']
        vf_b = vfs['vf_side_b']
        
        # Recalculate heat loads
        power_generated = SOLAR_IRRADIANCE * pvEfficiency * area_m2
        q_absorbed_total = SOLAR_IRRADIANCE * solarAbsorptivity * area_m2
        q_solar_waste = q_absorbed_total - power_generated
        
        q_earth_ir_a = EARTH_IR_FLUX * vf_a * emissivityPV * area_m2
        q_earth_ir_b = EARTH_IR_FLUX * vf_b * emissivityRad * area_m2
        q_earth_ir = q_earth_ir_a + q_earth_ir_b
        
        albedo_scaling = math.cos(beta * math.pi / 180)
        q_albedo = SOLAR_IRRADIANCE * EARTH_ALBEDO * vf_a * albedo_scaling * solarAbsorptivity * area_m2
        
        q_heat_loop = power_generated
        total_heat_in = q_solar_waste + q_earth_ir + q_albedo + q_heat_loop
        
        total_emissivity = emissivityPV + emissivityRad
        eq_temp_k = (total_heat_in / (SIGMA * area_m2 * total_emissivity) + T_SPACE**4) ** 0.25
        eq_temp_c = eq_temp_k - 273.15
        
        print(f"  {beta:3d}°     | {vf_a:.4f} | {vf_b:.4f} | {q_earth_ir/1e9:.3f} GW | {q_albedo/1e9:.3f} GW | {eq_temp_c:.1f}°C")


if __name__ == "__main__":
    eq_temp = audit_thermal()
    audit_beta_angle_sensitivity()
    
    print("\n" + "="*60)
    print("THERMAL AUDIT COMPLETE")
    print("="*60)

