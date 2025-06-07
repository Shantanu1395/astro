// Main Visualization Area - 3D Interactive Charts

import React, { Suspense, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Environment } from '@react-three/drei';
import { motion } from 'framer-motion';
import { 
  Eye, 
  RotateCcw, 
  ZoomIn, 
  ZoomOut, 
  Play, 
  Pause,
  Settings,
  Maximize2
} from 'lucide-react';
import { useJourneyStore } from '@/stores/journeyStore';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { cn } from '@/utils/cn';

// Lazy load 3D components for better performance
const VedicChart3D = React.lazy(() => import('./VedicChart3D'));
const TraditionalChart2D = React.lazy(() => import('./TraditionalChart2D'));

const VisualizationArea: React.FC = () => {
  const { 
    visualizationMode, 
    setVisualizationMode,
    animationsEnabled,
    toggleAnimation,
    chartData,
    currentModule,
    highlightedElements
  } = useJourneyStore();

  const [cameraPosition, setCameraPosition] = useState<[number, number, number]>([0, 200, 500]);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  const viewModes = [
    { id: '3d', name: '3D Celestial', icon: Eye, description: 'Interactive 3D cosmic view' },
    { id: '2d', name: 'Traditional', icon: RotateCcw, description: 'Classic Vedic charts' },
    { id: 'hybrid', name: 'Hybrid', icon: Settings, description: 'Combined perspective' },
  ];

  const handleResetCamera = () => {
    setCameraPosition([0, 200, 500]);
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  return (
    <div className="relative w-full h-full bg-cosmic-dark overflow-hidden">
      {/* Cosmic Background */}
      <div className="absolute inset-0 bg-gradient-radial from-cosmic-medium/10 via-cosmic-dark to-cosmic-dark" />
      
      {/* Floating Stars */}
      <div className="absolute inset-0 pointer-events-none">
        {Array.from({ length: 50 }).map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-0.5 h-0.5 bg-stellar-silver rounded-full opacity-40"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              opacity: [0.2, 0.8, 0.2],
              scale: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 3 + Math.random() * 4,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>

      {/* View Mode Controls */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="absolute top-4 left-4 z-20 flex gap-2"
      >
        {viewModes.map((mode) => (
          <motion.button
            key={mode.id}
            onClick={() => setVisualizationMode(mode.id as any)}
            className={cn(
              'px-4 py-2 rounded-lg border transition-all duration-200 flex items-center gap-2',
              visualizationMode === mode.id
                ? 'bg-stellar-blue/20 border-stellar-blue/40 text-stellar-blue glow-effect'
                : 'bg-cosmic-deep/60 border-stellar-silver/20 text-stellar-silver hover:bg-cosmic-medium/50'
            )}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            title={mode.description}
          >
            <mode.icon className="w-4 h-4" />
            <span className="text-sm font-medium">{mode.name}</span>
          </motion.button>
        ))}
      </motion.div>

      {/* Camera Controls */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="absolute top-4 right-4 z-20 flex gap-2"
      >
        <button
          onClick={handleResetCamera}
          className="p-2 bg-cosmic-deep/60 backdrop-blur-sm border border-stellar-silver/20 rounded-lg text-stellar-silver hover:bg-cosmic-medium/50 transition-all duration-200"
          title="Reset Camera"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
        
        <button
          onClick={toggleAnimation}
          className={cn(
            'p-2 backdrop-blur-sm border rounded-lg transition-all duration-200',
            animationsEnabled
              ? 'bg-stellar-blue/20 border-stellar-blue/40 text-stellar-blue'
              : 'bg-cosmic-deep/60 border-stellar-silver/20 text-stellar-silver hover:bg-cosmic-medium/50'
          )}
          title={animationsEnabled ? 'Pause Animations' : 'Play Animations'}
        >
          {animationsEnabled ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
        </button>

        <button
          onClick={toggleFullscreen}
          className="p-2 bg-cosmic-deep/60 backdrop-blur-sm border border-stellar-silver/20 rounded-lg text-stellar-silver hover:bg-cosmic-medium/50 transition-all duration-200"
          title="Toggle Fullscreen"
        >
          <Maximize2 className="w-4 h-4" />
        </button>
      </motion.div>

      {/* Module Context Info */}
      {currentModule && (
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="absolute bottom-4 left-4 z-20 bg-cosmic-deep/80 backdrop-blur-sm border border-stellar-silver/20 rounded-lg p-4 max-w-sm"
        >
          <h3 className="font-semibold text-stellar-silver mb-1">
            {currentModule.title}
          </h3>
          <p className="text-sm text-stellar-silver/80 mb-2">
            {currentModule.subtitle}
          </p>
          <div className="flex items-center gap-2">
            <span className={cn(
              'text-xs px-2 py-1 rounded-full',
              currentModule.level === 'beginner' 
                ? 'bg-green-500/20 text-green-400'
                : currentModule.level === 'intermediate'
                ? 'bg-yellow-500/20 text-yellow-400'
                : currentModule.level === 'advanced'
                ? 'bg-orange-500/20 text-orange-400'
                : 'bg-red-500/20 text-red-400'
            )}>
              {currentModule.level}
            </span>
            <span className="text-xs text-stellar-silver/60">
              {currentModule.duration} minutes
            </span>
          </div>
        </motion.div>
      )}

      {/* Main Visualization Canvas */}
      <div className="w-full h-full">
        {visualizationMode === '3d' && (
          <Canvas
            camera={{ position: cameraPosition, fov: 75 }}
            gl={{ antialias: true, alpha: true }}
            onCreated={({ gl }) => {
              gl.setClearColor('#0a0a0f', 0);
            }}
          >
            {/* Lighting */}
            <ambientLight intensity={0.4} />
            <directionalLight position={[10, 10, 5]} intensity={0.8} />
            <pointLight position={[0, 0, 0]} intensity={0.5} />

            {/* Environment */}
            <Environment preset="night" />

            {/* Camera Controls */}
            <OrbitControls
              enablePan={true}
              enableZoom={true}
              enableRotate={true}
              minDistance={100}
              maxDistance={1000}
              target={[0, 0, 0]}
            />

            {/* 3D Chart */}
            <Suspense fallback={null}>
              <VedicChart3D 
                chartData={chartData}
                highlightedElements={highlightedElements}
                animationsEnabled={animationsEnabled}
              />
            </Suspense>
          </Canvas>
        )}

        {visualizationMode === '2d' && (
          <div className="w-full h-full flex items-center justify-center">
            <Suspense fallback={<LoadingSpinner size="large" text="Loading traditional charts..." />}>
              <TraditionalChart2D 
                chartData={chartData}
                highlightedElements={highlightedElements}
              />
            </Suspense>
          </div>
        )}

        {visualizationMode === 'hybrid' && (
          <div className="w-full h-full grid grid-cols-2 gap-4 p-4">
            {/* 3D View */}
            <div className="relative bg-cosmic-deep/30 rounded-lg overflow-hidden">
              <Canvas
                camera={{ position: [0, 100, 300], fov: 75 }}
                gl={{ antialias: true, alpha: true }}
              >
                <ambientLight intensity={0.4} />
                <directionalLight position={[10, 10, 5]} intensity={0.8} />
                <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
                <Suspense fallback={null}>
                  <VedicChart3D 
                    chartData={chartData}
                    highlightedElements={highlightedElements}
                    animationsEnabled={animationsEnabled}
                  />
                </Suspense>
              </Canvas>
            </div>

            {/* 2D View */}
            <div className="relative bg-cosmic-deep/30 rounded-lg overflow-hidden">
              <Suspense fallback={<LoadingSpinner />}>
                <TraditionalChart2D 
                  chartData={chartData}
                  highlightedElements={highlightedElements}
                />
              </Suspense>
            </div>
          </div>
        )}
      </div>

      {/* Loading Overlay */}
      {!chartData && (
        <div className="absolute inset-0 bg-cosmic-dark/80 backdrop-blur-sm flex items-center justify-center z-30">
          <LoadingSpinner size="large" text="Loading cosmic data..." />
        </div>
      )}
    </div>
  );
};

export default VisualizationArea;
