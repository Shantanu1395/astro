#!/usr/bin/env python3
"""
Startup script for Comprehensive Vedic Astrology Backend API
Runs the organized backend exposing ALL Vedic analysis data
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def main():
    """Run the comprehensive backend API server."""

    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("🌟 COMPREHENSIVE VEDIC ASTROLOGY BACKEND API")
    print("=" * 60)
    print("🏗️ Organized Project Structure")
    print("📊 Exposing ALL Vedic Analysis Data")
    print("🔧 All Components Integrated")
    print("=" * 60)

    # Check if all required files exist in new structure
    required_files = [
        "src/api/comprehensive_backend_api.py",
        "src/core/vedic_calculator.py",
        "src/core/vedic_analysis.py",
        "src/core/prediction_engine.py",
        "src/core/divisional_analyzer.py",
        "src/core/current_influences.py",
        "src/core/advanced_timing.py",
        "src/services/specialized_engines.py",
        "src/services/engine_manager.py",
        "src/models/models.py"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\nPlease ensure all files are in place before starting.")
        return False

    print("✅ All required files found")
    print("\n🚀 Starting Comprehensive Backend API Server...")
    print("📡 Server will be available at: http://localhost:8006")
    print("📚 API Documentation: http://localhost:8006/api/docs")
    print("🔍 Health Check: http://localhost:8006/api/health")
    print("📊 Components Info: http://localhost:8006/api/components")
    print("\n" + "=" * 60)
    print("🎯 COMPREHENSIVE DATA EXPOSURE:")
    print("   • VedicCalculator - Core chart calculations")
    print("     - Planetary positions, houses, nakshatras")
    print("     - Dasha periods, planetary strengths")
    print("   • VedicAnalyzer - Analysis & interpretation")
    print("     - Personality traits, yogas, relationships")
    print("     - Behavioral patterns, dasha significance")
    print("   • VedicPredictionEngine - AI predictions")
    print("     - LLM-powered interpretations")
    print("     - Key themes, favorable periods")
    print("   • DivisionalAnalyzer - Divisional charts")
    print("     - D1, D2, D3, D4, D7, D9, D10, D12, D16, D20")
    print("     - Specialized analysis for each division")
    print("   • CurrentInfluenceAnalyzer - Real-time data")
    print("     - Current transits, lunar phases")
    print("     - Daily/monthly influences")
    print("   • AdvancedTimingCalculator - Timing analysis")
    print("     - Favorable/challenging periods")
    print("     - Muhurta analysis")
    print("   • SpecializedEngines - Domain-specific analysis")
    print("     - Career, relationship, health, financial, spiritual")
    print("=" * 60)
    print("📋 SAMPLE REQUEST:")
    print("""
    POST /api/comprehensive-analysis
    {
        "name": "John Doe",
        "birth_date": "1990-06-15",
        "birth_time": "14:30",
        "birth_location": "Mumbai, India",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "timezone": "Asia/Kolkata"
    }
    """)
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)

    try:
        # Start the comprehensive backend API server
        result = subprocess.run([
            sys.executable, "-m", "uvicorn",
            "src.api.comprehensive_backend_api:app",
            "--host", "0.0.0.0",
            "--port", "8006",
            "--reload",
            "--log-level", "info"
        ], cwd=project_root)

        return result.returncode == 0

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("✅ Server shutdown complete")
    else:
        print("❌ Server failed to start properly")
        sys.exit(1)
