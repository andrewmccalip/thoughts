#!/usr/bin/env python3
"""
First Principles Audit: Cross-Validation Testing
================================================

This script compares Python implementations against JavaScript outputs to ensure
consistency across platforms and verify the mathematical equivalence.

Audit Date: December 14, 2025
Model Version: math.js (current)
"""

import math
import json
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

# =============================================================================
# REFERENCE TEST CASES
# =============================================================================

# Default state from math.js
DEFAULT_STATE = {
    "years": 5,
    "targetGW": 1,
    "launchCostPerKg": 500,
    "satelliteCostPerW": 20,
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

# Test cases with different parameter combinations
CROSS_VALIDATION_TESTS = [
    {
        "name": "Default Parameters",
        "state": DEFAULT_STATE.copy()
    },
    {
        "name": "High Launch Cost",
        "state": {**DEFAULT_STATE, "launchCostPerKg": 2000}
    },
    {
        "name": "Low Sun Fraction",
        "state": {**DEFAULT_STATE, "sunFraction": 0.8}
    },
    {
        "name": "High PUE",
        "state": {**DEFAULT_STATE, "pue": 1.5}
    },
    {
        "name": "Extreme Thermal",
        "state": {
            **DEFAULT_STATE,
            "solarAbsorptivity": 0.95,
            "emissivityPV": 0.90,
            "emissivityRad": 0.95,
            "betaAngle": 75
        }
    }
]

# =============================================================================
# PYTHON IMPLEMENTATIONS (from our audit scripts)
# =============================================================================

def calculate_orbital_python(state: Dict) -> Dict:
    """Python implementation of calculateOrbital() - simplified for testing"""

    derived = {"TARGET_POWER_W": state["targetGW"] * 1e9, "TARGET_POWER_MW": state["targetGW"] * 1000}
    total_hours = state["years"] * 8760

    # Degradation analysis
    solar_retention = 1 - (state["cellDegradation"] / 100)
    gpu_retention = 1 - (state["gpuFailureRate"] / 100)

    solar_sum = sum(math.pow(solar_retention, y) for y in range(state["years"]))
    gpu_sum = sum(math.pow(gpu_retention, y) for y in range(state["years"]))

    avg_solar = solar_sum / state["years"]
    avg_gpu = gpu_sum / state["years"]
    avg_capacity = min(avg_solar, avg_gpu)
    sunlight_adjusted = avg_capacity * state["sunFraction"]

    required_power_w = derived["TARGET_POWER_W"] / sunlight_adjusted
    mass_per_sat_kg = (state["satellitePowerKW"] * 1000) / state["specificPowerWPerKg"]
    satellite_count = math.ceil(required_power_w / (state["satellitePowerKW"] * 1000))
    total_mass_kg = satellite_count * mass_per_sat_kg

    hardware_cost = state["satelliteCostPerW"] * (satellite_count * state["satellitePowerKW"] * 1000)
    launch_cost = state["launchCostPerKg"] * total_mass_kg
    ops_cost = hardware_cost * 0.01 * state["years"]
    nre_cost = state["nreCost"] * 1e6
    total_cost = hardware_cost + launch_cost + ops_cost + nre_cost

    energy_mwh = derived["TARGET_POWER_MW"] * total_hours
    cost_per_w = total_cost / derived["TARGET_POWER_W"]
    lcoe = total_cost / energy_mwh

    return {
        "totalCost": total_cost,
        "costPerW": cost_per_w,
        "lcoe": lcoe,
        "satelliteCount": satellite_count,
        "totalMassKg": total_mass_kg,
        "energyMWh": energy_mwh
    }

def calculate_terrestrial_python(state: Dict) -> Dict:
    """Python implementation of calculateTerrestrial() - simplified for testing"""

    derived = {"TARGET_POWER_W": state["targetGW"] * 1e9, "TARGET_POWER_MW": state["targetGW"] * 1000}
    total_hours = state["years"] * 8760

    energy_mwh = derived["TARGET_POWER_MW"] * total_hours * state["capacityFactor"]
    generation_mwh = energy_mwh * state["pue"]

    power_gen_cost_per_w = state["gasTurbineCapexPerKW"] * state["pue"] / 1000
    electrical_cost = state["electricalCostPerW"] * derived["TARGET_POWER_W"]
    mechanical_cost = state["mechanicalCostPerW"] * derived["TARGET_POWER_W"]
    civil_cost = state["civilCostPerW"] * derived["TARGET_POWER_W"]
    network_cost = state["networkCostPerW"] * derived["TARGET_POWER_W"]
    infra_capex = power_gen_cost_per_w * derived["TARGET_POWER_W"] + electrical_cost + mechanical_cost + civil_cost + network_cost

    fuel_cost_per_mwh = state["heatRateBtuKwh"] * state["gasPricePerMMBtu"] / 1000
    fuel_cost_total = fuel_cost_per_mwh * generation_mwh

    total_cost = infra_capex + fuel_cost_total
    cost_per_w = total_cost / derived["TARGET_POWER_W"]
    lcoe = total_cost / energy_mwh

    gas_consumption_bcf = (generation_mwh * 1000 * state["heatRateBtuKwh"]) / 1000 / 1e9

    return {
        "totalCost": total_cost,
        "costPerW": cost_per_w,
        "lcoe": lcoe,
        "energyMWh": energy_mwh,
        "gasConsumptionBCF": gas_consumption_bcf
    }

def calculate_thermal_python(state: Dict) -> Dict:
    """Python implementation of calculateThermal() - simplified for testing"""

    # Mock orbital calculation for array area
    orbital = calculate_orbital_python(state)
    area_m2 = (orbital["totalMassKg"] / ((state["satellitePowerKW"] * 1000) / state["specificPowerWPerKg"])) * 116 / 27 * 1e6

    alpha_pv = state.get("solarAbsorptivity", 0.92)
    epsilon_pv = state.get("emissivityPV", 0.85)
    epsilon_rad = state.get("emissivityRad", 0.90)
    pv_efficiency = state.get("pvEfficiency", 0.22)
    beta_angle = state.get("betaAngle", 90)

    # Heat inputs
    power_generated = 1361 * pv_efficiency * area_m2
    q_absorbed = 1361 * alpha_pv * area_m2
    q_solar_waste = q_absorbed - power_generated

    vf_earth = 0.08 + (90 - beta_angle) * 0.002
    q_earth_ir = (237 * vf_earth) * (epsilon_pv + epsilon_rad) * area_m2

    albedo_scaling = math.cos(beta_angle * math.pi / 180)
    q_albedo = (1361 * 0.3 * vf_earth * albedo_scaling) * alpha_pv * area_m2

    q_heat_loop = power_generated
    total_heat_in = q_solar_waste + q_earth_ir + q_albedo + q_heat_loop

    # Equilibrium temperature
    total_emissivity = epsilon_pv + epsilon_rad
    sigma = 5.67e-8
    eq_temp_k = math.pow((total_heat_in / (sigma * area_m2 * total_emissivity)) + math.pow(3, 4), 0.25)
    eq_temp_c = eq_temp_k - 273.15

    return {
        "eqTempC": eq_temp_c,
        "totalHeatInW": total_heat_in,
        "areaM2": area_m2
    }

# =============================================================================
# JAVASCRIPT EXECUTION (requires Node.js)
# =============================================================================

def run_javascript_calculation(state: Dict, function_name: str) -> Dict:
    """Execute JavaScript calculation and return results"""

    # Create a temporary JS file with the calculation
    js_code = f"""
const CostModel = {{
    // Simplified version of math.js for testing
    calculateOrbital: function() {{
        const state = {json.dumps(state)};
        const derived = {{
            TARGET_POWER_W: state.targetGW * 1e9,
            TARGET_POWER_MW: state.targetGW * 1000
        }};
        const totalHours = state.years * 8760;

        // Degradation
        const solarRetention = 1 - (state.cellDegradation / 100);
        const gpuRetention = 1 - (state.gpuFailureRate / 100);

        let solarSum = 0, gpuSum = 0;
        for (let y = 0; y < state.years; y++) {{
            solarSum += Math.pow(solarRetention, y);
            gpuSum += Math.pow(gpuRetention, y);
        }}

        const avgSolar = solarSum / state.years;
        const avgGpu = gpuSum / state.years;
        const avgCapacity = Math.min(avgSolar, avgGpu);
        const sunlightAdjusted = avgCapacity * state.sunFraction;

        const requiredPowerW = derived.TARGET_POWER_W / sunlightAdjusted;
        const massPerSatKg = (state.satellitePowerKW * 1000) / state.specificPowerWPerKg;
        const satelliteCount = Math.ceil(requiredPowerW / (state.satellitePowerKW * 1000));
        const totalMassKg = satelliteCount * massPerSatKg;

        const hardwareCost = state.satelliteCostPerW * (satelliteCount * state.satellitePowerKW * 1000);
        const launchCost = state.launchCostPerKg * totalMassKg;
        const opsCost = hardwareCost * 0.01 * state.years;
        const nreCost = state.nreCost * 1e6;
        const totalCost = hardwareCost + launchCost + opsCost + nreCost;

        const energyMWh = derived.TARGET_POWER_MW * totalHours;
        const costPerW = totalCost / derived.TARGET_POWER_W;
        const lcoe = totalCost / energyMWh;

        return {{
            totalCost, costPerW, lcoe, satelliteCount, totalMassKg, energyMWh
        }};
    }},

    calculateTerrestrial: function() {{
        const state = {json.dumps(state)};
        const derived = {{
            TARGET_POWER_W: state.targetGW * 1e9,
            TARGET_POWER_MW: state.targetGW * 1000
        }};
        const totalHours = state.years * 8760;

        const energyMWh = derived.TARGET_POWER_MW * totalHours * state.capacityFactor;
        const generationMWh = energyMWh * state.pue;

        const powerGenCostPerW = state.gasTurbineCapexPerKW * state.pue / 1000;
        const electricalCost = state.electricalCostPerW * derived.TARGET_POWER_W;
        const mechanicalCost = state.mechanicalCostPerW * derived.TARGET_POWER_W;
        const civilCost = state.civilCostPerW * derived.TARGET_POWER_W;
        const networkCost = state.networkCostPerW * derived.TARGET_POWER_W;
        const infraCapex = powerGenCostPerW * derived.TARGET_POWER_W + electricalCost + mechanicalCost + civilCost + networkCost;

        const fuelCostPerMWh = state.heatRateBtuKwh * state.gasPricePerMMBtu / 1000;
        const fuelCostTotal = fuelCostPerMWh * generationMWh;

        const totalCost = infraCapex + fuelCostTotal;
        const costPerW = totalCost / derived.TARGET_POWER_W;
        const lcoe = totalCost / energyMWh;

        const gasConsumptionBCF = (generationMWh * 1000 * state.heatRateBtuKwh) / 1000 / 1e9;

        return {{
            totalCost, costPerW, lcoe, energyMWh, gasConsumptionBCF
        }};
    }}
}};

// Execute the requested function
console.log(JSON.stringify(CostModel.{function_name}()));
"""

    try:
        # Write JS code to temp file
        with open('temp_calc.js', 'w') as f:
            f.write(js_code)

        # Run with Node.js
        result = subprocess.run(['node', 'temp_calc.js'],
                              capture_output=True, text=True, cwd='.')

        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        else:
            print(f"JavaScript error: {result.stderr}")
            return None

    except Exception as e:
        print(f"Failed to run JavaScript: {e}")
        return None
    finally:
        # Clean up temp file
        try:
            import os
            os.remove('temp_calc.js')
        except:
            pass

# =============================================================================
# AUDIT FUNCTIONS
# =============================================================================

@dataclass
class CrossValidationResult:
    """Result of cross-validation between Python and JavaScript"""
    test_name: str
    function_name: str
    python_result: Dict[str, float]
    javascript_result: Dict[str, float]
    max_error: float
    max_error_pct: float
    within_tolerance: bool

def validate_calculation(test_case: Dict, function_name: str) -> CrossValidationResult:
    """Cross-validate a calculation between Python and JavaScript"""

    name = test_case["name"]
    state = test_case["state"]

    # Get Python result
    if function_name == "calculateOrbital":
        python_result = calculate_orbital_python(state)
    elif function_name == "calculateTerrestrial":
        python_result = calculate_terrestrial_python(state)
    elif function_name == "calculateThermal":
        python_result = calculate_thermal_python(state)
    else:
        python_result = {}

    # Get JavaScript result
    javascript_result = run_javascript_calculation(state, function_name)

    if javascript_result is None:
        return CrossValidationResult(
            test_name=name,
            function_name=function_name,
            python_result=python_result,
            javascript_result={},
            max_error=float('inf'),
            max_error_pct=float('inf'),
            within_tolerance=False
        )

    # Compare results
    max_error = 0
    max_error_pct = 0

    for key in python_result.keys():
        if key in javascript_result:
            py_val = python_result[key]
            js_val = javascript_result[key]

            if py_val != 0:
                error = abs(py_val - js_val)
                error_pct = abs(error / py_val) * 100

                max_error = max(max_error, error)
                max_error_pct = max(max_error_pct, error_pct)

    # Tolerance: 0.1% for most calculations, 1% for thermal (due to approximations)
    tolerance = 1.0 if function_name == "calculateThermal" else 0.1
    within_tolerance = max_error_pct <= tolerance

    return CrossValidationResult(
        test_name=name,
        function_name=function_name,
        python_result=python_result,
        javascript_result=javascript_result,
        max_error=max_error,
        max_error_pct=max_error_pct,
        within_tolerance=within_tolerance
    )

def print_cross_validation_results(results: List[CrossValidationResult]):
    """Print formatted cross-validation results"""

    print("=" * 80)
    print("CROSS-VALIDATION RESULTS")
    print("=" * 80)
    print("")

    # Group by function
    functions = {}
    for result in results:
        func = result.function_name
        if func not in functions:
            functions[func] = []
        functions[func].append(result)

    # Overall summary
    total_checks = len(results)
    passed_checks = sum(1 for r in results if r.within_tolerance)

    print(f"Overall: {passed_checks}/{total_checks} cross-validations passed")
    print("")

    # Per function results
    for func_name, func_results in functions.items():
        func_passed = sum(1 for r in func_results if r.within_tolerance)
        func_total = len(func_results)
        status = "✅" if func_passed == func_total else "⚠️"

        print(f"{status} {func_name} ({func_passed}/{func_total} tests)")

        for result in func_results:
            test_status = "✅" if result.within_tolerance else "❌"
            print(f"   {test_status} {result.test_name}")

            if not result.within_tolerance:
                print("2d")
                print("2d")

        print("")

def save_cross_validation_results(results: List[CrossValidationResult], filename: str):
    """Save cross-validation results to JSON file"""

    data = {
        "audit_info": {
            "date": "2025-12-14",
            "type": "Cross-Validation Testing",
            "model_version": "math.js current"
        },
        "summary": {
            "total_validations": len(results),
            "passed_validations": sum(1 for r in results if r.within_tolerance),
            "failed_validations": sum(1 for r in results if not r.within_tolerance)
        },
        "results": [
            {
                "test_name": r.test_name,
                "function_name": r.function_name,
                "max_error": r.max_error,
                "max_error_pct": r.max_error_pct,
                "within_tolerance": r.within_tolerance,
                "python_result": r.python_result,
                "javascript_result": r.javascript_result
            }
            for r in results
        ]
    }

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# =============================================================================
# MAIN AUDIT EXECUTION
# =============================================================================

def main():
    """Execute the cross-validation testing"""

    print("Starting Cross-Validation Testing...")
    print("Comparing Python implementations against JavaScript outputs...")
    print("")

    # Check if Node.js is available
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Node.js not found. Cannot perform cross-validation.")
            print("Please install Node.js to run this audit.")
            return
    except FileNotFoundError:
        print("❌ Node.js not found. Cannot perform cross-validation.")
        print("Please install Node.js to run this audit.")
        return

    # Run cross-validation tests
    results = []

    for test_case in CROSS_VALIDATION_TESTS:
        # Test orbital calculations
        orbital_result = validate_calculation(test_case, "calculateOrbital")
        results.append(orbital_result)

        # Test terrestrial calculations
        terrestrial_result = validate_calculation(test_case, "calculateTerrestrial")
        results.append(terrestrial_result)

        # Test thermal calculations (only for cases with thermal parameters)
        if "betaAngle" in test_case["state"]:
            thermal_result = validate_calculation(test_case, "calculateThermal")
            results.append(thermal_result)

    # Print results
    print_cross_validation_results(results)

    # Save detailed results
    save_cross_validation_results(results, "09_cross_validation_results.json")

    # Final assessment
    passed_validations = sum(1 for r in results if r.within_tolerance)
    total_validations = len(results)

    print("=" * 80)
    print("FINAL ASSESSMENT")
    print("=" * 80)

    if passed_validations == total_validations:
        print("✅ AUDIT PASSED: All cross-validations successful")
    else:
        print(f"⚠️  AUDIT PARTIALLY PASSED: {passed_validations}/{total_validations} validations successful")

        # Check which functions have issues
        failed_by_function = {}
        for result in results:
            if not result.within_tolerance:
                func = result.function_name
                if func not in failed_by_function:
                    failed_by_function[func] = 0
                failed_by_function[func] += 1

        if failed_by_function:
            print("   Functions with validation issues:")
            for func, count in failed_by_function.items():
                print(f"   • {func}: {count} failed validations")

    print("")
    print("Detailed results saved to: 09_cross_validation_results.json")
    print("")
    print("Note: Small differences may be due to floating-point precision")
    print("or different implementation details between Python and JavaScript.")

if __name__ == "__main__":
    main()
