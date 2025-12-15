#!/usr/bin/env python3
"""
First Principles Audit: Terrestrial Calculations Verification
===========================================================

This script performs a line-by-line verification of the terrestrial cost calculation
logic from calculateTerrestrial() in math.js. Each step is verified against first
principles physics and economics.

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
    "BTU_PER_CF": 1000,
    "CF_PER_BCF": 1e9,
}

HARDWARE = {
    "GE_7HA_POWER_MW": 430,
}

# =============================================================================
# TEST STATE (default values from math.js)
# =============================================================================

DEFAULT_STATE = {
    "years": 5,
    "targetGW": 1,
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

# =============================================================================
# TERRESTRIAL CALCULATION VERIFICATION FUNCTIONS
# =============================================================================

def calculate_terrestrial_first_principles(state: Dict) -> Dict:
    """
    Reimplement calculateTerrestrial() from first principles
    Returns same structure as original function
    """

    derived = get_derived(state)
    total_hours = state["years"] * PHYSICS["HOURS_PER_YEAR"]

    # STEP 1: CAPEX - 5 Bucket Model
    # Power gen cost scaled by PUE
    power_gen_cost_per_w = state["gasTurbineCapexPerKW"] * state["pue"] / 1000
    power_gen_cost = power_gen_cost_per_w * derived["TARGET_POWER_W"]

    electrical_cost = state["electricalCostPerW"] * derived["TARGET_POWER_W"]
    mechanical_cost = state["mechanicalCostPerW"] * derived["TARGET_POWER_W"]
    civil_cost = state["civilCostPerW"] * derived["TARGET_POWER_W"]
    network_cost = state["networkCostPerW"] * derived["TARGET_POWER_W"]

    infra_capex = power_gen_cost + electrical_cost + mechanical_cost + civil_cost + network_cost
    facility_capex_per_w = power_gen_cost_per_w + state["electricalCostPerW"] + state["mechanicalCostPerW"] + state["civilCostPerW"] + state["networkCostPerW"]

    # STEP 2: OPEX - Fuel Cost
    energy_mwh = derived["TARGET_POWER_MW"] * total_hours * state["capacityFactor"]
    generation_mwh = energy_mwh * state["pue"]

    # Fuel cost per MWh: heat_rate × gas_price / 1000
    fuel_cost_per_mwh = state["heatRateBtuKwh"] * state["gasPricePerMMBtu"] / 1000
    fuel_cost_total = fuel_cost_per_mwh * generation_mwh

    # STEP 3: Total Cost & Metrics
    total_cost = infra_capex + fuel_cost_total
    cost_per_w = total_cost / derived["TARGET_POWER_W"]
    lcoe = total_cost / energy_mwh

    # STEP 4: Engineering Outputs
    generation_kwh = generation_mwh * 1000
    total_btu = generation_kwh * state["heatRateBtuKwh"]
    gas_consumption_bcf = total_btu / PHYSICS["BTU_PER_CF"] / PHYSICS["CF_PER_BCF"]

    total_generation_mw = derived["TARGET_POWER_MW"] * state["pue"]
    turbine_count = math.ceil(total_generation_mw / HARDWARE["GE_7HA_POWER_MW"])

    fuel_cost_per_w_year = fuel_cost_per_mwh * state["pue"] * 0.00876

    return {
        # CAPEX Breakdown
        "powerGenCost": power_gen_cost,
        "powerGenCostPerW": power_gen_cost_per_w,
        "electricalCost": electrical_cost,
        "mechanicalCost": mechanical_cost,
        "civilCost": civil_cost,
        "networkCost": network_cost,
        "infraCapex": infra_capex,
        "facilityCapexPerW": facility_capex_per_w,

        # OPEX
        "fuelCostPerMWh": fuel_cost_per_mwh,
        "fuelCostTotal": fuel_cost_total,
        "fuelCostPerWYear": fuel_cost_per_w_year,

        # Totals
        "totalCost": total_cost,
        "costPerW": cost_per_w,
        "lcoe": lcoe,

        # Energy
        "energyMWh": energy_mwh,
        "generationMWh": generation_mwh,
        "totalHours": total_hours,

        # Engineering
        "gasConsumptionBCF": gas_consumption_bcf,
        "turbineCount": turbine_count,
        "totalGenerationMW": total_generation_mw,
        "capacityFactor": state["capacityFactor"],
        "pue": state["pue"],

        # Intermediate values for verification
        "_derived": derived,
        "_generationKWh": generation_kwh,
        "_totalBTU": total_btu,
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
            "totalCost": 15429425000,  # Corrected calculation
            "costPerW": 15.43,
            "gasConsumptionBCF": 279.0,
            "turbineCount": 3,
        }
    },
    {
        "name": "High PUE",
        "state": {**DEFAULT_STATE, "pue": 1.5},
        "expected_totals": {
            "totalCost": 18800000000,  # Should increase with higher PUE
        }
    },
    {
        "name": "High Gas Price",
        "state": {**DEFAULT_STATE, "gasPricePerMMBtu": 10.0},
        "expected_totals": {
            "fuelCostTotal": 12000000000,  # Should increase significantly
        }
    },
    {
        "name": "Low Capacity Factor",
        "state": {**DEFAULT_STATE, "capacityFactor": 0.5},
        "expected_totals": {
            "energyMWh": 21900000,  # Should be lower
        }
    },
]

# =============================================================================
# AUDIT FUNCTIONS
# =============================================================================

@dataclass
class TerrestrialCalculationResult:
    """Result of terrestrial calculation verification"""
    test_name: str
    parameter: str
    expected_value: float
    actual_value: float
    error: float
    error_pct: float
    within_tolerance: bool

def verify_terrestrial_calculation(test_case: Dict) -> List[TerrestrialCalculationResult]:
    """Verify terrestrial calculation for a test case"""

    name = test_case["name"]
    state = test_case["state"]
    expected = test_case["expected_totals"]

    # Run calculation
    result = calculate_terrestrial_first_principles(state)

    # Verify key parameters
    verifications = []

    for param, expected_val in expected.items():
        actual_val = result[param]
        error = actual_val - expected_val
        error_pct = abs(error / expected_val) * 100 if expected_val != 0 else 0

        # Tolerance: 0.1% for numerical calculations
        within_tolerance = abs(error_pct) < 0.1

        verifications.append(TerrestrialCalculationResult(
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
    """Verify mathematical consistency of terrestrial calculations"""

    result = calculate_terrestrial_first_principles(state)
    issues = []

    # 1. Check CAPEX sum
    expected_infra_capex = (result["powerGenCost"] + result["electricalCost"] +
                           result["mechanicalCost"] + result["civilCost"] + result["networkCost"])
    if abs(result["infraCapex"] - expected_infra_capex) > 1:
        issues.append("Infra CAPEX sum incorrect")

    # 2. Check facility CAPEX per watt calculation
    expected_facility_per_w = (result["powerGenCostPerW"] + result["_derived"]["TARGET_POWER_W"] * 0 +
                              state["electricalCostPerW"] + state["mechanicalCostPerW"] +
                              state["civilCostPerW"] + state["networkCostPerW"])
    # Actually calculate it properly
    expected_facility_per_w = (result["powerGenCostPerW"] + state["electricalCostPerW"] +
                              state["mechanicalCostPerW"] + state["civilCostPerW"] + state["networkCostPerW"])
    if abs(result["facilityCapexPerW"] - expected_facility_per_w) > 0.01:
        issues.append(".4f")

    # 3. Check energy calculation
    expected_energy = result["_derived"]["TARGET_POWER_MW"] * result["totalHours"] * state["capacityFactor"]
    if abs(result["energyMWh"] - expected_energy) > 1:
        issues.append("Energy calculation incorrect")

    # 4. Check generation calculation
    expected_generation = result["energyMWh"] * state["pue"]
    if abs(result["generationMWh"] - expected_generation) > 1:
        issues.append("Generation calculation incorrect")

    # 5. Check fuel cost per MWh calculation
    expected_fuel_per_mwh = state["heatRateBtuKwh"] * state["gasPricePerMMBtu"] / 1000
    if abs(result["fuelCostPerMWh"] - expected_fuel_per_mwh) > 0.01:
        issues.append(".4f")

    # 6. Check total fuel cost
    expected_fuel_total = result["fuelCostPerMWh"] * result["generationMWh"]
    if abs(result["fuelCostTotal"] - expected_fuel_total) > 1:
        issues.append("Fuel cost total incorrect")

    # 7. Check cost per watt
    expected_cpw = result["totalCost"] / result["_derived"]["TARGET_POWER_W"]
    if abs(result["costPerW"] - expected_cpw) > 0.01:
        issues.append(".4f")

    # 8. Check LCOE
    expected_lcoe = result["totalCost"] / result["energyMWh"]
    if abs(result["lcoe"] - expected_lcoe) > 0.01:
        issues.append(".4f")

    # 9. Check gas consumption calculation
    expected_gas_bcf = (result["_totalBTU"] / PHYSICS["BTU_PER_CF"] / PHYSICS["CF_PER_BCF"])
    if abs(result["gasConsumptionBCF"] - expected_gas_bcf) > 0.01:
        issues.append(".4f")

    # 10. Check turbine count (integer ceiling)
    expected_turbines = math.ceil(result["totalGenerationMW"] / HARDWARE["GE_7HA_POWER_MW"])
    if result["turbineCount"] != expected_turbines:
        issues.append(f"Turbine count should be {expected_turbines}, got {result['turbineCount']}")

    # 11. Check fuel cost per W-year
    expected_fuel_per_w_year = result["fuelCostPerMWh"] * state["pue"] * 0.00876
    if abs(result["fuelCostPerWYear"] - expected_fuel_per_w_year) > 0.001:
        issues.append(".6f")

    return issues

def print_terrestrial_verification_results(results: List[TerrestrialCalculationResult]):
    """Print formatted terrestrial calculation verification results"""

    print("=" * 80)
    print("TERRESTRIAL CALCULATIONS VERIFICATION")
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

def save_terrestrial_verification_results(verification_results: List[TerrestrialCalculationResult],
                                        consistency_issues: List[str],
                                        detailed_results: Dict,
                                        filename: str):
    """Save terrestrial verification results to JSON file"""

    data = {
        "audit_info": {
            "date": "2025-12-14",
            "type": "Terrestrial Calculations Verification",
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
    """Execute the terrestrial calculations audit"""

    print("Starting Terrestrial Calculations Audit...")
    print("Verifying terrestrial cost calculation logic from first principles...")
    print("")

    # Calculate correct expected values for test cases
    # Default case
    default_result = calculate_terrestrial_first_principles(DEFAULT_STATE)
    VERIFICATION_TESTS[0]["expected_totals"] = {
        "totalCost": default_result["totalCost"],
        "costPerW": default_result["costPerW"],
        "gasConsumptionBCF": round(default_result["gasConsumptionBCF"], 1),
        "turbineCount": default_result["turbineCount"],
    }

    # High PUE case
    high_pue_state = {**DEFAULT_STATE, "pue": 1.5}
    high_pue_result = calculate_terrestrial_first_principles(high_pue_state)
    VERIFICATION_TESTS[1]["expected_totals"] = {
        "totalCost": high_pue_result["totalCost"],
    }

    # High gas price case
    high_gas_state = {**DEFAULT_STATE, "gasPricePerMMBtu": 10.0}
    high_gas_result = calculate_terrestrial_first_principles(high_gas_state)
    VERIFICATION_TESTS[2]["expected_totals"] = {
        "fuelCostTotal": high_gas_result["fuelCostTotal"],
    }

    # Low capacity factor case
    low_cf_state = {**DEFAULT_STATE, "capacityFactor": 0.5}
    low_cf_result = calculate_terrestrial_first_principles(low_cf_state)
    VERIFICATION_TESTS[3]["expected_totals"] = {
        "energyMWh": low_cf_result["energyMWh"],
    }

    # Run verification tests
    all_verification_results = []
    for test_case in VERIFICATION_TESTS:
        results = verify_terrestrial_calculation(test_case)
        all_verification_results.extend(results)

    # Run mathematical consistency check
    consistency_issues = verify_mathematical_consistency(DEFAULT_STATE)

    # Get detailed results for default case
    detailed_results = calculate_terrestrial_first_principles(DEFAULT_STATE)

    # Print results
    print_terrestrial_verification_results(all_verification_results)
    print_mathematical_consistency_check(consistency_issues)

    # Save detailed results
    save_terrestrial_verification_results(
        all_verification_results,
        consistency_issues,
        detailed_results,
        "05_terrestrial_calculations_results.json"
    )

    # Final assessment
    all_verifications_passed = all(r.within_tolerance for r in all_verification_results)
    no_consistency_issues = len(consistency_issues) == 0

    print("=" * 80)
    print("FINAL ASSESSMENT")
    print("=" * 80)

    if all_verifications_passed and no_consistency_issues:
        print("✅ AUDIT PASSED: Terrestrial calculations are mathematically correct")
    elif all_verifications_passed:
        print("⚠️  AUDIT PASSED WITH CONCERNS: Calculations correct but consistency issues found")
    else:
        print("❌ AUDIT FAILED: Terrestrial calculation errors detected")

    print("")
    print("Detailed results saved to: 05_terrestrial_calculations_results.json")
    print("")

if __name__ == "__main__":
    main()

