// Minimal Three.js Test Component

import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';

function RotatingCube() {
  const meshRef = useRef<any>(null);
  
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta;
      meshRef.current.rotation.y += delta * 0.5;
    }
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshBasicMaterial color="orange" />
    </mesh>
  );
}

export default function SimpleThreeTest() {
  return (
    <div className="w-full h-full bg-gray-900 relative">
      <div className="absolute top-4 left-4 z-10 bg-black/80 text-white p-3 rounded text-sm">
        <div className="font-bold text-green-400 mb-2">🧪 Minimal Three.js Test</div>
        <div className="text-xs space-y-1">
          <div>• Should show rotating orange cube</div>
          <div>• Check console for success message</div>
          <div>• If black screen = Three.js issue</div>
        </div>
      </div>

      <div className="absolute bottom-4 left-4 z-10 bg-black/80 text-white p-2 rounded text-xs">
        <div id="test-status">⏳ Loading Three.js...</div>
      </div>

      <Canvas
        camera={{ position: [0, 0, 5] }}
        style={{
          width: '100%',
          height: '100%',
          background: 'linear-gradient(45deg, #1a1a2e, #16213e)'
        }}
        onCreated={(state) => {
          console.log('✅ MINIMAL CANVAS CREATED SUCCESSFULLY!');
          console.log('📊 Test Canvas Size:', state.size);
          console.log('🎯 Test Camera:', state.camera.position);

          // Update status indicator
          const statusEl = document.getElementById('test-status');
          if (statusEl) {
            statusEl.textContent = '✅ Three.js Working!';
            statusEl.className = 'text-green-400';
          }

          // Try to log to terminal
          fetch('http://localhost:8000/api/debug-log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              message: '✅ MINIMAL THREE.JS TEST SUCCESSFUL - CUBE SHOULD BE VISIBLE!',
              level: 'success',
              component: 'three-test',
              data: {
                testType: 'minimal-cube',
                canvasSize: state.size,
                cameraPosition: state.camera.position,
                success: true
              },
              timestamp: new Date().toISOString()
            })
          }).catch(() => {});
        }}
        onError={(error) => {
          console.error('❌ MINIMAL CANVAS FAILED:', error);

          // Update status indicator
          const statusEl = document.getElementById('test-status');
          if (statusEl) {
            statusEl.textContent = '❌ Three.js Failed!';
            statusEl.className = 'text-red-400';
          }
        }}
      >
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <RotatingCube />
      </Canvas>
    </div>
  );
}
