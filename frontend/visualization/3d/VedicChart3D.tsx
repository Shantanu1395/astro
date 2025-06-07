// 3D Vedic Astrology Chart Component

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text, Sphere, Ring, Line } from '@react-three/drei';
import * as THREE from 'three';
import type { ChartData } from '@/types/astrology';

interface VedicChart3DProps {
  chartData: ChartData;
  highlightedElements: string[];
  animationsEnabled: boolean;
}

const VedicChart3D: React.FC<VedicChart3DProps> = ({
  chartData,
  highlightedElements,
  animationsEnabled,
}) => {
  const earthRef = useRef<THREE.Mesh>(null);
  const celestialSphereRef = useRef<THREE.Group>(null);

  // Rotate the celestial sphere
  useFrame((state, delta) => {
    if (animationsEnabled && celestialSphereRef.current) {
      celestialSphereRef.current.rotation.y += delta * 0.1;
    }
    
    if (animationsEnabled && earthRef.current) {
      earthRef.current.rotation.y += delta * 0.5;
    }
  });

  // Calculate planetary positions
  const planetaryPositions = useMemo(() => {
    if (!chartData?.planets) return [];
    
    return Object.entries(chartData.planets).map(([key, planet]) => {
      const angle = (planet.position.longitude * Math.PI) / 180;
      const distance = key === 'sun' ? 150 : key === 'moon' ? 80 : 200;
      
      return {
        key,
        planet,
        position: [
          Math.cos(angle) * distance,
          0,
          Math.sin(angle) * distance,
        ] as [number, number, number],
      };
    });
  }, [chartData]);

  // Calculate rashi positions
  const rashiPositions = useMemo(() => {
    return chartData?.rashis?.map((rashi, index) => {
      const angle = (index * 30 * Math.PI) / 180;
      const distance = 300;
      
      return {
        rashi,
        position: [
          Math.cos(angle) * distance,
          0,
          Math.sin(angle) * distance,
        ] as [number, number, number],
        angle,
      };
    }) || [];
  }, [chartData]);

  return (
    <group>
      {/* Earth at Center */}
      <Sphere ref={earthRef} args={[20, 32, 32]} position={[0, 0, 0]}>
        <meshPhongMaterial 
          color="#00aa88" 
          transparent 
          opacity={0.8}
          emissive="#001122"
        />
      </Sphere>

      {/* Earth Atmosphere */}
      <Sphere args={[25, 32, 32]} position={[0, 0, 0]}>
        <meshBasicMaterial 
          color="#4488ff" 
          transparent 
          opacity={0.2}
        />
      </Sphere>

      {/* Celestial Sphere */}
      <group ref={celestialSphereRef}>
        {/* Zodiac Ring */}
        <Ring args={[290, 310, 64]} rotation={[-Math.PI / 2, 0, 0]}>
          <meshBasicMaterial 
            color="#ff9500" 
            transparent 
            opacity={0.3}
            side={THREE.DoubleSide}
          />
        </Ring>

        {/* Rashis */}
        {rashiPositions.map(({ rashi, position, angle }, index) => (
          <group key={rashi.name} position={position}>
            <Sphere args={[12, 16, 16]}>
              <meshPhongMaterial 
                color={rashi.color || "#ff9500"} 
                transparent 
                opacity={highlightedElements.includes(rashi.name) ? 0.8 : 0.4}
                emissive={highlightedElements.includes(rashi.name) ? "#ff4400" : "#000000"}
              />
            </Sphere>
            
            <Text
              position={[0, -25, 0]}
              fontSize={8}
              color="#ffffff"
              anchorX="center"
              anchorY="middle"
            >
              {rashi.symbol}
            </Text>
          </group>
        ))}

        {/* Planets */}
        {planetaryPositions.map(({ key, planet, position }) => (
          <group key={key} position={position}>
            <Sphere args={[planet.size || 10, 16, 16]}>
              <meshPhongMaterial 
                color={planet.color || "#ffffff"} 
                transparent 
                opacity={highlightedElements.includes(planet.name) ? 0.9 : 0.6}
                emissive={key === 'sun' ? "#332200" : "#000000"}
              />
            </Sphere>

            {/* Planet Glow for Sun */}
            {key === 'sun' && (
              <Sphere args={[planet.size * 1.5 || 15, 16, 16]}>
                <meshBasicMaterial 
                  color="#ffff00" 
                  transparent 
                  opacity={0.3}
                />
              </Sphere>
            )}

            {/* Retrograde Indicator */}
            {planet.position.retrograde && (
              <Ring 
                args={[planet.size * 2 || 20, planet.size * 2.5 || 25, 16]} 
                rotation={[-Math.PI / 2, 0, 0]}
              >
                <meshBasicMaterial 
                  color="#ff6464" 
                  transparent 
                  opacity={0.7}
                  side={THREE.DoubleSide}
                />
              </Ring>
            )}

            <Text
              position={[0, -30, 0]}
              fontSize={6}
              color="#ffffff"
              anchorX="center"
              anchorY="middle"
            >
              {planet.name}
            </Text>
          </group>
        ))}

        {/* Orbital Lines */}
        {planetaryPositions.map(({ key, position }) => {
          const distance = Math.sqrt(position[0] ** 2 + position[2] ** 2);
          return (
            <Ring 
              key={`orbit-${key}`}
              args={[distance - 2, distance + 2, 64]} 
              rotation={[-Math.PI / 2, 0, 0]}
            >
              <meshBasicMaterial 
                color="#ffffff" 
                transparent 
                opacity={0.1}
                side={THREE.DoubleSide}
              />
            </Ring>
          );
        })}
      </group>

      {/* House Division Lines */}
      {Array.from({ length: 12 }).map((_, i) => {
        const angle = (i * 30 * Math.PI) / 180;
        const start = [0, 0, 0];
        const end = [Math.cos(angle) * 400, 0, Math.sin(angle) * 400];
        
        return (
          <Line
            key={`house-line-${i}`}
            points={[start, end]}
            color="#666666"
            transparent
            opacity={0.3}
            lineWidth={1}
          />
        );
      })}

      {/* Coordinate System Helper (Development) */}
      {process.env.NODE_ENV === 'development' && (
        <group>
          <Line points={[[0, 0, 0], [100, 0, 0]]} color="red" lineWidth={2} />
          <Line points={[[0, 0, 0], [0, 100, 0]]} color="green" lineWidth={2} />
          <Line points={[[0, 0, 0], [0, 0, 100]]} color="blue" lineWidth={2} />
        </group>
      )}
    </group>
  );
};

export default VedicChart3D;
