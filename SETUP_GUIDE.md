# 🌟 Vedic Astrology System - Setup Guide

## 🐍 **Virtual Environment Setup**

### **1. Create Virtual Environment**
```bash
cd /Users/shantanu/Documents/Coding/Python/SacredTextRag
python -m venv venv_astrology
```

### **2. Activate Virtual Environment**

**On macOS/Linux:**
```bash
source venv_astrology/bin/activate
```

**On Windows:**
```bash
venv_astrology\Scripts\activate
```

### **3. Install Core Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements_core.txt
```

### **4. Alternative: Install Manually**
If requirements.txt has conflicts, install core packages manually:
```bash
pip install fastapi uvicorn jinja2 python-multipart pydantic pyswisseph httpx python-dotenv requests
```

## 🚀 **Running the System**

### **Option 1: Backend Only**
```bash
# Activate virtual environment first
source venv_astrology/bin/activate

# Start comprehensive backend API
python scripts/run_comprehensive_backend.py
```
- **Access**: http://localhost:8006/api/docs

### **Option 2: Frontend + Backend**
```bash
# Terminal 1: Start Backend
source venv_astrology/bin/activate
python scripts/run_comprehensive_backend.py

# Terminal 2: Start Frontend
source venv_astrology/bin/activate
python -m uvicorn src.api.frontend_server:app --host 0.0.0.0 --port 8007 --reload
```

### **Option 3: Full System (Automated)**
```bash
source venv_astrology/bin/activate
python scripts/run_full_system.py
```

## 🌐 **Access Points**

### **Frontend (User Interface)**
- **Main App**: http://localhost:8007
- **Modern UI**: http://localhost:8007/modern
- **Status**: http://localhost:8007/api/status

### **Backend (API Services)**
- **API Docs**: http://localhost:8006/api/docs
- **Health Check**: http://localhost:8006/api/health
- **Components**: http://localhost:8006/api/components

## 📊 **Testing the API**

### **Sample Request**
```bash
curl -X POST "http://localhost:8006/api/comprehensive-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "birth_date": "1990-06-15",
    "birth_time": "14:30",
    "birth_location": "Mumbai, India"
  }'
```

### **Expected Response**
- Complete Vedic chart (planets, houses, signs)
- Planetary strengths and relationships
- Personality analysis
- Yoga combinations
- Divisional charts (D2, D3, D9, D10, D12)
- Current influences
- AI-powered predictions
- 100,000+ data points

## 🔧 **Project Structure**
```
vedic-astrology-system/
├── 📁 venv_astrology/        # Virtual environment
├── 📁 src/
│   ├── 📁 core/              # Core calculations
│   ├── 📁 api/               # API endpoints
│   ├── 📁 services/          # Business logic
│   ├── 📁 models/            # Data models
│   └── 📁 utils/             # Utilities
├── 📁 frontend/              # UI templates & static files
├── 📁 scripts/               # Startup scripts
├── 📁 tests/                 # Test suite
├── 📁 config/                # Configuration
├── requirements_core.txt     # Core dependencies
└── requirements.txt          # Full dependencies
```

## 🛠️ **Troubleshooting**

### **Port Already in Use**
```bash
# Kill existing processes
lsof -ti:8006 | xargs kill -9
lsof -ti:8007 | xargs kill -9
```

### **Dependency Conflicts**
Use the core requirements file:
```bash
pip install -r requirements_core.txt
```

### **Missing Dependencies**
Install individually:
```bash
pip install fastapi uvicorn jinja2 pyswisseph httpx
```

## ✅ **Quick Start Checklist**

1. ✅ Create virtual environment: `python -m venv venv_astrology`
2. ✅ Activate environment: `source venv_astrology/bin/activate`
3. ✅ Install dependencies: `pip install -r requirements_core.txt`
4. ✅ Start backend: `python scripts/run_comprehensive_backend.py`
5. ✅ Test API: Open http://localhost:8006/api/docs
6. ✅ (Optional) Start frontend: `python -m uvicorn src.api.frontend_server:app --port 8007`
7. ✅ Use system: Open http://localhost:8007

## 🎯 **Ready to Use!**

The Vedic Astrology System provides comprehensive astrological analysis with:
- Professional API with interactive documentation
- Modern web interface
- Complete data exposure from all components
- Fast response times (~11ms for full analysis)
- Organized, scalable codebase

**Happy Astrology Computing! 🌟**
