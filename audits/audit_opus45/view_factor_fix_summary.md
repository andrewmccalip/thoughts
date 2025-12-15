# View Factor Model Fix

## Issues Identified

### Issue 1: Ad-hoc View Factor Heuristic

The thermal view factor model in `math.js` used an **ad-hoc linear heuristic** rather than physics-based geometry:

```javascript
// OLD (non-physical):
const vfEarth = 0.08 + (90 - betaAngle) * 0.002;
```

This heuristic:
- Has no derivation from orbital geometry
- Does not account for Earth's angular size at orbital altitude
- Ignores the physics of sun-tracking panel orientation

### Issue 2: Incorrect Earth IR Formula (2x Overcounting)

The Earth IR calculation incorrectly multiplied `vfTotal × (εPV + εRad)`:

```javascript
// WRONG - 2x overcounting:
const qEarthIR = EARTH_IR * vfTotal * (epsilonPV + epsilonRad) * areaM2;
```

Each side should use its OWN view factor and emissivity (Kirchhoff's law):

```javascript
// CORRECT:
const qEarthIR = EARTH_IR * (vfSideA * epsilonPV + vfSideB * epsilonRad) * areaM2;
```

### Issue 3: Incorrect Albedo Formula

Albedo was applied using vfTotal, but only the PV side (Side A) has high solar absorptivity. The radiator side (Side B) is white paint with α ≈ 0.1-0.2:

```javascript
// WRONG:
const qAlbedo = SOLAR * ALBEDO * vfTotal * ... * alphaPV * areaM2;

// CORRECT - only PV side absorbs:
const qAlbedo = SOLAR * ALBEDO * vfSideA * ... * alphaPV * areaM2;
```

## Physics Background

### Earth View Factor from LEO

For a spacecraft at altitude *h* above Earth (radius *Rₑ*):

1. **Earth angular radius**: θ = arcsin(Rₑ / (Rₑ + h))
   - At 550 km (Starlink): θ = 67.0°
   - Earth subtends a HUGE solid angle from LEO!

2. **Maximum view factor** (nadir-pointing plate):
   - VF_nadir = sin²(θ) = (Rₑ / (Rₑ + h))²
   - At 550 km: VF_nadir = 0.847 (84.7%!)

3. **Tilted plate view factor**:
   - VF(γ) ≈ VF_nadir × cos(γ)
   - Where γ is the angle between plate normal and nadir

### Sun-Tracking Panel Geometry

For a sun-tracking solar panel at orbit beta angle β:
- Panel normal always points toward the sun
- At β = 90° (terminator): Panel is mostly edge-on to Earth
- At β = 60° (seasonal limit): Panel tilts to see more Earth
- View factor varies around the orbit and must be time-averaged

## Fix Applied

### New Code Structure in `math.js`

```javascript
// 1. Earth angular radius
function earthAngularRadius(altitudeKm) {
    return Math.asin(EARTH_RADIUS_KM / (EARTH_RADIUS_KM + altitudeKm));
}

// 2. Maximum (nadir) view factor
function nadirViewFactor(altitudeKm) {
    const theta = earthAngularRadius(altitudeKm);
    return Math.pow(Math.sin(theta), 2);
}

// 3. Tilted plate view factor (with minimum floor)
function tiltedPlateViewFactor(altitudeKm, tiltRad) {
    const vfNadir = nadirViewFactor(altitudeKm);
    const cosTilt = Math.cos(tiltRad);
    if (cosTilt <= 0) return vfNadir * 0.05;  // Floor for edge-on
    return vfNadir * cosTilt;
}

// 4. Orbit-averaged view factors for sun-tracking panel
function sunTrackingPanelViewFactors(altitudeKm, betaDeg) {
    // Integrates view factor over one orbit
    // Returns {vfSideA, vfSideB, vfTotal}
}
```

### Additional Changes

1. Added `EARTH_RADIUS_KM = 6371.0` to constants
2. Added `orbitalAltitudeKm` parameter (default 550 km)
3. Added altitude slider to UI (400-1200 km range)
4. Updated return values to include detailed view factor breakdown

## Impact Analysis

### View Factor Comparison (550 km altitude)

| Beta | Ad-hoc VF | Geometric VF | Ratio |
|------|-----------|--------------|-------|
| 90°  | 0.080     | 0.008        | 0.1x  |
| 85°  | 0.090     | 0.089        | 1.0x  |
| 80°  | 0.100     | 0.136        | 1.4x  |
| 75°  | 0.110     | 0.182        | 1.7x  |
| 70°  | 0.120     | 0.227        | 1.9x  |
| 65°  | 0.130     | 0.270        | 2.1x  |
| 60°  | 0.140     | 0.312        | 2.2x  |

### Corrected Thermal Results

| Beta | VF_A | VF_B | Q_IR (MW) | Q_alb (MW) | T_eq |
|------|------|------|-----------|------------|------|
| 90°  | 0.008 | 0.000 | 1.7 | 0.0 | 62.1°C |
| 85°  | 0.045 | 0.045 | 18.5 | 1.5 | 63.3°C |
| 80°  | 0.068 | 0.068 | 28.2 | 4.4 | 64.2°C |
| 75°  | 0.091 | 0.091 | 37.7 | 8.8 | 65.1°C |
| 70°  | 0.113 | 0.113 | 47.0 | 14.6 | 66.1°C |
| 65°  | 0.135 | 0.135 | 56.0 | 21.5 | 67.1°C |
| 60°  | 0.156 | 0.156 | 64.7 | 29.3 | **68.1°C** |

### Key Findings

1. **Temperature Range**: 62°C (terminator) to 68°C (seasonal hot)
2. **ΔT Range**: ~6°C from coldest to hottest orbit
3. **Earth Loads**: ~7% of total heat at β=60°
4. **Solar Dominates**: Solar absorption is >90% of thermal budget

### Bug Impact Analysis

The 2x overcounting bugs in Earth IR and albedo would have predicted:
- ~37 MW too much Earth IR at β=60°
- ~29 MW too much albedo at β=60°
- Equilibrium temperature ~5°C too high (false positive for thermal failure)

## Files Modified

1. `static/js/math.js`:
   - Added geometric view factor functions:
     - `earthAngularRadius(altitudeKm)`
     - `nadirViewFactor(altitudeKm)`
     - `tiltedPlateViewFactor(altitudeKm, tiltRad)`
     - `sunTrackingPanelViewFactors(altitudeKm, betaDeg)`
   - Added `EARTH_RADIUS_KM` constant (6371.0 km)
   - Added `orbitalAltitudeKm` state parameter (default 550 km)
   - **Fixed Earth IR formula**: Now uses per-side view factors
   - **Fixed Albedo formula**: Now uses only Side A (PV side)
   - Enhanced return values with `vfSideA`, `vfSideB`, `vfNadirMax`

2. `static/js/main.js`:
   - Added altitude slider setup

3. `templates/space-datacenters.html`:
   - Added orbital altitude slider (400-1200 km range)
   - Updated view factor formula tooltip to describe geometry-based calculation

## Verification

- JavaScript syntax: ✅ No errors
- Python verification script: ✅ Matches JavaScript implementation
- Dimensional analysis: ✅ All units consistent

## References

- NASA Technical Note TN D-5006: "Thermal Radiation Heat Transfer"
- Gilmore, D.G., "Spacecraft Thermal Control Handbook"
- View factor correlations for spacecraft applications
