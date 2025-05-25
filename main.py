from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime, date, time
import uvicorn

from models import BirthData, PredictionRequest, AstrologySystem
from vedic_calculator import VedicCalculator
from prediction_engine import VedicPredictionEngine
from utils import get_location_data
from config import config

app = FastAPI(title=config.APP_NAME)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize calculators
vedic_calc = VedicCalculator()
prediction_engine = VedicPredictionEngine()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with birth data input form."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(...),
    birth_time: str = Form(...),
    birth_location: str = Form(...)
):
    """Generate astrological prediction based on birth data."""
    try:
        # Parse birth data
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
        birth_time_obj = datetime.strptime(birth_time, "%H:%M").time()

        # Create birth data object
        birth_data = BirthData(
            name=name,
            birth_date=birth_date_obj,
            birth_time=birth_time_obj,
            birth_location=birth_location
        )

        # Get location coordinates
        location_data = get_location_data(birth_location)
        if not location_data:
            raise HTTPException(status_code=400, detail="Could not find location. Please try a different format.")

        # Calculate Vedic chart
        vedic_chart = vedic_calc.calculate_birth_chart(birth_data, location_data)

        # Calculate current dasha
        current_dasha = vedic_calc.calculate_current_dasha(birth_data, vedic_chart)

        # Calculate comprehensive planetary strengths for all planets
        planetary_strengths = {}
        for planet in vedic_chart.planets:
            planetary_strengths[planet.name] = vedic_calc.calculate_planetary_strength(planet.name, planet)

        # Calculate all planetary aspects
        planetary_aspects = vedic_calc.calculate_planetary_aspects(vedic_chart)

        # Calculate comprehensive divisional charts - ALL MAJOR VARGAS
        divisional_charts = {}
        # Primary charts (most important)
        primary_divisions = ["D2", "D3", "D9", "D10", "D12"]
        # Secondary charts (additional insights)
        secondary_divisions = ["D4", "D7", "D16", "D20", "D24", "D30", "D60"]

        # Calculate all divisional charts
        all_divisions = primary_divisions + secondary_divisions
        for division in all_divisions:
            divisional_charts[division] = vedic_calc.calculate_divisional_chart(vedic_chart, division)

        # Get comprehensive divisional analysis
        from divisional_analyzer import DivisionalAnalyzer
        divisional_analyzer = DivisionalAnalyzer()
        comprehensive_divisional_analysis = divisional_analyzer.analyze_comprehensive_divisional_charts(vedic_chart, divisional_charts)

        # Get comprehensive analysis from vedic_analysis.py
        from vedic_analysis import VedicAnalyzer
        analyzer = VedicAnalyzer()

        # Get detailed dasha analysis
        dasha_analysis = analyzer.analyze_dasha_significance(current_dasha, vedic_chart)

        # Get comprehensive planetary relationships
        planetary_relationships = analyzer.analyze_planetary_relationships(vedic_chart)

        # Get comprehensive personality analysis
        personality_analysis = analyzer.analyze_inherent_personality_traits(vedic_chart)

        # Generate prediction with enhanced analysis
        prediction = prediction_engine.generate_vedic_prediction(birth_data, vedic_chart, current_dasha, location_data)

        # COMPREHENSIVE CURRENT INFLUENCES ANALYSIS
        from current_influences import CurrentInfluenceAnalyzer
        current_analyzer = CurrentInfluenceAnalyzer()
        current_influences = current_analyzer.analyze_current_influences(birth_data, vedic_chart, location_data)

        return templates.TemplateResponse("results.html", {
            "request": request,
            "birth_data": birth_data,
            "location_data": location_data,
            "chart": vedic_chart,
            "prediction": prediction,
            "planetary_strengths": planetary_strengths,
            "planetary_aspects": planetary_aspects,
            "divisional_charts": divisional_charts,
            "comprehensive_divisional_analysis": comprehensive_divisional_analysis,
            "dasha_analysis": dasha_analysis,
            "planetary_relationships": planetary_relationships,
            "personality_analysis": personality_analysis,
            "current_influences": current_influences
        })

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.get("/api/chart/{name}")
async def get_chart_api(name: str):
    """API endpoint to get chart data (for future API usage)."""
    # This would be implemented for API access
    return {"message": "API endpoint for chart data", "name": name}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": config.APP_NAME}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG
    )
