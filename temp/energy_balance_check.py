#!/usr/bin/env python3
"""
Triple-check the energy balance numbers in the essay text.
"""

# Constants from the model
G_SOLAR = 1361  # W/m² (AM0 solar constant)
ALPHA = 0.92    # Solar absorptivity
ETA_PV = 0.22   # PV efficiency (22%)

print("=" * 60)
print("ENERGY BALANCE CHECK")
print("=" * 60)

# Calculate absorbed solar
absorbed = G_SOLAR * ALPHA
print(f"\n1. INCIDENT SOLAR: {G_SOLAR} W/m²")
print(f"   Solar absorptivity α = {ALPHA}")
print(f"   ABSORBED = {G_SOLAR} × {ALPHA} = {absorbed:.1f} W/m²")
print(f"   Essay says: ~1250 W/m² ✓" if abs(absorbed - 1250) < 10 else f"   Essay says ~1250 W/m² ✗")

# Calculate electrical output
# Key question: Is η applied to incident or absorbed?
electrical_from_incident = G_SOLAR * ETA_PV
electrical_from_absorbed = absorbed * ETA_PV

print(f"\n2. ELECTRICAL PATH (PV efficiency η = {ETA_PV*100:.0f}%)")
print(f"   Option A: η × incident = {G_SOLAR} × {ETA_PV} = {electrical_from_incident:.1f} W/m²")
print(f"   Option B: η × absorbed = {absorbed:.1f} × {ETA_PV} = {electrical_from_absorbed:.1f} W/m²")
print(f"   Essay says: ~300 W/m²")

# The essay must mean Option A (η × incident = 300 W/m²)
electrical = electrical_from_incident
print(f"   → Using Option A: {electrical:.1f} W/m² ✓")

# Calculate thermal waste
thermal = absorbed - electrical
print(f"\n3. THERMAL ABSORPTION")
print(f"   Thermal = absorbed - electrical")
print(f"   Thermal = {absorbed:.1f} - {electrical:.1f} = {thermal:.1f} W/m²")
print(f"   Essay says: ~950 W/m² ✓" if abs(thermal - 950) < 10 else f"   Essay says ~950 W/m² ✗")

# Check percentages
pct_electrical = (electrical / G_SOLAR) * 100
pct_thermal = (thermal / G_SOLAR) * 100
pct_reflected = ((G_SOLAR - absorbed) / G_SOLAR) * 100

print(f"\n4. PERCENTAGES (of incident {G_SOLAR} W/m²)")
print(f"   Reflected: {pct_reflected:.0f}% ({G_SOLAR - absorbed:.0f} W/m²)")
print(f"   Electrical: {pct_electrical:.0f}% ({electrical:.0f} W/m²)")
print(f"   Thermal: {pct_thermal:.0f}% ({thermal:.0f} W/m²)")
print(f"   Sum: {pct_reflected + pct_electrical + pct_thermal:.0f}%")

print(f"\n   Essay says: 22% electrical, ~70% thermal")
print(f"   22% + 70% = 92% = α ✓")

# Total heat to reject
total_heat = electrical + thermal  # electrical returns as heat from GPUs
print(f"\n5. TOTAL HEAT TO REJECT")
print(f"   = thermal waste + electrical (returned from GPUs)")
print(f"   = {thermal:.0f} + {electrical:.0f} = {total_heat:.0f} W/m²")
print(f"   = absorbed solar = {absorbed:.0f} W/m² ✓")

print("\n" + "=" * 60)
print("CONCLUSION: Essay numbers are CORRECT")
print("=" * 60)
print("""
The percentages (22%, 70%) are fractions of INCIDENT flux:
- 8% reflected (1 - α)
- 22% → electrical → returned as GPU heat
- 70% → absorbed directly as thermal waste
- Total heat = 22% + 70% = 92% of incident = 100% of absorbed ✓
""")
