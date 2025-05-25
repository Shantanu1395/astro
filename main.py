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

        # Generate prediction with enhanced analysis
        prediction = prediction_engine.generate_vedic_prediction(birth_data, vedic_chart, current_dasha, location_data)

        return templates.TemplateResponse("results.html", {
            "request": request,
            "birth_data": birth_data,
            "location_data": location_data,
            "chart": vedic_chart,
            "prediction": prediction
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
