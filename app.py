"""
Andrew McCalip's Personal Site
Flask application for essays and interactive analyses
"""

from flask import Flask, render_template
import json
import os

app = Flask(__name__)

"""
IMPORTANT NOTE ON "CONSTANTS"
----------------------------
The interactive model's mathematical source of truth is `static/js/math.js`.

This server-side `DEFAULT_CONSTANTS` dict previously powered a constants editor.
The project no longer exposes a preferences UI or JSON API; constants are configured
in code, and these defaults are kept for reference/consistency.

To avoid "split brain" bugs, the keys + defaults here intentionally mirror the
`constants` object in `static/js/math.js`. The frontend now loads these values
and applies them via `CostModel.setConstants(...)` on page load.
"""

# Default constants for Space Datacenters analysis (mirrors `static/js/math.js`)
DEFAULT_CONSTANTS = {
    # System / global
    "TARGET_POWER_MW": 1000,  # Legacy (the model primarily uses state.targetGW)
    "HOURS_PER_YEAR": 8760,

    # Starlink reference satellite (V2 Mini default)
    "STARLINK_MASS_KG": 740,
    "STARLINK_POWER_KW": 27,
    "STARLINK_ARRAY_M2": 116,

    # Launch vehicle
    "STARSHIP_PAYLOAD_KG": 100000,
    "STARSHIP_LOX_GAL_PER_LAUNCH": 787000,
    "STARSHIP_METHANE_GAL_PER_LAUNCH": 755000,

    # NatGas plant (engineering outputs + reference values)
    "NGCC_ACRES": 30,
    "NGCC_HEAT_RATE_BTU_KWH": 6370,
    "GE_7HA_POWER_MW": 430,
    "BTU_PER_CF": 1000,
    "CF_PER_BCF": 1e9,

    # Cost fractions
    "ORBITAL_OPS_FRAC": 0.01,
    "NATGAS_OVERHEAD_FRAC": 0.04,
    "NATGAS_MAINTENANCE_FRAC": 0.03,
    "NATGAS_COMMS_FRAC": 0.01,

    # Space environment (thermal model)
    "SOLAR_IRRADIANCE_W_M2": 1361,
    "EARTH_IR_FLUX_W_M2": 237,
    "EARTH_ALBEDO_FACTOR": 0.30,
    "T_SPACE_K": 3,
    "EARTH_RADIUS_KM": 6371.0,
}

CONSTANT_METADATA = {
    # System
    "TARGET_POWER_MW": {"label": "Target Power (legacy)", "unit": "MW", "category": "system"},
    "HOURS_PER_YEAR": {"label": "Hours per Year", "unit": "hrs", "category": "system"},

    # Orbital / reference spacecraft + launch
    "STARLINK_MASS_KG": {"label": "Starlink Satellite Mass (ref)", "unit": "kg", "category": "orbital"},
    "STARLINK_POWER_KW": {"label": "Starlink Satellite Power (ref)", "unit": "kW", "category": "orbital"},
    "STARLINK_ARRAY_M2": {"label": "Starlink Array Area (ref)", "unit": "m²", "category": "orbital"},
    "STARSHIP_PAYLOAD_KG": {"label": "Starship Payload to LEO", "unit": "kg", "category": "orbital"},
    "STARSHIP_LOX_GAL_PER_LAUNCH": {"label": "LOX per Starship Launch", "unit": "gal", "category": "orbital"},
    "STARSHIP_METHANE_GAL_PER_LAUNCH": {"label": "Methane per Starship Launch", "unit": "gal", "category": "orbital"},
    "ORBITAL_OPS_FRAC": {"label": "Orbital Ops Fraction (of hardware/yr)", "unit": "%", "category": "orbital", "is_percent": True},

    # Space environment / thermal (kept under "orbital" so preferences UI can render it)
    "SOLAR_IRRADIANCE_W_M2": {"label": "Solar Irradiance (AM0)", "unit": "W/m²", "category": "orbital"},
    "EARTH_IR_FLUX_W_M2": {"label": "Earth IR Flux (avg)", "unit": "W/m²", "category": "orbital"},
    "EARTH_ALBEDO_FACTOR": {"label": "Earth Albedo Factor", "unit": "", "category": "orbital"},
    "T_SPACE_K": {"label": "Deep Space Sink Temp", "unit": "K", "category": "orbital"},
    "EARTH_RADIUS_KM": {"label": "Earth Radius", "unit": "km", "category": "orbital"},

    # NatGas
    "NGCC_ACRES": {"label": "Plant Footprint", "unit": "acres", "category": "natgas"},
    "NGCC_HEAT_RATE_BTU_KWH": {"label": "Reference Heat Rate", "unit": "BTU/kWh", "category": "natgas"},
    "GE_7HA_POWER_MW": {"label": "GE 7HA.03 Turbine Power", "unit": "MW", "category": "natgas"},
    "BTU_PER_CF": {"label": "BTU per Cubic Foot", "unit": "BTU/cf", "category": "natgas"},
    "CF_PER_BCF": {"label": "Cubic Feet per BCF", "unit": "cf", "category": "natgas"},
    "NATGAS_OVERHEAD_FRAC": {"label": "Overhead Fraction", "unit": "%", "category": "natgas", "is_percent": True},
    "NATGAS_MAINTENANCE_FRAC": {"label": "Maintenance Fraction", "unit": "%", "category": "natgas", "is_percent": True},
    "NATGAS_COMMS_FRAC": {"label": "Communications Fraction", "unit": "%", "category": "natgas", "is_percent": True},
}

def get_constants_path():
    return os.path.join(app.static_folder, 'constants.json')

def load_constants():
    path = get_constants_path()
    if os.path.exists(path):
        with open(path, 'r') as f:
            saved = json.load(f)
            return {**DEFAULT_CONSTANTS, **saved}
    return DEFAULT_CONSTANTS.copy()

def save_constants(constants):
    path = get_constants_path()
    with open(path, 'w') as f:
        json.dump(constants, f, indent=2)

# ==========================================
# ROUTES
# ==========================================

@app.route('/')
def index():
    """Landing page for andrewmccalip.com"""
    return render_template('index.html')

@app.route('/space-datacenters')
def space_datacenters():
    """Space Datacenters analysis page"""
    return render_template('space-datacenters.html')

@app.route('/quote-styles')
def quote_styles():
    """Temp page to preview quote styles"""
    return render_template('quote-styles.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
