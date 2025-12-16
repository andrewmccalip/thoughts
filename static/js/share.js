/**
 * URL Parameter Sharing System
 * 
 * Encodes/decodes model state to/from URL query parameters.
 * Only non-default values are included to keep URLs short.
 */

const UrlShare = (function() {
    'use strict';

    // Short URL param keys mapped to state keys
    // Keep these short for compact URLs
    const PARAM_MAP = {
        // Shared
        y: 'years',
        gw: 'targetGW',
        
        // Thermal
        sa: 'solarAbsorptivity',
        epv: 'emissivityPV',
        erad: 'emissivityRad',
        pve: 'pvEfficiency',
        ba: 'betaAngle',
        alt: 'orbitalAltitudeKm',
        mdt: 'maxDieTempC',
        td: 'tempDropC',
        
        // Orbital
        lc: 'launchCostPerKg',
        sc: 'satelliteCostPerW',
        sp: 'specificPowerWPerKg',
        spw: 'satellitePowerKW',
        sf: 'sunFraction',
        cd: 'cellDegradation',
        gf: 'gpuFailureRate',
        nre: 'nreCost',
        
        // Terrestrial
        gtc: 'gasTurbineCapexPerKW',
        ec: 'electricalCostPerW',
        mc: 'mechanicalCostPerW',
        cc: 'civilCostPerW',
        nc: 'networkCostPerW',
        pue: 'pue',
        gp: 'gasPricePerMMBtu',
        hr: 'heatRateBtuKwh',
        cf: 'capacityFactor'
    };

    // Default values - must match math.js state defaults
    const DEFAULTS = {
        years: 5,
        targetGW: 1,
        solarAbsorptivity: 0.92,
        emissivityPV: 0.85,
        emissivityRad: 0.90,
        pvEfficiency: 0.22,
        betaAngle: 90,
        orbitalAltitudeKm: 550,
        maxDieTempC: 85,
        tempDropC: 10,
        launchCostPerKg: 500,
        satelliteCostPerW: 22,
        specificPowerWPerKg: 36.5,
        satellitePowerKW: 27,
        sunFraction: 0.98,
        cellDegradation: 2.5,
        gpuFailureRate: 9,
        nreCost: 1000,
        gasTurbineCapexPerKW: 1800,
        electricalCostPerW: 5.25,
        mechanicalCostPerW: 3.0,
        civilCostPerW: 2.5,
        networkCostPerW: 1.75,
        pue: 1.2,
        gasPricePerMMBtu: 4.30,
        heatRateBtuKwh: 6200,
        capacityFactor: 0.85
    };

    // Reverse map: state key -> short param
    const STATE_TO_PARAM = Object.fromEntries(
        Object.entries(PARAM_MAP).map(([k, v]) => [v, k])
    );

    /**
     * Generate shareable URL with current non-default state
     */
    function generateUrl() {
        const state = CostModel.getState();
        const params = new URLSearchParams();

        for (const [stateKey, defaultVal] of Object.entries(DEFAULTS)) {
            const currentVal = state[stateKey];
            // Only include if different from default (with float tolerance)
            if (Math.abs(currentVal - defaultVal) > 1e-9) {
                const shortKey = STATE_TO_PARAM[stateKey];
                // Round to reasonable precision to keep URLs clean
                const val = Number.isInteger(currentVal) ? currentVal : 
                            parseFloat(currentVal.toPrecision(6));
                params.set(shortKey, val);
            }
        }

        const queryString = params.toString();
        return window.location.origin + window.location.pathname + 
               (queryString ? '?' + queryString : '');
    }

    /**
     * Parse URL and apply parameters to model state
     */
    function applyUrlParams() {
        const params = new URLSearchParams(window.location.search);
        if (params.toString() === '') return false;

        const updates = {};
        for (const [shortKey, stateKey] of Object.entries(PARAM_MAP)) {
            if (params.has(shortKey)) {
                updates[stateKey] = parseFloat(params.get(shortKey));
            }
        }

        if (Object.keys(updates).length > 0) {
            // Merge with current state
            const currentState = CostModel.getState();
            CostModel.setState({ ...currentState, ...updates });
            return true;
        }
        return false;
    }

    /**
     * Sync slider UI elements to match current model state
     */
    function syncSlidersToState() {
        const state = CostModel.getState();
        
        // Map of slider IDs to state keys
        const sliderMap = {
            'capacity-slider': 'targetGW',
            'years-slider': 'years',
            'launch-cost-slider': 'launchCostPerKg',
            'sat-cost-slider': 'satelliteCostPerW',
            'specific-power-slider': 'specificPowerWPerKg',
            'sat-size-slider': 'satellitePowerKW',
            'sun-fraction-slider': 'sunFraction',
            'degradation-slider': 'cellDegradation',
            'gpu-failure-slider': 'gpuFailureRate',
            'nre-slider': 'nreCost',
            'heat-rate-slider': 'heatRateBtuKwh',
            'gas-price-slider': 'gasPricePerMMBtu',
            'pue-slider': 'pue',
            'solar-absorptivity-slider': 'solarAbsorptivity',
            'emissivity-pv-slider': 'emissivityPV',
            'emissivity-rad-slider': 'emissivityRad',
            'pv-efficiency-slider': 'pvEfficiency',
            'beta-angle-slider': 'betaAngle',
            'altitude-slider': 'orbitalAltitudeKm',
            'die-temp-slider': 'maxDieTempC',
            'temp-drop-slider': 'tempDropC'
        };

        for (const [sliderId, stateKey] of Object.entries(sliderMap)) {
            const slider = document.getElementById(sliderId);
            if (slider && state[stateKey] !== undefined) {
                slider.value = state[stateKey];
                // Trigger input event to update fill and display
                slider.dispatchEvent(new Event('input'));
            }
        }

        // Special handling for gas turbine slider (uses $/W display but stores $/kW)
        const gasTurbineSlider = document.getElementById('gas-turbine-slider');
        if (gasTurbineSlider && state.gasTurbineCapexPerKW !== undefined) {
            gasTurbineSlider.value = state.gasTurbineCapexPerKW / 1000;
            gasTurbineSlider.dispatchEvent(new Event('input'));
        }

        // Special handling for facility slider (derived from component costs)
        const facilitySlider = document.getElementById('facility-slider');
        if (facilitySlider) {
            const total = state.electricalCostPerW + state.mechanicalCostPerW + 
                         state.civilCostPerW + state.networkCostPerW;
            facilitySlider.value = total;
            facilitySlider.dispatchEvent(new Event('input'));
        }
    }

    /**
     * Create and inject the share button
     */
    function createShareButton() {
        const btn = document.createElement('button');
        btn.id = 'share-btn';
        btn.className = 'share-button';
        btn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="18" cy="5" r="3"></circle>
                <circle cx="6" cy="12" r="3"></circle>
                <circle cx="18" cy="19" r="3"></circle>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
            </svg>
            <span class="share-text">Share</span>
        `;

        btn.addEventListener('click', async function() {
            const url = generateUrl();
            
            try {
                await navigator.clipboard.writeText(url);
                btn.classList.add('copied');
                btn.querySelector('.share-text').textContent = 'Copied!';
                
                setTimeout(() => {
                    btn.classList.remove('copied');
                    btn.querySelector('.share-text').textContent = 'Share';
                }, 2000);
            } catch (err) {
                // Fallback: select a temporary input
                const input = document.createElement('input');
                input.value = url;
                document.body.appendChild(input);
                input.select();
                document.execCommand('copy');
                document.body.removeChild(input);
                
                btn.classList.add('copied');
                btn.querySelector('.share-text').textContent = 'Copied!';
                setTimeout(() => {
                    btn.classList.remove('copied');
                    btn.querySelector('.share-text').textContent = 'Share';
                }, 2000);
            }
        });

        // Position button based on viewport
        function positionButton() {
            const mobileSlot = document.getElementById('mobile-share-slot');
            const isMobile = window.innerWidth <= 1500;
            
            if (isMobile && mobileSlot && btn.parentElement !== mobileSlot) {
                mobileSlot.appendChild(btn);
            } else if (!isMobile && btn.parentElement !== document.body) {
                document.body.appendChild(btn);
            }
        }

        // Initial placement
        document.body.appendChild(btn);
        positionButton();

        // Reposition on resize
        window.addEventListener('resize', positionButton);
    }

    /**
     * Initialize: parse URL, sync UI, create button
     */
    function init() {
        // Wait for DOM and CostModel to be ready
        const doInit = () => {
            const hadParams = applyUrlParams();
            if (hadParams) {
                syncSlidersToState();
            }
            createShareButton();
        };

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', doInit);
        } else {
            doInit();
        }
    }

    return {
        init,
        generateUrl,
        applyUrlParams,
        syncSlidersToState,
        DEFAULTS
    };
})();

// Auto-initialize
UrlShare.init();

