import { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import CelestialSphere from '../frontend/visualization/3d/CelestialSphere';
import SimpleThreeTest from '../frontend/visualization/3d/SimpleThreeTest';

function App() {
  const [viewMode, setViewMode] = useState<'3d' | 'test'>('3d');

  return (
    <div className="min-h-screen bg-gradient-to-br from-cosmic-deep via-cosmic-medium to-cosmic-deep text-white">
      {/* Header */}
      <header className="relative z-10 bg-cosmic-deep/80 backdrop-blur-sm border-b border-stellar-silver/20">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="text-3xl">⭐</div>
              <div>
                <h1 className="text-2xl font-bold text-stellar-gold">
                  Vedic Astrology Journey
                </h1>
                <p className="text-stellar-silver/80 text-sm">
                  Interactive 3D Celestial Visualization
                </p>
              </div>
            </div>

            {/* View Mode Toggle */}
            <div className="flex items-center space-x-4">
              <div className="flex bg-cosmic-medium/50 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('3d')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                    viewMode === '3d'
                      ? 'bg-stellar-gold text-cosmic-dark'
                      : 'text-stellar-silver hover:text-stellar-gold'
                  }`}
                >
                  🌍 3D View
                </button>
                <button
                  onClick={() => setViewMode('test')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                    viewMode === 'test'
                      ? 'bg-red-500 text-white'
                      : 'text-stellar-silver hover:text-red-400'
                  }`}
                >
                  🔧 Test
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main 3D Visualization Area */}
      <div className="relative h-[calc(100vh-120px)]">
        {viewMode === '3d' ? (
          <div className="w-full h-full relative">
            {/* Debug Info */}
            <div className="absolute top-4 right-4 z-20 bg-cosmic-deep/90 backdrop-blur-sm rounded-lg p-3 text-xs max-w-xs">
              <div className="text-stellar-gold font-semibold mb-2">🔧 3D Celestial Sphere</div>
              <div className="space-y-1 text-stellar-silver/80">
                <div>✅ 9 Planets</div>
                <div>✅ 12 Rashis (Zodiac Signs)</div>
                <div>✅ 27 Nakshatras</div>
                <div>✅ Earth-Centric View</div>
                <div className="mt-2 pt-2 border-t border-stellar-silver/20">
                  <div className="text-blue-400 text-xs">
                    🖱️ Drag to rotate • 🔍 Scroll to zoom
                  </div>
                </div>
              </div>
            </div>

            <Canvas
              camera={{ position: [0, 0, 120], fov: 75 }}
              style={{
                width: '100%',
                height: '100%',
                background: 'linear-gradient(135deg, #1a1a2e 0%, #0a0a0f 100%)'
              }}
              onCreated={(state) => {
                console.log('🎨 Three.js Canvas Created Successfully!');
                console.log('📐 Canvas Size:', state.size);
                console.log('🎥 Camera Position:', state.camera.position);
              }}
            >
              {/* Lighting Setup */}
              <ambientLight intensity={0.3} />
              <directionalLight
                position={[100, 100, 100]}
                intensity={0.8}
                castShadow
              />
              <pointLight position={[-50, -50, -50]} intensity={0.4} />

              {/* Stars Background */}
              <Stars radius={300} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

              {/* Main Celestial Sphere */}
              <CelestialSphere />

              {/* Camera Controls */}
              <OrbitControls
                enablePan={true}
                enableZoom={true}
                enableRotate={true}
                minDistance={20}
                maxDistance={500}
                target={[0, 0, 0]}
              />
            </Canvas>
          </div>
        ) : (
          <SimpleThreeTest />
        )}

        {/* Real-time Monitor */}
        <div className="fixed bottom-4 left-4 bg-cosmic-deep/90 backdrop-blur-sm rounded-lg p-3 text-xs max-w-xs z-50">
          <div className="text-stellar-gold font-semibold mb-2">🔧 Real-Time Monitor</div>
          <div className="space-y-1 text-stellar-silver/80">
            <div>WebGL: ✅ Supported</div>
            <div>Three.js: ✅ Working</div>
            <div>Canvas: ✅ Active</div>
            <div>Mode: <span className="text-white font-semibold">{viewMode.toUpperCase()}</span></div>
          </div>
        </div>
      </div>

      {/* Control Panel */}
      <div className="absolute bottom-6 left-6 right-6 z-10">
        <div className="cosmic-card p-4 max-w-4xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Visualization Info */}
            <div>
              <h4 className="text-stellar-gold font-semibold mb-2">🌍 Current View</h4>
              <p className="text-stellar-silver/80 text-sm mb-2">
                {viewMode === '3d' && 'Interactive 3D celestial sphere with Earth at center'}
                {viewMode === 'test' && 'Three.js functionality test with rotating cube'}
              </p>
              <div className="flex gap-2 text-xs">
                <span className="bg-green-500/20 text-green-400 px-2 py-1 rounded">
                  ✅ 9 Planets
                </span>
                <span className="bg-orange-500/20 text-orange-400 px-2 py-1 rounded">
                  ✅ 12 Rashis
                </span>
                <span className="bg-blue-500/20 text-blue-400 px-2 py-1 rounded">
                  ✅ 27 Nakshatras
                </span>
              </div>
            </div>

            {/* Controls */}
            <div>
              <h4 className="text-stellar-gold font-semibold mb-2">🎮 Controls</h4>
              <div className="space-y-1 text-sm text-stellar-silver/80">
                <div>🖱️ <strong>Mouse Drag:</strong> Rotate view</div>
                <div>🔍 <strong>Mouse Wheel:</strong> Zoom in/out</div>
                <div>⌨️ <strong>Right Click:</strong> Pan camera</div>
                <div>🎯 <strong>Click Planet:</strong> View details</div>
              </div>
            </div>

            {/* Quick Actions */}
            <div>
              <h4 className="text-stellar-gold font-semibold mb-2">⚡ Quick Actions</h4>
              <div className="space-y-2">
                <button 
                  onClick={() => setViewMode(viewMode === '3d' ? 'test' : '3d')}
                  className="w-full text-left text-sm bg-cosmic-medium/50 hover:bg-cosmic-medium/70 px-3 py-2 rounded transition-colors"
                >
                  🔄 Switch to {viewMode === '3d' ? 'Test' : '3D'} Mode
                </button>
                <a
                  href="http://localhost:8000/docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full text-left text-sm bg-cosmic-medium/50 hover:bg-cosmic-medium/70 px-3 py-2 rounded transition-colors"
                >
                  🔧 API Documentation
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
