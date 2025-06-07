// Simple Camera Controls Component
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Camera, 
  RotateCcw, 
  Target,
  Navigation,
  Eye,
  EyeOff,
  Info,
  Move3D
} from 'lucide-react';

interface SimpleCameraControlsProps {
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  isFreeMovementMode?: boolean;
}

const SimpleCameraControls: React.FC<SimpleCameraControlsProps> = ({
  position = 'bottom-left',
  isFreeMovementMode = false
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [isVisible, setIsVisible] = useState(true);

  // Position classes
  const positionClasses = {
    'top-left': 'top-4 left-4',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-right': 'bottom-4 right-4'
  };

  if (!isVisible) {
    return (
      <div className={`fixed ${positionClasses[position]} z-50`}>
        <button
          onClick={() => setIsVisible(true)}
          className="bg-cosmic-deep/80 backdrop-blur-sm rounded-lg p-2 text-stellar-silver/60 hover:text-stellar-gold transition-colors"
        >
          <Eye className="w-4 h-4" />
        </button>
      </div>
    );
  }

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
            <span className="text-stellar-blue font-semibold">Enhanced Controls</span>
            {isFreeMovementMode && (
              <div className="px-2 py-1 bg-stellar-gold/20 rounded text-stellar-gold text-xs">
                FREE MODE
              </div>
            )}
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={(e) => {
                e.stopPropagation();
                setShowHelp(!showHelp);
              }}
              className="text-stellar-silver/60 hover:text-stellar-gold transition-colors"
            >
              <Info className="w-3 h-3" />
            </button>
            <button
              onClick={(e) => {
                e.stopPropagation();
                setIsVisible(false);
              }}
              className="text-stellar-silver/60 hover:text-stellar-gold transition-colors"
            >
              <EyeOff className="w-3 h-3" />
            </button>
            <motion.div
              animate={{ rotate: isExpanded ? 180 : 0 }}
              transition={{ duration: 0.2 }}
              className="text-stellar-silver/60"
            >
              ▼
            </motion.div>
          </div>
        </div>

        {/* Quick Controls (Always Visible) */}
        <div className="flex items-center justify-between px-3 pb-3">
          <div className="text-stellar-silver/80 text-xs">
            🖱️ Custom Mouse • 🔍 Zoom • ⌨️ WASD • 🎯 Focal Point
          </div>
          <div className="px-2 py-1 bg-stellar-gold/20 rounded text-stellar-gold text-xs">
            CAMERA POSITION
          </div>
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
              {/* Enhanced Features */}
              <div className="p-3 border-b border-stellar-silver/10">
                <div className="text-stellar-blue font-medium mb-2">Enhanced Features</div>
                <div className="space-y-1 text-stellar-silver/80">
                  <div className="flex items-center gap-2">
                    <Move3D className="w-3 h-3 text-green-400" />
                    <span>Free camera movement</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Target className="w-3 h-3 text-orange-400" />
                    <span>Dynamic targeting</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Navigation className="w-3 h-3 text-purple-400" />
                    <span>Enhanced zoom range</span>
                  </div>
                </div>
              </div>

              {/* Control Summary */}
              <div className="p-3">
                <div className="text-orange-400 font-medium mb-2">Controls</div>
                <div className="space-y-1 text-stellar-silver/80 text-xs">
                  <div>• <strong>Left Drag:</strong> Rotate around target</div>
                  <div>• <strong>Right Drag:</strong> Pan camera freely</div>
                  <div>• <strong>Mouse Wheel:</strong> Zoom in/out</div>
                  <div>• <strong>Double Click:</strong> Focus on object</div>
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
                  <h3 className="text-stellar-blue font-semibold">Enhanced Camera Controls</h3>
                </div>

                <div className="space-y-4 text-sm">
                  {/* Mouse Controls */}
                  <div>
                    <div className="text-orange-400 font-medium mb-2">🖱️ Mouse Controls</div>
                    <div className="space-y-1 text-stellar-silver/80 text-xs">
                      <div>• <strong>Mouse Wheel:</strong> Zoom in/out (3-2000 range)</div>
                      <div>• <strong>Left Drag:</strong> Rotates camera position around focal point</div>
                      <div>• <strong>Right Drag:</strong> Moves camera position and focal point</div>
                      <div>• <strong>Custom Handlers:</strong> Direct camera position changes</div>
                    </div>
                  </div>

                  {/* Keyboard Controls */}
                  <div>
                    <div className="text-purple-400 font-medium mb-2">⌨️ Precise WASD Movement</div>
                    <div className="space-y-1 text-stellar-silver/80 text-xs">
                      <div>• <strong>W:</strong> Forward only (camera direction)</div>
                      <div>• <strong>S:</strong> Backward only (camera direction)</div>
                      <div>• <strong>A:</strong> Left only (strafe left)</div>
                      <div>• <strong>D:</strong> Right only (strafe right)</div>
                      <div>• <strong>Q:</strong> Up only (world up)</div>
                      <div>• <strong>E:</strong> Down only (world down)</div>
                      <div>• <strong>R:</strong> Reset camera</div>
                      <div>• <strong>Home:</strong> Focus on Earth</div>
                    </div>
                  </div>

                  {/* Enhanced Features */}
                  <div>
                    <div className="text-green-400 font-medium mb-2">✨ Enhanced Features</div>
                    <div className="space-y-1 text-stellar-silver/80 text-xs">
                      <div>• <strong>Visible Focal Point:</strong> Yellow wireframe sphere</div>
                      <div>• <strong>Direct Camera Control:</strong> Custom mouse handlers</div>
                      <div>• <strong>Real Camera Movement:</strong> Position actually changes</div>
                      <div>• <strong>Spherical Rotation:</strong> Orbit around focal point</div>
                      <div>• <strong>Screen Space Panning:</strong> Intuitive movement</div>
                      <div>• <strong>Live Coordinates:</strong> Real-time position display</div>
                    </div>
                  </div>

                  {/* Custom Mouse Handlers */}
                  <div>
                    <div className="text-yellow-400 font-medium mb-2">🖱️ Custom Mouse Handlers</div>
                    <div className="space-y-1 text-stellar-silver/80 text-xs">
                      <div>• <strong>Left Drag:</strong> Spherical rotation around focal point</div>
                      <div>• <strong>Right Drag:</strong> Screen-space panning movement</div>
                      <div>• <strong>Mouse Wheel:</strong> Distance zoom (OrbitControls)</div>
                      <div>• <strong>Direct Control:</strong> Bypasses standard controls</div>
                      <div>• <strong>Real Position:</strong> Camera actually moves in 3D</div>
                    </div>
                  </div>

                  {/* Tips */}
                  <div>
                    <div className="text-purple-400 font-medium mb-2">💡 Tips</div>
                    <div className="space-y-1 text-stellar-silver/80 text-xs">
                      <div>• Watch camera coordinates change on mouse drag</div>
                      <div>• Left drag orbits around the yellow focal point</div>
                      <div>• Right drag moves both camera and focal point</div>
                      <div>• Use WASD for precise directional movement</div>
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

export default SimpleCameraControls;
