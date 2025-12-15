# Formula Audit Summary

## Status: ✅ Core Formulas Verified (with important integration notes)

All mathematical formulas have been audited and verified against Python implementations.

---

## 1. Orbital Cost Breakdown ✅

| Component | Formula | Value (default params) |
|-----------|---------|----------------------|
| Hardware | `satelliteCostPerW × actualInitialPowerW` | $23.60B |
| Launch | `launchCostPerKg × totalMassKg` | $14.70B |
| Ops | `hardwareCost × 0.01 × years` | $1.18B |
| GPU Replacement | `hardwareCost × (gpuFailureRate/100) × years` | $10.62B |
| NRE | `nreCostMillions × 1e6` | $1.00B |
| **TOTAL** | `hardware + launch + ops + gpuRepl + nre` | **$51.10B** |

**Sanity Check:** Sum of components = Total ✅

---

## 2. Terrestrial Cost Breakdown ✅

| Component | Formula | Value (default params) |
|-----------|---------|----------------------|
| Power Gen | `gasTurbineCapexPerKW × PUE / 1000 × targetPowerW` | $2.16B |
| Electrical | `electricalCostPerW × targetPowerW` | $5.25B |
| Mechanical | `mechanicalCostPerW × targetPowerW` | $3.00B |
| Civil | `civilCostPerW × targetPowerW` | $2.50B |
| Fit-out | `networkCostPerW × targetPowerW` | $1.75B |
| Fuel | `fuelCostPerMWh × generationMWh` | $1.19B |
| **TOTAL** | `sum of all 6 components` | **$15.85B** |

**Sanity Check:** Sum of components = Total ✅

---

## 3. LCOE Calculations ✅

| Option | Formula | Value |
|--------|---------|-------|
| Orbital | `totalCost / energyMWh` | $1,167/MWh |
| Terrestrial | `totalCost / energyMWh` | $426/MWh |

**Note:** Energy bases differ:
- Orbital: 43,800,000 MWh (1 GW × 5 years × 8760 hrs - 100% availability)
- Terrestrial: 37,230,000 MWh (1 GW × 5 years × 8760 hrs × 0.85 CF)

---

## 4. Solar Degradation Margin ✅

```
annualRetention = 1 - (cellDegradation / 100) = 0.975
avgCapacityFactor = Σ(annualRetention^year) / years = 0.9512
sunlightAdjustedFactor = avgCapacityFactor × sunFraction = 0.9322
requiredInitialPowerW = targetPowerW / sunlightAdjustedFactor
solarMargin = (actualInitialPower / targetPower - 1) × 100 = +7.3%
```

**Verified:** Margin correctly accounts for degradation over analysis period ✅

---

## 5. GPU Failure Margin ✅

```
gpuMarginPct = gpuFailureRate × years = 9% × 5 = 45%
gpuReplacementCost = hardwareCost × (gpuFailureRate/100) × years
```

**Note:** GPU margin is budgeted as replacement cost, not additional initial capacity.

---

## 6. Thermal Physics ✅

### Heat Balance
```
Total Heat In = Solar Waste + Earth IR + Albedo + Heat Loop Return
             = 9.53 + 0.02 + 0.00 + 2.99 = 12.54 GW (at 10 km² array)

Radiative Capacity = σ × Area × (ε_pv + ε_rad) × (T⁴ - T_space⁴)
                   = 12.54 GW at equilibrium
```

**Verified:** Heat in = Heat out at equilibrium ✅

### Equilibrium Temperature
- At β=90° (terminator): 62.1°C ✅ (within 75°C limit)
- At β=0° (noon-midnight): 76.4°C ⚠️ (exceeds 75°C limit)

### Energy Partition
- Incident solar: 100%
- Reflected (1-α): 8%
- Electrical (η): 22%
- Immediate thermal: 70%
- **Total: 100%** ✅

---

## 7. Heat Rate / Efficiency ✅

Formula: `efficiency = 3412 / heat_rate`

| Heat Rate | Efficiency |
|-----------|------------|
| 6,000 BTU/kWh | 56.9% |
| 6,200 BTU/kWh (default) | 55.0% |
| 7,500 BTU/kWh | 45.5% |
| 9,000 BTU/kWh | 37.9% |

**Verified:** Slider labels match calculated efficiencies ✅

---

## Summary

All formulas are mathematically correct and internally consistent:

1. ✅ Cost breakdowns sum to displayed totals (both orbital and terrestrial)
2. ✅ LCOE calculated correctly as total cost / energy output
3. ✅ Solar degradation margin accounts for year-over-year capacity loss
4. ✅ GPU margin correctly computed as cumulative failure rate
5. ✅ Thermal equilibrium calculation balances heat in = heat out
6. ✅ Energy partition sums to 100%
7. ✅ Heat rate to efficiency conversion is correct

No formula errors found in `static/js/math.js`.

---

## Integration / Consistency Notes (important)

1. **Preferences wiring (removed)**:
   - The project no longer uses a Flask API or a constants editor UI; constants are configured in-code.

2. **UI tooltips vs code (fixed)**:
   - The thermal tooltips now match the side-specific Earth-IR and PV-side-only albedo formulas used by the model.

