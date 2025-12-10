"""
Flask application for Space vs Gas Power Generation Cost Analysis
Engineering-grade interactive infographic with backend preferences editor
"""

from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# Default constants (matches math.js)
DEFAULT_CONSTANTS = {
    # System target
    "TARGET_POWER_MW": 1000,
    "HOURS_PER_YEAR": 8760,
    
    # Starlink V2 Mini reference satellite
    "SPECIFIC_POWER_W_PER_KG": 45,
    "STARLINK_MASS_KG": 600,
    "STARLINK_POWER_KW": 27,
    "STARLINK_ARRAY_M2": 105,
    
    # Launch vehicle
    "STARSHIP_PAYLOAD_KG": 100000,
    "STARSHIP_LOX_GAL_PER_LAUNCH": 787000,
    "STARSHIP_METHANE_GAL_PER_LAUNCH": 755000,
    
    # NatGas plant
    "NGCC_ACRES": 30,
    "NGCC_HEAT_RATE_BTU_KWH": 6370,
    "GE_7HA_POWER_MW": 430,
    "BTU_PER_CF": 1000,
    "CF_PER_BCF": 1e9,
    
    # Cost fractions - Orbital
    "ORBITAL_OVERHEAD_FRAC": 0.05,
    "ORBITAL_MAINTENANCE_FRAC": 0.03,
    "ORBITAL_COMMS_FRAC": 0.02,
    
    # Cost fractions - NatGas
    "NATGAS_OVERHEAD_FRAC": 0.04,
    "NATGAS_MAINTENANCE_FRAC": 0.03,
    "NATGAS_COMMS_FRAC": 0.01
}

# Constant metadata for the editor
CONSTANT_METADATA = {
    "TARGET_POWER_MW": {"label": "Target Power", "unit": "MW", "category": "system"},
    "HOURS_PER_YEAR": {"label": "Hours per Year", "unit": "hrs", "category": "system"},
    
    "SPECIFIC_POWER_W_PER_KG": {"label": "Specific Power", "unit": "W/kg", "category": "orbital"},
    "STARLINK_MASS_KG": {"label": "Satellite Mass (V2 Mini)", "unit": "kg", "category": "orbital"},
    "STARLINK_POWER_KW": {"label": "Satellite Power (V2 Mini)", "unit": "kW", "category": "orbital"},
    "STARLINK_ARRAY_M2": {"label": "Satellite Array Area", "unit": "m²", "category": "orbital"},
    "STARSHIP_PAYLOAD_KG": {"label": "Starship Payload to LEO", "unit": "kg", "category": "orbital"},
    "STARSHIP_LOX_GAL_PER_LAUNCH": {"label": "LOX per Starship Launch", "unit": "gal", "category": "orbital"},
    "STARSHIP_METHANE_GAL_PER_LAUNCH": {"label": "Methane per Starship Launch", "unit": "gal", "category": "orbital"},
    "ORBITAL_OVERHEAD_FRAC": {"label": "Overhead Fraction", "unit": "%", "category": "orbital", "is_percent": True},
    "ORBITAL_MAINTENANCE_FRAC": {"label": "Maintenance Fraction", "unit": "%", "category": "orbital", "is_percent": True},
    "ORBITAL_COMMS_FRAC": {"label": "Communications Fraction", "unit": "%", "category": "orbital", "is_percent": True},
    
    "NGCC_ACRES": {"label": "Plant Footprint", "unit": "acres", "category": "natgas"},
    "NGCC_HEAT_RATE_BTU_KWH": {"label": "Heat Rate", "unit": "BTU/kWh", "category": "natgas"},
    "GE_7HA_POWER_MW": {"label": "GE 7HA.03 Turbine Power", "unit": "MW", "category": "natgas"},
    "BTU_PER_CF": {"label": "BTU per Cubic Foot", "unit": "BTU/cf", "category": "natgas"},
    "CF_PER_BCF": {"label": "Cubic Feet per BCF", "unit": "cf", "category": "natgas"},
    "NATGAS_OVERHEAD_FRAC": {"label": "Overhead Fraction", "unit": "%", "category": "natgas", "is_percent": True},
    "NATGAS_MAINTENANCE_FRAC": {"label": "Maintenance Fraction", "unit": "%", "category": "natgas", "is_percent": True},
    "NATGAS_COMMS_FRAC": {"label": "Communications Fraction", "unit": "%", "category": "natgas", "is_percent": True}
}

def get_constants_path():
    return os.path.join(app.static_folder, 'constants.json')

def load_constants():
    path = get_constants_path()
    if os.path.exists(path):
        with open(path, 'r') as f:
            saved = json.load(f)
            # Merge with defaults to ensure all keys exist
            return {**DEFAULT_CONSTANTS, **saved}
    return DEFAULT_CONSTANTS.copy()

def save_constants(constants):
    path = get_constants_path()
    with open(path, 'w') as f:
        json.dump(constants, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preferences')
def preferences():
    return render_template('preferences.html')

@app.route('/api/references')
def get_references():
    refs_path = os.path.join(app.static_folder, 'references.json')
    with open(refs_path, 'r') as f:
        refs = json.load(f)
    return jsonify(refs)

@app.route('/api/constants', methods=['GET'])
def get_constants():
    constants = load_constants()
    return jsonify({
        'constants': constants,
        'metadata': CONSTANT_METADATA
    })

@app.route('/api/constants', methods=['POST'])
def update_constants():
    new_constants = request.json
    current = load_constants()
    current.update(new_constants)
    save_constants(current)
    return jsonify({'success': True, 'constants': current})

@app.route('/api/constants/reset', methods=['POST'])
def reset_constants():
    save_constants(DEFAULT_CONSTANTS)
    return jsonify({'success': True, 'constants': DEFAULT_CONSTANTS})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
