# Vedic Astrology Visualization Components

This folder contains all visualization-related components for the Vedic Astrology Journey application.

## 📁 Folder Structure

```
frontend/visualization/
├── 3d/                     # Three.js 3D Components
│   ├── CelestialSphere.tsx # Main 3D celestial sphere with planets, rashis, nakshatras
│   ├── SimpleThreeTest.tsx # Basic Three.js test component (rotating cube)
│   ├── Simple3DTest.tsx    # Alternative 3D test component
│   └── VedicChart3D.tsx    # 3D Vedic chart visualization
├── 2d/                     # Traditional 2D Components
│   └── TraditionalChart2D.tsx # Traditional Vedic birth chart
├── shared/                 # Shared utilities (future)
├── VisualizationArea.tsx   # Main visualization container
├── index.ts               # Export index for easy imports
├── types.ts               # TypeScript type definitions
└── README.md              # This file
```

## 🎯 Main Components

### 3D Components

#### `CelestialSphere.tsx`
- **Purpose**: Main 3D celestial sphere visualization
- **Features**: 
  - Earth at center with rotation and atmosphere
  - 9 Vedic planets with floating animations
  - 12 Rashis (zodiac signs) in rotating orange ring
  - 27 Nakshatras in rotating blue ring
  - Interactive controls (rotate, zoom, pan)
- **Usage**: Primary 3D visualization for the app

#### `SimpleThreeTest.tsx`
- **Purpose**: Basic Three.js functionality test
- **Features**: Rotating orange cube with status indicators
- **Usage**: Testing Three.js setup and WebGL support

### 2D Components

#### `TraditionalChart2D.tsx`
- **Purpose**: Traditional Vedic birth chart layout
- **Features**: Classic square/diamond chart format
- **Usage**: Alternative view for traditional astrologers

## 🔧 Usage

### Import Components

```typescript
// Individual imports
import CelestialSphere from '../frontend/visualization/3d/CelestialSphere';
import SimpleThreeTest from '../frontend/visualization/3d/SimpleThreeTest';

// Or use the index file (when available)
import { CelestialSphere, SimpleThreeTest } from '../frontend/visualization';
```

### Basic Usage

```typescript
// 3D Celestial Sphere
<Canvas camera={{ position: [0, 0, 50], fov: 75 }}>
  <ambientLight intensity={0.3} />
  <directionalLight position={[100, 100, 100]} intensity={0.8} />
  <Stars radius={300} depth={50} count={5000} />
  <CelestialSphere />
  <OrbitControls />
</Canvas>

// Three.js Test
<SimpleThreeTest />
```

## 🎨 Styling

All components use:
- **Cosmic theme**: Dark backgrounds with stellar colors
- **Tailwind CSS**: For consistent styling
- **Three.js materials**: For 3D rendering
- **Responsive design**: Adapts to different screen sizes

## 🔮 Vedic Elements

### Planets (Grahas)
- Sun (Surya) - Gold
- Moon (Chandra) - Silver
- Mars (Mangal) - Red
- Mercury (Budh) - Green
- Jupiter (Guru) - Blue
- Venus (Shukra) - Pink
- Saturn (Shani) - Purple
- Rahu - Gray
- Ketu - Gray

### Rashis (Zodiac Signs)
- 12 signs in orange rotating ring
- Traditional Sanskrit names with English translations

### Nakshatras (Lunar Mansions)
- 27 nakshatras in blue rotating ring
- Individual markers with labels

## 🚀 Future Enhancements

- [ ] Real astronomical data integration
- [ ] Interactive planet clicking for details
- [ ] Customizable color schemes
- [ ] Animation speed controls
- [ ] Export functionality
- [ ] VR/AR support
- [ ] Multi-language support

## 🛠️ Development

### Adding New Components

1. Create component in appropriate subfolder (`3d/`, `2d/`, `shared/`)
2. Add export to `index.ts`
3. Update types in `types.ts` if needed
4. Update this README

### Testing

- Use `SimpleThreeTest` to verify Three.js functionality
- Check browser console for WebGL support
- Test on different devices and browsers

## 📚 Dependencies

- **@react-three/fiber**: React renderer for Three.js
- **@react-three/drei**: Useful helpers for React Three Fiber
- **three**: 3D graphics library
- **React**: UI framework
- **TypeScript**: Type safety
