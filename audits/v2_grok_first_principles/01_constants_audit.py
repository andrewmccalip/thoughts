#!/usr/bin/env python3
"""
First Principles Audit: Physical Constants Verification
=======================================================

This script verifies all physical constants used in the space datacenter model
against authoritative sources. Each constant is checked for accuracy within
accepted scientific ranges.

Audit Date: December 14, 2025
Model Version: math.js (current)
"""

import math
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

# =============================================================================
# PHYSICAL CONSTANTS FROM MODEL (static/js/math.js)
# =============================================================================

MODEL_CONSTANTS = {
    # Space Environment (Section 1)
    "SOLAR_IRRADIANCE_W_M2": 1361,          # Solar constant at 1 AU (AM0 spectrum)
    "EARTH_IR_FLUX_W_M2": 237,              # Earth's average infrared emission
    "EARTH_ALBEDO": 0.30,                   # Earth's average reflectivity (unitless)
    "T_SPACE_K": 3,                         # Deep space background temperature (Kelvin)
    "STEFAN_BOLTZMANN": 5.67e-8,            # σ = 5.67×10⁻⁸ W·m⁻²·K⁻⁴

    # Time Constants
    "HOURS_PER_YEAR": 8760,                 # 365 days × 24 hours

    # Energy Conversions
    "BTU_PER_CF": 1000,                     # BTU per cubic foot of natural gas
    "CF_PER_BCF": 1e9                       # Cubic feet per billion cubic feet
}

# =============================================================================
# AUTHORITATIVE REFERENCE VALUES
# =============================================================================

REFERENCE_VALUES = {
    # Solar Irradiance (AM0 - Air Mass Zero)
    # Source: NASA/NOAA Solar Radiation Data Sets, ASTM E490-00a
    "SOLAR_IRRADIANCE_W_M2": {
        "value": 1366.1,  # W/m² (accepted range: 1360-1370)
        "tolerance": 0.01,  # ±1% acceptable variation
        "source": "NASA/NOAA ASTM E490-00a",
        "notes": "AM0 spectrum at 1 AU. Model uses 1361 W/m² (0.37% low)"
    },

    # Stefan-Boltzmann Constant
    # Source: NIST CODATA 2022
    "STEFAN_BOLTZMANN": {
        "value": 5.670367e-8,  # W·m⁻²·K⁻⁴
        "tolerance": 1e-10,    # Extremely precise
        "source": "NIST CODATA 2022",
        "notes": "σ = 5.670367×10⁻⁸. Model uses 5.67×10⁻⁸ (0.006% low)"
    },

    # Earth Infrared Flux
    # Source: NASA CERES dataset, Trenberth et al. (2009)
    "EARTH_IR_FLUX_W_M2": {
        "value": 239.7,  # W/m² (global average)
        "tolerance": 0.05,  # ±5% due to seasonal/cloud variation
        "source": "NASA CERES / Trenberth et al. (2009)",
        "notes": "Global average IR emission. Model uses 237 W/m² (1.1% low)"
    },

    # Earth Albedo (Bond Albedo)
    # Source: NASA Earth Observatory, Stephens et al. (2015)
    "EARTH_ALBEDO": {
        "value": 0.306,  # Unitless (planetary Bond albedo)
        "tolerance": 0.03,  # ±3% variation with clouds/season
        "source": "NASA / Stephens et al. (2015)",
        "notes": "Planetary Bond albedo. Model uses 0.30 (1.3% low)"
    },

    # Deep Space Temperature
    # Source: COBE/FIRAS CMB measurements, Fixsen et al. (1996)
    "T_SPACE_K": {
        "value": 2.725,  # Kelvin (CMB temperature)
        "tolerance": 0.01,  # Extremely precise measurement
        "source": "COBE/FIRAS CMB measurements",
        "notes": "Cosmic Microwave Background temperature. Model uses 3 K (10% high)"
    },

    # Hours per Year
    # Source: Gregorian calendar calculation
    "HOURS_PER_YEAR": {
        "value": 8760,  # 365 × 24 = 8760 (non-leap year)
        "tolerance": 0.0,  # Exact by definition
        "source": "Gregorian calendar arithmetic",
        "notes": "365 days × 24 hours. Model value exact."
    },

    # Natural Gas Energy Content
    # Source: EIA Natural Gas Monthly, API standards
    "BTU_PER_CF": {
        "value": 1034,  # BTU/cf (EIA average for US natural gas)
        "tolerance": 0.05,  # ±5% variation by region/gas composition
        "source": "EIA Natural Gas Monthly / API standards",
        "notes": "Average US natural gas: 1034 BTU/cf. Model uses 1000 BTU/cf (3.1% low)"
    },

    # Billion Cubic Feet Conversion
    # Source: Standard SI/unit definition
    "CF_PER_BCF": {
        "value": 1_000_000_000,  # 10^9 by definition
        "tolerance": 0.0,  # Exact by definition
        "source": "SI unit definition (10^9)",
        "notes": "1 BCF = 1 × 10^9 CF by definition. Model value exact."
    }
}

# =============================================================================
# AUDIT FUNCTIONS
# =============================================================================

@dataclass
class AuditResult:
    """Result of auditing a single constant"""
    constant_name: str
    model_value: float
    reference_value: float
    deviation: float
    deviation_pct: float
    within_tolerance: bool
    confidence: str
    notes: str

def audit_constant(name: str, model_val: float, ref_data: Dict) -> AuditResult:
    """Audit a single physical constant"""

    ref_val = ref_data["value"]
    tolerance = ref_data["tolerance"]

    # Calculate deviation
    deviation = model_val - ref_val
    deviation_pct = abs(deviation / ref_val) * 100

    # Check if within tolerance
    within_tolerance = abs(deviation) <= (ref_val * tolerance)

    # Assign confidence level
    if abs(deviation_pct) < 0.1:
        confidence = "VERY HIGH"
    elif abs(deviation_pct) < 1.0:
        confidence = "HIGH"
    elif abs(deviation_pct) < 5.0:
        confidence = "MEDIUM"
    elif abs(deviation_pct) < 10.0:
        confidence = "LOW"
    else:
        confidence = "VERY LOW"

    return AuditResult(
        constant_name=name,
        model_value=model_val,
        reference_value=ref_val,
        deviation=deviation,
        deviation_pct=deviation_pct,
        within_tolerance=within_tolerance,
        confidence=confidence,
        notes=ref_data["notes"]
    )

def print_audit_results(results: List[AuditResult]):
    """Print formatted audit results"""

    print("=" * 80)
    print("PHYSICAL CONSTANTS AUDIT RESULTS")
    print("=" * 80)
    print("")

    # Summary stats
    total = len(results)
    within_tol = sum(1 for r in results if r.within_tolerance)
    high_conf = sum(1 for r in results if r.confidence in ["VERY HIGH", "HIGH"])

    print(f"Summary: {within_tol}/{total} within tolerance, {high_conf}/{total} high confidence")
    print("")

    # Individual results
    for result in results:
        status = "✅" if result.within_tolerance else "⚠️"
        print(f"{status} {result.constant_name}")
        print("2d")
        print("2d")
        print(f"   Confidence: {result.confidence}")
        print(f"   Notes: {result.notes}")
        print("")

def save_audit_results(results: List[AuditResult], filename: str):
    """Save audit results to JSON file"""

    data = {
        "audit_info": {
            "date": "2025-12-14",
            "type": "Physical Constants Verification",
            "model_version": "math.js current"
        },
        "summary": {
            "total_constants": len(results),
            "within_tolerance": sum(1 for r in results if r.within_tolerance),
            "high_confidence": sum(1 for r in results if r.confidence in ["VERY HIGH", "HIGH"]),
            "medium_confidence": sum(1 for r in results if r.confidence == "MEDIUM"),
            "low_confidence": sum(1 for r in results if r.confidence in ["LOW", "VERY LOW"])
        },
        "results": [
            {
                "constant": r.constant_name,
                "model_value": r.model_value,
                "reference_value": r.reference_value,
                "deviation": r.deviation,
                "deviation_pct": r.deviation_pct,
                "within_tolerance": r.within_tolerance,
                "confidence": r.confidence,
                "notes": r.notes
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
    """Execute the physical constants audit"""

    print("Starting Physical Constants Audit...")
    print("Verifying all constants against authoritative sources...")
    print("")

    results = []

    # Audit each constant
    for name, model_val in MODEL_CONSTANTS.items():
        if name in REFERENCE_VALUES:
            result = audit_constant(name, model_val, REFERENCE_VALUES[name])
            results.append(result)
        else:
            print(f"⚠️  WARNING: No reference data for {name}")

    # Print results
    print_audit_results(results)

    # Save detailed results
    save_audit_results(results, "01_constants_audit_results.json")

    # Final assessment
    all_within_tol = all(r.within_tolerance for r in results)
    high_conf_count = sum(1 for r in results if r.confidence in ["VERY HIGH", "HIGH"])

    print("=" * 80)
    print("FINAL ASSESSMENT")
    print("=" * 80)

    if all_within_tol and high_conf_count >= len(results) * 0.8:
        print("✅ AUDIT PASSED: All constants within tolerance with high confidence")
    elif all_within_tol:
        print("⚠️  AUDIT PASSED WITH CONCERNS: All within tolerance but some low confidence")
    else:
        print("❌ AUDIT FAILED: Some constants outside acceptable tolerance")

    print("")
    print("Detailed results saved to: 01_constants_audit_results.json")
    print("")

if __name__ == "__main__":
    main()
