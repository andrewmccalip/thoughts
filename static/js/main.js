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
        const natgas = CostModel.calculateNatGas();
        const breakeven = CostModel.calculateBreakeven();
        const state = CostModel.getState();
        const constants = CostModel.getConstants();
        
        // Find max values for bar scaling
        const maxCost = Math.max(
            orbital.hardwareCost,
            orbital.launchCost,
            natgas.capexTotal,
            natgas.fuelCostTotal,
            natgas.omCostTotal,
            natgas.landCostTotal
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
        
        // Update NatGas display
        updateText('ngcc-total', CostModel.formatCost(natgas.totalCost));
        updateText('ngcc-capex-value', CostModel.formatCost(natgas.capexTotal));
        updateText('ngcc-fuel-value', CostModel.formatCost(natgas.fuelCostTotal));
        updateText('ngcc-om-value', CostModel.formatCost(natgas.omCostTotal));
        updateText('ngcc-land-value', CostModel.formatCost(natgas.landCostTotal));
        updateText('ngcc-hours', CostModel.formatHours(natgas.totalHours));
        updateText('ngcc-cpw', `$${natgas.costPerW.toFixed(2)}/W`);
        updateText('ngcc-energy', CostModel.formatEnergy(natgas.energyMWh));
        updateText('ngcc-lcoe', CostModel.formatLCOE(natgas.lcoe));
        updateText('ngcc-overhead', CostModel.formatCost(natgas.overheadCost));
        updateText('ngcc-maintenance', CostModel.formatCost(natgas.maintenanceCost));
        updateText('ngcc-comms', CostModel.formatCost(natgas.commsCost));
        
        // Update NatGas bars
        document.getElementById('ngcc-capex-bar').style.width = `${(natgas.capexTotal / maxCost) * 100}%`;
        document.getElementById('ngcc-fuel-bar').style.width = `${(natgas.fuelCostTotal / maxCost) * 100}%`;
        document.getElementById('ngcc-om-bar').style.width = `${(natgas.omCostTotal / maxCost) * 100}%`;
        document.getElementById('ngcc-land-bar').style.width = `${(natgas.landCostTotal / maxCost) * 100}%`;
        
        // Update breakeven
        updateText('breakeven-launch', CostModel.formatCostPerKg(breakeven));
        
        // Update header subtitle and footer
        updateText('years-display', state.years);
        updateText('footer-sun', `${Math.round(state.sunFraction * 100)}%`);
        
        // Update assumptions
        updateText('assumption-years', `${state.years} years`);
        updateText('assumption-mass', CostModel.formatMass(orbital.totalMassKg));
        updateText('assumption-specific-power', `${state.specificPowerWPerKg} W/kg`);
        
        // Update reading panel values
        updateText('reading-years', state.years);
        updateText('reading-years-2', state.years);
        updateText('reading-sat-cost', state.satelliteCostPerW);
        updateText('reading-launch-cost', state.launchCostPerKg.toLocaleString());
        updateText('reading-launch-cost-2', state.launchCostPerKg.toLocaleString());
        updateText('reading-mass', (orbital.totalMassKg / 1e6).toFixed(1));
        updateText('reading-launch-total', CostModel.formatCost(orbital.launchCost));
        updateText('reading-hardware-total', CostModel.formatCost(orbital.hardwareCost));
        updateText('reading-capex', state.capexPerKW);
        updateText('reading-fuel', state.fuelCostPerMWh);
        updateText('reading-orbital-total', CostModel.formatCost(orbital.totalCost));
        updateText('reading-ngcc-total', CostModel.formatCost(natgas.totalCost));
        
        // Update engineering outputs - Orbital
        updateText('eng-orbital-mass', CostModel.formatMass(orbital.totalMassKg));
        updateText('eng-orbital-specific-power', `${state.specificPowerWPerKg} W/kg`);
        updateText('eng-orbital-array-area', `${orbital.arrayAreaKm2.toFixed(1)} km²`);
        updateText('eng-orbital-sat-count', `~${orbital.satelliteCount.toLocaleString()}`);
        updateText('eng-orbital-launches', `~${orbital.starshipLaunches.toLocaleString()}`);
        updateText('eng-orbital-lox', `${(orbital.loxGallons / 1e6).toFixed(0)}M gal`);
        updateText('eng-orbital-methane', `${(orbital.methaneGallons / 1e6).toFixed(0)}M gal`);
        updateText('eng-orbital-energy', CostModel.formatEnergy(orbital.energyMWh));
        
        // Update engineering outputs - NatGas
        updateText('eng-ngcc-footprint', `${constants.NGCC_ACRES} acres`);
        updateText('eng-ngcc-turbines', `${natgas.turbineCount} units`);
        updateText('eng-ngcc-heat-rate', `${constants.NGCC_HEAT_RATE_BTU_KWH.toLocaleString()} BTU/kWh`);
        updateText('eng-ngcc-gas-consumption', `${natgas.gasConsumptionBCF.toFixed(0)} BCF`);
        updateText('eng-ngcc-energy', CostModel.formatEnergy(natgas.energyMWh));
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
    
    function init() {
        // Years slider
        setupSlider('years-slider', 'years-fill', 'years-value', 3, 10, 'years', v => `${v} years`);
        
        // Launch cost slider
        setupSlider('launch-cost-slider', 'launch-cost-fill', 'launch-cost-value', 100, 2940, 'launchCostPerKg', v => `$${v.toLocaleString()}/kg`);
        
        // Satellite cost slider
        setupSlider('sat-cost-slider', 'sat-cost-fill', 'sat-cost-value', 4, 18, 'satelliteCostPerW', v => `$${v}/W`);
        
        // Specific power slider
        setupSlider('specific-power-slider', 'specific-power-fill', 'specific-power-value', 3, 100, 'specificPowerWPerKg', v => `${v} W/kg`);
        
        // Sun fraction slider
        setupSlider('sun-fraction-slider', 'sun-fraction-fill', 'sun-fraction-value', 0.55, 1.0, 'sunFraction', v => `${Math.round(v * 100)}%`);
        
        // NatGas Capex slider
        setupSlider('capex-slider', 'capex-fill', 'capex-value', 400, 2000, 'capexPerKW', v => `$${v.toLocaleString()}/kW`);
        
        // Fuel cost slider
        setupSlider('fuel-cost-slider', 'fuel-cost-fill', 'fuel-cost-value', 10, 100, 'fuelCostPerMWh', v => `$${v}/MWh`);
        
        // O&M cost slider
        setupSlider('om-cost-slider', 'om-cost-fill', 'om-cost-value', 2, 20, 'omCostPerMWh', v => `$${v}/MWh`);
        
        // Land cost slider
        setupSlider('land-cost-slider', 'land-cost-fill', 'land-cost-value', 5, 200, 'landCostPerAcre', v => `$${v}k/acre`);
        
        // Initial UI update
        updateUI();
        
        // Load references
        loadReferences();
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
