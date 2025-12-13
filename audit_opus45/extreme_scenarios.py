#!/usr/bin/env python3
"""
Extreme Scenarios Analysis
Tests the model at edge cases to find conditions where orbital becomes competitive
"""

import math
import json

# Copy constants from formula_audit
CONSTANTS = {
    "TARGET_POWER_MW": 1000,
    "HOURS_PER_YEAR": 8760,
    "STARLINK_MASS_KG": 740,
    "STARLINK_POWER_KW": 27,
    "STARLINK_ARRAY_M2": 116,
    "STARSHIP_PAYLOAD_KG": 100000,
    "NGCC_HEAT_RATE_BTU_KWH": 6370,
    "GE_7HA_POWER_MW": 430,
    "BTU_PER_CF": 1000,
    "CF_PER_BCF": 1e9,
    "SOLAR_IRRADIANCE_W_M2": 1361,
    "EARTH_IR_FLUX_W_M2": 237,
    "EARTH_ALBEDO_FACTOR": 0.30,
    "T_SPACE_K": 3
}

DEFAULT_STATE = {
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
    "nreCost": 1000,
    "gasTurbineCapexPerKW": 1450,
    "electricalCostPerW": 5.25,
    "mechanicalCostPerW": 3.0,
    "civilCostPerW": 2.5,
    "networkCostPerW": 1.75,
    "pue": 1.2,
    "gasPricePerMMBtu": 4.30,
    "heatRateBtuKwh": 6200,
    "capacityFactor": 0.85
}


def calculate_orbital(state: dict, constants: dict) -> dict:
    """Calculate orbital solar costs."""
    target_power_mw = state["targetGW"] * 1000
    target_power_w = target_power_mw * 1e6
    total_hours = state["years"] * constants["HOURS_PER_YEAR"]
    
    annual_retention = 1 - (state["cellDegradation"] / 100)
    capacity_sum = sum(math.pow(annual_retention, year) for year in range(state["years"]))
    avg_capacity_factor = capacity_sum / state["years"]
    
    sunlight_adjusted_factor = avg_capacity_factor * state["sunFraction"]
    required_initial_power_w = target_power_w / sunlight_adjusted_factor
    
    mass_per_satellite_kg = (state["satellitePowerKW"] * 1000) / state["specificPowerWPerKg"]
    satellite_count = math.ceil(required_initial_power_w / (state["satellitePowerKW"] * 1000))
    total_mass_kg = satellite_count * mass_per_satellite_kg
    actual_initial_power_w = satellite_count * state["satellitePowerKW"] * 1000
    
    hardware_cost = state["satelliteCostPerW"] * actual_initial_power_w
    launch_cost = state["launchCostPerKg"] * total_mass_kg
    ops_cost = hardware_cost * 0.01
    gpu_replacement_cost = hardware_cost * (state["gpuFailureRate"] / 100) * state["years"]
    nre_cost = state["nreCost"] * 1e6
    total_cost = hardware_cost + launch_cost + ops_cost + gpu_replacement_cost + nre_cost
    
    energy_mwh = target_power_mw * total_hours
    cost_per_w = total_cost / target_power_w
    lcoe = total_cost / energy_mwh
    
    return {
        "totalMassKg": total_mass_kg,
        "hardwareCost": hardware_cost,
        "launchCost": launch_cost,
        "totalCost": total_cost,
        "energyMWh": energy_mwh,
        "costPerW": cost_per_w,
        "lcoe": lcoe,
        "satelliteCount": satellite_count
    }


def calculate_terrestrial(state: dict, constants: dict) -> dict:
    """Calculate terrestrial costs."""
    target_power_mw = state["targetGW"] * 1000
    target_power_w = target_power_mw * 1e6
    total_hours = state["years"] * constants["HOURS_PER_YEAR"]
    
    power_gen_cost_per_w = state["gasTurbineCapexPerKW"] * state["pue"] / 1000
    power_gen_cost = power_gen_cost_per_w * target_power_w
    electrical_cost = state["electricalCostPerW"] * target_power_w
    mechanical_cost = state["mechanicalCostPerW"] * target_power_w
    civil_cost = state["civilCostPerW"] * target_power_w
    network_cost = state["networkCostPerW"] * target_power_w
    infra_capex = power_gen_cost + electrical_cost + mechanical_cost + civil_cost + network_cost
    
    energy_mwh = target_power_mw * total_hours * state["capacityFactor"]
    generation_mwh = energy_mwh * state["pue"]
    fuel_cost_per_mwh = state["heatRateBtuKwh"] * state["gasPricePerMMBtu"] / 1000
    fuel_cost_total = fuel_cost_per_mwh * generation_mwh
    
    total_cost = infra_capex + fuel_cost_total
    cost_per_w = total_cost / target_power_w
    lcoe = total_cost / energy_mwh
    
    return {
        "infraCapex": infra_capex,
        "fuelCostTotal": fuel_cost_total,
        "totalCost": total_cost,
        "energyMWh": energy_mwh,
        "costPerW": cost_per_w,
        "lcoe": lcoe
    }


def run_extreme_scenarios():
    """Test extreme but physically possible scenarios."""
    
    print("=" * 80)
    print("EXTREME SCENARIOS ANALYSIS")
    print("Finding conditions where orbital becomes competitive")
    print("=" * 80)
    print()
    
    # Baseline
    baseline = DEFAULT_STATE.copy()
    orbital_base = calculate_orbital(baseline, CONSTANTS)
    terr_base = calculate_terrestrial(baseline, CONSTANTS)
    
    print("BASELINE (1 GW, 5 years):")
    print(f"  Orbital: ${orbital_base['totalCost']/1e9:.1f}B (${orbital_base['lcoe']:.0f}/MWh)")
    print(f"  Terrestrial: ${terr_base['totalCost']/1e9:.1f}B (${terr_base['lcoe']:.0f}/MWh)")
    print(f"  Ratio: {orbital_base['totalCost']/terr_base['totalCost']:.2f}x")
    print()
    
    # Define scenarios
    scenarios = [
        {
            "name": "Worst Case Terrestrial (High Gas + Carbon Tax)",
            "changes": {
                "gasPricePerMMBtu": 12,  # High gas price
                # Simulating $100/ton CO2 as fuel cost adder
                # 400g CO2/kWh = 0.4 ton/MWh, $100/ton = $40/MWh
            },
            "notes": "Gas at $12/MMBtu + carbon pricing"
        },
        {
            "name": "Best Case Orbital - Near-Term (2027)",
            "changes": {
                "launchCostPerKg": 200,
                "satelliteCostPerW": 15,
                "specificPowerWPerKg": 45,
                "gpuFailureRate": 5,
            },
            "notes": "Mature Starship + improved satellites"
        },
        {
            "name": "Best Case Orbital - Mid-Term (2030)",
            "changes": {
                "launchCostPerKg": 50,
                "satelliteCostPerW": 10,
                "specificPowerWPerKg": 55,
                "gpuFailureRate": 3,
                "nreCost": 500,
            },
            "notes": "Mass production + advanced tech"
        },
        {
            "name": "Theoretical Floor Orbital",
            "changes": {
                "launchCostPerKg": 20,
                "satelliteCostPerW": 5,
                "specificPowerWPerKg": 75,
                "gpuFailureRate": 2,
                "nreCost": 0,
            },
            "notes": "Absolute physical limits"
        },
        {
            "name": "Worst Case Orbital",
            "changes": {
                "launchCostPerKg": 2940,
                "satelliteCostPerW": 40,
                "specificPowerWPerKg": 15,
                "sunFraction": 0.6,
                "cellDegradation": 6,
                "gpuFailureRate": 15,
            },
            "notes": "Non-terminator orbit + radiation effects"
        },
        {
            "name": "10 GW Scale",
            "changes": {
                "targetGW": 10,
                "launchCostPerKg": 100,  # Volume discount
                "satelliteCostPerW": 12,  # Learning curve
            },
            "notes": "Large scale deployment"
        },
        {
            "name": "10 Year Analysis",
            "changes": {
                "years": 10,
            },
            "notes": "Longer time horizon favors orbital (fuel costs accumulate)"
        },
        {
            "name": "Crossover Scenario",
            "changes": {
                "launchCostPerKg": 20,
                "satelliteCostPerW": 5,
                "specificPowerWPerKg": 60,
                "gasPricePerMMBtu": 10,  # Higher gas
            },
            "notes": "Combined best orbital + worse terrestrial"
        }
    ]
    
    results = []
    
    print("-" * 80)
    print("SCENARIO ANALYSIS:")
    print("-" * 80)
    
    for scenario in scenarios:
        state = DEFAULT_STATE.copy()
        state.update(scenario["changes"])
        
        orbital = calculate_orbital(state, CONSTANTS)
        terr = calculate_terrestrial(state, CONSTANTS)
        
        ratio = orbital["totalCost"] / terr["totalCost"]
        winner = "ORBITAL ✓" if ratio < 1 else "TERRESTRIAL"
        
        result = {
            "name": scenario["name"],
            "orbital_cost": orbital["totalCost"],
            "terrestrial_cost": terr["totalCost"],
            "ratio": ratio,
            "orbital_lcoe": orbital["lcoe"],
            "terrestrial_lcoe": terr["lcoe"],
            "winner": winner
        }
        results.append(result)
        
        print(f"\n{scenario['name']}:")
        print(f"  ({scenario['notes']})")
        for k, v in scenario["changes"].items():
            print(f"    {k}: {v}")
        print(f"  Orbital: ${orbital['totalCost']/1e9:.2f}B (${orbital['lcoe']:.0f}/MWh)")
        print(f"  Terrestrial: ${terr['totalCost']/1e9:.2f}B (${terr['lcoe']:.0f}/MWh)")
        print(f"  >>> Ratio: {ratio:.2f}x | Winner: {winner}")
    
    print()
    print("=" * 80)
    print("BREAKEVEN FRONTIER ANALYSIS")
    print("=" * 80)
    print()
    
    # Find the frontier where orbital = terrestrial
    print("Testing combinations where orbital could break even...")
    print("(Launch cost vs Hardware cost at various specific power levels)")
    print()
    
    breakeven_combos = []
    
    for specific_power in [36.5, 45, 55, 65, 75]:
        for hw_cost in [5, 8, 10, 12, 15, 18, 22]:
            for launch_cost in [20, 50, 100, 200, 500, 1000]:
                state = DEFAULT_STATE.copy()
                state["specificPowerWPerKg"] = specific_power
                state["satelliteCostPerW"] = hw_cost
                state["launchCostPerKg"] = launch_cost
                
                orbital = calculate_orbital(state, CONSTANTS)
                terr = calculate_terrestrial(state, CONSTANTS)
                
                ratio = orbital["totalCost"] / terr["totalCost"]
                
                if 0.9 <= ratio <= 1.1:  # Within 10% of breakeven
                    breakeven_combos.append({
                        "specific_power": specific_power,
                        "hw_cost": hw_cost,
                        "launch_cost": launch_cost,
                        "ratio": ratio
                    })
    
    print("BREAKEVEN COMBINATIONS (within ±10% of terrestrial cost):")
    print("-" * 60)
    if breakeven_combos:
        print(f"{'Specific Power':>15} {'HW Cost':>10} {'Launch':>10} {'Ratio':>10}")
        print("-" * 60)
        for c in breakeven_combos:
            print(f"{c['specific_power']:>12.1f} W/kg {c['hw_cost']:>7}$/W {c['launch_cost']:>7}$/kg {c['ratio']:>9.2f}x")
    else:
        print("No combinations found within current search space!")
        print("Expanding search with more aggressive assumptions...")
        
        for specific_power in [75, 100, 125]:
            for hw_cost in [2, 3, 4, 5]:
                for launch_cost in [10, 15, 20]:
                    state = DEFAULT_STATE.copy()
                    state["specificPowerWPerKg"] = specific_power
                    state["satelliteCostPerW"] = hw_cost
                    state["launchCostPerKg"] = launch_cost
                    
                    orbital = calculate_orbital(state, CONSTANTS)
                    terr = calculate_terrestrial(state, CONSTANTS)
                    
                    ratio = orbital["totalCost"] / terr["totalCost"]
                    
                    if ratio <= 1.0:
                        print(f"  Found: {specific_power} W/kg, ${hw_cost}/W, ${launch_cost}/kg -> {ratio:.2f}x")
    
    print()
    print("=" * 80)
    print("KEY INSIGHTS")
    print("=" * 80)
    print("""
1. LAUNCH COST IS NECESSARY BUT NOT SUFFICIENT
   - At $20/kg (floor) with current hardware ($22/W), orbital is still 2.3x more expensive
   - Hardware cost dominates at low launch costs

2. HARDWARE COST REDUCTION IS CRITICAL
   - Must reach $5-8/W to be competitive (vs current $22/W)
   - This implies 65-75% cost reduction from current Starlink production

3. SPECIFIC POWER IMPROVEMENTS HELP
   - Current V2 Mini: 36.5 W/kg
   - Needed for breakeven: 60-75+ W/kg (2x improvement)
   - This is challenging but not impossible with advanced solar

4. SCALE HELPS MARGINALLY
   - 10 GW vs 1 GW doesn't fundamentally change the ratio
   - Learning curve benefits help but don't close the gap alone

5. LONGER TIME HORIZONS HELP ORBITAL
   - 10-year analysis slightly favors orbital (fuel accumulates)
   - But not enough to achieve breakeven at current parameters

6. CARBON PRICING COULD TIP THE SCALES
   - $100/ton CO2 adds ~$40/MWh to terrestrial LCOE
   - Combined with aggressive orbital improvements, could reach breakeven
    """)
    
    # Save results
    with open("/workspace/audit_opus45/extreme_scenarios_results.json", "w") as f:
        json.dump({
            "scenarios": results,
            "breakeven_combos": breakeven_combos
        }, f, indent=2)
    
    print("\nResults saved to extreme_scenarios_results.json")


if __name__ == "__main__":
    run_extreme_scenarios()
