// WebGL Performance Monitor using stats-gl
import React, { useEffect, useRef } from 'react';
import Stats from 'stats-gl';

interface StatsMonitorProps {
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
  trackGPU?: boolean;
  minimal?: boolean;
  horizontal?: boolean;
}

const StatsMonitor: React.FC<StatsMonitorProps> = ({
  position = 'top-left',
  trackGPU = true,
  minimal = false,
  horizontal = true
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const statsRef = useRef<Stats | null>(null);

  // Position classes
  const positionClasses = {
    'top-left': 'top-4 left-4',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-right': 'bottom-4 right-4'
  };

  useEffect(() => {
    if (!containerRef.current) return;

    // Create stats-gl instance
    const stats = new Stats({
      trackGPU: trackGPU,
      logsPerSecond: 20,
      samplesLog: 100,
      samplesGraph: 10,
      precision: 2,
      horizontal: horizontal,
      minimal: minimal,
      mode: 0 // Start with FPS mode
    });

    // Style the stats container to match our theme
    if (stats.dom) {
      stats.dom.style.cssText = `
        position: relative !important;
        background: rgba(15, 15, 35, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(8px) !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
      `;

      // Append to our container
      containerRef.current.appendChild(stats.dom);
    }

    statsRef.current = stats;

    // Animation loop for stats updates
    const animate = () => {
      if (statsRef.current) {
        statsRef.current.begin();
        
        // Simulate some work (in real app, this would be your render loop)
        // The stats will automatically track the time between begin() and end()
        
        statsRef.current.end();
        statsRef.current.update();
      }
      requestAnimationFrame(animate);
    };

    animate();

    // Cleanup
    return () => {
      if (statsRef.current && containerRef.current && stats.dom) {
        containerRef.current.removeChild(stats.dom);
      }
    };
  }, [trackGPU, minimal, horizontal]);

  return (
    <div 
      ref={containerRef}
      className={`fixed ${positionClasses[position]} z-40`}
      style={{ pointerEvents: 'auto' }}
    />
  );
};

export default StatsMonitor;
