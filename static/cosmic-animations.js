// Cosmic Animations for Vedic Astrology App using p5.js

// Global variables for cosmic background
let stars = [];
let planets = [];
let cosmicTime = 0;
let backgroundSketch;

// Planet colors and characteristics
const planetData = {
    sun: { color: [255, 204, 0], size: 25, speed: 0.5, rings: false },
    moon: { color: [220, 220, 255], size: 20, speed: 1.2, rings: false },
    mars: { color: [255, 100, 100], size: 18, speed: 0.8, rings: false },
    mercury: { color: [150, 255, 150], size: 15, speed: 1.5, rings: false },
    jupiter: { color: [255, 180, 100], size: 30, speed: 0.3, rings: true },
    venus: { color: [255, 150, 255], size: 22, speed: 0.9, rings: false },
    saturn: { color: [200, 200, 255], size: 28, speed: 0.2, rings: true },
    rahu: { color: [100, 100, 255], size: 16, speed: -0.4, rings: false },
    ketu: { color: [255, 100, 150], size: 16, speed: -0.6, rings: false }
};

// Individual planet sketches
const planetSketches = {};

// Slime Mold Class for organic background
class Mold {
    constructor(p) {
        this.p = p;
        // Start from center area for cosmic effect
        this.x = p.random(p.width/2 - 50, p.width/2 + 50);
        this.y = p.random(p.height/2 - 30, p.height/2 + 30);
        this.r = 0.3; // Smaller for subtle effect

        this.heading = p.random(360);
        this.vx = p.cos(this.heading);
        this.vy = p.sin(this.heading);
        this.rotAngle = 45;

        // Sensor variables
        this.rSensorPos = p.createVector(0, 0);
        this.lSensorPos = p.createVector(0, 0);
        this.fSensorPos = p.createVector(0, 0);
        this.sensorAngle = 45;
        this.sensorDist = 8; // Smaller sensor distance

        // Cosmic properties
        this.opacity = p.random(0.1, 0.3);
        this.cosmicHue = p.random(200, 280); // Blue to purple range
    }

    update() {
        this.vx = this.p.cos(this.heading);
        this.vy = this.p.sin(this.heading);

        // Slower movement for subtle effect
        this.x = (this.x + this.vx * 0.5 + this.p.width) % this.p.width;
        this.y = (this.y + this.vy * 0.5 + this.p.height) % this.p.height;

        // Get sensor positions
        this.getSensorPos(this.rSensorPos, this.heading + this.sensorAngle);
        this.getSensorPos(this.lSensorPos, this.heading - this.sensorAngle);
        this.getSensorPos(this.fSensorPos, this.heading);

        // Simplified movement logic without pixel sensing for now
        // This ensures the molds move even if pixel sensing fails
        if (this.p.random(1) < 0.1) {
            if (this.p.random(1) < 0.5) {
                this.heading += this.rotAngle;
            } else {
                this.heading -= this.rotAngle;
            }
        }

        // Try pixel sensing if pixels are available
        if (this.p.pixels && this.p.pixels.length > 0) {
            try {
                let d = this.p.pixelDensity();
                let index, l, r, f;

                index = 4*(d * this.p.floor(this.rSensorPos.y)) * (d * this.p.width) + 4*(d * this.p.floor(this.rSensorPos.x));
                r = this.p.pixels[index] || 0;

                index = 4*(d * this.p.floor(this.lSensorPos.y)) * (d * this.p.width) + 4*(d * this.p.floor(this.lSensorPos.x));
                l = this.p.pixels[index] || 0;

                index = 4*(d * this.p.floor(this.fSensorPos.y)) * (d * this.p.width) + 4*(d * this.p.floor(this.fSensorPos.x));
                f = this.p.pixels[index] || 0;

                // Movement logic based on pixel sensing
                if (f > l && f > r) {
                    this.heading += 0;
                } else if (f < l && f < r) {
                    if (this.p.random(1) < 0.5) {
                        this.heading += this.rotAngle;
                    } else {
                        this.heading -= this.rotAngle;
                    }
                } else if (l > r) {
                    this.heading += -this.rotAngle;
                } else if (r > l) {
                    this.heading += this.rotAngle;
                }
            } catch (e) {
                // If pixel sensing fails, use random movement
                if (this.p.random(1) < 0.05) {
                    this.heading += this.p.random(-this.rotAngle, this.rotAngle);
                }
            }
        }
    }

    display() {
        this.p.noStroke();
        this.p.colorMode(this.p.HSB, 360, 100, 100, 1);
        this.p.fill(this.cosmicHue, 60, 80, this.opacity);
        this.p.ellipse(this.x, this.y, this.r*2, this.r*2);
        this.p.colorMode(this.p.RGB, 255);
    }

    getSensorPos(sensor, angle) {
        sensor.x = (this.x + this.sensorDist * this.p.cos(angle) + this.p.width) % this.p.width;
        sensor.y = (this.y + this.sensorDist * this.p.sin(angle) + this.p.height) % this.p.height;
    }
}

// Cosmic Background Animation with Slime Mold
function createCosmicBackground() {
    backgroundSketch = function(p) {
        let molds = [];
        let numMolds = 50; // Drastically reduced for performance

        p.setup = function() {
            const canvas = p.createCanvas(p.windowWidth, 200);
            canvas.parent('cosmic-background');
            p.angleMode(p.DEGREES);

            // Create slime molds
            for (let i = 0; i < numMolds; i++) {
                molds[i] = new Mold(p);
            }

            // Create stars
            for (let i = 0; i < 100; i++) {
                stars.push({
                    x: p.random(p.width),
                    y: p.random(p.height),
                    size: p.random(1, 2),
                    brightness: p.random(0.2, 0.8),
                    twinkleSpeed: p.random(0.01, 0.03)
                });
            }
        };

        p.draw = function() {
            // Create deep space gradient background with slight transparency for trails
            p.background(0, 8); // Slight transparency for slime mold trails

            // Add gradient overlay
            for (let i = 0; i <= p.height; i += 4) {
                let inter = p.map(i, 0, p.height, 0, 1);
                let c = p.lerpColor(p.color(15, 15, 35, 20), p.color(5, 5, 15, 20), inter);
                p.stroke(c);
                p.line(0, i, p.width, i);
            }

            cosmicTime += 0.01;

            // Skip pixel loading for performance
            // p.loadPixels(); // Disabled for performance

            // Update and display slime molds
            for (let i = 0; i < numMolds; i++) {
                molds[i].update();
                molds[i].display();
            }

            // Draw twinkling stars
            for (let star of stars) {
                let brightness = star.brightness + p.sin(cosmicTime * star.twinkleSpeed) * 0.3;
                p.fill(255, 255, 255, brightness * 150);
                p.noStroke();
                p.ellipse(star.x, star.y, star.size);

                // Add subtle glow
                p.fill(255, 255, 255, brightness * 30);
                p.ellipse(star.x, star.y, star.size * 2);
            }

            // Add cosmic dust effect
            p.stroke(255, 255, 255, 15);
            p.strokeWeight(1);
            for (let i = 0; i < 3; i++) {
                let x1 = p.noise(cosmicTime * 0.1 + i) * p.width;
                let y1 = p.noise(cosmicTime * 0.1 + i + 100) * p.height;
                let x2 = p.noise(cosmicTime * 0.1 + i + 0.1) * p.width;
                let y2 = p.noise(cosmicTime * 0.1 + i + 100.1) * p.height;
                p.line(x1, y1, x2, y2);
            }
        };

        p.windowResized = function() {
            p.resizeCanvas(p.windowWidth, 200);
        };
    };

    new p5(backgroundSketch);
}

// Individual Planet Animations
function createPlanetAnimation(planetName, containerId) {
    const data = planetData[planetName.toLowerCase()] || planetData.sun;

    planetSketches[planetName] = function(p) {
        let angle = 0;
        let pulsePhase = 0;

        p.setup = function() {
            const canvas = p.createCanvas(80, 80);
            canvas.parent(containerId);
        };

        p.draw = function() {
            p.clear();

            angle += data.speed * 0.02;
            pulsePhase += 0.05;

            // Planet glow
            let glowSize = data.size + p.sin(pulsePhase) * 3;
            p.fill(data.color[0], data.color[1], data.color[2], 30);
            p.noStroke();
            p.ellipse(40, 40, glowSize * 2);

            // Planet body
            p.fill(data.color[0], data.color[1], data.color[2]);
            p.ellipse(40, 40, data.size);

            // Planet surface details
            p.fill(data.color[0] * 0.8, data.color[1] * 0.8, data.color[2] * 0.8);
            p.ellipse(40 + p.cos(angle) * 3, 40 + p.sin(angle) * 2, data.size * 0.3);
            p.ellipse(40 - p.cos(angle * 1.5) * 4, 40 - p.sin(angle * 1.5) * 3, data.size * 0.2);

            // Planet highlight
            p.fill(255, 255, 255, 150);
            p.ellipse(40 - data.size * 0.2, 40 - data.size * 0.2, data.size * 0.3);

            // Rings for Jupiter and Saturn
            if (data.rings) {
                p.stroke(data.color[0], data.color[1], data.color[2], 100);
                p.strokeWeight(2);
                p.noFill();
                p.ellipse(40, 40, data.size * 1.8, data.size * 0.6);
                p.ellipse(40, 40, data.size * 2.2, data.size * 0.8);
            }

            // Orbital trail effect
            p.stroke(data.color[0], data.color[1], data.color[2], 50);
            p.strokeWeight(1);
            p.noFill();
            let trailRadius = 35;
            for (let i = 0; i < 8; i++) {
                let trailAngle = angle - i * 0.3;
                let x = 40 + p.cos(trailAngle) * trailRadius;
                let y = 40 + p.sin(trailAngle) * trailRadius;
                p.point(x, y);
            }
        };
    };

    new p5(planetSketches[planetName]);
}

// Constellation Visualization
function createConstellationVisualization() {
    const constellationSketch = function(p) {
        let constellationPlanets = [];
        let connections = [];
        let mouseInfluence = { x: 0, y: 0 };

        p.setup = function() {
            const canvas = p.createCanvas(400, 300);
            canvas.parent('constellation-viz');

            // Create constellation of planets based on chart data
            const planetNames = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];

            for (let i = 0; i < planetNames.length; i++) {
                const angle = (i / planetNames.length) * p.TWO_PI;
                const radius = 80 + p.random(-20, 20);

                constellationPlanets.push({
                    name: planetNames[i],
                    x: p.width/2 + p.cos(angle) * radius,
                    y: p.height/2 + p.sin(angle) * radius,
                    originalX: p.width/2 + p.cos(angle) * radius,
                    originalY: p.height/2 + p.sin(angle) * radius,
                    size: p.random(8, 15),
                    color: planetData[planetNames[i].toLowerCase()]?.color || [255, 255, 255],
                    pulsePhase: p.random(p.TWO_PI),
                    orbitAngle: angle,
                    selected: false
                });
            }

            // Create connections between planets
            for (let i = 0; i < constellationPlanets.length; i++) {
                for (let j = i + 1; j < constellationPlanets.length; j++) {
                    const dist = p.dist(
                        constellationPlanets[i].x, constellationPlanets[i].y,
                        constellationPlanets[j].x, constellationPlanets[j].y
                    );

                    if (dist < 120) {
                        connections.push({
                            from: i,
                            to: j,
                            strength: p.map(dist, 0, 120, 1, 0.1)
                        });
                    }
                }
            }
        };

        p.draw = function() {
            // Deep space background
            p.background(15, 15, 35);

            // Add stars
            p.fill(255, 255, 255, 100);
            p.noStroke();
            for (let i = 0; i < 50; i++) {
                let x = (p.noise(i * 0.1, p.frameCount * 0.001) * p.width);
                let y = (p.noise(i * 0.1 + 100, p.frameCount * 0.001) * p.height);
                p.ellipse(x, y, 1);
            }

            // Update mouse influence
            if (p.mouseX > 0 && p.mouseX < p.width && p.mouseY > 0 && p.mouseY < p.height) {
                mouseInfluence.x = p.lerp(mouseInfluence.x, p.mouseX, 0.1);
                mouseInfluence.y = p.lerp(mouseInfluence.y, p.mouseY, 0.1);
            }

            // Draw connections
            for (let connection of connections) {
                const from = constellationPlanets[connection.from];
                const to = constellationPlanets[connection.to];

                p.stroke(100, 150, 255, connection.strength * 100);
                p.strokeWeight(connection.strength * 2);
                p.line(from.x, from.y, to.x, to.y);

                // Add energy flow along connections
                let flowPos = (p.frameCount * 0.02) % 1;
                let flowX = p.lerp(from.x, to.x, flowPos);
                let flowY = p.lerp(from.y, to.y, flowPos);

                p.fill(150, 200, 255, 150);
                p.noStroke();
                p.ellipse(flowX, flowY, 3);
            }

            // Update and draw planets
            for (let i = 0; i < constellationPlanets.length; i++) {
                let planet = constellationPlanets[i];

                // Mouse interaction
                let mouseDistance = p.dist(mouseInfluence.x, mouseInfluence.y, planet.x, planet.y);
                if (mouseDistance < 50) {
                    let force = p.map(mouseDistance, 0, 50, 10, 0);
                    let angle = p.atan2(planet.y - mouseInfluence.y, planet.x - mouseInfluence.x);
                    planet.x += p.cos(angle) * force * 0.1;
                    planet.y += p.sin(angle) * force * 0.1;
                    planet.selected = true;
                } else {
                    // Return to original position
                    planet.x = p.lerp(planet.x, planet.originalX, 0.05);
                    planet.y = p.lerp(planet.y, planet.originalY, 0.05);
                    planet.selected = false;
                }

                // Gentle orbital motion
                planet.orbitAngle += 0.005;
                planet.originalX = p.width/2 + p.cos(planet.orbitAngle) * 80;
                planet.originalY = p.height/2 + p.sin(planet.orbitAngle) * 80;

                // Pulsing effect
                planet.pulsePhase += 0.05;
                let pulseSize = planet.size + p.sin(planet.pulsePhase) * 2;

                // Planet glow
                let glowSize = planet.selected ? pulseSize * 3 : pulseSize * 2;
                p.fill(planet.color[0], planet.color[1], planet.color[2], 30);
                p.noStroke();
                p.ellipse(planet.x, planet.y, glowSize);

                // Planet body
                p.fill(planet.color[0], planet.color[1], planet.color[2]);
                p.ellipse(planet.x, planet.y, pulseSize);

                // Planet highlight
                p.fill(255, 255, 255, 150);
                p.ellipse(planet.x - pulseSize * 0.2, planet.y - pulseSize * 0.2, pulseSize * 0.3);

                // Planet name on hover
                if (planet.selected) {
                    p.fill(255, 255, 255);
                    p.textAlign(p.CENTER);
                    p.textSize(12);
                    p.text(planet.name, planet.x, planet.y - pulseSize - 10);
                }
            }

            // Central cosmic energy
            p.fill(255, 255, 255, 50);
            p.noStroke();
            let centralPulse = p.sin(p.frameCount * 0.02) * 10;
            p.ellipse(p.width/2, p.height/2, 20 + centralPulse);
        };

        p.mousePressed = function() {
            // Add ripple effect on click
            if (p.mouseX > 0 && p.mouseX < p.width && p.mouseY > 0 && p.mouseY < p.height) {
                createRipple(p.mouseX, p.mouseY);
            }
        };

        function createRipple(x, y) {
            let rippleSize = 0;
            let rippleOpacity = 255;

            function animateRipple() {
                p.stroke(150, 200, 255, rippleOpacity);
                p.strokeWeight(2);
                p.noFill();
                p.ellipse(x, y, rippleSize);

                rippleSize += 5;
                rippleOpacity -= 8;

                if (rippleOpacity > 0) {
                    setTimeout(animateRipple, 16);
                }
            }

            animateRipple();
        }
    };

    new p5(constellationSketch);
}

// Test animation removed - slime mold is working

// Full-screen Slime Mold Background
function createFullScreenSlimeMold() {
    const slimeMoldSketch = function(p) {
        let molds = [];
        let numMolds = 0; // Disabled for performance

        p.setup = function() {
            console.log('Slime mold setup called');

            // Get full document dimensions including scroll height
            const documentHeight = Math.max(
                document.body.scrollHeight,
                document.body.offsetHeight,
                document.documentElement.clientHeight,
                document.documentElement.scrollHeight,
                document.documentElement.offsetHeight,
                window.innerHeight
            );

            const documentWidth = Math.max(
                document.body.scrollWidth,
                document.body.offsetWidth,
                document.documentElement.clientWidth,
                document.documentElement.scrollWidth,
                document.documentElement.offsetWidth,
                window.innerWidth
            );

            console.log('Creating canvas with full document size:', documentWidth, 'x', documentHeight);
            console.log('Viewport size:', window.innerWidth, 'x', window.innerHeight);

            const canvas = p.createCanvas(documentWidth, documentHeight);
            canvas.parent('slime-mold-background');

            // Set canvas style to ensure it covers the full document
            canvas.canvas.style.position = 'absolute';
            canvas.canvas.style.top = '0';
            canvas.canvas.style.left = '0';
            canvas.canvas.style.width = documentWidth + 'px';
            canvas.canvas.style.height = documentHeight + 'px';
            canvas.canvas.style.zIndex = '-1';

            p.angleMode(p.DEGREES);
            console.log('Slime mold canvas created, size:', p.width, 'x', p.height);

            // Create slime molds starting from multiple centers for organic spread
            for (let i = 0; i < numMolds; i++) {
                molds[i] = new Mold(p);

                // Create multiple starting clusters for interesting patterns
                let clusterChoice = i % 4;
                if (clusterChoice === 0) {
                    // Center cluster
                    molds[i].x = p.random(p.width * 0.4, p.width * 0.6);
                    molds[i].y = p.random(p.height * 0.4, p.height * 0.6);
                } else if (clusterChoice === 1) {
                    // Top-left cluster
                    molds[i].x = p.random(p.width * 0.1, p.width * 0.3);
                    molds[i].y = p.random(p.height * 0.1, p.height * 0.3);
                } else if (clusterChoice === 2) {
                    // Bottom-right cluster
                    molds[i].x = p.random(p.width * 0.7, p.width * 0.9);
                    molds[i].y = p.random(p.height * 0.7, p.height * 0.9);
                } else {
                    // Random scattered
                    molds[i].x = p.random(p.width);
                    molds[i].y = p.random(p.height);
                }

                // Cosmic color variations
                molds[i].cosmicHue = p.random(200, 300); // Blue to purple range
                molds[i].opacity = p.random(0.3, 0.6); // Much more visible for testing
                molds[i].r = p.random(1.0, 2.0); // Larger for testing
            }

            console.log('Slime mold background initialized with', numMolds, 'agents');
        };

        p.draw = function() {
            // Very subtle background fade for trail effect
            p.background(0, 8);

            // Update and display all slime molds
            for (let i = 0; i < numMolds; i++) {
                molds[i].update();
                molds[i].display();
            }

            // Debug info
            if (p.frameCount % 60 === 0) {
                console.log('Slime mold frame:', p.frameCount, 'molds:', molds.length);
            }
        };

        p.windowResized = function() {
            // Recalculate full document dimensions
            const documentHeight = Math.max(
                document.body.scrollHeight,
                document.body.offsetHeight,
                document.documentElement.clientHeight,
                document.documentElement.scrollHeight,
                document.documentElement.offsetHeight,
                window.innerHeight
            );

            const documentWidth = Math.max(
                document.body.scrollWidth,
                document.body.offsetWidth,
                document.documentElement.clientWidth,
                document.documentElement.scrollWidth,
                document.documentElement.offsetWidth,
                window.innerWidth
            );

            console.log('Resizing canvas to full document:', documentWidth, 'x', documentHeight);
            p.resizeCanvas(documentWidth, documentHeight);

            // Ensure canvas style remains correct after resize
            p.canvas.style.position = 'absolute';
            p.canvas.style.top = '0';
            p.canvas.style.left = '0';
            p.canvas.style.width = documentWidth + 'px';
            p.canvas.style.height = documentHeight + 'px';
            p.canvas.style.zIndex = '-1';
        };
    };

    console.log('Creating slime mold sketch...');
    new p5(slimeMoldSketch);
}

// Initialize all animations when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, checking p5.js...');

    // Check if p5.js is loaded
    if (typeof p5 === 'undefined') {
        console.error('p5.js is not loaded!');
        return;
    }
    console.log('p5.js is loaded successfully');

    // Check if slime mold container exists
    const slimeMoldContainer = document.getElementById('slime-mold-background');
    if (!slimeMoldContainer) {
        console.error('Slime mold container not found!');
        return;
    }
    console.log('Slime mold container found:', slimeMoldContainer);

    // Start slime mold background immediately
    console.log('Starting slime mold background...');
    try {
        createFullScreenSlimeMold();
        console.log('Slime mold background creation initiated');
    } catch (error) {
        console.error('Error creating slime mold background:', error);
        console.log('Slime mold animation failed to initialize');
    }

    // Create cosmic background for header
    console.log('Starting cosmic background...');
    createCosmicBackground();

    // Create constellation visualization
    console.log('Starting constellation visualization...');
    createConstellationVisualization();

    // Create planet animations for each planet card
    const planetCards = document.querySelectorAll('.planet-modern-card');
    console.log('Found', planetCards.length, 'planet cards');
    planetCards.forEach(card => {
        const planetName = card.getAttribute('data-planet');
        const animationContainer = card.querySelector('.planet-animation');
        if (planetName && animationContainer) {
            console.log('Creating animation for planet:', planetName);
            createPlanetAnimation(planetName, animationContainer.id);
        }
    });

    // Add smooth content transition after slime mold starts
    setTimeout(() => {
        const appContainer = document.querySelector('.app-container');
        if (appContainer) {
            appContainer.classList.add('loaded');
            console.log('Content transition started');

            // Update canvas size after content is loaded
            setTimeout(() => {
                updateCanvasSize();
            }, 500);
        }
    }, 1000); // Start content transition after 1 second
});

// Function to update canvas size dynamically
function updateCanvasSize() {
    const fullHeight = Math.max(
        document.documentElement.clientHeight,
        document.documentElement.scrollHeight,
        document.documentElement.offsetHeight,
        window.innerHeight,
        document.body.scrollHeight,
        document.body.offsetHeight
    );

    const fullWidth = Math.max(
        document.documentElement.clientWidth,
        document.documentElement.scrollWidth,
        document.documentElement.offsetWidth,
        window.innerWidth,
        document.body.scrollWidth,
        document.body.offsetWidth
    );

    console.log('Updating canvas size to cover full document:', fullWidth, 'x', fullHeight);

    // Trigger window resize event to update p5.js canvas
    setTimeout(() => {
        window.dispatchEvent(new Event('resize'));
    }, 100);
}

// Enhanced interactive effects for better user experience

// Add interactive hover effects
document.addEventListener('DOMContentLoaded', function() {
    const planetCards = document.querySelectorAll('.planet-modern-card');

    planetCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
            this.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.4)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '';
        });
    });
});

// Add cosmic particle effects on tab switches
function addTabSwitchEffects() {
    const navButtons = document.querySelectorAll('.nav-btn');

    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Create temporary particle burst effect
            createParticleBurst(this);

            // Update canvas size after tab content changes
            setTimeout(() => {
                updateCanvasSize();
            }, 300);
        });
    });
}

function createParticleBurst(element) {
    const rect = element.getBoundingClientRect();

    for (let i = 0; i < 12; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'fixed';
        particle.style.left = rect.left + rect.width / 2 + 'px';
        particle.style.top = rect.top + rect.height / 2 + 'px';
        particle.style.width = '4px';
        particle.style.height = '4px';
        particle.style.backgroundColor = '#6366f1';
        particle.style.borderRadius = '50%';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '9999';

        document.body.appendChild(particle);

        const angle = (i / 12) * Math.PI * 2;
        const velocity = 50 + Math.random() * 30;
        const vx = Math.cos(angle) * velocity;
        const vy = Math.sin(angle) * velocity;

        let x = 0, y = 0, opacity = 1;

        function animate() {
            x += vx * 0.02;
            y += vy * 0.02;
            opacity -= 0.02;

            particle.style.transform = `translate(${x}px, ${y}px)`;
            particle.style.opacity = opacity;

            if (opacity > 0) {
                requestAnimationFrame(animate);
            } else {
                document.body.removeChild(particle);
            }
        }

        animate();
    }
}

// Initialize tab effects
document.addEventListener('DOMContentLoaded', addTabSwitchEffects);
