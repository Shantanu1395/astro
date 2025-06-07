/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  safelist: [
    // Ensure cosmic theme classes are always included
    'bg-cosmic-dark',
    'bg-cosmic-deep',
    'bg-cosmic-medium',
    'text-stellar-silver',
    'text-stellar-gold',
    'text-stellar-blue',
    'border-stellar-silver',
    // Include opacity variants
    'bg-cosmic-deep/80',
    'bg-cosmic-medium/50',
    'border-stellar-silver/20',
    'text-stellar-silver/80',
    'text-stellar-silver/60',
  ],
  theme: {
    extend: {
      colors: {
        // Cosmic Theme
        'cosmic-dark': '#0a0a0f',
        'cosmic-deep': '#1a1a2e',
        'cosmic-medium': '#16213e',
        'cosmic-light': '#2d3748',
        // Stellar Colors
        'stellar-blue': '#1e3a8a',
        'stellar-silver': '#e5e7eb',
        'stellar-gold': '#fbbf24',
        'stellar-purple': '#7c3aed',
        // Planetary Colors
        planets: {
          sun: '#fbbf24',      // Solar gold
          moon: '#e5e7eb',     // Lunar silver
          mars: '#dc2626',     // Mars red
          mercury: '#059669',  // Mercury green
          jupiter: '#2563eb',  // Jupiter blue
          venus: '#ec4899',    // Venus pink
          saturn: '#7c3aed',   // Saturn purple
          rahu: '#78716c',     // Rahu brown
          ketu: '#78716c',     // Ketu brown
        },
        // Astrological Elements
        elements: {
          fire: '#dc2626',     // Aries, Leo, Sagittarius
          earth: '#059669',    // Taurus, Virgo, Capricorn
          air: '#3b82f6',      // Gemini, Libra, Aquarius
          water: '#7c3aed',    // Cancer, Scorpio, Pisces
        },
        // UI Semantic Colors
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
        info: '#3b82f6',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        body: ['Source Sans Pro', 'system-ui', 'sans-serif'],
        sanskrit: ['Noto Sans Devanagari', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'spin-slow': 'spin 20s linear infinite',
        'pulse-slow': 'pulse 4s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(59, 130, 246, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(59, 130, 246, 0.8)' },
        },
      },
      backdropBlur: {
        xs: '2px',
        sm: '4px',
        md: '8px',
        lg: '16px',
        xl: '24px',
      },
    },
  },
  plugins: [],
}
