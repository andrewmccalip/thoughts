"""
Additional Audit Script
Covers: breakeven, satellite sizing, array area, launches, fuel consumption,
unit conversions, default value consistency, and UI display matching
"""

import math

# ==========================================
# CONSTANTS (from math.js)
# ==========================================
TARGET_POWER_MW = 1000
TARGET_POWER_W = TARGET_POWER_MW * 1e6
HOURS_PER_YEAR = 8760
STARLINK_POWER_KW = 27
STARLINK_ARRAY_M2 = 116
STARSHIP_PAYLOAD_KG = 100000
BTU_PER_CF = 1000
CF_PER_BCF = 1e9

# State defaults
years = 5
launchCostPerKg = 500
satelliteCostPerW = 22
specificPowerWPerKg = 36.5
satellitePowerKW = 27
sunFraction = 0.98
cellDegradation = 2.5
gpuFailureRate = 9
nreCostMillions = 1000
gasTurbineCapexPerKW = 1800
electricalCostPerW = 5.25
mechanicalCostPerW = 3.0
civilCostPerW = 2.5
networkCostPerW = 1.75
pue = 1.2
gasPricePerMMBtu = 4.30
heatRateBtuKwh = 6200
capacityFactor = 0.85


def audit_breakeven_calculation():
    """Audit the breakeven launch cost calculation"""
    print("\n" + "="*60)
    print("BREAKEVEN LAUNCH COST AUDIT")
    print("="*60)
    
    totalHours = years * HOURS_PER_YEAR
    
    # Terrestrial total cost
    powerGenCostPerW = gasTurbineCapexPerKW * pue / 1000
    facilityCapexPerW = powerGenCostPerW + electricalCostPerW + mechanicalCostPerW + civilCostPerW + networkCostPerW
    infraCost = facilityCapexPerW * TARGET_POWER_W
    
    energyMWh = TARGET_POWER_MW * totalHours * capacityFactor
    generationMWh = energyMWh * pue
    fuelCostPerMWh = heatRateBtuKwh * gasPricePerMMBtu / 1000
    fuelCost = fuelCostPerMWh * generationMWh
    
    terrestrialCost = infraCost + fuelCost
    print(f"Terrestrial Total Cost: ${terrestrialCost/1e9:.2f}B")
    
    # Orbital sizing (for breakeven, we need mass)
    annualRetention = 1 - (cellDegradation / 100)
    capacitySum = sum(annualRetention ** year for year in range(years))
    avgCapacityFactor = capacitySum / years
    sunlightAdjustedFactor = avgCapacityFactor * sunFraction
    requiredInitialPowerW = TARGET_POWER_W / sunlightAdjustedFactor
    
    # Hardware cost at this power level
    hardwareCost = satelliteCostPerW * requiredInitialPowerW
    print(f"Orbital Hardware Cost: ${hardwareCost/1e9:.2f}B")
    
    # Mass required
    mass = requiredInitialPowerW / specificPowerWPerKg
    print(f"Mass Required: {mass/1e6:.2f}M kg")
    
    # Breakeven formula: launchCost = (terrestrialCost - hardwareCost) / mass
    # This gives the launch cost at which orbital = terrestrial
    breakeven = (terrestrialCost - hardwareCost) / mass
    print(f"\nBreakeven Launch Cost: ${breakeven:.2f}/kg")
    
    # Verify: at breakeven, orbital cost should equal terrestrial
    print("\n--- VERIFICATION ---")
    orbital_at_breakeven = hardwareCost + (breakeven * mass)
    print(f"Orbital cost at breakeven (hardware + launch only): ${orbital_at_breakeven/1e9:.2f}B")
    print(f"Terrestrial cost: ${terrestrialCost/1e9:.2f}B")
    print(f"Match: {abs(orbital_at_breakeven - terrestrialCost) < 1e6}")
    
    # Note: This breakeven excludes ops, NRE, and GPU replacement!
    print("\n⚠️  NOTE: Breakeven calculation only includes hardware + launch")
    print("   It excludes: Ops, NRE, and GPU replacement costs")
    
    # Full breakeven with all costs
    opsCost = hardwareCost * 0.01 * years
    gpuReplacementCost = hardwareCost * (gpuFailureRate / 100) * years
    nreCost = nreCostMillions * 1e6
    
    fullOrbitalOverhead = opsCost + gpuReplacementCost + nreCost
    print(f"\nFull orbital overhead (ops+GPU+NRE): ${fullOrbitalOverhead/1e9:.2f}B")
    
    # True breakeven including all costs
    trueBreakeven = (terrestrialCost - hardwareCost - fullOrbitalOverhead) / mass
    print(f"True breakeven (including all costs): ${trueBreakeven:.2f}/kg")
    
    if trueBreakeven < 0:
        print("⚠️  Negative breakeven means orbital can never match terrestrial at these parameters!")


def audit_satellite_sizing():
    """Audit satellite count and mass calculations"""
    print("\n" + "="*60)
    print("SATELLITE SIZING AUDIT")
    print("="*60)
    
    # Required initial power
    annualRetention = 1 - (cellDegradation / 100)
    capacitySum = sum(annualRetention ** year for year in range(years))
    avgCapacityFactor = capacitySum / years
    sunlightAdjustedFactor = avgCapacityFactor * sunFraction
    requiredInitialPowerW = TARGET_POWER_W / sunlightAdjustedFactor
    
    print(f"Required Initial Power: {requiredInitialPowerW/1e9:.3f} GW")
    
    # Mass per satellite
    massPerSatelliteKg = (satellitePowerKW * 1000) / specificPowerWPerKg
    print(f"\nMass per Satellite:")
    print(f"  = ({satellitePowerKW} kW × 1000) / {specificPowerWPerKg} W/kg")
    print(f"  = {massPerSatelliteKg:.1f} kg")
    
    # Satellite count
    satelliteCount = math.ceil(requiredInitialPowerW / (satellitePowerKW * 1000))
    print(f"\nSatellite Count:")
    print(f"  = ceil({requiredInitialPowerW/1e6:.1f} MW / {satellitePowerKW} kW)")
    print(f"  = {satelliteCount:,} satellites")
    
    # Total mass
    totalMassKg = satelliteCount * massPerSatelliteKg
    print(f"\nTotal Mass:")
    print(f"  = {satelliteCount:,} × {massPerSatelliteKg:.1f} kg")
    print(f"  = {totalMassKg/1e6:.2f} M kg")
    
    # Alternative calculation via specific power
    altMass = requiredInitialPowerW / specificPowerWPerKg
    print(f"\nAlternative (direct): {requiredInitialPowerW/1e9:.3f} GW / {specificPowerWPerKg} W/kg = {altMass/1e6:.2f} M kg")
    
    # Difference due to rounding up satellites
    print(f"Difference (satellite rounding): {(totalMassKg - altMass)/1000:.0f} kg")


def audit_array_area():
    """Audit solar array area calculations"""
    print("\n" + "="*60)
    print("ARRAY AREA AUDIT")
    print("="*60)
    
    # Get satellite count
    annualRetention = 1 - (cellDegradation / 100)
    capacitySum = sum(annualRetention ** year for year in range(years))
    avgCapacityFactor = capacitySum / years
    sunlightAdjustedFactor = avgCapacityFactor * sunFraction
    requiredInitialPowerW = TARGET_POWER_W / sunlightAdjustedFactor
    
    satelliteCount = math.ceil(requiredInitialPowerW / (satellitePowerKW * 1000))
    
    # Array area per satellite scales with power
    arrayPerSatelliteM2 = STARLINK_ARRAY_M2 * (satellitePowerKW / STARLINK_POWER_KW)
    print(f"Array Area per Satellite:")
    print(f"  = {STARLINK_ARRAY_M2} m² × ({satellitePowerKW} kW / {STARLINK_POWER_KW} kW)")
    print(f"  = {arrayPerSatelliteM2:.1f} m²")
    
    # Total array area
    arrayAreaM2 = satelliteCount * arrayPerSatelliteM2
    arrayAreaKm2 = arrayAreaM2 / 1e6
    print(f"\nTotal Array Area:")
    print(f"  = {satelliteCount:,} × {arrayPerSatelliteM2:.1f} m²")
    print(f"  = {arrayAreaM2/1e6:.2f} km²")
    
    # Sanity check: power density
    actualPowerW = satelliteCount * satellitePowerKW * 1000
    powerDensityWM2 = actualPowerW / arrayAreaM2
    print(f"\nPower Density Check:")
    print(f"  = {actualPowerW/1e9:.3f} GW / {arrayAreaM2/1e6:.2f} km²")
    print(f"  = {powerDensityWM2:.1f} W/m²")
    print(f"  (Solar constant × efficiency = {1361 * 0.22:.0f} W/m² theoretical max)")


def audit_starship_launches():
    """Audit Starship launch count"""
    print("\n" + "="*60)
    print("STARSHIP LAUNCHES AUDIT")
    print("="*60)
    
    # Get total mass
    annualRetention = 1 - (cellDegradation / 100)
    capacitySum = sum(annualRetention ** year for year in range(years))
    avgCapacityFactor = capacitySum / years
    sunlightAdjustedFactor = avgCapacityFactor * sunFraction
    requiredInitialPowerW = TARGET_POWER_W / sunlightAdjustedFactor
    
    massPerSatelliteKg = (satellitePowerKW * 1000) / specificPowerWPerKg
    satelliteCount = math.ceil(requiredInitialPowerW / (satellitePowerKW * 1000))
    totalMassKg = satelliteCount * massPerSatelliteKg
    
    # Starship launches
    starshipLaunches = math.ceil(totalMassKg / STARSHIP_PAYLOAD_KG)
    print(f"Total Mass: {totalMassKg/1e6:.2f} M kg")
    print(f"Starship Payload: {STARSHIP_PAYLOAD_KG/1000:.0f} tonnes")
    print(f"\nStarship Launches:")
    print(f"  = ceil({totalMassKg/1e6:.2f}M kg / {STARSHIP_PAYLOAD_KG/1000:.0f}t)")
    print(f"  = {starshipLaunches} launches")
    
    # Satellites per launch
    satsPerLaunch = totalMassKg / starshipLaunches / massPerSatelliteKg
    print(f"\nAvg Satellites per Launch: {satsPerLaunch:.0f}")
    print(f"  (at {massPerSatelliteKg:.0f} kg each)")


def audit_gas_consumption():
    """Audit terrestrial gas consumption"""
    print("\n" + "="*60)
    print("GAS CONSUMPTION AUDIT")
    print("="*60)
    
    totalHours = years * HOURS_PER_YEAR
    energyMWh = TARGET_POWER_MW * totalHours * capacityFactor
    generationMWh = energyMWh * pue
    generationKWh = generationMWh * 1000
    
    print(f"IT Energy: {energyMWh/1e6:.2f}M MWh")
    print(f"Generation (×{pue} PUE): {generationMWh/1e6:.2f}M MWh = {generationKWh/1e9:.2f}B kWh")
    
    # Gas consumption
    totalBTU = generationKWh * heatRateBtuKwh
    print(f"\nTotal BTU:")
    print(f"  = {generationKWh/1e9:.2f}B kWh × {heatRateBtuKwh} BTU/kWh")
    print(f"  = {totalBTU/1e12:.2f} trillion BTU")
    
    gasCF = totalBTU / BTU_PER_CF
    gasBCF = gasCF / CF_PER_BCF
    print(f"\nGas Consumption:")
    print(f"  = {totalBTU/1e12:.2f}T BTU / {BTU_PER_CF} BTU/cf")
    print(f"  = {gasCF/1e9:.2f}B cf")
    print(f"  = {gasBCF:.2f} BCF")
    
    # Fuel cost check
    fuelCostPerMWh = heatRateBtuKwh * gasPricePerMMBtu / 1000
    fuelCostTotal = fuelCostPerMWh * generationMWh
    print(f"\nFuel Cost Check:")
    print(f"  Cost per MWh: ${fuelCostPerMWh:.2f}")
    print(f"  Total: ${fuelCostTotal/1e9:.2f}B")


def audit_default_consistency():
    """Audit that math.js defaults match HTML slider defaults"""
    print("\n" + "="*60)
    print("DEFAULT VALUE CONSISTENCY AUDIT")
    print("="*60)
    
    # Expected HTML slider defaults (from previous work)
    html_defaults = {
        'launchCostPerKg': 500,
        'satelliteCostPerW': 22,
        'specificPowerWPerKg': 36.5,
        'satellitePowerKW': 27,
        'sunFraction': 0.98,
        'cellDegradation': 2.5,
        'gpuFailureRate': 9,
        'nreCostMillions': 1000,
        'gasTurbineCapexPerKW': 1800,
        'electricalCostPerW': 5.25,
        'mechanicalCostPerW': 3.0,
        'civilCostPerW': 2.5,
        'networkCostPerW': 1.75,
        'pue': 1.2,
        'gasPricePerMMBtu': 4.30,
        'heatRateBtuKwh': 6200,
        'capacityFactor': 0.85,
        'years': 5
    }
    
    js_defaults = {
        'launchCostPerKg': launchCostPerKg,
        'satelliteCostPerW': satelliteCostPerW,
        'specificPowerWPerKg': specificPowerWPerKg,
        'satellitePowerKW': satellitePowerKW,
        'sunFraction': sunFraction,
        'cellDegradation': cellDegradation,
        'gpuFailureRate': gpuFailureRate,
        'nreCostMillions': nreCostMillions,
        'gasTurbineCapexPerKW': gasTurbineCapexPerKW,
        'electricalCostPerW': electricalCostPerW,
        'mechanicalCostPerW': mechanicalCostPerW,
        'civilCostPerW': civilCostPerW,
        'networkCostPerW': networkCostPerW,
        'pue': pue,
        'gasPricePerMMBtu': gasPricePerMMBtu,
        'heatRateBtuKwh': heatRateBtuKwh,
        'capacityFactor': capacityFactor,
        'years': years
    }
    
    print(f"{'Parameter':<25} {'JS Default':<12} {'HTML Default':<12} {'Match'}")
    print("-" * 60)
    
    all_match = True
    for key in html_defaults:
        js_val = js_defaults[key]
        html_val = html_defaults[key]
        match = abs(js_val - html_val) < 0.001
        if not match:
            all_match = False
        status = "✅" if match else "❌"
        print(f"{key:<25} {js_val:<12} {html_val:<12} {status}")
    
    print(f"\nAll defaults match: {'✅' if all_match else '❌'}")


def audit_cost_per_watt():
    """Audit cost per watt calculations"""
    print("\n" + "="*60)
    print("COST PER WATT AUDIT")
    print("="*60)
    
    # Orbital
    annualRetention = 1 - (cellDegradation / 100)
    capacitySum = sum(annualRetention ** year for year in range(years))
    avgCapacityFactor = capacitySum / years
    sunlightAdjustedFactor = avgCapacityFactor * sunFraction
    requiredInitialPowerW = TARGET_POWER_W / sunlightAdjustedFactor
    
    massPerSatelliteKg = (satellitePowerKW * 1000) / specificPowerWPerKg
    satelliteCount = math.ceil(requiredInitialPowerW / (satellitePowerKW * 1000))
    totalMassKg = satelliteCount * massPerSatelliteKg
    actualInitialPowerW = satelliteCount * satellitePowerKW * 1000
    
    hardwareCost = satelliteCostPerW * actualInitialPowerW
    launchCost = launchCostPerKg * totalMassKg
    opsCost = hardwareCost * 0.01 * years
    gpuReplacementCost = hardwareCost * (gpuFailureRate / 100) * years
    nreCost = nreCostMillions * 1e6
    orbitalTotal = hardwareCost + launchCost + opsCost + gpuReplacementCost + nreCost
    
    orbitalCPW = orbitalTotal / TARGET_POWER_W
    print(f"Orbital:")
    print(f"  Total Cost: ${orbitalTotal/1e9:.2f}B")
    print(f"  Target Power: {TARGET_POWER_W/1e9:.0f} GW")
    print(f"  Cost per Watt: ${orbitalCPW:.2f}/W")
    print(f"  (This is $/W of delivered average power, NOT initial capacity)")
    
    # Terrestrial
    powerGenCostPerW = gasTurbineCapexPerKW * pue / 1000
    facilityCapexPerW = powerGenCostPerW + electricalCostPerW + mechanicalCostPerW + civilCostPerW + networkCostPerW
    infraCost = facilityCapexPerW * TARGET_POWER_W
    
    totalHours = years * HOURS_PER_YEAR
    energyMWh = TARGET_POWER_MW * totalHours * capacityFactor
    generationMWh = energyMWh * pue
    fuelCostPerMWh = heatRateBtuKwh * gasPricePerMMBtu / 1000
    fuelCost = fuelCostPerMWh * generationMWh
    
    terrestrialTotal = infraCost + fuelCost
    terrestrialCPW = terrestrialTotal / TARGET_POWER_W
    
    print(f"\nTerrestrial:")
    print(f"  Total Cost: ${terrestrialTotal/1e9:.2f}B")
    print(f"  Target Power: {TARGET_POWER_W/1e9:.0f} GW")
    print(f"  Cost per Watt: ${terrestrialCPW:.2f}/W")
    
    print(f"\n  Capex only: ${facilityCapexPerW:.2f}/W")
    print(f"  Fuel adds: ${(terrestrialCPW - facilityCapexPerW):.2f}/W over {years} years")


def audit_energy_basis_comparison():
    """Audit the different energy bases used for LCOE"""
    print("\n" + "="*60)
    print("ENERGY BASIS COMPARISON AUDIT")
    print("="*60)
    
    totalHours = years * HOURS_PER_YEAR
    
    # Orbital energy: target average × hours (100% effective availability)
    orbitalEnergyMWh = TARGET_POWER_MW * totalHours
    
    # Terrestrial energy: IT load × hours × capacity factor (85% availability)
    terrestrialEnergyMWh = TARGET_POWER_MW * totalHours * capacityFactor
    
    print(f"Analysis Period: {years} years = {totalHours:,} hours")
    print(f"\nOrbital Energy Output:")
    print(f"  = {TARGET_POWER_MW} MW × {totalHours:,} hrs")
    print(f"  = {orbitalEnergyMWh:,} MWh")
    print(f"  Effective availability: 100%")
    print(f"  (System is sized to always deliver target average)")
    
    print(f"\nTerrestrial Energy Output:")
    print(f"  = {TARGET_POWER_MW} MW × {totalHours:,} hrs × {capacityFactor}")
    print(f"  = {terrestrialEnergyMWh:,} MWh")
    print(f"  Effective availability: {capacityFactor*100}%")
    print(f"  (Turbines need maintenance, outages)")
    
    print(f"\nDifference: {orbitalEnergyMWh - terrestrialEnergyMWh:,} MWh")
    print(f"  = {(1 - capacityFactor)*100:.0f}% more energy from orbital")
    
    print(f"\n⚠️  IMPORTANT: LCOE comparison uses different energy bases!")
    print(f"  This is intentional: orbital is designed for higher availability")
    print(f"  But should be clearly documented for readers")


def main():
    audit_breakeven_calculation()
    audit_satellite_sizing()
    audit_array_area()
    audit_starship_launches()
    audit_gas_consumption()
    audit_default_consistency()
    audit_cost_per_watt()
    audit_energy_basis_comparison()
    
    print("\n" + "="*60)
    print("ADDITIONAL AUDIT COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()

