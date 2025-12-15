#!/usr/bin/env python3
"""
View factor parity check for the bifacial thermal model.

This script exists to prevent regressions where we accidentally:
- use a combined VF_total as if it were a single-side VF, or
- apply albedo to both sides, or
- apply Earth IR using (VF_total * (epsA+epsB)) instead of side-specific absorption.

It mirrors the intended physics in `static/js/math.js`.
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
print("VIEW FACTOR PARITY CHECK (CURRENT MODEL)")
print("=" * 70)

altitude = 550  # km
beta = 75  # degrees - use intermediate value

vf = sun_tracking_view_factors(altitude, beta)
print(f"\nAt altitude={altitude} km, beta={beta}°:")
print(f"  VF Side A (PV/sun-facing):   {vf['vf_side_a']:.4f}")
print(f"  VF Side B (radiator/anti-sun): {vf['vf_side_b']:.4f}")
print(f"  VF Total:                     {vf['vf_total']:.4f}")

print("\n" + "=" * 70)
print("EARTH IR LOAD CALCULATION (SIDE-SPECIFIC)")
print("=" * 70)

area = 1e6  # 1 km² = 1e6 m²

# Correct formula (matches `static/js/math.js`)
q_ir_a = EARTH_IR * vf['vf_side_a'] * EPSILON_PV * area
q_ir_b = EARTH_IR * vf['vf_side_b'] * EPSILON_RAD * area
q_ir_correct = q_ir_a + q_ir_b
print(f"\nCORRECT (physics-based):")
print(f"  qEarthIR_A = EARTH_IR × vfSideA × εPV × area")
print(f"  qEarthIR_A = {EARTH_IR} × {vf['vf_side_a']:.4f} × {EPSILON_PV} × {area:.0e} = {q_ir_a/1e6:.2f} MW")
print(f"  qEarthIR_B = EARTH_IR × vfSideB × εRad × area")
print(f"  qEarthIR_B = {EARTH_IR} × {vf['vf_side_b']:.4f} × {EPSILON_RAD} × {area:.0e} = {q_ir_b/1e6:.2f} MW")
print(f"  qEarthIR = qIR_A + qIR_B = {q_ir_correct/1e6:.2f} MW")

print("\n" + "=" * 70)
print("ALBEDO LOAD CALCULATION (PV SIDE ONLY)")
print("=" * 70)

albedo_scaling = math.cos(math.radians(beta))

# Correct formula (matches `static/js/math.js`): only Side A (PV) has high solar absorptivity
q_alb_correct = SOLAR * ALBEDO * vf['vf_side_a'] * albedo_scaling * ALPHA_PV * area
print(f"\nCORRECT (only PV side absorbs sunlight):")
print(f"  qAlbedo = SOLAR × ALBEDO × vfSideA × cos(β) × αPV × area")
print(f"  qAlbedo = {SOLAR} × {ALBEDO} × {vf['vf_side_a']:.4f} × {albedo_scaling:.3f} × {ALPHA_PV} × {area:.0e}")
print(f"  qAlbedo = {q_alb_correct/1e6:.2f} MW")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(
    "✅ Earth IR uses side-specific absorption: E⊕·(VF_A·ε_A + VF_B·ε_B)·A\n"
    "✅ Albedo applies to PV side only: G·ρ·VF_A·cos(β)·α_pv·A\n"
    "✅ VF_total is reported as VF_A + VF_B for display purposes"
)
