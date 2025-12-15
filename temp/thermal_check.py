"""
Quick sanity check for thermal panel math from static/js/math.js.
Uses the same default constants/state to recompute thermal outputs.
"""

import math

# Constants mirrored from math.js
SOLAR_IRRADIANCE_W_M2 = 1361
EARTH_IR_FLUX_W_M2 = 237
EARTH_ALBEDO_FACTOR = 0.30
T_SPACE_K = 3
STARLINK_ARRAY_M2 = 116
STARLINK_POWER_KW = 27
STARSHIP_PAYLOAD_KG = 100000
HOURS_PER_YEAR = 8760

# Default state from math.js
state = {
    "years": 5,
    "targetGW": 1,
    "solarAbsorptivity": 0.92,
    "emissivityPV": 0.85,
    "emissivityRad": 0.90,
    "pvEfficiency": 0.22,
    "betaAngle": 90,
    "maxDieTempC": 85,
    "tempDropC": 10,
    "launchCostPerKg": 1000,
    "satelliteCostPerW": 22,
    "specificPowerWPerKg": 36.5,
    "satellitePowerKW": 27,
    "sunFraction": 0.98,
    "cellDegradation": 2.5,
    "gpuFailureRate": 9,
    "nreCost": 500,
}


def calculate_orbital_area_m2():
    target_power_mw = state["targetGW"] * 1000
    target_power_w = target_power_mw * 1e6

    annual_retention = 1 - state["cellDegradation"] / 100
    capacity_sum = sum(math.pow(annual_retention, year) for year in range(state["years"]))
    avg_capacity_factor = capacity_sum / state["years"]
    sunlight_adjusted_factor = avg_capacity_factor * state["sunFraction"]
    required_initial_power_w = target_power_w / sunlight_adjusted_factor

    sat_power_w = state["satellitePowerKW"] * 1000
    sat_count = math.ceil(required_initial_power_w / sat_power_w)
    array_per_sat_m2 = STARLINK_ARRAY_M2 * (state["satellitePowerKW"] / STARLINK_POWER_KW)
    array_area_m2 = sat_count * array_per_sat_m2
    return array_area_m2


def calculate_thermal():
    SIGMA = 5.67e-8
    area_m2 = calculate_orbital_area_m2()

    alpha_pv = state["solarAbsorptivity"]
    epsilon_pv = state["emissivityPV"]
    epsilon_rad = state["emissivityRad"]
    pv_eff = state["pvEfficiency"]
    beta = state["betaAngle"]

    vf_earth = 0.08 + (90 - beta) * 0.002

    power_generated = SOLAR_IRRADIANCE_W_M2 * pv_eff * area_m2
    q_solar = SOLAR_IRRADIANCE_W_M2 * alpha_pv * area_m2 - power_generated
    q_earth_ir = EARTH_IR_FLUX_W_M2 * vf_earth * (epsilon_pv + epsilon_rad) * area_m2
    albedo_scaling = math.cos(math.radians(beta))
    q_albedo = SOLAR_IRRADIANCE_W_M2 * EARTH_ALBEDO_FACTOR * vf_earth * albedo_scaling * alpha_pv * area_m2
    q_heatloop = power_generated

    total_heat_in = q_solar + q_earth_ir + q_albedo + q_heatloop
    total_emissivity = epsilon_pv + epsilon_rad

    eq_temp_k = ((total_heat_in / (SIGMA * area_m2 * total_emissivity)) + T_SPACE_K**4) ** 0.25
    eq_temp_c = eq_temp_k - 273.15

    compute_heat_in = q_solar + q_earth_ir + q_albedo + power_generated
    compute_temp_k = ((compute_heat_in / (SIGMA * area_m2 * total_emissivity)) + T_SPACE_K**4) ** 0.25
    compute_temp_c = compute_temp_k - 273.15

    radiator_temp_c = state["maxDieTempC"] - state["tempDropC"]
    delta_t4 = (radiator_temp_c + 273.15) ** 4 - T_SPACE_K**4
    area_required_m2 = total_heat_in / (SIGMA * total_emissivity * delta_t4)

    return {
        "area_m2": area_m2,
        "power_generated_mw": power_generated / 1e6,
        "q_solar_mw": q_solar / 1e6,
        "q_earth_ir_mw": q_earth_ir / 1e6,
        "q_albedo_mw": q_albedo / 1e6,
        "q_heatloop_mw": q_heatloop / 1e6,
        "total_heat_mw": total_heat_in / 1e6,
        "eq_temp_c": eq_temp_c,
        "compute_temp_c": compute_temp_c,
        "radiator_temp_c": radiator_temp_c,
        "area_required_km2": area_required_m2 / 1e6,
    }


if __name__ == "__main__":
    result = calculate_thermal()
    print("Area (km^2):", result["area_m2"] / 1e6)
    print("Power generated (MW):", result["power_generated_mw"])
    print("Q_solar (MW):", result["q_solar_mw"])
    print("Q_earth_ir (MW):", result["q_earth_ir_mw"])
    print("Q_albedo (MW):", result["q_albedo_mw"])
    print("Q_heatloop (MW):", result["q_heatloop_mw"])
    print("Total heat in (MW):", result["total_heat_mw"])
    print("Eq temp (C):", result["eq_temp_c"])
    print("Compute temp (C):", result["compute_temp_c"])
    print("Radiator target (C):", result["radiator_temp_c"])
    print("Area required (km^2):", result["area_required_km2"])

