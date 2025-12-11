"""
Quick parity check for CostModel calculations in static/js/math.js.

This mirrors the JS logic to validate displayed figures against the
Python recomputation. Run with the repo venv:

    ..\\venv\\Scripts\\python.exe temp\\check_numbers.py
"""

from dataclasses import dataclass
from math import ceil, pow


# Constants copied from static/js/math.js (JS defaults)
CONSTANTS = {
    "TARGET_POWER_MW": 1000,
    "HOURS_PER_YEAR": 8760,
    "STARLINK_MASS_KG": 740,
    "STARLINK_POWER_KW": 27,
    "STARLINK_ARRAY_M2": 116,
    "STARSHIP_PAYLOAD_KG": 100_000,
    "STARSHIP_LOX_GAL_PER_LAUNCH": 787_000,
    "STARSHIP_METHANE_GAL_PER_LAUNCH": 755_000,
    "NGCC_ACRES": 30,
    "NGCC_HEAT_RATE_BTU_KWH": 6370,
    "GE_7HA_POWER_MW": 430,
    "BTU_PER_CF": 1000,
    "CF_PER_BCF": 1e9,
    "ORBITAL_OPS_FRAC": 0.01,
    "NATGAS_OVERHEAD_FRAC": 0.04,
    "NATGAS_MAINTENANCE_FRAC": 0.03,
    "NATGAS_COMMS_FRAC": 0.01,
    "SOLAR_IRRADIANCE_W_M2": 1361,
}


# Slider defaults from static/js/math.js
STATE = {
    "years": 5,
    "targetGW": 1,
    "emissivity": 0.85,
    "albedoViewFactor": 0.2,
    "maxDieTempC": 75,
    "tempDropC": 10,
    "launchCostPerKg": 1000,
    "satelliteCostPerW": 22,
    "specificPowerWPerKg": 36.5,
    "satellitePowerKW": 27,
    "sunFraction": 0.98,
    "cellDegradation": 2.5,
    "gpuFailureRate": 9,
    "nreCost": 500,
    "gasTurbineCapexPerKW": 1450,
    "electricalCostPerW": 5.25,
    "mechanicalCostPerW": 3.0,
    "civilCostPerW": 2.5,
    "networkCostPerW": 1.75,
    "pue": 1.2,
    "gasPricePerMMBtu": 4.30,
    "heatRateBtuKwh": 6200,
    "capacityFactor": 0.85,
}


@dataclass
class Derived:
    TARGET_POWER_MW: float
    TARGET_POWER_W: float
    TARGET_POWER_KW: float


def get_derived(state) -> Derived:
    target_power_mw = state["targetGW"] * 1000
    return Derived(
        TARGET_POWER_MW=target_power_mw,
        TARGET_POWER_W=target_power_mw * 1e6,
        TARGET_POWER_KW=target_power_mw * 1000,
    )


def calculate_orbital(state):
    derived = get_derived(state)
    total_hours = state["years"] * CONSTANTS["HOURS_PER_YEAR"]

    annual_pv_retention = 1 - (state["cellDegradation"] / 100)
    annual_gpu_retention = 1 - (state["gpuFailureRate"] / 100)
    annual_retention = annual_pv_retention * annual_gpu_retention
    capacity_sum = sum(pow(annual_retention, year) for year in range(state["years"]))
    avg_capacity_factor = capacity_sum / state["years"]
    sunlight_adjusted = avg_capacity_factor * state["sunFraction"]
    required_initial_power_w = derived.TARGET_POWER_W / sunlight_adjusted

    mass_per_sat = (state["satellitePowerKW"] * 1000) / state["specificPowerWPerKg"]
    satellite_count = ceil(required_initial_power_w / (state["satellitePowerKW"] * 1000))
    total_mass_kg = satellite_count * mass_per_sat
    actual_initial_power_w = satellite_count * state["satellitePowerKW"] * 1000

    hardware_cost = state["satelliteCostPerW"] * actual_initial_power_w
    launch_cost = state["launchCostPerKg"] * total_mass_kg
    base_cost = hardware_cost + launch_cost
    ops_cost = hardware_cost * CONSTANTS["ORBITAL_OPS_FRAC"]
    gpu_replace = 0
    nre_cost = state["nreCost"] * 1e6
    total_cost = base_cost + ops_cost + nre_cost

    energy_mwh = derived.TARGET_POWER_MW * total_hours
    cost_per_w = total_cost / derived.TARGET_POWER_W
    lcoe = total_cost / energy_mwh

    array_per_sat_m2 = CONSTANTS["STARLINK_ARRAY_M2"] * (
        state["satellitePowerKW"] / CONSTANTS["STARLINK_POWER_KW"]
    )
    array_area_m2 = satellite_count * array_per_sat_m2
    array_area_km2 = array_area_m2 / 1e6

    starship_launches = ceil(total_mass_kg / CONSTANTS["STARSHIP_PAYLOAD_KG"])
    lox_gal = starship_launches * CONSTANTS["STARSHIP_LOX_GAL_PER_LAUNCH"]
    methane_gal = starship_launches * CONSTANTS["STARSHIP_METHANE_GAL_PER_LAUNCH"]

    degradation_margin = (actual_initial_power_w / derived.TARGET_POWER_W - 1) * 100

    return {
        "totalMassKg": total_mass_kg,
        "hardwareCost": hardware_cost,
        "launchCost": launch_cost,
        "opsCost": ops_cost,
        "gpuReplacementCost": gpu_replace,
        "nreCost": nre_cost,
        "baseCost": base_cost,
        "totalCost": total_cost,
        "energyMWh": energy_mwh,
        "costPerW": cost_per_w,
        "lcoe": lcoe,
        "satelliteCount": satellite_count,
        "arrayAreaKm2": array_area_km2,
        "starshipLaunches": starship_launches,
        "loxGallons": lox_gal,
        "methaneGallons": methane_gal,
        "avgCapacityFactor": avg_capacity_factor,
        "degradationMargin": degradation_margin,
        "actualInitialPowerW": actual_initial_power_w,
        "requiredInitialPowerW": required_initial_power_w,
    }


def calculate_terrestrial(state):
    derived = get_derived(state)
    total_hours = state["years"] * CONSTANTS["HOURS_PER_YEAR"]

    power_gen_cost_per_w = state["gasTurbineCapexPerKW"] * state["pue"] / 1000
    power_gen_cost = power_gen_cost_per_w * derived.TARGET_POWER_W
    electrical_cost = state["electricalCostPerW"] * derived.TARGET_POWER_W
    mechanical_cost = state["mechanicalCostPerW"] * derived.TARGET_POWER_W
    civil_cost = state["civilCostPerW"] * derived.TARGET_POWER_W
    network_cost = state["networkCostPerW"] * derived.TARGET_POWER_W

    infra_capex = (
        power_gen_cost + electrical_cost + mechanical_cost + civil_cost + network_cost
    )
    facility_capex_per_w = (
        power_gen_cost_per_w
        + state["electricalCostPerW"]
        + state["mechanicalCostPerW"]
        + state["civilCostPerW"]
        + state["networkCostPerW"]
    )

    energy_mwh = derived.TARGET_POWER_MW * total_hours * state["capacityFactor"]
    generation_mwh = energy_mwh * state["pue"]
    fuel_cost_per_mwh = state["heatRateBtuKwh"] * state["gasPricePerMMBtu"] / 1000
    fuel_cost_total = fuel_cost_per_mwh * generation_mwh

    total_cost = infra_capex + fuel_cost_total
    cost_per_w = total_cost / derived.TARGET_POWER_W
    lcoe = total_cost / energy_mwh

    gas_consumption_bcf = (
        generation_mwh * 1000 * state["heatRateBtuKwh"] / CONSTANTS["BTU_PER_CF"] / CONSTANTS["CF_PER_BCF"]
    )
    total_generation_mw = derived.TARGET_POWER_MW * state["pue"]
    turbine_count = ceil(total_generation_mw / CONSTANTS["GE_7HA_POWER_MW"])

    fuel_cost_per_w_year = fuel_cost_per_mwh * state["pue"] * 0.00876

    return {
        "powerGenCost": power_gen_cost,
        "powerGenCostPerW": power_gen_cost_per_w,
        "electricalCost": electrical_cost,
        "mechanicalCost": mechanical_cost,
        "civilCost": civil_cost,
        "networkCost": network_cost,
        "infraCapex": infra_capex,
        "facilityCapexPerW": facility_capex_per_w,
        "fuelCostPerMWh": fuel_cost_per_mwh,
        "fuelCostTotal": fuel_cost_total,
        "fuelCostPerWYear": fuel_cost_per_w_year,
        "totalCost": total_cost,
        "energyMWh": energy_mwh,
        "generationMWh": generation_mwh,
        "costPerW": cost_per_w,
        "lcoe": lcoe,
        "totalHours": total_hours,
        "gasConsumptionBCF": gas_consumption_bcf,
        "turbineCount": turbine_count,
        "totalGenerationMW": total_generation_mw,
    }


def fmt_dollars(num):
    if abs(num) >= 1e12:
        return f"${num/1e12:.1f}T"
    if abs(num) >= 1e9:
        return f"${num/1e9:.1f}B"
    if abs(num) >= 1e6:
        return f"${num/1e6:.0f}M"
    return f"${num:,.0f}"


def main():
    orbital = calculate_orbital(STATE)
    terrestrial = calculate_terrestrial(STATE)

    print("=== Orbital ===")
    print("Total cost:", fmt_dollars(orbital["totalCost"]))
    print("Hardware:", fmt_dollars(orbital["hardwareCost"]))
    print("Launch:", fmt_dollars(orbital["launchCost"]))
    print("Ops+GPU:", fmt_dollars(orbital["opsCost"] + orbital["gpuReplacementCost"]))
    print("Mass to LEO:", f"{orbital['totalMassKg']/1e6:.1f}M kg")
    print("LCOE:", f"${orbital['lcoe']:.0f}/MWh")
    print("Cost per W:", f"${orbital['costPerW']:.2f}/W")
    print("Starship launches:", orbital["starshipLaunches"])

    print("\n=== Terrestrial ===")
    print("Total cost:", fmt_dollars(terrestrial["totalCost"]))
    print("Power gen:", fmt_dollars(terrestrial["powerGenCost"]))
    print("Electrical:", fmt_dollars(terrestrial["electricalCost"]))
    print("Mechanical:", fmt_dollars(terrestrial["mechanicalCost"]))
    print("Civil:", fmt_dollars(terrestrial["civilCost"]))
    print("Fuel:", fmt_dollars(terrestrial["fuelCostTotal"]))
    print("Capex $/W:", f"${terrestrial['facilityCapexPerW']:.2f}/W")
    print("Cost per W:", f"${terrestrial['costPerW']:.2f}/W")
    print("LCOE:", f"${terrestrial['lcoe']:.0f}/MWh")
    print("Turbines:", terrestrial["turbineCount"])


if __name__ == "__main__":
    main()

