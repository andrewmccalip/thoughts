#!/usr/bin/env python3
"""
Triple-check the view factor implementation for Earth IR and Albedo.
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

def earth_angular_radius(altitude_km):
    """θ = arcsin(Re / (Re + h))"""
    r_orbit = EARTH_RADIUS_KM + altitude_km
    return math.asin(EARTH_RADIUS_KM / r_orbit)

def nadir_view_factor(altitude_km):
    """VF_nadir = sin²(θ)"""
    theta = earth_angular_radius(altitude_km)
    return math.sin(theta) ** 2

def tilted_plate_view_factor(altitude_km, tilt_rad):
    """VF for tilted plate, with minimum floor for edge-on."""
    vf_nadir = nadir_view_factor(altitude_km)
    cos_tilt = math.cos(tilt_rad)
    if cos_tilt <= 0:
        return vf_nadir * 0.05  # 5% floor
    return vf_nadir * cos_tilt

def sun_tracking_view_factors(altitude_km, beta_deg):
    """Orbit-averaged VF for sun-tracking bifacial panel."""
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

print("=" * 70)
print("VIEW FACTOR BUG CHECK")
print("=" * 70)

altitude = 550  # km
beta = 75  # degrees - use intermediate value

vf = sun_tracking_view_factors(altitude, beta)
print(f"\nAt altitude={altitude} km, beta={beta}°:")
print(f"  VF Side A (PV/sun-facing):   {vf['vf_side_a']:.4f}")
print(f"  VF Side B (radiator/anti-sun): {vf['vf_side_b']:.4f}")
print(f"  VF Total:                     {vf['vf_total']:.4f}")

print("\n" + "=" * 70)
print("EARTH IR LOAD CALCULATION")
print("=" * 70)

area = 1e6  # 1 km² = 1e6 m²

# WRONG formula (current implementation)
q_ir_wrong = EARTH_IR * vf['vf_total'] * (EPSILON_PV + EPSILON_RAD) * area
print(f"\nWRONG (current code):")
print(f"  qEarthIR = EARTH_IR × vfTotal × (εPV + εRad) × area")
print(f"  qEarthIR = {EARTH_IR} × {vf['vf_total']:.4f} × ({EPSILON_PV} + {EPSILON_RAD}) × {area:.0e}")
print(f"  qEarthIR = {q_ir_wrong/1e6:.2f} MW")

# CORRECT formula
q_ir_a = EARTH_IR * vf['vf_side_a'] * EPSILON_PV * area
q_ir_b = EARTH_IR * vf['vf_side_b'] * EPSILON_RAD * area
q_ir_correct = q_ir_a + q_ir_b
print(f"\nCORRECT (physics-based):")
print(f"  qEarthIR_A = EARTH_IR × vfSideA × εPV × area")
print(f"  qEarthIR_A = {EARTH_IR} × {vf['vf_side_a']:.4f} × {EPSILON_PV} × {area:.0e} = {q_ir_a/1e6:.2f} MW")
print(f"  qEarthIR_B = EARTH_IR × vfSideB × εRad × area")
print(f"  qEarthIR_B = {EARTH_IR} × {vf['vf_side_b']:.4f} × {EPSILON_RAD} × {area:.0e} = {q_ir_b/1e6:.2f} MW")
print(f"  qEarthIR = qIR_A + qIR_B = {q_ir_correct/1e6:.2f} MW")

print(f"\nERROR: Wrong is {q_ir_wrong/q_ir_correct:.2f}x the correct value!")
print(f"       Overcounting by {(q_ir_wrong - q_ir_correct)/1e6:.1f} MW")

print("\n" + "=" * 70)
print("ALBEDO LOAD CALCULATION")
print("=" * 70)

albedo_scaling = math.cos(math.radians(beta))

# WRONG formula (current implementation)
q_alb_wrong = SOLAR * ALBEDO * vf['vf_total'] * albedo_scaling * ALPHA_PV * area
print(f"\nWRONG (current code):")
print(f"  qAlbedo = SOLAR × ALBEDO × vfTotal × cos(β) × αPV × area")
print(f"  qAlbedo = {SOLAR} × {ALBEDO} × {vf['vf_total']:.4f} × {albedo_scaling:.3f} × {ALPHA_PV} × {area:.0e}")
print(f"  qAlbedo = {q_alb_wrong/1e6:.2f} MW")

# CORRECT formula - only Side A (PV side) absorbs sunlight!
# Side B (radiator) has low solar absorptivity
q_alb_correct = SOLAR * ALBEDO * vf['vf_side_a'] * albedo_scaling * ALPHA_PV * area
print(f"\nCORRECT (only PV side absorbs sunlight):")
print(f"  qAlbedo = SOLAR × ALBEDO × vfSideA × cos(β) × αPV × area")
print(f"  qAlbedo = {SOLAR} × {ALBEDO} × {vf['vf_side_a']:.4f} × {albedo_scaling:.3f} × {ALPHA_PV} × {area:.0e}")
print(f"  qAlbedo = {q_alb_correct/1e6:.2f} MW")

print(f"\nERROR: Wrong is {q_alb_wrong/q_alb_correct:.2f}x the correct value!")

print("\n" + "=" * 70)
print("SUMMARY OF BUGS")
print("=" * 70)
print("""
BUG 1: Earth IR calculation
  - Current: EARTH_IR × vfTotal × (εPV + εRad) × area
  - Correct: EARTH_IR × (vfA × εPV + vfB × εRad) × area
  - Error: ~2x overcounting when vfA ≈ vfB

BUG 2: Albedo calculation  
  - Current: uses vfTotal (both sides)
  - Correct: should only use vfSideA (PV side)
  - Reason: Only the PV side has solar absorptivity α
           The radiator side (white paint) has α ≈ 0.1-0.2
  - Error: ~2x overcounting

BUG 3: What is vfTotal?
  - Current: vfTotal = vfSideA + vfSideB
  - This sums TWO separate view factors
  - For symmetric case: vfTotal ≈ 2 × vfSingle
  - The original ad-hoc VF was meant to be a SINGLE effective VF
""")

# Show impact at different beta angles
print("\n" + "=" * 70)
print("IMPACT AT DIFFERENT BETA ANGLES")
print("=" * 70)
print(f"\n{'Beta':>6} | {'VF_A':>8} | {'VF_B':>8} | {'VF_Total':>8} | {'IR Error':>10} | {'Alb Error':>10}")
print("-" * 70)

for beta in [90, 80, 70, 60]:
    vf = sun_tracking_view_factors(altitude, beta)
    
    # IR error
    q_ir_wrong = EARTH_IR * vf['vf_total'] * (EPSILON_PV + EPSILON_RAD)
    q_ir_correct = EARTH_IR * (vf['vf_side_a'] * EPSILON_PV + vf['vf_side_b'] * EPSILON_RAD)
    ir_error = q_ir_wrong / q_ir_correct if q_ir_correct > 0 else float('inf')
    
    # Albedo error
    alb_scale = math.cos(math.radians(beta))
    q_alb_wrong = SOLAR * ALBEDO * vf['vf_total'] * alb_scale * ALPHA_PV
    q_alb_correct = SOLAR * ALBEDO * vf['vf_side_a'] * alb_scale * ALPHA_PV
    alb_error = q_alb_wrong / q_alb_correct if q_alb_correct > 0 else float('inf')
    
    print(f"{beta:>6}° | {vf['vf_side_a']:>8.4f} | {vf['vf_side_b']:>8.4f} | {vf['vf_total']:>8.4f} | {ir_error:>9.2f}x | {alb_error:>9.2f}x")
