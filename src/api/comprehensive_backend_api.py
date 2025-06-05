"""
Comprehensive Backend API - Exposing ALL Vedic Analysis Data
Works with existing project structure and exposes complete data from all components
"""

import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, date, time

# Import existing components with new structure
from src.core.vedic_calculator import VedicCalculator
from src.core.vedic_analysis import VedicAnalyzer
from src.core.prediction_engine import VedicPredictionEngine
from src.core.divisional_analyzer import DivisionalAnalyzer
from src.core.current_influences import CurrentInfluenceAnalyzer
from src.core.advanced_timing import AdvancedTimingCalculator
from src.core.astrological_meanings import AstrologicalMeanings
from src.services.specialized_engines import (
    CareerPredictionEngine, RelationshipPredictionEngine,
    HealthPredictionEngine, FinancialPredictionEngine, SpiritualPredictionEngine
)
from src.services.engine_manager import SpecializedEngineManager
from src.models.models import BirthData, LocationData, VedicChart, DashaPeriod
from src.utils.date_calculator import AstrologicalDateCalculator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Comprehensive Vedic Astrology Backend API",
    description="Complete backend API exposing ALL Vedic analysis data and components",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize all components
vedic_calculator = VedicCalculator()
vedic_analyzer = VedicAnalyzer()
prediction_engine = VedicPredictionEngine()
divisional_analyzer = DivisionalAnalyzer()
current_influences_analyzer = CurrentInfluenceAnalyzer()
advanced_timing_calculator = AdvancedTimingCalculator()
astrological_meanings = AstrologicalMeanings()
date_calculator = AstrologicalDateCalculator()

# Initialize specialized engines with required parameters
specialized_engine_manager = SpecializedEngineManager(vedic_analyzer, date_calculator)

# Request/Response Models
class ComprehensiveAnalysisRequest(BaseModel):
    """Request model for comprehensive analysis."""
    name: str
    birth_date: str  # YYYY-MM-DD format
    birth_time: str  # HH:MM format
    birth_location: str
    latitude: Optional[float] = 19.0760  # Default Mumbai
    longitude: Optional[float] = 72.8777
    timezone: Optional[str] = "Asia/Kolkata"

class ComprehensiveAnalysisResponse(BaseModel):
    """Response model for comprehensive analysis."""
    success: bool
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    error: Optional[str] = None

# API Endpoints

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "service": "comprehensive-vedic-backend-api",
        "components_initialized": [
            "VedicCalculator",
            "VedicAnalyzer",
            "VedicPredictionEngine",
            "DivisionalAnalyzer",
            "CurrentInfluenceAnalyzer",
            "AdvancedTimingCalculator",
            "SpecializedEngineManager"
        ]
    }

@app.options("/api/comprehensive-analysis")
async def comprehensive_analysis_options():
    """Handle CORS preflight."""
    return {"message": "OK"}

@app.post("/api/comprehensive-analysis", response_model=ComprehensiveAnalysisResponse)
async def create_comprehensive_analysis(request: ComprehensiveAnalysisRequest):
    """
    Generate comprehensive astrological analysis using ALL available components.

    This endpoint exposes complete data from:
    - VedicCalculator: Core chart calculations, planetary positions, houses
    - VedicAnalyzer: Personality analysis, yogas, planetary relationships
    - VedicPredictionEngine: AI-powered predictions and interpretations
    - DivisionalAnalyzer: All divisional charts analysis
    - CurrentInfluenceAnalyzer: Current transits and influences
    - AdvancedTimingCalculator: Timing predictions and muhurta
    - SpecializedEngines: Career, health, relationship, financial, spiritual analysis
    """
    try:
        logger.info(f"Creating comprehensive analysis for {request.name}")
        start_time = datetime.now()

        # 1. Parse birth data
        birth_data = BirthData(
            name=request.name,
            birth_date=date.fromisoformat(request.birth_date),
            birth_time=time.fromisoformat(request.birth_time),
            birth_location=request.birth_location
        )

        location_data = LocationData(
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone,
            city="Mumbai",  # Default city
            country="India"  # Default country
        )

        # 2. CORE CHART CALCULATION (VedicCalculator)
        logger.info("Calculating Vedic chart...")
        vedic_chart = vedic_calculator.calculate_birth_chart(birth_data, location_data)
        current_dasha = vedic_calculator.calculate_current_dasha(birth_data, vedic_chart)
        # Create house analysis from chart data
        house_analysis = {
            "houses": vedic_chart.houses,
            "ascendant": vedic_chart.ascendant_sign,
            "house_lords": {}  # Could be calculated if needed
        }

        # Calculate planetary strengths
        planetary_strengths = {}
        for planet in vedic_chart.planets:
            planetary_strengths[planet.name] = vedic_calculator.calculate_planetary_strength(planet.name, planet)

        # 3. COMPREHENSIVE ANALYSIS (VedicAnalyzer)
        logger.info("Performing Vedic analysis...")
        planetary_relationships = vedic_analyzer.analyze_planetary_relationships(vedic_chart)
        personality_analysis = vedic_analyzer.analyze_inherent_personality_traits(vedic_chart)
        dasha_analysis = vedic_analyzer.analyze_dasha_significance(current_dasha, vedic_chart)

        # Get yogas analysis
        yogas = vedic_analyzer._identify_yogas(vedic_chart)

        # 4. AI PREDICTIONS (VedicPredictionEngine)
        logger.info("Generating AI predictions...")
        ai_prediction = prediction_engine.generate_vedic_prediction(birth_data, vedic_chart, current_dasha, location_data)

        # 5. DIVISIONAL CHARTS ANALYSIS (DivisionalAnalyzer)
        logger.info("Analyzing divisional charts...")
        divisional_charts = {}
        major_divisions = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20"]

        for division in major_divisions:
            try:
                divisional_chart = divisional_analyzer.calculate_divisional_chart(vedic_chart, division)
                divisional_analysis = divisional_analyzer.analyze_divisional_chart(divisional_chart, division)
                divisional_charts[division] = {
                    "chart": divisional_chart,
                    "analysis": divisional_analysis
                }
            except Exception as e:
                logger.warning(f"Error calculating {division}: {e}")
                divisional_charts[division] = {"error": str(e)}

        # 6. CURRENT INFLUENCES (CurrentInfluenceAnalyzer)
        logger.info("Analyzing current influences...")
        try:
            current_influences = current_influences_analyzer.analyze_current_influences(birth_data, vedic_chart, location_data)
        except Exception as e:
            logger.warning(f"Error analyzing current influences: {e}")
            current_influences = {"error": str(e)}

        # 7. ADVANCED TIMING (AdvancedTimingCalculator)
        logger.info("Calculating advanced timing...")
        try:
            timing_analysis = {
                "favorable_periods": advanced_timing_calculator.calculate_favorable_periods(vedic_chart, current_dasha),
                "challenging_periods": advanced_timing_calculator.calculate_challenging_periods(vedic_chart, current_dasha),
                "muhurta_analysis": advanced_timing_calculator.get_current_muhurta_analysis()
            }
        except Exception as e:
            logger.warning(f"Error in timing analysis: {e}")
            timing_analysis = {"error": str(e)}

        # 8. SPECIALIZED PREDICTIONS (SpecializedEngines)
        logger.info("Generating specialized predictions...")
        try:
            specialized_predictions = {
                "career": specialized_engine_manager.generate_career_prediction(birth_data, vedic_chart, current_dasha),
                "relationship": specialized_engine_manager.generate_relationship_prediction(birth_data, vedic_chart, current_dasha),
                "health": specialized_engine_manager.generate_health_prediction(birth_data, vedic_chart, current_dasha),
                "financial": specialized_engine_manager.generate_financial_prediction(birth_data, vedic_chart, current_dasha),
                "spiritual": specialized_engine_manager.generate_spiritual_prediction(birth_data, vedic_chart, current_dasha)
            }
        except Exception as e:
            logger.warning(f"Error in specialized predictions: {e}")
            specialized_predictions = {"error": str(e)}

        # 9. ASTROLOGICAL MEANINGS (AstrologicalMeanings)
        logger.info("Getting astrological meanings...")
        try:
            # Extract key astrological elements
            sun_sign = None
            moon_sign = None
            ascendant_sign = vedic_chart.ascendant_sign
            current_dasha_planet = current_dasha.planet

            # Get sun and moon signs from planets
            for planet in vedic_chart.planets:
                if planet.name == "Sun":
                    sun_sign = planet.sign
                elif planet.name == "Moon":
                    moon_sign = planet.sign

            # Get meanings from astrological meanings service
            astrological_meanings_data = {
                "general_explanations": astrological_meanings.get_general_explanations(),
                "sun_sign": {
                    "sign": sun_sign,
                    "meaning": astrological_meanings.get_sun_sign_meaning(sun_sign) if sun_sign else None
                },
                "moon_sign": {
                    "sign": moon_sign,
                    "meaning": astrological_meanings.get_moon_sign_meaning(moon_sign) if moon_sign else None
                },
                "ascendant": {
                    "sign": ascendant_sign,
                    "meaning": astrological_meanings.get_ascendant_meaning(ascendant_sign) if ascendant_sign else None
                },
                "current_dasha": {
                    "planet": current_dasha_planet,
                    "meaning": astrological_meanings.get_dasha_meaning(current_dasha_planet) if current_dasha_planet else None
                }
            }
        except Exception as e:
            logger.warning(f"Error getting astrological meanings: {e}")
            astrological_meanings_data = {"error": str(e)}

        end_time = datetime.now()
        generation_time = (end_time - start_time).total_seconds() * 1000

        # 10. COMPILE COMPREHENSIVE DATA
        comprehensive_data = {
            # Core chart data from VedicCalculator
            "vedic_chart": {
                "planets": [planet.model_dump() for planet in vedic_chart.planets],
                "houses": vedic_chart.houses,
                "ascendant": vedic_chart.ascendant,
                "ascendant_sign": vedic_chart.ascendant_sign,
                "moon_sign": vedic_chart.moon_sign,
                "sun_sign": vedic_chart.sun_sign,
                "birth_nakshatra": vedic_chart.birth_nakshatra,
                "birth_nakshatra_pada": vedic_chart.birth_nakshatra_pada
            },

            "current_dasha": current_dasha.model_dump(),
            "house_analysis": house_analysis,
            "planetary_strengths": planetary_strengths,

            # Analysis from VedicAnalyzer
            "planetary_relationships": planetary_relationships,
            "personality_analysis": personality_analysis,
            "dasha_analysis": dasha_analysis,
            "yogas": yogas,

            # AI predictions from VedicPredictionEngine
            "ai_prediction": ai_prediction.model_dump(),

            # Divisional charts from DivisionalAnalyzer
            "divisional_charts": divisional_charts,

            # Current influences from CurrentInfluenceAnalyzer
            "current_influences": current_influences,

            # Timing analysis from AdvancedTimingCalculator
            "timing_analysis": timing_analysis,

            # Specialized predictions from SpecializedEngines
            "specialized_predictions": specialized_predictions,

            # Astrological meanings for signs, ascendants, and dashas
            "astrological_meanings": astrological_meanings_data
        }

        # Create response metadata
        response_metadata = {
            "person_name": request.name,
            "birth_date": request.birth_date,
            "birth_time": request.birth_time,
            "birth_location": request.birth_location,
            "generation_time_ms": generation_time,
            "generated_at": end_time.isoformat(),
            "components_used": [
                "VedicCalculator", "VedicAnalyzer", "VedicPredictionEngine",
                "DivisionalAnalyzer", "CurrentInfluenceAnalyzer",
                "AdvancedTimingCalculator", "SpecializedEngines"
            ],
            "data_points_generated": len(str(comprehensive_data)),
            "api_version": "2.0.0"
        }

        logger.info(f"Comprehensive analysis completed in {generation_time:.2f}ms")

        return ComprehensiveAnalysisResponse(
            success=True,
            data=comprehensive_data,
            metadata=response_metadata
        )

    except Exception as e:
        logger.error(f"Error creating comprehensive analysis: {e}")
        return ComprehensiveAnalysisResponse(
            success=False,
            data={},
            metadata={"error_occurred_at": datetime.now().isoformat()},
            error=str(e)
        )

@app.get("/api/components")
async def get_available_components():
    """Get information about all available analysis components."""
    return {
        "core_components": {
            "vedic_calculator": {
                "description": "Core Vedic chart calculations using Swiss Ephemeris",
                "data_provided": [
                    "Planetary positions (longitude, latitude, sign, house, degree)",
                    "House occupancy and analysis",
                    "Nakshatra and pada calculations",
                    "Dasha period calculations",
                    "Planetary strength analysis",
                    "Ascendant, Moon sign, Sun sign"
                ]
            },
            "vedic_analyzer": {
                "description": "Comprehensive Vedic analysis and interpretation",
                "data_provided": [
                    "Personality trait analysis",
                    "Planetary relationship analysis",
                    "Yoga identification and descriptions",
                    "Dasha significance analysis",
                    "Behavioral pattern analysis"
                ]
            },
            "prediction_engine": {
                "description": "AI-powered prediction generation",
                "data_provided": [
                    "AI-generated predictions",
                    "Key life themes",
                    "Favorable and challenging periods",
                    "Current transit analysis"
                ]
            }
        },
        "specialized_analyzers": {
            "divisional_analyzer": {
                "description": "Divisional charts (Vargas) analysis",
                "charts_supported": ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20"],
                "data_provided": ["Divisional chart calculations", "Specialized analysis for each division"]
            },
            "current_influences": {
                "description": "Real-time planetary influences",
                "data_provided": ["Current transits", "Lunar phases", "Daily influences", "Monthly themes"]
            },
            "advanced_timing": {
                "description": "Advanced timing calculations",
                "data_provided": ["Favorable periods", "Challenging periods", "Muhurta analysis"]
            }
        },
        "specialized_engines": {
            "career_engine": "Professional life and career guidance",
            "relationship_engine": "Relationships and compatibility analysis",
            "health_engine": "Health and wellness guidance",
            "financial_engine": "Wealth and financial prospects",
            "spiritual_engine": "Spiritual path and practices"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.comprehensive_backend_api:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
        log_level="info"
    )
