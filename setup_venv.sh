#!/bin/bash

# 🌟 Vedic Astrology System - Virtual Environment Setup Script

echo "🌟 VEDIC ASTROLOGY SYSTEM - VIRTUAL ENVIRONMENT SETUP"
echo "======================================================"

# Check if Python 3.8+ is available
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 1 ]]; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python $python_version is not compatible. Requires Python 3.8+"
    exit 1
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv_astrology

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv_astrology/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install core dependencies
echo "📚 Installing core dependencies..."
pip install fastapi uvicorn jinja2 python-multipart pydantic pyswisseph httpx python-dotenv requests geopy python-dateutil openai aiofiles pytest pytest-asyncio pytz

echo ""
echo "✅ SETUP COMPLETE!"
echo "=================="
echo ""
echo "🚀 TO START THE SYSTEM:"
echo "   1. Activate environment: source venv_astrology/bin/activate"
echo "   2. Start backend: python scripts/run_comprehensive_backend.py"
echo "   3. (Optional) Start frontend: python -m uvicorn src.api.frontend_server:app --port 8007"
echo ""
echo "🌐 ACCESS POINTS:"
echo "   Backend API: http://localhost:8006/api/docs"
echo "   Frontend UI: http://localhost:8007"
echo ""
echo "🎯 Ready to use!"
