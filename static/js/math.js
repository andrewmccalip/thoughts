/**
 * Orbital Solar vs NatGas Cost Analysis - Math Engine
 * 
 * All constants and calculations are defined here.
 * This file is the single source of truth for the model.
 */

const CostModel = (function() {
    'use strict';

    // ==========================================
    // CONSTANTS (editable via preferences)
    // ==========================================
    
    let constants = {
        // System target
        TARGET_POWER_MW: 1000,              // 1 GW nameplate capacity
        HOURS_PER_YEAR: 8760,               // 365 × 24
        
        // Starlink V2 Mini reference satellite
        SPECIFIC_POWER_W_PER_KG: 45,        // W/kg specific power
        STARLINK_MASS_KG: 600,              // V2 Mini mass per satellite
        STARLINK_POWER_KW: 27,              // V2 Mini power output per satellite
        STARLINK_ARRAY_M2: 105,             // V2 Mini array area per satellite
        
        // Launch vehicle
        STARSHIP_PAYLOAD_KG: 100000,        // Starship LEO payload capacity
        STARSHIP_LOX_GAL_PER_LAUNCH: 787000,    // ~3,400 metric tons LOX
        STARSHIP_METHANE_GAL_PER_LAUNCH: 755000, // ~1,200 metric tons CH4
        
        // NatGas plant
        NGCC_ACRES: 30,                     // Plant footprint
        NGCC_HEAT_RATE_BTU_KWH: 6370,       // Modern NGCC heat rate
        GE_7HA_POWER_MW: 430,               // GE 7HA.03 turbine output
        BTU_PER_CF: 1000,                   // BTU per cubic foot of natural gas
        CF_PER_BCF: 1e9,                    // Cubic feet per billion cubic feet
        
        // Cost fractions - Orbital
        ORBITAL_OVERHEAD_FRAC: 0.05,
        ORBITAL_MAINTENANCE_FRAC: 0.03,
        ORBITAL_COMMS_FRAC: 0.02,
        
        // Cost fractions - NatGas
        NATGAS_OVERHEAD_FRAC: 0.04,
        NATGAS_MAINTENANCE_FRAC: 0.03,
        NATGAS_COMMS_FRAC: 0.01
    };

    // ==========================================
    // SLIDER STATE (user-adjustable parameters)
    // ==========================================
    
    let state = {
        // Shared parameters
        years: 5,
        
        // Orbital parameters
        launchCostPerKg: 1000,
        satelliteCostPerW: 9,
        specificPowerWPerKg: 45,  // W/kg - user adjustable
        sunFraction: 0.80,
        
        // NatGas parameters
        capexPerKW: 898,
        fuelCostPerMWh: 25,
        omCostPerMWh: 6,
        landCostPerAcre: 50
    };
    
    // Satellite specific power presets (W/kg)
    const SATELLITE_PRESETS = {
        ISS: 3,           // ISS solar arrays ~3 W/kg (old tech, heavy structure)
        V1: 25,           // Starlink V1 ~25 W/kg
        V2_MINI: 45,      // Starlink V2 Mini ~45 W/kg (current reference)
        V3: 70            // Starlink V3 projected ~70 W/kg
    };

    // ==========================================
    // DERIVED CONSTANTS
    // ==========================================
    
    function getDerived() {
        return {
            TARGET_POWER_W: constants.TARGET_POWER_MW * 1e6,
            TARGET_POWER_KW: constants.TARGET_POWER_MW * 1000
        };
    }

    // ==========================================
    // CALCULATIONS
    // ==========================================
    
    function calculateOrbital() {
        const derived = getDerived();
        const totalHours = state.years * constants.HOURS_PER_YEAR;
        
        // Mass required for target power at specific power (use state value, not constant)
        const totalMassKg = derived.TARGET_POWER_W / state.specificPowerWPerKg;
        
        // Satellite hardware cost: $/W × watts
        const hardwareCost = state.satelliteCostPerW * derived.TARGET_POWER_W;
        
        // Launch cost: $/kg × total kg
        const launchCost = state.launchCostPerKg * totalMassKg;
        
        // Base cost before overhead/maintenance/comms
        const baseCost = hardwareCost + launchCost;
        
        // Overhead, maintenance, communications
        const overheadCost = baseCost * constants.ORBITAL_OVERHEAD_FRAC;
        const maintenanceCost = baseCost * constants.ORBITAL_MAINTENANCE_FRAC;
        const commsCost = baseCost * constants.ORBITAL_COMMS_FRAC;
        
        // Total system cost
        const totalCost = baseCost + overheadCost + maintenanceCost + commsCost;
        
        // Energy output: power × hours × sun fraction
        const energyMWh = constants.TARGET_POWER_MW * totalHours * state.sunFraction;
        
        // Cost per watt
        const costPerW = totalCost / derived.TARGET_POWER_W;
        
        // Levelized cost of energy
        const lcoe = totalCost / energyMWh;
        
        // Engineering outputs
        const satelliteCount = Math.ceil(totalMassKg / constants.STARLINK_MASS_KG);
        const arrayAreaM2 = (derived.TARGET_POWER_W / (constants.STARLINK_POWER_KW * 1000)) * constants.STARLINK_ARRAY_M2;
        const arrayAreaKm2 = arrayAreaM2 / 1e6;
        const starshipLaunches = Math.ceil(totalMassKg / constants.STARSHIP_PAYLOAD_KG);
        const loxGallons = starshipLaunches * constants.STARSHIP_LOX_GAL_PER_LAUNCH;
        const methaneGallons = starshipLaunches * constants.STARSHIP_METHANE_GAL_PER_LAUNCH;
        
        return {
            totalMassKg,
            hardwareCost,
            launchCost,
            baseCost,
            overheadCost,
            maintenanceCost,
            commsCost,
            totalCost,
            energyMWh,
            costPerW,
            lcoe,
            satelliteCount,
            arrayAreaKm2,
            starshipLaunches,
            loxGallons,
            methaneGallons
        };
    }
    
    function calculateNatGas() {
        const derived = getDerived();
        const totalHours = state.years * constants.HOURS_PER_YEAR;
        
        // Capex: $/kW × kW
        const capexTotal = state.capexPerKW * derived.TARGET_POWER_KW;
        
        // Energy output: power × hours (continuous operation)
        const energyMWh = constants.TARGET_POWER_MW * totalHours;
        
        // Fuel cost: $/MWh × MWh
        const fuelCostTotal = state.fuelCostPerMWh * energyMWh;
        
        // O&M cost: $/MWh × MWh
        const omCostTotal = state.omCostPerMWh * energyMWh;
        
        // Land cost: $/acre × acres (convert from $k/acre)
        const landCostTotal = state.landCostPerAcre * 1000 * constants.NGCC_ACRES;
        
        // Base cost before overhead/maintenance/comms
        const baseCost = capexTotal + fuelCostTotal + omCostTotal + landCostTotal;
        
        // Overhead, maintenance, communications
        const overheadCost = baseCost * constants.NATGAS_OVERHEAD_FRAC;
        const maintenanceCost = baseCost * constants.NATGAS_MAINTENANCE_FRAC;
        const commsCost = baseCost * constants.NATGAS_COMMS_FRAC;
        
        // Total system cost
        const totalCost = baseCost + overheadCost + maintenanceCost + commsCost;
        
        // Cost per watt
        const costPerW = totalCost / derived.TARGET_POWER_W;
        
        // LCOE
        const lcoe = totalCost / energyMWh;
        
        // Engineering outputs
        const energyKWh = energyMWh * 1000;
        const totalBTU = energyKWh * constants.NGCC_HEAT_RATE_BTU_KWH;
        const gasConsumptionBCF = totalBTU / constants.BTU_PER_CF / constants.CF_PER_BCF;
        const turbineCount = Math.ceil(constants.TARGET_POWER_MW / constants.GE_7HA_POWER_MW);
        
        return {
            capexTotal,
            fuelCostTotal,
            omCostTotal,
            landCostTotal,
            baseCost,
            overheadCost,
            maintenanceCost,
            commsCost,
            totalCost,
            energyMWh,
            costPerW,
            lcoe,
            totalHours,
            gasConsumptionBCF,
            turbineCount
        };
    }
    
    function calculateBreakeven() {
        const derived = getDerived();
        const totalHours = state.years * constants.HOURS_PER_YEAR;
        const energyMWh = constants.TARGET_POWER_MW * totalHours;
        
        // NatGas costs
        const ngccCost = state.capexPerKW * derived.TARGET_POWER_KW 
            + state.fuelCostPerMWh * energyMWh 
            + state.omCostPerMWh * energyMWh 
            + state.landCostPerAcre * 1000 * constants.NGCC_ACRES;
        
        const hardwareCost = state.satelliteCostPerW * derived.TARGET_POWER_W;
        const mass = derived.TARGET_POWER_W / state.specificPowerWPerKg;
        
        return (ngccCost - hardwareCost) / mass;
    }

    // ==========================================
    // FORMATTING UTILITIES
    // ==========================================
    
    function formatCost(cost) {
        if (Math.abs(cost) >= 1e12) return `$${(cost / 1e12).toFixed(1)}T`;
        if (Math.abs(cost) >= 1e9) return `$${(cost / 1e9).toFixed(1)}B`;
        if (Math.abs(cost) >= 1e6) return `$${(cost / 1e6).toFixed(0)}M`;
        return `$${Math.round(cost).toLocaleString()}`;
    }
    
    function formatCostPerKg(cost) {
        if (cost < 0) return `−$${Math.abs(Math.round(cost)).toLocaleString()}/kg`;
        return `$${Math.round(cost).toLocaleString()}/kg`;
    }
    
    function formatMass(kg) {
        if (kg >= 1e6) return `${(kg / 1e6).toFixed(1)}M kg`;
        return `${Math.round(kg).toLocaleString()} kg`;
    }
    
    function formatEnergy(mwh) {
        if (mwh >= 1e6) return `${(mwh / 1e6).toFixed(1)} TWh`;
        return `${(mwh / 1e3).toFixed(1)} GWh`;
    }
    
    function formatLCOE(lcoe) {
        return `$${Math.round(lcoe)}/MWh`;
    }
    
    function formatHours(hours) {
        return `${hours.toLocaleString()} hrs`;
    }

    // ==========================================
    // PUBLIC API
    // ==========================================
    
    return {
        // Access constants
        getConstants: () => ({ ...constants }),
        setConstants: (newConstants) => {
            constants = { ...constants, ...newConstants };
        },
        
        // Access state
        getState: () => ({ ...state }),
        setState: (newState) => {
            state = { ...state, ...newState };
        },
        updateState: (key, value) => {
            state[key] = value;
        },
        
        // Satellite presets
        getSatellitePresets: () => ({ ...SATELLITE_PRESETS }),
        
        // Calculations
        calculateOrbital,
        calculateNatGas,
        calculateBreakeven,
        
        // Formatters
        formatCost,
        formatCostPerKg,
        formatMass,
        formatEnergy,
        formatLCOE,
        formatHours
    };
})();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CostModel;
}

