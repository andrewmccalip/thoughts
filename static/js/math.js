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
        
        // Starlink reference satellite (V2 Mini default)
        // Updated from Starlink techno-economic analysis
        STARLINK_MASS_KG: 740,              // V2 Mini mass per satellite
        STARLINK_POWER_KW: 27,              // V2 Mini power output per satellite (27 kW nameplate)
        STARLINK_ARRAY_M2: 116,             // V2 Mini array area per satellite
        
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
        
        // Orbital parameters (V2 Mini defaults from Starlink analysis)
        launchCostPerKg: 1000,
        satelliteCostPerW: 22,        // V2 Mini: ~$22/W (BOM at $800/kg)
        specificPowerWPerKg: 36.5,    // V2 Mini: 36.5 W/kg (27 kW / 740 kg)
        satellitePowerKW: 27,         // V2 Mini: 27 kW nameplate
        sunFraction: 0.98,            // Terminator orbit default
        cellDegradation: 2.5,         // % per year silicon cell degradation
        nreCost: 500,                 // NRE cost in millions ($500M default)
        
        // Terrestrial parameters - On-Site Gas Generation (xAI/Hyperscale style)
        // Source: Techno-Economic Analysis Report, EIA, Sargent & Lundy
        // Total Capex Target: ~$13.80/W (range $11.60-$16.00/W)
        
        // CAPEX buckets (5 categories from report)
        // 1. Power Generation: $1.30/W (9%) - Turbines, Gas Lateral, Tap
        gasTurbineCapexPerKW: 1100,    // Frame CCGT $/kW ($1,084-$1,420 range)
        
        // 2. Electrical Distribution: $5.25/W (38%) - Switchgear, Transformers, UPS, Gensets
        electricalCostPerW: 5.25,      // MV/LV switchgear, UPS (Li-ion), backup gensets, busway
        
        // 3. Mechanical/Cooling: $3.00/W (22%) - Chillers, CDUs, Piping, Towers
        mechanicalCostPerW: 3.0,       // DLC infrastructure, CDUs (~$21.5k/300kW), manifolds
        
        // 4. Civil & Shell: $2.50/W (18%) - Shell, Land, Site Prep, Roads
        civilCostPerW: 2.5,            // Land (~$244k/acre), building shell ($105-235/sqft)
        
        // 5. Networking/Fit-out: $1.75/W (13%) - Fiber Plant, Racks, Security, BMS
        networkCostPerW: 1.75,         // Dark fiber, structured cabling, racks, security
        
        // PUE
        pue: 1.2,                       // Liquid cooled efficiency
        
        // OPEX - Fuel (from report)
        gasPricePerMMBtu: 4.30,         // EIA 2025 forecast Henry Hub
        heatRateBtuKwh: 6200,           // Frame CCGT heat rate (6,200-6,560 range)
        capacityFactor: 0.85            // 85% capacity factor default
    };
    
    // Satellite presets from Starlink techno-economic analysis
    // Source: UK technical study, SpaceX filings, engineering estimates
    const SATELLITE_PRESETS = {
        // Specific power (W/kg) - nameplate solar power per kg of spacecraft mass
        SPECIFIC_POWER: {
            ISS: 3,           // ISS solar arrays ~3 W/kg (old tech, heavy structure)
            V1: 24.7,         // Starlink V1.x: 7 kW / 283 kg = 24.7 W/kg
            V2_MINI: 36.5,    // Starlink V2 Mini: 27 kW / 740 kg = 36.5 W/kg
            V3: 31.6          // Starlink V3: 60 kW / 1,900 kg = 31.6 W/kg (speculative)
        },
        // Hardware cost ($/W) - BOM cost normalized to solar power
        // Based on ~$800/kg manufacturing cost estimate
        COST_PER_W: {
            V1: 32,           // $230k / 7 kW ≈ $32/W
            V2_MINI: 22,      // $590k / 27 kW ≈ $22/W
            V3: 25            // $1.52M / 60 kW ≈ $25/W (speculative)
        },
        // Satellite power output (kW nameplate)
        POWER_KW: {
            V1: 7,            // 7 kW nameplate (30 m² array)
            V2_MINI: 27,      // 27 kW nameplate (116 m² array)
            V3: 60            // 60 kW nameplate (250 m² array, speculative)
        },
        // Mass per satellite (kg)
        MASS_KG: {
            V1: 283,          // v1.0/v1.5 average
            V2_MINI: 740,     // v2 mini
            V3: 1900          // v3 (speculative)
        },
        // Solar array area (m²)
        ARRAY_M2: {
            V1: 30,
            V2_MINI: 116,
            V3: 250           // speculative
        }
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
        
        // ========================================
        // DEGRADATION: Calculate capacity needed to maintain 1GW average
        // ========================================
        
        // Year-by-year degradation: capacity at year n = (1 - deg)^n
        // More accurate than linear approximation
        const annualRetention = 1 - (state.cellDegradation / 100);
        
        // Calculate average capacity factor over analysis period
        // Sum of geometric series: (1 + r + r^2 + ... + r^(n-1)) / n
        let capacitySum = 0;
        for (let year = 0; year < state.years; year++) {
            capacitySum += Math.pow(annualRetention, year);
        }
        const avgCapacityFactor = capacitySum / state.years;
        
        // To maintain TARGET_POWER average output, we need more initial capacity
        const requiredInitialPowerW = derived.TARGET_POWER_W / avgCapacityFactor;
        
        // ========================================
        // SATELLITE SIZING
        // ========================================
        
        // Each satellite produces satellitePowerKW at specific power (W/kg)
        // Mass per satellite = power / specific power
        const massPerSatelliteKg = (state.satellitePowerKW * 1000) / state.specificPowerWPerKg;
        
        // Number of satellites needed for required initial capacity
        const satelliteCount = Math.ceil(requiredInitialPowerW / (state.satellitePowerKW * 1000));
        
        // Total mass based on actual satellite count
        const totalMassKg = satelliteCount * massPerSatelliteKg;
        
        // Actual initial power (may be slightly higher due to rounding up satellites)
        const actualInitialPowerW = satelliteCount * state.satellitePowerKW * 1000;
        
        // ========================================
        // COSTS
        // ========================================
        
        // Satellite hardware cost: $/W × actual initial watts
        const hardwareCost = state.satelliteCostPerW * actualInitialPowerW;
        
        // Launch cost: $/kg × total kg
        const launchCost = state.launchCostPerKg * totalMassKg;
        
        // Base cost before overhead/maintenance/comms
        const baseCost = hardwareCost + launchCost;
        
        // O&M cost (as fraction of hardware)
        const omCost = hardwareCost * (constants.ORBITAL_OVERHEAD_FRAC + constants.ORBITAL_MAINTENANCE_FRAC + constants.ORBITAL_COMMS_FRAC);
        
        // NRE cost (non-recurring engineering)
        const nreCost = state.nreCost * 1e6;  // Convert from millions
        
        // Overhead, maintenance, communications
        const overheadCost = baseCost * constants.ORBITAL_OVERHEAD_FRAC;
        const maintenanceCost = baseCost * constants.ORBITAL_MAINTENANCE_FRAC;
        const commsCost = baseCost * constants.ORBITAL_COMMS_FRAC;
        
        // Total system cost (including NRE)
        const totalCost = baseCost + overheadCost + maintenanceCost + commsCost + nreCost;
        
        // ========================================
        // ENERGY OUTPUT
        // ========================================
        
        // Energy output: average power (1GW target) × hours × sun fraction
        // Degradation is already accounted for by launching extra capacity
        const energyMWh = constants.TARGET_POWER_MW * totalHours * state.sunFraction;
        
        // Cost per watt (of delivered average power, not initial capacity)
        const costPerW = totalCost / derived.TARGET_POWER_W;
        
        // Levelized cost of energy
        const lcoe = totalCost / energyMWh;
        
        // ========================================
        // ENGINEERING OUTPUTS
        // ========================================
        
        // Array area based on satellite count
        // Scale array area proportionally to satellite power vs reference
        const arrayPerSatelliteM2 = constants.STARLINK_ARRAY_M2 * (state.satellitePowerKW / constants.STARLINK_POWER_KW);
        const arrayAreaM2 = satelliteCount * arrayPerSatelliteM2;
        const arrayAreaKm2 = arrayAreaM2 / 1e6;
        
        const starshipLaunches = Math.ceil(totalMassKg / constants.STARSHIP_PAYLOAD_KG);
        const loxGallons = starshipLaunches * constants.STARSHIP_LOX_GAL_PER_LAUNCH;
        const methaneGallons = starshipLaunches * constants.STARSHIP_METHANE_GAL_PER_LAUNCH;
        
        // Degradation margin: how much extra capacity we're launching
        const degradationMargin = (actualInitialPowerW / derived.TARGET_POWER_W - 1) * 100;
        
        return {
            totalMassKg,
            hardwareCost,
            launchCost,
            omCost,
            nreCost,
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
            methaneGallons,
            avgCapacityFactor,
            degradationMargin,
            actualInitialPowerW,
            requiredInitialPowerW
        };
    }
    
    function calculateTerrestrial() {
        const derived = getDerived();
        const totalHours = state.years * constants.HOURS_PER_YEAR;
        
        // ========================================
        // CAPEX: 5 Buckets from Techno-Economic Report
        // Total Target: ~$13.80/W
        // ========================================
        
        // 1. Power Generation (9%): Gas Turbine + Balance of Plant
        // $/kW × PUE / 1000 = $/W of IT load
        const powerGenCostPerW = state.gasTurbineCapexPerKW * state.pue / 1000;
        const powerGenCost = powerGenCostPerW * derived.TARGET_POWER_W;
        
        // 2. Electrical Distribution (38%): Switchgear, Transformers, UPS, Gensets
        const electricalCost = state.electricalCostPerW * derived.TARGET_POWER_W;
        
        // 3. Mechanical/Cooling (22%): DLC, Chillers, CDUs, Piping
        const mechanicalCost = state.mechanicalCostPerW * derived.TARGET_POWER_W;
        
        // 4. Civil & Shell (18%): Land, Building Shell, Site Prep
        const civilCost = state.civilCostPerW * derived.TARGET_POWER_W;
        
        // 5. Networking/Fit-out (13%): Fiber Plant, Racks, Security, BMS
        const networkCost = state.networkCostPerW * derived.TARGET_POWER_W;
        
        // Total infrastructure capex
        const infraCapex = powerGenCost + electricalCost + mechanicalCost + civilCost + networkCost;
        
        // Facility capex per watt (all 5 buckets)
        const facilityCapexPerW = powerGenCostPerW + state.electricalCostPerW + 
                                   state.mechanicalCostPerW + state.civilCostPerW + state.networkCostPerW;
        
        // ========================================
        // OPEX: Fuel cost (NatGas CCGT)
        // ========================================
        
        // Energy output: IT power × hours × capacity factor
        const energyMWh = constants.TARGET_POWER_MW * totalHours * state.capacityFactor;
        
        // Total generation needed (IT load × PUE)
        const generationMWh = energyMWh * state.pue;
        
        // Fuel cost per MWh: heat rate × gas price
        // $/MWh = (BTU/kWh) × ($/MMBtu) / 1000
        const fuelCostPerMWh = state.heatRateBtuKwh * state.gasPricePerMMBtu / 1000;
        
        // Total fuel cost over analysis period
        const fuelCostTotal = fuelCostPerMWh * generationMWh;
        
        // ========================================
        // TOTAL
        // ========================================
        
        const totalCost = infraCapex + fuelCostTotal;
        const costPerW = totalCost / derived.TARGET_POWER_W;
        
        // LCOE (based on IT energy delivered)
        const lcoe = totalCost / energyMWh;
        
        // ========================================
        // Engineering outputs
        // ========================================
        const generationKWh = generationMWh * 1000;
        const totalBTU = generationKWh * state.heatRateBtuKwh;
        const gasConsumptionBCF = totalBTU / constants.BTU_PER_CF / constants.CF_PER_BCF;
        
        // Turbine count (H-class ~430 MW each)
        const totalGenerationMW = constants.TARGET_POWER_MW * state.pue;
        const turbineCount = Math.ceil(totalGenerationMW / constants.GE_7HA_POWER_MW);
        
        // Fuel cost per W-year (for display)
        const fuelCostPerWYear = fuelCostPerMWh * state.pue * 0.00876;
        
        return {
            // Capex breakdown (5 buckets)
            powerGenCost,
            powerGenCostPerW,
            electricalCost,
            mechanicalCost,
            civilCost,
            networkCost,
            infraCapex,
            facilityCapexPerW,
            
            // Opex
            fuelCostPerMWh,
            fuelCostTotal,
            fuelCostPerWYear,
            
            // Totals
            totalCost,
            energyMWh,
            generationMWh,
            costPerW,
            lcoe,
            totalHours,
            
            // Engineering
            gasConsumptionBCF,
            turbineCount,
            totalGenerationMW,
            capacityFactor: state.capacityFactor,
            pue: state.pue
        };
    }
    
    function calculateBreakeven() {
        const derived = getDerived();
        const totalHours = state.years * constants.HOURS_PER_YEAR;
        const energyMWh = constants.TARGET_POWER_MW * totalHours * state.capacityFactor;
        const generationMWh = energyMWh * state.pue;
        
        // Terrestrial costs (5 buckets from report)
        const powerGenCostPerW = state.gasTurbineCapexPerKW * state.pue / 1000;
        const infraCost = (powerGenCostPerW + state.electricalCostPerW + state.mechanicalCostPerW + 
                          state.civilCostPerW + state.networkCostPerW) * derived.TARGET_POWER_W;
        const fuelCostPerMWh = state.heatRateBtuKwh * state.gasPricePerMMBtu / 1000;
        const fuelCost = fuelCostPerMWh * generationMWh;
        const terrestrialCost = infraCost + fuelCost;
        
        // Calculate degradation-adjusted orbital capacity needed
        const annualRetention = 1 - (state.cellDegradation / 100);
        let capacitySum = 0;
        for (let year = 0; year < state.years; year++) {
            capacitySum += Math.pow(annualRetention, year);
        }
        const avgCapacityFactor = capacitySum / state.years;
        const requiredInitialPowerW = derived.TARGET_POWER_W / avgCapacityFactor;
        
        const hardwareCost = state.satelliteCostPerW * requiredInitialPowerW;
        const mass = requiredInitialPowerW / state.specificPowerWPerKg;
        
        return (terrestrialCost - hardwareCost) / mass;
    }
    
    // Alias for backwards compatibility
    function calculateNatGas() {
        return calculateTerrestrial();
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
        calculateTerrestrial,
        calculateNatGas,  // Alias for backwards compatibility
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

