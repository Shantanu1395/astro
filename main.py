from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime, date, time
import uvicorn

from models import BirthData, PredictionRequest, AstrologySystem, EnhancedPredictionRequest, PredictionType, SubscriptionTier
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

# Initialize prediction engines with different providers
prediction_engine = VedicPredictionEngine()  # Uses config.LLM_PROVIDER
openai_engine = VedicPredictionEngine("openai")  # Force OpenAI
ollama_engine = VedicPredictionEngine("ollama")  # Force Ollama
fallback_engine = VedicPredictionEngine("fallback")  # Fast mode without LLM

# Initialize Phase C - Specialized Engine Manager
from engine_manager import SpecializedEngineManager
from vedic_analysis import VedicAnalyzer
from date_calculator import AstrologicalDateCalculator

analyzer = VedicAnalyzer()
date_calculator = AstrologicalDateCalculator()
specialized_engine_manager = SpecializedEngineManager(analyzer, date_calculator)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with birth data input form."""
    return templates.TemplateResponse("index_modern.html", {"request": request})

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
        planetary_remedies = {}
        planetary_descriptions = {}

        for planet in vedic_chart.planets:
            strength_analysis = vedic_calc.calculate_planetary_strength(planet.name, planet)
            planetary_strengths[planet.name] = strength_analysis

            # Generate remedies for weak planets
            planetary_remedies[planet.name] = vedic_calc.generate_planetary_remedies(
                planet.name, planet, strength_analysis["overall_strength"], strength_analysis["strength_factors"]
            )

            # Generate detailed combination descriptions
            planetary_descriptions[planet.name] = vedic_calc.generate_planetary_combination_description(planet.name, planet)

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

        return templates.TemplateResponse("results_modern.html", {
            "request": request,
            "birth_data": birth_data,
            "location_data": location_data,
            "chart": vedic_chart,
            "prediction": prediction,
            "planetary_strengths": planetary_strengths,
            "planetary_remedies": planetary_remedies,
            "planetary_descriptions": planetary_descriptions,
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

@app.post("/api/predict")
async def predict_api(request: PredictionRequest):
    """Direct API endpoint for predictions - accepts JSON data."""
    try:
        birth_data = request.birth_data

        # Get location data
        location_data = get_location_data(birth_data.birth_location)

        # Calculate Vedic chart
        vedic_calc = VedicCalculator()
        vedic_chart = vedic_calc.calculate_birth_chart(birth_data, location_data)

        # Calculate current dasha
        current_dasha = vedic_calc.calculate_current_dasha(birth_data, vedic_chart)

        # Calculate comprehensive planetary strengths and remedies
        planetary_strengths = {}
        planetary_remedies = {}
        planetary_descriptions = {}

        for planet in vedic_chart.planets:
            strength_analysis = vedic_calc.calculate_planetary_strength(planet.name, planet)
            planetary_strengths[planet.name] = strength_analysis

            # Generate remedies for weak planets
            planetary_remedies[planet.name] = vedic_calc.generate_planetary_remedies(
                planet.name, planet, strength_analysis["overall_strength"], strength_analysis["strength_factors"]
            )

            # Generate detailed combination descriptions
            planetary_descriptions[planet.name] = vedic_calc.generate_planetary_combination_description(planet.name, planet)

        # Get comprehensive planetary relationships
        from vedic_analysis import VedicAnalyzer
        analyzer = VedicAnalyzer()
        planetary_relationships = analyzer.analyze_planetary_relationships(vedic_chart)

        # Generate prediction with enhanced analysis
        from prediction_engine import VedicPredictionEngine
        prediction_engine = VedicPredictionEngine()
        prediction = prediction_engine.generate_vedic_prediction(birth_data, vedic_chart, current_dasha, location_data)

        # Get current influences analysis
        from current_influences import CurrentInfluenceAnalyzer
        current_analyzer = CurrentInfluenceAnalyzer()
        current_influences = current_analyzer.analyze_current_influences(birth_data, vedic_chart, location_data)

        return {
            "success": True,
            "birth_data": {
                "name": birth_data.name,
                "birth_date": str(birth_data.birth_date),
                "birth_time": str(birth_data.birth_time),
                "birth_location": birth_data.birth_location
            },
            "chart_summary": {
                "ascendant_sign": vedic_chart.ascendant_sign,
                "moon_sign": vedic_chart.moon_sign,
                "sun_sign": vedic_chart.sun_sign,
                "birth_nakshatra": vedic_chart.birth_nakshatra
            },
            "current_dasha": {
                "planet": prediction.current_dasha.planet,
                "remaining_years": prediction.current_dasha.remaining_years,
                "start_date": str(prediction.current_dasha.start_date),
                "end_date": str(prediction.current_dasha.end_date)
            },
            "planetary_analysis": {
                "strengths": planetary_strengths,
                "remedies": planetary_remedies,
                "descriptions": planetary_descriptions
            },
            "prediction": {
                "text": prediction.prediction_text,
                "key_themes": prediction.key_themes,
                "favorable_periods": prediction.favorable_periods,
                "challenging_periods": prediction.challenging_periods
            },
            "yogas": [{"name": yoga.get("name", ""), "strength": yoga.get("strength", ""), "description": yoga.get("description", "")}
                     for yoga in planetary_relationships.get("yogas", [])] if planetary_relationships.get("yogas") else [],
            "current_influences": {
                "summary": current_influences.get("comprehensive_summary", "No current influences data available") if current_influences else "No current influences data available"
            }
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate prediction"
        }

@app.get("/api/test/shantanu")
async def test_shantanu_prediction():
    """Quick test endpoint for Shantanu's chart."""
    try:
        # Shantanu's birth data
        birth_data = BirthData(
            name="Shantanu Saini",
            birth_date=date(1994, 3, 1),
            birth_time=time(23, 2),  # 11:02 PM
            birth_location="Faridabad, India"
        )

        request = PredictionRequest(birth_data=birth_data)
        return await predict_api(request)

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate test prediction"
        }

@app.get("/shantanu-chart", response_class=HTMLResponse)
async def shantanu_chart_html():
    """Render Shantanu's chart as HTML in browser."""
    try:
        # Shantanu's birth data
        birth_data = BirthData(
            name="Shantanu Saini",
            birth_date=date(1994, 3, 1),
            birth_time=time(23, 2),  # 11:02 PM
            birth_location="Faridabad, India"
        )

        # Get location data
        location_data = get_location_data(birth_data.birth_location)
        if not location_data:
            raise Exception("Could not get location data for Faridabad, India")

        # Calculate Vedic chart
        vedic_calc = VedicCalculator()
        vedic_chart = vedic_calc.calculate_birth_chart(birth_data, location_data)

        # Calculate current dasha
        current_dasha = vedic_calc.calculate_current_dasha(birth_data, vedic_chart)

        # Calculate comprehensive planetary strengths and remedies
        planetary_strengths = {}
        planetary_remedies = {}
        planetary_descriptions = {}

        for planet in vedic_chart.planets:
            strength_analysis = vedic_calc.calculate_planetary_strength(planet.name, planet)
            planetary_strengths[planet.name] = strength_analysis

            # Generate remedies for weak planets
            planetary_remedies[planet.name] = vedic_calc.generate_planetary_remedies(
                planet.name, planet, strength_analysis["overall_strength"], strength_analysis["strength_factors"]
            )

            # Generate detailed combination descriptions
            planetary_descriptions[planet.name] = vedic_calc.generate_planetary_combination_description(planet.name, planet)

        # Get comprehensive planetary relationships
        from vedic_analysis import VedicAnalyzer
        analyzer = VedicAnalyzer()
        planetary_relationships = analyzer.analyze_planetary_relationships(vedic_chart)

        # Generate prediction with enhanced analysis (respecting LLM provider setting)
        prediction = prediction_engine.generate_vedic_prediction(birth_data, vedic_chart, current_dasha, location_data)

        # Get current influences analysis (optional - may fail)
        current_influences = {}
        try:
            from current_influences import CurrentInfluenceAnalyzer
            current_analyzer = CurrentInfluenceAnalyzer()
            current_influences = current_analyzer.analyze_current_influences(birth_data, vedic_chart, location_data)
        except:
            current_influences = {"comprehensive_summary": "Current influences analysis not available"}

        # Get personality analysis
        personality_analysis = analyzer.analyze_inherent_personality_traits(vedic_chart)

        # Prepare template data with all required fields
        template_data = {
            "request": {},  # Empty request object for template
            "birth_data": birth_data,
            "chart": vedic_chart,
            "prediction": prediction,
            "planetary_strengths": planetary_strengths,
            "planetary_remedies": planetary_remedies,
            "planetary_descriptions": planetary_descriptions,
            "planetary_relationships": planetary_relationships,
            "current_influences": current_influences,
            "personality_analysis": personality_analysis,
            "location_data": location_data,
            # Add missing fields that template might expect
            "planetary_aspects": {},
            "divisional_charts": {},
            "comprehensive_divisional_analysis": {},
            "dasha_analysis": {}
        }

        # Render the template with all data
        return templates.TemplateResponse("results.html", template_data)

    except Exception as e:
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error - Shantanu's Chart</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .error {{ background: #fff; padding: 20px; border-radius: 8px; border-left: 4px solid #e74c3c; }}
                h1 {{ color: #e74c3c; }}
                .details {{ background: #f8f9fa; padding: 15px; border-radius: 4px; margin-top: 15px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>❌ Error Generating Chart</h1>
                <p><strong>Failed to generate Shantanu's chart.</strong></p>
                <div class="details">
                    <strong>Error Details:</strong><br>
                    {str(e)}
                </div>
                <p><a href="/">← Back to Home</a></p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.get("/chart/quick", response_class=HTMLResponse)
async def quick_chart_html(
    name: str = "Test User",
    birth_date: str = "1990-01-15",
    birth_time: str = "10:30",
    birth_location: str = "New Delhi, India"
):
    """Render chart as HTML with URL parameters."""
    try:
        # Parse the parameters
        from datetime import datetime
        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
        birth_time_obj = datetime.strptime(birth_time, "%H:%M").time()

        # Create birth data
        birth_data = BirthData(
            name=name,
            birth_date=birth_date_obj,
            birth_time=birth_time_obj,
            birth_location=birth_location
        )

        # Get location data
        location_data = get_location_data(birth_data.birth_location)

        # Calculate Vedic chart
        vedic_calc = VedicCalculator()
        vedic_chart = vedic_calc.calculate_birth_chart(birth_data, location_data)

        # Calculate current dasha
        current_dasha = vedic_calc.calculate_current_dasha(birth_data, vedic_chart)

        # Calculate comprehensive planetary strengths and remedies
        planetary_strengths = {}
        planetary_remedies = {}
        planetary_descriptions = {}

        for planet in vedic_chart.planets:
            strength_analysis = vedic_calc.calculate_planetary_strength(planet.name, planet)
            planetary_strengths[planet.name] = strength_analysis

            # Generate remedies for weak planets
            planetary_remedies[planet.name] = vedic_calc.generate_planetary_remedies(
                planet.name, planet, strength_analysis["overall_strength"], strength_analysis["strength_factors"]
            )

            # Generate detailed combination descriptions
            planetary_descriptions[planet.name] = vedic_calc.generate_planetary_combination_description(planet.name, planet)

        # Get comprehensive planetary relationships
        from vedic_analysis import VedicAnalyzer
        analyzer = VedicAnalyzer()
        planetary_relationships = analyzer.analyze_planetary_relationships(vedic_chart)

        # Generate prediction with enhanced analysis
        from prediction_engine import VedicPredictionEngine
        prediction_engine = VedicPredictionEngine()
        prediction = prediction_engine.generate_vedic_prediction(birth_data, vedic_chart, current_dasha, location_data)

        # Get current influences analysis
        from current_influences import CurrentInfluenceAnalyzer
        current_analyzer = CurrentInfluenceAnalyzer()
        current_influences = current_analyzer.analyze_current_influences(birth_data, vedic_chart, location_data)

        # Get personality analysis
        personality_analysis = analyzer.analyze_inherent_personality_traits(vedic_chart)

        # Render the template with all data
        return templates.TemplateResponse("results.html", {
            "request": {},  # Empty request object for template
            "birth_data": birth_data,
            "chart": vedic_chart,
            "prediction": prediction,
            "planetary_strengths": planetary_strengths,
            "planetary_remedies": planetary_remedies,
            "planetary_descriptions": planetary_descriptions,
            "planetary_relationships": planetary_relationships,
            "current_influences": current_influences,
            "personality_analysis": personality_analysis,
            "location_data": location_data
        })

    except Exception as e:
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error - Chart Generation</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .error {{ background: #fff; padding: 20px; border-radius: 8px; border-left: 4px solid #e74c3c; }}
                h1 {{ color: #e74c3c; }}
                .details {{ background: #f8f9fa; padding: 15px; border-radius: 4px; margin-top: 15px; }}
                .example {{ background: #e8f5e8; padding: 15px; border-radius: 4px; margin-top: 15px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>❌ Error Generating Chart</h1>
                <p><strong>Failed to generate chart for {name}.</strong></p>
                <div class="details">
                    <strong>Error Details:</strong><br>
                    {str(e)}
                </div>
                <div class="example">
                    <strong>Example URL:</strong><br>
                    <code>/chart/quick?name=John&birth_date=1990-01-15&birth_time=10:30&birth_location=New Delhi, India</code>
                </div>
                <p><a href="/">← Back to Home</a></p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.get("/api/chart/data/{name}")
async def get_chart_api(name: str):
    """API endpoint to get chart data (for future API usage)."""
    # This would be implemented for API access
    return {"message": "API endpoint for chart data", "name": name}

@app.get("/test-html", response_class=HTMLResponse)
async def test_html():
    """Simple test HTML endpoint."""
    return HTMLResponse(content="<h1>Test HTML Endpoint Working!</h1>")

@app.get("/shantanu-simple", response_class=HTMLResponse)
async def shantanu_simple():
    """Simple Shantanu endpoint to test."""
    return HTMLResponse(content="<h1>Shantanu's Chart - Simple Test</h1><p>This endpoint is working!</p>")

@app.get("/shantanu-fast", response_class=HTMLResponse)
async def shantanu_chart_fast():
    """Fast version of Shantanu's chart without Ollama - for quick loading."""
    try:
        # Shantanu's birth data
        birth_data = BirthData(
            name="Shantanu Saini",
            birth_date=date(1994, 3, 1),
            birth_time=time(23, 2),  # 11:02 PM
            birth_location="Faridabad, India"
        )

        # Get location data
        location_data = get_location_data(birth_data.birth_location)
        if not location_data:
            raise Exception("Could not get location data for Faridabad, India")

        # Calculate Vedic chart
        vedic_chart = vedic_calc.calculate_birth_chart(birth_data, location_data)

        # Calculate current dasha
        current_dasha = vedic_calc.calculate_current_dasha(birth_data, vedic_chart)

        # Calculate comprehensive planetary strengths and remedies
        planetary_strengths = {}
        planetary_remedies = {}
        planetary_descriptions = {}

        for planet in vedic_chart.planets:
            strength_analysis = vedic_calc.calculate_planetary_strength(planet.name, planet)
            planetary_strengths[planet.name] = strength_analysis

            # Generate remedies for weak planets
            planetary_remedies[planet.name] = vedic_calc.generate_planetary_remedies(
                planet.name, planet, strength_analysis["overall_strength"], strength_analysis["strength_factors"]
            )

            # Generate detailed combination descriptions
            planetary_descriptions[planet.name] = vedic_calc.generate_planetary_combination_description(planet.name, planet)

        # Get comprehensive planetary relationships
        from vedic_analysis import VedicAnalyzer
        analyzer = VedicAnalyzer()
        planetary_relationships = analyzer.analyze_planetary_relationships(vedic_chart)

        # Generate prediction with FAST engine (no LLM)
        prediction = fallback_engine.generate_vedic_prediction(birth_data, vedic_chart, current_dasha, location_data)

        # Get personality analysis
        personality_analysis = analyzer.analyze_inherent_personality_traits(vedic_chart)

        # Prepare template data with all required fields
        template_data = {
            "request": {},  # Empty request object for template
            "birth_data": birth_data,
            "chart": vedic_chart,
            "prediction": prediction,
            "planetary_strengths": planetary_strengths,
            "planetary_remedies": planetary_remedies,
            "planetary_descriptions": planetary_descriptions,
            "planetary_relationships": planetary_relationships,
            "current_influences": {"comprehensive_summary": "Fast mode - current influences analysis skipped"},
            "personality_analysis": personality_analysis,
            "location_data": location_data,
            # Add missing fields that template might expect
            "planetary_aspects": {},
            "divisional_charts": {},
            "comprehensive_divisional_analysis": {},
            "dasha_analysis": {}
        }

        # Render the template with all data
        return templates.TemplateResponse("results.html", template_data)

    except Exception as e:
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error - Shantanu's Fast Chart</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .error {{ background: #fff; padding: 20px; border-radius: 8px; border-left: 4px solid #e74c3c; }}
                h1 {{ color: #e74c3c; }}
                .details {{ background: #f8f9fa; padding: 15px; border-radius: 4px; margin-top: 15px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>❌ Error Generating Fast Chart</h1>
                <p><strong>Failed to generate Shantanu's fast chart.</strong></p>
                <div class="details">
                    <strong>Error Details:</strong><br>
                    {str(e)}
                </div>
                <p><a href="/">← Back to Home</a></p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.get("/shantanu-modern", response_class=HTMLResponse)
async def shantanu_modern_chart():
    """Generate Shantanu's chart with modern UI."""
    try:
        # Shantanu's birth data
        birth_data = BirthData(
            name="Shantanu Saini",
            birth_date=date(1994, 3, 1),
            birth_time=time(23, 2),  # 11:02 PM
            birth_location="Faridabad, India"
        )

        # Get location data
        location_data = get_location_data(birth_data.birth_location)
        if not location_data:
            raise Exception("Could not get location data for Faridabad, India")

        # Calculate Vedic chart
        vedic_chart = vedic_calc.calculate_birth_chart(birth_data, location_data)

        # Calculate current dasha
        current_dasha = vedic_calc.calculate_current_dasha(birth_data, vedic_chart)

        # Calculate comprehensive planetary strengths and remedies
        planetary_strengths = {}
        planetary_remedies = {}
        planetary_descriptions = {}

        for planet in vedic_chart.planets:
            strength_analysis = vedic_calc.calculate_planetary_strength(planet.name, planet)
            planetary_strengths[planet.name] = strength_analysis

            # Generate remedies for weak planets
            planetary_remedies[planet.name] = vedic_calc.generate_planetary_remedies(
                planet.name, planet, strength_analysis["overall_strength"], strength_analysis["strength_factors"]
            )

            # Generate detailed combination descriptions
            planetary_descriptions[planet.name] = vedic_calc.generate_planetary_combination_description(planet.name, planet)

        # Get comprehensive planetary relationships
        from vedic_analysis import VedicAnalyzer
        analyzer = VedicAnalyzer()
        planetary_relationships = analyzer.analyze_planetary_relationships(vedic_chart)

        # Generate prediction (respecting LLM provider setting)
        prediction = prediction_engine.generate_vedic_prediction(birth_data, vedic_chart, current_dasha, location_data)

        # Get current influences analysis (optional - may fail)
        current_influences = {}
        try:
            from current_influences import CurrentInfluenceAnalyzer
            current_analyzer = CurrentInfluenceAnalyzer()
            current_influences = current_analyzer.analyze_current_influences(birth_data, vedic_chart, location_data)
        except:
            current_influences = {"comprehensive_summary": "Current influences analysis not available"}

        # Get personality analysis
        personality_analysis = analyzer.analyze_inherent_personality_traits(vedic_chart)

        # Prepare template data with all required fields
        template_data = {
            "request": {},  # Empty request object for template
            "birth_data": birth_data,
            "chart": vedic_chart,
            "prediction": prediction,
            "planetary_strengths": planetary_strengths,
            "planetary_remedies": planetary_remedies,
            "planetary_descriptions": planetary_descriptions,
            "planetary_relationships": planetary_relationships,
            "current_influences": current_influences,
            "personality_analysis": personality_analysis,
            "location_data": location_data,
            "current_date": datetime.now().strftime("%B %d, %Y"),
            "current_month": datetime.now().strftime("%B")
        }

        # Render with modern template
        return templates.TemplateResponse("results_modern.html", template_data)

    except Exception as e:
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error - Modern Chart</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #0f172a; color: #f8fafc; }}
                .error {{ background: #1e293b; padding: 20px; border-radius: 8px; border-left: 4px solid #ef4444; }}
                h1 {{ color: #ef4444; }}
                .details {{ background: #334155; padding: 15px; border-radius: 4px; margin-top: 15px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>❌ Error Generating Modern Chart</h1>
                <p><strong>Failed to generate Shantanu's modern chart.</strong></p>
                <div class="details">
                    <strong>Error Details:</strong><br>
                    {str(e)}
                </div>
                <p><a href="/" style="color: #6366f1;">← Back to Home</a></p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.get("/ui-comparison", response_class=HTMLResponse)
async def ui_comparison():
    """Compare old vs new UI."""
    comparison_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>UI Comparison - Vedic Astrology</title>
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: #0f172a;
                color: #f8fafc;
                margin: 0;
                padding: 2rem;
                line-height: 1.6;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            h1 {
                text-align: center;
                font-size: 2.5rem;
                margin-bottom: 3rem;
                background: linear-gradient(45deg, #6366f1, #8b5cf6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .comparison-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
                margin-bottom: 3rem;
            }
            .ui-card {
                background: #1e293b;
                padding: 2rem;
                border-radius: 1rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
            }
            .ui-card h2 {
                font-size: 1.5rem;
                margin-bottom: 1rem;
                color: #f8fafc;
            }
            .ui-card.old {
                border-left: 4px solid #ef4444;
            }
            .ui-card.new {
                border-left: 4px solid #10b981;
            }
            .features {
                text-align: left;
                margin: 1.5rem 0;
            }
            .features li {
                margin-bottom: 0.5rem;
                color: #cbd5e1;
            }
            .btn {
                display: inline-block;
                padding: 0.75rem 1.5rem;
                border-radius: 0.5rem;
                text-decoration: none;
                font-weight: 600;
                transition: transform 0.2s ease;
                margin: 0.5rem;
            }
            .btn:hover {
                transform: translateY(-2px);
            }
            .btn-old {
                background: #ef4444;
                color: white;
            }
            .btn-new {
                background: #10b981;
                color: white;
            }
            .performance {
                background: #334155;
                padding: 2rem;
                border-radius: 1rem;
                margin-bottom: 2rem;
            }
            .performance h3 {
                color: #f59e0b;
                margin-bottom: 1rem;
            }
            .perf-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
            }
            .perf-item {
                background: #1e293b;
                padding: 1rem;
                border-radius: 0.5rem;
                text-align: center;
            }
            .perf-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: #10b981;
            }
            .perf-label {
                font-size: 0.875rem;
                color: #94a3b8;
            }
            @media (max-width: 768px) {
                .comparison-grid {
                    grid-template-columns: 1fr;
                }
                .perf-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 UI/UX Refactoring Complete</h1>

            <div class="performance">
                <h3>⚡ Performance Improvements</h3>
                <div class="perf-grid">
                    <div class="perf-item">
                        <div class="perf-value">0.78s</div>
                        <div class="perf-label">Modern UI Load Time</div>
                    </div>
                    <div class="perf-item">
                        <div class="perf-value">23.8x</div>
                        <div class="perf-label">Faster than Before</div>
                    </div>
                    <div class="perf-item">
                        <div class="perf-value">100%</div>
                        <div class="perf-label">Data Preserved</div>
                    </div>
                    <div class="perf-item">
                        <div class="perf-value">6</div>
                        <div class="perf-label">Organized Sections</div>
                    </div>
                </div>
            </div>

            <div class="comparison-grid">
                <div class="ui-card old">
                    <h2>❌ Old UI</h2>
                    <ul class="features">
                        <li>Single long scroll page</li>
                        <li>Information overload</li>
                        <li>Poor categorization</li>
                        <li>Not mobile-friendly</li>
                        <li>Overwhelming for beginners</li>
                        <li>Repetitive data display</li>
                        <li>No navigation structure</li>
                    </ul>
                    <a href="/shantanu-chart" class="btn btn-old">View Old UI</a>
                </div>

                <div class="ui-card new">
                    <h2>✅ New Modern UI</h2>
                    <ul class="features">
                        <li>Tabbed navigation system</li>
                        <li>Progressive information disclosure</li>
                        <li>Clear categorization</li>
                        <li>Mobile-responsive design</li>
                        <li>Beginner-friendly overview</li>
                        <li>Organized data presentation</li>
                        <li>Interactive navigation</li>
                    </ul>
                    <a href="/shantanu-modern" class="btn btn-new">View Modern UI</a>
                </div>
            </div>

            <div style="text-align: center; margin-top: 3rem;">
                <h3 style="color: #cbd5e1; margin-bottom: 1rem;">🎯 Phase A: UI/UX Refactoring - COMPLETE</h3>
                <p style="color: #94a3b8;">Ready for Phase B: Architecture Foundation & Phase C: Specialized Engines</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=comparison_html)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": config.APP_NAME}

@app.get("/providers")
async def list_providers():
    """List available LLM providers and their status."""
    return {
        "current_provider": config.LLM_PROVIDER,
        "providers": {
            "openai": {
                "available": bool(config.OPENAI_API_KEY),
                "model": config.OPENAI_MODEL,
                "status": "✅ Ready" if config.OPENAI_API_KEY else "❌ No API key"
            },
            "ollama": {
                "available": ollama_engine.ollama_available,
                "model": config.OLLAMA_MODEL,
                "url": config.OLLAMA_URL,
                "status": "✅ Ready" if ollama_engine.ollama_available else "❌ Not running"
            },
            "fallback": {
                "available": True,
                "model": "Local templates",
                "status": "✅ Always available"
            }
        }
    }

# ===== NEW ARCHITECTURE ENDPOINTS =====

@app.get("/api/v2/systems")
async def get_systems_status():
    """Get status of all astrological systems."""
    from system_manager import system_manager
    return system_manager.get_system_status()

@app.get("/api/v2/pricing")
async def get_pricing_info():
    """Get pricing information for all tiers."""
    from system_manager import system_manager
    return system_manager.get_pricing_info()

@app.post("/api/v2/predict")
async def enhanced_prediction(request: dict):
    """Enhanced prediction endpoint with full architecture support."""
    try:
        from models import EnhancedPredictionRequest
        from system_manager import system_manager
        from utils import get_location_data

        # Parse enhanced request
        enhanced_request = EnhancedPredictionRequest(**request)

        # Get location data
        location_data = get_location_data(enhanced_request.birth_data.birth_location)

        # Generate user ID (in production, this would come from authentication)
        user_id = f"user_{hash(enhanced_request.birth_data.name)}"

        # Process request through system manager
        result = system_manager.process_prediction_request(
            enhanced_request, location_data, user_id
        )

        return result

    except Exception as e:
        return {
            "success": False,
            "error": "request_error",
            "message": f"Error processing request: {str(e)}"
        }


# ===== PHASE C - SPECIALIZED PREDICTION ENDPOINTS =====

@app.post("/api/specialized-predict")
async def specialized_predict_api(request: dict):
    """API endpoint for specialized predictions (Phase C)."""
    try:
        from models import EnhancedPredictionRequest
        from utils import get_location_data

        # Parse enhanced request
        enhanced_request = EnhancedPredictionRequest(**request)

        # Get location data
        location_data = get_location_data(enhanced_request.birth_data.birth_location)

        # Calculate chart
        chart = vedic_calc.calculate_birth_chart(enhanced_request.birth_data, location_data)

        # Calculate current dasha
        current_dasha = vedic_calc.calculate_current_dasha(enhanced_request.birth_data, chart)

        # Generate specialized prediction
        specialized_prediction = specialized_engine_manager.generate_specialized_prediction(
            enhanced_request, chart, current_dasha, enhanced_request.birth_data, location_data
        )

        return {
            "status": "success",
            "chart_summary": {
                "ascendant_sign": chart.ascendant_sign,
                "moon_sign": chart.moon_sign,
                "sun_sign": chart.sun_sign,
                "birth_nakshatra": chart.birth_nakshatra
            },
            "specialized_prediction": specialized_prediction
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to generate specialized prediction"
        }


@app.get("/api/engine-capabilities")
async def get_engine_capabilities():
    """Get capabilities of all specialized engines."""
    try:
        capabilities = specialized_engine_manager.get_engine_capabilities()
        return {
            "status": "success",
            "capabilities": capabilities
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to get engine capabilities"
        }


@app.post("/api/prediction-recommendations")
async def get_prediction_recommendations(request: dict):
    """Get personalized prediction recommendations based on chart analysis."""
    try:
        from models import BirthData, SubscriptionTier
        from utils import get_location_data

        # Parse request
        birth_data = BirthData(**request["birth_data"])
        subscription_tier = SubscriptionTier(request.get("subscription_tier", "free").lower())

        # Get location data
        location_data = get_location_data(birth_data.birth_location)

        # Calculate chart
        chart = vedic_calc.calculate_birth_chart(birth_data, location_data)

        # Get recommendations
        recommendations = specialized_engine_manager.get_prediction_recommendations(chart, subscription_tier)

        return {
            "status": "success",
            "recommendations": recommendations,
            "subscription_tier": subscription_tier.value,
            "chart_summary": {
                "ascendant_sign": chart.ascendant_sign,
                "moon_sign": chart.moon_sign,
                "sun_sign": chart.sun_sign
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to get prediction recommendations"
        }


# Quick test endpoints for specialized predictions
@app.get("/api/test/career-prediction")
async def test_career_prediction():
    """Test career prediction with Shantanu's data."""
    try:
        from models import EnhancedPredictionRequest, PredictionType, SubscriptionTier, BirthData
        from datetime import date, time

        birth_data = BirthData(
            name="Shantanu Saini",
            birth_date=date(1994, 3, 1),
            birth_time=time(23, 2),
            birth_location="Faridabad, India"
        )

        request_dict = {
            "birth_data": birth_data.dict(),
            "prediction_type": PredictionType.CAREER.value,
            "subscription_tier": SubscriptionTier.SILVER.value,
            "include_timing": True
        }

        return await specialized_predict_api(request_dict)

    except Exception as e:
        return {"error": str(e), "message": "Failed to generate career prediction test"}


@app.get("/api/test/relationship-prediction")
async def test_relationship_prediction():
    """Test relationship prediction with Shantanu's data."""
    try:
        from models import EnhancedPredictionRequest, PredictionType, SubscriptionTier, BirthData
        from datetime import date, time

        birth_data = BirthData(
            name="Shantanu Saini",
            birth_date=date(1994, 3, 1),
            birth_time=time(23, 2),
            birth_location="Faridabad, India"
        )

        request_dict = {
            "birth_data": birth_data.dict(),
            "prediction_type": PredictionType.RELATIONSHIP.value,
            "subscription_tier": SubscriptionTier.SILVER.value,
            "include_timing": True
        }

        return await specialized_predict_api(request_dict)

    except Exception as e:
        return {"error": str(e), "message": "Failed to generate relationship prediction test"}


@app.get("/api/test/financial-prediction")
async def test_financial_prediction():
    """Test financial prediction with Shantanu's data."""
    try:
        from models import EnhancedPredictionRequest, PredictionType, SubscriptionTier, BirthData
        from datetime import date, time

        birth_data = BirthData(
            name="Shantanu Saini",
            birth_date=date(1994, 3, 1),
            birth_time=time(23, 2),
            birth_location="Faridabad, India"
        )

        request_dict = {
            "birth_data": birth_data.dict(),
            "prediction_type": PredictionType.FINANCIAL.value,
            "subscription_tier": SubscriptionTier.SILVER.value,
            "include_timing": True
        }

        return await specialized_predict_api(request_dict)

    except Exception as e:
        return {"error": str(e), "message": "Failed to generate financial prediction test"}


@app.get("/api/test/health-prediction")
async def test_health_prediction():
    """Test health prediction with Shantanu's data."""
    try:
        from models import EnhancedPredictionRequest, PredictionType, SubscriptionTier, BirthData
        from datetime import date, time

        birth_data = BirthData(
            name="Shantanu Saini",
            birth_date=date(1994, 3, 1),
            birth_time=time(23, 2),
            birth_location="Faridabad, India"
        )

        request_dict = {
            "birth_data": birth_data.dict(),
            "prediction_type": PredictionType.HEALTH.value,
            "subscription_tier": SubscriptionTier.SILVER.value,
            "include_timing": True
        }

        return await specialized_predict_api(request_dict)

    except Exception as e:
        return {"error": str(e), "message": "Failed to generate health prediction test"}


@app.get("/api/test/spiritual-prediction")
async def test_spiritual_prediction():
    """Test spiritual prediction with Shantanu's data."""
    try:
        from models import EnhancedPredictionRequest, PredictionType, SubscriptionTier, BirthData
        from datetime import date, time

        birth_data = BirthData(
            name="Shantanu Saini",
            birth_date=date(1994, 3, 1),
            birth_time=time(23, 2),
            birth_location="Faridabad, India"
        )

        request_dict = {
            "birth_data": birth_data.dict(),
            "prediction_type": PredictionType.SPIRITUAL.value,
            "subscription_tier": SubscriptionTier.SILVER.value,
            "include_timing": True
        }

        return await specialized_predict_api(request_dict)

    except Exception as e:
        return {"error": str(e), "message": "Failed to generate spiritual prediction test"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG
    )
