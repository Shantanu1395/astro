// 3D Celestial Sphere Component for Vedic Astrology Visualization

import { useRef, useMemo } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import { Sphere, Text, Ring } from '@react-three/drei';
import * as THREE from 'three';
import { TextureLoader } from 'three';

// Enhanced Realistic Planet Texture Generation
function createPlanetTexture(type: string, color: string): THREE.Texture {
  const canvas = document.createElement('canvas');
  canvas.width = 1024;
  canvas.height = 1024;
  const ctx = canvas.getContext('2d')!;

  switch (type) {
    case 'solar':
      // Realistic Sun surface with solar granulation and prominences
      const sunGradient = ctx.createRadialGradient(512, 512, 0, 512, 512, 512);
      sunGradient.addColorStop(0, '#FFF5B7');
      sunGradient.addColorStop(0.2, '#FFE55C');
      sunGradient.addColorStop(0.5, '#FFB347');
      sunGradient.addColorStop(0.8, '#FF6B35');
      sunGradient.addColorStop(1, '#D2001F');
      ctx.fillStyle = sunGradient;
      ctx.fillRect(0, 0, 1024, 1024);

      // Solar granulation pattern (convection cells)
      for (let i = 0; i < 300; i++) {
        const x = Math.random() * 1024;
        const y = Math.random() * 1024;
        const size = Math.random() * 20 + 8;
        const brightness = Math.random() * 0.4 + 0.2;

        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${brightness})`;
        ctx.fill();

        // Darker edges for granulation effect
        ctx.beginPath();
        ctx.arc(x, y, size * 1.2, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(255, 100, 0, ${brightness * 0.5})`;
        ctx.lineWidth = 2;
        ctx.stroke();
      }

      // Solar prominences and flares
      for (let i = 0; i < 15; i++) {
        const x = Math.random() * 1024;
        const y = Math.random() * 1024;
        const width = Math.random() * 80 + 40;
        const height = Math.random() * 200 + 100;

        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(Math.random() * Math.PI * 2);

        const flareGradient = ctx.createLinearGradient(0, 0, 0, height);
        flareGradient.addColorStop(0, 'rgba(255, 255, 255, 0.8)');
        flareGradient.addColorStop(0.5, 'rgba(255, 150, 0, 0.6)');
        flareGradient.addColorStop(1, 'rgba(255, 0, 0, 0.2)');

        ctx.fillStyle = flareGradient;
        ctx.fillRect(-width/2, 0, width, height);
        ctx.restore();
      }
      break;

    case 'rocky':
      // Mercury-like heavily cratered rocky surface
      ctx.fillStyle = '#8C7853';
      ctx.fillRect(0, 0, 1024, 1024);

      // Add realistic crater patterns with proper depth
      const mercuryCraters = [
        { x: 200, y: 150, size: 80, depth: 0.8 },
        { x: 600, y: 300, size: 120, depth: 0.9 },
        { x: 800, y: 700, size: 60, depth: 0.7 },
        { x: 300, y: 800, size: 90, depth: 0.8 },
        { x: 700, y: 100, size: 50, depth: 0.6 }
      ];

      // Major craters
      mercuryCraters.forEach(crater => {
        // Crater rim (raised edge)
        ctx.beginPath();
        ctx.arc(crater.x, crater.y, crater.size, 0, Math.PI * 2);
        ctx.fillStyle = '#A0916B';
        ctx.fill();

        // Crater floor (depressed)
        ctx.beginPath();
        ctx.arc(crater.x, crater.y, crater.size * 0.8, 0, Math.PI * 2);
        ctx.fillStyle = '#6B5D42';
        ctx.fill();

        // Central peak (for larger craters)
        if (crater.size > 70) {
          ctx.beginPath();
          ctx.arc(crater.x, crater.y, crater.size * 0.15, 0, Math.PI * 2);
          ctx.fillStyle = '#9A8A6B';
          ctx.fill();
        }
      });

      // Smaller impact craters scattered across surface
      for (let i = 0; i < 100; i++) {
        const x = Math.random() * 1024;
        const y = Math.random() * 1024;
        const size = Math.random() * 25 + 5;

        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 0, 0, ${Math.random() * 0.4 + 0.3})`;
        ctx.fill();
      }
      break;

    case 'cloudy':
      // Venus-like thick sulfuric acid cloud atmosphere
      const venusGradient = ctx.createLinearGradient(0, 0, 1024, 1024);
      venusGradient.addColorStop(0, '#FFC649');
      venusGradient.addColorStop(0.3, '#FFB347');
      venusGradient.addColorStop(0.7, '#FF8C42');
      venusGradient.addColorStop(1, '#E67E22');
      ctx.fillStyle = venusGradient;
      ctx.fillRect(0, 0, 1024, 1024);

      // Add realistic swirling cloud patterns
      for (let i = 0; i < 60; i++) {
        const x = Math.random() * 1024;
        const y = Math.random() * 1024;
        const width = Math.random() * 150 + 80;
        const height = Math.random() * 40 + 20;
        const rotation = Math.random() * Math.PI * 2;

        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rotation);

        // Create swirling cloud effect
        ctx.beginPath();
        ctx.ellipse(0, 0, width, height, 0, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${Math.random() * 0.4 + 0.2})`;
        ctx.fill();

        // Add darker cloud shadows
        ctx.beginPath();
        ctx.ellipse(width * 0.3, height * 0.2, width * 0.6, height * 0.8, 0, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(200, 150, 100, ${Math.random() * 0.3 + 0.1})`;
        ctx.fill();

        ctx.restore();
      }

      // Add atmospheric bands (Venus retrograde rotation effect)
      for (let y = 0; y < 1024; y += 80) {
        ctx.fillStyle = `rgba(255, 200, 150, ${Math.random() * 0.2 + 0.1})`;
        ctx.fillRect(0, y, 1024, Math.random() * 30 + 15);
      }
      break;

    case 'desert':
      // Mars-like red desert with realistic surface features
      ctx.fillStyle = '#CD5C5C';
      ctx.fillRect(0, 0, 1024, 1024);

      // Add Martian surface features (canyons, valleys)
      for (let i = 0; i < 40; i++) {
        const x = Math.random() * 1024;
        const y = Math.random() * 1024;
        const width = Math.random() * 300 + 100;
        const height = Math.random() * 80 + 20;
        const rotation = Math.random() * Math.PI;

        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rotation);

        // Canyon/valley feature
        ctx.fillStyle = '#8B4513';
        ctx.fillRect(-width/2, -height/2, width, height);

        // Add depth shading
        ctx.fillStyle = '#654321';
        ctx.fillRect(-width/2 + 10, -height/2 + 5, width - 20, height - 10);

        ctx.restore();
      }

      // Polar ice caps (more realistic)
      ctx.beginPath();
      ctx.arc(512, 150, 120, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
      ctx.fill();

      ctx.beginPath();
      ctx.arc(512, 874, 100, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
      ctx.fill();

      // Add dust storm effects
      for (let i = 0; i < 20; i++) {
        const x = Math.random() * 1024;
        const y = Math.random() * 1024;
        const size = Math.random() * 100 + 50;

        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(210, 180, 140, ${Math.random() * 0.3 + 0.1})`;
        ctx.fill();
      }
      break;

    case 'gas_giant':
      // Jupiter-like atmospheric bands with realistic storm systems
      for (let y = 0; y < 1024; y += 80) {
        const hue = 25 + (y / 1024) * 50; // Orange to brown gradient
        const lightness = 35 + Math.sin(y / 150) * 25;
        const saturation = 60 + Math.sin(y / 100) * 20;

        ctx.fillStyle = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
        ctx.fillRect(0, y, 1024, 80);

        // Add turbulence and storm systems within bands
        for (let x = 0; x < 1024; x += 120) {
          const stormSize = Math.random() * 60 + 30;
          const stormOpacity = Math.random() * 0.4 + 0.2;

          ctx.fillStyle = `rgba(255, 255, 255, ${stormOpacity})`;
          ctx.beginPath();
          ctx.ellipse(x + Math.random() * 100, y + Math.random() * 60, stormSize, stormSize * 0.6, 0, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // Great Red Spot (iconic Jupiter feature)
      ctx.beginPath();
      ctx.ellipse(400, 650, 180, 120, 0.2, 0, Math.PI * 2);
      ctx.fillStyle = '#B22222';
      ctx.fill();

      // Add swirling pattern inside Great Red Spot
      ctx.beginPath();
      ctx.ellipse(420, 670, 120, 80, 0.2, 0, Math.PI * 2);
      ctx.fillStyle = '#8B0000';
      ctx.fill();

      // Smaller storm systems
      for (let i = 0; i < 8; i++) {
        const x = Math.random() * 1024;
        const y = Math.random() * 1024;
        const size = Math.random() * 40 + 20;

        ctx.beginPath();
        ctx.ellipse(x, y, size, size * 0.7, Math.random() * Math.PI, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(139, 69, 19, ${Math.random() * 0.6 + 0.3})`;
        ctx.fill();
      }
      break;

    case 'ringed':
      // Saturn-like pale golden atmosphere
      const saturnGradient = ctx.createRadialGradient(512, 512, 0, 512, 512, 512);
      saturnGradient.addColorStop(0, '#FFFACD');
      saturnGradient.addColorStop(0.5, '#F0E68C');
      saturnGradient.addColorStop(1, '#DAA520');
      ctx.fillStyle = saturnGradient;
      ctx.fillRect(0, 0, 1024, 1024);

      // Add subtle atmospheric bands
      for (let y = 0; y < 1024; y += 60) {
        const bandOpacity = Math.random() * 0.3 + 0.1;
        ctx.fillStyle = `rgba(255, 255, 255, ${bandOpacity})`;
        ctx.fillRect(0, y, 1024, Math.random() * 25 + 15);
      }

      // Add hexagonal storm at pole (Saturn's unique feature)
      ctx.save();
      ctx.translate(512, 150);
      ctx.beginPath();
      for (let i = 0; i < 6; i++) {
        const angle = (i * Math.PI) / 3;
        const x = Math.cos(angle) * 60;
        const y = Math.sin(angle) * 60;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.fillStyle = 'rgba(139, 69, 19, 0.6)';
      ctx.fill();
      ctx.restore();
      break;

    case 'lunar':
      // Realistic lunar surface with major features
      ctx.fillStyle = '#C0C0C0';
      ctx.fillRect(0, 0, 1024, 1024);

      // Major lunar maria (dark basaltic plains)
      const maria = [
        { name: 'Mare Tranquillitatis', x: 400, y: 300, width: 200, height: 150 },
        { name: 'Mare Serenitatis', x: 600, y: 200, width: 180, height: 120 },
        { name: 'Mare Imbrium', x: 300, y: 500, width: 250, height: 200 },
        { name: 'Mare Crisium', x: 700, y: 600, width: 120, height: 100 }
      ];

      maria.forEach(mare => {
        ctx.beginPath();
        ctx.ellipse(mare.x, mare.y, mare.width, mare.height, 0, 0, Math.PI * 2);
        ctx.fillStyle = '#696969';
        ctx.fill();
      });

      // Major lunar craters with realistic features
      const lunarCraters = [
        { name: 'Tycho', x: 350, y: 700, size: 80 },
        { name: 'Copernicus', x: 500, y: 400, size: 60 },
        { name: 'Kepler', x: 250, y: 350, size: 40 },
        { name: 'Aristarchus', x: 150, y: 250, size: 45 }
      ];

      lunarCraters.forEach(crater => {
        // Crater rim
        ctx.beginPath();
        ctx.arc(crater.x, crater.y, crater.size, 0, Math.PI * 2);
        ctx.fillStyle = '#E5E5E5';
        ctx.fill();

        // Crater floor
        ctx.beginPath();
        ctx.arc(crater.x, crater.y, crater.size * 0.8, 0, Math.PI * 2);
        ctx.fillStyle = '#A0A0A0';
        ctx.fill();

        // Central peak (for larger craters)
        if (crater.size > 50) {
          ctx.beginPath();
          ctx.arc(crater.x, crater.y, crater.size * 0.1, 0, Math.PI * 2);
          ctx.fillStyle = '#D3D3D3';
          ctx.fill();
        }

        // Ray system (for young craters like Tycho)
        if (crater.name === 'Tycho') {
          for (let i = 0; i < 8; i++) {
            const angle = (i * Math.PI * 2) / 8;
            const rayLength = 200 + Math.random() * 100;

            ctx.beginPath();
            ctx.moveTo(crater.x, crater.y);
            ctx.lineTo(
              crater.x + Math.cos(angle) * rayLength,
              crater.y + Math.sin(angle) * rayLength
            );
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
            ctx.lineWidth = 8;
            ctx.stroke();
          }
        }
      });
      break;

    case 'shadow':
      // Ethereal shadow planets (Rahu/Ketu) with mystical energy
      const shadowGradient = ctx.createRadialGradient(512, 512, 0, 512, 512, 512);
      shadowGradient.addColorStop(0, 'rgba(75, 85, 99, 0.9)');
      shadowGradient.addColorStop(0.5, 'rgba(55, 65, 81, 0.7)');
      shadowGradient.addColorStop(1, 'rgba(31, 41, 55, 0.5)');
      ctx.fillStyle = shadowGradient;
      ctx.fillRect(0, 0, 1024, 1024);

      // Add ethereal energy patterns and wisps
      for (let i = 0; i < 30; i++) {
        const x = Math.random() * 1024;
        const y = Math.random() * 1024;
        const size = Math.random() * 80 + 40;
        const opacity = Math.random() * 0.4 + 0.2;

        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(156, 163, 175, ${opacity})`;
        ctx.fill();

        // Add swirling energy patterns
        ctx.beginPath();
        ctx.arc(x, y, size * 0.6, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(209, 213, 219, ${opacity * 0.5})`;
        ctx.fill();
      }

      // Add mystical energy streams
      for (let i = 0; i < 15; i++) {
        ctx.strokeStyle = `rgba(156, 163, 175, ${Math.random() * 0.4 + 0.2})`;
        ctx.lineWidth = Math.random() * 8 + 3;
        ctx.beginPath();

        const startX = Math.random() * 1024;
        const startY = Math.random() * 1024;
        const controlX = Math.random() * 1024;
        const controlY = Math.random() * 1024;
        const endX = Math.random() * 1024;
        const endY = Math.random() * 1024;

        ctx.moveTo(startX, startY);
        ctx.quadraticCurveTo(controlX, controlY, endX, endY);
        ctx.stroke();
      }
      break;

    default:
      // Default rocky texture
      const defaultGradient = ctx.createRadialGradient(512, 512, 0, 512, 512, 512);
      defaultGradient.addColorStop(0, color);
      defaultGradient.addColorStop(1, '#333333');
      ctx.fillStyle = defaultGradient;
      ctx.fillRect(0, 0, 1024, 1024);
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  texture.generateMipmaps = true;
  return texture;
}

// Constellation symbols and data
const CONSTELLATIONS = [
  { name: 'Aries', symbol: '♈', unicode: '♈', color: '#ff6b6b' },
  { name: 'Taurus', symbol: '♉', unicode: '♉', color: '#4ecdc4' },
  { name: 'Gemini', symbol: '♊', unicode: '♊', color: '#45b7d1' },
  { name: 'Cancer', symbol: '♋', unicode: '♋', color: '#96ceb4' },
  { name: 'Leo', symbol: '♌', unicode: '♌', color: '#feca57' },
  { name: 'Virgo', symbol: '♍', unicode: '♍', color: '#ff9ff3' },
  { name: 'Libra', symbol: '♎', unicode: '♎', color: '#54a0ff' },
  { name: 'Scorpio', symbol: '♏', unicode: '♏', color: '#5f27cd' },
  { name: 'Sagittarius', symbol: '♐', unicode: '♐', color: '#00d2d3' },
  { name: 'Capricorn', symbol: '♑', unicode: '♑', color: '#ff6348' },
  { name: 'Aquarius', symbol: '♒', unicode: '♒', color: '#2ed573' },
  { name: 'Pisces', symbol: '♓', unicode: '♓', color: '#747d8c' }
];

// Vedic Astrology Data with EARTH-CENTRIC Accurate Distances
// All distances are from EARTH's perspective (geocentric view)
// Scaled down for visibility while maintaining relative proportions

// Calculate positions in circular orbits around Earth (geocentric view)
const calculatePosition = (distance: number, angle: number = 0): [number, number, number] => {
  return [
    Math.cos(angle) * distance,
    Math.sin(angle * 0.3) * 2, // Slight vertical variation for visibility
    Math.sin(angle) * distance
  ];
};

// Moon is handled separately as it orbits Earth, not included in PLANETS array
const PLANETS = [
  {
    name: 'Venus (Shukra)',
    position: calculatePosition(4.2, Math.PI * 0.7), // 0.17-1.74 AU from Earth (average ~0.42)
    color: '#fbbf24', // Bright yellowish-white (thick atmosphere)
    emissive: '#f59e0b',
    size: 0.95,
    texture: 'cloudy', // Thick cloud cover
    realDistance: '25-261 million km (0.17-1.74 AU from Earth)',
    isMoving: true, // Venus moves in its orbit
    orbitSpeed: 0.15 // Faster orbit
  },
  {
    name: 'Mercury (Budh)',
    position: calculatePosition(9.0, Math.PI * 0.3), // 0.32-1.48 AU from Earth (average ~0.9)
    color: '#a3a3a3', // Dark gray rocky surface
    emissive: '#737373',
    size: 0.38,
    texture: 'rocky', // Heavily cratered like Moon
    realDistance: '48-222 million km (0.32-1.48 AU from Earth)',
    isMoving: true, // Mercury moves in its orbit
    orbitSpeed: 0.25 // Fastest orbit (closest to Sun)
  },
  {
    name: 'Sun (Surya)',
    position: calculatePosition(10.0, 0), // 1.0 AU from Earth - at 0° angle (positive X-axis)
    color: '#fbbf24', // Bright golden-yellow
    emissive: '#f59e0b',
    size: 2.5,
    texture: 'solar', // Plasma surface with solar flares
    realDistance: '149.6 million km (1.0 AU from Earth)',
    isMoving: true, // Sun appears to move from Earth's perspective
    orbitSpeed: 0.05 // Slow apparent movement (1 year cycle)
  },
  {
    name: 'Mars (Mangal)',
    position: calculatePosition(12.0, Math.PI * 1.4), // 0.23-2.68 AU from Earth (average ~1.2)
    color: '#dc2626', // Rusty red iron oxide
    emissive: '#991b1b',
    size: 0.53,
    texture: 'desert', // Red desert with polar ice caps
    realDistance: '35-401 million km (0.23-2.68 AU from Earth)',
    isMoving: true, // Mars moves in its orbit
    orbitSpeed: 0.08 // Slower than inner planets
  },
  {
    name: 'Jupiter (Guru)',
    position: calculatePosition(44.0, Math.PI), // 2.6-6.2 AU from Earth - at 180° angle (negative X-axis)
    color: '#d97706', // Orange-brown with bands
    emissive: '#92400e',
    size: 2.2,
    texture: 'gas_giant', // Swirling gas bands and Great Red Spot
    realDistance: '390-928 million km (2.6-6.2 AU from Earth)',
    isMoving: true, // Jupiter moves in its orbit
    orbitSpeed: 0.03 // Much slower (12-year cycle)
  },
  {
    name: 'Saturn (Shani)',
    position: calculatePosition(82.0, Math.PI * 0.1), // 5.0-11.2 AU from Earth (average ~8.2)
    color: '#fbbf24', // Pale golden-yellow
    emissive: '#d97706',
    size: 1.8,
    texture: 'ringed', // Pale with prominent rings
    realDistance: '746-1.68 billion km (5.0-11.2 AU from Earth)',
    isMoving: true, // Saturn moves in its orbit
    orbitSpeed: 0.02 // Very slow (29-year cycle)
  },
  {
    name: 'Rahu',
    position: calculatePosition(15.0, Math.PI * 1.6), // Conceptual distance
    color: '#4b5563', // Dark shadow
    emissive: '#374151',
    size: 0.3,
    texture: 'shadow', // Ethereal shadow planet
    realDistance: 'Shadow planet (conceptual)',
    isMoving: false, // Rahu is FIXED (lunar node)
    orbitSpeed: 0 // No orbital movement
  },
  {
    name: 'Ketu',
    position: calculatePosition(15.0, Math.PI * 1.6 + Math.PI), // Opposite Rahu
    color: '#6b7280', // Lighter shadow
    emissive: '#4b5563',
    size: 0.3,
    texture: 'shadow', // Ethereal shadow planet
    realDistance: 'Shadow planet (conceptual)',
    isMoving: false, // Ketu is FIXED (lunar node)
    orbitSpeed: 0 // No orbital movement
  },
];

const RASHIS = [
  'Aries (Mesha)', 'Taurus (Vrishabha)', 'Gemini (Mithuna)',
  'Cancer (Karka)', 'Leo (Simha)', 'Virgo (Kanya)',
  'Libra (Tula)', 'Scorpio (Vrishchika)', 'Sagittarius (Dhanu)',
  'Capricorn (Makara)', 'Aquarius (Kumbha)', 'Pisces (Meena)'
];

const NAKSHATRAS = [
  'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
  'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
  'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
  'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
  'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
];

// Individual Planet Component with Realistic Textures and Vedic Movement
function Planet({ name, position, color, size, emissive, texture, isMoving = true, orbitSpeed = 0.1 }: {
  name: string;
  position: [number, number, number];
  color: string;
  size: number;
  emissive: string;
  texture: string;
  isMoving?: boolean;
  orbitSpeed?: number;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const atmosphereRef = useRef<THREE.Mesh>(null);
  const orbitGroupRef = useRef<THREE.Group>(null);

  // Create realistic texture for this planet
  const planetTexture = useMemo(() => createPlanetTexture(texture, color), [texture, color]);

  useFrame((state) => {
    if (meshRef.current) {
      // Gentle floating animation (for all planets)
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime + position[0]) * 0.2;

      // Rotation based on planet type (all planets rotate on axis)
      if (texture === 'gas_giant' || texture === 'ringed') {
        // Gas giants rotate faster
        meshRef.current.rotation.y = state.clock.elapsedTime * 0.3;
      } else if (texture === 'solar') {
        // Sun has complex rotation
        meshRef.current.rotation.y = state.clock.elapsedTime * 0.1;
        meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.1) * 0.1;
      } else {
        // Rocky planets rotate slower
        meshRef.current.rotation.y = state.clock.elapsedTime * 0.05;
      }
    }

    if (atmosphereRef.current) {
      // Atmosphere rotates independently
      atmosphereRef.current.rotation.y = state.clock.elapsedTime * 0.08;
    }

    // Orbital movement - only for moving planets (not Rahu/Ketu)
    if (orbitGroupRef.current && isMoving) {
      orbitGroupRef.current.rotation.y = state.clock.elapsedTime * orbitSpeed;
    }
  });

  // Determine material properties based on texture type
  const getMaterialProps = () => {
    switch (texture) {
      case 'solar':
        return {
          emissiveIntensity: 0.8,
          shininess: 100,
          opacity: 0.9,
          roughness: 0.1,
          metalness: 0.0
        };
      case 'gas_giant':
        return {
          emissiveIntensity: 0.2,
          shininess: 20,
          opacity: 0.7,
          roughness: 0.9,
          metalness: 0.0
        };
      case 'cloudy':
        return {
          emissiveIntensity: 0.3,
          shininess: 80,
          opacity: 0.8,
          roughness: 0.2,
          metalness: 0.0
        };
      case 'rocky':
      case 'lunar':
        return {
          emissiveIntensity: 0.05,
          shininess: 5,
          opacity: 0.6,
          roughness: 0.95,
          metalness: 0.1
        };
      case 'desert':
        return {
          emissiveIntensity: 0.1,
          shininess: 10,
          opacity: 0.65,
          roughness: 0.9,
          metalness: 0.05
        };
      case 'shadow':
        return {
          emissiveIntensity: 0.1,
          shininess: 0,
          opacity: 0.4,
          roughness: 1.0,
          metalness: 0.0
        };
      default:
        return {
          emissiveIntensity: 0.15,
          shininess: 30,
          opacity: 0.6,
          roughness: 0.8,
          metalness: 0.1
        };
    }
  };

  const materialProps = getMaterialProps();

  return (
    <group ref={orbitGroupRef}>
      {/* Main Planet Sphere with Realistic Texture */}
      <Sphere ref={meshRef} position={position} args={[size, 128, 128]}>
        <meshStandardMaterial
          map={planetTexture}
          color={color}
          emissive={emissive}
          emissiveIntensity={materialProps.emissiveIntensity}
          roughness={materialProps.roughness}
          metalness={materialProps.metalness}
          transparent
          opacity={materialProps.opacity}
        />
      </Sphere>

      {/* Atmosphere for gas giants and Venus */}
      {(texture === 'gas_giant' || texture === 'cloudy' || texture === 'solar') && (
        <Sphere ref={atmosphereRef} position={position} args={[size * 1.1, 32, 32]}>
          <meshBasicMaterial
            color={emissive}
            transparent
            opacity={0.15}
            side={THREE.BackSide}
          />
        </Sphere>
      )}

      {/* Saturn's Rings */}
      {texture === 'ringed' && (
        <Ring
          position={position}
          args={[size * 1.5, size * 2.5, 64]}
          rotation={[Math.PI / 2 + 0.2, 0, 0]}
        >
          <meshBasicMaterial
            color="#d1d5db"
            transparent
            opacity={0.4}
            side={THREE.DoubleSide}
          />
        </Ring>
      )}

      {/* Planet Label */}
      <Text
        position={[position[0], position[1] + size + 1, position[2]]}
        fontSize={0.8}
        color={isMoving ? color : '#6b7280'} // Dimmer color for fixed planets
        anchorX="center"
        anchorY="middle"
      >
        {name} {!isMoving}
      </Text>

      {/* Orbital glow effect */}
      <Ring
        position={position}
        args={[size + 0.2, size + 0.4, 16]}
        rotation={[Math.PI / 2, 0, 0]}
      >
        <meshBasicMaterial
          color={color}
          transparent
          opacity={isMoving ? 0.2 : 0.1} // Dimmer glow for fixed planets
          side={THREE.DoubleSide}
        />
      </Ring>
    </group>
  );
}

// Moon Component - Orbits around Earth
function Moon() {
  const moonRef = useRef<THREE.Mesh>(null);
  const orbitRef = useRef<THREE.Group>(null);

  // Create realistic lunar texture
  const moonTexture = useMemo(() => createPlanetTexture('lunar', '#d1d5db'), []);

  useFrame((state) => {
    if (orbitRef.current) {
      // Moon orbits around Earth - MOVING (faster than planets)
      orbitRef.current.rotation.y = state.clock.elapsedTime * 0.8; // Faster orbit speed
    }

    if (moonRef.current) {
      // Moon rotation on its axis (slower)
      moonRef.current.rotation.y = state.clock.elapsedTime * 0.1;
    }
  });

  const moonDistance = 2.5; // Distance from Earth center (scaled)

  return (
    <group ref={orbitRef}>
      {/* Moon Orbital Path */}
      <Ring args={[moonDistance - 0.05, moonDistance + 0.05, 64]} rotation={[Math.PI / 2, 0, 0]}>
        <meshBasicMaterial
          color="#9ca3af"
          transparent
          opacity={0.2}
          side={THREE.DoubleSide}
        />
      </Ring>

      {/* Moon with Realistic Texture */}
      <Sphere ref={moonRef} position={[moonDistance, 0, 0]} args={[0.15, 64, 64]}>
        <meshStandardMaterial
          map={moonTexture}
          color="#d1d5db" // Realistic gray-white lunar surface
          emissive="#9ca3af"
          emissiveIntensity={0.05}
          roughness={0.95}
          metalness={0.1}
          transparent
          opacity={0.7}
        />
      </Sphere>

      {/* Moon Label */}
      <Text
        position={[moonDistance, 0.5, 0]}
        fontSize={0.4}
        color="#d1d5db"
        anchorX="center"
        anchorY="middle"
      >
        🌙 Moon (Chandra) - MOVING
      </Text>

      {/* Moon Glow Effect */}
      <Ring
        position={[moonDistance, 0, 0]}
        args={[0.18, 0.25, 16]}
        rotation={[Math.PI / 2, 0, 0]}
      >
        <meshBasicMaterial
          color="#d1d5db"
          transparent
          opacity={0.15}
          side={THREE.DoubleSide}
        />
      </Ring>
    </group>
  );
}

// Earth at Center Component - Enhanced 3D Appearance with Blinking Effect
function Earth() {
  const earthRef = useRef<THREE.Mesh>(null);
  const cloudsRef = useRef<THREE.Mesh>(null);
  const atmosphereRef = useRef<THREE.Mesh>(null);
  const pulseRingRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (earthRef.current) {
      // Earth rotation
      earthRef.current.rotation.y = state.clock.elapsedTime * 0.1;

      // Blinking effect - pulsing emissive intensity
      const blinkIntensity = 0.2 + Math.sin(state.clock.elapsedTime * 2) * 0.15;
      (earthRef.current.material as THREE.MeshPhongMaterial).emissiveIntensity = blinkIntensity;
    }

    if (cloudsRef.current) {
      // Clouds rotate slightly faster
      cloudsRef.current.rotation.y = state.clock.elapsedTime * 0.12;
    }

    if (atmosphereRef.current) {
      // Atmosphere pulsing effect
      const atmospherePulse = 0.1 + Math.sin(state.clock.elapsedTime * 1.5) * 0.05;
      (atmosphereRef.current.material as THREE.MeshBasicMaterial).opacity = atmospherePulse;
    }

    if (pulseRingRef.current) {
      // Pulsing ring around Earth
      const ringPulse = 0.3 + Math.sin(state.clock.elapsedTime * 3) * 0.2;
      (pulseRingRef.current.material as THREE.MeshBasicMaterial).opacity = ringPulse;
      pulseRingRef.current.rotation.z = state.clock.elapsedTime * 0.5;
    }
  });

  return (
    <group>
      {/* Earth Core - Realistic blue-green with continents */}
      <Sphere ref={earthRef} args={[1.0, 64, 64]}>
        <meshPhongMaterial
          color="#1e40af" // Deep ocean blue
          emissive="#065f46" // Dark green continents
          emissiveIntensity={0.2}
          shininess={50}
          specular="#ffffff"
          transparent
          opacity={0.7}
        />
      </Sphere>

      {/* Earth Clouds Layer - More realistic */}
      <Sphere ref={cloudsRef} args={[1.05, 32, 32]}>
        <meshBasicMaterial
          color="#f8fafc" // Slightly off-white clouds
          transparent
          opacity={0.25}
          side={THREE.DoubleSide}
        />
      </Sphere>

      {/* Earth Atmosphere - Pulsing blue glow */}
      <Sphere ref={atmosphereRef} args={[1.15, 32, 32]}>
        <meshBasicMaterial
          color="#3b82f6"
          transparent
          opacity={0.1}
          side={THREE.BackSide}
        />
      </Sphere>

      {/* Pulsing Ring Effect around Earth */}
      <Ring
        ref={pulseRingRef}
        args={[1.3, 1.6, 32]}
        rotation={[Math.PI / 2, 0, 0]}
      >
        <meshBasicMaterial
          color="#22c55e"
          transparent
          opacity={0.3}
          side={THREE.DoubleSide}
        />
      </Ring>

      {/* Secondary Pulse Ring */}
      <Ring
        args={[1.7, 1.9, 32]}
        rotation={[Math.PI / 2, 0, 0]}
      >
        <meshBasicMaterial
          color="#10b981"
          transparent
          opacity={0.15}
          side={THREE.DoubleSide}
        />
      </Ring>

      {/* Earth Label with Enhanced Visibility */}
      <Text
        position={[0, -2.5, 0]}
        fontSize={0.8}
        color="#10b981"
        anchorX="center"
        anchorY="middle"
      >
        🌍 EARTH (Prithvi) - CENTER
      </Text>

      {/* Directional Indicator */}
      <Text
        position={[0, 2.5, 0]}
        fontSize={0.6}
        color="#fbbf24"
        anchorX="center"
        anchorY="middle"
      >
        ⭐ REFERENCE POINT ⭐
      </Text>

      {/* Orbital Path Indicators */}
      <Ring args={[2.5, 2.7, 64]} rotation={[Math.PI / 2, 0, 0]}>
        <meshBasicMaterial
          color="#22c55e"
          transparent
          opacity={0.2}
          side={THREE.DoubleSide}
        />
      </Ring>

      <Ring args={[3.0, 3.2, 64]} rotation={[Math.PI / 2, 0, 0]}>
        <meshBasicMaterial
          color="#10b981"
          transparent
          opacity={0.1}
          side={THREE.DoubleSide}
        />
      </Ring>

      {/* Cardinal Direction Markers */}
      <Sphere position={[2.8, 0, 0]} args={[0.05, 8, 8]}>
        <meshBasicMaterial color="#fbbf24" />
      </Sphere>
      <Sphere position={[-2.8, 0, 0]} args={[0.05, 8, 8]}>
        <meshBasicMaterial color="#fbbf24" />
      </Sphere>
      <Sphere position={[0, 0, 2.8]} args={[0.05, 8, 8]}>
        <meshBasicMaterial color="#fbbf24" />
      </Sphere>
      <Sphere position={[0, 0, -2.8]} args={[0.05, 8, 8]}>
        <meshBasicMaterial color="#fbbf24" />
      </Sphere>
    </group>
  );
}

// 3D Constellation Sectors Component - STATIC (Fixed Star Patterns)
function ConstellationSectors() {
  // Constellations are STATIC - they are fixed star patterns spanning 30° each

  const constellationSectors = useMemo(() => {
    return CONSTELLATIONS.map((constellation, index) => {
      const startAngle = (index * 30) * (Math.PI / 180); // 30 degrees per rashi
      const endAngle = ((index + 1) * 30) * (Math.PI / 180);
      const centerAngle = startAngle + (30 * Math.PI / 180) / 2; // Center of 30° sector
      const radius = 50;

      // Create sector geometry points
      const sectorPoints = [];
      const segments = 16; // Number of segments for smooth curve

      // Add center point
      sectorPoints.push(new THREE.Vector3(0, 0, 0));

      // Add arc points
      for (let i = 0; i <= segments; i++) {
        const angle = startAngle + (i / segments) * (endAngle - startAngle);
        sectorPoints.push(new THREE.Vector3(
          Math.cos(angle) * radius,
          0,
          Math.sin(angle) * radius
        ));
      }

      return {
        constellation,
        startAngle,
        endAngle,
        centerAngle,
        radius,
        sectorPoints,
        centerPosition: [
          Math.cos(centerAngle) * radius,
          0,
          Math.sin(centerAngle) * radius
        ] as [number, number, number],
        symbolPosition: [
          Math.cos(centerAngle) * (radius * 0.7), // Closer to center
          5, // Elevated above the plane
          Math.sin(centerAngle) * (radius * 0.7)
        ] as [number, number, number]
      };
    });
  }, []);

  return (
    <group>
      {/* 3D Constellation Sectors */}
      {constellationSectors.map((sector, index) => (
        <group key={index}>
          {/* 3D Sector Area - Transparent colored region */}
          <mesh>
            <cylinderGeometry
              args={[
                sector.radius, // top radius
                sector.radius, // bottom radius
                0.5, // height
                32, // radial segments
                1, // height segments
                false, // open ended
                sector.startAngle, // theta start
                (30 * Math.PI / 180) // theta length (30 degrees)
              ]}
            />
            <meshBasicMaterial
              color={sector.constellation.color}
              transparent
              opacity={0.05}
              side={THREE.DoubleSide}
            />
          </mesh>

          {/* Subtle Sector Border Lines */}
          <group>
            {/* Start angle line - more subtle */}


            {/* End angle line - more subtle */}
          </group>

          {/* Large 3D Constellation Symbol */}
          <Text
            position={sector.symbolPosition}
            fontSize={3.0}
            color={sector.constellation.color}
            anchorX="center"
            anchorY="middle"
          >
            {sector.constellation.symbol}
          </Text>

          {/* Constellation Name */}
          <Text
            position={[
              sector.symbolPosition[0],
              sector.symbolPosition[1] - 2,
              sector.symbolPosition[2]
            ]}
            fontSize={0.8}
            color={sector.constellation.color}
            anchorX="center"
            anchorY="middle"
          >
            {sector.constellation.name}
          </Text>

          {/* 30° Sector Label */}
          <Text
            position={[
              sector.symbolPosition[0],
              sector.symbolPosition[1] - 3.5,
              sector.symbolPosition[2]
            ]}
            fontSize={0.4}
            color={sector.constellation.color}
            anchorX="center"
            anchorY="middle"
          >
          </Text>

          {/* 3D Star Pattern within sector */}
          {Array.from({ length: 8 }).map((_, starIndex) => {
            // Distribute stars within the 30° sector
            const starAngle = sector.startAngle + (starIndex / 7) * (30 * Math.PI / 180);
            const starRadius = 30 + Math.random() * 15; // Vary distance
            const starHeight = (Math.random() - 0.5) * 8; // Vary height
            const starPos: [number, number, number] = [
              Math.cos(starAngle) * starRadius,
              starHeight,
              Math.sin(starAngle) * starRadius
            ];

            return (
              <Sphere key={starIndex} position={starPos} args={[0.08, 8, 8]}>
                <meshBasicMaterial
                  color={sector.constellation.color}
                  transparent
                  opacity={0.9}
                />
              </Sphere>
            );
          })}

          {/* Removed messy connecting lines - cleaner visualization */}
        </group>
      ))}

      {/* Outer boundary ring */}
      <Ring args={[49, 51, 64]} rotation={[Math.PI / 2, 0, 0]}>
        <meshBasicMaterial
          color="#ffffff"
          transparent
          opacity={0.2}
          side={THREE.DoubleSide}
        />
      </Ring>
    </group>
  );
}

// Nakshatra Ring Component - STATIC (Fixed Star Patterns)
function NakshatraRing() {
  // Nakshatras are STATIC - they are fixed star patterns and should not move

  const nakshatraPositions = useMemo(() => {
    return NAKSHATRAS.map((_, index) => {
      const angle = (index / NAKSHATRAS.length) * Math.PI * 2;
      const radius = 58; // Brought much closer - outer ring beyond zodiac
      return {
        position: [
          Math.cos(angle) * radius,
          Math.sin(index * 0.5) * 3, // Slight vertical variation
          Math.sin(angle) * radius
        ] as [number, number, number],
        name: NAKSHATRAS[index]
      };
    });
  }, []);

  return (
    <group>
      {/* Nakshatra Ring - STATIC */}
      <Ring args={[55, 61, 64]} rotation={[Math.PI / 2, 0, 0]}>
        <meshBasicMaterial
          color="#3b82f6"
          transparent
          opacity={0.08}
          side={THREE.DoubleSide}
        />
      </Ring>

      {/* Nakshatra Points - STATIC */}
      {nakshatraPositions.map((nakshatra, index) => (
        <group key={index}>
          <Sphere position={nakshatra.position} args={[0.1, 8, 8]}>
            <meshBasicMaterial color="#3b82f6" />
          </Sphere>
          <Text
            position={[nakshatra.position[0], nakshatra.position[1] + 0.8, nakshatra.position[2]]}
            fontSize={0.4}
            color="#60a5fa"
            anchorX="center"
            anchorY="middle"
          >
            {nakshatra.name} (STATIC)
          </Text>
        </group>
      ))}
    </group>
  );
}

// Main Celestial Sphere Component
export default function CelestialSphere() {
  return (
    <group>
      {/* Central Earth */}
      <Earth />

      {/* Moon orbiting Earth */}
      <Moon />

      {/* Planets with Vedic Movement */}
      {PLANETS.map((planet, index) => (
        <Planet
          key={index}
          name={planet.name}
          position={planet.position}
          color={planet.color}
          size={planet.size}
          emissive={planet.emissive}
          texture={planet.texture}
          isMoving={planet.isMoving}
          orbitSpeed={planet.orbitSpeed}
        />
      ))}

      {/* 3D Constellation Sectors */}
      <ConstellationSectors />

      {/* Nakshatras Ring */}
      <NakshatraRing />

      {/* Cosmic Grid */}
      <gridHelper args={[150, 30, '#374151', '#1f2937']} />
    </group>
  );
}
