# Third-Party Audit – Orbital vs Terrestrial Economic Analysis
**Date:** 2025-12-11  
**Auditor:** GPT-5.1 Codex (independent run)

## Scope & Method
- Reviewed the economic math engine in `static/js/math.js` and mirrored Python parity script `temp/check_numbers.py`.
- Recomputed every intermediate value for the baseline configuration (1 GW target, 5-year horizon) via both Node and Python to confirm parity.
- Added a scenario harness (`temp/run_setpoints.js`) and captured results in `audit/setpoint_runs.json` to probe non-default inputs.
- Cross-checked numerical outputs against relevant physics/industry heuristics (Starship payload limits, NGCC gas burn, array areas, etc.).
- Flagged any inconsistencies or risky assumptions, and summarized residual risks.

## Baseline Inputs (shared state)
| Parameter | Value | Notes |
| --- | --- | --- |
| Target capacity | 1 GW IT load | `state.targetGW = 1`
| Analysis window | 5 years | `state.years = 5`
| Sunlight fraction | 0.98 | Terminator orbit assumption
| Cell degradation | 2.5%/yr | Compounded via geometric mean
| GPU failure rate | 9%/yr | Irrecoverable attrition folded into capacity sizing
| Launch cost | $1,000/kg | Starship early price target
| Satellite cost | $22/W | Derived from ~$800/kg BOM
| Specific power | 36.5 W/kg | Starlink V2 Mini reference
| PUE (terrestrial) | 1.2 | Liquid cooling assumption
| Gas price | $4.30/MMBtu | EIA 2025 forecast
| Capacity factor | 0.85 | Reflects high GPU utilization

## Orbital Cost Model Review
Key equations are implemented in `calculateOrbital()` and follow the sequence shown below:
```164:265:static/js/math.js
function calculateOrbital() {
    const totalHours = state.years * constants.HOURS_PER_YEAR;
    const annualPvRetention = 1 - (state.cellDegradation / 100);
    const annualGpuRetention = 1 - (state.gpuFailureRate / 100);
    const annualRetention = annualPvRetention * annualGpuRetention;
    let capacitySum = 0;
    for (let year = 0; year < state.years; year++) {
        capacitySum += Math.pow(annualRetention, year);
    }
    const avgCapacityFactor = capacitySum / state.years;
    const sunlightAdjustedFactor = avgCapacityFactor * state.sunFraction;
    const requiredInitialPowerW = derived.TARGET_POWER_W / sunlightAdjustedFactor;
    const massPerSatelliteKg = (state.satellitePowerKW * 1000) / state.specificPowerWPerKg;
    const satelliteCount = Math.ceil(requiredInitialPowerW / (state.satellitePowerKW * 1000));
    const totalMassKg = satelliteCount * massPerSatelliteKg;
    const hardwareCost = state.satelliteCostPerW * (satelliteCount * state.satellitePowerKW * 1000);
    const launchCost = state.launchCostPerKg * totalMassKg;
    const opsCost = hardwareCost * constants.ORBITAL_OPS_FRAC;
    const gpuReplacementCost = 0; // failures are irrecoverable on orbit
    const nreCost = state.nreCost * 1e6;
    const totalCost = hardwareCost + launchCost + opsCost + nreCost;
    const energyMWh = derived.TARGET_POWER_MW * totalHours;
    const costPerW = totalCost / derived.TARGET_POWER_W;
    const lcoe = totalCost / energyMWh;
    const arrayPerSatelliteM2 = constants.STARLINK_ARRAY_M2 * (state.satellitePowerKW / constants.STARLINK_POWER_KW);
    const arrayAreaM2 = satelliteCount * arrayPerSatelliteM2;
    const starshipLaunches = Math.ceil(totalMassKg / constants.STARSHIP_PAYLOAD_KG);
    const degradationMargin = (satelliteCount * state.satellitePowerKW * 1000 / derived.TARGET_POWER_W - 1) * 100;
    return { ... };
}
```

### Baseline numeric trace
| Step | Result | Validation |
| --- | --- | --- |
| Average capacity retention | 0.79852 | Product of PV (97.5%) and GPU (91%) retention over 5 yrs
| Required initial power | 1.2779 GW | 1 GW / (0.79852 × 0.98)
| Satellite count | 47,329 | Ceiling(1.2779 GW / 27 kW)
| Mass per satellite | 739.7 kg | 27,000 W / 36.5 W·kg⁻¹
| Total mass to LEO | 35.01 Mkg | 47,329 × 739.7 kg
| Hardware cost | $28.11 B | $22/W × 1.2779 GW
| Launch cost | $35.01 B | $1,000/kg × 35.01 Mkg
| GPU replacement | $0 | Replacements impossible on orbit
| NRE | $0.50 B | 500 M USD slider (converted from millions)
| Total program cost | $63.91 B | Sum of all contributions
| Cost per delivered watt | $63.91/W | $63.91 B / 1 GW
| LCOE | $1,459/MWh | $63.91 B / 43.8 M MWh
| Degradation margin | 27.79% | (1.2779 GW / 1 GW − 1)
| Starship launches | 351 flights | 35.01 Mkg / 100 t per launch
| Array area | 5.49 km² | 47,329 × 116 m²

### Observations
- Launch spending (54.8%) now dominates the hardware bill (44.0%), so any launch-cost optimism directly drives total program cost.
- GPU attrition is treated like PV degradation, forcing a 27.8% overbuild up front and increasing required launches from 294 → 351.
- The model still sizes solely for average power; no explicit battery, thermal, or interconnect mass penalties are included, so results remain optimistic relative to a full orbital compute stack.
- Starship propellant bookkeeping (276 M gal LOX, 265 M gal CH₄) matches 351 launches × manifest propellant per `constants` and is internally consistent.

## Terrestrial Cost Model Review
The terrestrial pathway lives in `calculateTerrestrial()`:
```288:392:static/js/math.js
const powerGenCostPerW = state.gasTurbineCapexPerKW * state.pue / 1000;
const powerGenCost = powerGenCostPerW * derived.TARGET_POWER_W;
const electricalCost = state.electricalCostPerW * derived.TARGET_POWER_W;
const mechanicalCost = state.mechanicalCostPerW * derived.TARGET_POWER_W;
const civilCost = state.civilCostPerW * derived.TARGET_POWER_W;
const networkCost = state.networkCostPerW * derived.TARGET_POWER_W;
const infraCapex = powerGenCost + electricalCost + mechanicalCost + civilCost + networkCost;
const energyMWh = derived.TARGET_POWER_MW * totalHours * state.capacityFactor;
const generationMWh = energyMWh * state.pue;
const fuelCostPerMWh = state.heatRateBtuKwh * state.gasPricePerMMBtu / 1000;
const fuelCostTotal = fuelCostPerMWh * generationMWh;
const totalCost = infraCapex + fuelCostTotal;
const costPerW = totalCost / derived.TARGET_POWER_W;
const lcoe = totalCost / energyMWh;
const gasConsumptionBCF = generationMWh * 1000 * state.heatRateBtuKwh / (constants.BTU_PER_CF * constants.CF_PER_BCF);
const totalGenerationMW = derived.TARGET_POWER_MW * state.pue;
const turbineCount = Math.ceil(totalGenerationMW / constants.GE_7HA_POWER_MW);
```

### Baseline numeric trace
| Bucket | Cost | Share |
| --- | --- | --- |
| Power generation | $1.74 B | 12.2% of capex (PUE-adjusted gas turbine + BOP)
| Electrical | $5.25 B | 36.9%
| Mechanical | $3.00 B | 21.1%
| Civil & shell | $2.50 B | 17.6%
| Network/facilities | $1.75 B | 12.3%
| **Infrastructure capex** | **$14.24 B** | 92.3% of total spend
| Fuel spend (5 yrs) | $1.19 B | 7.7% of total
| **Total program cost** | **$15.43 B** | Cost per watt = $15.43/W
| LCOE | $414/MWh | $15.43 B / 37.23 M MWh delivered
| Fuel cost per W-year | $0.28 | Matches $26.66/MWh × 1.2 PUE × 0.00876
| Turbine count | 3 × GE 7HA | 1.2 GW generation vs 430 MW nameplate per unit
| Gas consumption | 277 BCF | 44.676 TWh gross × 6.2 MMBtu/MWh / 1e3 Btu/CF

### Observations
- The cost stack intentionally excludes fixed O&M beyond fuel; if added (~$5/MWh), the LCOE would rise modestly but not close the orbital gap.
- Infrastructure costs dwarf fuel over a five-year horizon, so gas-price risk mostly affects opex tail rather than the headline cost per watt.
- Facility capex per watt (14.24 $/W) matches the sum of the five cited buckets, validating the techno-economic ratios.

## Scenario Sweep (non-default set points)
Full JSON output: `audit/setpoint_runs.json`. Key metrics:

| Scenario | Orbital $/W | Orbital LCOE ($/MWh) | Starship flights | Terrestrial $/W | Terrestrial LCOE ($/MWh) |
| --- | --- | --- | --- | --- | --- |
| Baseline | 63.91 | 1,459 | 351 | 15.43 | 414 |
| Orbital – optimistic Starship | 21.88 | 499 | 209 | 15.43 | 414 |
| Orbital – pessimistic | 154.76 | 3,533 | 541 | 15.43 | 414 |
| Terrestrial – high gas ($8/MMBtu) | 63.91 | 1,459 | 351 | 16.60 | 446 |
| Terrestrial – low CF (0.60, PUE 1.3) | 63.91 | 1,459 | 351 | 15.44 | 588 |
| 2 GW scale-up (7 yrs) | 60.06 | 979 | 779 | 16.09 | 292 |

### Scenario insights
- Even after stacking optimistic orbital assumptions (200 $/kg launch, 55 W/kg buses, 35 kW sats, gentler degradation), cost per watt bottoms out at $21.88—still ~42% higher than terrestrial capex—and needs 209 Starship flights.
- Pessimistic orbital inputs explode the budget: 541 launches, $155/W, and $3.5k/MWh LCOE due to compounded degradation plus higher launch/hardware costs.
- Terrestrial economics remain comparatively insensitive; doubling gas cost to $8/MMBtu only raises cost per watt by $1.17 (7.5%) and LCOE by $32/MWh.
- Low capacity factor punishes terrestrial LCOE (energy denominator shrinks) but barely moves cost per watt because capex is unchanged—consistent with expectations.
- Scaling to 2 GW with a longer life still leaves orbital LCOE at $979/MWh versus $292/MWh on Earth, even before considering the 779-launch logistics burden.

## Sanity Checks (high-level)
- **Mass-to-orbit feasibility:** 35.0 million kg now requires 351 Starship launches (100 t each). At a sustained rate of 60 launches/year, this single program would still monopolize the manifest for nearly six years—highlighting logistics strain beyond pure cost.
- **Array area plausibility:** 47,329 satellites × 116 m² per V2 Mini array yields 5.49 km² of deployed PV/radiator surface, matching the engineering outputs and aligning with known Starlink geometries.
- **Energy accounting:** Orbital energy tally (43.8 million MWh for 1 GW × 5 yrs) equals the terrestrial IT-load energy (37.23 million MWh) once the 0.85 capacity factor is applied, confirming both models share a consistent load target.
- **Fuel burn realism:** 277 BCF over five years implies 55.4 BCF/yr, ~0.14% of US annual natural gas production—large but within the throughput of a single interstate pipeline, so the terrestrial supply assumption is credible.
- **Cost comparison vs market:** A $414/MWh LCOE for the terrestrial NGCC-powered datacenter is ~10× higher than wholesale electricity because the analysis allocates the entire facility capex to “power production.” This conservative framing still undercuts orbital solutions by ~4× on cost per watt and LCOE.

## Issues & Variances
1. **Static HTML numbers diverge from model outputs:** The placeholder figures baked into `templates/space-datacenters.html` (e.g., `$31.2B` orbital total, `$14.8B` terrestrial) no longer match the current math engine (>$63B orbital). The JavaScript overwrites these at runtime, but users with scripting disabled would see stale values. Recommend syncing or generating these values server-side to avoid audit drift.
2. **Legacy `gpuReplacementCost` field:** The property now always returns zero (failures are irrecoverable and handled via sizing). Consider renaming or hiding it in the UI so readers don’t assume orbital ops budgets cover swaps that cannot occur.
3. **Terrestrial O&M exclusions:** Fixed O&M (labor, insurance) and financing are omitted, which understates terrestrial costs by ~5–10%. Given the magnitude of the orbital premium, this does not flip the conclusion but is worth documenting.

No arithmetic defects were found inside `calculateOrbital` or `calculateTerrestrial`; recomputation via Python (`temp/check_numbers.py`) matched the Node outputs to machine precision.

## Artifacts Created
- `temp/audit_plan.md` – planning notes per workspace instructions.
- `temp/run_setpoints.js` – scenario harness for the audit.
- `audit/setpoint_runs.json` – raw outputs for six audited scenarios.
- `audit/third_party_audit.md` – this report.

## Conclusion
All orbital and terrestrial economic calculations audit cleanly—the formulas align with their documented assumptions, and independent recomputation reproduces every displayed value. Scenario sweeps confirm the model reacts monotonically to key inputs, and even generous orbital assumptions fail to reach terrestrial economics due to the overwhelming launch mass requirement. The primary variance is stale placeholder numbers in the HTML template; updating or auto-generating those figures will keep external narratives synchronized with the audited math. No other calculation defects were observed.
