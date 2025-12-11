const CostModel = require('../static/js/math.js');

const defaultState = CostModel.getState();

function runScenario(name, overrides) {
  const newState = { ...defaultState, ...overrides };
  CostModel.setState(newState);
  const orbital = CostModel.calculateOrbital();
  const terrestrial = CostModel.calculateTerrestrial();
  CostModel.setState(defaultState);
  return { name, overrides, orbital, terrestrial };
}

const scenarios = [
  {
    name: 'baseline',
    overrides: {}
  },
  {
    name: 'orbital_optimistic_starship',
    overrides: {
      launchCostPerKg: 200,
      satelliteCostPerW: 15,
      specificPowerWPerKg: 55,
      satellitePowerKW: 35,
      sunFraction: 0.99,
      cellDegradation: 1.5,
      gpuFailureRate: 5,
      nreCost: 300
    }
  },
  {
    name: 'orbital_pessimistic',
    overrides: {
      launchCostPerKg: 2000,
      satelliteCostPerW: 30,
      specificPowerWPerKg: 28,
      satellitePowerKW: 20,
      sunFraction: 0.9,
      cellDegradation: 4,
      gpuFailureRate: 12,
      nreCost: 800
    }
  },
  {
    name: 'terrestrial_high_gas',
    overrides: {
      gasPricePerMMBtu: 8.0,
      heatRateBtuKwh: 6600
    }
  },
  {
    name: 'terrestrial_low_capacity_factor',
    overrides: {
      capacityFactor: 0.6,
      pue: 1.3,
      gasPricePerMMBtu: 5.0
    }
  },
  {
    name: 'scaled_two_gw',
    overrides: {
      targetGW: 2,
      years: 7,
      capacityFactor: 0.9,
      launchCostPerKg: 800,
      satelliteCostPerW: 20,
      gasPricePerMMBtu: 4.5
    }
  }
];

const results = scenarios.map(({ name, overrides }) => runScenario(name, overrides));

console.log(JSON.stringify(results, null, 2));
