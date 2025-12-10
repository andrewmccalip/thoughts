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
            const response = await fetch('/api/references');
            references = await response.json();
            renderReferences();
            setupReferenceInteractions();
        } catch (error) {
            console.error('Failed to load references:', error);
        }
    }
    
    function renderReferences() {
        const container = document.getElementById('references-list');
        if (!container) return;
        
        container.innerHTML = references.map(ref => `
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
        
        container.querySelectorAll('.reference-item').forEach(item => {
            item.addEventListener('click', () => {
                const refId = parseInt(item.dataset.refId);
                const ref = references.find(r => r.id === refId);
                if (ref && ref.url && ref.url !== '#') {
                    window.open(ref.url, '_blank');
                }
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
            orbital.omCost,
            terrestrial.powerGenCost,
            terrestrial.electricalCost,
            terrestrial.mechanicalCost,
            terrestrial.civilCost,
            terrestrial.fuelCostTotal
        );
        
        // Update orbital display
        updateText('orbital-total', CostModel.formatCost(orbital.totalCost));
        updateText('orbital-hardware-value', CostModel.formatCost(orbital.hardwareCost));
        updateText('orbital-launch-value', CostModel.formatCost(orbital.launchCost));
        updateText('orbital-mass', CostModel.formatMass(orbital.totalMassKg));
        updateText('orbital-cpw', `$${orbital.costPerW.toFixed(2)}/W`);
        updateText('orbital-energy', CostModel.formatEnergy(orbital.energyMWh));
        updateText('orbital-lcoe', CostModel.formatLCOE(orbital.lcoe));
        updateText('orbital-overhead', CostModel.formatCost(orbital.overheadCost));
        updateText('orbital-maintenance', CostModel.formatCost(orbital.maintenanceCost));
        updateText('orbital-comms', CostModel.formatCost(orbital.commsCost));
        
        // Update orbital bars
        document.getElementById('orbital-hardware-bar').style.width = `${(orbital.hardwareCost / maxCost) * 100}%`;
        document.getElementById('orbital-launch-bar').style.width = `${(orbital.launchCost / maxCost) * 100}%`;
        document.getElementById('orbital-om-bar').style.width = `${(orbital.omCost / maxCost) * 100}%`;
        updateText('orbital-om-value', CostModel.formatCost(orbital.omCost));
        
        // Update Terrestrial display (5 buckets from report)
        updateText('terrestrial-total', CostModel.formatCost(terrestrial.totalCost));
        updateText('terrestrial-powergen-value', CostModel.formatCost(terrestrial.powerGenCost));
        updateText('terrestrial-electrical-value', CostModel.formatCost(terrestrial.electricalCost));
        updateText('terrestrial-mechanical-value', CostModel.formatCost(terrestrial.mechanicalCost));
        updateText('terrestrial-civil-value', CostModel.formatCost(terrestrial.civilCost));
        updateText('terrestrial-fuel-value', CostModel.formatCost(terrestrial.fuelCostTotal));
        updateText('terrestrial-capex-cpw', `$${terrestrial.facilityCapexPerW.toFixed(2)}/W`);
        updateText('terrestrial-cpw', `$${terrestrial.costPerW.toFixed(2)}/W`);
        updateText('terrestrial-energy', CostModel.formatEnergy(terrestrial.energyMWh));
        updateText('terrestrial-lcoe', CostModel.formatLCOE(terrestrial.lcoe));
        
        // Update Terrestrial bars (5 buckets)
        document.getElementById('terrestrial-powergen-bar').style.width = `${(terrestrial.powerGenCost / maxCost) * 100}%`;
        document.getElementById('terrestrial-electrical-bar').style.width = `${(terrestrial.electricalCost / maxCost) * 100}%`;
        document.getElementById('terrestrial-mechanical-bar').style.width = `${(terrestrial.mechanicalCost / maxCost) * 100}%`;
        document.getElementById('terrestrial-civil-bar').style.width = `${(terrestrial.civilCost / maxCost) * 100}%`;
        document.getElementById('terrestrial-fuel-bar').style.width = `${(terrestrial.fuelCostTotal / maxCost) * 100}%`;
        
        // Update breakeven
        updateText('breakeven-launch', CostModel.formatCostPerKg(breakeven));
        
        // Update header subtitle and footer
        updateText('capacity-display', state.targetGW);
        updateText('years-display', state.years);
        updateText('footer-sun', `${Math.round(state.sunFraction * 100)}%`);
        
        // Update assumptions
        updateText('assumption-capacity', `${state.targetGW} GW`);
        updateText('assumption-years', `${state.years} years`);
        updateText('assumption-mass', CostModel.formatMass(orbital.totalMassKg));
        updateText('assumption-specific-power', `${state.specificPowerWPerKg} W/kg`);
        
        // Update engineering outputs - Orbital
        updateText('eng-orbital-mass', CostModel.formatMass(orbital.totalMassKg));
        updateText('eng-orbital-array-area', `${orbital.arrayAreaKm2.toFixed(1)} km²`);
        updateText('eng-orbital-sat-count', `~${orbital.satelliteCount.toLocaleString()}`);
        updateText('eng-orbital-launches', `~${orbital.starshipLaunches.toLocaleString()}`);
        updateText('eng-orbital-lox', `${(orbital.loxGallons / 1e6).toFixed(0)}M gal`);
        updateText('eng-orbital-methane', `${(orbital.methaneGallons / 1e6).toFixed(0)}M gal`);
        updateText('eng-orbital-degradation', `+${orbital.degradationMargin.toFixed(1)}%`);
        updateText('eng-orbital-energy', CostModel.formatEnergy(orbital.energyMWh));
        
        // Update engineering outputs - Terrestrial (CCGT)
        updateText('eng-ngcc-turbines', `${terrestrial.turbineCount} units`);
        updateText('eng-ngcc-generation', `${terrestrial.totalGenerationMW.toLocaleString()} MW`);
        updateText('eng-ngcc-capacity-factor', `${Math.round(terrestrial.capacityFactor * 100)}%`);
        updateText('eng-ngcc-heat-rate', `${state.heatRateBtuKwh.toLocaleString()} BTU/kWh`);
        updateText('eng-ngcc-gas-consumption', `${terrestrial.gasConsumptionBCF.toFixed(0)} BCF`);
        updateText('eng-ngcc-fuel-cost', `$${terrestrial.fuelCostPerMWh.toFixed(0)}/MWh`);
        updateText('eng-ngcc-energy', CostModel.formatEnergy(terrestrial.energyMWh));

        // Thermal analysis outputs
        updateText('thermal-available-area', `${thermal.availableAreaKm2.toFixed(2)} km²`);
        updateText('thermal-effective-emissivity', `${thermal.effectiveEmissivity.toFixed(2)}`);
        updateText('thermal-radiator-temp', `${thermal.radiatorTempC.toFixed(1)} °C`);
        updateText('thermal-incident', `${(thermal.incidentSolarW / 1e6).toFixed(0)} MW`);
        updateText('thermal-waste-heat', `${(thermal.wasteHeatW / 1e6).toFixed(0)} MW`);
        updateText('thermal-electrical-heat', `${(thermal.electricalHeatW / 1e6).toFixed(0)} MW`);
        updateText('thermal-heat-load', `${(thermal.heatLoadW / 1e6).toFixed(0)} MW`);
        updateText('thermal-capacity', `${(thermal.capacityW / 1e6).toFixed(0)} MW`);
        
        // Margin - pass if positive (capacity > load)
        const marginEl = document.getElementById('thermal-margin');
        const marginBadgeEl = document.getElementById('thermal-margin-badge');
        if (marginEl) {
            marginEl.textContent = `${thermal.marginPct.toFixed(1)}%`;
            marginEl.classList.toggle('status-pass', thermal.marginPct >= 0);
            marginEl.classList.toggle('status-fail', thermal.marginPct < 0);
        }
        if (marginBadgeEl) {
            const pass = thermal.marginPct >= 0;
            marginBadgeEl.textContent = pass ? 'PASS' : 'FAIL';
            marginBadgeEl.classList.toggle('status-pass', pass);
            marginBadgeEl.classList.toggle('status-fail', !pass);
        }
        
        // Required temp - fail if above max die temp (physically impossible)
        const reqTempEl = document.getElementById('thermal-required-temp');
        if (reqTempEl) {
            reqTempEl.textContent = `${thermal.requiredTempC.toFixed(1)} °C`;
            const tempOk = thermal.requiredTempC <= state.maxDieTempC;
            reqTempEl.classList.toggle('status-pass', tempOk);
            reqTempEl.classList.toggle('status-fail', !tempOk);
        }
        
        // Required area - fail if significantly more than available
        const reqAreaEl = document.getElementById('thermal-required-area');
        if (reqAreaEl) {
            reqAreaEl.textContent = `${thermal.areaRequiredKm2.toFixed(2)} km²`;
            const areaOk = thermal.areaRequiredKm2 <= thermal.availableAreaKm2;
            reqAreaEl.classList.toggle('status-pass', areaOk);
            reqAreaEl.classList.toggle('status-fail', !areaOk);
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

    function positionSliderTicks() {
        document.querySelectorAll('.slider-container').forEach(container => {
            const slider = container.querySelector('input[type="range"]');
            const ticksContainer = container.querySelector('.slider-ticks');
            if (!slider || !ticksContainer) return;
            
            const min = parseFloat(slider.min);
            const max = parseFloat(slider.max);
            const range = max - min;
            
            ticksContainer.querySelectorAll('.tick').forEach(tick => {
                const value = parseFloat(tick.dataset.value);
                const percentage = ((value - min) / range) * 100;
                tick.style.left = percentage + '%';
                tick.style.position = 'absolute';
                tick.style.transform = 'translateX(-50%)';
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
        setupSlider('capacity-slider', 'capacity-fill', 'capacity-value', 1, 100, 'targetGW', v => `${v} GW`);
        
        // Years slider
        setupSlider('years-slider', 'years-fill', 'years-value', 3, 10, 'years', v => `${v} years`);
        
        // Launch cost slider
        setupSlider('launch-cost-slider', 'launch-cost-fill', 'launch-cost-value', 100, 2940, 'launchCostPerKg', v => `$${v.toLocaleString()}/kg`);
        
        // Satellite cost slider (from Starlink BOM analysis)
        setupSlider('sat-cost-slider', 'sat-cost-fill', 'sat-cost-value', 15, 40, 'satelliteCostPerW', v => `$${v}/W`);
        
        // Specific power slider (W/kg from Starlink analysis)
        setupSlider('specific-power-slider', 'specific-power-fill', 'specific-power-value', 3, 50, 'specificPowerWPerKg', v => `${v.toFixed(1)} W/kg`);
        
        // Satellite size slider (kW nameplate)
        setupSlider('sat-size-slider', 'sat-size-fill', 'sat-size-value', 5, 80, 'satellitePowerKW', v => `${v} kW`);
        
        // Sun fraction slider
        setupSlider('sun-fraction-slider', 'sun-fraction-fill', 'sun-fraction-value', 0.55, 1.0, 'sunFraction', v => `${Math.round(v * 100)}%`);
        
        // Cell degradation slider
        setupSlider('degradation-slider', 'degradation-fill', 'degradation-value', 0, 5, 'cellDegradation', v => `${v.toFixed(1)}%/yr`);
        
        // NRE cost slider
        setupSlider('nre-slider', 'nre-fill', 'nre-value', 0, 2000, 'nreCost', v => v >= 1000 ? `$${(v/1000).toFixed(1)}B` : `$${v}M`);
        
        // Terrestrial sliders (5 buckets from report)
        // CCGT turbine capex slider
        setupSlider('gas-turbine-slider', 'gas-turbine-fill', 'gas-turbine-value', 900, 1500, 'gasTurbineCapexPerKW', v => `$${v.toLocaleString()}/kW`);
        
        // Heat rate slider
        setupSlider('heat-rate-slider', 'heat-rate-fill', 'heat-rate-value', 6000, 9000, 'heatRateBtuKwh', v => `${v.toLocaleString()} BTU/kWh`);
        
        // Gas price slider
        setupSlider('gas-price-slider', 'gas-price-fill', 'gas-price-value', 2, 10, 'gasPricePerMMBtu', v => `$${v.toFixed(2)}/MMBtu`);
        
        // PUE slider
        setupSlider('pue-slider', 'pue-fill', 'pue-value', 1.05, 1.6, 'pue', v => v.toFixed(2));

        // Thermal sliders
        setupSlider('emissivity-slider', 'emissivity-fill', 'emissivity-value', 0.6, 0.98, 'emissivity', v => v.toFixed(2));
        setupSlider('albedo-slider', 'albedo-fill', 'albedo-value', 0.0, 0.5, 'albedoViewFactor', v => v.toFixed(2));
        setupSlider('die-temp-slider', 'die-temp-fill', 'die-temp-value', 60, 90, 'maxDieTempC', v => `${v.toFixed(0)} °C`);
        setupSlider('temp-drop-slider', 'temp-drop-fill', 'temp-drop-value', 5, 25, 'tempDropC', v => `${v.toFixed(0)} °C`);
        
        // Facility capex slider (combined 4 buckets: electrical + mechanical + civil + network)
        // From report: ~$12.50/W total (excluding power gen)
        const facilitySlider = document.getElementById('facility-slider');
        const facilityFill = document.getElementById('facility-fill');
        const facilityValue = document.getElementById('facility-value');
        if (facilitySlider && facilityFill && facilityValue) {
            function updateFacilitySlider() {
                const state = CostModel.getState();
                const total = state.electricalCostPerW + state.mechanicalCostPerW + state.civilCostPerW + state.networkCostPerW;
                const percentage = ((total - 8) / (18 - 8)) * 100;
                facilityFill.style.width = `${Math.max(0, Math.min(100, percentage))}%`;
                facilityValue.textContent = `$${total.toFixed(2)}/W`;
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
