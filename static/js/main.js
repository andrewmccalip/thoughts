/**
 * Orbital Solar vs NatGas Cost Analysis - UI Controller
 * 
 * Handles all DOM manipulation, slider interactions, and visual updates.
 * All calculations come from math.js (CostModel).
 */

(function() {
    'use strict';

    // ==========================================
    // REFERENCES
    // ==========================================
    
    let references = [];
    let hoveredRefId = null;
    
    async function loadReferences() {
        try {
            // Load from static file (no Flask API needed)
            const response = await fetch('/static/references.json');
            references = await response.json();
            renderReferences();
            setupReferenceInteractions();
        } catch (error) {
            console.error('Failed to load references:', error);
        }
    }
    
    function renderReferences() {
        const refHTML = references.map(ref => `
            <div class="reference-item" data-ref-id="${ref.id}">
                <div class="reference-item-inner">
                    <span class="reference-number">${ref.id}.</span>
                    <div class="reference-content">
                        <span class="reference-title">${ref.title}</span>
                        <span class="reference-year">${ref.year}</span>
                    </div>
                </div>
            </div>
        `).join('');
        
        // Populate both desktop and mobile containers
        const containers = [
            document.getElementById('references-list'),
            document.getElementById('references-list-mobile')
        ];
        
        containers.forEach(container => {
            if (!container) return;
            container.innerHTML = refHTML;
            
            container.querySelectorAll('.reference-item').forEach(item => {
                item.addEventListener('click', () => {
                    const refId = parseInt(item.dataset.refId);
                    const ref = references.find(r => r.id === refId);
                    if (ref && ref.url && ref.url !== '#') {
                        window.open(ref.url, '_blank');
                    }
                });
            });
        });
    }
    
    function setupReferenceInteractions() {
        const readingPanel = document.querySelector('.reading-panel');
        if (!readingPanel) return;
        
        readingPanel.addEventListener('mouseover', (e) => {
            if (e.target.tagName === 'SUP') {
                const refId = e.target.getAttribute('data-ref');
                if (refId) {
                    highlightReference(parseInt(refId));
                    e.target.classList.add('highlighted');
                }
            }
        });
        
        readingPanel.addEventListener('mouseout', (e) => {
            if (e.target.tagName === 'SUP') {
                clearReferenceHighlight();
                e.target.classList.remove('highlighted');
            }
        });
        
        const refsList = document.getElementById('references-list');
        if (refsList) {
            refsList.addEventListener('mouseover', (e) => {
                const item = e.target.closest('.reference-item');
                if (item) {
                    const refId = parseInt(item.dataset.refId);
                    highlightReference(refId);
                    highlightSupElements(refId);
                }
            });
            
            refsList.addEventListener('mouseout', (e) => {
                const item = e.target.closest('.reference-item');
                if (item) {
                    clearReferenceHighlight();
                    clearSupHighlights();
                }
            });
        }
    }
    
    function highlightReference(refId) {
        hoveredRefId = refId;
        document.querySelectorAll('.reference-item').forEach(item => {
            item.classList.toggle('highlighted', parseInt(item.dataset.refId) === refId);
        });
    }
    
    function clearReferenceHighlight() {
        hoveredRefId = null;
        document.querySelectorAll('.reference-item').forEach(item => {
            item.classList.remove('highlighted');
        });
    }
    
    function highlightSupElements(refId) {
        document.querySelectorAll('.reading-panel sup').forEach(sup => {
            if (parseInt(sup.getAttribute('data-ref')) === refId) {
                sup.classList.add('highlighted');
            }
        });
    }
    
    function clearSupHighlights() {
        document.querySelectorAll('.reading-panel sup').forEach(sup => {
            sup.classList.remove('highlighted');
        });
    }

    // ==========================================
    // UI UPDATE
    // ==========================================
    
    function updateText(id, value) {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    }
    
    function updateUI() {
        const orbital = CostModel.calculateOrbital();
        const terrestrial = CostModel.calculateTerrestrial();
        const breakeven = CostModel.calculateBreakeven();
        const thermal = CostModel.calculateThermal();
        const state = CostModel.getState();
        const constants = CostModel.getConstants();
        
        // Find max values for bar scaling
        const maxCost = Math.max(
            orbital.hardwareCost,
            orbital.launchCost,
            orbital.opsCost,
            orbital.nreCost + orbital.gpuReplacementCost,
            terrestrial.powerGenCost,
            terrestrial.electricalCost,
            terrestrial.mechanicalCost,
            terrestrial.civilCost,
            terrestrial.networkCost,
            terrestrial.fuelCostTotal
        );
        
        // Update orbital display (desktop + mobile + sticky)
        updateText('orbital-total', CostModel.formatCost(orbital.totalCost));
        updateText('orbital-total-mobile', CostModel.formatCost(orbital.totalCost));
        updateText('orbital-total-sticky', CostModel.formatCost(orbital.totalCost));
        updateText('orbital-hardware-value', CostModel.formatCost(orbital.hardwareCost));
        updateText('orbital-hardware-value-mobile', CostModel.formatCost(orbital.hardwareCost));
        updateText('orbital-launch-value', CostModel.formatCost(orbital.launchCost));
        updateText('orbital-launch-value-mobile', CostModel.formatCost(orbital.launchCost));
        updateText('orbital-mass', CostModel.formatMass(orbital.totalMassKg));
        updateText('orbital-mass-mobile', CostModel.formatMass(orbital.totalMassKg));
        updateText('orbital-cpw', `$${orbital.costPerW.toFixed(2)}/W`);
        updateText('orbital-cpw-mobile', `$${orbital.costPerW.toFixed(2)}/W`);
        updateText('orbital-energy', CostModel.formatEnergy(orbital.energyMWh));
        updateText('orbital-energy-mobile', CostModel.formatEnergy(orbital.energyMWh));
        updateText('orbital-lcoe', CostModel.formatLCOE(orbital.lcoe));
        updateText('orbital-lcoe-mobile', CostModel.formatLCOE(orbital.lcoe));
        // Update orbital bars (desktop + mobile)
        const setBarWidth = (id, pct) => {
            const el = document.getElementById(id);
            if (el) el.style.width = `${pct}%`;
        };
        setBarWidth('orbital-hardware-bar', (orbital.hardwareCost / maxCost) * 100);
        setBarWidth('orbital-hardware-bar-mobile', (orbital.hardwareCost / maxCost) * 100);
        setBarWidth('orbital-launch-bar', (orbital.launchCost / maxCost) * 100);
        setBarWidth('orbital-launch-bar-mobile', (orbital.launchCost / maxCost) * 100);
        setBarWidth('orbital-om-bar', (orbital.opsCost / maxCost) * 100);
        setBarWidth('orbital-om-bar-mobile', (orbital.opsCost / maxCost) * 100);
        updateText('orbital-om-value', CostModel.formatCost(orbital.opsCost));
        updateText('orbital-om-value-mobile', CostModel.formatCost(orbital.opsCost));
        // NRE + GPU replacement combined
        const nreReplCost = orbital.nreCost + orbital.gpuReplacementCost;
        setBarWidth('orbital-nre-bar', (nreReplCost / maxCost) * 100);
        setBarWidth('orbital-nre-bar-mobile', (nreReplCost / maxCost) * 100);
        updateText('orbital-nre-value', CostModel.formatCost(nreReplCost));
        updateText('orbital-nre-value-mobile', CostModel.formatCost(nreReplCost));
        
        // Update Terrestrial display (desktop + mobile + sticky)
        updateText('terrestrial-total', CostModel.formatCost(terrestrial.totalCost));
        updateText('terrestrial-total-mobile', CostModel.formatCost(terrestrial.totalCost));
        updateText('terrestrial-total-sticky', CostModel.formatCost(terrestrial.totalCost));
        updateText('terrestrial-powergen-value', CostModel.formatCost(terrestrial.powerGenCost));
        updateText('terrestrial-powergen-value-mobile', CostModel.formatCost(terrestrial.powerGenCost));
        updateText('terrestrial-electrical-value', CostModel.formatCost(terrestrial.electricalCost));
        updateText('terrestrial-electrical-value-mobile', CostModel.formatCost(terrestrial.electricalCost));
        updateText('terrestrial-mechanical-value', CostModel.formatCost(terrestrial.mechanicalCost));
        updateText('terrestrial-mechanical-value-mobile', CostModel.formatCost(terrestrial.mechanicalCost));
        updateText('terrestrial-civil-value', CostModel.formatCost(terrestrial.civilCost));
        updateText('terrestrial-civil-value-mobile', CostModel.formatCost(terrestrial.civilCost));
        updateText('terrestrial-fuel-value', CostModel.formatCost(terrestrial.fuelCostTotal));
        updateText('terrestrial-fuel-value-mobile', CostModel.formatCost(terrestrial.fuelCostTotal));
        updateText('terrestrial-capex-cpw', `$${terrestrial.facilityCapexPerW.toFixed(2)}/W`);
        updateText('terrestrial-capex-cpw-mobile', `$${terrestrial.facilityCapexPerW.toFixed(2)}/W`);
        updateText('terrestrial-cpw', `$${terrestrial.costPerW.toFixed(2)}/W`);
        updateText('terrestrial-cpw-mobile', `$${terrestrial.costPerW.toFixed(2)}/W`);
        updateText('terrestrial-energy', CostModel.formatEnergy(terrestrial.energyMWh));
        updateText('terrestrial-energy-mobile', CostModel.formatEnergy(terrestrial.energyMWh));
        updateText('terrestrial-lcoe', CostModel.formatLCOE(terrestrial.lcoe));
        updateText('terrestrial-lcoe-mobile', CostModel.formatLCOE(terrestrial.lcoe));
        
        // Update Terrestrial bars (desktop + mobile)
        setBarWidth('terrestrial-powergen-bar', (terrestrial.powerGenCost / maxCost) * 100);
        setBarWidth('terrestrial-powergen-bar-mobile', (terrestrial.powerGenCost / maxCost) * 100);
        setBarWidth('terrestrial-electrical-bar', (terrestrial.electricalCost / maxCost) * 100);
        setBarWidth('terrestrial-electrical-bar-mobile', (terrestrial.electricalCost / maxCost) * 100);
        setBarWidth('terrestrial-mechanical-bar', (terrestrial.mechanicalCost / maxCost) * 100);
        setBarWidth('terrestrial-mechanical-bar-mobile', (terrestrial.mechanicalCost / maxCost) * 100);
        setBarWidth('terrestrial-civil-bar', (terrestrial.civilCost / maxCost) * 100);
        setBarWidth('terrestrial-civil-bar-mobile', (terrestrial.civilCost / maxCost) * 100);
        setBarWidth('terrestrial-fitout-bar', (terrestrial.networkCost / maxCost) * 100);
        setBarWidth('terrestrial-fitout-bar-mobile', (terrestrial.networkCost / maxCost) * 100);
        updateText('terrestrial-fitout-value', CostModel.formatCost(terrestrial.networkCost));
        updateText('terrestrial-fitout-value-mobile', CostModel.formatCost(terrestrial.networkCost));
        setBarWidth('terrestrial-fuel-bar', (terrestrial.fuelCostTotal / maxCost) * 100);
        setBarWidth('terrestrial-fuel-bar-mobile', (terrestrial.fuelCostTotal / maxCost) * 100);
        
        // Update breakeven
        updateText('breakeven-launch', CostModel.formatCostPerKg(breakeven));
        
        // Update footer
        updateText('footer-sun', `${Math.round(state.sunFraction * 100)}%`);
        
        // Update assumptions
        updateText('assumption-capacity', `${state.targetGW} GW`);
        updateText('assumption-years', `${state.years} years`);
        updateText('assumption-mass', CostModel.formatMass(orbital.totalMassKg));
        updateText('assumption-specific-power', `${state.specificPowerWPerKg} W/kg`);
        
        // Update engineering outputs - Orbital
        updateText('eng-orbital-mass', CostModel.formatMass(orbital.totalMassKg));
        updateText('eng-orbital-fleet-array', `${orbital.arrayAreaKm2.toFixed(1)} km²`);
        updateText('eng-orbital-sat-array', `${orbital.singleSatArrayM2.toFixed(0)} m²`);
        updateText('eng-orbital-sat-count', `~${orbital.satelliteCount.toLocaleString()}`);
        updateText('eng-orbital-launches', `~${orbital.starshipLaunches.toLocaleString()}`);
        updateText('eng-orbital-lox', `${(orbital.loxGallons / 1e6).toFixed(0)}M gal`);
        updateText('eng-orbital-methane', `${(orbital.methaneGallons / 1e6).toFixed(0)}M gal`);
        updateText('eng-orbital-gpu-margin', `+${orbital.gpuMarginPct.toFixed(1)}%`);
        updateText('eng-orbital-solar-margin', `+${orbital.solarMarginPct.toFixed(1)}%`);
        updateText('eng-orbital-energy', CostModel.formatEnergy(orbital.energyMWh));
        
        // Update engineering outputs - Terrestrial (CCGT)
        updateText('eng-ngcc-turbines', `${terrestrial.turbineCount} units`);
        updateText('eng-ngcc-generation', `${terrestrial.totalGenerationMW.toLocaleString()} MW`);
        updateText('eng-ngcc-capacity-factor', `${Math.round(terrestrial.capacityFactor * 100)}%`);
        updateText('eng-ngcc-heat-rate', `${state.heatRateBtuKwh.toLocaleString()} BTU/kWh`);
        updateText('eng-ngcc-gas-consumption', `${terrestrial.gasConsumptionBCF.toFixed(0)} BCF`);
        updateText('eng-ngcc-fuel-cost', `$${terrestrial.fuelCostPerMWh.toFixed(0)}/MWh`);
        updateText('eng-ngcc-energy', CostModel.formatEnergy(terrestrial.energyMWh));

        // Thermal analysis outputs - Bifacial Model
        updateText('thermal-available-area', `${thermal.availableAreaKm2.toFixed(2)} km²`);
        updateText('thermal-effective-emissivity', `${thermal.effectiveEmissivity.toFixed(2)}`);
        updateText('thermal-total-emissivity', `${thermal.totalEmissivity.toFixed(2)}`);
        updateText('thermal-beta-angle', `${thermal.betaAngle}°`);
        updateText('thermal-view-factor', `${thermal.vfEarth.toFixed(3)}`);
        
        // Heat loads
        updateText('thermal-q-solar', `${(thermal.qSolarW / 1e6).toFixed(0)} MW`);
        updateText('thermal-q-earth-ir', `${(thermal.qEarthIRW / 1e6).toFixed(1)} MW`);
        updateText('thermal-q-albedo', `${(thermal.qAlbedoW / 1e6).toFixed(1)} MW`);
        updateText('thermal-q-heatloop', `${(thermal.qHeatLoopW / 1e6).toFixed(0)} MW`);
        updateText('thermal-total-heat-in', `${(thermal.totalHeatInW / 1e6).toFixed(0)} MW`);
        updateText('thermal-power-generated', `${(thermal.powerGeneratedW / 1e6).toFixed(0)} MW`);
        
        // Equilibrium temperature - main result
        const eqTempEl = document.getElementById('thermal-eq-temp');
        if (eqTempEl) {
            eqTempEl.textContent = `${thermal.eqTempC.toFixed(1)} °C`;
            const tempOk = thermal.eqTempC <= thermal.radiatorTempC;
            eqTempEl.classList.toggle('status-pass', tempOk);
            eqTempEl.classList.toggle('status-fail', !tempOk);
        }
        
        updateText('thermal-compute-temp', `${thermal.computeTempC.toFixed(1)} °C`);
        updateText('thermal-radiator-target', `${thermal.radiatorTempC.toFixed(1)} °C`);
        updateText('thermal-capacity', `${(thermal.radiativeCapacityW / 1e6).toFixed(0)} MW`);
        
        // Margin - pass if equilibrium temp below radiator limit
        const marginEl = document.getElementById('thermal-margin');
        const marginBadgeEl = document.getElementById('thermal-margin-badge');
        if (marginEl) {
            marginEl.textContent = `${thermal.tempMarginC.toFixed(1)} °C`;
            marginEl.classList.toggle('status-pass', thermal.areaSufficient);
            marginEl.classList.toggle('status-fail', !thermal.areaSufficient);
        }
        if (marginBadgeEl) {
            marginBadgeEl.textContent = thermal.areaSufficient ? 'PASS' : 'FAIL';
            marginBadgeEl.classList.toggle('status-pass', thermal.areaSufficient);
            marginBadgeEl.classList.toggle('status-fail', !thermal.areaSufficient);
        }
        
        // Required area - fail if more than available
        const reqAreaEl = document.getElementById('thermal-required-area');
        if (reqAreaEl) {
            reqAreaEl.textContent = `${thermal.areaRequiredKm2.toFixed(2)} km²`;
            const areaOk = thermal.areaRequiredKm2 <= thermal.availableAreaKm2;
            reqAreaEl.classList.toggle('status-pass', areaOk);
            reqAreaEl.classList.toggle('status-fail', !areaOk);
        }
        
        // Update thermal diagram values
        updateThermalDiagram(thermal);
    }
    
    function updateThermalDiagram(thermal) {
        // Update diagram heat flow values
        updateText('diagram-q-solar', `${(thermal.qSolarW / 1e6).toFixed(0)} MW`);
        updateText('diagram-q-earth-ir', `${(thermal.qEarthIRW / 1e6).toFixed(1)} MW`);
        updateText('diagram-q-albedo', `${(thermal.qAlbedoW / 1e6).toFixed(1)} MW`);
        updateText('diagram-q-heatloop', `${(thermal.qHeatLoopW / 1e6).toFixed(0)} MW`);
        // Separate radiation for each side based on different emissivities
        updateText('diagram-q-rad-pv', `${(thermal.qRadAW / 1e6).toFixed(0)} MW`);
        updateText('diagram-q-rad-back', `${(thermal.qRadBW / 1e6).toFixed(0)} MW`);
        updateText('diagram-power-out', `${(thermal.powerGeneratedW / 1e6).toFixed(0)} MW`);
        
        // Update T_eq with pass/fail coloring
        const eqTempEl = document.getElementById('diagram-eq-temp');
        if (eqTempEl) {
            eqTempEl.textContent = `${thermal.eqTempC.toFixed(0)}°C`;
            eqTempEl.classList.toggle('temp-pass', thermal.areaSufficient);
            eqTempEl.classList.toggle('temp-fail', !thermal.areaSufficient);
        }
    }

    // ==========================================
    // SLIDER SETUP
    // ==========================================

    function setupSlider(sliderId, fillId, valueId, min, max, stateKey, formatValue) {
        const slider = document.getElementById(sliderId);
        const fill = document.getElementById(fillId);
        const valueDisplay = document.getElementById(valueId);
        
        if (!slider || !fill || !valueDisplay) return;
        
        function updateSlider() {
            const value = CostModel.getState()[stateKey];
            const percentage = ((value - min) / (max - min)) * 100;
            fill.style.width = `${percentage}%`;
            valueDisplay.textContent = formatValue(value);
        }
        
        slider.addEventListener('input', function() {
            CostModel.updateState(stateKey, parseFloat(this.value));
            updateSlider();
            updateUI();
        });
        
        updateSlider();
    }

    // Logarithmic slider - better for wide ranges where low values need more resolution
    function setupLogSlider(sliderId, fillId, valueId, min, max, stateKey, formatValue) {
        const slider = document.getElementById(sliderId);
        const fill = document.getElementById(fillId);
        const valueDisplay = document.getElementById(valueId);
        
        if (!slider || !fill || !valueDisplay) return;
        
        const logMin = Math.log(min);
        const logMax = Math.log(max);
        const logRange = logMax - logMin;
        
        // Convert actual value to slider position (0-100)
        function valueToPosition(value) {
            return ((Math.log(value) - logMin) / logRange) * 100;
        }
        
        // Convert slider position (0-100) to actual value
        function positionToValue(position) {
            return Math.exp(logMin + (position / 100) * logRange);
        }
        
        function updateSlider() {
            const value = CostModel.getState()[stateKey];
            const percentage = valueToPosition(value);
            fill.style.width = `${percentage}%`;
            valueDisplay.textContent = formatValue(value);
            slider.value = percentage;
        }
        
        slider.addEventListener('input', function() {
            const actualValue = positionToValue(parseFloat(this.value));
            CostModel.updateState(stateKey, actualValue);
            fill.style.width = `${this.value}%`;
            valueDisplay.textContent = formatValue(actualValue);
            updateUI();
        });
        
        // Store log params for tick positioning
        slider.dataset.logScale = 'true';
        slider.dataset.logMin = min;
        slider.dataset.logMax = max;
        
        updateSlider();
    }

    function positionSliderTicks() {
        document.querySelectorAll('.slider-container').forEach(container => {
            const slider = container.querySelector('input[type="range"]');
            const ticksContainer = container.querySelector('.slider-ticks');
            if (!slider || !ticksContainer) return;
            
            const isLogScale = slider.dataset.logScale === 'true';
            const ticks = ticksContainer.querySelectorAll('.tick');
            const tickCount = ticks.length;
            
            let getPercentage;
            if (isLogScale) {
                const logMin = Math.log(parseFloat(slider.dataset.logMin));
                const logMax = Math.log(parseFloat(slider.dataset.logMax));
                const logRange = logMax - logMin;
                getPercentage = (value) => ((Math.log(value) - logMin) / logRange) * 100;
            } else {
                const min = parseFloat(slider.min);
                const max = parseFloat(slider.max);
                const range = max - min;
                getPercentage = (value) => ((value - min) / range) * 100;
            }
            
            ticks.forEach((tick, index) => {
                const value = parseFloat(tick.dataset.value);
                const percentage = getPercentage(value);
                tick.style.left = percentage + '%';
                tick.style.position = 'absolute';
                
                // Adjust transform based on position to prevent overflow
                if (index === 0) {
                    // First tick: align left edge
                    tick.style.transform = 'translateX(0)';
                } else if (index === tickCount - 1) {
                    // Last tick: align right edge
                    tick.style.transform = 'translateX(-100%)';
                } else {
                    // Middle ticks: center
                    tick.style.transform = 'translateX(-50%)';
                }
            });
            
            // Ensure ticks container is positioned relatively
            ticksContainer.style.position = 'relative';
            ticksContainer.style.display = 'flex';
            ticksContainer.style.justifyContent = 'flex-start';
            ticksContainer.style.width = '100%';
        });
    }
    
    function init() {
        // Target capacity slider (GW)
        setupSlider('capacity-slider', 'capacity-fill', 'capacity-value', 1, 1000, 'targetGW', v => `${v} GW`);
        
        // Years slider
        setupSlider('years-slider', 'years-fill', 'years-value', 3, 10, 'years', v => `${v} years`);
        
        // Launch cost slider (min $1/kg for extreme future scenarios)
        setupSlider('launch-cost-slider', 'launch-cost-fill', 'launch-cost-value', 1, 2940, 'launchCostPerKg', v => `$${v.toLocaleString()}/kg`);
        
        // Satellite cost slider (min $1/W for extreme future scenarios)
        setupSlider('sat-cost-slider', 'sat-cost-fill', 'sat-cost-value', 1, 40, 'satelliteCostPerW', v => `$${v}/W`);
        
        // Specific power slider (W/kg) - LOG SCALE for better resolution at lower values
        setupLogSlider('specific-power-slider', 'specific-power-fill', 'specific-power-value', 3, 500, 'specificPowerWPerKg', v => `${Math.round(v)} W/kg`);
        
        // Satellite size slider (kW nameplate) - LOG SCALE for better resolution at lower values
        setupLogSlider('sat-size-slider', 'sat-size-fill', 'sat-size-value', 5, 500, 'satellitePowerKW', v => `${Math.round(v)} kW`);
        
        // Sun fraction slider
        setupSlider('sun-fraction-slider', 'sun-fraction-fill', 'sun-fraction-value', 0.55, 1.0, 'sunFraction', v => `${Math.round(v * 100)}%`);
        
        // Cell degradation slider
        setupSlider('degradation-slider', 'degradation-fill', 'degradation-value', 0, 12, 'cellDegradation', v => `${v.toFixed(1)}%/yr`);
        
        // GPU failure rate slider
        setupSlider('gpu-failure-slider', 'gpu-failure-fill', 'gpu-failure-value', 0, 10, 'gpuFailureRate', v => `${v.toFixed(1)}%/yr`);
        
        // NRE cost slider
        setupSlider('nre-slider', 'nre-fill', 'nre-value', 0, 10000, 'nreCost', v => v >= 1000 ? `$${(v/1000).toFixed(1)}B` : `$${v}M`);
        
        // Terrestrial sliders
        // Gas turbine capex slider ($/W, converted to $/kW for state)
        const gasTurbineSlider = document.getElementById('gas-turbine-slider');
        const gasTurbineFill = document.getElementById('gas-turbine-fill');
        const gasTurbineValue = document.getElementById('gas-turbine-value');
        if (gasTurbineSlider && gasTurbineFill && gasTurbineValue) {
            function updateGasTurbineSlider() {
                const state = CostModel.getState();
                const valuePerW = state.gasTurbineCapexPerKW / 1000;
                const percentage = ((valuePerW - 1.45) / (2.30 - 1.45)) * 100;
                gasTurbineFill.style.width = `${Math.max(0, Math.min(100, percentage))}%`;
                gasTurbineValue.textContent = `$${valuePerW.toFixed(2)}/W`;
            }
            gasTurbineSlider.addEventListener('input', function() {
                const valuePerW = parseFloat(this.value);
                CostModel.updateState('gasTurbineCapexPerKW', valuePerW * 1000);
                updateGasTurbineSlider();
                updateUI();
            });
            updateGasTurbineSlider();
        }
        
        // Heat rate slider
        setupSlider('heat-rate-slider', 'heat-rate-fill', 'heat-rate-value', 6000, 9000, 'heatRateBtuKwh', v => `${v.toLocaleString()} BTU/kWh`);
        
        // Gas price slider (regional pricing)
        setupSlider('gas-price-slider', 'gas-price-fill', 'gas-price-value', 2, 15, 'gasPricePerMMBtu', v => `$${v.toFixed(2)}/MMBtu`);
        
        // PUE slider
        setupSlider('pue-slider', 'pue-fill', 'pue-value', 1.1, 1.5, 'pue', v => v.toFixed(2));

        // Thermal sliders - Bifacial Model
        setupSlider('solar-absorptivity-slider', 'solar-absorptivity-fill', 'solar-absorptivity-value', 0.80, 0.98, 'solarAbsorptivity', v => v.toFixed(2));
        setupSlider('emissivity-pv-slider', 'emissivity-pv-fill', 'emissivity-pv-value', 0, 0.95, 'emissivityPV', v => v.toFixed(2));
        setupSlider('emissivity-rad-slider', 'emissivity-rad-fill', 'emissivity-rad-value', 0, 0.98, 'emissivityRad', v => v.toFixed(2));
        setupSlider('pv-efficiency-slider', 'pv-efficiency-fill', 'pv-efficiency-value', 0.20, 0.24, 'pvEfficiency', v => `${(v * 100).toFixed(0)}%`);
        setupSlider('beta-angle-slider', 'beta-angle-fill', 'beta-angle-value', 60, 90, 'betaAngle', v => `${v}°`);
        setupSlider('altitude-slider', 'altitude-fill', 'altitude-value', 400, 1200, 'orbitalAltitudeKm', v => `${v} km`);
        setupSlider('die-temp-slider', 'die-temp-fill', 'die-temp-value', 70, 100, 'maxDieTempC', v => `${v.toFixed(0)} °C`);
        setupSlider('temp-drop-slider', 'temp-drop-fill', 'temp-drop-value', 5, 25, 'tempDropC', v => `${v.toFixed(0)} °C`);
        
        
        // DC Infrastructure slider with breakdown
        // Percentages from report: Electrical 45%, Mechanical 20%, Shell 17%, Fit-out 8%, Site 5%, Fees 5%
        const facilitySlider = document.getElementById('facility-slider');
        const facilityFill = document.getElementById('facility-fill');
        const facilityValue = document.getElementById('facility-value');
        if (facilitySlider && facilityFill && facilityValue) {
            const DC_BREAKDOWN_PCTS = {
                electrical: 0.45,
                mechanical: 0.20,
                shell: 0.17,
                fitout: 0.08,
                site: 0.05,
                fees: 0.05
            };
            
            function updateFacilitySlider() {
                const state = CostModel.getState();
                const total = state.electricalCostPerW + state.mechanicalCostPerW + state.civilCostPerW + state.networkCostPerW;
                const percentage = ((total - 10) / (17 - 10)) * 100;
                facilityFill.style.width = `${Math.max(0, Math.min(100, percentage))}%`;
                facilityValue.textContent = `$${total.toFixed(2)}/W`;
                
                // Update breakdown display
                const updateEl = (id, val) => {
                    const el = document.getElementById(id);
                    if (el) el.textContent = `$${val.toFixed(2)}/W`;
                };
                updateEl('dc-electrical', total * DC_BREAKDOWN_PCTS.electrical);
                updateEl('dc-mechanical', total * DC_BREAKDOWN_PCTS.mechanical);
                updateEl('dc-shell', total * DC_BREAKDOWN_PCTS.shell);
                updateEl('dc-fitout', total * DC_BREAKDOWN_PCTS.fitout);
                updateEl('dc-site', total * DC_BREAKDOWN_PCTS.site);
                updateEl('dc-fees', total * DC_BREAKDOWN_PCTS.fees);
            }
            facilitySlider.addEventListener('input', function() {
                const newTotal = parseFloat(this.value);
                // Scale each component proportionally (maintain report ratios)
                const state = CostModel.getState();
                const oldTotal = state.electricalCostPerW + state.mechanicalCostPerW + state.civilCostPerW + state.networkCostPerW;
                const scale = newTotal / oldTotal;
                CostModel.updateState('electricalCostPerW', state.electricalCostPerW * scale);
                CostModel.updateState('mechanicalCostPerW', state.mechanicalCostPerW * scale);
                CostModel.updateState('civilCostPerW', state.civilCostPerW * scale);
                CostModel.updateState('networkCostPerW', state.networkCostPerW * scale);
                updateFacilitySlider();
                updateUI();
            });
            
            updateFacilitySlider();
        }
        
        // Initial UI update
        updateUI();
        
        // Load references
        loadReferences();
        
        // Position ticks after DOM is ready and sliders are initialized
        positionSliderTicks();
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
