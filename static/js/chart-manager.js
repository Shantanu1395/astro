/**
 * Chart Manager - Handles chart data integration and UI interactions
 * Bridges between backend data and p5.js visualization
 */

class ChartManager {
    constructor() {
        this.currentChart = null;
        this.chartVisualizer = null;
        this.chartData = null;
        this.divisionalCharts = {};
        this.currentChartType = 'birth'; // birth, navamsa, dasamsa, etc.

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.createChartContainer();
    }

    setupEventListeners() {
        // Listen for planet selection events
        document.addEventListener('planetSelected', (event) => {
            this.handlePlanetSelection(event.detail);
        });

        // Listen for house selection events
        document.addEventListener('houseSelected', (event) => {
            this.handleHouseSelection(event.detail);
        });

        // Chart type switching
        document.addEventListener('chartTypeChanged', (event) => {
            this.switchChartType(event.detail.chartType);
        });
    }

    createChartContainer() {
        // Create chart container if it doesn't exist
        if (!document.getElementById('chart-container')) {
            const container = document.createElement('div');
            container.id = 'chart-container';
            container.className = 'chart-visualization-container';

            // Add to results section
            const resultsSection = document.querySelector('.results-section');
            if (resultsSection) {
                resultsSection.insertBefore(container, resultsSection.firstChild);
            }
        }
    }

    async loadChartData(birthData) {
        try {
            console.log('🔄 Loading chart data for:', birthData);

            // Get chart data from backend
            const response = await fetch('/api/chart-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(birthData)
            });

            console.log('📡 API Response status:', response.status);

            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }

            const responseData = await response.json();
            console.log('📊 Received chart data:', responseData);

            if (responseData.status === 'success') {
                this.chartData = responseData.chart_data;
                this.processChartData();
                this.renderChart();
                console.log('✅ Chart loaded successfully');
            } else {
                throw new Error(responseData.error || 'Unknown API error');
            }

        } catch (error) {
            console.error('❌ Error loading chart data:', error);
            this.showError(`Failed to load chart data: ${error.message}`);
        }
    }

    processChartData() {
        if (!this.chartData) {
            console.warn('⚠️ No chart data to process');
            return;
        }

        console.log('🔄 Processing chart data:', this.chartData);

        // Process planets data for visualization
        if (this.chartData.planets) {
            this.chartData.planets = this.chartData.planets.map(planet => ({
                name: planet.name,
                longitude: planet.longitude,
                sign: planet.sign,
                house: planet.house,
                degree: planet.degree || (planet.longitude % 30),
                retrograde: planet.retrograde || false
            }));
            console.log('✅ Processed planets:', this.chartData.planets.length);
        }

        // Process houses data - create proper house structure
        if (this.chartData.houses) {
            // If houses is an object (house number -> planets array)
            if (typeof this.chartData.houses === 'object' && !Array.isArray(this.chartData.houses)) {
                this.chartData.houses = Object.entries(this.chartData.houses).map(([number, planets]) => ({
                    number: parseInt(number),
                    planets: planets || [],
                    sign: this.getHouseSign(parseInt(number))
                }));
            } else if (Array.isArray(this.chartData.houses)) {
                // Ensure each house has proper structure
                this.chartData.houses = this.chartData.houses.map((house, index) => ({
                    number: house.number || (index + 1),
                    sign: house.sign || this.getHouseSign(house.number || (index + 1)),
                    planets: house.planets || []
                }));
            }
            console.log('✅ Processed houses:', this.chartData.houses.length);
        } else {
            // Create houses from planet data if houses not provided
            this.chartData.houses = this.createHousesFromPlanets();
            console.log('✅ Created houses from planets:', this.chartData.houses.length);
        }

        // Add visualization settings
        this.chartData.showAspects = false;
        this.chartData.showDegrees = true;
        this.chartData.showRetrograde = true;

        console.log('✅ Chart data processing complete');
    }

    renderChart() {
        if (!this.chartData) return;

        // Hide loading message
        this.hideLoadingMessage();

        // Destroy existing chart
        if (this.chartVisualizer) {
            this.chartVisualizer.destroy();
        }

        // Create new chart visualization
        this.chartVisualizer = new VedicChartVisualizer('chart-container', this.chartData);

        // Add chart controls
        this.addChartControls();
    }

    hideLoadingMessage() {
        const container = document.getElementById('chart-container');
        if (!container) return;

        // Remove all loading-related elements
        const loadingElements = container.querySelectorAll('.chart-loading, .chart-loading-spinner');
        loadingElements.forEach(element => {
            element.style.display = 'none';
            element.remove();
        });

        // Remove any loading text (more comprehensive search)
        const allTextElements = container.querySelectorAll('p, div, span');
        allTextElements.forEach(element => {
            const text = element.textContent.toLowerCase();
            if (text.includes('loading') || text.includes('cosmic') || text.includes('preparing')) {
                element.style.display = 'none';
                element.remove();
            }
        });

        // Clear container if it only contains loading elements
        if (container.children.length === 0 ||
            (container.children.length === 1 && container.children[0].classList.contains('chart-loading'))) {
            container.innerHTML = '';
        }

        console.log('🧹 Loading message hidden, container cleared');
    }

    addChartControls() {
        const container = document.getElementById('chart-container');
        if (!container) return;

        // Remove existing controls
        const existingControls = container.querySelector('.chart-controls');
        if (existingControls) {
            existingControls.remove();
        }

        // Create controls panel
        const controls = document.createElement('div');
        controls.className = 'chart-controls';
        controls.innerHTML = `
            <div class="chart-controls-panel">
                <div class="chart-type-selector">
                    <label>Chart Type:</label>
                    <select id="chart-type-select">
                        <option value="birth">Birth Chart (D1)</option>
                        <option value="navamsa">Navamsa (D9)</option>
                        <option value="dasamsa">Dasamsa (D10)</option>
                        <option value="dwadasamsa">Dwadasamsa (D12)</option>
                    </select>
                </div>

                <div class="chart-options">
                    <label>
                        <input type="checkbox" id="show-aspects"> Show Aspects
                    </label>
                    <label>
                        <input type="checkbox" id="show-degrees" checked> Show Degrees
                    </label>
                    <label>
                        <input type="checkbox" id="show-transits"> Show Current Transits
                    </label>
                </div>

                <div class="chart-actions">
                    <button id="reset-chart" class="chart-btn">Reset View</button>
                    <button id="export-chart" class="chart-btn">Export Chart</button>
                    <button id="fullscreen-chart" class="chart-btn">Fullscreen</button>
                </div>
            </div>
        `;

        container.appendChild(controls);
        this.bindControlEvents();
    }

    bindControlEvents() {
        // Chart type selector
        const chartTypeSelect = document.getElementById('chart-type-select');
        if (chartTypeSelect) {
            chartTypeSelect.addEventListener('change', (e) => {
                this.switchChartType(e.target.value);
            });
        }

        // Aspects toggle
        const aspectsToggle = document.getElementById('show-aspects');
        if (aspectsToggle) {
            aspectsToggle.addEventListener('change', (e) => {
                if (this.chartVisualizer && this.chartData) {
                    this.chartData.showAspects = e.target.checked;
                    this.chartVisualizer.updateChartData(this.chartData);
                }
            });
        }

        // Degrees toggle
        const degreesToggle = document.getElementById('show-degrees');
        if (degreesToggle) {
            degreesToggle.addEventListener('change', (e) => {
                if (this.chartVisualizer && this.chartData) {
                    this.chartData.showDegrees = e.target.checked;
                    this.chartVisualizer.updateChartData(this.chartData);
                }
            });
        }

        // Transits toggle
        const transitsToggle = document.getElementById('show-transits');
        if (transitsToggle) {
            transitsToggle.addEventListener('change', (e) => {
                this.toggleTransits(e.target.checked);
            });
        }

        // Reset chart
        const resetBtn = document.getElementById('reset-chart');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.resetChart();
            });
        }

        // Export chart
        const exportBtn = document.getElementById('export-chart');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportChart();
            });
        }

        // Fullscreen
        const fullscreenBtn = document.getElementById('fullscreen-chart');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => {
                this.toggleFullscreen();
            });
        }
    }

    async switchChartType(chartType) {
        this.currentChartType = chartType;

        if (chartType === 'birth') {
            // Use existing birth chart data
            this.renderChart();
        } else {
            // Load divisional chart data
            await this.loadDivisionalChart(chartType);
        }
    }

    async loadDivisionalChart(chartType) {
        try {
            const response = await fetch(`/api/divisional-chart/${chartType}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(window.birthData) // Use global birth data
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch ${chartType} chart`);
            }

            const divisionalData = await response.json();
            this.divisionalCharts[chartType] = divisionalData;

            // Update chart with divisional data
            this.chartData = {
                ...this.chartData,
                planets: divisionalData.planets,
                houses: divisionalData.houses
            };

            this.chartVisualizer.updateChartData(this.chartData);

        } catch (error) {
            console.error(`Error loading ${chartType} chart:`, error);
            this.showError(`Failed to load ${chartType} chart`);
        }
    }

    async toggleTransits(show) {
        if (show) {
            await this.loadCurrentTransits();
        } else {
            this.hideTransits();
        }
    }

    async loadCurrentTransits() {
        try {
            const response = await fetch('/api/current-transits', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(window.birthData)
            });

            if (!response.ok) {
                throw new Error('Failed to fetch current transits');
            }

            const transitsData = await response.json();

            // Add transit planets to chart data
            this.chartData.transitPlanets = transitsData.current_positions;
            this.chartVisualizer.updateChartData(this.chartData);

        } catch (error) {
            console.error('Error loading transits:', error);
            this.showError('Failed to load current transits');
        }
    }

    hideTransits() {
        if (this.chartData.transitPlanets) {
            delete this.chartData.transitPlanets;
            this.chartVisualizer.updateChartData(this.chartData);
        }
    }

    resetChart() {
        if (this.chartVisualizer) {
            // Reset chart data to original state
            if (this.chartData) {
                this.chartData.showAspects = false;
                this.chartData.showDegrees = true;
                delete this.chartData.transitPlanets;

                // Update UI controls
                const aspectsToggle = document.getElementById('show-aspects');
                const degreesToggle = document.getElementById('show-degrees');
                const transitsToggle = document.getElementById('show-transits');

                if (aspectsToggle) aspectsToggle.checked = false;
                if (degreesToggle) degreesToggle.checked = true;
                if (transitsToggle) transitsToggle.checked = false;

                // Reset chart type to birth chart
                const chartTypeSelect = document.getElementById('chart-type-select');
                if (chartTypeSelect) chartTypeSelect.value = 'birth';

                // Update visualization
                this.chartVisualizer.updateChartData(this.chartData);
                this.chartVisualizer.startAnimation();
            }
        }
    }

    exportChart() {
        if (this.chartVisualizer && this.chartVisualizer.p5Instance) {
            this.chartVisualizer.p5Instance.save('vedic-chart.png');
        }
    }

    toggleFullscreen() {
        const container = document.getElementById('chart-container');
        if (!container) return;

        if (!document.fullscreenElement) {
            container.requestFullscreen().catch(err => {
                console.error('Error attempting to enable fullscreen:', err);
            });
        } else {
            document.exitFullscreen();
        }
    }

    handlePlanetSelection(detail) {
        const { planet, chartData } = detail;

        // Show planet information panel
        this.showPlanetInfo(planet);

        // Highlight planet in other UI elements
        this.highlightPlanetInUI(planet);
    }

    handleHouseSelection(detail) {
        const { house, chartData } = detail;

        // Show house information panel
        this.showHouseInfo(house);

        // Highlight house in other UI elements
        this.highlightHouseInUI(house);
    }

    showPlanetInfo(planetName) {
        // Find planet data
        const planet = this.chartData.planets.find(p => p.name === planetName);
        if (!planet) return;

        // Create or update info panel
        this.updateInfoPanel({
            type: 'planet',
            title: `${planetName}`,
            content: `
                <div class="planet-info">
                    <p><strong>Sign:</strong> ${planet.sign}</p>
                    <p><strong>House:</strong> ${planet.house}</p>
                    <p><strong>Degree:</strong> ${planet.degree}°</p>
                    ${planet.retrograde ? '<p><strong>Status:</strong> Retrograde</p>' : ''}
                    <p><strong>Longitude:</strong> ${planet.longitude.toFixed(2)}°</p>
                </div>
            `
        });
    }

    showHouseInfo(houseNumber) {
        // Find house data
        const house = this.chartData.houses.find(h => h.number === houseNumber);
        if (!house) return;

        // Get detailed house analysis from our existing analysis
        const houseAnalysis = this.getDetailedHouseAnalysis(houseNumber);

        // Create or update info panel
        this.updateInfoPanel({
            type: 'house',
            title: `House ${houseNumber} - ${this.getHouseName(houseNumber)}`,
            content: `
                <div class="house-info">
                    <p><strong>Sign:</strong> ${house.sign}</p>
                    <p><strong>Planets:</strong> ${house.planets.length > 0 ? house.planets.join(', ') : 'Empty'}</p>
                    <p><strong>Significance:</strong> ${this.getHouseSignificance(houseNumber)}</p>
                    <div class="house-analysis">
                        <h5>Analysis:</h5>
                        <p>${houseAnalysis}</p>
                    </div>
                    <div class="house-themes">
                        <h5>Key Themes:</h5>
                        <ul>
                            ${this.getHouseThemes(houseNumber).map(theme => `<li>${theme}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `
        });
    }

    getHouseName(houseNumber) {
        const houseNames = {
            1: 'Ascendant (Lagna)',
            2: 'Wealth & Family',
            3: 'Siblings & Courage',
            4: 'Home & Mother',
            5: 'Children & Creativity',
            6: 'Health & Service',
            7: 'Marriage & Partnership',
            8: 'Transformation & Longevity',
            9: 'Fortune & Dharma',
            10: 'Career & Reputation',
            11: 'Gains & Friends',
            12: 'Loss & Spirituality'
        };
        return houseNames[houseNumber] || 'Unknown';
    }

    getDetailedHouseAnalysis(houseNumber) {
        // This would ideally come from the backend analysis
        // For now, provide basic analysis based on planets in house
        const house = this.chartData.houses.find(h => h.number === houseNumber);
        if (!house || house.planets.length === 0) {
            return `This house is empty, which means its themes are expressed through the sign ruler and aspects from other planets.`;
        }

        const planetAnalysis = house.planets.map(planet => {
            return `${planet} brings its energy to this house area`;
        }).join('. ');

        return `${planetAnalysis}. This creates a focus on ${this.getHouseSignificance(houseNumber).toLowerCase()}.`;
    }

    getHouseThemes(houseNumber) {
        const themes = {
            1: ['Physical appearance', 'Personality', 'First impressions', 'Overall vitality'],
            2: ['Money and possessions', 'Family values', 'Speech and communication', 'Food and eating habits'],
            3: ['Siblings and neighbors', 'Short journeys', 'Courage and initiative', 'Communication skills'],
            4: ['Home and property', 'Mother and maternal figures', 'Emotional security', 'Education foundation'],
            5: ['Children and creativity', 'Romance and love affairs', 'Intelligence and wisdom', 'Speculation and investments'],
            6: ['Health and disease', 'Daily work and service', 'Enemies and obstacles', 'Pets and small animals'],
            7: ['Marriage and partnerships', 'Business relationships', 'Open enemies', 'Legal matters'],
            8: ['Longevity and death', 'Transformation and rebirth', 'Occult and mysteries', 'Shared resources'],
            9: ['Higher learning and philosophy', 'Long journeys and foreign lands', 'Father and paternal figures', 'Luck and fortune'],
            10: ['Career and profession', 'Reputation and status', 'Authority and government', 'Public image'],
            11: ['Gains and income', 'Friends and social circles', 'Hopes and aspirations', 'Elder siblings'],
            12: ['Loss and expenditure', 'Foreign lands and isolation', 'Spirituality and moksha', 'Hidden enemies']
        };
        return themes[houseNumber] || ['Unknown themes'];
    }

    updateInfoPanel(info) {
        // Remove existing info panel
        const existingPanel = document.querySelector('.chart-info-panel');
        if (existingPanel) {
            existingPanel.remove();
        }

        // Create new info panel
        const panel = document.createElement('div');
        panel.className = 'chart-info-panel';
        panel.innerHTML = `
            <div class="info-panel-header">
                <h4>${info.title}</h4>
                <button class="close-panel">&times;</button>
            </div>
            <div class="info-panel-content">
                ${info.content}
            </div>
        `;

        // Add to chart container
        const container = document.getElementById('chart-container');
        if (container) {
            container.appendChild(panel);

            // Bind close event
            const closeBtn = panel.querySelector('.close-panel');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    panel.remove();
                });
            }
        }
    }

    getHouseSignificance(houseNumber) {
        const significances = {
            1: 'Self, personality, physical body',
            2: 'Wealth, family, speech',
            3: 'Siblings, courage, communication',
            4: 'Home, mother, happiness',
            5: 'Children, creativity, intelligence',
            6: 'Health, enemies, service',
            7: 'Marriage, partnerships, business',
            8: 'Longevity, transformation, occult',
            9: 'Fortune, dharma, higher learning',
            10: 'Career, reputation, authority',
            11: 'Gains, friends, aspirations',
            12: 'Loss, spirituality, foreign lands'
        };

        return significances[houseNumber] || 'Unknown';
    }

    highlightPlanetInUI(planetName) {
        // Highlight planet in prediction text or other UI elements
        const planetElements = document.querySelectorAll(`[data-planet="${planetName}"]`);
        planetElements.forEach(el => {
            el.classList.add('highlighted');
            setTimeout(() => el.classList.remove('highlighted'), 3000);
        });
    }

    highlightHouseInUI(houseNumber) {
        // Highlight house in prediction text or other UI elements
        const houseElements = document.querySelectorAll(`[data-house="${houseNumber}"]`);
        houseElements.forEach(el => {
            el.classList.add('highlighted');
            setTimeout(() => el.classList.remove('highlighted'), 3000);
        });
    }

    getHouseSign(houseNumber) {
        // This is a simplified approach - in reality, house signs depend on ascendant
        // For now, we'll use a basic mapping
        const signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ];
        return signs[(houseNumber - 1) % 12];
    }

    createHousesFromPlanets() {
        const houses = [];

        // Create 12 empty houses
        for (let i = 1; i <= 12; i++) {
            houses.push({
                number: i,
                sign: this.getHouseSign(i),
                planets: []
            });
        }

        // Add planets to their respective houses
        if (this.chartData.planets) {
            this.chartData.planets.forEach(planet => {
                const houseIndex = planet.house - 1;
                if (houseIndex >= 0 && houseIndex < 12) {
                    houses[houseIndex].planets.push(planet.name);
                }
            });
        }

        return houses;
    }

    showError(message) {
        console.error(message);

        // Show error in UI
        const container = document.getElementById('chart-container');
        if (container) {
            container.innerHTML = `
                <div class="chart-error">
                    <h3>Chart Visualization Error</h3>
                    <p>${message}</p>
                    <button onclick="location.reload()">Retry</button>
                </div>
            `;
        }
    }

    destroy() {
        if (this.chartVisualizer) {
            this.chartVisualizer.destroy();
        }
    }
}

// Initialize chart manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.chartManager = new ChartManager();
});

// Export for global access
window.ChartManager = ChartManager;
