#!/usr/bin/env python3
"""
Startup script for Comprehensive Vedic Astrology API
Runs the new organized backend with all components
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def main():
    """Run the comprehensive API server."""
    
    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🌟 COMPREHENSIVE VEDIC ASTROLOGY API")
    print("=" * 50)
    print("🏗️ New Organized Project Structure")
    print("📊 Exposing ALL Vedic Analysis Data")
    print("🔧 All Components Integrated")
    print("=" * 50)
    
    # Check if all required files exist
    required_files = [
        "src/api/comprehensive_api.py",
        "src/services/comprehensive_prediction_service.py",
        "src/core/vedic_calculator.py",
        "src/core/vedic_analysis.py",
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
    print("\n🚀 Starting Comprehensive API Server...")
    print("📡 Server will be available at: http://localhost:8005")
    print("📚 API Documentation: http://localhost:8005/api/docs")
    print("🔍 Health Check: http://localhost:8005/api/health")
    print("📊 Analysis Components: http://localhost:8005/api/analysis-components")
    print("\n" + "=" * 50)
    print("🎯 COMPREHENSIVE DATA EXPOSURE:")
    print("   • VedicCalculator - Core chart calculations")
    print("   • VedicAnalyzer - Personality & relationship analysis")
    print("   • VedicPredictionEngine - AI-powered predictions")
    print("   • DivisionalAnalyzer - All divisional charts (D1-D60)")
    print("   • CurrentInfluenceAnalyzer - Real-time transits")
    print("   • AdvancedTimingCalculator - Timing & muhurta")
    print("   • PlanetaryCombinationDescriptions - Yoga details")
    print("   • Specialized Engines - Career, health, relationships")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the comprehensive API server
        result = subprocess.run([
            sys.executable, "-m", "uvicorn",
            "src.api.comprehensive_api:app",
            "--host", "0.0.0.0",
            "--port", "8005", 
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
