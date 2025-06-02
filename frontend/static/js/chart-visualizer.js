/**
 * Vedic Astrology Chart Visualizer - Simplified and Functional
 * Creates clear, interactive birth charts with proper Vedic layout
 */

class VedicChartVisualizer {
    constructor(containerId, chartData) {
        this.containerId = containerId;
        this.chartData = chartData;
        this.p5Instance = null;
        this.chartSize = 0;
        this.centerX = 0;
        this.centerY = 0;
        this.housePositions = [];
        this.selectedHouse = null;
        this.selectedPlanet = null;
        this.isLoaded = false;

        // Vedic Chart Colors
        this.colors = {
            background: '#1a1a2e',
            chartBorder: '#6366f1',
            houseBorder: '#4f46e5',
            houseBackground: 'rgba(255, 255, 255, 0.05)',
            houseSelected: 'rgba(99, 102, 241, 0.3)',
            houseText: '#ffffff',
            planetColors: {
                'Sun': '#ff6b35',
                'Moon': '#e8e8e8',
                'Mars': '#ff4757',
                'Mercury': '#2ed573',
                'Jupiter': '#ffa502',
                'Venus': '#ff6348',
                'Saturn': '#747d8c',
                'Rahu': '#5f27cd',
                'Ketu': '#c44569'
            }
        };

        // Vedic house layout (North Indian style)
        this.houseLayout = [
            // Row 1 (top)
            {house: 12, row: 0, col: 0}, {house: 1, row: 0, col: 1}, {house: 2, row: 0, col: 2}, {house: 3, row: 0, col: 3},
            // Row 2
            {house: 11, row: 1, col: 0}, {house: 0, row: 1, col: 1, center: true}, {house: 0, row: 1, col: 2, center: true}, {house: 4, row: 1, col: 3},
            // Row 3
            {house: 10, row: 2, col: 0}, {house: 0, row: 2, col: 1, center: true}, {house: 0, row: 2, col: 2, center: true}, {house: 5, row: 2, col: 3},
            // Row 4 (bottom)
            {house: 9, row: 3, col: 0}, {house: 8, row: 3, col: 1}, {house: 7, row: 3, col: 2}, {house: 6, row: 3, col: 3}
        ];

        this.init();
    }

    init() {
        // Create p5.js sketch
        const sketch = (p) => {
            p.setup = () => this.setup(p);
            p.draw = () => this.draw(p);
            p.mouseClicked = () => this.mouseClicked(p);
            p.mouseMoved = () => this.mouseMoved(p);
            p.windowResized = () => this.windowResized(p);
        };

        this.p5Instance = new p5(sketch, this.containerId);
    }

    setup(p) {
        const container = document.getElementById(this.containerId);
        const size = Math.min(container.offsetWidth, 600);

        p.createCanvas(size, size);
        p.colorMode(p.RGB, 255);

        this.chartSize = size * 0.8; // 80% of canvas
        this.centerX = size / 2;
        this.centerY = size / 2;

        this.calculateHousePositions();
        this.isLoaded = true;
    }

    draw(p) {
        if (!this.isLoaded || !this.chartData) return;

        // Clear background
        p.background(this.colors.background);

        // Draw the Vedic chart grid
        this.drawVedicChart(p);

        // Draw house information
        this.drawHouseInfo(p);

        // Draw planets in houses
        this.drawPlanetsInHouses(p);

        // Draw chart title
        this.drawChartTitle(p);
    }

    drawVedicChart(p) {
        const startX = this.centerX - this.chartSize / 2;
        const startY = this.centerY - this.chartSize / 2;
        const cellSize = this.chartSize / 4;

        // Draw the 4x4 grid
        p.stroke(this.colors.chartBorder);
        p.strokeWeight(2);
        p.noFill();

        // Draw grid lines
        for (let i = 0; i <= 4; i++) {
            // Vertical lines
            p.line(startX + i * cellSize, startY, startX + i * cellSize, startY + this.chartSize);
            // Horizontal lines
            p.line(startX, startY + i * cellSize, startX + this.chartSize, startY + i * cellSize);
        }

        // Draw house backgrounds and numbers
        for (let layout of this.houseLayout) {
            if (layout.center) continue; // Skip center cells

            const x = startX + layout.col * cellSize;
            const y = startY + layout.row * cellSize;

            // House background
            if (this.selectedHouse === layout.house) {
                p.fill(this.colors.houseSelected);
            } else {
                p.fill(this.colors.houseBackground);
            }
            p.rect(x, y, cellSize, cellSize);

            // House number
            p.fill(this.colors.houseText);
            p.noStroke();
            p.textAlign(p.LEFT, p.TOP);
            p.textSize(12);
            p.text(layout.house, x + 5, y + 5);

            // Store position for click detection
            this.housePositions[layout.house] = {x, y, width: cellSize, height: cellSize};
        }

        // Draw center area with detailed information
        const centerX = startX + cellSize;
        const centerY = startY + cellSize;
        p.fill(this.colors.houseBackground);
        p.stroke(this.colors.chartBorder);
        p.strokeWeight(2);
        p.rect(centerX, centerY, cellSize * 2, cellSize * 2);

        // Chart information in center
        p.fill(this.colors.houseText);
        p.noStroke();
        p.textAlign(p.CENTER, p.CENTER);

        const centerCenterX = centerX + cellSize;
        const centerCenterY = centerY + cellSize;

        // Chart type (top)
        p.textSize(16);
        p.fill(255, 255, 255);
        p.text(this.getChartTypeName(this.chartData.chart_type || 'birth'),
               centerCenterX, centerCenterY - 40);

        // Birth details (if available)
        if (this.chartData.birth_info) {
            p.textSize(12);
            p.fill(200, 200, 255);
            p.text(this.chartData.birth_info.name || 'Birth Chart',
                   centerCenterX, centerCenterY - 20);

            p.textSize(9);
            p.fill(180, 180, 180);
            p.text(`${this.chartData.birth_info.birth_date} ${this.chartData.birth_info.birth_time}`,
                   centerCenterX, centerCenterY - 5);

            p.textSize(8);
            p.text(this.chartData.birth_info.birth_location,
                   centerCenterX, centerCenterY + 8);
        }

        // Ascendant information (center)
        p.textSize(14);
        p.fill(255, 200, 100);
        p.text(`Lagna: ${this.chartData.ascendant || 'Unknown'}`,
               centerCenterX, centerCenterY + 25);

        // Additional chart summary
        if (this.chartData.chart_summary) {
            p.textSize(8);
            p.fill(150, 150, 150);
            p.text(`Moon: ${this.chartData.chart_summary.moon_sign || 'Unknown'}`,
                   centerCenterX - 30, centerCenterY + 40);
            p.text(`Sun: ${this.chartData.chart_summary.sun_sign || 'Unknown'}`,
                   centerCenterX + 30, centerCenterY + 40);
        }

        // Add decorative elements
        p.stroke(this.colors.chartBorder);
        p.strokeWeight(1);
        p.noFill();
        // Decorative border
        p.rect(centerX + 8, centerY + 8, cellSize * 2 - 16, cellSize * 2 - 16);

        // Corner decorations
        p.strokeWeight(2);
        p.line(centerX + 15, centerY + 15, centerX + 25, centerY + 15);
        p.line(centerX + 15, centerY + 15, centerX + 15, centerY + 25);

        p.line(centerX + cellSize * 2 - 15, centerY + 15, centerX + cellSize * 2 - 25, centerY + 15);
        p.line(centerX + cellSize * 2 - 15, centerY + 15, centerX + cellSize * 2 - 15, centerY + 25);

        p.line(centerX + 15, centerY + cellSize * 2 - 15, centerX + 25, centerY + cellSize * 2 - 15);
        p.line(centerX + 15, centerY + cellSize * 2 - 15, centerX + 15, centerY + cellSize * 2 - 25);

        p.line(centerX + cellSize * 2 - 15, centerY + cellSize * 2 - 15, centerX + cellSize * 2 - 25, centerY + cellSize * 2 - 15);
        p.line(centerX + cellSize * 2 - 15, centerY + cellSize * 2 - 15, centerX + cellSize * 2 - 15, centerY + cellSize * 2 - 25);
    }

    drawHouseInfo(p) {
        if (!this.chartData.houses) return;

        const startX = this.centerX - this.chartSize / 2;
        const startY = this.centerY - this.chartSize / 2;
        const cellSize = this.chartSize / 4;

        // Draw house signs and additional info
        for (let layout of this.houseLayout) {
            if (layout.center) continue;

            const houseNumber = layout.house;
            const x = startX + layout.col * cellSize;
            const y = startY + layout.row * cellSize;

            // Get house sign from chart data or calculate it
            const houseSign = this.getHouseSign(houseNumber);

            // Draw sign name
            p.fill(this.colors.houseText);
            p.noStroke();
            p.textAlign(p.CENTER, p.TOP);
            p.textSize(9);
            p.text(houseSign, x + cellSize/2, y + 20);

            // Draw house significance (small text)
            p.textSize(7);
            p.fill(150, 150, 150);
            const significance = this.getHouseKeyword(houseNumber);
            p.text(significance, x + cellSize/2, y + cellSize - 15);
        }
    }

    getHouseSign(houseNumber) {
        // In a real Vedic chart, this would be calculated based on ascendant
        // For now, we'll use the ascendant as house 1 and calculate from there
        const ascendantSign = this.chartData.ascendant || 'Makara';
        const signOrder = [
            'Mesha', 'Vrishabha', 'Mithuna', 'Karka', 'Simha', 'Kanya',
            'Tula', 'Vrishchika', 'Dhanu', 'Makara', 'Kumbha', 'Meena'
        ];

        // Find ascendant index
        let ascendantIndex = signOrder.findIndex(sign => sign === ascendantSign);
        if (ascendantIndex === -1) ascendantIndex = 9; // Default to Makara

        // Calculate house sign
        const houseSignIndex = (ascendantIndex + houseNumber - 1) % 12;
        return signOrder[houseSignIndex];
    }

    getHouseKeyword(houseNumber) {
        const keywords = {
            1: 'Self', 2: 'Wealth', 3: 'Siblings', 4: 'Home',
            5: 'Children', 6: 'Health', 7: 'Marriage', 8: 'Longevity',
            9: 'Fortune', 10: 'Career', 11: 'Gains', 12: 'Loss'
        };
        return keywords[houseNumber] || '';
    }

    drawPlanetsInHouses(p) {
        if (!this.chartData.planets) return;

        const startX = this.centerX - this.chartSize / 2;
        const startY = this.centerY - this.chartSize / 2;
        const cellSize = this.chartSize / 4;

        // Group planets by house
        const planetsByHouse = {};
        for (let planet of this.chartData.planets) {
            if (!planetsByHouse[planet.house]) {
                planetsByHouse[planet.house] = [];
            }
            planetsByHouse[planet.house].push(planet);
        }

        // Draw planets in each house
        for (let houseNum in planetsByHouse) {
            const planets = planetsByHouse[houseNum];
            const layout = this.houseLayout.find(l => l.house === parseInt(houseNum));
            if (!layout || layout.center) continue;

            const x = startX + layout.col * cellSize;
            const y = startY + layout.row * cellSize;

            // Draw planets in a more organized way
            planets.forEach((planet, index) => {
                const planetsPerRow = Math.min(3, planets.length);
                const totalRows = Math.ceil(planets.length / planetsPerRow);
                const currentRow = Math.floor(index / planetsPerRow);
                const currentCol = index % planetsPerRow;

                // Calculate position to center planets in the house
                const planetSpacing = 20;
                const startX = x + (cellSize - (planetsPerRow - 1) * planetSpacing) / 2;
                const startY = y + 40 + (cellSize - 80 - (totalRows - 1) * 18) / 2;

                const planetX = startX + currentCol * planetSpacing;
                const planetY = startY + currentRow * 18;

                // Planet background circle
                p.fill(this.colors.planetColors[planet.name] || '#ffffff');
                p.stroke(0);
                p.strokeWeight(1);
                p.circle(planetX, planetY, 14);

                // Planet symbol
                p.fill(0);
                p.noStroke();
                p.textAlign(p.CENTER, p.CENTER);
                p.textSize(8);
                p.text(this.getPlanetSymbol(planet.name), planetX, planetY);

                // Add degree information if available
                if (planet.degree !== undefined) {
                    p.textSize(6);
                    p.fill(this.colors.houseText);
                    p.text(`${Math.floor(planet.degree)}°`, planetX, planetY + 12);
                }
            });
        }
    }

    drawChartTitle(p) {
        p.fill(this.colors.houseText);
        p.noStroke();
        p.textAlign(p.CENTER, p.TOP);
        p.textSize(18);
        p.text('Vedic Birth Chart', this.centerX, 20);

        if (this.chartData.chart_type && this.chartData.chart_type !== 'birth') {
            p.textSize(14);
            p.text(`(${this.getChartTypeName(this.chartData.chart_type)})`, this.centerX, 45);
        }
    }

    drawInteractiveStars(p) {
        // Static stars
        p.fill(255, 255, 255, 80);
        p.noStroke();
        for (let i = 0; i < 30; i++) {
            const x = (i * 37 + 100) % p.width;
            const y = (i * 73 + 50) % p.height;
            const size = 1 + (i % 3);
            p.circle(x, y, size);
        }

        // Mouse trail stars
        const mouseDistance = p.dist(p.mouseX, p.mouseY, p.pmouseX, p.pmouseY);
        if (mouseDistance > 2 && p.mouseX > 0 && p.mouseY > 0) {
            // Create trailing stars
            for (let i = 0; i < 5; i++) {
                const alpha = p.map(i, 0, 5, 150, 20);
                const size = p.map(i, 0, 5, 4, 1);
                const trailX = p.lerp(p.mouseX, p.pmouseX, i / 5);
                const trailY = p.lerp(p.mouseY, p.pmouseY, i / 5);

                p.fill(255, 255, 255, alpha);
                p.circle(trailX + p.random(-2, 2), trailY + p.random(-2, 2), size);
            }
        }

        // Constellation effect around mouse
        if (p.mouseX > 0 && p.mouseY > 0) {
            p.stroke(255, 255, 255, 30);
            p.strokeWeight(1);
            for (let i = 0; i < 8; i++) {
                const angle = (i / 8) * p.TWO_PI;
                const radius = 50 + p.sin(p.frameCount * 0.02 + i) * 10;
                const x = p.mouseX + p.cos(angle) * radius;
                const y = p.mouseY + p.sin(angle) * radius;
                p.line(p.mouseX, p.mouseY, x, y);

                p.fill(255, 255, 255, 60);
                p.noStroke();
                p.circle(x, y, 2);
            }
        }
    }

    drawChartBorder(p) {
        p.stroke(this.colors.chartBorder);
        p.strokeWeight(3);
        p.noFill();
        p.circle(this.centerX, this.centerY, this.chartRadius * 2);

        // Inner circle
        p.strokeWeight(1);
        p.circle(this.centerX, this.centerY, this.chartRadius * 1.6);
    }

    drawHouses(p) {
        p.strokeWeight(1);
        p.stroke(this.colors.houseBorder);

        for (let i = 0; i < 12; i++) {
            const angle1 = this.houseAngles[i];
            const angle2 = this.houseAngles[(i + 1) % 12];

            // House lines
            const x1 = this.centerX + Math.cos(angle1) * this.chartRadius * 0.8;
            const y1 = this.centerY + Math.sin(angle1) * this.chartRadius * 0.8;
            const x2 = this.centerX + Math.cos(angle1) * this.chartRadius;
            const y2 = this.centerY + Math.sin(angle1) * this.chartRadius;

            p.line(x1, y1, x2, y2);

            // House background (subtle)
            if (this.selectedHouse === i + 1) {
                p.fill(this.colors.houseBackground);
                p.noStroke();
                p.beginShape();
                p.vertex(this.centerX, this.centerY);

                const steps = 20;
                for (let j = 0; j <= steps; j++) {
                    const a = p.lerp(angle1, angle2, j / steps);
                    const x = this.centerX + Math.cos(a) * this.chartRadius;
                    const y = this.centerY + Math.sin(a) * this.chartRadius;
                    p.vertex(x, y);
                }
                p.endShape(p.CLOSE);
            }

            // House numbers
            const midAngle = (angle1 + angle2) / 2;
            const textX = this.centerX + Math.cos(midAngle) * this.chartRadius * 0.9;
            const textY = this.centerY + Math.sin(midAngle) * this.chartRadius * 0.9;

            p.fill(255, 255, 255, 180);
            p.noStroke();
            p.textAlign(p.CENTER, p.CENTER);
            p.textSize(12);
            p.text(i + 1, textX, textY);
        }
    }

    drawSigns(p) {
        const signs = [
            'Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir',
            'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis'
        ];

        p.textAlign(p.CENTER, p.CENTER);
        p.textSize(10);

        for (let i = 0; i < 12; i++) {
            const angle = (i * 30 - 90) * Math.PI / 180; // Start from Aries at top
            const x = this.centerX + Math.cos(angle) * this.chartRadius * 1.15;
            const y = this.centerY + Math.sin(angle) * this.chartRadius * 1.15;

            p.fill(this.colors.signColors[this.getFullSignName(signs[i])]);
            p.noStroke();
            p.text(signs[i], x, y);
        }
    }

    drawPlanets(p) {
        if (!this.chartData.planets) return;

        this.chartData.planets.forEach((planet, index) => {
            const angle = (planet.longitude - 90) * Math.PI / 180;
            const animatedRadius = this.chartRadius * 0.7 * this.animationProgress;
            const x = this.centerX + Math.cos(angle) * animatedRadius;
            const y = this.centerY + Math.sin(angle) * animatedRadius;

            // Planet circle
            const planetColor = this.colors.planetColors[planet.name] || '#ffffff';
            p.fill(planetColor);
            p.noStroke();

            const planetSize = this.selectedPlanet === planet.name ? 12 : 8;
            p.circle(x, y, planetSize);

            // Planet symbol/name
            p.fill(255);
            p.textAlign(p.CENTER, p.CENTER);
            p.textSize(8);
            p.text(this.getPlanetSymbol(planet.name), x, y + 15);

            // Degree text
            p.textSize(6);
            p.fill(255, 255, 255, 150);
            p.text(`${planet.longitude.toFixed(1)}°`, x, y + 25);
        });
    }

    calculateHousePositions() {
        // Initialize house positions array
        this.housePositions = {};
        // Positions will be calculated during drawing
    }

    startAnimation() {
        this.isAnimating = true;
        this.animationProgress = 0;
    }

    mouseClicked(p) {
        // Check if clicked on a house
        for (let houseNum in this.housePositions) {
            const pos = this.housePositions[houseNum];
            if (p.mouseX >= pos.x && p.mouseX <= pos.x + pos.width &&
                p.mouseY >= pos.y && p.mouseY <= pos.y + pos.height) {

                this.selectedHouse = parseInt(houseNum);
                this.showHouseInfo(parseInt(houseNum));
                return;
            }
        }

        // Clear selection if clicked elsewhere
        this.selectedHouse = null;
    }

    mouseMoved(p) {
        // Add hover effects here if needed
    }

    windowResized(p) {
        const container = document.getElementById(this.containerId);
        const width = container.offsetWidth;
        const height = Math.min(width, 600);

        p.resizeCanvas(width, height);

        this.centerX = width / 2;
        this.centerY = height / 2;
        this.chartRadius = Math.min(width, height) * 0.35;
    }

    // Helper methods
    getPlanetSymbol(planetName) {
        const symbols = {
            'Sun': 'Su',
            'Moon': 'Mo',
            'Mars': 'Ma',
            'Mercury': 'Me',
            'Jupiter': 'Ju',
            'Venus': 'Ve',
            'Saturn': 'Sa',
            'Rahu': 'Ra',
            'Ketu': 'Ke'
        };
        return symbols[planetName] || planetName.substring(0, 2);
    }

    getChartTypeName(chartType) {
        const names = {
            'navamsa': 'Navamsa D9',
            'dasamsa': 'Dasamsa D10',
            'dwadasamsa': 'Dwadasamsa D12'
        };
        return names[chartType] || chartType;
    }

    getFullSignName(shortName) {
        const signMap = {
            'Ari': 'Aries', 'Tau': 'Taurus', 'Gem': 'Gemini',
            'Can': 'Cancer', 'Leo': 'Leo', 'Vir': 'Virgo',
            'Lib': 'Libra', 'Sco': 'Scorpio', 'Sag': 'Sagittarius',
            'Cap': 'Capricorn', 'Aqu': 'Aquarius', 'Pis': 'Pisces'
        };
        return signMap[shortName] || shortName;
    }

    getPlanetAtPosition(x, y, p) {
        if (!this.chartData.planets) return null;

        for (const planet of this.chartData.planets) {
            const angle = (planet.longitude - 90) * Math.PI / 180;
            const planetX = this.centerX + Math.cos(angle) * this.chartRadius * 0.7;
            const planetY = this.centerY + Math.sin(angle) * this.chartRadius * 0.7;

            if (p.dist(x, y, planetX, planetY) < 15) {
                return planet.name;
            }
        }
        return null;
    }

    getHouseAtPosition(x, y, p) {
        const angle = Math.atan2(y - this.centerY, x - this.centerX);
        const normalizedAngle = (angle + Math.PI / 2 + 2 * Math.PI) % (2 * Math.PI);
        const house = Math.floor(normalizedAngle / (Math.PI / 6)) + 1;
        return house;
    }

    showPlanetInfo(planetName) {
        // Emit event for parent component to handle
        const event = new CustomEvent('planetSelected', {
            detail: { planet: planetName, chartData: this.chartData }
        });
        document.dispatchEvent(event);
    }

    showHouseInfo(houseNumber) {
        console.log('House clicked:', houseNumber);
        // Emit event for parent component to handle
        const event = new CustomEvent('houseSelected', {
            detail: { house: houseNumber, chartData: this.chartData }
        });
        document.dispatchEvent(event);
    }

    drawInfoPanel(p) {
        // Draw info panel for selected planet/house
        if (this.selectedPlanet || this.selectedHouse) {
            p.fill(0, 0, 0, 180);
            p.noStroke();
            p.rect(10, 10, 200, 100, 10);

            p.fill(255);
            p.textAlign(p.LEFT, p.TOP);
            p.textSize(12);

            if (this.selectedPlanet) {
                p.text(`Selected: ${this.selectedPlanet}`, 20, 25);
                p.text('Click for detailed info', 20, 45);
            } else if (this.selectedHouse) {
                p.text(`House: ${this.selectedHouse}`, 20, 25);
                p.text('Click for house details', 20, 45);
            }
        }
    }

    drawAspects(p) {
        // Draw planetary aspects (lines between planets)
        if (!this.chartData.planets || this.chartData.planets.length < 2) return;

        p.strokeWeight(1);

        for (let i = 0; i < this.chartData.planets.length; i++) {
            for (let j = i + 1; j < this.chartData.planets.length; j++) {
                const planet1 = this.chartData.planets[i];
                const planet2 = this.chartData.planets[j];

                const aspect = this.calculateAspect(planet1.longitude, planet2.longitude);
                if (aspect) {
                    const angle1 = (planet1.longitude - 90) * Math.PI / 180;
                    const angle2 = (planet2.longitude - 90) * Math.PI / 180;

                    const x1 = this.centerX + Math.cos(angle1) * this.chartRadius * 0.7;
                    const y1 = this.centerY + Math.sin(angle1) * this.chartRadius * 0.7;
                    const x2 = this.centerX + Math.cos(angle2) * this.chartRadius * 0.7;
                    const y2 = this.centerY + Math.sin(angle2) * this.chartRadius * 0.7;

                    p.stroke(aspect.color);
                    p.line(x1, y1, x2, y2);
                }
            }
        }
    }

    calculateAspect(long1, long2) {
        const diff = Math.abs(long1 - long2);
        const angle = Math.min(diff, 360 - diff);

        // Major aspects with orbs
        if (Math.abs(angle - 0) < 8) return { type: 'conjunction', color: 'rgba(255, 255, 0, 0.6)' };
        if (Math.abs(angle - 60) < 6) return { type: 'sextile', color: 'rgba(0, 255, 0, 0.6)' };
        if (Math.abs(angle - 90) < 6) return { type: 'square', color: 'rgba(255, 0, 0, 0.6)' };
        if (Math.abs(angle - 120) < 6) return { type: 'trine', color: 'rgba(0, 255, 255, 0.6)' };
        if (Math.abs(angle - 180) < 8) return { type: 'opposition', color: 'rgba(255, 0, 255, 0.6)' };

        return null;
    }

    // Public methods for external control
    toggleAspects() {
        this.chartData.showAspects = !this.chartData.showAspects;
    }

    updateChartData(newChartData) {
        this.chartData = newChartData;
        this.startAnimation();
    }

    destroy() {
        if (this.p5Instance) {
            this.p5Instance.remove();
        }
    }
}

// Export for use in other modules
window.VedicChartVisualizer = VedicChartVisualizer;
