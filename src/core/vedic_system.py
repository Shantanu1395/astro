"""
Vedic Astrology System Implementation.

This module implements the Vedic astrological system following the new
multi-system architecture, integrating with existing vedic_calculator.py
and prediction_engine.py components.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from src.models.models import (
    BirthData, LocationData, AstrologySystem, PredictionType,
    EnhancedPredictionRequest
)
from src.core.astrological_systems import (
    AstrologicalCalculator, PredictionEngine, RemedialSystem,
    AstrologicalSystemInterface, Chart, Prediction
)
from src.core.vedic_calculator import VedicCalculator
from src.core.prediction_engine import VedicPredictionEngine as LegacyVedicPredictionEngine
from src.core.vedic_analysis import VedicAnalyzer


class VedicChartAdapter(Chart):
    """Vedic-specific chart implementation."""

    def __init__(self, vedic_chart_data, birth_data: BirthData):
        super().__init__(
            system=AstrologySystem.VEDIC,
            birth_data=birth_data
        )
        self.vedic_data = vedic_chart_data

    class Config:
        arbitrary_types_allowed = True

    def get_planetary_positions(self) -> List[Dict[str, Any]]:
        """Get planetary positions in Vedic format."""
        return [
            {
                "name": planet.name,
                "longitude": planet.longitude,
                "sign": planet.sign,
                "house": planet.house,
                "nakshatra": planet.nakshatra,
                "nakshatra_pada": planet.nakshatra_pada
            }
            for planet in self.vedic_data.planets
        ]

    def get_houses(self) -> Dict[int, Any]:
        """Get house system in Vedic format."""
        return {
            house_num: {
                "planets": planets,
                "sign": self._get_house_sign(house_num),
                "lord": self._get_house_lord(house_num)
            }
            for house_num, planets in self.vedic_data.houses.items()
        }

    def _get_house_sign(self, house_num: int) -> str:
        """Get sign of a house (simplified - would need proper calculation)."""
        # This is a placeholder - proper implementation would calculate house signs
        return "Aries"  # Placeholder

    def _get_house_lord(self, house_num: int) -> str:
        """Get lord of a house (simplified - would need proper calculation)."""
        # This is a placeholder - proper implementation would calculate house lords
        return "Mars"  # Placeholder


class VedicPredictionAdapter(Prediction):
    """Vedic-specific prediction implementation."""

    def __init__(self, vedic_prediction_data, chart: VedicChartAdapter):
        super().__init__(
            system=AstrologySystem.VEDIC,
            prediction_type=PredictionType.CURRENT_PERIOD,  # Default, can be overridden
            chart=chart.dict(),
            prediction_text=vedic_prediction_data.prediction_text,
            key_themes=vedic_prediction_data.key_themes
        )
        self.vedic_data = vedic_prediction_data

    class Config:
        arbitrary_types_allowed = True

    def get_timing_information(self) -> Dict[str, Any]:
        """Get Vedic timing information."""
        return {
            "current_dasha": {
                "planet": self.vedic_data.current_dasha.planet,
                "remaining_years": self.vedic_data.current_dasha.remaining_years,
                "end_date": self.vedic_data.current_dasha.end_date.isoformat()
            },
            "upcoming_dasha": {
                "planet": self.vedic_data.upcoming_dasha.planet,
                "start_date": self.vedic_data.upcoming_dasha.start_date.isoformat()
            },
            "favorable_periods": self.vedic_data.favorable_periods,
            "challenging_periods": self.vedic_data.challenging_periods
        }

    def get_remedial_suggestions(self) -> List[Dict[str, Any]]:
        """Get Vedic remedial suggestions."""
        # This would integrate with the existing remedial system
        return [
            {
                "type": "mantra",
                "description": "Chant planetary mantras",
                "timing": "Daily during sunrise"
            },
            {
                "type": "gemstone",
                "description": "Wear appropriate gemstone",
                "timing": "After proper consultation"
            }
        ]


class VedicCalculatorAdapter(AstrologicalCalculator):
    """Adapter for existing VedicCalculator to new architecture."""

    def __init__(self):
        super().__init__(AstrologySystem.VEDIC)
        self.vedic_calculator = VedicCalculator()

    def calculate_chart(self, birth_data: BirthData, location_data: LocationData) -> VedicChartAdapter:
        """Calculate Vedic birth chart."""
        vedic_chart_data = self.vedic_calculator.calculate_birth_chart(birth_data, location_data)
        return VedicChartAdapter(vedic_chart_data, birth_data)

    def calculate_current_transits(self, birth_chart: VedicChartAdapter, current_date: datetime) -> Dict[str, Any]:
        """Calculate current Vedic transits."""
        # This would use existing transit calculation logic
        return {
            "transits": [],
            "significant_aspects": [],
            "eclipse_effects": []
        }

    def calculate_planetary_periods(self, birth_chart: VedicChartAdapter) -> List[Dict[str, Any]]:
        """Calculate Vimshottari Dasha periods."""
        current_dasha = self.vedic_calculator.calculate_current_dasha(birth_chart.birth_data)
        return [
            {
                "planet": current_dasha.planet,
                "start_date": current_dasha.start_date.isoformat(),
                "end_date": current_dasha.end_date.isoformat(),
                "level": current_dasha.level,
                "remaining_years": current_dasha.remaining_years
            }
        ]

    def calculate_planetary_strengths(self, birth_chart: VedicChartAdapter) -> Dict[str, float]:
        """Calculate Shadbala planetary strengths."""
        strengths = {}
        for planet in birth_chart.vedic_data.planets:
            # This would use existing strength calculation logic
            strength_data = self.vedic_calculator.calculate_planetary_strength(planet, birth_chart.vedic_data)
            strengths[planet.name] = strength_data.get("overall_strength", 0.5)
        return strengths


class VedicPredictionEngineAdapter(PredictionEngine):
    """Adapter for existing VedicPredictionEngine to new architecture."""

    def __init__(self, calculator: VedicCalculatorAdapter):
        super().__init__(AstrologySystem.VEDIC, calculator)
        self.legacy_engine = LegacyVedicPredictionEngine()
        self.analyzer = VedicAnalyzer()

    def generate_prediction(self, request: EnhancedPredictionRequest, chart: VedicChartAdapter) -> VedicPredictionAdapter:
        """Generate Vedic prediction using existing engine."""
        # Calculate current dasha
        current_dasha = self.calculator.vedic_calculator.calculate_current_dasha(request.birth_data)

        # Use existing prediction engine
        vedic_prediction_data = self.legacy_engine.generate_vedic_prediction(
            request.birth_data,
            chart.vedic_data,
            current_dasha
        )

        return VedicPredictionAdapter(vedic_prediction_data, chart)

    def get_supported_prediction_types(self) -> List[PredictionType]:
        """Get supported Vedic prediction types."""
        return [
            PredictionType.CURRENT_PERIOD,
            PredictionType.YEARLY,
            PredictionType.MONTHLY,
            PredictionType.CAREER,
            PredictionType.RELATIONSHIP,
            PredictionType.HEALTH,
            PredictionType.SPIRITUAL,
            PredictionType.LIFE_PHASES
        ]

    def validate_request(self, request: EnhancedPredictionRequest) -> Tuple[bool, Optional[str]]:
        """Validate Vedic prediction request."""
        if request.system != AstrologySystem.VEDIC:
            return False, "Request is not for Vedic system"

        if request.prediction_type not in self.get_supported_prediction_types():
            return False, f"Prediction type {request.prediction_type.value} not supported"

        return True, None


class VedicRemedialSystem(RemedialSystem):
    """Vedic remedial system implementation."""

    def __init__(self):
        super().__init__(AstrologySystem.VEDIC)
        self.vedic_calculator = VedicCalculator()

    def get_remedies(self, chart: VedicChartAdapter, focus_area: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get Vedic remedial recommendations."""
        remedies = []

        for planet in chart.vedic_data.planets:
            planet_remedies = self.vedic_calculator.calculate_planetary_remedies(planet, chart.vedic_data)
            remedies.append({
                "planet": planet.name,
                "remedies": planet_remedies
            })

        return remedies

    def get_timing_for_remedies(self, chart: VedicChartAdapter, remedies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get optimal timing for Vedic remedies."""
        return {
            "best_days": ["Tuesday", "Thursday", "Sunday"],
            "best_times": ["Sunrise", "Sunset"],
            "avoid_periods": ["Eclipse periods", "Amavasya"]
        }


class VedicSystem(AstrologicalSystemInterface):
    """Complete Vedic astrological system implementation."""

    def __init__(self):
        super().__init__(AstrologySystem.VEDIC)

    def _create_calculator(self) -> VedicCalculatorAdapter:
        """Create Vedic calculator."""
        return VedicCalculatorAdapter()

    def _create_prediction_engine(self) -> VedicPredictionEngineAdapter:
        """Create Vedic prediction engine."""
        return VedicPredictionEngineAdapter(self.calculator)

    def _create_remedial_system(self) -> VedicRemedialSystem:
        """Create Vedic remedial system."""
        return VedicRemedialSystem()

    def _get_system_features(self) -> List[str]:
        """Get Vedic system features."""
        return [
            "Vimshottari Dasha System",
            "Shadbala Planetary Strengths",
            "Comprehensive Yoga Analysis",
            "Divisional Charts (Vargas)",
            "Nakshatra Analysis",
            "Transit Analysis",
            "Remedial Recommendations"
        ]
