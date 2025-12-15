#!/usr/bin/env python3
"""
Verify the corrected view factor implementation.
"""
import math

# Constants
EARTH_RADIUS_KM = 6371.0
EARTH_IR = 237  # W/m²
ALBEDO = 0.30
SOLAR = 1361  # W/m²
EPSILON_PV = 0.85
EPSILON_RAD = 0.90
ALPHA_PV = 0.92
PV_EFF = 0.22
T_SPACE = 3  # K
SIGMA = 5.67e-8  # W/m²/K⁴

def earth_angular_radius(altitude_km):
    r_orbit = EARTH_RADIUS_KM + altitude_km
    return math.asin(EARTH_RADIUS_KM / r_orbit)

def nadir_view_factor(altitude_km):
    theta = earth_angular_radius(altitude_km)
    return math.sin(theta) ** 2

def tilted_plate_view_factor(altitude_km, tilt_rad):
    vf_nadir = nadir_view_factor(altitude_km)
    cos_tilt = math.cos(tilt_rad)
    if cos_tilt <= 0:
        return vf_nadir * 0.05
    return vf_nadir * cos_tilt

def sun_tracking_view_factors(altitude_km, beta_deg):
    beta_rad = math.radians(beta_deg)
    n_points = 72
    
    vf_a_sum = 0.0
    vf_b_sum = 0.0
    
    for i in range(n_points):
        nu = 2 * math.pi * i / n_points
        cos_gamma = math.cos(beta_rad) * math.cos(nu)
        
        gamma_a = math.acos(max(-1, min(1, cos_gamma)))
        vf_a = tilted_plate_view_factor(altitude_km, gamma_a)
        
        gamma_b = math.pi - gamma_a
        vf_b = tilted_plate_view_factor(altitude_km, gamma_b)
        
        vf_a_sum += vf_a
        vf_b_sum += vf_b
    
    return {
        'vf_side_a': vf_a_sum / n_points,
        'vf_side_b': vf_b_sum / n_points,
        'vf_total': (vf_a_sum + vf_b_sum) / n_points
    }

def calculate_thermal_corrected(altitude_km, beta_deg, area_m2):
    """Corrected thermal calculation matching fixed math.js"""
    vf = sun_tracking_view_factors(altitude_km, beta_deg)
    vf_a = vf['vf_side_a']
    vf_b = vf['vf_side_b']
    
    # Direct solar
    q_absorbed = SOLAR * ALPHA_PV * area_m2
    power_gen = SOLAR * PV_EFF * area_m2
    q_solar_waste = q_absorbed - power_gen
    
    # Earth IR - CORRECT: separate per side
    q_earth_ir_a = EARTH_IR * vf_a * EPSILON_PV * area_m2
    q_earth_ir_b = EARTH_IR * vf_b * EPSILON_RAD * area_m2
    q_earth_ir = q_earth_ir_a + q_earth_ir_b
    
    # Albedo - CORRECT: only PV side
    albedo_scale = math.cos(math.radians(beta_deg))
    q_albedo = SOLAR * ALBEDO * vf_a * albedo_scale * ALPHA_PV * area_m2
    
    # Heat loop return
    q_heat_loop = power_gen
    
    # Total heat
    total_heat = q_solar_waste + q_earth_ir + q_albedo + q_heat_loop
    
    # Equilibrium temperature
    eps_total = EPSILON_PV + EPSILON_RAD
    t_eq_k = ((total_heat / (SIGMA * area_m2 * eps_total)) + T_SPACE**4) ** 0.25
    t_eq_c = t_eq_k - 273.15
    
    return {
        'vf_a': vf_a,
        'vf_b': vf_b,
        'q_solar_waste': q_solar_waste,
        'q_earth_ir': q_earth_ir,
        'q_albedo': q_albedo,
        'q_heat_loop': q_heat_loop,
        'total_heat': total_heat,
        't_eq_c': t_eq_c
    }

print("=" * 70)
print("CORRECTED THERMAL MODEL VERIFICATION")
print("=" * 70)

altitude = 550  # km
area = 1e6  # 1 km²

print(f"\nParameters: altitude={altitude} km, area=1 km²")
print(f"α_PV={ALPHA_PV}, ε_PV={EPSILON_PV}, ε_rad={EPSILON_RAD}, η={PV_EFF}")

print("\n" + "-" * 70)
print(f"{'Beta':>6} | {'VF_A':>7} | {'VF_B':>7} | {'Q_sol':>8} | {'Q_IR':>7} | {'Q_alb':>7} | {'Q_loop':>8} | {'Total':>8} | {'T_eq':>7}")
print("-" * 70)

for beta in [90, 85, 80, 75, 70, 65, 60]:
    result = calculate_thermal_corrected(altitude, beta, area)
    print(f"{beta:>6}° | {result['vf_a']:>7.4f} | {result['vf_b']:>7.4f} | "
          f"{result['q_solar_waste']/1e6:>7.0f}M | {result['q_earth_ir']/1e6:>6.1f}M | "
          f"{result['q_albedo']/1e6:>6.1f}M | {result['q_heat_loop']/1e6:>7.0f}M | "
          f"{result['total_heat']/1e6:>7.0f}M | {result['t_eq_c']:>6.1f}°C")

print("\n" + "=" * 70)
print("SANITY CHECKS")
print("=" * 70)

# Check at beta=90 (terminator)
r90 = calculate_thermal_corrected(altitude, 90, area)
print(f"\nAt β=90° (terminator orbit):")
print(f"  Solar waste: {r90['q_solar_waste']/1e6:.0f} MW (absorbed - electrical)")
print(f"  Earth IR: {r90['q_earth_ir']/1e6:.1f} MW (small due to edge-on)")
print(f"  Albedo: {r90['q_albedo']/1e6:.1f} MW (zero - cos(90°)=0)")
print(f"  Heat loop: {r90['q_heat_loop']/1e6:.0f} MW (electrical→heat)")
print(f"  T_eq = {r90['t_eq_c']:.1f}°C")

# Verify solar heat = absorbed
absorbed = SOLAR * ALPHA_PV * area
print(f"\n  Solar absorbed = {absorbed/1e6:.0f} MW")
print(f"  Solar waste + heat loop = {(r90['q_solar_waste'] + r90['q_heat_loop'])/1e6:.0f} MW")
print(f"  Match: {'✓' if abs(absorbed - (r90['q_solar_waste'] + r90['q_heat_loop'])) < 1000 else '✗'}")

# Check at beta=60 (hot case)
r60 = calculate_thermal_corrected(altitude, 60, area)
print(f"\nAt β=60° (seasonal hot case):")
print(f"  Solar waste: {r60['q_solar_waste']/1e6:.0f} MW")
print(f"  Earth IR: {r60['q_earth_ir']/1e6:.1f} MW")
print(f"  Albedo: {r60['q_albedo']/1e6:.1f} MW")
print(f"  Heat loop: {r60['q_heat_loop']/1e6:.0f} MW")
print(f"  T_eq = {r60['t_eq_c']:.1f}°C")
print(f"  ΔT from terminator: +{r60['t_eq_c'] - r90['t_eq_c']:.1f}°C")

# Earth loads as percentage of total
pct_earth = (r60['q_earth_ir'] + r60['q_albedo']) / r60['total_heat'] * 100
print(f"\n  Earth loads at β=60°: {pct_earth:.1f}% of total heat")
