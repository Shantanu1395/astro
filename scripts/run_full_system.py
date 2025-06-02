#!/usr/bin/env python3
"""
Full System Startup Script
Runs both backend API and frontend server together
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path
import threading
import requests

def main():
    """Start both backend and frontend servers."""
    
    print("🌟 VEDIC ASTROLOGY FULL SYSTEM STARTUP")
    print("=" * 60)
    print("🏗️ Starting Backend + Frontend Integration")
    print("📊 Complete Vedic Analysis System")
    print("🌐 Modern Web Interface")
    print("=" * 60)
    
    # Check if all required files exist
    required_files = [
        "src/api/comprehensive_backend_api.py",
        "src/api/frontend_server.py",
        "frontend/templates/index.html",
        "frontend/static/style.css"
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
        return
    
    print("✅ All required files found\n")
    
    # Store process references
    backend_process = None
    frontend_process = None
    
    def signal_handler(sig, frame):
        """Handle Ctrl+C gracefully."""
        print("\n🛑 Shutting down servers...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Servers stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Start backend server
        print("🚀 Starting Backend API Server...")
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "src.api.comprehensive_backend_api:app",
            "--host", "0.0.0.0",
            "--port", "8006",
            "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for backend to start
        print("⏳ Waiting for backend to initialize...")
        backend_ready = False
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get("http://localhost:8006/api/health", timeout=2)
                if response.status_code == 200:
                    backend_ready = True
                    break
            except:
                pass
            time.sleep(1)
            print(f"   Checking backend... ({i+1}/30)")
        
        if not backend_ready:
            print("❌ Backend failed to start within 30 seconds")
            return
        
        print("✅ Backend API ready at http://localhost:8006")
        
        # Start frontend server
        print("\n🌐 Starting Frontend Server...")
        frontend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "src.api.frontend_server:app",
            "--host", "0.0.0.0", 
            "--port", "8007",
            "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for frontend to start
        print("⏳ Waiting for frontend to initialize...")
        frontend_ready = False
        for i in range(15):  # Wait up to 15 seconds
            try:
                response = requests.get("http://localhost:8007/api/status", timeout=2)
                if response.status_code == 200:
                    frontend_ready = True
                    break
            except:
                pass
            time.sleep(1)
            print(f"   Checking frontend... ({i+1}/15)")
        
        if not frontend_ready:
            print("❌ Frontend failed to start within 15 seconds")
            return
        
        print("✅ Frontend ready at http://localhost:8007")
        
        # Display startup summary
        print("\n" + "=" * 60)
        print("🎉 FULL SYSTEM READY!")
        print("=" * 60)
        print("🌐 FRONTEND INTERFACE:")
        print("   • Main App: http://localhost:8007")
        print("   • Modern UI: http://localhost:8007/modern")
        print("   • Status: http://localhost:8007/api/status")
        print()
        print("🔧 BACKEND API:")
        print("   • API Server: http://localhost:8006")
        print("   • Documentation: http://localhost:8006/api/docs")
        print("   • Health Check: http://localhost:8006/api/health")
        print()
        print("📊 FEATURES AVAILABLE:")
        print("   • Complete Vedic chart calculations")
        print("   • Planetary strength analysis")
        print("   • Personality analysis")
        print("   • Yoga combinations")
        print("   • Divisional charts (D2, D3, D9, D10, D12)")
        print("   • Current influences")
        print("   • AI-powered predictions")
        print("   • 100,000+ data points per analysis")
        print()
        print("🎯 USAGE:")
        print("   1. Open http://localhost:8007 in your browser")
        print("   2. Enter birth details in the form")
        print("   3. Get comprehensive Vedic analysis")
        print()
        print("=" * 60)
        print("Press Ctrl+C to stop both servers")
        print("=" * 60)
        
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
    
    except KeyboardInterrupt:
        print("\n🛑 Received shutdown signal")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Cleanup complete")

if __name__ == "__main__":
    main()
