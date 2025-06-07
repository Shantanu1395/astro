// Application Entry Point

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App_Simple';
import './index.css';

// Error handling for the entire application
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
});

// Performance monitoring
if (process.env.NODE_ENV === 'development') {
  // Log performance metrics
  window.addEventListener('load', () => {
    const perfData = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    console.log('🚀 Performance Metrics:', {
      'DOM Content Loaded': `${perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart}ms`,
      'Load Complete': `${perfData.loadEventEnd - perfData.loadEventStart}ms`,
      'Total Load Time': `${perfData.loadEventEnd - perfData.fetchStart}ms`,
    });
  });
}

// Initialize React application
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
