"""
Frontend Server for Vedic Astrology System
Serves HTML templates and integrates with comprehensive backend API
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import httpx
import logging
from datetime import datetime, date, time
from typing import Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app for frontend
app = FastAPI(
    title="Vedic Astrology Frontend",
    description="Frontend interface for comprehensive Vedic astrology analysis",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="frontend/templates")

# Backend API URL
BACKEND_API_URL = "http://localhost:8006"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/modern", response_class=HTMLResponse)
async def modern_home(request: Request):
    """Serve the modern UI page."""
    return templates.TemplateResponse("index_modern.html", {"request": request})

@app.post("/predict")
async def predict(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(...),
    birth_time: str = Form(...),
    birth_location: str = Form(...)
):
    """
    Handle prediction form submission and call comprehensive backend API.
    """
    try:
        logger.info(f"Processing prediction request for {name}")
        
        # Prepare request data for backend API
        backend_request = {
            "name": name,
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_location": birth_location
        }
        
        # Call comprehensive backend API
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{BACKEND_API_URL}/api/comprehensive-analysis",
                json=backend_request
            )
            
            if response.status_code == 200:
                analysis_data = response.json()
                
                if analysis_data.get("success"):
                    # Extract data from backend response
                    data = analysis_data["data"]

                    # Prepare data for template (matching template variable names)
                    template_data = {
                        "request": request,
                        "analysis": data,
                        "metadata": analysis_data["metadata"],
                        "person_name": name,

                        # Birth data for template
                        "birth_data": {
                            "name": name,
                            "birth_date": birth_date,
                            "birth_time": birth_time,
                            "birth_location": birth_location
                        },

                        # Chart data
                        "chart": data.get("vedic_chart", {}),

                        # Prediction data
                        "prediction": {
                            "current_dasha": data.get("current_dasha", {})
                        },
                        "current_dasha": data.get("current_dasha", {}),

                        # Planetary data
                        "planetary_strengths": data.get("planetary_strengths", {}),
                        "planetary_relationships": data.get("planetary_relationships", {}),
                        "planetary_descriptions": data.get("planetary_descriptions", {}),
                        "planetary_remedies": data.get("planetary_remedies", {}),
                        "planetary_aspects": data.get("planetary_aspects", []),

                        # Divisional charts
                        "comprehensive_divisional_analysis": data.get("divisional_charts", {}),

                        # Other analysis
                        "dasha_analysis": data.get("dasha_analysis", {}),
                        "personality_analysis": data.get("personality_analysis", {}),
                        "current_influences": data.get("current_influences", {}),
                        "ai_prediction": data.get("ai_prediction", {}),
                        "specialized_predictions": data.get("specialized_predictions", {})
                    }

                    # Render results page with comprehensive data
                    return templates.TemplateResponse("cosmic-results.html", template_data)
                else:
                    error_message = analysis_data.get("error", "Unknown error occurred")
                    return templates.TemplateResponse("index.html", {
                        "request": request,
                        "error": f"Analysis failed: {error_message}"
                    })
            else:
                logger.error(f"Backend API error: {response.status_code}")
                return templates.TemplateResponse("index.html", {
                    "request": request,
                    "error": f"Backend service error: {response.status_code}"
                })
                
    except httpx.TimeoutException:
        logger.error("Backend API timeout")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Request timeout. Please try again."
        })
    except Exception as e:
        logger.error(f"Error processing prediction: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"An error occurred: {str(e)}"
        })

@app.get("/api/status")
async def frontend_status():
    """Check frontend and backend status."""
    try:
        # Check backend health
        async with httpx.AsyncClient(timeout=10.0) as client:
            backend_response = await client.get(f"{BACKEND_API_URL}/api/health")
            backend_healthy = backend_response.status_code == 200
            backend_data = backend_response.json() if backend_healthy else None
    except:
        backend_healthy = False
        backend_data = None
    
    return {
        "frontend": {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        },
        "backend": {
            "status": "healthy" if backend_healthy else "unhealthy",
            "url": BACKEND_API_URL,
            "data": backend_data
        },
        "integration": {
            "status": "working" if backend_healthy else "backend_unavailable",
            "endpoints": {
                "home": "/",
                "modern_ui": "/modern",
                "prediction": "/predict",
                "status": "/api/status"
            }
        }
    }

@app.get("/test")
async def test_page(request: Request):
    """Test page for development."""
    return templates.TemplateResponse("chart_test.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.frontend_server:app",
        host="0.0.0.0",
        port=8007,
        reload=True,
        log_level="info"
    )
