// System Performance Monitor Component
import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Activity, Cpu, HardDrive, Wifi, Zap, Monitor } from 'lucide-react';

interface SystemMetrics {
  success: boolean;
  timestamp: string;
  system: {
    cpu_percent: number;
    memory: {
      total: number;
      available: number;
      percent: number;
      used: number;
      free: number;
    };
    disk: {
      total: number;
      used: number;
      free: number;
      percent: number;
    };
    network: {
      bytes_sent: number;
      bytes_recv: number;
      packets_sent: number;
      packets_recv: number;
    } | { error: string };
  };
  process: {
    pid: number;
    cpu_percent: number;
    memory: {
      rss: number;
      vms: number;
      percent: number;
    };
    threads: number;
    status: string;
    create_time: number;
    name: string;
  };
}

interface BrowserMetrics {
  fps: number;
  memory: {
    usedJSHeapSize: number;
    totalJSHeapSize: number;
    jsHeapSizeLimit: number;
  };
  timing: {
    loadTime: number;
    domContentLoaded: number;
  };
}

interface SystemMonitorProps {
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  updateInterval?: number;
  compact?: boolean;
}

const SystemMonitor: React.FC<SystemMonitorProps> = ({
  position = 'top-right',
  updateInterval = 2000,
  compact = false
}) => {
  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics | null>(null);
  const [browserMetrics, setBrowserMetrics] = useState<BrowserMetrics | null>(null);
  const [isExpanded, setIsExpanded] = useState(!compact);
  const [error, setError] = useState<string | null>(null);
  const frameCountRef = useRef(0);
  const lastTimeRef = useRef(performance.now());
  const fpsRef = useRef(0);

  // Position classes
  const positionClasses = {
    'top-left': 'top-4 left-4',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-right': 'bottom-4 right-4'
  };

  // FPS calculation
  useEffect(() => {
    const calculateFPS = () => {
      frameCountRef.current++;
      const now = performance.now();
      const delta = now - lastTimeRef.current;

      if (delta >= 1000) {
        fpsRef.current = Math.round((frameCountRef.current * 1000) / delta);
        frameCountRef.current = 0;
        lastTimeRef.current = now;
      }

      requestAnimationFrame(calculateFPS);
    };

    calculateFPS();
  }, []);

  // Browser metrics collection
  useEffect(() => {
    const updateBrowserMetrics = () => {
      const memory = (performance as any).memory;
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;

      setBrowserMetrics({
        fps: fpsRef.current,
        memory: memory ? {
          usedJSHeapSize: memory.usedJSHeapSize,
          totalJSHeapSize: memory.totalJSHeapSize,
          jsHeapSizeLimit: memory.jsHeapSizeLimit
        } : { usedJSHeapSize: 0, totalJSHeapSize: 0, jsHeapSizeLimit: 0 },
        timing: {
          loadTime: navigation ? navigation.loadEventEnd - navigation.fetchStart : 0,
          domContentLoaded: navigation ? navigation.domContentLoadedEventEnd - navigation.fetchStart : 0
        }
      });
    };

    updateBrowserMetrics();
    const interval = setInterval(updateBrowserMetrics, updateInterval);
    return () => clearInterval(interval);
  }, [updateInterval]);

  // System metrics fetching
  useEffect(() => {
    const fetchSystemMetrics = async () => {
      try {
        const response = await fetch('/api/system-metrics');
        const data = await response.json();
        
        if (data.success) {
          setSystemMetrics(data);
          setError(null);
        } else {
          setError(data.error || 'Failed to fetch system metrics');
        }
      } catch (err) {
        setError('Network error fetching system metrics');
      }
    };

    fetchSystemMetrics();
    const interval = setInterval(fetchSystemMetrics, updateInterval);
    return () => clearInterval(interval);
  }, [updateInterval]);

  // Format bytes
  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // Get status color
  const getStatusColor = (percent: number): string => {
    if (percent < 50) return 'text-green-400';
    if (percent < 80) return 'text-yellow-400';
    return 'text-red-400';
  };

  if (error && !systemMetrics) {
    return (
      <div className={`fixed ${positionClasses[position]} z-50`}>
        <div className="bg-red-900/90 backdrop-blur-sm rounded-lg p-3 text-xs text-red-200">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4" />
            <span>Monitor Error</span>
          </div>
          <div className="mt-1 text-red-300">{error}</div>
        </div>
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
      <div className="bg-cosmic-deep/95 backdrop-blur-sm rounded-lg border border-stellar-silver/20 text-xs">
        {/* Header */}
        <div 
          className="flex items-center justify-between p-3 cursor-pointer"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-stellar-gold" />
            <span className="text-stellar-gold font-semibold">System Monitor</span>
          </div>
          <motion.div
            animate={{ rotate: isExpanded ? 180 : 0 }}
            transition={{ duration: 0.2 }}
            className="text-stellar-silver/60"
          >
            ▼
          </motion.div>
        </div>

        {/* Expanded Content */}
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="border-t border-stellar-silver/20"
          >
            {/* Browser Metrics */}
            {browserMetrics && (
              <div className="p-3 border-b border-stellar-silver/10">
                <div className="flex items-center gap-2 mb-2">
                  <Monitor className="w-3 h-3 text-blue-400" />
                  <span className="text-blue-400 font-medium">Browser</span>
                </div>
                <div className="space-y-1 text-stellar-silver/80">
                  <div className="flex justify-between">
                    <span>FPS:</span>
                    <span className={getStatusColor(browserMetrics.fps < 30 ? 80 : 20)}>
                      {browserMetrics.fps}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>JS Heap:</span>
                    <span className={getStatusColor((browserMetrics.memory.usedJSHeapSize / browserMetrics.memory.jsHeapSizeLimit) * 100)}>
                      {formatBytes(browserMetrics.memory.usedJSHeapSize)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Load Time:</span>
                    <span className="text-stellar-silver">
                      {(browserMetrics.timing.loadTime / 1000).toFixed(2)}s
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* System Metrics */}
            {systemMetrics && (
              <>
                {/* CPU & Memory */}
                <div className="p-3 border-b border-stellar-silver/10">
                  <div className="flex items-center gap-2 mb-2">
                    <Cpu className="w-3 h-3 text-orange-400" />
                    <span className="text-orange-400 font-medium">System</span>
                  </div>
                  <div className="space-y-1 text-stellar-silver/80">
                    <div className="flex justify-between">
                      <span>CPU:</span>
                      <span className={getStatusColor(systemMetrics.system.cpu_percent)}>
                        {systemMetrics.system.cpu_percent.toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Memory:</span>
                      <span className={getStatusColor(systemMetrics.system.memory.percent)}>
                        {systemMetrics.system.memory.percent.toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Used:</span>
                      <span className="text-stellar-silver">
                        {formatBytes(systemMetrics.system.memory.used)}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Process Metrics */}
                <div className="p-3 border-b border-stellar-silver/10">
                  <div className="flex items-center gap-2 mb-2">
                    <Zap className="w-3 h-3 text-purple-400" />
                    <span className="text-purple-400 font-medium">Process</span>
                  </div>
                  <div className="space-y-1 text-stellar-silver/80">
                    <div className="flex justify-between">
                      <span>PID:</span>
                      <span className="text-stellar-silver">{systemMetrics.process.pid}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>CPU:</span>
                      <span className={getStatusColor(systemMetrics.process.cpu_percent)}>
                        {systemMetrics.process.cpu_percent.toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Memory:</span>
                      <span className={getStatusColor(systemMetrics.process.memory.percent)}>
                        {formatBytes(systemMetrics.process.memory.rss)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Threads:</span>
                      <span className="text-stellar-silver">{systemMetrics.process.threads}</span>
                    </div>
                  </div>
                </div>

                {/* Disk & Network */}
                <div className="p-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="flex items-center gap-1 mb-1">
                        <HardDrive className="w-3 h-3 text-green-400" />
                        <span className="text-green-400 font-medium text-xs">Disk</span>
                      </div>
                      <div className="text-stellar-silver/80 text-xs">
                        <div className={getStatusColor(systemMetrics.system.disk.percent)}>
                          {systemMetrics.system.disk.percent.toFixed(1)}%
                        </div>
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center gap-1 mb-1">
                        <Wifi className="w-3 h-3 text-cyan-400" />
                        <span className="text-cyan-400 font-medium text-xs">Network</span>
                      </div>
                      <div className="text-stellar-silver/80 text-xs">
                        {'error' in systemMetrics.system.network ? (
                          <span className="text-red-400">N/A</span>
                        ) : (
                          <span className="text-stellar-silver">Active</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default SystemMonitor;
