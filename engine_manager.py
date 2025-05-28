"""
Specialized Engine Manager for Phase C Implementation
Coordinates all specialized prediction engines and routing
"""

from typing import Dict, List, Any, Optional, Type
from datetime import datetime

from models import (
    EnhancedPredictionRequest, VedicChart, DashaPeriod,
    PredictionType, SubscriptionTier, BirthData, LocationData
)
from specialized_engines import (
    BaseSpecializedEngine, CareerPredictionEngine, RelationshipPredictionEngine,
    HealthPredictionEngine, FinancialPredictionEngine, SpiritualPredictionEngine,
    TimeframePredictionEngine, SpecializedPrediction
)
from advanced_timing import AdvancedTimingCalculator
from vedic_analysis import VedicAnalyzer
from date_calculator import AstrologicalDateCalculator
from pricing_system import PricingEngine


class SpecializedEngineManager:
    """Manager for all specialized prediction engines."""

    def __init__(self, analyzer: VedicAnalyzer, date_calculator: AstrologicalDateCalculator):
        self.analyzer = analyzer
        self.date_calculator = date_calculator
        self.advanced_timing = AdvancedTimingCalculator()
        self.pricing_system = PricingEngine()

        # Initialize all specialized engines
        self.engines = self._initialize_engines()

        # Engine routing configuration
        self.engine_routing = self._configure_engine_routing()

    def _initialize_engines(self) -> Dict[str, BaseSpecializedEngine]:
        """Initialize all specialized prediction engines."""
        engines = {
            "career": CareerPredictionEngine(self.analyzer, self.date_calculator),
            "relationship": RelationshipPredictionEngine(self.analyzer, self.date_calculator),
            "health": HealthPredictionEngine(self.analyzer, self.date_calculator),
            "financial": FinancialPredictionEngine(self.analyzer, self.date_calculator),
            "spiritual": SpiritualPredictionEngine(self.analyzer, self.date_calculator),
            "timeframe": TimeframePredictionEngine(self.analyzer, self.date_calculator)
        }
        return engines

    def _configure_engine_routing(self) -> Dict[PredictionType, str]:
        """Configure which engine handles which prediction type."""
        routing = {
            # Specialized area predictions
            PredictionType.CAREER: "career",
            PredictionType.RELATIONSHIP: "relationship",
            PredictionType.HEALTH: "health",
            PredictionType.FINANCIAL: "financial",
            PredictionType.SPIRITUAL: "spiritual",
            PredictionType.EDUCATION: "career",  # Education uses career engine

            # Timeframe predictions
            PredictionType.DAILY: "timeframe",
            PredictionType.WEEKLY: "timeframe",
            PredictionType.MONTHLY: "timeframe",
            PredictionType.YEARLY: "timeframe",

            # Life phase predictions
            PredictionType.LIFE_PHASES: "spiritual",  # Life phases use spiritual engine
            PredictionType.CURRENT_PERIOD: "timeframe"  # Current period uses timeframe engine
        }
        return routing

    def generate_specialized_prediction(self, request: EnhancedPredictionRequest,
                                      chart: VedicChart, current_dasha: DashaPeriod,
                                      birth_data: BirthData, location_data: LocationData = None) -> Dict[str, Any]:
        """Generate specialized prediction based on request type."""

        # Validate subscription tier
        if not self._validate_subscription_access(request):
            return self._create_access_denied_response(request)

        # Route to appropriate engine
        engine_key = self.engine_routing.get(request.prediction_type)
        if not engine_key:
            return self._create_unsupported_type_response(request)

        engine = self.engines[engine_key]

        # Generate specialized prediction
        try:
            specialized_prediction = engine.generate_prediction(request, chart, current_dasha)

            # Enhance with advanced timing if requested
            if request.include_timing:
                timing_analysis = self._generate_advanced_timing(
                    request, chart, current_dasha, birth_data, location_data
                )
                specialized_prediction.advanced_timing = timing_analysis

            # Add pricing information
            pricing_info = self.pricing_system.get_tier_features(request.subscription_tier)

            # Format response
            response = self._format_specialized_response(
                specialized_prediction, request, pricing_info
            )

            return response

        except Exception as e:
            return self._create_error_response(request, str(e))

    def _validate_subscription_access(self, request: EnhancedPredictionRequest) -> bool:
        """Validate if subscription tier has access to specialized predictions."""

        # Free tier only gets basic current period predictions
        if request.subscription_tier == SubscriptionTier.FREE:
            return request.prediction_type == PredictionType.CURRENT_PERIOD

        # Silver tier gets most specialized predictions
        if request.subscription_tier == SubscriptionTier.SILVER:
            allowed_types = [
                PredictionType.CURRENT_PERIOD, PredictionType.DAILY, PredictionType.WEEKLY,
                PredictionType.MONTHLY, PredictionType.YEARLY, PredictionType.CAREER,
                PredictionType.RELATIONSHIP, PredictionType.HEALTH, PredictionType.FINANCIAL
            ]
            return request.prediction_type in allowed_types

        # Gold tier gets all predictions
        if request.subscription_tier == SubscriptionTier.GOLD:
            return True

        return False

    def _generate_advanced_timing(self, request: EnhancedPredictionRequest, chart: VedicChart,
                                current_dasha: DashaPeriod, birth_data: BirthData,
                                location_data: LocationData = None) -> Dict[str, Any]:
        """Generate advanced timing analysis for the prediction."""

        timing_analysis = {}

        # Generate timing based on prediction type
        if request.prediction_type == PredictionType.CAREER:
            timing_analysis = self.advanced_timing.calculate_career_timing(
                chart, current_dasha, timeframe_years=5
            )
        elif request.prediction_type == PredictionType.RELATIONSHIP:
            timing_analysis = self.advanced_timing.calculate_relationship_timing(
                chart, current_dasha, timeframe_years=3
            )
        elif request.prediction_type == PredictionType.FINANCIAL:
            timing_analysis = self.advanced_timing.calculate_financial_timing(
                chart, current_dasha, timeframe_years=5
            )
        elif request.prediction_type == PredictionType.HEALTH:
            timing_analysis = self.advanced_timing.calculate_health_timing(
                chart, current_dasha, timeframe_years=2
            )
        else:
            # General timing analysis for other types
            timing_analysis = {
                "general_timing": "Advanced timing analysis available for specialized predictions",
                "recommendation": "Upgrade to specialized prediction for detailed timing"
            }

        return timing_analysis

    def _format_specialized_response(self, prediction: SpecializedPrediction,
                                   request: EnhancedPredictionRequest,
                                   pricing_info: Dict[str, Any]) -> Dict[str, Any]:
        """Format the specialized prediction response."""

        # Get the full prediction data
        prediction_dict = prediction.to_dict()

        response = {
            "prediction_type": request.prediction_type.value,
            "specialization_level": prediction.specialization_level.value,
            "generated_at": prediction.generated_at.isoformat(),
            "confidence_score": prediction.confidence_score,
            "subscription_tier": request.subscription_tier.value,
            "pricing_info": pricing_info,
            "prediction_data": prediction_dict
        }

        # Extract key fields that frontend expects at top level
        if hasattr(prediction, 'prediction_text') and prediction.prediction_text:
            response["prediction_text"] = prediction.prediction_text
        if hasattr(prediction, 'key_themes') and prediction.key_themes:
            response["key_themes"] = prediction.key_themes
        if hasattr(prediction, 'favorable_periods') and prediction.favorable_periods:
            response["favorable_periods"] = prediction.favorable_periods
        if hasattr(prediction, 'challenging_periods') and prediction.challenging_periods:
            response["challenging_periods"] = prediction.challenging_periods

        # Add specialized analysis if available
        if hasattr(prediction, 'career_analysis'):
            response["career_analysis"] = prediction.career_analysis
        if hasattr(prediction, 'relationship_analysis'):
            response["relationship_analysis"] = prediction.relationship_analysis
        if hasattr(prediction, 'health_analysis'):
            response["health_analysis"] = prediction.health_analysis
        if hasattr(prediction, 'financial_analysis'):
            response["financial_analysis"] = prediction.financial_analysis
        if hasattr(prediction, 'spiritual_analysis'):
            response["spiritual_analysis"] = prediction.spiritual_analysis
        if hasattr(prediction, 'daily_analysis'):
            response["daily_analysis"] = prediction.daily_analysis
        if hasattr(prediction, 'weekly_analysis'):
            response["weekly_analysis"] = prediction.weekly_analysis
        if hasattr(prediction, 'monthly_analysis'):
            response["monthly_analysis"] = prediction.monthly_analysis
        if hasattr(prediction, 'yearly_analysis'):
            response["yearly_analysis"] = prediction.yearly_analysis

        # Add timing analysis if available
        if hasattr(prediction, 'timing_analysis'):
            response["timing_analysis"] = prediction.timing_analysis
        if hasattr(prediction, 'advanced_timing'):
            response["advanced_timing"] = prediction.advanced_timing

        # Add guidance if available
        if hasattr(prediction, 'guidance'):
            response["guidance"] = prediction.guidance

        return response

    def _create_access_denied_response(self, request: EnhancedPredictionRequest) -> Dict[str, Any]:
        """Create response for access denied due to subscription tier."""
        return {
            "error": "access_denied",
            "message": f"Subscription tier {request.subscription_tier.value} does not have access to {request.prediction_type.value} predictions",
            "required_tier": "silver" if request.prediction_type != PredictionType.SPIRITUAL else "gold",
            "upgrade_url": "/upgrade",
            "available_predictions": self._get_available_predictions(request.subscription_tier)
        }

    def _create_unsupported_type_response(self, request: EnhancedPredictionRequest) -> Dict[str, Any]:
        """Create response for unsupported prediction type."""
        return {
            "error": "unsupported_type",
            "message": f"Prediction type {request.prediction_type.value} is not yet supported",
            "supported_types": list(self.engine_routing.keys()),
            "suggestion": "Try one of the supported prediction types"
        }

    def _create_error_response(self, request: EnhancedPredictionRequest, error_message: str) -> Dict[str, Any]:
        """Create error response for prediction generation failures."""
        return {
            "error": "prediction_failed",
            "message": f"Failed to generate {request.prediction_type.value} prediction: {error_message}",
            "timestamp": datetime.now().isoformat(),
            "request_id": f"{request.prediction_type.value}_{datetime.now().timestamp()}"
        }

    def _get_available_predictions(self, tier: SubscriptionTier) -> List[str]:
        """Get list of available prediction types for a subscription tier."""
        if tier == SubscriptionTier.FREE:
            return ["current_period"]
        elif tier == SubscriptionTier.SILVER:
            return ["current_period", "yearly", "monthly", "career", "relationship", "health", "financial"]
        else:  # GOLD
            return [pt.value for pt in PredictionType]

    def get_engine_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Get capabilities of all specialized engines."""
        capabilities = {}

        for engine_name, engine in self.engines.items():
            capabilities[engine_name] = {
                "specialization_areas": engine.get_specialization_areas(),
                "supported_tiers": [tier.value for tier in engine.supported_tiers],
                "engine_type": engine.__class__.__name__
            }

        return capabilities

    def get_prediction_recommendations(self, chart: VedicChart,
                                     subscription_tier: SubscriptionTier) -> List[Dict[str, Any]]:
        """Get personalized prediction recommendations based on chart analysis."""
        recommendations = []

        # Analyze chart to suggest most relevant predictions
        chart_analysis = self._analyze_chart_focus_areas(chart)

        for area, strength in chart_analysis.items():
            if strength > 0.7:  # Strong indication for this area
                prediction_type = self._map_area_to_prediction_type(area)
                if prediction_type and self._is_type_available(prediction_type, subscription_tier):
                    recommendations.append({
                        "prediction_type": prediction_type.value,
                        "area": area,
                        "strength": strength,
                        "reason": f"Strong {area} indicators in your chart",
                        "priority": "high" if strength > 0.8 else "medium"
                    })

        return sorted(recommendations, key=lambda x: x["strength"], reverse=True)

    def _analyze_chart_focus_areas(self, chart: VedicChart) -> Dict[str, float]:
        """Analyze chart to determine focus areas with strength scores."""
        focus_areas = {}

        # Career analysis (10th house strength)
        tenth_house_planets = [p for p in chart.planets if p.house == 10]
        career_strength = 0.8 if tenth_house_planets else 0.6
        focus_areas["career"] = career_strength

        # Relationship analysis (7th house strength)
        seventh_house_planets = [p for p in chart.planets if p.house == 7]
        relationship_strength = 0.8 if seventh_house_planets else 0.6
        focus_areas["relationships"] = relationship_strength

        # Health analysis (6th house strength)
        sixth_house_planets = [p for p in chart.planets if p.house == 6]
        health_strength = 0.7 if sixth_house_planets else 0.5
        focus_areas["health"] = health_strength

        # Wealth analysis (2nd and 11th house strength)
        wealth_planets = [p for p in chart.planets if p.house in [2, 11]]
        wealth_strength = 0.8 if wealth_planets else 0.6
        focus_areas["wealth"] = wealth_strength

        # Spirituality analysis (9th and 12th house strength)
        spiritual_planets = [p for p in chart.planets if p.house in [9, 12]]
        spiritual_strength = 0.7 if spiritual_planets else 0.5
        focus_areas["spirituality"] = spiritual_strength

        return focus_areas

    def _map_area_to_prediction_type(self, area: str) -> Optional[PredictionType]:
        """Map chart analysis area to prediction type."""
        area_mapping = {
            "career": PredictionType.CAREER,
            "relationships": PredictionType.RELATIONSHIP,
            "health": PredictionType.HEALTH,
            "wealth": PredictionType.FINANCIAL,
            "spirituality": PredictionType.SPIRITUAL,
            "education": PredictionType.EDUCATION
        }
        return area_mapping.get(area.lower())

    def _is_type_available(self, prediction_type: PredictionType, tier: SubscriptionTier) -> bool:
        """Check if prediction type is available for subscription tier."""
        available_types = self._get_available_predictions(tier)
        return prediction_type.value in available_types
