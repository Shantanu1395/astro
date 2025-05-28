/**
 * Planetary Analysis Component
 * Shows detailed planetary information with house and zodiac details
 */

class PlanetaryAnalysis {
    constructor(containerId) {
        this.containerId = containerId;
        this.chartData = null;
        this.analysisData = null;
        this.init();
    }
    
    init() {
        this.createAnalysisContainer();
        this.bindEvents();
    }
    
    createAnalysisContainer() {
        const container = document.getElementById(this.containerId);
        if (!container) return;
        
        container.innerHTML = `
            <div class="planetary-analysis-container">
                <div class="analysis-header">
                    <h3>🪐 Planetary Analysis</h3>
                    <p>Click on planets in the chart or select from the list below</p>
                </div>
                
                <div class="planet-selector">
                    <div class="planet-buttons">
                        <button class="planet-btn" data-planet="Sun">☉ Sun</button>
                        <button class="planet-btn" data-planet="Moon">☽ Moon</button>
                        <button class="planet-btn" data-planet="Mars">♂ Mars</button>
                        <button class="planet-btn" data-planet="Mercury">☿ Mercury</button>
                        <button class="planet-btn" data-planet="Jupiter">♃ Jupiter</button>
                        <button class="planet-btn" data-planet="Venus">♀ Venus</button>
                        <button class="planet-btn" data-planet="Saturn">♄ Saturn</button>
                        <button class="planet-btn" data-planet="Rahu">☊ Rahu</button>
                        <button class="planet-btn" data-planet="Ketu">☋ Ketu</button>
                    </div>
                </div>
                
                <div class="planet-details" id="planet-details">
                    <div class="no-selection">
                        <p>Select a planet to see detailed analysis</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    bindEvents() {
        // Listen for planet button clicks
        const planetButtons = document.querySelectorAll('.planet-btn');
        planetButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const planetName = e.target.dataset.planet;
                this.showPlanetAnalysis(planetName);
                this.setActiveButton(e.target);
            });
        });
        
        // Listen for chart planet selections
        document.addEventListener('planetSelected', (event) => {
            this.showPlanetAnalysis(event.detail.planet);
            this.setActiveButtonByName(event.detail.planet);
        });
    }
    
    setActiveButton(button) {
        // Remove active class from all buttons
        document.querySelectorAll('.planet-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        // Add active class to clicked button
        button.classList.add('active');
    }
    
    setActiveButtonByName(planetName) {
        const button = document.querySelector(`[data-planet="${planetName}"]`);
        if (button) {
            this.setActiveButton(button);
        }
    }
    
    updateChartData(chartData, analysisData = null) {
        this.chartData = chartData;
        this.analysisData = analysisData;
    }
    
    showPlanetAnalysis(planetName) {
        if (!this.chartData || !this.chartData.planets) {
            this.showError('Chart data not available');
            return;
        }
        
        const planet = this.chartData.planets.find(p => p.name === planetName);
        if (!planet) {
            this.showError(`Planet ${planetName} not found in chart`);
            return;
        }
        
        const house = this.chartData.houses.find(h => h.number === planet.house);
        const analysis = this.generatePlanetAnalysis(planet, house);
        
        this.renderPlanetDetails(planet, house, analysis);
    }
    
    generatePlanetAnalysis(planet, house) {
        // Generate comprehensive analysis
        return {
            basic_info: this.getBasicPlanetInfo(planet),
            sign_analysis: this.getSignAnalysis(planet),
            house_analysis: this.getHouseAnalysis(planet, house),
            strength_analysis: this.getStrengthAnalysis(planet),
            life_themes: this.getLifeThemes(planet),
            current_influence: this.getCurrentInfluence(planet)
        };
    }
    
    getBasicPlanetInfo(planet) {
        const planetMeanings = {
            'Sun': 'Soul, ego, father, authority, government, health, vitality',
            'Moon': 'Mind, emotions, mother, public, water, travel, intuition',
            'Mars': 'Energy, courage, siblings, property, sports, conflicts',
            'Mercury': 'Intelligence, communication, business, education, friends',
            'Jupiter': 'Wisdom, spirituality, children, teachers, wealth, fortune',
            'Venus': 'Love, beauty, arts, luxury, vehicles, marriage, creativity',
            'Saturn': 'Discipline, delays, hard work, longevity, service, karma',
            'Rahu': 'Desires, illusions, foreign lands, technology, sudden gains',
            'Ketu': 'Spirituality, detachment, past life, moksha, research'
        };
        
        return {
            meaning: planetMeanings[planet.name] || 'Unknown planet',
            longitude: planet.longitude.toFixed(2),
            degree: planet.degree.toFixed(1),
            retrograde: planet.retrograde || false
        };
    }
    
    getSignAnalysis(planet) {
        const signQualities = {
            'Aries': 'Cardinal Fire - Initiative, leadership, pioneering spirit',
            'Taurus': 'Fixed Earth - Stability, material security, persistence',
            'Gemini': 'Mutable Air - Communication, versatility, curiosity',
            'Cancer': 'Cardinal Water - Nurturing, emotional, protective',
            'Leo': 'Fixed Fire - Creative, dramatic, authoritative',
            'Virgo': 'Mutable Earth - Analytical, practical, service-oriented',
            'Libra': 'Cardinal Air - Harmony, relationships, justice',
            'Scorpio': 'Fixed Water - Intense, transformative, mysterious',
            'Sagittarius': 'Mutable Fire - Philosophical, adventurous, optimistic',
            'Capricorn': 'Cardinal Earth - Ambitious, disciplined, practical',
            'Aquarius': 'Fixed Air - Innovative, humanitarian, independent',
            'Pisces': 'Mutable Water - Intuitive, compassionate, spiritual'
        };
        
        return {
            sign: planet.sign,
            quality: signQualities[planet.sign] || 'Unknown sign qualities',
            influence: `${planet.name} in ${planet.sign} brings ${this.getSignInfluence(planet.name, planet.sign)}`
        };
    }
    
    getSignInfluence(planetName, sign) {
        // Simplified sign influence
        const influences = {
            'Sun': {
                'Aries': 'strong leadership and pioneering energy',
                'Leo': 'natural authority and creative expression',
                'Libra': 'diplomatic leadership but some ego challenges'
            },
            'Moon': {
                'Cancer': 'strong emotional intuition and nurturing nature',
                'Taurus': 'emotional stability and material comfort',
                'Scorpio': 'intense emotions and transformative experiences'
            }
        };
        
        return influences[planetName]?.[sign] || `${planetName.toLowerCase()} energy expressed through ${sign.toLowerCase()} qualities`;
    }
    
    getHouseAnalysis(planet, house) {
        const houseThemes = {
            1: 'Self, personality, physical body, first impressions',
            2: 'Wealth, family, speech, food, values',
            3: 'Siblings, courage, communication, short journeys',
            4: 'Home, mother, happiness, property, education',
            5: 'Children, creativity, intelligence, romance, speculation',
            6: 'Health, enemies, service, daily work, obstacles',
            7: 'Marriage, partnerships, business, open enemies',
            8: 'Longevity, transformation, occult, shared resources',
            9: 'Fortune, dharma, higher learning, long journeys, father',
            10: 'Career, reputation, authority, government, public image',
            11: 'Gains, friends, aspirations, elder siblings, income',
            12: 'Loss, spirituality, foreign lands, expenses, moksha'
        };
        
        return {
            house_number: planet.house,
            house_theme: houseThemes[planet.house] || 'Unknown house themes',
            house_sign: house?.sign || 'Unknown',
            influence: `${planet.name} in House ${planet.house} influences ${houseThemes[planet.house]?.toLowerCase() || 'life areas'}`
        };
    }
    
    getStrengthAnalysis(planet) {
        // Simplified strength analysis
        let strength = 'Moderate';
        let factors = [];
        
        // Check for exaltation/debilitation
        const exaltations = {
            'Sun': 'Aries', 'Moon': 'Taurus', 'Mars': 'Capricorn',
            'Mercury': 'Virgo', 'Jupiter': 'Cancer', 'Venus': 'Pisces', 'Saturn': 'Libra'
        };
        
        const debilitations = {
            'Sun': 'Libra', 'Moon': 'Scorpio', 'Mars': 'Cancer',
            'Mercury': 'Pisces', 'Jupiter': 'Capricorn', 'Venus': 'Virgo', 'Saturn': 'Aries'
        };
        
        if (exaltations[planet.name] === planet.sign) {
            strength = 'Very Strong';
            factors.push('Exalted in own sign');
        } else if (debilitations[planet.name] === planet.sign) {
            strength = 'Weak';
            factors.push('Debilitated in this sign');
        }
        
        return {
            overall_strength: strength,
            strength_factors: factors,
            recommendation: this.getStrengthRecommendation(strength)
        };
    }
    
    getStrengthRecommendation(strength) {
        const recommendations = {
            'Very Strong': 'This planet is very well-placed. Utilize its positive energy.',
            'Strong': 'This planet supports you well. Focus on its themes.',
            'Moderate': 'This planet has mixed results. Balance is key.',
            'Weak': 'This planet may need support through remedies and conscious effort.'
        };
        
        return recommendations[strength] || 'Consult an astrologer for detailed analysis.';
    }
    
    getLifeThemes(planet) {
        // Generate life themes based on planet placement
        return [
            `${planet.name} in ${planet.sign} emphasizes ${this.getSignTheme(planet.sign)}`,
            `House ${planet.house} placement brings focus on ${this.getHouseTheme(planet.house)}`,
            `This combination suggests ${this.getCombinationTheme(planet.name, planet.sign, planet.house)}`
        ];
    }
    
    getSignTheme(sign) {
        const themes = {
            'Aries': 'leadership and initiative',
            'Taurus': 'stability and material security',
            'Gemini': 'communication and learning',
            'Cancer': 'nurturing and emotional security',
            'Leo': 'creativity and self-expression',
            'Virgo': 'service and attention to detail',
            'Libra': 'harmony and relationships',
            'Scorpio': 'transformation and depth',
            'Sagittarius': 'wisdom and expansion',
            'Capricorn': 'discipline and achievement',
            'Aquarius': 'innovation and humanitarian ideals',
            'Pisces': 'spirituality and compassion'
        };
        return themes[sign] || 'unique qualities';
    }
    
    getHouseTheme(house) {
        const themes = {
            1: 'personal identity and self-expression',
            2: 'wealth building and family values',
            3: 'communication and sibling relationships',
            4: 'home life and emotional foundations',
            5: 'creativity and children',
            6: 'health and daily service',
            7: 'partnerships and marriage',
            8: 'transformation and shared resources',
            9: 'higher learning and spiritual growth',
            10: 'career and public reputation',
            11: 'friendships and aspirations',
            12: 'spirituality and letting go'
        };
        return themes[house] || 'life experiences';
    }
    
    getCombinationTheme(planet, sign, house) {
        return `a life path focused on expressing ${planet.toLowerCase()} energy through ${sign.toLowerCase()} qualities in the area of ${this.getHouseTheme(house)}`;
    }
    
    getCurrentInfluence(planet) {
        return {
            current_phase: 'This planet is currently influencing your life through its house and sign placement',
            timing: 'The effects are ongoing and will evolve with planetary transits',
            advice: `Focus on the positive qualities of ${planet.name} in ${planet.sign} to maximize benefits`
        };
    }
    
    renderPlanetDetails(planet, house, analysis) {
        const detailsContainer = document.getElementById('planet-details');
        if (!detailsContainer) return;
        
        detailsContainer.innerHTML = `
            <div class="planet-analysis-content">
                <div class="planet-header">
                    <h4>${this.getPlanetSymbol(planet.name)} ${planet.name}</h4>
                    <div class="planet-position">
                        <span class="sign">${planet.sign}</span>
                        <span class="house">House ${planet.house}</span>
                        <span class="degree">${analysis.basic_info.degree}°</span>
                    </div>
                </div>
                
                <div class="analysis-sections">
                    <div class="analysis-section">
                        <h5>🎯 Basic Information</h5>
                        <p><strong>Represents:</strong> ${analysis.basic_info.meaning}</p>
                        <p><strong>Position:</strong> ${analysis.basic_info.longitude}° longitude</p>
                        ${analysis.basic_info.retrograde ? '<p><strong>Status:</strong> Retrograde ⟲</p>' : ''}
                    </div>
                    
                    <div class="analysis-section">
                        <h5>♈ Sign Analysis</h5>
                        <p><strong>Sign:</strong> ${analysis.sign_analysis.sign}</p>
                        <p><strong>Quality:</strong> ${analysis.sign_analysis.quality}</p>
                        <p><strong>Influence:</strong> ${analysis.sign_analysis.influence}</p>
                    </div>
                    
                    <div class="analysis-section">
                        <h5>🏠 House Analysis</h5>
                        <p><strong>House ${analysis.house_analysis.house_number}:</strong> ${analysis.house_analysis.house_theme}</p>
                        <p><strong>House Sign:</strong> ${analysis.house_analysis.house_sign}</p>
                        <p><strong>Effect:</strong> ${analysis.house_analysis.influence}</p>
                    </div>
                    
                    <div class="analysis-section">
                        <h5>💪 Strength Analysis</h5>
                        <p><strong>Overall Strength:</strong> ${analysis.strength_analysis.overall_strength}</p>
                        ${analysis.strength_analysis.strength_factors.length > 0 ? 
                            `<p><strong>Factors:</strong> ${analysis.strength_analysis.strength_factors.join(', ')}</p>` : ''}
                        <p><strong>Recommendation:</strong> ${analysis.strength_analysis.recommendation}</p>
                    </div>
                    
                    <div class="analysis-section">
                        <h5>🌟 Life Themes</h5>
                        <ul>
                            ${analysis.life_themes.map(theme => `<li>${theme}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="analysis-section">
                        <h5>⏰ Current Influence</h5>
                        <p><strong>Phase:</strong> ${analysis.current_influence.current_phase}</p>
                        <p><strong>Timing:</strong> ${analysis.current_influence.timing}</p>
                        <p><strong>Advice:</strong> ${analysis.current_influence.advice}</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    getPlanetSymbol(planetName) {
        const symbols = {
            'Sun': '☉', 'Moon': '☽', 'Mars': '♂', 'Mercury': '☿',
            'Jupiter': '♃', 'Venus': '♀', 'Saturn': '♄',
            'Rahu': '☊', 'Ketu': '☋'
        };
        return symbols[planetName] || '●';
    }
    
    showError(message) {
        const detailsContainer = document.getElementById('planet-details');
        if (!detailsContainer) return;
        
        detailsContainer.innerHTML = `
            <div class="error-message">
                <p>❌ ${message}</p>
            </div>
        `;
    }
}

// Export for global access
window.PlanetaryAnalysis = PlanetaryAnalysis;
