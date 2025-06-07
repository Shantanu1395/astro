// Enhanced Performance Monitor Component
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  Cpu, 
  HardDrive, 
  Wifi, 
  Zap, 
  Monitor, 
  Eye,
  EyeOff,
  Settings,
  BarChart3
} from 'lucide-react';
import { usePerformanceMonitor } from './usePerformanceMonitor';

interface EnhancedMonitorProps {
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  updateInterval?: number;
  trackGPU?: boolean;
  trackSystem?: boolean;
  trackWebGL?: boolean;
  defaultExpanded?: boolean;
}

const EnhancedMonitor: React.FC<EnhancedMonitorProps> = ({
  position = 'top-right',
  updateInterval = 1000,
  trackGPU = true,
  trackSystem = true,
  trackWebGL = true,
  defaultExpanded = false
}) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const [activeTab, setActiveTab] = useState<'overview' | 'system' | 'browser' | 'webgl'>('overview');
  const [isVisible, setIsVisible] = useState(true);

  const { metrics, isSupported, error, formatBytes, getStatusColor } = usePerformanceMonitor({
    updateInterval,
    trackGPU,
    trackSystem,
    trackWebGL
  });

  // Position classes
  const positionClasses = {
    'top-left': 'top-4 left-4',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-right': 'bottom-4 right-4'
  };

  if (!isSupported) {
    return (
      <div className={`fixed ${positionClasses[position]} z-50`}>
        <div className="bg-red-900/90 backdrop-blur-sm rounded-lg p-3 text-xs text-red-200">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4" />
            <span>Performance monitoring not supported</span>
          </div>
        </div>
      </div>
    );
  }

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
      className={`fixed ${positionClasses[position]} z-50`}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="bg-cosmic-deep/95 backdrop-blur-sm rounded-lg border border-stellar-silver/20 text-xs min-w-[280px]">
        {/* Header */}
        <div className="flex items-center justify-between p-3 border-b border-stellar-silver/20">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-stellar-gold" />
            <span className="text-stellar-gold font-semibold">Performance Monitor</span>
            {metrics && (
              <div className="flex items-center gap-1">
                <div className={`w-2 h-2 rounded-full ${
                  metrics.fps > 50 ? 'bg-green-400' : 
                  metrics.fps > 30 ? 'bg-yellow-400' : 'bg-red-400'
                }`} />
                <span className="text-stellar-silver/80">{metrics.fps} FPS</span>
              </div>
            )}
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-stellar-silver/60 hover:text-stellar-gold transition-colors"
            >
              <Settings className="w-3 h-3" />
            </button>
            <button
              onClick={() => setIsVisible(false)}
              className="text-stellar-silver/60 hover:text-stellar-gold transition-colors"
            >
              <EyeOff className="w-3 h-3" />
            </button>
          </div>
        </div>

        {/* Quick Stats (Always Visible) */}
        {metrics && (
          <div className="p-3 border-b border-stellar-silver/10">
            <div className="grid grid-cols-3 gap-3 text-center">
              <div>
                <div className={`text-sm font-medium ${getStatusColor(metrics.fps < 30 ? 80 : 20)}`}>
                  {metrics.fps}
                </div>
                <div className="text-stellar-silver/60 text-xs">FPS</div>
              </div>
              <div>
                <div className={`text-sm font-medium ${getStatusColor(metrics.memory.percentage)}`}>
                  {metrics.memory.percentage.toFixed(0)}%
                </div>
                <div className="text-stellar-silver/60 text-xs">Memory</div>
              </div>
              <div>
                <div className={`text-sm font-medium ${getStatusColor(metrics.system.cpu)}`}>
                  {metrics.system.cpu.toFixed(0)}%
                </div>
                <div className="text-stellar-silver/60 text-xs">CPU</div>
              </div>
            </div>
          </div>
        )}

        {/* Expanded Content */}
        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              {/* Tab Navigation */}
              <div className="flex border-b border-stellar-silver/10">
                {[
                  { id: 'overview', label: 'Overview', icon: BarChart3 },
                  { id: 'system', label: 'System', icon: Cpu },
                  { id: 'browser', label: 'Browser', icon: Monitor },
                  { id: 'webgl', label: 'WebGL', icon: Zap }
                ].map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`flex-1 flex items-center justify-center gap-1 p-2 text-xs transition-colors ${
                      activeTab === tab.id
                        ? 'bg-stellar-gold/20 text-stellar-gold'
                        : 'text-stellar-silver/60 hover:text-stellar-silver'
                    }`}
                  >
                    <tab.icon className="w-3 h-3" />
                    <span className="hidden sm:inline">{tab.label}</span>
                  </button>
                ))}
              </div>

              {/* Tab Content */}
              <div className="p-3">
                {error && (
                  <div className="mb-3 p-2 bg-red-900/50 rounded text-red-200 text-xs">
                    {error}
                  </div>
                )}

                {metrics && (
                  <>
                    {activeTab === 'overview' && (
                      <div className="space-y-3">
                        <div>
                          <div className="text-stellar-gold font-medium mb-2">Performance Overview</div>
                          <div className="space-y-1">
                            <div className="flex justify-between">
                              <span>Frame Time:</span>
                              <span className="text-stellar-silver">{metrics.frameTime.toFixed(2)}ms</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Memory Usage:</span>
                              <span className={getStatusColor(metrics.memory.percentage)}>
                                {formatBytes(metrics.memory.used)}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>Process CPU:</span>
                              <span className={getStatusColor(metrics.process.cpu)}>
                                {metrics.process.cpu.toFixed(1)}%
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {activeTab === 'system' && (
                      <div className="space-y-3">
                        <div>
                          <div className="text-orange-400 font-medium mb-2">System Resources</div>
                          <div className="space-y-1">
                            <div className="flex justify-between">
                              <span>CPU:</span>
                              <span className={getStatusColor(metrics.system.cpu)}>
                                {metrics.system.cpu.toFixed(1)}%
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>Memory:</span>
                              <span className={getStatusColor(metrics.system.memory)}>
                                {metrics.system.memory.toFixed(1)}%
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>Disk:</span>
                              <span className={getStatusColor(metrics.system.disk)}>
                                {metrics.system.disk.toFixed(1)}%
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>Network:</span>
                              <span className={metrics.system.network ? 'text-green-400' : 'text-red-400'}>
                                {metrics.system.network ? 'Active' : 'Inactive'}
                              </span>
                            </div>
                          </div>
                        </div>
                        <div>
                          <div className="text-purple-400 font-medium mb-2">Process Info</div>
                          <div className="space-y-1">
                            <div className="flex justify-between">
                              <span>PID:</span>
                              <span className="text-stellar-silver">{metrics.process.pid}</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Threads:</span>
                              <span className="text-stellar-silver">{metrics.process.threads}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {activeTab === 'browser' && (
                      <div className="space-y-3">
                        <div>
                          <div className="text-blue-400 font-medium mb-2">Browser Performance</div>
                          <div className="space-y-1">
                            <div className="flex justify-between">
                              <span>JS Heap Used:</span>
                              <span className="text-stellar-silver">
                                {formatBytes(metrics.memory.used)}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>JS Heap Total:</span>
                              <span className="text-stellar-silver">
                                {formatBytes(metrics.memory.total)}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>JS Heap Limit:</span>
                              <span className="text-stellar-silver">
                                {formatBytes(metrics.memory.limit)}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>Memory Usage:</span>
                              <span className={getStatusColor(metrics.memory.percentage)}>
                                {metrics.memory.percentage.toFixed(1)}%
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {activeTab === 'webgl' && (
                      <div className="space-y-3">
                        <div>
                          <div className="text-cyan-400 font-medium mb-2">WebGL Info</div>
                          <div className="space-y-1">
                            <div className="flex justify-between">
                              <span>Vendor:</span>
                              <span className="text-stellar-silver text-xs">
                                {metrics.gpu.vendor.substring(0, 20)}...
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>Renderer:</span>
                              <span className="text-stellar-silver text-xs">
                                {metrics.gpu.renderer.substring(0, 20)}...
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>Draw Calls:</span>
                              <span className="text-stellar-silver">{metrics.webgl.drawCalls}</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Triangles:</span>
                              <span className="text-stellar-silver">{metrics.webgl.triangles}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export default EnhancedMonitor;
