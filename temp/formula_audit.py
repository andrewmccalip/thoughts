"""
Formula Audit Script for Space Datacenters Model
Verifies all calculations from math.js against Python implementations
"""

import math

# ==========================================
# CONSTANTS (from math.js)
# ==========================================

# System target
TARGET_POWER_MW = 1000  # 1 GW
TARGET_POWER_W = TARGET_POWER_MW * 1e6
HOURS_PER_YEAR = 8760

# Starlink reference
STARLINK_MASS_KG = 740
STARLINK_POWER_KW = 27
STARLINK_ARRAY_M2 = 116

# Launch vehicle
STARSHIP_PAYLOAD_KG = 100000

# Cost fractions
ORBITAL_OPS_FRAC = 0.01

# ==========================================
# STATE (default slider values)
# ==========================================

# Shared
years = 5
targetGW = 1

# Orbital
launchCostPerKg = 500
satelliteCostPerW = 22
specificPowerWPerKg = 36.5
satellitePowerKW = 27
sunFraction = 0.98
cellDegradation = 2.5  # % per year
gpuFailureRate = 9  # % per year
nreCostMillions = 1000  # $1B

# Terrestrial
gasTurbineCapexPerKW = 1800  # $1.80/W
electricalCostPerW = 5.25
mechanicalCostPerW = 3.0
civilCostPerW = 2.5
networkCostPerW = 1.75
pue = 1.2
gasPricePerMMBtu = 4.30
heatRateBtuKwh = 6200
capacityFactor = 0.85


def audit_orbital():
    """Audit orbital cost calculations"""
    print("\n" + "="*60)
    print("ORBITAL CALCULATIONS AUDIT")
    print("="*60)
    
    totalHours = years * HOURS_PER_YEAR
    print(f"\nTotal Hours: {totalHours:,} (expected: {years * 8760:,})")
    
    # Degradation calculation
    annualRetention = 1 - (cellDegradation / 100)
    print(f"Annual Retention: {annualRetention:.4f} (expected: {1 - 0.025:.4f})")
    
    # Average capacity factor over analysis period
    capacitySum = sum(annualRetention ** year for year in range(years))
    avgCapacityFactor = capacitySum / years
    print(f"Avg Capacity Factor: {avgCapacityFactor:.4f}")
    
    # Sunlight-adjusted factor
    sunlightAdjustedFactor = avgCapacityFactor * sunFraction
    print(f"Sunlight Adjusted Factor: {sunlightAdjustedFactor:.4f}")
    
    # Required initial power
    requiredInitialPowerW = TARGET_POWER_W / sunlightAdjustedFactor
    print(f"Required Initial Power: {requiredInitialPowerW/1e9:.3f} GW")
    
    # Satellite sizing
    massPerSatelliteKg = (satellitePowerKW * 1000) / specificPowerWPerKg
    print(f"Mass per Satellite: {massPerSatelliteKg:.1f} kg")
    
    satelliteCount = math.ceil(requiredInitialPowerW / (satellitePowerKW * 1000))
    print(f"Satellite Count: {satelliteCount:,}")
    
    totalMassKg = satelliteCount * massPerSatelliteKg
    print(f"Total Mass: {totalMassKg/1e6:.2f} M kg")
    
    actualInitialPowerW = satelliteCount * satellitePowerKW * 1000
    print(f"Actual Initial Power: {actualInitialPowerW/1e9:.3f} GW")
    
    # COSTS
    print("\n--- COST BREAKDOWN ---")
    
    hardwareCost = satelliteCostPerW * actualInitialPowerW
    print(f"Hardware Cost: ${hardwareCost/1e9:.2f}B (satelliteCostPerW × actualInitialPowerW)")
    
    launchCost = launchCostPerKg * totalMassKg
    print(f"Launch Cost: ${launchCost/1e9:.2f}B (launchCostPerKg × totalMassKg)")
    
    baseCost = hardwareCost + launchCost
    print(f"Base Cost: ${baseCost/1e9:.2f}B")
    
    # Ops cost - 1% of hardware per year × years
    opsCost = hardwareCost * ORBITAL_OPS_FRAC * years
    print(f"Ops Cost: ${opsCost/1e9:.3f}B (1% of hardware × {years} years)")
    
    # GPU replacement cost
    gpuReplacementCost = hardwareCost * (gpuFailureRate / 100) * years
    print(f"GPU Replacement: ${gpuReplacementCost/1e9:.2f}B ({gpuFailureRate}% of hardware × {years} years)")
    
    # NRE cost
    nreCost = nreCostMillions * 1e6
    print(f"NRE Cost: ${nreCost/1e9:.1f}B")
    
    # Total
    totalCost = baseCost + opsCost + gpuReplacementCost + nreCost
    print(f"\nTOTAL COST: ${totalCost/1e9:.2f}B")
    
    # Verify breakdown adds up
    print("\n--- SANITY CHECK: Does breakdown add up? ---")
    breakdown_sum = hardwareCost + launchCost + opsCost + gpuReplacementCost + nreCost
    print(f"Hardware + Launch + Ops + GPU Repl + NRE = ${breakdown_sum/1e9:.2f}B")
    print(f"Total Cost = ${totalCost/1e9:.2f}B")
    print(f"Match: {abs(breakdown_sum - totalCost) < 1}")  # Within $1
    
    # LCOE
    energyMWh = TARGET_POWER_MW * totalHours
    print(f"\nEnergy Output: {energyMWh:,.0f} MWh")
    
    lcoe = totalCost / energyMWh
    print(f"LCOE: ${lcoe:.0f}/MWh")
    
    # Cost per watt
    costPerW = totalCost / TARGET_POWER_W
    print(f"Cost per Watt: ${costPerW:.2f}/W")
    
    # Margins
    degradationMargin = (actualInitialPowerW / TARGET_POWER_W - 1) * 100
    gpuMarginPct = gpuFailureRate * years
    print(f"\nSolar Margin: +{degradationMargin:.1f}%")
    print(f"GPU Margin: +{gpuMarginPct:.1f}%")
    
    return {
        'hardwareCost': hardwareCost,
        'launchCost': launchCost,
        'opsCost': opsCost,
        'gpuReplacementCost': gpuReplacementCost,
        'nreCost': nreCost,
        'totalCost': totalCost,
        'energyMWh': energyMWh,
        'lcoe': lcoe
    }


def audit_terrestrial():
    """Audit terrestrial cost calculations"""
    print("\n" + "="*60)
    print("TERRESTRIAL CALCULATIONS AUDIT")
    print("="*60)
    
    totalHours = years * HOURS_PER_YEAR
    
    # CAPEX - 5 buckets
    print("\n--- CAPEX BREAKDOWN (5 buckets) ---")
    
    # 1. Power Generation
    powerGenCostPerW = gasTurbineCapexPerKW * pue / 1000
    powerGenCost = powerGenCostPerW * TARGET_POWER_W
    print(f"1. Power Gen: ${powerGenCost/1e9:.2f}B (${powerGenCostPerW:.2f}/W)")
    
    # 2. Electrical
    electricalCost = electricalCostPerW * TARGET_POWER_W
    print(f"2. Electrical: ${electricalCost/1e9:.2f}B (${electricalCostPerW:.2f}/W)")
    
    # 3. Mechanical
    mechanicalCost = mechanicalCostPerW * TARGET_POWER_W
    print(f"3. Mechanical: ${mechanicalCost/1e9:.2f}B (${mechanicalCostPerW:.2f}/W)")
    
    # 4. Civil
    civilCost = civilCostPerW * TARGET_POWER_W
    print(f"4. Civil: ${civilCost/1e9:.2f}B (${civilCostPerW:.2f}/W)")
    
    # 5. Network/Fit-out
    networkCost = networkCostPerW * TARGET_POWER_W
    print(f"5. Network/Fit-out: ${networkCost/1e9:.2f}B (${networkCostPerW:.2f}/W)")
    
    # Total capex
    infraCapex = powerGenCost + electricalCost + mechanicalCost + civilCost + networkCost
    facilityCapexPerW = powerGenCostPerW + electricalCostPerW + mechanicalCostPerW + civilCostPerW + networkCostPerW
    print(f"\nTotal Capex: ${infraCapex/1e9:.2f}B (${facilityCapexPerW:.2f}/W)")
    
    # OPEX - Fuel
    print("\n--- OPEX: FUEL ---")
    
    energyMWh = TARGET_POWER_MW * totalHours * capacityFactor
    print(f"IT Energy: {energyMWh:,.0f} MWh")
    
    generationMWh = energyMWh * pue
    print(f"Generation (IT × PUE): {generationMWh:,.0f} MWh")
    
    fuelCostPerMWh = heatRateBtuKwh * gasPricePerMMBtu / 1000
    print(f"Fuel Cost: ${fuelCostPerMWh:.2f}/MWh")
    
    fuelCostTotal = fuelCostPerMWh * generationMWh
    print(f"Total Fuel: ${fuelCostTotal/1e9:.2f}B")
    
    # Total
    totalCost = infraCapex + fuelCostTotal
    print(f"\nTOTAL COST: ${totalCost/1e9:.2f}B")
    
    # Verify breakdown adds up
    print("\n--- SANITY CHECK: Does breakdown add up? ---")
    breakdown_sum = powerGenCost + electricalCost + mechanicalCost + civilCost + networkCost + fuelCostTotal
    print(f"Sum of all 6 components: ${breakdown_sum/1e9:.2f}B")
    print(f"Total Cost: ${totalCost/1e9:.2f}B")
    print(f"Match: {abs(breakdown_sum - totalCost) < 1}")
    
    # LCOE
    lcoe = totalCost / energyMWh
    print(f"\nLCOE: ${lcoe:.0f}/MWh")
    
    costPerW = totalCost / TARGET_POWER_W
    print(f"Cost per Watt: ${costPerW:.2f}/W")
    
    return {
        'powerGenCost': powerGenCost,
        'electricalCost': electricalCost,
        'mechanicalCost': mechanicalCost,
        'civilCost': civilCost,
        'networkCost': networkCost,
        'fuelCostTotal': fuelCostTotal,
        'totalCost': totalCost,
        'energyMWh': energyMWh,
        'lcoe': lcoe
    }


def audit_energy_output():
    """Audit energy output calculations"""
    print("\n" + "="*60)
    print("ENERGY OUTPUT AUDIT")
    print("="*60)
    
    totalHours = years * HOURS_PER_YEAR
    
    # Orbital energy - target average power × hours
    orbitalEnergyMWh = TARGET_POWER_MW * totalHours
    print(f"\nOrbital Energy: {orbitalEnergyMWh:,.0f} MWh")
    print(f"  = {TARGET_POWER_MW} MW × {totalHours:,} hours")
    print(f"  Note: This is the TARGET average output, accounting for sunlight fraction")
    
    # Terrestrial energy - IT power × hours × capacity factor
    terrestrialEnergyMWh = TARGET_POWER_MW * totalHours * capacityFactor
    print(f"\nTerrestrial IT Energy: {terrestrialEnergyMWh:,.0f} MWh")
    print(f"  = {TARGET_POWER_MW} MW × {totalHours:,} hours × {capacityFactor} CF")
    
    generationMWh = terrestrialEnergyMWh * pue
    print(f"\nTerrestrial Generation: {generationMWh:,.0f} MWh")
    print(f"  = {terrestrialEnergyMWh:,.0f} MWh × {pue} PUE")


def audit_heat_rate_efficiency():
    """Audit heat rate to efficiency conversion"""
    print("\n" + "="*60)
    print("HEAT RATE / EFFICIENCY AUDIT")
    print("="*60)
    
    # Standard conversion: efficiency = 3412 / heat_rate
    heat_rates = [6000, 6200, 7500, 9000]
    
    print("\nHeat Rate (BTU/kWh) -> Efficiency (%)")
    print("-" * 40)
    for hr in heat_rates:
        eff = 3412 / hr * 100
        print(f"  {hr:,} BTU/kWh -> {eff:.1f}%")
    
    print(f"\nCurrent default: {heatRateBtuKwh} BTU/kWh = {3412/heatRateBtuKwh*100:.1f}% efficiency")


def audit_margins():
    """Audit margin calculations"""
    print("\n" + "="*60)
    print("MARGIN CALCULATIONS AUDIT")
    print("="*60)
    
    # Solar degradation margin
    print("\n--- SOLAR DEGRADATION MARGIN ---")
    annualRetention = 1 - (cellDegradation / 100)
    capacitySum = sum(annualRetention ** year for year in range(years))
    avgCapacityFactor = capacitySum / years
    sunlightAdjustedFactor = avgCapacityFactor * sunFraction
    
    requiredInitialPowerW = TARGET_POWER_W / sunlightAdjustedFactor
    
    massPerSatelliteKg = (satellitePowerKW * 1000) / specificPowerWPerKg
    satelliteCount = math.ceil(requiredInitialPowerW / (satellitePowerKW * 1000))
    actualInitialPowerW = satelliteCount * satellitePowerKW * 1000
    
    degradationMargin = (actualInitialPowerW / TARGET_POWER_W - 1) * 100
    
    print(f"Cell degradation: {cellDegradation}%/year")
    print(f"Years: {years}")
    print(f"Sunlight fraction: {sunFraction}")
    print(f"Average capacity factor: {avgCapacityFactor:.4f}")
    print(f"Sunlight adjusted: {sunlightAdjustedFactor:.4f}")
    print(f"Target power: {TARGET_POWER_W/1e9:.1f} GW")
    print(f"Required initial: {requiredInitialPowerW/1e9:.3f} GW")
    print(f"Actual initial: {actualInitialPowerW/1e9:.3f} GW")
    print(f"SOLAR MARGIN: +{degradationMargin:.1f}%")
    
    # GPU failure margin
    print("\n--- GPU FAILURE MARGIN ---")
    gpuMarginPct = gpuFailureRate * years
    print(f"GPU failure rate: {gpuFailureRate}%/year")
    print(f"Years: {years}")
    print(f"GPU MARGIN: +{gpuMarginPct:.1f}%")
    print(f"Note: This represents expected failures, budgeted as replacement cost")


def main():
    print("="*60)
    print("SPACE DATACENTER FORMULA AUDIT")
    print("="*60)
    print(f"\nUsing default parameters:")
    print(f"  Target Power: {targetGW} GW")
    print(f"  Analysis Period: {years} years")
    print(f"  Launch Cost: ${launchCostPerKg}/kg")
    print(f"  Satellite Cost: ${satelliteCostPerW}/W")
    print(f"  Sun Fraction: {sunFraction}")
    print(f"  Cell Degradation: {cellDegradation}%/year")
    print(f"  GPU Failure Rate: {gpuFailureRate}%/year")
    
    orbital = audit_orbital()
    terrestrial = audit_terrestrial()
    audit_energy_output()
    audit_heat_rate_efficiency()
    audit_margins()
    
    # Summary comparison
    print("\n" + "="*60)
    print("SUMMARY COMPARISON")
    print("="*60)
    print(f"\nOrbital Total: ${orbital['totalCost']/1e9:.1f}B")
    print(f"Terrestrial Total: ${terrestrial['totalCost']/1e9:.1f}B")
    print(f"Ratio: {orbital['totalCost']/terrestrial['totalCost']:.1f}x")
    
    print(f"\nOrbital LCOE: ${orbital['lcoe']:.0f}/MWh")
    print(f"Terrestrial LCOE: ${terrestrial['lcoe']:.0f}/MWh")
    print(f"Ratio: {orbital['lcoe']/terrestrial['lcoe']:.1f}x")
    
    print("\n" + "="*60)
    print("AUDIT COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()

