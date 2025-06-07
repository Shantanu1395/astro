# System Monitoring Implementation

## Overview

This document describes the comprehensive system monitoring implementation added to the Vedic Astrology visualization application. The monitoring system provides real-time CPU and memory utilization tracking for both the current running process and the overall system.

## Architecture

### Backend Components

#### 1. System Metrics API Endpoint
**File**: `src/api/main.py`
**Endpoint**: `GET /api/system-metrics`

```python
@app.get("/api/system-metrics")
async def get_system_metrics():
    """Get real-time system metrics for monitoring."""
```

**Features**:
- Real-time CPU usage monitoring
- Memory usage tracking (total, used, available, percentage)
- Disk usage statistics
- Network I/O statistics
- Process-specific metrics (PID, CPU, memory, threads)
- Error handling for unavailable metrics

**Dependencies**:
- `psutil==5.9.8` - Cross-platform system and process utilities

#### 2. Response Format
```json
{
  "success": true,
  "timestamp": "2025-06-07T18:35:07.190009",
  "system": {
    "cpu_percent": 24.7,
    "memory": {
      "total": 38654705664,
      "available": 16192782336,
      "percent": 58.1,
      "used": 20096909312,
      "free": 427261952
    },
    "disk": {
      "total": 994662584320,
      "used": 16016371712,
      "free": 681345347584,
      "percent": 1.61
    },
    "network": {
      "bytes_sent": 6418189312,
      "bytes_recv": 5914971136,
      "packets_sent": 11896443,
      "packets_recv": 18984816
    }
  },
  "process": {
    "pid": 76665,
    "cpu_percent": 0.0,
    "memory": {
      "rss": 82624512,
      "vms": 421513084928,
      "percent": 0.21
    },
    "threads": 2,
    "status": "running",
    "create_time": 1733598907.0,
    "name": "python"
  }
}
```

### Frontend Components

#### 1. Enhanced Performance Monitor
**File**: `frontend/visualization/shared/EnhancedMonitor.tsx`

**Features**:
- Real-time system metrics display
- Tabbed interface (Overview, System, Browser, WebGL)
- Expandable/collapsible design
- Color-coded status indicators
- Positioning options (top-left, top-right, bottom-left, bottom-right)
- Show/hide functionality

#### 2. Performance Monitoring Hook
**File**: `frontend/visualization/shared/usePerformanceMonitor.ts`

**Features**:
- FPS calculation and tracking
- Browser memory monitoring (JS heap)
- System metrics fetching
- WebGL performance tracking
- Automatic metric updates
- Error handling

#### 3. System Monitor Component
**File**: `frontend/visualization/shared/SystemMonitor.tsx`

**Features**:
- Dedicated system resource monitoring
- Server-side metrics integration
- Browser performance metrics
- Real-time updates
- Compact and expanded views

#### 4. Stats Monitor Component
**File**: `frontend/visualization/shared/StatsMonitor.tsx`

**Features**:
- WebGL performance monitoring using stats-gl
- GPU tracking capabilities
- Three.js integration
- Customizable positioning

## Integration

### App Integration
**File**: `src/App_Simple.tsx`

```tsx
import EnhancedMonitor from '../frontend/visualization/shared/EnhancedMonitor';

// In component JSX:
<EnhancedMonitor 
  position="top-right" 
  updateInterval={1000}
  trackGPU={true}
  trackSystem={true}
  trackWebGL={true}
  defaultExpanded={false}
/>
```

## Metrics Tracked

### System Metrics
- **CPU Usage**: Real-time CPU utilization percentage
- **Memory Usage**: Total, used, available, and percentage
- **Disk Usage**: Total, used, free space and percentage
- **Network**: Bytes sent/received, packets sent/received

### Process Metrics
- **Process ID**: Current process identifier
- **CPU Usage**: Process-specific CPU utilization
- **Memory**: RSS (Resident Set Size), VMS (Virtual Memory Size)
- **Threads**: Number of active threads
- **Status**: Process status (running, sleeping, etc.)
- **Creation Time**: Process start timestamp

### Browser Metrics
- **FPS**: Frames per second calculation
- **JS Heap**: Used, total, and limit memory
- **Load Time**: Page load performance
- **DOM Content Loaded**: DOM parsing time

### WebGL Metrics
- **GPU Info**: Vendor, renderer, version
- **Draw Calls**: Number of WebGL draw calls
- **Triangles**: Rendered triangle count
- **Geometries**: Number of geometries
- **Textures**: Number of loaded textures

## Configuration

### Update Intervals
- Default: 1000ms (1 second)
- Configurable per component
- Automatic FPS calculation

### Positioning
- `top-left`
- `top-right` (default)
- `bottom-left`
- `bottom-right`

### Display Options
- Compact mode
- Expanded mode with tabs
- Show/hide toggle
- Color-coded status indicators

## Status Indicators

### Color Coding
- **Green**: Good performance (< 50% usage)
- **Yellow**: Moderate usage (50-80%)
- **Red**: High usage (> 80%)

### FPS Indicators
- **Green**: > 50 FPS
- **Yellow**: 30-50 FPS
- **Red**: < 30 FPS

## Dependencies

### Backend
```txt
psutil==5.9.8
```

### Frontend
```json
{
  "stats-gl": "^2.0.0",
  "framer-motion": "^10.0.0",
  "lucide-react": "^0.263.1"
}
```

## Usage Examples

### Basic Usage
```tsx
import { EnhancedMonitor } from '../frontend/visualization/shared';

<EnhancedMonitor />
```

### Advanced Configuration
```tsx
<EnhancedMonitor 
  position="bottom-left"
  updateInterval={2000}
  trackGPU={false}
  trackSystem={true}
  trackWebGL={false}
  defaultExpanded={true}
/>
```

### Custom Hook Usage
```tsx
import { usePerformanceMonitor } from '../frontend/visualization/shared';

const { metrics, isSupported, error, formatBytes, getStatusColor } = usePerformanceMonitor({
  updateInterval: 1000,
  trackGPU: true,
  trackSystem: true,
  trackWebGL: true
});
```

## Performance Considerations

- Monitoring updates run at configurable intervals
- FPS calculation uses requestAnimationFrame for accuracy
- System metrics are fetched asynchronously
- Error handling prevents monitoring failures from affecting app
- Minimal performance impact on visualization rendering

## Browser Compatibility

- Modern browsers with WebGL support
- Performance.memory API (Chrome, Edge)
- RequestAnimationFrame support
- Fetch API support

## Future Enhancements

1. **Historical Data**: Store and display performance trends
2. **Alerts**: Configurable performance thresholds
3. **Export**: Save performance data to files
4. **Comparison**: Compare performance across sessions
5. **Advanced WebGL**: More detailed GPU metrics
6. **Mobile Support**: Touch-friendly interface
7. **Real-time Graphs**: Visual performance charts

## Troubleshooting

### Common Issues

1. **System metrics unavailable**: Check backend server connection
2. **WebGL info missing**: Verify WebGL support in browser
3. **Memory metrics unavailable**: Use Chrome/Edge for full support
4. **High CPU usage**: Increase update intervals

### Debug Mode
Enable console logging for detailed monitoring information:
```javascript
localStorage.setItem('debug-monitoring', 'true');
```

## Conclusion

The system monitoring implementation provides comprehensive real-time performance tracking for both system resources and application-specific metrics. It integrates seamlessly with the existing Vedic Astrology visualization while providing valuable insights into system performance and resource utilization.
