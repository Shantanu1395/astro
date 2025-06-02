"""
Comprehensive Vedic Astrology API
Exposes ALL data from Vedic Calculator, Analysis, and Prediction engines
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, date, time

# Import models
from src.models.models import BirthData, LocationData, VedicChart, DashaPeriod

# Import services
from src.services.comprehensive_prediction_service import ComprehensivePredictionService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Comprehensive Vedic Astrology API",
    description="Complete API exposing ALL Vedic analysis components and data",
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

# Initialize comprehensive service
comprehensive_service = ComprehensivePredictionService()

# Request/Response Models
class ComprehensiveAnalysisRequest(BaseModel):
    """Request model for comprehensive analysis."""
    birth_data: BirthData
    location_data: Optional[LocationData] = None
    include_all_components: bool = True
    include_divisional_charts: bool = True
    include_timing_analysis: bool = True
    include_remedial_guidance: bool = True
    include_specialized_predictions: bool = True

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
        "service": "comprehensive-vedic-astrology-api",
        "components_available": [
            "VedicCalculator - Core chart calculations",
            "VedicAnalyzer - Personality and relationship analysis", 
            "VedicPredictionEngine - AI-powered predictions",
            "DivisionalAnalyzer - All divisional charts (D1-D60)",
            "CurrentInfluenceAnalyzer - Current transits and influences",
            "AdvancedTimingCalculator - Timing predictions and muhurta",
            "PlanetaryCombinationDescriptions - Detailed yoga descriptions",
            "CareerPredictionEngine - Career analysis",
            "RelationshipPredictionEngine - Relationship analysis",
            "HealthPredictionEngine - Health analysis",
            "FinancialPredictionEngine - Financial analysis",
            "SpiritualPredictionEngine - Spiritual analysis"
        ]
    }

@app.options("/api/comprehensive-analysis")
async def comprehensive_analysis_options():
    """Handle CORS preflight for comprehensive analysis."""
    return {"message": "OK"}

@app.post("/api/comprehensive-analysis", response_model=ComprehensiveAnalysisResponse)
async def create_comprehensive_analysis(request: ComprehensiveAnalysisRequest):
    """
    Generate comprehensive astrological analysis using ALL available components.
    
    This endpoint provides the most complete analysis possible, including:
    
    **Core Components:**
    - Complete Vedic chart calculation (VedicCalculator)
    - All planetary positions, houses, nakshatras
    - Current dasha periods and timing
    - Planetary strength calculations
    
    **Analysis Components:**
    - Complete personality analysis (VedicAnalyzer)
    - All planetary relationships and aspects
    - Comprehensive yoga identification and analysis
    - Behavioral patterns and life themes
    
    **Divisional Charts:**
    - All major divisional charts (D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60)
    - Varga Bala calculations
    - Divisional chart analysis and insights
    
    **Current Influences:**
    - Real-time planetary transits
    - Current lunar phase and effects
    - Monthly and daily influences
    - Transit-natal interactions
    
    **Timing Analysis:**
    - Advanced dasha calculations
    - Favorable and challenging periods
    - Muhurta analysis
    - Event timing predictions
    
    **Specialized Predictions:**
    - Career analysis and timing
    - Relationship compatibility and timing
    - Health analysis and recommendations
    - Financial prospects and timing
    - Spiritual path and practices
    
    **Remedial Guidance:**
    - Gemstone recommendations
    - Mantra and yantra therapy
    - Lifestyle modifications
    - Timing for remedies
    
    **AI Predictions:**
    - LLM-powered interpretations
    - Contextual analysis
    - Personalized guidance
    """
    try:
        logger.info(f"Creating comprehensive analysis for {request.birth_data.name}")
        start_time = datetime.now()
        
        # Generate complete analysis using all components
        complete_analysis = await comprehensive_service.generate_complete_analysis(
            request.birth_data, 
            request.location_data
        )
        
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds() * 1000
        
        # Create response metadata
        response_metadata = {
            "request_processed_at": end_time.isoformat(),
            "total_processing_time_ms": total_time,
            "components_included": complete_analysis.get("metadata", {}).get("analysis_components", []),
            "data_completeness": complete_analysis.get("metadata", {}).get("data_completeness", "Unknown"),
            "confidence_score": complete_analysis.get("metadata", {}).get("confidence_score", 0.0),
            "api_version": "2.0.0",
            "birth_data": {
                "name": request.birth_data.name,
                "birth_date": request.birth_data.birth_date.isoformat(),
                "birth_time": request.birth_data.birth_time.isoformat(),
                "birth_location": request.birth_data.birth_location
            }
        }
        
        response = ComprehensiveAnalysisResponse(
            success=True,
            data=complete_analysis,
            metadata=response_metadata
        )
        
        logger.info(f"Comprehensive analysis completed in {total_time:.2f}ms")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating comprehensive analysis: {e}")
        return ComprehensiveAnalysisResponse(
            success=False,
            data={},
            metadata={"error_occurred_at": datetime.now().isoformat()},
            error=str(e)
        )

@app.get("/api/analysis-components")
async def get_analysis_components():
    """Get detailed information about all available analysis components."""
    return {
        "core_components": {
            "vedic_calculator": {
                "description": "Core Vedic chart calculations using Swiss Ephemeris",
                "capabilities": [
                    "Planetary position calculations",
                    "House system calculations", 
                    "Nakshatra and pada calculations",
                    "Dasha period calculations",
                    "Planetary strength analysis",
                    "Aspect calculations"
                ],
                "accuracy": "Professional grade using Swiss Ephemeris",
                "coordinate_system": "Sidereal (Lahiri Ayanamsa)"
            },
            "vedic_analyzer": {
                "description": "Comprehensive Vedic analysis and interpretation",
                "capabilities": [
                    "Personality trait analysis",
                    "Planetary relationship analysis",
                    "Yoga identification and analysis",
                    "Behavioral pattern analysis",
                    "Life theme identification",
                    "Compatibility analysis"
                ],
                "analysis_depth": "Deep psychological and spiritual insights",
                "traditional_basis": "Classical Vedic texts and principles"
            },
            "prediction_engine": {
                "description": "AI-powered prediction generation",
                "capabilities": [
                    "LLM-based interpretations",
                    "Contextual analysis",
                    "Personalized guidance",
                    "Multiple prediction types",
                    "Timing predictions"
                ],
                "ai_models": ["OpenAI GPT", "Ollama (local)", "Fallback (rule-based)"],
                "prediction_accuracy": "High confidence with traditional validation"
            }
        },
        "specialized_analyzers": {
            "divisional_analyzer": {
                "description": "Complete divisional chart analysis",
                "charts_supported": [
                    "D1 (Rashi) - Overall life",
                    "D2 (Hora) - Wealth", 
                    "D3 (Drekkana) - Siblings",
                    "D4 (Chaturthamsa) - Fortune",
                    "D7 (Saptamsa) - Children",
                    "D9 (Navamsa) - Marriage & Dharma",
                    "D10 (Dasamsa) - Career",
                    "D12 (Dvadasamsa) - Parents",
                    "D16 (Shodasamsa) - Vehicles",
                    "D20 (Vimsamsa) - Spirituality",
                    "D24 (Chaturvimsamsa) - Learning",
                    "D27 (Bhamsa) - Strength",
                    "D30 (Trimsamsa) - Misfortunes",
                    "D40 (Khavedamsa) - Maternal",
                    "D45 (Akshavedamsa) - Character",
                    "D60 (Shashtyamsa) - Karma"
                ],
                "analysis_features": ["Varga Bala", "Divisional yogas", "Specialized predictions"]
            },
            "current_influences": {
                "description": "Real-time planetary influences and transits",
                "capabilities": [
                    "Current planetary transits",
                    "Lunar phase analysis",
                    "Daily influence calculations",
                    "Monthly theme analysis",
                    "Transit-natal interactions",
                    "Eclipse effects"
                ],
                "update_frequency": "Real-time calculations"
            },
            "advanced_timing": {
                "description": "Advanced timing calculations and muhurta",
                "capabilities": [
                    "Ashtakavarga calculations",
                    "Shadbala calculations",
                    "Muhurta analysis",
                    "Favorable period identification",
                    "Event timing predictions",
                    "Remedial timing"
                ],
                "calculation_methods": "Traditional Vedic timing systems"
            }
        },
        "specialized_engines": {
            "career_engine": {
                "focus": "Professional life and career guidance",
                "analysis_areas": ["Suitable professions", "Career timing", "Business potential", "Professional growth"]
            },
            "relationship_engine": {
                "focus": "Relationships and compatibility",
                "analysis_areas": ["Marriage compatibility", "Relationship timing", "Partnership analysis", "Family dynamics"]
            },
            "health_engine": {
                "focus": "Health and wellness guidance", 
                "analysis_areas": ["Health vulnerabilities", "Constitutional analysis", "Preventive measures", "Healing recommendations"]
            },
            "financial_engine": {
                "focus": "Wealth and financial prospects",
                "analysis_areas": ["Wealth indicators", "Financial timing", "Investment guidance", "Money management"]
            },
            "spiritual_engine": {
                "focus": "Spiritual path and practices",
                "analysis_areas": ["Spiritual inclinations", "Meditation practices", "Dharmic path", "Moksha indicators"]
            }
        },
        "data_coverage": {
            "total_data_points": "1000+",
            "planetary_analysis": "Complete analysis for all 9 planets",
            "house_analysis": "Detailed analysis for all 12 houses", 
            "yoga_combinations": "100+ yoga combinations identified",
            "divisional_charts": "16 major divisional charts analyzed",
            "timing_predictions": "Multiple timing systems integrated",
            "remedial_guidance": "Comprehensive remedy recommendations"
        }
    }

@app.get("/api/sample-analysis")
async def get_sample_analysis():
    """Get a sample analysis to understand the data structure."""
    sample_birth_data = BirthData(
        name="Sample User",
        birth_date=date(1990, 6, 15),
        birth_time=time(14, 30),
        birth_location="Mumbai, India"
    )
    
    try:
        # Generate sample analysis
        sample_analysis = await comprehensive_service.generate_complete_analysis(sample_birth_data)
        
        # Return structure overview instead of full data
        return {
            "message": "Sample analysis structure",
            "data_structure": {
                "metadata": "Analysis metadata and timing information",
                "chart_data": "Complete Vedic chart from VedicCalculator",
                "planetary_analysis": "Comprehensive planetary analysis from VedicAnalyzer", 
                "yogas_analysis": "All yoga combinations with descriptions",
                "divisional_analysis": "All divisional charts (D1-D60)",
                "current_influences": "Real-time transits and influences",
                "timing_analysis": "Advanced timing and muhurta calculations",
                "personality_analysis": "Complete personality profile",
                "specialized_predictions": "Career, health, relationship, financial, spiritual",
                "remedial_guidance": "Comprehensive remedy recommendations",
                "ai_predictions": "LLM-powered interpretations",
                "advanced_calculations": "Ashtakavarga, Shadbala, etc."
            },
            "sample_metadata": sample_analysis.get("metadata", {}),
            "note": "Use POST /api/comprehensive-analysis with your birth data to get complete analysis"
        }
        
    except Exception as e:
        return {"error": f"Error generating sample: {e}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.comprehensive_api:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        log_level="info"
    )
