// 3D Celestial Sphere Component for Vedic Astrology Visualization

import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, Text, Ring } from '@react-three/drei';
import * as THREE from 'three';

// Vedic Astrology Data
const PLANETS = [
  { name: 'Sun (Surya)', position: [8, 2, 0] as [number, number, number], color: '#fbbf24', size: 0.8 },
  { name: 'Moon (Chandra)', position: [6, -3, 2] as [number, number, number], color: '#e5e7eb', size: 0.6 },
  { name: 'Mars (Mangal)', position: [10, 1, -2] as [number, number, number], color: '#dc2626', size: 0.5 },
  { name: 'Mercury (Budh)', position: [7, 4, 1] as [number, number, number], color: '#059669', size: 0.4 },
  { name: 'Jupiter (Guru)', position: [12, -1, 3] as [number, number, number], color: '#2563eb', size: 1.0 },
  { name: 'Venus (Shukra)', position: [9, -4, -1] as [number, number, number], color: '#ec4899', size: 0.7 },
  { name: 'Saturn (Shani)', position: [14, 2, -3] as [number, number, number], color: '#7c3aed', size: 0.9 },
  { name: 'Rahu', position: [11, 5, 2] as [number, number, number], color: '#78716c', size: 0.3 },
  { name: 'Ketu', position: [13, -3, -2] as [number, number, number], color: '#78716c', size: 0.3 },
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

// Individual Planet Component
function Planet({ name, position, color, size }: { 
  name: string; 
  position: [number, number, number]; 
  color: string; 
  size: number; 
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      // Gentle floating animation
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime + position[0]) * 0.2;
    }
  });

  return (
    <group>
      <Sphere ref={meshRef} position={position} args={[size, 16, 16]}>
        <meshStandardMaterial 
          color={color} 
          emissive={color} 
          emissiveIntensity={0.3}
          transparent
          opacity={0.8}
        />
      </Sphere>
      
      {/* Planet Label */}
      <Text
        position={[position[0], position[1] + size + 1, position[2]]}
        fontSize={0.8}
        color={color}
        anchorX="center"
        anchorY="middle"
      >
        {name}
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
          opacity={0.2}
          side={THREE.DoubleSide}
        />
      </Ring>
    </group>
  );
}

// Earth at Center Component
function Earth() {
  const earthRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (earthRef.current) {
      earthRef.current.rotation.y = state.clock.elapsedTime * 0.1;
    }
  });

  return (
    <group>
      {/* Earth Core */}
      <Sphere ref={earthRef} args={[2, 32, 32]}>
        <meshStandardMaterial 
          color="#4ade80" 
          emissive="#059669" 
          emissiveIntensity={0.1}
        />
      </Sphere>
      
      {/* Earth Atmosphere */}
      <Sphere args={[2.3, 32, 32]}>
        <meshBasicMaterial 
          color="#3b82f6" 
          transparent 
          opacity={0.2}
          side={THREE.BackSide}
        />
      </Sphere>
      
      {/* Earth Label */}
      <Text
        position={[0, -3.5, 0]}
        fontSize={1.2}
        color="#4ade80"
        anchorX="center"
        anchorY="middle"
      >
        🌍 Earth (Prithvi)
      </Text>
    </group>
  );
}

// Zodiac Ring Component
function ZodiacRing() {
  const ringRef = useRef<THREE.Group>(null);
  
  useFrame((state) => {
    if (ringRef.current) {
      ringRef.current.rotation.y = state.clock.elapsedTime * 0.02;
    }
  });

  const rashiPositions = useMemo(() => {
    return RASHIS.map((_, index) => {
      const angle = (index / RASHIS.length) * Math.PI * 2;
      const radius = 18;
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
    <group ref={ringRef}>
      {/* Zodiac Ring */}
      <Ring args={[17, 19, 64]} rotation={[Math.PI / 2, 0, 0]}>
        <meshBasicMaterial 
          color="#f97316" 
          transparent 
          opacity={0.1}
          side={THREE.DoubleSide}
        />
      </Ring>
      
      {/* Rashi Labels */}
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
          {rashi.name}
        </Text>
      ))}
    </group>
  );
}

// Nakshatra Ring Component
function NakshatraRing() {
  const ringRef = useRef<THREE.Group>(null);
  
  useFrame((state) => {
    if (ringRef.current) {
      ringRef.current.rotation.y = -state.clock.elapsedTime * 0.01;
    }
  });

  const nakshatraPositions = useMemo(() => {
    return NAKSHATRAS.map((_, index) => {
      const angle = (index / NAKSHATRAS.length) * Math.PI * 2;
      const radius = 22;
      return {
        position: [
          Math.cos(angle) * radius,
          Math.sin(index * 0.5) * 2, // Slight vertical variation
          Math.sin(angle) * radius
        ] as [number, number, number],
        name: NAKSHATRAS[index]
      };
    });
  }, []);

  return (
    <group ref={ringRef}>
      {/* Nakshatra Ring */}
      <Ring args={[21, 23, 64]} rotation={[Math.PI / 2, 0, 0]}>
        <meshBasicMaterial 
          color="#3b82f6" 
          transparent 
          opacity={0.08}
          side={THREE.DoubleSide}
        />
      </Ring>
      
      {/* Nakshatra Points */}
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
            {nakshatra.name}
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
      
      {/* Planets */}
      {PLANETS.map((planet, index) => (
        <Planet
          key={index}
          name={planet.name}
          position={planet.position}
          color={planet.color}
          size={planet.size}
        />
      ))}
      
      {/* Zodiac Signs Ring */}
      <ZodiacRing />
      
      {/* Nakshatras Ring */}
      <NakshatraRing />
      
      {/* Cosmic Grid */}
      <gridHelper args={[50, 20, '#374151', '#1f2937']} />
    </group>
  );
}
