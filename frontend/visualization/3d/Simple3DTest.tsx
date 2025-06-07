// Simple 3D Test Component

import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

// Rotating Earth component
function Earth() {
  const earthRef = useRef<THREE.Mesh>(null);
  
  useFrame((state, delta) => {
    if (earthRef.current) {
      earthRef.current.rotation.y += delta * 0.5;
    }
  });

  return (
    <mesh ref={earthRef} position={[0, 0, 0]}>
      <sphereGeometry args={[1, 32, 32]} />
      <meshPhongMaterial color="#00aa88" />
    </mesh>
  );
}

// Simple planet component
function Planet({ position, color, size = 0.3 }: { position: [number, number, number], color: string, size?: number }) {
  const planetRef = useRef<THREE.Mesh>(null);
  
  useFrame((state, delta) => {
    if (planetRef.current) {
      planetRef.current.rotation.y += delta * 2;
    }
  });

  return (
    <mesh ref={planetRef} position={position}>
      <sphereGeometry args={[size, 16, 16]} />
      <meshPhongMaterial color={color} />
    </mesh>
  );
}

// Main 3D Test component
const Simple3DTest: React.FC = () => {
  return (
    <div className="w-full h-96 bg-cosmic-deep/50 rounded-lg border border-stellar-silver/20 overflow-hidden">
      <Canvas camera={{ position: [0, 2, 5], fov: 75 }}>
        {/* Lighting */}
        <ambientLight intensity={0.4} />
        <directionalLight position={[10, 10, 5]} intensity={0.8} />
        <pointLight position={[0, 0, 0]} intensity={0.5} />

        {/* Controls */}
        <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />

        {/* Earth at center */}
        <Earth />

        {/* Simple planets */}
        <Planet position={[3, 0, 0]} color="#fbbf24" size={0.4} /> {/* Sun */}
        <Planet position={[-2, 0, 0]} color="#e5e7eb" size={0.2} /> {/* Moon */}
        <Planet position={[0, 0, 4]} color="#dc2626" size={0.25} /> {/* Mars */}
        <Planet position={[0, 0, -3]} color="#2563eb" size={0.35} /> {/* Jupiter */}

        {/* Orbital rings */}
        <mesh rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[2.8, 3.2, 32]} />
          <meshBasicMaterial color="#ffffff" transparent opacity={0.1} side={THREE.DoubleSide} />
        </mesh>
        
        <mesh rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[3.8, 4.2, 32]} />
          <meshBasicMaterial color="#ffffff" transparent opacity={0.1} side={THREE.DoubleSide} />
        </mesh>
      </Canvas>
      
      {/* Overlay Info */}
      <div className="absolute top-4 left-4 bg-cosmic-dark/80 backdrop-blur-sm rounded-lg p-3 border border-stellar-silver/20">
        <h3 className="text-sm font-semibold text-stellar-gold mb-1">
          🌍 3D Visualization Test
        </h3>
        <p className="text-xs text-stellar-silver/80">
          Drag to rotate • Scroll to zoom
        </p>
      </div>
    </div>
  );
};

export default Simple3DTest;
