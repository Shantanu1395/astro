// 3D Celestial Sphere Component for Vedic Astrology Visualization

import { useRef, useMemo } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import { Sphere, Text, Ring } from '@react-three/drei';
import * as THREE from 'three';

// Procedural Texture Generation for Realistic Planets
function createPlanetTexture(type: string, color: string): THREE.Texture {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d')!;

  // Create gradient background
  const gradient = ctx.createRadialGradient(256, 256, 0, 256, 256, 256);

  switch (type) {
    case 'solar':
      // Sun texture with solar flares
      gradient.addColorStop(0, '#ffff88');
      gradient.addColorStop(0.3, '#ffaa00');
      gradient.addColorStop(0.7, '#ff6600');
      gradient.addColorStop(1, '#cc3300');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 512, 512);

      // Add solar flares
      for (let i = 0; i < 20; i++) {
        ctx.fillStyle = `rgba(255, 255, 0, ${Math.random() * 0.5})`;
        ctx.beginPath();
        ctx.arc(Math.random() * 512, Math.random() * 512, Math.random() * 30 + 10, 0, Math.PI * 2);
        ctx.fill();
      }
      break;

    case 'rocky':
      // Rocky planet texture (Mercury)
      gradient.addColorStop(0, '#888888');
      gradient.addColorStop(0.5, '#666666');
      gradient.addColorStop(1, '#444444');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 512, 512);

      // Add craters
      for (let i = 0; i < 50; i++) {
        ctx.fillStyle = `rgba(0, 0, 0, ${Math.random() * 0.3 + 0.2})`;
        ctx.beginPath();
        ctx.arc(Math.random() * 512, Math.random() * 512, Math.random() * 20 + 5, 0, Math.PI * 2);
        ctx.fill();
      }
      break;

    case 'cloudy':
      // Venus cloud texture
      gradient.addColorStop(0, '#ffffcc');
      gradient.addColorStop(0.5, '#ffcc99');
      gradient.addColorStop(1, '#cc9966');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 512, 512);

      // Add cloud swirls
      for (let i = 0; i < 30; i++) {
        ctx.strokeStyle = `rgba(255, 255, 255, ${Math.random() * 0.3})`;
        ctx.lineWidth = Math.random() * 10 + 2;
        ctx.beginPath();
        ctx.arc(Math.random() * 512, Math.random() * 512, Math.random() * 50 + 20, 0, Math.PI * Math.random());
        ctx.stroke();
      }
      break;

    case 'desert':
      // Mars desert texture
      gradient.addColorStop(0, '#ff6666');
      gradient.addColorStop(0.5, '#cc3333');
      gradient.addColorStop(1, '#990000');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 512, 512);

      // Add dust storms and polar caps
      ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
      ctx.beginPath();
      ctx.arc(100, 100, 30, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(400, 400, 25, 0, Math.PI * 2);
      ctx.fill();
      break;

    case 'gas_giant':
      // Jupiter gas bands
      for (let y = 0; y < 512; y += 20) {
        const hue = Math.sin(y * 0.01) * 30 + 30;
        ctx.fillStyle = `hsl(${hue}, 70%, ${50 + Math.sin(y * 0.02) * 20}%)`;
        ctx.fillRect(0, y, 512, 20);
      }

      // Add Great Red Spot for Jupiter
      ctx.fillStyle = 'rgba(200, 50, 50, 0.8)';
      ctx.beginPath();
      ctx.ellipse(300, 200, 40, 25, 0, 0, Math.PI * 2);
      ctx.fill();
      break;

    case 'ringed':
      // Saturn pale yellow
      gradient.addColorStop(0, '#ffffaa');
      gradient.addColorStop(0.5, '#ffff88');
      gradient.addColorStop(1, '#cccc66');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 512, 512);

      // Add subtle bands
      for (let y = 0; y < 512; y += 40) {
        ctx.fillStyle = `rgba(255, 255, 255, ${Math.random() * 0.2})`;
        ctx.fillRect(0, y, 512, 10);
      }
      break;

    case 'lunar':
      // Moon texture
      gradient.addColorStop(0, '#dddddd');
      gradient.addColorStop(0.5, '#bbbbbb');
      gradient.addColorStop(1, '#999999');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 512, 512);

      // Add maria (dark spots)
      for (let i = 0; i < 15; i++) {
        ctx.fillStyle = `rgba(100, 100, 100, ${Math.random() * 0.4 + 0.3})`;
        ctx.beginPath();
        ctx.arc(Math.random() * 512, Math.random() * 512, Math.random() * 60 + 20, 0, Math.PI * 2);
        ctx.fill();
      }
      break;

    case 'shadow':
      // Rahu/Ketu ethereal texture
      gradient.addColorStop(0, 'rgba(100, 100, 100, 0.8)');
      gradient.addColorStop(0.5, 'rgba(70, 70, 70, 0.6)');
      gradient.addColorStop(1, 'rgba(40, 40, 40, 0.4)');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 512, 512);

      // Add ethereal wisps
      for (let i = 0; i < 20; i++) {
        ctx.strokeStyle = `rgba(150, 150, 150, ${Math.random() * 0.3})`;
        ctx.lineWidth = Math.random() * 5 + 1;
        ctx.beginPath();
        ctx.moveTo(Math.random() * 512, Math.random() * 512);
        ctx.quadraticCurveTo(Math.random() * 512, Math.random() * 512, Math.random() * 512, Math.random() * 512);
        ctx.stroke();
      }
      break;

    default:
      // Default texture
      gradient.addColorStop(0, color);
      gradient.addColorStop(1, '#333333');
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 512, 512);
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
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
      <Sphere ref={meshRef} position={position} args={[size, 64, 64]}>
        <meshPhongMaterial
          map={planetTexture}
          color={color}
          emissive={emissive}
          emissiveIntensity={materialProps.emissiveIntensity}
          shininess={materialProps.shininess}
          specular="#ffffff"
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
      <Sphere ref={moonRef} position={[moonDistance, 0, 0]} args={[0.15, 32, 32]}>
        <meshPhongMaterial
          map={moonTexture}
          color="#d1d5db" // Realistic gray-white lunar surface
          emissive="#9ca3af"
          emissiveIntensity={0.05}
          shininess={5}
          specular="#ffffff"
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

// Constellation Ring Component - STATIC (Fixed Star Patterns)
function ConstellationRing() {
  // Constellations are STATIC - they are fixed star patterns and should not move

  const constellationPositions = useMemo(() => {
    return CONSTELLATIONS.map((constellation, index) => {
      const angle = (index / CONSTELLATIONS.length) * Math.PI * 2;
      const radius = 50; // Brought much closer - between Jupiter and Saturn
      return {
        position: [
          Math.cos(angle) * radius,
          0,
          Math.sin(angle) * radius
        ] as [number, number, number],
        rotation: [0, -angle, 0] as [number, number, number],
        constellation
      };
    });
  }, []);

  return (
    <group>
      {/* Constellation Ring - STATIC */}
      <Ring args={[47, 53, 64]} rotation={[Math.PI / 2, 0, 0]}>
        <meshBasicMaterial
          color="#f97316"
          transparent
          opacity={0.1}
          side={THREE.DoubleSide}
        />
      </Ring>

      {/* Constellation Symbols - STATIC */}
      {constellationPositions.map((item, index) => (
        <group key={index}>
          {/* Large Constellation Symbol */}
          <Text
            position={item.position}
            rotation={item.rotation}
            fontSize={2.0}
            color={item.constellation.color}
            anchorX="center"
            anchorY="middle"
          >
            {item.constellation.symbol}
          </Text>

          {/* Constellation Name */}
          <Text
            position={[item.position[0], item.position[1] - 3, item.position[2]]}
            rotation={item.rotation}
            fontSize={0.5}
            color={item.constellation.color}
            anchorX="center"
            anchorY="middle"
          >
            {item.constellation.name}
          </Text>

          {/* Star Pattern Points */}
          {Array.from({ length: Math.floor(Math.random() * 5) + 3 }).map((_, starIndex) => {
            const starAngle = (starIndex / 5) * Math.PI * 2;
            const starRadius = Math.random() * 2 + 1;
            const starPos: [number, number, number] = [
              item.position[0] + Math.cos(starAngle) * starRadius,
              item.position[1] + (Math.random() - 0.5) * 2,
              item.position[2] + Math.sin(starAngle) * starRadius
            ];

            return (
              <Sphere key={starIndex} position={starPos} args={[0.05, 8, 8]}>
                <meshBasicMaterial
                  color={item.constellation.color}
                  transparent
                  opacity={0.8}
                />
              </Sphere>
            );
          })}
        </group>
      ))}
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

      {/* Constellation Symbols Ring */}
      <ConstellationRing />

      {/* Nakshatras Ring */}
      <NakshatraRing />

      {/* Cosmic Grid */}
      <gridHelper args={[150, 30, '#374151', '#1f2937']} />
    </group>
  );
}
