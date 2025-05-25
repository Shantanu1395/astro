from pydantic import BaseModel, Field, validator
from datetime import datetime, date, time
from typing import Optional, Dict, List, Any
from enum import Enum

class AstrologySystem(str, Enum):
    VEDIC = "vedic"
    WESTERN = "western"
    CHINESE = "chinese"
    MAYAN = "mayan"

class BirthData(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    birth_date: date = Field(..., description="Birth date")
    birth_time: time = Field(..., description="Birth time")
    birth_location: str = Field(..., min_length=1, description="Birth location (city, country)")
    timezone: Optional[str] = Field(None, description="Timezone (auto-detected if not provided)")
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        if v > date.today():
            raise ValueError('Birth date cannot be in the future')
        if v.year < 1900:
            raise ValueError('Birth date must be after 1900')
        return v

class LocationData(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    timezone: str
    city: str
    country: str

class PlanetPosition(BaseModel):
    name: str
    longitude: float  # Degrees
    latitude: float   # Degrees
    sign: str
    house: int
    nakshatra: Optional[str] = None
    nakshatra_pada: Optional[int] = None

class VedicChart(BaseModel):
    planets: List[PlanetPosition]
    houses: Dict[int, List[str]]  # House number -> planets in that house
    ascendant: float
    ascendant_sign: str
    moon_sign: str
    sun_sign: str
    birth_nakshatra: str
    birth_nakshatra_pada: int

class DashaPeriod(BaseModel):
    planet: str
    start_date: date
    end_date: date
    level: str  # "mahadasha", "antardasha", "pratyantardasha"
    remaining_years: float

class VedicPrediction(BaseModel):
    current_dasha: DashaPeriod
    upcoming_dasha: DashaPeriod
    current_transits: List[str]
    prediction_text: str
    key_themes: List[str]
    favorable_periods: List[str]
    challenging_periods: List[str]

class PredictionRequest(BaseModel):
    birth_data: BirthData
    system: AstrologySystem = AstrologySystem.VEDIC
    prediction_type: str = "current_period"  # "current_period", "yearly", "monthly"
