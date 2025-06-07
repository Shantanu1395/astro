// 3D Celestial Sphere Component for Vedic Astrology Visualization

import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, Text, Ring } from '@react-three/drei';
import * as THREE from 'three';

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
      {/* Main Planet Sphere */}
      <Sphere ref={meshRef} position={position} args={[size, 64, 64]}>
        <meshPhongMaterial
          color={color}
          emissive={emissive}
          emissiveIntensity={materialProps.emissiveIntensity}
          shininess={materialProps.shininess}
          specular="#ffffff"
          transparent
          opacity={materialProps.opacity}
          roughness={materialProps.roughness}
          metalness={materialProps.metalness}
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

      {/* Moon */}
      <Sphere ref={moonRef} position={[moonDistance, 0, 0]} args={[0.15, 32, 32]}>
        <meshPhongMaterial
          color="#d1d5db" // Realistic gray-white lunar surface
          emissive="#9ca3af"
          emissiveIntensity={0.05}
          shininess={5}
          specular="#ffffff"
          transparent
          opacity={0.7}
          roughness={0.95}
          metalness={0.1}
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
          roughness={0.6}
          metalness={0.1}
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

// Zodiac Ring Component - STATIC (Fixed Star Patterns)
function ZodiacRing() {
  // Rashis are STATIC - they are fixed star patterns and should not move

  const rashiPositions = useMemo(() => {
    return RASHIS.map((_, index) => {
      const angle = (index / RASHIS.length) * Math.PI * 2;
      const radius = 50; // Brought much closer - between Jupiter and Saturn
      return {
        position: [
          Math.cos(angle) * radius,
          0,
          Math.sin(angle) * radius
        ] as [number, number, number],
        rotation: [0, -angle, 0] as [number, number, number],
        name: RASHIS[index]
      };
    });
  }, []);

  return (
    <group>
      {/* Zodiac Ring - STATIC */}
      <Ring args={[47, 53, 64]} rotation={[Math.PI / 2, 0, 0]}>
        <meshBasicMaterial
          color="#f97316"
          transparent
          opacity={0.1}
          side={THREE.DoubleSide}
        />
      </Ring>

      {/* Rashi Labels - STATIC */}
      {rashiPositions.map((rashi, index) => (
        <Text
          key={index}
          position={rashi.position}
          rotation={rashi.rotation}
          fontSize={0.6}
          color="#f97316"
          anchorX="center"
          anchorY="middle"
        >
          {rashi.name} (STATIC)
        </Text>
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

      {/* Zodiac Signs Ring */}
      <ZodiacRing />

      {/* Nakshatras Ring */}
      <NakshatraRing />

      {/* Cosmic Grid */}
      <gridHelper args={[150, 30, '#374151', '#1f2937']} />
    </group>
  );
}
