"""
Sanity check for math calculations in the model.
Verifies that with URL params, the calculated values are reasonable.
"""

# Test parameters from URL: ?y=10&gw=100&lc=100&ba=60&pue=1.4&gp=12
test_state = {
    'years': 10,
    'targetGW': 100,
    'launchCostPerKg': 100,
    'betaAngle': 60,
    'pue': 1.4,
    'gasPricePerMMBtu': 12.0,
    
    # Remaining defaults
    'solarAbsorptivity': 0.92,
    'emissivityPV': 0.85,
    'emissivityRad': 0.90,
    'pvEfficiency': 0.22,
    'orbitalAltitudeKm': 550,
    'maxDieTempC': 85,
    'tempDropC': 10,
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
    'heatRateBtuKwh': 6200,
    'capacityFactor': 0.85
}

# Constants from math.js
HOURS_PER_YEAR = 8760
STARLINK_ARRAY_M2 = 116
STARLINK_POWER_KW = 27
STARSHIP_PAYLOAD_KG = 100000
ORBITAL_OPS_FRAC = 0.01
BTU_PER_CF = 1000
CF_PER_BCF = 1e9
GE_7HA_POWER_MW = 430


def calculate_orbital():
    """Simplified orbital calculation."""
    target_power_w = test_state['targetGW'] * 1e9
    total_hours = test_state['years'] * HOURS_PER_YEAR
    
    # Degradation
    annual_retention = 1 - (test_state['cellDegradation'] / 100)
    capacity_sum = sum(annual_retention ** year for year in range(test_state['years']))
    avg_capacity_factor = capacity_sum / test_state['years']
    
    # Required initial power
    sunlight_adjusted = avg_capacity_factor * test_state['sunFraction']
    required_initial_power_w = target_power_w / sunlight_adjusted
    
    # Satellite sizing
    mass_per_sat_kg = (test_state['satellitePowerKW'] * 1000) / test_state['specificPowerWPerKg']
    satellite_count = int(required_initial_power_w / (test_state['satellitePowerKW'] * 1000)) + 1
    total_mass_kg = satellite_count * mass_per_sat_kg
    actual_initial_power_w = satellite_count * test_state['satellitePowerKW'] * 1000
    
    # Costs
    hardware_cost = test_state['satelliteCostPerW'] * actual_initial_power_w
    launch_cost = test_state['launchCostPerKg'] * total_mass_kg
    ops_cost = hardware_cost * ORBITAL_OPS_FRAC * test_state['years']
    gpu_replacement = hardware_cost * (test_state['gpuFailureRate'] / 100) * test_state['years']
    nre_cost = test_state['nreCost'] * 1e6
    total_cost = hardware_cost + launch_cost + ops_cost + gpu_replacement + nre_cost
    
    # Energy
    energy_mwh = test_state['targetGW'] * 1000 * total_hours
    cost_per_w = total_cost / target_power_w
    lcoe = total_cost / energy_mwh
    
    return {
        'total_cost': total_cost,
        'cost_per_w': cost_per_w,
        'lcoe': lcoe,
        'satellite_count': satellite_count,
        'total_mass_kg': total_mass_kg,
        'energy_mwh': energy_mwh,
        'hardware_cost': hardware_cost,
        'launch_cost': launch_cost,
    }


def calculate_terrestrial():
    """Simplified terrestrial calculation."""
    target_power_w = test_state['targetGW'] * 1e9
    total_hours = test_state['years'] * HOURS_PER_YEAR
    
    # CAPEX
    power_gen_cost_per_w = test_state['gasTurbineCapexPerKW'] * test_state['pue'] / 1000
    power_gen_cost = power_gen_cost_per_w * target_power_w
    electrical_cost = test_state['electricalCostPerW'] * target_power_w
    mechanical_cost = test_state['mechanicalCostPerW'] * target_power_w
    civil_cost = test_state['civilCostPerW'] * target_power_w
    network_cost = test_state['networkCostPerW'] * target_power_w
    infra_capex = power_gen_cost + electrical_cost + mechanical_cost + civil_cost + network_cost
    
    # Energy
    energy_mwh = test_state['targetGW'] * 1000 * total_hours * test_state['capacityFactor']
    generation_mwh = energy_mwh * test_state['pue']
    
    # Fuel cost
    fuel_cost_per_mwh = test_state['heatRateBtuKwh'] * test_state['gasPricePerMMBtu'] / 1000
    fuel_cost = fuel_cost_per_mwh * generation_mwh
    
    total_cost = infra_capex + fuel_cost
    cost_per_w = total_cost / target_power_w
    lcoe = total_cost / energy_mwh
    
    return {
        'total_cost': total_cost,
        'cost_per_w': cost_per_w,
        'lcoe': lcoe,
        'energy_mwh': energy_mwh,
        'fuel_cost': fuel_cost,
        'infra_capex': infra_capex,
        'fuel_cost_per_mwh': fuel_cost_per_mwh,
    }


def format_currency(val):
    if val >= 1e12:
        return f"${val/1e12:.1f}T"
    elif val >= 1e9:
        return f"${val/1e9:.1f}B"
    elif val >= 1e6:
        return f"${val/1e6:.0f}M"
    return f"${val:.0f}"


def main():
    print("=" * 60)
    print("MATH SANITY CHECK FOR URL PARAMS")
    print("=" * 60)
    print(f"\nTest URL: ?y=10&gw=100&lc=100&ba=60&pue=1.4&gp=12")
    print()
    
    orbital = calculate_orbital()
    terrestrial = calculate_terrestrial()
    
    print("ORBITAL SOLAR:")
    print(f"  Total Cost: {format_currency(orbital['total_cost'])}")
    print(f"  Cost per Watt: ${orbital['cost_per_w']:.2f}/W")
    print(f"  LCOE: ${orbital['lcoe']:.0f}/MWh")
    print(f"  Satellite Count: ~{orbital['satellite_count']:,}")
    print(f"  Total Mass: {orbital['total_mass_kg']/1e6:.1f}M kg")
    print(f"  Energy Output: {orbital['energy_mwh']/1e6:.0f}M MWh")
    print(f"  Hardware Cost: {format_currency(orbital['hardware_cost'])}")
    print(f"  Launch Cost: {format_currency(orbital['launch_cost'])}")
    print()
    
    print("TERRESTRIAL (CCGT):")
    print(f"  Total Cost: {format_currency(terrestrial['total_cost'])}")
    print(f"  Cost per Watt: ${terrestrial['cost_per_w']:.2f}/W")
    print(f"  LCOE: ${terrestrial['lcoe']:.0f}/MWh")
    print(f"  Energy Output: {terrestrial['energy_mwh']/1e6:.0f}M MWh")
    print(f"  Fuel Cost: {format_currency(terrestrial['fuel_cost'])}")
    print(f"  Fuel $/MWh: ${terrestrial['fuel_cost_per_mwh']:.0f}/MWh")
    print(f"  Infrastructure: {format_currency(terrestrial['infra_capex'])}")
    print()
    
    # Sanity checks
    print("SANITY CHECKS:")
    checks_passed = True
    
    # 1. 100 GW should cost trillions, not billions or quadrillions
    if 1e12 < orbital['total_cost'] < 1e14:
        print("  ✓ Orbital cost in expected range ($1T-$100T)")
    else:
        print(f"  ✗ Orbital cost unexpected: {format_currency(orbital['total_cost'])}")
        checks_passed = False
    
    if 1e12 < terrestrial['total_cost'] < 1e14:
        print("  ✓ Terrestrial cost in expected range ($1T-$100T)")
    else:
        print(f"  ✗ Terrestrial cost unexpected: {format_currency(terrestrial['total_cost'])}")
        checks_passed = False
    
    # 2. Cost per watt should be in reasonable range ($10-$100/W for orbital)
    if 10 < orbital['cost_per_w'] < 200:
        print(f"  ✓ Orbital $/W reasonable: ${orbital['cost_per_w']:.2f}/W")
    else:
        print(f"  ✗ Orbital $/W unexpected: ${orbital['cost_per_w']:.2f}/W")
        checks_passed = False
    
    if 10 < terrestrial['cost_per_w'] < 50:
        print(f"  ✓ Terrestrial $/W reasonable: ${terrestrial['cost_per_w']:.2f}/W")
    else:
        print(f"  ✗ Terrestrial $/W unexpected: ${terrestrial['cost_per_w']:.2f}/W")
        checks_passed = False
    
    # 3. Energy output sanity (100 GW * 10 years * 8760 hours ≈ 8.76 TWh)
    expected_energy_mwh = 100 * 1000 * 10 * HOURS_PER_YEAR
    if abs(orbital['energy_mwh'] - expected_energy_mwh) < 1e6:
        print(f"  ✓ Orbital energy correct: {orbital['energy_mwh']/1e6:.0f}M MWh")
    else:
        print(f"  ✗ Orbital energy wrong: got {orbital['energy_mwh']/1e6:.0f}M, expected {expected_energy_mwh/1e6:.0f}M")
        checks_passed = False
    
    # 4. Fuel cost should be higher with $12 gas
    if terrestrial['fuel_cost_per_mwh'] > 70:
        print(f"  ✓ High gas price reflected: ${terrestrial['fuel_cost_per_mwh']:.0f}/MWh fuel cost")
    else:
        print(f"  ✗ Fuel cost too low for $12 gas: ${terrestrial['fuel_cost_per_mwh']:.0f}/MWh")
        checks_passed = False
    
    # 5. With cheap $100/kg launch, orbital should be more competitive
    if orbital['total_cost'] < terrestrial['total_cost'] * 5:
        print(f"  ✓ Cheap launch makes orbital more competitive: orbital/terrestrial = {orbital['total_cost']/terrestrial['total_cost']:.1f}x")
    else:
        print(f"  ⚠ Even with $100/kg launch, orbital still expensive: {orbital['total_cost']/terrestrial['total_cost']:.1f}x terrestrial")
        # Not a failure, just an observation
    
    print()
    print("=" * 60)
    if checks_passed:
        print("ALL SANITY CHECKS PASSED!")
    else:
        print("SOME CHECKS FAILED!")
    print("=" * 60)
    
    return checks_passed


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

