#!/usr/bin/env python3
"""
Environment Setup Script for Vedic Astrology System
Creates virtual environment and installs all dependencies
"""

import subprocess
import sys
import os
from pathlib import Path
import platform

def print_banner():
    """Print setup banner."""
    print("🐍" * 30)
    print("🐍 VEDIC ASTROLOGY ENVIRONMENT SETUP")
    print("🐍" * 30)
    print("🔧 Creating Virtual Environment")
    print("📦 Installing Dependencies")
    print("✅ Setting up Project")
    print("=" * 60)

def run_command(command, description, check=True):
    """Run a command with description."""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Requires Python 3.8 or higher")
        return False

def setup_virtual_environment():
    """Set up virtual environment."""
    project_root = Path(__file__).parent.parent
    venv_path = project_root / "venv_astrology"
    
    print(f"📁 Project root: {project_root}")
    print(f"🐍 Virtual environment: {venv_path}")
    
    # Change to project directory
    os.chdir(project_root)
    
    # Remove existing venv if it exists
    if venv_path.exists():
        print("🗑️  Removing existing virtual environment...")
        if platform.system() == "Windows":
            run_command(f"rmdir /s /q {venv_path}", "Removing old venv", check=False)
        else:
            run_command(f"rm -rf {venv_path}", "Removing old venv", check=False)
    
    # Create new virtual environment
    if not run_command(f"python -m venv {venv_path}", "Creating virtual environment"):
        return False
    
    # Determine activation script path
    if platform.system() == "Windows":
        activate_script = venv_path / "Scripts" / "activate"
        pip_path = venv_path / "Scripts" / "pip"
    else:
        activate_script = venv_path / "bin" / "activate"
        pip_path = venv_path / "bin" / "pip"
    
    print(f"🔧 Activation script: {activate_script}")
    
    # Upgrade pip in virtual environment
    if not run_command(f"{pip_path} install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies"):
        return False
    
    return True, activate_script

def create_activation_scripts():
    """Create convenient activation scripts."""
    project_root = Path(__file__).parent.parent
    
    # Create activation script for Unix/Mac
    activate_script_content = """#!/bin/bash
# Vedic Astrology System - Environment Activation Script

echo "🌟 Activating Vedic Astrology Virtual Environment..."
source venv_astrology/bin/activate
echo "✅ Virtual environment activated!"
echo ""
echo "🚀 Available commands:"
echo "   python scripts/run_full_system.py     # Start full system (backend + frontend)"
echo "   python scripts/run_comprehensive_backend.py  # Backend only"
echo "   python -m uvicorn src.api.frontend_server:app --port 8007  # Frontend only"
echo ""
echo "🌐 URLs when running:"
echo "   Frontend: http://localhost:8007"
echo "   Backend:  http://localhost:8006"
echo ""
"""
    
    with open(project_root / "activate.sh", "w") as f:
        f.write(activate_script_content)
    
    # Make it executable
    run_command("chmod +x activate.sh", "Making activation script executable", check=False)
    
    # Create Windows batch file
    activate_bat_content = """@echo off
REM Vedic Astrology System - Environment Activation Script

echo 🌟 Activating Vedic Astrology Virtual Environment...
call venv_astrology\\Scripts\\activate.bat
echo ✅ Virtual environment activated!
echo.
echo 🚀 Available commands:
echo    python scripts/run_full_system.py     # Start full system (backend + frontend)
echo    python scripts/run_comprehensive_backend.py  # Backend only
echo    python -m uvicorn src.api.frontend_server:app --port 8007  # Frontend only
echo.
echo 🌐 URLs when running:
echo    Frontend: http://localhost:8007
echo    Backend:  http://localhost:8006
echo.
"""
    
    with open(project_root / "activate.bat", "w") as f:
        f.write(activate_bat_content)
    
    print("✅ Created activation scripts: activate.sh (Unix/Mac) and activate.bat (Windows)")

def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    result = setup_virtual_environment()
    if not result:
        print("❌ Failed to set up virtual environment")
        sys.exit(1)
    
    success, activate_script = result
    if not success:
        sys.exit(1)
    
    # Create activation scripts
    create_activation_scripts()
    
    print()
    print("=" * 60)
    print("🎉 ENVIRONMENT SETUP COMPLETE!")
    print("=" * 60)
    print()
    print("🐍 Virtual Environment: venv_astrology/")
    print("📦 All dependencies installed from requirements.txt")
    print("🔧 Project structure organized and ready")
    print()
    print("🚀 TO START USING:")
    print()
    
    if platform.system() == "Windows":
        print("   1. Run: activate.bat")
        print("   2. Run: python scripts/run_full_system.py")
    else:
        print("   1. Run: source activate.sh")
        print("   2. Run: python scripts/run_full_system.py")
    
    print()
    print("🌐 OR manually activate:")
    if platform.system() == "Windows":
        print(f"   {activate_script}")
    else:
        print(f"   source {activate_script}")
    
    print()
    print("✅ Ready to run the Vedic Astrology System!")
    print("=" * 60)

if __name__ == "__main__":
    main()
