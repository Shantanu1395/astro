from pydantic import BaseModel, Field, validator
from datetime import datetime, date, time
from typing import Optional, Dict, List, Any, Union
from enum import Enum
from abc import ABC, abstractmethod

class AstrologySystem(str, Enum):
    VEDIC = "vedic"
    WESTERN = "western"
    CHINESE = "chinese"
    MAYAN = "mayan"

class PredictionType(str, Enum):
    """Enhanced prediction types for different focuses and timeframes."""
    CURRENT_PERIOD = "current_period"
    YEARLY = "yearly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    DAILY = "daily"
    LIFE_PHASES = "life_phases"
    CAREER = "career"
    RELATIONSHIP = "relationship"
    HEALTH = "health"
    SPIRITUAL = "spiritual"
    FINANCIAL = "financial"
    EDUCATION = "education"

class SubscriptionTier(str, Enum):
    """Subscription tiers with different feature access levels."""
    FREE = "free"
    SILVER = "silver"
    GOLD = "gold"

class DetailLevel(str, Enum):
    """Level of detail in predictions."""
    BASIC = "basic"
    STANDARD = "standard"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"

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

class CurrentInfluences(BaseModel):
    current_date: str
    lunar_phase: Dict[str, Any]
    month_theme: Dict[str, Any]
    daily_changes: List[str]
    monthly_changes: List[str]
    personal_effects: List[Dict[str, Any]]
    recommendations: List[str]

class VedicPrediction(BaseModel):
    current_dasha: DashaPeriod
    upcoming_dasha: DashaPeriod
    current_transits: List[str]
    prediction_text: str
    key_themes: List[str]
    favorable_periods: List[str]
    challenging_periods: List[str]
    current_influences: Optional[CurrentInfluences] = None

class PredictionRequest(BaseModel):
    birth_data: BirthData
    system: AstrologySystem = AstrologySystem.VEDIC
    prediction_type: str = "current_period"  # "current_period", "yearly", "monthly"

# ===== ENHANCED ARCHITECTURE MODELS =====

class EnhancedPredictionRequest(BaseModel):
    """Enhanced prediction request with full feature support."""
    birth_data: BirthData
    system: AstrologySystem = AstrologySystem.VEDIC
    prediction_type: PredictionType = PredictionType.CURRENT_PERIOD
    specific_question: Optional[str] = Field(None, max_length=500, description="Specific question to focus on")
    focus_area: Optional[str] = Field(None, max_length=100, description="Specific life area to emphasize")
    timeframe: Optional[str] = Field(None, description="Specific timeframe (e.g., 'next 6 months', '2024')")
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    detail_level: DetailLevel = DetailLevel.STANDARD
    include_remedies: bool = True
    include_timing: bool = True
    include_transits: bool = True

class PricingRule(BaseModel):
    """Pricing rules for different tiers and features."""
    tier: SubscriptionTier
    allowed_systems: List[AstrologySystem]
    allowed_prediction_types: List[PredictionType]
    max_requests_per_month: int
    includes_cross_system_analysis: bool
    includes_detailed_timing: bool
    includes_personalized_remedies: bool
    cost_per_request: float = 0.0

class FeatureAccess(BaseModel):
    """Feature access validation for subscription tiers."""
    tier: SubscriptionTier
    can_access_system: bool
    can_access_prediction_type: bool
    can_access_cross_system: bool
    remaining_requests: int
    upgrade_required: bool = False
    upgrade_message: Optional[str] = None

# ===== ABSTRACT BASE CLASSES FOR MULTI-SYSTEM ARCHITECTURE =====

class Chart(BaseModel, ABC):
    """Abstract base class for all astrological charts."""
    system: AstrologySystem
    birth_data: BirthData
    calculation_date: datetime = Field(default_factory=datetime.now)

    @abstractmethod
    def get_planetary_positions(self) -> List[Dict[str, Any]]:
        """Get planetary positions in system-specific format."""
        pass

    @abstractmethod
    def get_houses(self) -> Dict[int, Any]:
        """Get house system in system-specific format."""
        pass

class Prediction(BaseModel, ABC):
    """Abstract base class for all predictions."""
    system: AstrologySystem
    prediction_type: PredictionType
    chart: Dict[str, Any]  # Chart data in JSON format
    prediction_text: str
    key_themes: List[str]
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.8)
    generated_at: datetime = Field(default_factory=datetime.now)

    @abstractmethod
    def get_timing_information(self) -> Dict[str, Any]:
        """Get timing-specific information for this prediction."""
        pass

    @abstractmethod
    def get_remedial_suggestions(self) -> List[Dict[str, Any]]:
        """Get remedial suggestions specific to this system."""
        pass
