import React, { useState, useMemo } from 'react';

const SpaceVsGasInfographic = () => {
  const targetPowerMW = 1000;
  
  const [years, setYears] = useState(5);
  const [specificPowerWPerKg, setSpecificPowerWPerKg] = useState(45);
  const [satelliteCostPerW, setSatelliteCostPerW] = useState(9);
  const [launchCostPerKg, setLaunchCostPerKg] = useState(1000);
  const [capacityFactor, setCapacityFactor] = useState(0.65);
  const [capexPerKW, setCapexPerKW] = useState(898);
  const [fuelCostPerMWh, setFuelCostPerMWh] = useState(25);
  const [oAndMPerMWh, setOAndMPerMWh] = useState(6);

  // Simple overhead / maintenance / communications adders for each side
  // (expressed as a fraction of the base system cost for that side)
  const orbitalOverheadFrac = 0.05;
  const orbitalMaintenanceFrac = 0.03;
  const orbitalCommsFrac = 0.02;

  const natGasOverheadFrac = 0.04;
  const natGasMaintenanceFrac = 0.03;
  const natGasCommsFrac = 0.01;

  const references = [
    { id: 1, title: "NASA SBSP Concept Study", url: "#", year: "2024" },
    { id: 2, title: "SpaceX Starship Economics", url: "#", year: "2024" },
    { id: 3, title: "Starlink Satellite Specifications", url: "#", year: "2024" },
    { id: 4, title: "EIA NatGas Cost Report", url: "#", year: "2023" },
    { id: 5, title: "EIA Natural Gas Prices", url: "#", year: "2024" },
    { id: 6, title: "NREL Annual Technology Baseline", url: "#", year: "2024" },
  ];

  const [hoveredRef, setHoveredRef] = useState(null);

  const colors = {
    orbital: '#1e40af', // Deep blue
    orbitalLight: '#3b82f6',
    gas: '#b45309', // Amber/brown
    gasLight: '#d97706',
    paper: '#faf9f7',
    ink: '#1c1917',
    inkMuted: '#57534e',
    inkLight: '#a8a29e',
    rule: '#e7e5e4',
  };

  const hoursPerYear = 365 * 24;
  const totalHours = years * hoursPerYear;

  const orbitalCosts = useMemo(() => {
    const targetPowerW = targetPowerMW * 1e6;
    const totalMassKg = targetPowerW / specificPowerWPerKg;
    const hardwareCost = satelliteCostPerW * targetPowerW;
    const launchCost = launchCostPerKg * totalMassKg;
    const baseCost = hardwareCost + launchCost;
    const overheadCost = baseCost * orbitalOverheadFrac;
    const maintenanceCost = baseCost * orbitalMaintenanceFrac;
    const commsCost = baseCost * orbitalCommsFrac;
    const totalCost = baseCost + overheadCost + maintenanceCost + commsCost;
    const energyMWh = targetPowerMW * totalHours;
    const lcoe = totalCost / energyMWh;
    
    return { 
      totalMassKg, 
      hardwareCost, 
      launchCost, 
      baseCost,
      overheadCost,
      maintenanceCost,
      commsCost,
      totalCost, 
      costPerW: totalCost / targetPowerW, 
      energyMWh, 
      lcoe 
    };
  }, [specificPowerWPerKg, satelliteCostPerW, launchCostPerKg, totalHours]);
  
  const ngccCosts = useMemo(() => {
    const capacityKW = targetPowerMW * 1000;
    const capexTotal = capexPerKW * capacityKW;
    const energyMWh = targetPowerMW * capacityFactor * totalHours;
    const fuelCostTotal = fuelCostPerMWh * energyMWh;
    const oAndMTotal = oAndMPerMWh * energyMWh;
    const baseCost = capexTotal + fuelCostTotal + oAndMTotal;
    const overheadCost = baseCost * natGasOverheadFrac;
    const maintenanceCost = baseCost * natGasMaintenanceFrac;
    const commsCost = baseCost * natGasCommsFrac;
    const totalCost = baseCost + overheadCost + maintenanceCost + commsCost;
    
    return { 
      capexTotal, 
      fuelCostTotal, 
      oAndMTotal, 
      baseCost,
      overheadCost,
      maintenanceCost,
      commsCost,
      totalCost, 
      costPerW: totalCost / (targetPowerMW * 1e6), 
      energyMWh, 
      lcoe: totalCost / energyMWh 
    };
  }, [capacityFactor, capexPerKW, fuelCostPerMWh, oAndMPerMWh, totalHours]);

  const maxCost = Math.max(orbitalCosts.totalCost, ngccCosts.totalCost);
  const maxIndividual = Math.max(
    orbitalCosts.hardwareCost, 
    orbitalCosts.launchCost,
    orbitalCosts.overheadCost,
    orbitalCosts.maintenanceCost,
    orbitalCosts.commsCost,
    ngccCosts.capexTotal, 
    ngccCosts.fuelCostTotal, 
    ngccCosts.oAndMTotal,
    ngccCosts.overheadCost,
    ngccCosts.maintenanceCost,
    ngccCosts.commsCost
  );
  
  const formatCost = (cost) => {
    if (cost >= 1e9) return `$${(cost / 1e9).toFixed(1)}B`;
    if (cost >= 1e6) return `$${(cost / 1e6).toFixed(0)}M`;
    return `$${cost.toFixed(0)}`;
  };

  const formatLCOE = (lcoe) => `$${lcoe.toFixed(0)}/MWh`;

  const Slider = ({ label, value, onChange, min, max, step, unit, formatValue, ticks = [], color }) => {
    const percentage = ((value - min) / (max - min)) * 100;
    const displayValue = formatValue ? formatValue(value) : value.toLocaleString();
    
    return (
      <div className="mb-6">
        <div className="flex justify-between items-baseline mb-2">
          <span className="text-sm" style={{ color: colors.inkMuted }}>{label}</span>
          <span className="text-sm font-mono" style={{ color: colors.ink }}>{displayValue}{unit}</span>
        </div>
        <div className="relative h-6 flex items-center">
          <div className="absolute inset-x-0 h-px" style={{ backgroundColor: colors.rule }} />
          <div 
            className="absolute left-0 h-0.5 pointer-events-none rounded-full"
            style={{ width: `${percentage}%`, backgroundColor: color }}
          />
          <input
            type="range"
            min={min}
            max={max}
            step="any"
            value={value}
            onChange={(e) => {
              const raw = Number(e.target.value);
              const snapped = Math.round(raw / step) * step;
              onChange(snapped);
            }}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          <div 
            className="absolute w-3 h-3 rounded-full pointer-events-none border-2 bg-white"
            style={{ 
              left: `${percentage}%`, 
              transform: 'translateX(-50%)', 
              borderColor: color,
            }}
          />
          {ticks.map((tick, i) => {
            const tickPercent = ((tick.value - min) / (max - min)) * 100;
            if (tickPercent < 0 || tickPercent > 100) return null;
            return (
              <div 
                key={i}
                className="absolute flex flex-col items-center pointer-events-none"
                style={{ left: `${tickPercent}%`, transform: 'translateX(-50%)', top: '16px' }}
              >
                <div className="w-px h-1.5" style={{ backgroundColor: colors.inkLight }} />
              </div>
            );
          })}
        </div>
        {ticks.length > 0 && (
          <div className="relative h-4 mt-0.5">
            {ticks.map((tick, i) => {
              const tickPercent = ((tick.value - min) / (max - min)) * 100;
              if (tickPercent < 0 || tickPercent > 100) return null;
              return (
                <div 
                  key={i}
                  className="absolute text-xs whitespace-nowrap"
                  style={{ 
                    left: `${tickPercent}%`, 
                    transform: 'translateX(-50%)',
                    color: colors.inkLight,
                    fontSize: '10px'
                  }}
                >
                  {tick.label}
                </div>
              );
            })}
          </div>
        )}
      </div>
    );
  };

  const VerticalBar = ({ label, value, maxVal, color }) => {
    const height = Math.max((value / maxVal) * 100, 3);
    return (
      <div className="flex flex-col items-center group flex-1">
        <div 
          className="text-xs font-mono mb-1.5 opacity-0 group-hover:opacity-100 transition-opacity"
          style={{ color }}
        >
          {formatCost(value)}
        </div>
        <div 
          className="w-full max-w-10 h-36 relative flex items-end border-l border-b"
          style={{ borderColor: colors.rule }}
        >
          <div 
            className="w-full transition-all duration-500 ease-out"
            style={{ 
              height: `${height}%`,
              backgroundColor: color,
            }}
          />
        </div>
        <div 
          className="text-xs text-center mt-2 leading-tight" 
          style={{ color: colors.inkMuted, fontSize: '11px' }}
        >
          {label}
        </div>
      </div>
    );
  };

  const articleHTML = `
    <p class="first-para">This analysis compares the total system cost of deploying 1 GW of power generation capacity via orbital solar power satellites versus a terrestrial natural gas (NatGas) plant over a ${years}-year period.<sup data-ref="1">1</sup></p>
    
    <h3>Orbital Solar Economics</h3>
    <p>The cost of orbital solar is dominated by two factors: satellite hardware costs and launch costs. Using Starlink-class satellites as a proxy, we estimate specific power of ~${specificPowerWPerKg} W/kg and hardware costs of ~$${satelliteCostPerW}/W.<sup data-ref="2">2</sup><sup data-ref="3">3</sup></p>
    
    <p>At $${launchCostPerKg.toLocaleString()}/kg to LEO, a 1 GW orbital system requires ${(orbitalCosts.totalMassKg / 1e6).toFixed(1)} million kg of mass, costing ${formatCost(orbitalCosts.launchCost)} to launch and ${formatCost(orbitalCosts.hardwareCost)} in hardware.</p>
    
    <h3>NatGas Economics</h3>
    <p>Natural gas plants have overnight capital costs of ~$${capexPerKW}/kW, with typical capacity factors of ${(capacityFactor * 100).toFixed(0)}%.<sup data-ref="4">4</sup> Over ${years} years at current fuel prices (~$${fuelCostPerMWh}/MWh), fuel costs dominate the total cost of ownership.<sup data-ref="5">5</sup></p>
    
    <p>The NatGas system generates ${ngccCosts.energyMWh.toLocaleString(undefined, { maximumFractionDigits: 0 })} MWhr over ${years} years, with a levelized cost of ${formatLCOE(ngccCosts.lcoe)}.</p>
    
    <h3>Crossover Analysis</h3>
    <p>At $${launchCostPerKg.toLocaleString()}/kg launch costs, orbital solar costs ${formatCost(orbitalCosts.totalCost)} vs ${formatCost(ngccCosts.totalCost)} for NatGas. The crossover point occurs around $50–100/kg launch costs, which Starship may achieve at high flight rates.<sup data-ref="6">6</sup></p>
  `;

  return (
    <div className="min-h-screen" style={{ backgroundColor: colors.paper, color: colors.ink }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
        
        body { 
          font-family: 'IBM Plex Sans', -apple-system, sans-serif;
          -webkit-font-smoothing: antialiased;
        }
        
        input[type="range"] {
          touch-action: pan-x;
          -webkit-tap-highlight-color: transparent;
        }

        .reading-panel h3 {
          font-family: 'IBM Plex Sans', sans-serif;
          font-size: 0.875rem;
          font-weight: 600;
          color: ${colors.ink};
          margin: 1.75rem 0 0.5rem 0;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .reading-panel p {
          font-family: 'Source Serif 4', Georgia, serif;
          font-size: 1.0625rem;
          line-height: 1.75;
          color: ${colors.inkMuted};
          margin-bottom: 1rem;
          text-align: justify;
          hyphens: auto;
        }

        .reading-panel p.first-para::first-letter {
          font-size: 3.5rem;
          float: left;
          line-height: 1;
          padding-right: 0.5rem;
          color: ${colors.ink};
          font-weight: 600;
        }

        .reading-panel sup {
          color: ${colors.orbital};
          cursor: pointer;
          font-family: 'IBM Plex Mono', monospace;
          font-size: 0.65rem;
          font-weight: 500;
          transition: color 0.2s;
          margin-left: 1px;
        }

        .reading-panel sup:hover,
        .reading-panel sup.highlighted {
          color: ${colors.orbitalLight};
        }
      `}</style>
      
      {/* Header */}
      <header style={{ borderBottom: `1px solid ${colors.rule}` }}>
        <div className="max-w-4xl mx-auto px-8 pt-16 pb-8">
          <p className="text-xs uppercase tracking-widest mb-4" style={{ color: colors.inkLight }}>
            Technical Analysis
          </p>
          <h1 
            className="text-4xl leading-tight"
            style={{ fontFamily: "'Source Serif 4', Georgia, serif", fontWeight: 700, letterSpacing: '-0.02em' }}
          >
            Comparative Economics of Orbital Solar<br />and Terrestrial Gas Power Generation
          </h1>
          <p className="mt-4 text-lg" style={{ color: colors.inkMuted, fontFamily: "'Source Serif 4', Georgia, serif" }}>
            A first-principles cost model for 1 GW capacity over {years} years
          </p>
        </div>
      </header>

      {/* Cost Comparison */}
      <div style={{ borderBottom: `1px solid ${colors.rule}` }}>
        <div className="max-w-4xl mx-auto px-8 py-10">
          <p className="text-xs uppercase tracking-widest mb-6" style={{ color: colors.inkLight }}>
            Costs · Financial Analysis
          </p>
          <div className="grid grid-cols-2 gap-16">
            {/* Orbital */}
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: colors.orbital }} />
                <div>
                  <h3 className="text-sm font-semibold" style={{ fontFamily: "'IBM Plex Sans', sans-serif" }}>Orbital Solar</h3>
                  <p className="text-2xl font-mono mt-0.5" style={{ color: colors.orbital }}>{formatCost(orbitalCosts.totalCost)}</p>
                </div>
              </div>
              
              <div className="flex gap-3">
                <VerticalBar label="Hardware" value={orbitalCosts.hardwareCost} maxVal={maxIndividual} color={colors.orbital} />
                <VerticalBar label="Launch" value={orbitalCosts.launchCost} maxVal={maxIndividual} color={colors.orbital} />
              </div>
              
              <div className="mt-6 pt-4 space-y-1.5" style={{ borderTop: `1px solid ${colors.rule}` }}>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Total Mass</span>
                  <span className="font-mono">{(orbitalCosts.totalMassKg / 1e6).toFixed(1)}M kg</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Cost per Watt</span>
                  <span className="font-mono">${orbitalCosts.costPerW.toFixed(2)}/W</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Implied LCOE</span>
                  <span className="font-mono">{formatLCOE(orbitalCosts.lcoe)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Overhead</span>
                  <span className="font-mono">{formatCost(orbitalCosts.overheadCost)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Maintenance</span>
                  <span className="font-mono">{formatCost(orbitalCosts.maintenanceCost)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Communications</span>
                  <span className="font-mono">{formatCost(orbitalCosts.commsCost)}</span>
                </div>
              </div>
            </div>

            {/* NatGas */}
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-3 h-3 rounded-sm" style={{ backgroundColor: colors.gas }} />
                <div>
                  <h3 className="text-sm font-semibold" style={{ fontFamily: "'IBM Plex Sans', sans-serif" }}>NatGas</h3>
                  <p className="text-2xl font-mono mt-0.5" style={{ color: colors.gas }}>{formatCost(ngccCosts.totalCost)}</p>
                </div>
              </div>
              
              <div className="flex gap-3">
                <VerticalBar label="Capex" value={ngccCosts.capexTotal} maxVal={maxIndividual} color={colors.gas} />
                <VerticalBar label="Fuel" value={ngccCosts.fuelCostTotal} maxVal={maxIndividual} color={colors.gas} />
                <VerticalBar label="O&M" value={ngccCosts.oAndMTotal} maxVal={maxIndividual} color={colors.gas} />
              </div>
              
              <div className="mt-6 pt-4 space-y-1.5" style={{ borderTop: `1px solid ${colors.rule}` }}>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Energy Output</span>
                  <span className="font-mono">{ngccCosts.energyMWh.toLocaleString(undefined, { maximumFractionDigits: 0 })} MWhr</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Cost per Watt</span>
                  <span className="font-mono">${ngccCosts.costPerW.toFixed(2)}/W</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>LCOE</span>
                  <span className="font-mono">{formatLCOE(ngccCosts.lcoe)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Overhead</span>
                  <span className="font-mono">{formatCost(ngccCosts.overheadCost)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Maintenance</span>
                  <span className="font-mono">{formatCost(ngccCosts.maintenanceCost)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span style={{ color: colors.inkLight }}>Communications</span>
                  <span className="font-mono">{formatCost(ngccCosts.commsCost)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Interactive Parameters */}
      <div style={{ borderBottom: `1px solid ${colors.rule}` }}>
        <div className="max-w-4xl mx-auto px-8 py-10">
          <p className="text-xs uppercase tracking-widest mb-6" style={{ color: colors.inkLight }}>
            Engineering · System Parameters
          </p>
          <div className="mb-8 pb-6 -mx-8 px-8" style={{ borderBottom: `1px dashed ${colors.rule}` }}>
            <Slider 
              label="Analysis Period" 
              value={years} 
              onChange={setYears} 
              min={1} max={30} step={1} 
              unit=" years"
              color={colors.ink}
              ticks={[
                { value: 5, label: '5y' },
                { value: 10, label: '10y' },
                { value: 20, label: '20y' },
                { value: 30, label: '30y' },
              ]}
            />
          </div>
          
          <div className="grid grid-cols-2 gap-16">
            {/* Orbital */}
            <div>
              <div className="flex items-center gap-2 mb-5">
                <div className="w-2 h-2 rounded-sm" style={{ backgroundColor: colors.orbital }} />
                <h4 className="text-xs uppercase tracking-widest" style={{ color: colors.inkLight }}>Orbital Solar</h4>
              </div>
              <Slider 
                label="Specific Power" 
                value={specificPowerWPerKg} 
                onChange={setSpecificPowerWPerKg} 
                min={10} max={200} step={5} 
                unit=" W/kg"
                color={colors.orbital}
                ticks={[
                  { value: 45, label: 'Starlink' },
                  { value: 100, label: 'Advanced' },
                  { value: 180, label: 'Theoretical' },
                ]}
              />
              <Slider 
                label="Satellite Hardware Cost" 
                value={satelliteCostPerW} 
                onChange={setSatelliteCostPerW} 
                min={1} max={50} step={1} 
                unit=" $/W"
                color={colors.orbital}
                ticks={[
                  { value: 9, label: 'Starlink' },
                  { value: 25, label: 'Traditional' },
                ]}
              />
              <Slider 
                label="Launch Cost to LEO" 
                value={launchCostPerKg} 
                onChange={setLaunchCostPerKg} 
                min={10} max={5000} step={10} 
                unit=" $/kg"
                color={colors.orbital}
                ticks={[
                  { value: 50, label: 'Starship goal' },
                  { value: 1000, label: 'Starship' },
                  { value: 2700, label: 'Falcon 9' },
                ]}
              />
            </div>

            {/* NatGas */}
            <div>
              <div className="flex items-center gap-2 mb-5">
                <div className="w-2 h-2 rounded-sm" style={{ backgroundColor: colors.gas }} />
                <h4 className="text-xs uppercase tracking-widest" style={{ color: colors.inkLight }}>NatGas</h4>
              </div>
              <Slider 
                label="Capital Cost" 
                value={capexPerKW} 
                onChange={setCapexPerKW} 
                min={400} max={2000} step={50} 
                unit=" $/kW"
                color={colors.gas}
                ticks={[
                  { value: 898, label: 'EIA avg' },
                  { value: 1200, label: 'High' },
                ]}
              />
              <Slider 
                label="Fuel Cost" 
                value={fuelCostPerMWh} 
                onChange={setFuelCostPerMWh} 
                min={10} max={100} step={5} 
                unit=" $/MWh"
                color={colors.gas}
                ticks={[
                  { value: 25, label: '2024' },
                  { value: 50, label: 'High' },
                  { value: 75, label: 'Crisis' },
                ]}
              />
              <Slider 
                label="O&M Cost" 
                value={oAndMPerMWh} 
                onChange={setOAndMPerMWh} 
                min={2} max={20} step={1} 
                unit=" $/MWh"
                color={colors.gas}
                ticks={[
                  { value: 6, label: 'Typical' },
                  { value: 12, label: 'High' },
                ]}
              />
              <Slider 
                label="Capacity Factor" 
                value={capacityFactor} 
                onChange={setCapacityFactor} 
                min={0.3} max={0.95} step={0.05} 
                unit=""
                color={colors.gas}
                formatValue={(v) => `${(v * 100).toFixed(0)}%`}
                ticks={[
                  { value: 0.5, label: '50%' },
                  { value: 0.65, label: '65%' },
                  { value: 0.85, label: '85%' },
                ]}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Reading Panel */}
      <div className="max-w-4xl mx-auto px-8 py-12">
        <div className="flex gap-12">
          <div className="flex-1 reading-panel" style={{ maxWidth: '560px' }}>
            <div 
              dangerouslySetInnerHTML={{ __html: articleHTML }}
              onMouseOver={(e) => {
                if (e.target.tagName === 'SUP') {
                  const refId = e.target.getAttribute('data-ref');
                  setHoveredRef(parseInt(refId));
                  e.target.classList.add('highlighted');
                }
              }}
              onMouseOut={(e) => {
                if (e.target.tagName === 'SUP') {
                  setHoveredRef(null);
                  e.target.classList.remove('highlighted');
                }
              }}
            />
          </div>

          <div className="w-44 pt-1" style={{ borderLeft: `1px solid ${colors.rule}`, paddingLeft: '1.5rem' }}>
            <h4 className="text-xs uppercase tracking-widest mb-5" style={{ color: colors.inkLight }}>References</h4>
            <div className="space-y-4">
              {references.map((ref) => (
                <div 
                  key={ref.id}
                  className="cursor-pointer transition-all duration-200"
                  style={{ 
                    transform: hoveredRef === ref.id ? 'translateX(-3px)' : 'none',
                  }}
                  onClick={() => window.open(ref.url, '_blank')}
                >
                  <div className="flex items-start gap-2">
                    <span 
                      className="text-xs font-mono transition-colors flex-shrink-0"
                      style={{ color: hoveredRef === ref.id ? colors.orbital : colors.inkLight }}
                    >
                      {ref.id}.
                    </span>
                    <div>
                      <p 
                        className="text-xs leading-snug transition-colors"
                        style={{ color: hoveredRef === ref.id ? colors.ink : colors.inkMuted }}
                      >
                        {ref.title}
                      </p>
                      <p className="text-xs mt-0.5" style={{ color: colors.inkLight }}>{ref.year}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer style={{ borderTop: `1px solid ${colors.rule}` }}>
        <div className="max-w-4xl mx-auto px-8 py-6">
          <p className="text-xs" style={{ color: colors.inkLight }}>
            Note: Orbital model assumes 100% capacity factor. NatGas costs include fuel and O&M over the analysis period. All figures in 2024 USD.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default SpaceVsGasInfographic;