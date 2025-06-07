// Camera Control UI Component
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Camera, 
  Move3D, 
  RotateCcw, 
  ZoomIn, 
  ZoomOut,
  Target,
  Navigation,
  Eye,
  Settings,
  Keyboard,
  Mouse,
  Info
} from 'lucide-react';
import * as THREE from 'three';

interface CameraControlUIProps {
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  onResetCamera?: () => void;
  onFocusEarth?: () => void;
  onToggleFreeMove?: () => void;
  currentTarget?: THREE.Vector3;
  cameraPosition?: THREE.Vector3;
  isFreeMoveMode?: boolean;
}

const CameraControlUI: React.FC<CameraControlUIProps> = ({
  position = 'bottom-left',
  onResetCamera,
  onFocusEarth,
  onToggleFreeMove,
  currentTarget,
  cameraPosition,
  isFreeMoveMode = false
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [showHelp, setShowHelp] = useState(false);

  // Position classes
  const positionClasses = {
    'top-left': 'top-4 left-4',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-right': 'bottom-4 right-4'
  };

  // Format vector for display
  const formatVector = (vector?: THREE.Vector3): string => {
    if (!vector) return 'N/A';
    return `(${vector.x.toFixed(1)}, ${vector.y.toFixed(1)}, ${vector.z.toFixed(1)})`;
  };

  // Calculate distance from camera to target
  const getDistance = (): string => {
    if (!cameraPosition || !currentTarget) return 'N/A';
    const distance = cameraPosition.distanceTo(currentTarget);
    return distance.toFixed(1);
  };

  return (
    <motion.div
      className={`fixed ${positionClasses[position]} z-40`}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="bg-cosmic-deep/95 backdrop-blur-sm rounded-lg border border-stellar-silver/20 text-xs">
        {/* Header */}
        <div 
          className="flex items-center justify-between p-3 cursor-pointer"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <div className="flex items-center gap-2">
            <Camera className="w-4 h-4 text-stellar-blue" />
            <span className="text-stellar-blue font-semibold">Camera Controls</span>
            {isFreeMoveMode && (
              <div className="px-2 py-1 bg-stellar-gold/20 rounded text-stellar-gold text-xs">
                FREE MOVE
              </div>
            )}
          </div>
          <motion.div
            animate={{ rotate: isExpanded ? 180 : 0 }}
            transition={{ duration: 0.2 }}
            className="text-stellar-silver/60"
          >
            ▼
          </motion.div>
        </div>

        {/* Quick Controls (Always Visible) */}
        <div className="flex items-center gap-1 px-3 pb-3">
          <button
            onClick={onResetCamera}
            className="p-2 bg-cosmic-medium/50 hover:bg-cosmic-medium/70 rounded border border-stellar-silver/20 text-stellar-silver hover:text-stellar-gold transition-colors"
            title="Reset Camera (R)"
          >
            <RotateCcw className="w-3 h-3" />
          </button>
          
          <button
            onClick={onFocusEarth}
            className="p-2 bg-cosmic-medium/50 hover:bg-cosmic-medium/70 rounded border border-stellar-silver/20 text-stellar-silver hover:text-stellar-gold transition-colors"
            title="Focus on Earth (E)"
          >
            <Target className="w-3 h-3" />
          </button>
          
          <button
            onClick={onToggleFreeMove}
            className={`p-2 rounded border border-stellar-silver/20 transition-colors ${
              isFreeMoveMode 
                ? 'bg-stellar-gold/20 text-stellar-gold border-stellar-gold/40' 
                : 'bg-cosmic-medium/50 hover:bg-cosmic-medium/70 text-stellar-silver hover:text-stellar-gold'
            }`}
            title="Toggle Free Movement (F)"
          >
            <Move3D className="w-3 h-3" />
          </button>
          
          <button
            onClick={() => setShowHelp(!showHelp)}
            className="p-2 bg-cosmic-medium/50 hover:bg-cosmic-medium/70 rounded border border-stellar-silver/20 text-stellar-silver hover:text-stellar-gold transition-colors"
            title="Show Help"
          >
            <Info className="w-3 h-3" />
          </button>
        </div>

        {/* Expanded Content */}
        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="border-t border-stellar-silver/20 overflow-hidden"
            >
              {/* Camera Info */}
              <div className="p-3 border-b border-stellar-silver/10">
                <div className="text-stellar-blue font-medium mb-2">Camera Status</div>
                <div className="space-y-1 text-stellar-silver/80">
                  <div className="flex justify-between">
                    <span>Position:</span>
                    <span className="text-stellar-silver font-mono text-xs">
                      {formatVector(cameraPosition)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Target:</span>
                    <span className="text-stellar-silver font-mono text-xs">
                      {formatVector(currentTarget)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Distance:</span>
                    <span className="text-stellar-silver">{getDistance()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Mode:</span>
                    <span className={isFreeMoveMode ? 'text-stellar-gold' : 'text-stellar-silver'}>
                      {isFreeMoveMode ? 'Free Movement' : 'Orbit Mode'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Movement Controls */}
              <div className="p-3 border-b border-stellar-silver/10">
                <div className="text-orange-400 font-medium mb-2">Movement</div>
                <div className="grid grid-cols-2 gap-2">
                  <button className="p-2 bg-cosmic-medium/30 rounded border border-stellar-silver/10 text-stellar-silver hover:bg-cosmic-medium/50 transition-colors text-xs">
                    <ZoomIn className="w-3 h-3 mx-auto mb-1" />
                    Zoom In
                  </button>
                  <button className="p-2 bg-cosmic-medium/30 rounded border border-stellar-silver/10 text-stellar-silver hover:bg-cosmic-medium/50 transition-colors text-xs">
                    <ZoomOut className="w-3 h-3 mx-auto mb-1" />
                    Zoom Out
                  </button>
                  <button className="p-2 bg-cosmic-medium/30 rounded border border-stellar-silver/10 text-stellar-silver hover:bg-cosmic-medium/50 transition-colors text-xs">
                    <Navigation className="w-3 h-3 mx-auto mb-1" />
                    Pan
                  </button>
                  <button className="p-2 bg-cosmic-medium/30 rounded border border-stellar-silver/10 text-stellar-silver hover:bg-cosmic-medium/50 transition-colors text-xs">
                    <RotateCcw className="w-3 h-3 mx-auto mb-1" />
                    Rotate
                  </button>
                </div>
              </div>

              {/* Quick Focus Targets */}
              <div className="p-3">
                <div className="text-purple-400 font-medium mb-2">Quick Focus</div>
                <div className="grid grid-cols-2 gap-1">
                  <button
                    onClick={onFocusEarth}
                    className="p-1 bg-cosmic-medium/30 rounded border border-stellar-silver/10 text-stellar-silver hover:bg-cosmic-medium/50 transition-colors text-xs"
                    title="Focus on Earth (E key)"
                  >
                    🌍 Earth
                  </button>
                  <button
                    onClick={() => {/* Focus on Sun */}}
                    className="p-1 bg-cosmic-medium/30 rounded border border-stellar-silver/10 text-stellar-silver hover:bg-cosmic-medium/50 transition-colors text-xs"
                    title="Focus on Sun (1 key)"
                  >
                    ☀️ Sun
                  </button>
                  <button
                    onClick={() => {/* Focus on Moon */}}
                    className="p-1 bg-cosmic-medium/30 rounded border border-stellar-silver/10 text-stellar-silver hover:bg-cosmic-medium/50 transition-colors text-xs"
                    title="Focus on Moon (2 key)"
                  >
                    🌙 Moon
                  </button>
                  <button
                    onClick={() => {/* Focus on Jupiter */}}
                    className="p-1 bg-cosmic-medium/30 rounded border border-stellar-silver/10 text-stellar-silver hover:bg-cosmic-medium/50 transition-colors text-xs"
                    title="Focus on Jupiter (3 key)"
                  >
                    🪐 Jupiter
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Help Modal */}
        <AnimatePresence>
          {showHelp && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center"
              onClick={() => setShowHelp(false)}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-cosmic-deep/95 backdrop-blur-sm rounded-lg border border-stellar-silver/20 p-6 max-w-md mx-4"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex items-center gap-2 mb-4">
                  <Info className="w-5 h-5 text-stellar-blue" />
                  <h3 className="text-stellar-blue font-semibold">Camera Controls Help</h3>
                </div>

                <div className="space-y-4 text-sm">
                  {/* Mouse Controls */}
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Mouse className="w-4 h-4 text-orange-400" />
                      <span className="text-orange-400 font-medium">Mouse Controls</span>
                    </div>
                    <div className="space-y-1 text-stellar-silver/80 text-xs">
                      <div>• <strong>Left Click + Drag:</strong> Rotate around target</div>
                      <div>• <strong>Right Click + Drag:</strong> Pan camera</div>
                      <div>• <strong>Scroll Wheel:</strong> Zoom in/out</div>
                      <div>• <strong>Double Click:</strong> Focus on object</div>
                    </div>
                  </div>

                  {/* Keyboard Controls */}
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Keyboard className="w-4 h-4 text-purple-400" />
                      <span className="text-purple-400 font-medium">Keyboard Shortcuts</span>
                    </div>
                    <div className="space-y-1 text-stellar-silver/80 text-xs">
                      <div>• <strong>F:</strong> Toggle free movement mode</div>
                      <div>• <strong>R:</strong> Reset camera to default</div>
                      <div>• <strong>E:</strong> Focus on Earth</div>
                      <div>• <strong>WASD:</strong> Move in free mode</div>
                      <div>• <strong>Q/E:</strong> Move up/down in free mode</div>
                    </div>
                  </div>

                  {/* Movement Modes */}
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Move3D className="w-4 h-4 text-green-400" />
                      <span className="text-green-400 font-medium">Movement Modes</span>
                    </div>
                    <div className="space-y-1 text-stellar-silver/80 text-xs">
                      <div>• <strong>Orbit Mode:</strong> Camera orbits around target</div>
                      <div>• <strong>Free Mode:</strong> Unrestricted camera movement</div>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => setShowHelp(false)}
                  className="mt-4 w-full p-2 bg-stellar-blue/20 hover:bg-stellar-blue/30 rounded border border-stellar-blue/40 text-stellar-blue transition-colors"
                >
                  Got it!
                </button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export default CameraControlUI;
