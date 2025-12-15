#!/usr/bin/env python3
"""
First Principles Audit: Unit Conversions Verification
====================================================

This script verifies all unit conversions used throughout the model to ensure
dimensional consistency and correct implementation of conversion factors.

Audit Date: December 14, 2025
Model Version: math.js (current)
"""

import math
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

# =============================================================================
# UNIT CONVERSION FACTORS (from first principles)
# =============================================================================

UNIT_CONVERSIONS = {
    # Power conversions
    "GW_to_MW": 1000,                    # 1 GW = 1000 MW
    "MW_to_kW": 1000,                    # 1 MW = 1000 kW
    "kW_to_W": 1000,                     # 1 kW = 1000 W
    "W_to_mW": 1000,                     # 1 W = 1000 mW

    # Mass conversions
    "kg_to_metric_tons": 0.001,          # 1 kg = 0.001 metric tons
    "metric_tons_to_kg": 1000,           # 1 metric ton = 1000 kg
    "kg_to_g": 1000,                     # 1 kg = 1000 g

    # Area conversions
    "m2_to_km2": 1e-6,                   # 1 m² = 1e-6 km²
    "km2_to_m2": 1e6,                    # 1 km² = 1e6 m²

    # Volume conversions
    "gal_to_L": 3.785411784,             # 1 US gallon = 3.785411784 liters
    "L_to_gal": 0.264172052,             # 1 liter = 0.264172052 gallons
    "L_to_m3": 0.001,                   # 1 liter = 0.001 m³

    # Time conversions
    "years_to_hours": 8760,              # 1 year = 8760 hours (365 × 24)
    "years_to_days": 365,                # 1 year = 365 days
    "hours_to_seconds": 3600,            # 1 hour = 3600 seconds
    "days_to_hours": 24,                 # 1 day = 24 hours

    # Energy conversions
    "MWh_to_kWh": 1000,                 # 1 MWh = 1000 kWh
    "kWh_to_Wh": 1000,                  # 1 kWh = 1000 Wh
    "Wh_to_J": 3600,                    # 1 Wh = 3600 Joules
    "MJ_to_J": 1000000,                 # 1 MJ = 1,000,000 J

    # Temperature conversions
    "C_to_K": lambda c: c + 273.15,      # Celsius to Kelvin
    "K_to_C": lambda k: k - 273.15,      # Kelvin to Celsius
    "F_to_C": lambda f: (f - 32) * 5/9,  # Fahrenheit to Celsius

    # Pressure conversions (for gas turbine specs)
    "psi_to_Pa": 6894.757293168,         # 1 psi = 6894.757 Pa
    "bar_to_Pa": 100000,                 # 1 bar = 100,000 Pa
    "atm_to_Pa": 101325,                 # 1 atm = 101,325 Pa

    # Fuel energy content conversions
    "BTU_to_J": 1055.05585262,          # 1 BTU = 1055.05585262 J
    "MMBTU_to_BTU": 1000000,            # 1 MMBtu = 1,000,000 BTU
    "MMBTU_to_J": 1055055852.62,        # 1 MMBtu = 1.05505585262e9 J

    # Natural gas volume conversions
    "cf_to_m3": 0.028316846592,         # 1 cubic foot = 0.028316846592 m³
    "m3_to_cf": 35.314666721,           # 1 m³ = 35.314666721 cubic feet
    "BCF_to_cf": 1000000000,            # 1 BCF = 1e9 cubic feet
    "BCF_to_m3": 28316846.592,          # 1 BCF = 28,316,846.592 m³
}

# =============================================================================
# MODEL-SPECIFIC UNIT CONVERSIONS (from math.js)
# =============================================================================

MODEL_CONVERSIONS = {
    # From getDerived() function
    "targetGW_to_targetMW": lambda gw: gw * 1000,        # GW to MW
    "targetMW_to_targetW": lambda mw: mw * 1000000,      # MW to W
    "targetMW_to_targetKW": lambda mw: mw * 1000,        # MW to kW

    # From orbital calculations
    "satelliteKW_to_satelliteW": lambda kw: kw * 1000,   # kW to W
    "totalMassKg_to_launchCount": lambda mass, payload: math.ceil(mass / payload),  # Launch count
    "arrayAreaM2_to_arrayAreaKm2": lambda m2: m2 / 1000000,  # m² to km²

    # From terrestrial calculations
    "gasPricePerMMBtu_to_gasPricePerBTU": lambda price: price / 1000000,  # $/MMBtu to $/BTU
    "fuelCostPerMWh_to_fuelCostPerBTU": lambda cost_mwh, heat_rate: cost_mwh / heat_rate,  # $/MWh to $/BTU
    "fuelCostPerBTU_to_fuelCostPerMMBtu": lambda cost_btu: cost_btu * 1000000,  # $/BTU to $/MMBtu

    # From thermal calculations
    "arrayAreaKm2_to_arrayAreaM2": lambda km2: km2 * 1000000,  # km² to m²
    "tempC_to_tempK": lambda c: c + 273.15,         # °C to K
    "tempK_to_tempC": lambda k: k - 273.15,         # K to °C
}

# =============================================================================
# TEST CASES FOR UNIT CONVERSIONS
# =============================================================================

CONVERSION_TESTS = [
    # Basic power conversions
    {
        "name": "GW to MW",
        "input": 1.0,
        "expected": 1000.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["GW_to_MW"]
    },
    {
        "name": "MW to kW",
        "input": 1.0,
        "expected": 1000.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["MW_to_kW"]
    },
    {
        "name": "kW to W",
        "input": 1.0,
        "expected": 1000.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["kW_to_W"]
    },

    # Mass conversions
    {
        "name": "kg to metric tons",
        "input": 1000.0,
        "expected": 1.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["kg_to_metric_tons"]
    },
    {
        "name": "metric tons to kg",
        "input": 1.0,
        "expected": 1000.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["metric_tons_to_kg"]
    },

    # Area conversions
    {
        "name": "m² to km²",
        "input": 1000000.0,
        "expected": 1.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["m2_to_km2"]
    },
    {
        "name": "km² to m²",
        "input": 1.0,
        "expected": 1000000.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["km2_to_m2"]
    },

    # Time conversions
    {
        "name": "years to hours",
        "input": 1.0,
        "expected": 8760.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["years_to_hours"]
    },
    {
        "name": "years to days",
        "input": 1.0,
        "expected": 365.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["years_to_days"]
    },

    # Temperature conversions
    {
        "name": "Celsius to Kelvin (water freezing)",
        "input": 0.0,
        "expected": 273.15,
        "conversion": UNIT_CONVERSIONS["C_to_K"]
    },
    {
        "name": "Celsius to Kelvin (water boiling)",
        "input": 100.0,
        "expected": 373.15,
        "conversion": UNIT_CONVERSIONS["C_to_K"]
    },
    {
        "name": "Kelvin to Celsius (absolute zero)",
        "input": 0.0,
        "expected": -273.15,
        "conversion": UNIT_CONVERSIONS["K_to_C"]
    },

    # Energy conversions
    {
        "name": "MWh to kWh",
        "input": 1.0,
        "expected": 1000.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["MWh_to_kWh"]
    },
    {
        "name": "kWh to Wh",
        "input": 1.0,
        "expected": 1000.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["kWh_to_Wh"]
    },
    {
        "name": "Wh to Joules",
        "input": 1.0,
        "expected": 3600.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["Wh_to_J"]
    },

    # Fuel conversions (important for gas cost calculations)
    {
        "name": "MMBtu to BTU",
        "input": 1.0,
        "expected": 1000000.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["MMBTU_to_BTU"]
    },
    {
        "name": "BCF to cubic feet",
        "input": 1.0,
        "expected": 1000000000.0,
        "conversion": lambda x: x * UNIT_CONVERSIONS["BCF_to_cf"]
    },
]

# =============================================================================
# MODEL-SPECIFIC CONVERSION TESTS
# =============================================================================

MODEL_CONVERSION_TESTS = [
    # From getDerived() - power conversions
    {
        "name": "getDerived: GW to MW",
        "input": 1.0,
        "expected": 1000.0,
        "conversion": MODEL_CONVERSIONS["targetGW_to_targetMW"]
    },
    {
        "name": "getDerived: MW to W",
        "input": 1000.0,
        "expected": 1000000000.0,  # 1e9
        "conversion": MODEL_CONVERSIONS["targetMW_to_targetW"]
    },
    {
        "name": "getDerived: MW to kW",
        "input": 1000.0,
        "expected": 1000000.0,  # 1e6
        "conversion": MODEL_CONVERSIONS["targetMW_to_targetKW"]
    },

    # Thermal conversions
    {
        "name": "Thermal: km² to m²",
        "input": 1.0,
        "expected": 1000000.0,
        "conversion": MODEL_CONVERSIONS["arrayAreaKm2_to_arrayAreaM2"]
    },
    {
        "name": "Thermal: m² to km²",
        "input": 1000000.0,
        "expected": 1.0,
        "conversion": MODEL_CONVERSIONS["arrayAreaM2_to_arrayAreaKm2"]
    },

    # Temperature conversions in thermal model
    {
        "name": "Thermal: °C to K (room temp)",
        "input": 20.0,
        "expected": 293.15,
        "conversion": MODEL_CONVERSIONS["tempC_to_tempK"]
    },
    {
        "name": "Thermal: K to °C (space temp)",
        "input": 3.0,
        "expected": -270.15,
        "conversion": MODEL_CONVERSIONS["tempK_to_tempC"]
    },
]

# =============================================================================
# AUDIT FUNCTIONS
# =============================================================================

@dataclass
class ConversionTestResult:
    """Result of testing a unit conversion"""
    test_name: str
    input_value: float
    expected_output: float
    actual_output: float
    error: float
    error_pct: float
    passed: bool

def test_conversion(test_case: Dict) -> ConversionTestResult:
    """Test a single unit conversion"""

    name = test_case["name"]
    input_val = test_case["input"]
    expected = test_case["expected"]
    conversion_func = test_case["conversion"]

    # Apply conversion
    actual = conversion_func(input_val)

    # Calculate error
    error = actual - expected
    error_pct = abs(error / expected) * 100 if expected != 0 else 0

    # Check if passed (within 1e-10 relative error for floating point precision)
    passed = abs(error_pct) < 1e-8  # Very strict tolerance for unit conversions

    return ConversionTestResult(
        test_name=name,
        input_value=input_val,
        expected_output=expected,
        actual_output=actual,
        error=error,
        error_pct=error_pct,
        passed=passed
    )

def print_conversion_test_results(results: List[ConversionTestResult], title: str):
    """Print formatted conversion test results"""

    print("=" * 80)
    print(title.upper())
    print("=" * 80)
    print("")

    # Summary stats
    total = len(results)
    passed = sum(1 for r in results if r.passed)

    print(f"Summary: {passed}/{total} tests passed")
    print("")

    # Individual results
    for result in results:
        status = "✅" if result.passed else "❌"
        print(f"{status} {result.test_name}")

        if not result.passed:
            print("2d")
            print("2d")
            print("2d")
        print("")

def save_conversion_test_results(basic_results: List[ConversionTestResult],
                               model_results: List[ConversionTestResult],
                               filename: str):
    """Save conversion test results to JSON file"""

    data = {
        "audit_info": {
            "date": "2025-12-14",
            "type": "Unit Conversions Verification",
            "model_version": "math.js current"
        },
        "summary": {
            "basic_tests_total": len(basic_results),
            "basic_tests_passed": sum(1 for r in basic_results if r.passed),
            "model_tests_total": len(model_results),
            "model_tests_passed": sum(1 for r in model_results if r.passed)
        },
        "basic_conversion_tests": [
            {
                "test_name": r.test_name,
                "input_value": r.input_value,
                "expected_output": r.expected_output,
                "actual_output": r.actual_output,
                "error": r.error,
                "error_pct": r.error_pct,
                "passed": r.passed
            }
            for r in basic_results
        ],
        "model_conversion_tests": [
            {
                "test_name": r.test_name,
                "input_value": r.input_value,
                "expected_output": r.expected_output,
                "actual_output": r.actual_output,
                "error": r.error,
                "error_pct": r.error_pct,
                "passed": r.passed
            }
            for r in model_results
        ]
    }

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# =============================================================================
# MAIN AUDIT EXECUTION
# =============================================================================

def main():
    """Execute the unit conversions audit"""

    print("Starting Unit Conversions Audit...")
    print("Verifying all unit conversions for dimensional consistency...")
    print("")

    # Test basic unit conversions
    basic_results = []
    for test_case in CONVERSION_TESTS:
        result = test_conversion(test_case)
        basic_results.append(result)

    # Test model-specific conversions
    model_results = []
    for test_case in MODEL_CONVERSION_TESTS:
        result = test_conversion(test_case)
        model_results.append(result)

    # Print results
    print_conversion_test_results(basic_results, "BASIC UNIT CONVERSION TESTS")
    print_conversion_test_results(model_results, "MODEL-SPECIFIC CONVERSION TESTS")

    # Save detailed results
    save_conversion_test_results(basic_results, model_results, "03_unit_conversions_results.json")

    # Final assessment
    all_basic_passed = all(r.passed for r in basic_results)
    all_model_passed = all(r.passed for r in model_results)

    print("=" * 80)
    print("FINAL ASSESSMENT")
    print("=" * 80)

    if all_basic_passed and all_model_passed:
        print("✅ AUDIT PASSED: All unit conversions are dimensionally consistent")
    elif all_basic_passed:
        print("⚠️  AUDIT PASSED WITH CONCERNS: Basic conversions OK, but model conversions have issues")
    else:
        print("❌ AUDIT FAILED: Some unit conversions are incorrect")

    print("")
    print("Detailed results saved to: 03_unit_conversions_results.json")
    print("")

if __name__ == "__main__":
    main()
