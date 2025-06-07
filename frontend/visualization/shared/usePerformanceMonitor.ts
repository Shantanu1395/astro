// Performance Monitoring Hook
import { useState, useEffect, useRef, useCallback } from 'react';

interface PerformanceMetrics {
  fps: number;
  frameTime: number;
  memory: {
    used: number;
    total: number;
    limit: number;
    percentage: number;
  };
  gpu: {
    vendor: string;
    renderer: string;
    version: string;
  };
  system: {
    cpu: number;
    memory: number;
    disk: number;
    network: boolean;
  };
  process: {
    pid: number;
    cpu: number;
    memory: number;
    threads: number;
  };
  webgl: {
    drawCalls: number;
    triangles: number;
    geometries: number;
    textures: number;
  };
}

interface UsePerformanceMonitorOptions {
  updateInterval?: number;
  trackGPU?: boolean;
  trackSystem?: boolean;
  trackWebGL?: boolean;
}

export const usePerformanceMonitor = (options: UsePerformanceMonitorOptions = {}) => {
  const {
    updateInterval = 1000,
    trackGPU = true,
    trackSystem = true,
    trackWebGL = true
  } = options;

  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  const [isSupported, setIsSupported] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // FPS tracking
  const frameCountRef = useRef(0);
  const lastTimeRef = useRef(performance.now());
  const frameTimesRef = useRef<number[]>([]);

  // WebGL tracking
  const webglInfoRef = useRef<any>(null);

  // Initialize WebGL info
  useEffect(() => {
    if (!trackWebGL) return;

    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      
      if (gl) {
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        webglInfoRef.current = {
          vendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : 'Unknown',
          renderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : 'Unknown',
          version: gl.getParameter(gl.VERSION)
        };
      }
    } catch (err) {
      console.warn('WebGL info not available:', err);
    }
  }, [trackWebGL]);

  // FPS calculation
  const updateFPS = useCallback(() => {
    frameCountRef.current++;
    const now = performance.now();
    const frameTime = now - lastTimeRef.current;
    
    frameTimesRef.current.push(frameTime);
    if (frameTimesRef.current.length > 60) {
      frameTimesRef.current.shift();
    }

    lastTimeRef.current = now;
    requestAnimationFrame(updateFPS);
  }, []);

  useEffect(() => {
    updateFPS();
  }, [updateFPS]);

  // System metrics fetching
  const fetchSystemMetrics = useCallback(async () => {
    if (!trackSystem) return null;

    try {
      const response = await fetch('/api/system-metrics');
      const data = await response.json();
      
      if (data.success) {
        return {
          cpu: data.system.cpu_percent,
          memory: data.system.memory.percent,
          disk: data.system.disk.percent,
          network: !('error' in data.system.network),
          process: {
            pid: data.process.pid,
            cpu: data.process.cpu_percent,
            memory: data.process.memory.percent,
            threads: data.process.threads
          }
        };
      }
    } catch (err) {
      console.warn('System metrics not available:', err);
    }
    
    return null;
  }, [trackSystem]);

  // Memory info
  const getMemoryInfo = useCallback(() => {
    const memory = (performance as any).memory;
    if (!memory) return null;

    return {
      used: memory.usedJSHeapSize,
      total: memory.totalJSHeapSize,
      limit: memory.jsHeapSizeLimit,
      percentage: (memory.usedJSHeapSize / memory.jsHeapSizeLimit) * 100
    };
  }, []);

  // WebGL stats (placeholder - would need Three.js renderer reference)
  const getWebGLStats = useCallback(() => {
    if (!trackWebGL) return null;

    // This would typically come from Three.js renderer.info
    // For now, return placeholder data
    return {
      drawCalls: 0,
      triangles: 0,
      geometries: 0,
      textures: 0
    };
  }, [trackWebGL]);

  // Main metrics update
  useEffect(() => {
    const updateMetrics = async () => {
      try {
        const now = performance.now();
        const timeSinceLastFrame = now - lastTimeRef.current;
        
        // Calculate FPS from frame times
        const avgFrameTime = frameTimesRef.current.length > 0 
          ? frameTimesRef.current.reduce((a, b) => a + b, 0) / frameTimesRef.current.length
          : 16.67; // Default to 60fps
        
        const fps = Math.round(1000 / avgFrameTime);

        // Get memory info
        const memoryInfo = getMemoryInfo();

        // Get system metrics
        const systemInfo = await fetchSystemMetrics();

        // Get WebGL stats
        const webglStats = getWebGLStats();

        const newMetrics: PerformanceMetrics = {
          fps: Math.max(0, Math.min(120, fps)), // Clamp between 0-120
          frameTime: avgFrameTime,
          memory: memoryInfo || {
            used: 0,
            total: 0,
            limit: 0,
            percentage: 0
          },
          gpu: webglInfoRef.current || {
            vendor: 'Unknown',
            renderer: 'Unknown',
            version: 'Unknown'
          },
          system: systemInfo ? {
            cpu: systemInfo.cpu,
            memory: systemInfo.memory,
            disk: systemInfo.disk,
            network: systemInfo.network
          } : {
            cpu: 0,
            memory: 0,
            disk: 0,
            network: false
          },
          process: systemInfo?.process || {
            pid: 0,
            cpu: 0,
            memory: 0,
            threads: 0
          },
          webgl: webglStats || {
            drawCalls: 0,
            triangles: 0,
            geometries: 0,
            textures: 0
          }
        };

        setMetrics(newMetrics);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      }
    };

    updateMetrics();
    const interval = setInterval(updateMetrics, updateInterval);

    return () => clearInterval(interval);
  }, [updateInterval, getMemoryInfo, fetchSystemMetrics, getWebGLStats]);

  // Check support
  useEffect(() => {
    const supported = !!(
      performance &&
      performance.now &&
      requestAnimationFrame
    );
    setIsSupported(supported);
  }, []);

  return {
    metrics,
    isSupported,
    error,
    // Utility functions
    formatBytes: (bytes: number) => {
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    getStatusColor: (percent: number) => {
      if (percent < 50) return 'text-green-400';
      if (percent < 80) return 'text-yellow-400';
      return 'text-red-400';
    }
  };
};
