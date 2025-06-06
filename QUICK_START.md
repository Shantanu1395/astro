# 🌟 Vedic Astrology API - Quick Start Guide

## 🚀 Fastest Way to Run

```bash
# 1. Activate virtual environment
source venv_astrology/bin/activate

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Run the server
gunicorn src.api.main:app -c gunicorn.conf.py

# 4. Test the API
curl http://localhost:8000/api/test/yourname
```

## 🌐 Access Points

- **API Server**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:8000/

## ⚙️ Configuration Options

### Development Mode (1 worker, auto-reload)
```bash
ENVIRONMENT=development gunicorn src.api.main:app -c gunicorn.conf.py
```

### Performance Mode (3 workers)
```bash
WORKER_COUNT=3 gunicorn src.api.main:app -c gunicorn.conf.py
```

### Production Mode (auto-scaling)
```bash
ENVIRONMENT=production gunicorn src.api.main:app -c gunicorn.conf.py
```

## 🔧 LLM Configuration

Edit `.env` file:

### Option 1: Ollama (Recommended)
```env
LLM_PROVIDER=ollama
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=codestral
```

### Option 2: OpenAI
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### Option 3: Fallback (No LLM)
```env
LLM_PROVIDER=fallback
```

## 📊 Performance Testing

```bash
# Basic load test
python scripts/load_test.py

# Intensive stress test
python scripts/intensive_stress_test.py
```

## 🔍 API Testing

```bash
# Test prediction endpoint
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "birth_date": "1994-03-01",
      "birth_time": "23:02", 
      "birth_location": "Faridabad, India"
    }
  }'
```

## 🛠️ Troubleshooting

### Port in use
```bash
lsof -ti:8000 | xargs kill -9
```

### Import errors
```bash
python scripts/fix_imports.py
```

### Check Ollama
```bash
curl http://localhost:11434
```

## 📋 Key Features

✅ **Vedic Astrology Calculations** - Swiss Ephemeris precision  
✅ **Async Geocoding** - Optimized for performance  
✅ **Multi-worker Scaling** - 1-29 workers based on load  
✅ **LLM Integration** - OpenAI/Ollama/Fallback modes  
✅ **Comprehensive API** - Full documentation at `/docs`  
✅ **Load Testing** - Built-in performance monitoring  

## 🎯 Main API Endpoints

- `POST /api/predict` - Main prediction endpoint
- `POST /api/comprehensive-analysis` - Detailed analysis  
- `POST /api/quick-chart` - Quick birth chart
- `POST /api/divisional-charts` - Varga charts
- `POST /api/current-transits` - Current planetary positions
- `GET /api/test/{name}` - Health check

---

For complete setup instructions, run: `./run_project`
