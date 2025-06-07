// Visualization Component Types

export interface Planet {
  name: string;
  position: [number, number, number];
  color: string;
  size: number;
}

export interface VedicData {
  planets: Planet[];
  rashis: string[];
  nakshatras: string[];
}

export interface VisualizationProps {
  data?: VedicData;
  interactive?: boolean;
  showLabels?: boolean;
  animationSpeed?: number;
}

export type ViewMode = '3d' | '2d' | 'hybrid' | 'test';

export interface CameraSettings {
  position: [number, number, number];
  fov: number;
  minDistance: number;
  maxDistance: number;
}
