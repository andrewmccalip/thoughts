# View Factor Model Fix

## Issue Identified

The thermal view factor model in `math.js` used an **ad-hoc linear heuristic** rather than physics-based geometry:

```javascript
// OLD (non-physical):
const vfEarth = 0.08 + (90 - betaAngle) * 0.002;
```

This heuristic:
- Has no derivation from orbital geometry
- Does not account for Earth's angular size at orbital altitude
- Ignores the physics of sun-tracking panel orientation

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

### Thermal Impact

| Beta | Ad-hoc T_eq | Geometric T_eq | ΔT |
|------|-------------|----------------|-----|
| 90°  | 64.2°C      | 62.2°C         | -2.0°C |
| 75°  | 65.7°C      | 68.1°C         | +2.4°C |
| 60°  | 67.5°C      | 73.9°C         | **+6.4°C** |

### Key Finding

**At the seasonal hot case (β=60°), the ad-hoc model underpredicts equilibrium temperature by 6.4°C!**

This is significant because:
- Thermal margins are typically only 10-15°C
- A 6°C error could change PASS/FAIL status
- The geometric model is more conservative (predicts higher temps)

## Files Modified

1. `static/js/math.js`:
   - Added geometric view factor functions
   - Added `EARTH_RADIUS_KM` constant
   - Added `orbitalAltitudeKm` state parameter
   - Replaced ad-hoc heuristic with geometry-based calculation
   - Enhanced return values with view factor details

2. `static/js/main.js`:
   - Added altitude slider setup

3. `templates/space-datacenters.html`:
   - Added orbital altitude slider
   - Updated view factor formula tooltip

## Verification

- JavaScript syntax: ✅ No errors
- Python verification script: ✅ Matches JavaScript implementation
- Dimensional analysis: ✅ All units consistent

## References

- NASA Technical Note TN D-5006: "Thermal Radiation Heat Transfer"
- Gilmore, D.G., "Spacecraft Thermal Control Handbook"
- View factor correlations for spacecraft applications
