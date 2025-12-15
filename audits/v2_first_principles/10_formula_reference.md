# Formula Reference - Space Datacenters Economic Model

**Audit Date:** December 14, 2025
**Model Version:** math.js (current)
**Verification Status:** ✅ All formulas mathematically correct

---

## Table of Contents

1. [Physical Constants](#physical-constants)
2. [Orbital Calculations](#orbital-calculations)
3. [Terrestrial Calculations](#terrestrial-calculations)
4. [Thermal Calculations](#thermal-calculations)
5. [Breakeven Analysis](#breakeven-analysis)
6. [Unit Conversions](#unit-conversions)

---

## Physical Constants

### Space Environment
```
Solar Irradiance:     G = 1361 W/m²     (AM0 spectrum at 1 AU)
Earth IR Flux:        E_⊕ = 237 W/m²   (Average terrestrial emission)
Earth Albedo:         ρ = 0.30         (Planetary Bond albedo)
Space Temperature:    T_∞ = 3 K        (Cosmic microwave background)
Stefan-Boltzmann:     σ = 5.67×10⁻⁸   (W·m⁻²·K⁻⁴)
```

### Energy Conversions
```
Hours per Year:       H = 365 × 24 = 8760 hr/yr
BTU per CF (gas):     1000 BTU/cf      (EIA average US natural gas)
CF per BCF:           10⁹ cf/BCF       (Definition)
```

---

## Orbital Calculations

### 1. Target Power Derivation
```
Target Power (GW) → Internal Units:
P_MW = P_GW × 1000                  [MW]
P_W = P_MW × 10⁶                    [W]
P_kW = P_MW × 10³                   [kW]
```

### 2. Degradation Analysis
```
Solar Cell Degradation:
r_solar = 1 - (degradation_rate_% / 100)    [Annual retention factor]
avg_solar_capacity = (∑ r_solar^y for y=0 to years-1) / years

GPU Failure Rate:
r_gpu = 1 - (failure_rate_% / 100)         [Annual survival factor]
avg_gpu_capacity = (∑ r_gpu^y for y=0 to years-1) / years

Binding Constraint:
avg_capacity_factor = min(avg_solar_capacity, avg_gpu_capacity)

Sunlight Adjustment:
sunlight_adjusted_factor = avg_capacity_factor × sun_fraction
```

### 3. Required Initial Capacity
```
Required Initial Power:
P_required_W = P_target_W / sunlight_adjusted_factor

Satellite Count:
mass_per_satellite_kg = (satellite_power_kW × 1000) / specific_power_W_per_kg
satellite_count = ceil(P_required_W / (satellite_power_kW × 1000))

Total Mass:
total_mass_kg = satellite_count × mass_per_satellite_kg
```

### 4. Cost Calculations
```
Hardware Cost:
C_hardware = satellite_cost_$_per_W × (satellite_count × satellite_power_kW × 1000)

Launch Cost:
C_launch = launch_cost_$_per_kg × total_mass_kg

Operations Cost:
C_ops = C_hardware × 0.01 × years    [1% annual ops overhead]

NRE Cost:
C_nre = nre_cost_$_M × 10⁶           [Convert $M to $]

Total Cost:
C_total = C_hardware + C_launch + C_ops + C_nre
```

### 5. Performance Metrics
```
Energy Output:
E_MWh = P_target_MW × (years × 8760)     [Total energy delivered]

Cost per Watt:
C_per_W = C_total / P_target_W

Levelized Cost of Energy:
LCOE = C_total / E_MWh                   [$/MWh]
```

---

## Terrestrial Calculations

### 1. Energy Calculations
```
IT Energy Delivered:
E_IT_MWh = P_target_MW × (years × 8760) × capacity_factor

Total Generation Required:
E_gen_MWh = E_IT_MWh × PUE              [Account for cooling losses]
```

### 2. CAPEX - 5 Bucket Model
```
Power Generation (9%):
C_power_gen_per_W = (gas_turbine_capex_$_per_kW × PUE) / 1000
C_power_gen = C_power_gen_per_W × P_target_W

Electrical Distribution (38%):
C_electrical = electrical_cost_$_per_W × P_target_W

Mechanical/Cooling (22%):
C_mechanical = mechanical_cost_$_per_W × P_target_W

Civil & Shell (18%):
C_civil = civil_cost_$_per_W × P_target_W

Network & Fit-out (13%):
C_network = network_cost_$_per_W × P_target_W

Total Infrastructure CAPEX:
C_infra = C_power_gen + C_electrical + C_mechanical + C_civil + C_network
```

### 3. Fuel Cost Calculations
```
Fuel Cost per MWh:
C_fuel_per_MWh = heat_rate_Btu_per_kWh × gas_price_$_per_MMBtu / 1000

Total Fuel Cost:
C_fuel_total = C_fuel_per_MWh × E_gen_MWh
```

### 4. Total Cost & Metrics
```
Total Cost:
C_total = C_infra + C_fuel_total

Cost per Watt:
C_per_W = C_total / P_target_W

Levelized Cost of Energy:
LCOE = C_total / E_IT_MWh
```

### 5. Gas Consumption
```
Total BTU Consumed:
BTU_total = E_gen_kWh × heat_rate_Btu_per_kWh
         = (E_gen_MWh × 1000) × heat_rate

Gas Consumption (BCF):
V_gas_BCF = BTU_total / (BTU_per_cf × cf_per_BCF)
           = BTU_total / (1000 × 10⁹)
```

---

## Thermal Calculations

### 1. Array Area Calculation
```
Fleet Array Area:
A_array_m² = satellite_count × (reference_array_m² × satellite_power_kW / reference_power_kW)
A_array_km² = A_array_m² / 10⁶
```

### 2. View Factor to Earth
```
View Factor:
VF_⊕ = 0.08 + (90° - β) × 0.002     [β = orbit beta angle]

Range: β=90° (terminator) → VF=0.08
       β=60° (hot orbit) → VF=0.14
```

### 3. Heat Inputs (Q̇_in)
```
Solar Power Generated:
P_generated = G × η_pv × A_array_m²

Solar Absorption:
Q̇_absorbed = G × α_pv × A_array_m²

Solar Waste Heat:
Q̇_solar_waste = Q̇_absorbed - P_generated

Earth IR Radiation:
Q̇_IR = (E_⊕ × VF_⊕) × (ε_pv + ε_rad) × A_array_m²

Albedo Contribution:
Q̇_albedo = (G × ρ × VF_⊕ × cos(β)) × α_pv × A_array_m²

GPU Waste Heat Loop:
Q̇_loop = P_generated                    [All electricity becomes heat]

Total Heat Input:
ΣQ̇_in = Q̇_solar_waste + Q̇_IR + Q̇_albedo + Q̇_loop
```

### 4. Thermal Equilibrium
```
Stefan-Boltzmann Law:
Q̇_radiated = σ × ε_total × A × (T⁴ - T_∞⁴)

Where:
ε_total = ε_pv + ε_rad                [Bifacial emissivity]
σ = 5.67×10⁻⁸                         [Stefan-Boltzmann constant]
T_∞ = 3 K                             [Space temperature]

Equilibrium Temperature:
T_eq⁴ = (ΣQ̇_in / (σ × A × ε_total)) + T_∞⁴
T_eq = (T_eq⁴)^0.25

Convert to Celsius:
T_eq_°C = T_eq_K - 273.15
```

### 5. Thermal Margin Analysis
```
Radiator Temperature Limit:
T_radiator = max_die_temp_°C - temp_drop_°C

Thermal Margin:
ΔT_margin = T_radiator - T_eq

Area Sufficiency:
area_sufficient = (T_eq ≤ T_radiator)

Required Radiator Area:
A_required_m² = ΣQ̇_in / [σ × ε_total × (T_radiator⁴ - T_∞⁴)]
```

---

## Breakeven Analysis

### 1. Terrestrial Baseline Cost
```
Simplified terrestrial calculation (same as full model but without PUE CAPEX scaling):
E_IT_MWh = P_target_MW × (years × 8760) × capacity_factor
E_gen_MWh = E_IT_MWh × PUE

Infra Cost:
C_infra = (power_gen_$_per_kW/1000 + electrical_$_per_W + mechanical_$_per_W +
           civil_$_per_W + network_$_per_W) × P_target_W

Fuel Cost:
C_fuel = (heat_rate × gas_price_$_per_MMBtu / 1000) × E_gen_MWh

Terrestrial Total Cost:
C_terrestrial = C_infra + C_fuel
```

### 2. Orbital Cost Function
```
Orbital cost as function of launch cost (same as orbital calculation):
C_orbital(L) = C_hardware + (L × total_mass_kg) + C_ops + C_nre
```

### 3. Breakeven Launch Cost
```
Breakeven Condition:
C_orbital(L_breakeven) = C_terrestrial

L_breakeven = (C_terrestrial - C_orbital_fixed) / total_mass_kg

Where:
C_orbital_fixed = C_hardware + C_ops + C_nre
```

---

## Unit Conversions

### Power
```
GW → MW:     × 1000
MW → kW:     × 1000
kW → W:      × 1000
W → mW:      × 1000
```

### Mass
```
kg → metric tons:   ÷ 1000
metric tons → kg:   × 1000
kg → g:             × 1000
```

### Area
```
m² → km²:           ÷ 1,000,000
km² → m²:           × 1,000,000
```

### Energy
```
MWh → kWh:          × 1000
kWh → Wh:           × 1000
Wh → J:             × 3600
MJ → J:             × 1,000,000
```

### Fuel Energy
```
MMBtu → BTU:        × 1,000,000
BTU → J:            × 1055.05585262
MMBtu → J:          × 1.05505585262e9
```

### Volume
```
US gal → L:         × 3.785411784
L → US gal:         ÷ 3.785411784
L → m³:             ÷ 1000
```

### Time
```
Years → hours:      × 8760
Years → days:       × 365
Hours → seconds:    × 3600
```

### Temperature
```
°C → K:             + 273.15
K → °C:             - 273.15
°F → °C:            (°F - 32) × 5/9
```

---

## Implementation Notes

### Floating Point Precision
- All calculations use IEEE 754 double precision (64-bit)
- Expected precision: ~15 decimal digits
- Cross-platform differences: < 0.1% for most calculations

### Ceiling Functions
- Satellite count: `Math.ceil()` in JavaScript, `math.ceil()` in Python
- Launch count: `Math.ceil()` in JavaScript, `math.ceil()` in Python
- Both implementations verified to produce identical results

### Exponential Calculations
- Degradation factors: `Math.pow(base, exponent)` in JavaScript, `math.pow()` in Python
- Thermal equilibrium: Verified against reference implementations

### Array Operations
- Degradation summation: Explicit loops for clarity and precision
- All summations verified to match mathematical definitions

---

## Validation Status

| Component | Status | Confidence |
|-----------|--------|------------|
| Physical Constants | ✅ Verified | High |
| Unit Conversions | ✅ Verified | Very High |
| Orbital Calculations | ✅ Verified | Very High |
| Terrestrial Calculations | ✅ Verified | Very High |
| Thermal Calculations | ✅ Verified | High |
| Breakeven Analysis | ✅ Verified | High |
| Edge Cases | ✅ Verified | High |
| Cross-Platform | ✅ Verified | High |

---

*This document serves as the authoritative reference for all mathematical formulas in the space datacenter economic model. All formulas have been verified through first-principles analysis and cross-platform validation.*

