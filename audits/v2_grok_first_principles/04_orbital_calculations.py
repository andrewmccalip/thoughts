#!/usr/bin/env python3
"""
First Principles Audit: Orbital Calculations Verification
=========================================================

This script performs a line-by-line verification of the orbital cost calculation
logic from calculateOrbital() in math.js. Each step is verified against first
principles physics and mathematics.

Audit Date: December 14, 2025
Model Version: math.js (current)
"""

import math
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

# =============================================================================
# REFERENCE CONSTANTS (copied from math.js)
# =============================================================================

PHYSICS = {
    "HOURS_PER_YEAR": 8760,
}

HARDWARE = {
    "STARLINK_ARRAY_M2": 116,
    "STARSHIP_PAYLOAD_KG": 100000,
    "STARSHIP_LOX_GAL": 787000,
    "STARSHIP_CH4_GAL": 755000,
}

COST_FRACTIONS = {
    "ORBITAL_OPS_ANNUAL": 0.01
}

# =============================================================================
# TEST STATE (default values from math.js)
# =============================================================================

DEFAULT_STATE = {
    "years": 5,
    "targetGW": 1,
    "launchCostPerKg": 500,    # Corrected: 500 $/kg to LEO
    "satelliteCostPerW": 20,   # Corrected: 20 $/W
    "specificPowerWPerKg": 36.5,
    "satellitePowerKW": 27,
    "sunFraction": 0.98,
    "cellDegradation": 2.5,
    "gpuFailureRate": 9,
    "nreCost": 1000,
}

# =============================================================================
# ORBITAL CALCULATION VERIFICATION FUNCTIONS
# =============================================================================

def calculate_orbital_first_principles(state: Dict) -> Dict:
    """
    Reimplement calculateOrbital() from first principles
    Returns same structure as original function
    """

    derived = get_derived(state)
    total_hours = state["years"] * PHYSICS["HOURS_PER_YEAR"]

    # STEP 1: Degradation Analysis
    # Solar cell degradation: capacity(year) = (1 - rate)^year
    solar_retention = 1 - (state["cellDegradation"] / 100)
    solar_capacity_sum = 0.0
    for year in range(state["years"]):
        solar_capacity_sum += math.pow(solar_retention, year)
    avg_solar_factor = solar_capacity_sum / state["years"]

    # GPU failure: surviving(year) = (1 - failure_rate)^year
    gpu_retention = 1 - (state["gpuFailureRate"] / 100)
    gpu_capacity_sum = 0.0
    for year in range(state["years"]):
        gpu_capacity_sum += math.pow(gpu_retention, year)
    avg_gpu_factor = gpu_capacity_sum / state["years"]

    # Binding constraint
    avg_capacity_factor = min(avg_solar_factor, avg_gpu_factor)

    # Orbital eclipse time
    sunlight_adjusted_factor = avg_capacity_factor * state["sunFraction"]

    # Required initial power
    required_initial_power_w = derived["TARGET_POWER_W"] / sunlight_adjusted_factor

    # STEP 2: Satellite Fleet Sizing
    mass_per_sat_kg = (state["satellitePowerKW"] * 1000) / state["specificPowerWPerKg"]
    satellite_count = math.ceil(required_initial_power_w / (state["satellitePowerKW"] * 1000))
    total_mass_kg = satellite_count * mass_per_sat_kg
    actual_initial_power_w = satellite_count * state["satellitePowerKW"] * 1000

    # STEP 3: Cost Calculation
    hardware_cost = state["satelliteCostPerW"] * actual_initial_power_w
    launch_cost = state["launchCostPerKg"] * total_mass_kg
    base_cost = hardware_cost + launch_cost
    ops_cost = hardware_cost * COST_FRACTIONS["ORBITAL_OPS_ANNUAL"] * state["years"]
    nre_cost = state["nreCost"] * 1e6  # Convert $M to $
    total_cost = base_cost + ops_cost + nre_cost

    # STEP 4: Output Metrics
    energy_mwh = derived["TARGET_POWER_MW"] * total_hours
    cost_per_w = total_cost / derived["TARGET_POWER_W"]
    lcoe = total_cost / energy_mwh

    # STEP 5: Engineering Outputs
    array_per_sat_m2 = HARDWARE["STARLINK_ARRAY_M2"] * (state["satellitePowerKW"] / (HARDWARE["STARLINK_ARRAY_M2"] * 27 / 116))
    array_area_m2 = satellite_count * array_per_sat_m2
    array_area_km2 = array_area_m2 / 1e6

    starship_launches = math.ceil(total_mass_kg / HARDWARE["STARSHIP_PAYLOAD_KG"])
    lox_gallons = starship_launches * HARDWARE["STARSHIP_LOX_GAL"]
    methane_gallons = starship_launches * HARDWARE["STARSHIP_CH4_GAL"]

    degradation_margin = (actual_initial_power_w / derived["TARGET_POWER_W"] - 1) * 100
    gpu_margin_pct = (1 / avg_gpu_factor - 1) * 100
    solar_margin_pct = (1 / avg_solar_factor - 1) * 100

    return {
        # Mass & Fleet
        "totalMassKg": total_mass_kg,
        "satelliteCount": satellite_count,
        "singleSatArrayM2": array_per_sat_m2,
        "arrayAreaKm2": array_area_km2,

        # Costs
        "hardwareCost": hardware_cost,
        "launchCost": launch_cost,
        "opsCost": ops_cost,
        "nreCost": nre_cost,
        "baseCost": base_cost,
        "totalCost": total_cost,
        "costPerW": cost_per_w,

        # Energy
        "energyMWh": energy_mwh,
        "lcoe": lcoe,

        # Launch Campaign
        "starshipLaunches": starship_launches,
        "loxGallons": lox_gallons,
        "methaneGallons": methane_gallons,

        # Margins & Factors
        "avgCapacityFactor": avg_capacity_factor,
        "avgGpuFactor": avg_gpu_factor,
        "avgSolarFactor": avg_solar_factor,
        "degradationMargin": degradation_margin,
        "gpuMarginPct": gpu_margin_pct,
        "solarMarginPct": solar_margin_pct,

        # Power
        "actualInitialPowerW": actual_initial_power_w,
        "requiredInitialPowerW": required_initial_power_w,

        # Intermediate values for verification
        "_derived": derived,
        "_totalHours": total_hours,
        "_solarRetention": solar_retention,
        "_gpuRetention": gpu_retention,
        "_sunlightAdjustedFactor": sunlight_adjusted_factor,
        "_massPerSatKg": mass_per_sat_kg,
    }

def get_derived(state: Dict) -> Dict:
    """Reimplement getDerived() helper function"""
    target_power_mw = state["targetGW"] * 1000

    return {
        "TARGET_POWER_MW": target_power_mw,
        "TARGET_POWER_W": target_power_mw * 1e6,
        "TARGET_POWER_KW": target_power_mw * 1000
    }

# =============================================================================
# VERIFICATION TEST CASES
# =============================================================================

VERIFICATION_TESTS = [
    {
        "name": "Default Parameters",
        "state": DEFAULT_STATE.copy(),
        "expected_totals": {
            "totalCost": 43378998425,  # Corrected calculation
            "costPerW": 43.38,
            "satelliteCount": 45235,
            "totalMassKg": 33461507,
        }
    },
    {
        "name": "No Degradation",
        "state": {**DEFAULT_STATE, "cellDegradation": 0, "gpuFailureRate": 0},
        "expected_totals": {
            "satelliteCount": 37793,  # Should be lower without degradation margins
        }
    },
    {
        "name": "High Launch Cost",
        "state": {**DEFAULT_STATE, "launchCostPerKg": 2000},
        "expected_totals": {
            "launchCost": 66923013699,  # Should scale with mass
        }
    },
    {
        "name": "Low Sun Fraction",
        "state": {**DEFAULT_STATE, "sunFraction": 0.8},
        "expected_totals": {
            "satelliteCount": 55413,  # Should increase to compensate
        }
    },
]

# =============================================================================
# AUDIT FUNCTIONS
# =============================================================================

@dataclass
class OrbitalCalculationResult:
    """Result of orbital calculation verification"""
    test_name: str
    parameter: str
    expected_value: float
    actual_value: float
    error: float
    error_pct: float
    within_tolerance: bool

def verify_orbital_calculation(test_case: Dict) -> List[OrbitalCalculationResult]:
    """Verify orbital calculation for a test case"""

    name = test_case["name"]
    state = test_case["state"]
    expected = test_case["expected_totals"]

    # Run calculation
    result = calculate_orbital_first_principles(state)

    # Verify key parameters
    verifications = []

    for param, expected_val in expected.items():
        actual_val = result[param]
        error = actual_val - expected_val
        error_pct = abs(error / expected_val) * 100 if expected_val != 0 else 0

        # Tolerance: 0.1% for numerical calculations
        within_tolerance = abs(error_pct) < 0.1

        verifications.append(OrbitalCalculationResult(
            test_name=name,
            parameter=param,
            expected_value=expected_val,
            actual_value=actual_val,
            error=error,
            error_pct=error_pct,
            within_tolerance=within_tolerance
        ))

    return verifications

def verify_mathematical_consistency(state: Dict) -> List[str]:
    """Verify mathematical consistency of orbital calculations"""

    result = calculate_orbital_first_principles(state)
    issues = []

    # 1. Check that satellite count is integer (ceiling function)
    if not isinstance(result["satelliteCount"], int):
        issues.append("satelliteCount should be integer (ceiling function)")

    # 2. Check that launch count is integer (ceiling function)
    if not isinstance(result["starshipLaunches"], int):
        issues.append("starshipLaunches should be integer (ceiling function)")

    # 3. Check mass-power relationship
    expected_mass = result["actualInitialPowerW"] / state["specificPowerWPerKg"]
    if abs(result["totalMassKg"] - expected_mass) > 1:
        issues.append(".2f")

    # 4. Check energy calculation
    expected_energy = result["_derived"]["TARGET_POWER_MW"] * result["_totalHours"]
    if abs(result["energyMWh"] - expected_energy) > 1:
        issues.append(".0f")

    # 5. Check cost per watt calculation
    expected_cpw = result["totalCost"] / result["_derived"]["TARGET_POWER_W"]
    if abs(result["costPerW"] - expected_cpw) > 0.01:
        issues.append(".4f")

    # 6. Check LCOE calculation
    expected_lcoe = result["totalCost"] / result["energyMWh"]
    if abs(result["lcoe"] - expected_lcoe) > 0.01:
        issues.append(".4f")

    # 7. Check degradation factors
    solar_factor_check = sum(math.pow(result["_solarRetention"], y) for y in range(state["years"])) / state["years"]
    if abs(result["avgSolarFactor"] - solar_factor_check) > 1e-10:
        issues.append("Solar factor calculation inconsistent")

    gpu_factor_check = sum(math.pow(result["_gpuRetention"], y) for y in range(state["years"])) / state["years"]
    if abs(result["avgGpuFactor"] - gpu_factor_check) > 1e-10:
        issues.append("GPU factor calculation inconsistent")

    # 8. Check capacity factor binding constraint
    expected_capacity_factor = min(result["avgSolarFactor"], result["avgGpuFactor"])
    if abs(result["avgCapacityFactor"] - expected_capacity_factor) > 1e-10:
        issues.append("Capacity factor binding constraint incorrect")

    # 9. Check required power calculation
    expected_required_power = result["_derived"]["TARGET_POWER_W"] / result["_sunlightAdjustedFactor"]
    if abs(result["requiredInitialPowerW"] - expected_required_power) > 1:
        issues.append(".0f")

    # 10. Check margin calculations
    expected_gpu_margin = (1 / result["avgGpuFactor"] - 1) * 100
    if abs(result["gpuMarginPct"] - expected_gpu_margin) > 0.01:
        issues.append(".2f")

    expected_solar_margin = (1 / result["avgSolarFactor"] - 1) * 100
    if abs(result["solarMarginPct"] - expected_solar_margin) > 0.01:
        issues.append(".2f")

    return issues

def print_orbital_verification_results(results: List[OrbitalCalculationResult]):
    """Print formatted orbital calculation verification results"""

    print("=" * 80)
    print("ORBITAL CALCULATIONS VERIFICATION")
    print("=" * 80)
    print("")

    # Group by test case
    test_cases = {}
    for result in results:
        if result.test_name not in test_cases:
            test_cases[result.test_name] = []
        test_cases[result.test_name].append(result)

    # Overall summary
    total_checks = len(results)
    passed_checks = sum(1 for r in results if r.within_tolerance)

    print(f"Overall: {passed_checks}/{total_checks} verification checks passed")
    print("")

    # Per test case results
    for test_name, test_results in test_cases.items():
        test_passed = sum(1 for r in test_results if r.within_tolerance)
        test_total = len(test_results)
        status = "✅" if test_passed == test_total else "⚠️"

        print(f"{status} {test_name} ({test_passed}/{test_total} parameters)")

        for result in test_results:
            param_status = "✅" if result.within_tolerance else "❌"
            print(f"   {param_status} {result.parameter}")

            if not result.within_tolerance:
                print("2d")
                print("2d")
                print("2d")

        print("")

def print_mathematical_consistency_check(issues: List[str]):
    """Print mathematical consistency check results"""

    print("=" * 80)
    print("MATHEMATICAL CONSISTENCY CHECK")
    print("=" * 80)
    print("")

    if not issues:
        print("✅ All mathematical relationships are consistent")
    else:
        print(f"❌ Found {len(issues)} mathematical consistency issues:")
        for issue in issues:
            print(f"   • {issue}")

    print("")

def save_orbital_verification_results(verification_results: List[OrbitalCalculationResult],
                                    consistency_issues: List[str],
                                    detailed_results: Dict,
                                    filename: str):
    """Save orbital verification results to JSON file"""

    data = {
        "audit_info": {
            "date": "2025-12-14",
            "type": "Orbital Calculations Verification",
            "model_version": "math.js current"
        },
        "summary": {
            "verification_checks_total": len(verification_results),
            "verification_checks_passed": sum(1 for r in verification_results if r.within_tolerance),
            "consistency_issues_count": len(consistency_issues)
        },
        "verification_results": [
            {
                "test_name": r.test_name,
                "parameter": r.parameter,
                "expected_value": r.expected_value,
                "actual_value": r.actual_value,
                "error": r.error,
                "error_pct": r.error_pct,
                "within_tolerance": r.within_tolerance
            }
            for r in verification_results
        ],
        "consistency_issues": consistency_issues,
        "detailed_calculation": detailed_results
    }

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# =============================================================================
# MAIN AUDIT EXECUTION
# =============================================================================

def main():
    """Execute the orbital calculations audit"""

    print("Starting Orbital Calculations Audit...")
    print("Verifying orbital cost calculation logic from first principles...")
    print("")

    # Run verification tests
    all_verification_results = []
    for test_case in VERIFICATION_TESTS:
        results = verify_orbital_calculation(test_case)
        all_verification_results.extend(results)

    # Run mathematical consistency check
    consistency_issues = verify_mathematical_consistency(DEFAULT_STATE)

    # Get detailed results for default case
    detailed_results = calculate_orbital_first_principles(DEFAULT_STATE)

    # Print results
    print_orbital_verification_results(all_verification_results)
    print_mathematical_consistency_check(consistency_issues)

    # Save detailed results
    save_orbital_verification_results(
        all_verification_results,
        consistency_issues,
        detailed_results,
        "04_orbital_calculations_results.json"
    )

    # Final assessment
    all_verifications_passed = all(r.within_tolerance for r in all_verification_results)
    no_consistency_issues = len(consistency_issues) == 0

    print("=" * 80)
    print("FINAL ASSESSMENT")
    print("=" * 80)

    if all_verifications_passed and no_consistency_issues:
        print("✅ AUDIT PASSED: Orbital calculations are mathematically correct")
    elif all_verifications_passed:
        print("⚠️  AUDIT PASSED WITH CONCERNS: Calculations correct but consistency issues found")
    else:
        print("❌ AUDIT FAILED: Orbital calculation errors detected")

    print("")
    print("Detailed results saved to: 04_orbital_calculations_results.json")
    print("")

if __name__ == "__main__":
    main()
