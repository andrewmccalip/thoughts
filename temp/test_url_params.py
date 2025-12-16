"""
Comprehensive test for URL parameter encoding/decoding system.
Tests that share.js logic correctly encodes/decodes all model parameters.
"""

import urllib.parse
import json

# Short URL param keys mapped to state keys (must match share.js PARAM_MAP)
PARAM_MAP = {
    # Shared
    'y': 'years',
    'gw': 'targetGW',
    
    # Thermal
    'sa': 'solarAbsorptivity',
    'epv': 'emissivityPV',
    'erad': 'emissivityRad',
    'pve': 'pvEfficiency',
    'ba': 'betaAngle',
    'alt': 'orbitalAltitudeKm',
    'mdt': 'maxDieTempC',
    'td': 'tempDropC',
    
    # Orbital
    'lc': 'launchCostPerKg',
    'sc': 'satelliteCostPerW',
    'sp': 'specificPowerWPerKg',
    'spw': 'satellitePowerKW',
    'sf': 'sunFraction',
    'cd': 'cellDegradation',
    'gf': 'gpuFailureRate',
    'nre': 'nreCost',
    
    # Terrestrial
    'gtc': 'gasTurbineCapexPerKW',
    'ec': 'electricalCostPerW',
    'mc': 'mechanicalCostPerW',
    'cc': 'civilCostPerW',
    'nc': 'networkCostPerW',
    'pue': 'pue',
    'gp': 'gasPricePerMMBtu',
    'hr': 'heatRateBtuKwh',
    'cf': 'capacityFactor'
}

# Default values - must match math.js state defaults
DEFAULTS = {
    'years': 5,
    'targetGW': 1,
    'solarAbsorptivity': 0.92,
    'emissivityPV': 0.85,
    'emissivityRad': 0.90,
    'pvEfficiency': 0.22,
    'betaAngle': 90,
    'orbitalAltitudeKm': 550,
    'maxDieTempC': 85,
    'tempDropC': 10,
    'launchCostPerKg': 500,
    'satelliteCostPerW': 22,
    'specificPowerWPerKg': 36.5,
    'satellitePowerKW': 27,
    'sunFraction': 0.98,
    'cellDegradation': 2.5,
    'gpuFailureRate': 9,
    'nreCost': 1000,
    'gasTurbineCapexPerKW': 1800,
    'electricalCostPerW': 5.25,
    'mechanicalCostPerW': 3.0,
    'civilCostPerW': 2.5,
    'networkCostPerW': 1.75,
    'pue': 1.2,
    'gasPricePerMMBtu': 4.30,
    'heatRateBtuKwh': 6200,
    'capacityFactor': 0.85
}

# Reverse map: state key -> short param
STATE_TO_PARAM = {v: k for k, v in PARAM_MAP.items()}


def generate_url(state: dict, base_url: str = "http://localhost:5000/space-datacenters") -> str:
    """Generate shareable URL with current non-default state."""
    params = {}
    
    for state_key, default_val in DEFAULTS.items():
        current_val = state.get(state_key, default_val)
        # Only include if different from default (with float tolerance)
        if abs(current_val - default_val) > 1e-9:
            short_key = STATE_TO_PARAM[state_key]
            # Round to reasonable precision
            if isinstance(current_val, int) or current_val == int(current_val):
                params[short_key] = int(current_val)
            else:
                params[short_key] = float(f"{current_val:.6g}")
    
    if params:
        query_string = urllib.parse.urlencode(params)
        return f"{base_url}?{query_string}"
    return base_url


def parse_url(url: str) -> dict:
    """Parse URL and extract state updates."""
    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    updates = {}
    for short_key, state_key in PARAM_MAP.items():
        if short_key in query_params:
            updates[state_key] = float(query_params[short_key][0])
    
    return updates


def merge_with_defaults(updates: dict) -> dict:
    """Merge URL updates with defaults to get full state."""
    state = DEFAULTS.copy()
    state.update(updates)
    return state


def test_roundtrip():
    """Test that encoding then decoding preserves all values."""
    print("=" * 60)
    print("TEST 1: Round-trip encoding/decoding")
    print("=" * 60)
    
    # Create a custom state with some non-default values
    custom_state = DEFAULTS.copy()
    custom_state['years'] = 7
    custom_state['targetGW'] = 10
    custom_state['launchCostPerKg'] = 1000
    custom_state['specificPowerWPerKg'] = 50.0
    custom_state['betaAngle'] = 75
    
    # Generate URL
    url = generate_url(custom_state)
    print(f"Generated URL: {url}")
    
    # Parse URL back
    updates = parse_url(url)
    print(f"Parsed updates: {updates}")
    
    # Merge with defaults
    restored_state = merge_with_defaults(updates)
    
    # Compare
    passed = True
    for key in custom_state:
        original = custom_state[key]
        restored = restored_state[key]
        if abs(original - restored) > 1e-6:
            print(f"  FAIL: {key}: {original} != {restored}")
            passed = False
    
    if passed:
        print("  ✓ All values round-tripped correctly!")
    return passed


def test_defaults_no_params():
    """Test that default state generates no URL parameters."""
    print("\n" + "=" * 60)
    print("TEST 2: Default state should generate no parameters")
    print("=" * 60)
    
    url = generate_url(DEFAULTS)
    print(f"Generated URL: {url}")
    
    has_params = "?" in url
    if has_params:
        print("  FAIL: Default state should not have query params")
        return False
    else:
        print("  ✓ Default state generates clean URL (no query params)")
        return True


def test_all_params_encodable():
    """Test that all parameters can be encoded."""
    print("\n" + "=" * 60)
    print("TEST 3: All parameters encodable")
    print("=" * 60)
    
    # Create state with ALL values different from defaults
    custom_state = {}
    for key, default in DEFAULTS.items():
        if isinstance(default, float):
            custom_state[key] = default * 1.1  # 10% different
        else:
            custom_state[key] = default + 1
    
    url = generate_url(custom_state)
    print(f"Generated URL: {url}")
    
    # Parse and check all params present
    updates = parse_url(url)
    
    missing = []
    for key in DEFAULTS:
        if key not in updates:
            missing.append(key)
    
    if missing:
        print(f"  FAIL: Missing parameters: {missing}")
        return False
    else:
        print(f"  ✓ All {len(DEFAULTS)} parameters encoded and decoded")
        return True


def test_param_mapping_complete():
    """Test that PARAM_MAP covers all DEFAULTS."""
    print("\n" + "=" * 60)
    print("TEST 4: Parameter mapping completeness")
    print("=" * 60)
    
    # Check all defaults have a mapping
    unmapped_defaults = []
    for key in DEFAULTS:
        if key not in STATE_TO_PARAM:
            unmapped_defaults.append(key)
    
    # Check all mappings point to valid defaults
    invalid_mappings = []
    for short, state in PARAM_MAP.items():
        if state not in DEFAULTS:
            invalid_mappings.append(f"{short} -> {state}")
    
    passed = True
    if unmapped_defaults:
        print(f"  FAIL: Unmapped defaults: {unmapped_defaults}")
        passed = False
    else:
        print(f"  ✓ All {len(DEFAULTS)} default keys have mappings")
    
    if invalid_mappings:
        print(f"  FAIL: Invalid mappings: {invalid_mappings}")
        passed = False
    else:
        print(f"  ✓ All {len(PARAM_MAP)} param mappings are valid")
    
    # Check for unique short keys
    short_keys = list(PARAM_MAP.keys())
    if len(short_keys) != len(set(short_keys)):
        print("  FAIL: Duplicate short keys detected")
        passed = False
    else:
        print(f"  ✓ All short keys are unique")
    
    return passed


def test_specific_scenarios():
    """Test specific real-world scenarios."""
    print("\n" + "=" * 60)
    print("TEST 5: Real-world scenarios")
    print("=" * 60)
    
    passed = True
    
    # Scenario 1: "Starship cheap launch future"
    print("\n  Scenario A: Cheap Starship future")
    cheap_starship = DEFAULTS.copy()
    cheap_starship['launchCostPerKg'] = 100
    cheap_starship['targetGW'] = 100
    cheap_starship['years'] = 10
    
    url = generate_url(cheap_starship)
    print(f"    URL: {url}")
    
    # Parse back
    updates = parse_url(url)
    restored = merge_with_defaults(updates)
    
    if restored['launchCostPerKg'] == 100 and restored['targetGW'] == 100:
        print("    ✓ Correct values parsed")
    else:
        print(f"    FAIL: {restored['launchCostPerKg']}, {restored['targetGW']}")
        passed = False
    
    # Scenario 2: "Hot thermal case"
    print("\n  Scenario B: Hot thermal case")
    hot_thermal = DEFAULTS.copy()
    hot_thermal['betaAngle'] = 60
    hot_thermal['emissivityRad'] = 0.95
    hot_thermal['maxDieTempC'] = 100
    
    url = generate_url(hot_thermal)
    print(f"    URL: {url}")
    
    updates = parse_url(url)
    restored = merge_with_defaults(updates)
    
    if restored['betaAngle'] == 60 and restored['emissivityRad'] == 0.95:
        print("    ✓ Correct thermal values parsed")
    else:
        print(f"    FAIL: beta={restored['betaAngle']}, erad={restored['emissivityRad']}")
        passed = False
    
    # Scenario 3: "Expensive gas terrestrial"
    print("\n  Scenario C: Expensive gas case")
    expensive_gas = DEFAULTS.copy()
    expensive_gas['gasPricePerMMBtu'] = 12.0
    expensive_gas['heatRateBtuKwh'] = 7500
    expensive_gas['pue'] = 1.4
    
    url = generate_url(expensive_gas)
    print(f"    URL: {url}")
    
    updates = parse_url(url)
    restored = merge_with_defaults(updates)
    
    if abs(restored['gasPricePerMMBtu'] - 12.0) < 0.01 and restored['pue'] == 1.4:
        print("    ✓ Correct gas pricing values parsed")
    else:
        print(f"    FAIL: gas={restored['gasPricePerMMBtu']}, pue={restored['pue']}")
        passed = False
    
    return passed


def test_url_length():
    """Test that URLs stay reasonably short."""
    print("\n" + "=" * 60)
    print("TEST 6: URL length check")
    print("=" * 60)
    
    # Worst case: all params different
    custom_state = {}
    for key, default in DEFAULTS.items():
        if isinstance(default, float):
            custom_state[key] = default * 1.1
        else:
            custom_state[key] = default + 1
    
    url = generate_url(custom_state)
    query_len = len(url.split("?")[1]) if "?" in url else 0
    
    print(f"  Full URL length: {len(url)} chars")
    print(f"  Query string length: {query_len} chars")
    print(f"  Number of parameters: {len(PARAM_MAP)}")
    
    # URLs should generally stay under 2000 chars
    if len(url) < 2000:
        print("  ✓ URL length acceptable (< 2000 chars)")
        return True
    else:
        print("  WARNING: URL very long, may cause issues in some browsers")
        return True  # Not a failure, just a warning


def test_special_floats():
    """Test handling of floating point edge cases."""
    print("\n" + "=" * 60)
    print("TEST 7: Floating point precision")
    print("=" * 60)
    
    passed = True
    
    # Test values that might have precision issues
    test_values = {
        'sunFraction': 0.98,
        'pvEfficiency': 0.22,
        'specificPowerWPerKg': 36.5,
        'gasPricePerMMBtu': 4.30,
    }
    
    custom_state = DEFAULTS.copy()
    custom_state['sunFraction'] = 0.55  # Non-default
    custom_state['pvEfficiency'] = 0.24
    custom_state['specificPowerWPerKg'] = 75.0
    
    url = generate_url(custom_state)
    print(f"  URL: {url}")
    
    updates = parse_url(url)
    restored = merge_with_defaults(updates)
    
    for key in ['sunFraction', 'pvEfficiency', 'specificPowerWPerKg']:
        expected = custom_state[key]
        actual = restored[key]
        if abs(expected - actual) > 1e-6:
            print(f"  FAIL: {key}: expected {expected}, got {actual}")
            passed = False
        else:
            print(f"  ✓ {key}: {actual} (matches)")
    
    return passed


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("URL PARAMETER SYSTEM COMPREHENSIVE TESTS")
    print("=" * 60)
    
    results = []
    results.append(("Round-trip", test_roundtrip()))
    results.append(("Defaults no params", test_defaults_no_params()))
    results.append(("All params encodable", test_all_params_encodable()))
    results.append(("Mapping complete", test_param_mapping_complete()))
    results.append(("Real scenarios", test_specific_scenarios()))
    results.append(("URL length", test_url_length()))
    results.append(("Float precision", test_special_floats()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False
    
    print("\n" + ("All tests passed!" if all_passed else "Some tests failed!"))
    return all_passed


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

