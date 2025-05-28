"""
Specialized Prediction Engines for Different Life Areas and Timeframes
Phase C Implementation - Advanced prediction engines with specialized focus
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date, timedelta
from enum import Enum

from models import (
    BirthData, VedicChart, DashaPeriod, LocationData,
    PredictionType, EnhancedPredictionRequest, SubscriptionTier
)
from vedic_analysis import VedicAnalyzer
from date_calculator import AstrologicalDateCalculator
from current_influences import CurrentInfluenceAnalyzer


class SpecializationLevel(str, Enum):
    """Level of specialization for predictions."""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class SpecializedPrediction:
    """Base class for specialized predictions."""

    def __init__(self, prediction_type: PredictionType, specialization_level: SpecializationLevel):
        self.prediction_type = prediction_type
        self.specialization_level = specialization_level
        self.generated_at = datetime.now()
        self.confidence_score = 0.8

    def to_dict(self) -> Dict[str, Any]:
        """Convert prediction to dictionary format."""
        result = {
            "prediction_type": self.prediction_type.value,
            "specialization_level": self.specialization_level.value,
            "generated_at": self.generated_at.isoformat(),
            "confidence_score": self.confidence_score
        }

        # Add all additional attributes that were set on the prediction
        for attr_name, attr_value in self.__dict__.items():
            if attr_name not in ['prediction_type', 'specialization_level', 'generated_at', 'confidence_score']:
                # Convert datetime objects to ISO format
                if hasattr(attr_value, 'isoformat'):
                    result[attr_name] = attr_value.isoformat()
                else:
                    result[attr_name] = attr_value

        return result


class BaseSpecializedEngine(ABC):
    """Abstract base class for all specialized prediction engines."""

    def __init__(self, analyzer: VedicAnalyzer, date_calculator: AstrologicalDateCalculator):
        self.analyzer = analyzer
        self.date_calculator = date_calculator
        self.supported_tiers = [SubscriptionTier.SILVER, SubscriptionTier.GOLD]

    @abstractmethod
    def generate_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                          current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate specialized prediction."""
        pass

    @abstractmethod
    def get_specialization_areas(self) -> List[str]:
        """Get areas of specialization for this engine."""
        pass

    def validate_subscription_tier(self, tier: SubscriptionTier) -> bool:
        """Check if subscription tier supports this specialized engine."""
        return tier in self.supported_tiers


class CareerPredictionEngine(BaseSpecializedEngine):
    """Specialized engine for career and professional life predictions."""

    def __init__(self, analyzer: VedicAnalyzer, date_calculator: AstrologicalDateCalculator):
        super().__init__(analyzer, date_calculator)
        self.career_houses = [1, 2, 6, 10, 11]  # Key career houses
        self.career_planets = ["Sun", "Mars", "Mercury", "Jupiter", "Saturn"]

        # Import and initialize advanced timing calculator
        from advanced_timing import AdvancedTimingCalculator
        self.advanced_timing = AdvancedTimingCalculator()

    def generate_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                          current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate career-focused prediction."""

        # Analyze career-relevant chart factors
        career_analysis = self._analyze_career_factors(chart, current_dasha)

        # Get career timing
        career_timing = self._calculate_career_timing(chart, current_dasha)

        # Generate career-specific guidance
        career_guidance = self._generate_career_guidance(career_analysis, career_timing)

        prediction = SpecializedPrediction(PredictionType.CAREER, SpecializationLevel.ADVANCED)
        prediction.career_analysis = career_analysis
        prediction.timing_analysis = career_timing
        prediction.guidance = career_guidance
        prediction.confidence_score = self._calculate_career_confidence(chart)

        return prediction

    def _analyze_career_factors(self, chart: VedicChart, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Analyze career-specific astrological factors."""
        analysis = {
            "tenth_house_analysis": self._analyze_tenth_house(chart),
            "career_planet_positions": self._analyze_career_planets(chart),
            "dasha_career_impact": self._analyze_dasha_career_impact(current_dasha, chart),
            "professional_strengths": self._identify_professional_strengths(chart),
            "career_challenges": self._identify_career_challenges(chart),
            "ideal_career_fields": self._suggest_career_fields(chart)
        }
        return analysis

    def _calculate_career_timing(self, chart: VedicChart, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Calculate career-specific timing and opportunities."""
        # Use advanced timing calculator for precise career timing
        advanced_career_timing = self.advanced_timing.calculate_career_timing(chart, current_dasha)

        timing = {
            "current_career_phase": self._get_current_career_phase(current_dasha),
            "upcoming_opportunities": self._calculate_career_opportunities(chart, current_dasha),
            "promotion_periods": self._calculate_promotion_periods(chart),
            "job_change_timing": self._calculate_job_change_timing(chart),
            "business_timing": self._calculate_business_timing(chart),
            "financial_growth_periods": self._calculate_financial_growth_periods(chart)
        }

        # Add advanced timing data
        timing.update(advanced_career_timing)

        return timing

    def _generate_career_guidance(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific career guidance and recommendations."""
        guidance = {
            "immediate_actions": self._get_immediate_career_actions(analysis, timing),
            "skill_development": self._suggest_skill_development(analysis),
            "networking_guidance": self._provide_networking_guidance(timing),
            "investment_advice": self._provide_investment_advice(timing),
            "risk_management": self._provide_risk_management_advice(analysis),
            "long_term_strategy": self._develop_long_term_career_strategy(analysis, timing)
        }
        return guidance

    def get_specialization_areas(self) -> List[str]:
        """Get career specialization areas."""
        return [
            "Professional Growth", "Career Transitions", "Business Ventures",
            "Leadership Development", "Financial Planning", "Skill Development",
            "Industry Analysis", "Promotion Timing", "Job Market Analysis"
        ]

    def _analyze_tenth_house(self, chart: VedicChart) -> Dict[str, Any]:
        """Detailed analysis of 10th house for career insights."""
        tenth_house_planets = [p for p in chart.planets if p.house == 10]

        analysis = {
            "ruling_planet": self._get_tenth_house_ruler(chart),
            "planets_in_tenth": [p.name for p in tenth_house_planets],
            "tenth_house_sign": self._get_tenth_house_sign(chart),
            "career_nature": self._determine_career_nature(tenth_house_planets),
            "authority_potential": self._assess_authority_potential(tenth_house_planets),
            "public_recognition": self._assess_public_recognition_potential(chart)
        }
        return analysis

    def _calculate_career_opportunities(self, chart: VedicChart, current_dasha: DashaPeriod) -> List[Dict[str, Any]]:
        """Calculate upcoming career opportunities with specific dates."""
        opportunities = []
        current_date = date.today()

        # Analyze next 2 years for career opportunities
        for months_ahead in range(0, 24, 3):  # Every 3 months for 2 years
            target_date = current_date + timedelta(days=months_ahead * 30)

            opportunity = self._assess_career_opportunity_at_date(chart, target_date, current_dasha)
            if opportunity["strength"] > 0.6:  # Only include strong opportunities
                opportunities.append(opportunity)

        return opportunities

    def _calculate_career_confidence(self, chart: VedicChart) -> float:
        """Calculate confidence score for career predictions."""
        confidence_factors = []

        # Strong 10th house = higher confidence
        tenth_house_planets = [p for p in chart.planets if p.house == 10]
        if tenth_house_planets:
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.7)

        # Career planets in good positions
        career_planet_strength = self._assess_career_planet_strength(chart)
        confidence_factors.append(career_planet_strength)

        return sum(confidence_factors) / len(confidence_factors)

    # Missing methods for CareerPredictionEngine
    def _get_current_career_phase(self, current_dasha: DashaPeriod) -> str:
        """Get current career phase based on dasha."""
        career_phases = {
            "Jupiter": "Expansion and Growth Phase",
            "Saturn": "Foundation Building Phase",
            "Sun": "Leadership Development Phase",
            "Mars": "Action and Initiative Phase",
            "Mercury": "Communication and Learning Phase"
        }
        return career_phases.get(current_dasha.planet, "General Development Phase")

    def _get_tenth_house_ruler(self, chart: VedicChart) -> str:
        """Get 10th house ruler."""
        # Simplified - would need actual calculation
        return "Saturn"  # Default

    def _get_tenth_house_sign(self, chart: VedicChart) -> str:
        """Get 10th house sign."""
        # Simplified calculation
        return "Capricorn"  # Default

    def _determine_career_nature(self, tenth_house_planets: List) -> str:
        """Determine career nature from 10th house planets."""
        if not tenth_house_planets:
            return "Balanced professional approach"

        planet_influences = {
            "Sun": "Leadership and authority roles",
            "Moon": "Public service and nurturing careers",
            "Mars": "Dynamic and competitive fields",
            "Mercury": "Communication and analytical work",
            "Jupiter": "Teaching, advisory, and wisdom-based careers",
            "Venus": "Creative and aesthetic fields",
            "Saturn": "Structured and disciplined professions"
        }

        primary_planet = tenth_house_planets[0].name if tenth_house_planets else "Sun"
        return planet_influences.get(primary_planet, "Diverse professional interests")

    def _assess_authority_potential(self, tenth_house_planets: List) -> str:
        """Assess authority potential."""
        if not tenth_house_planets:
            return "Moderate authority potential"

        authority_planets = ["Sun", "Mars", "Jupiter", "Saturn"]
        has_authority_planet = any(p.name in authority_planets for p in tenth_house_planets)

        return "High authority potential" if has_authority_planet else "Moderate authority potential"

    def _assess_public_recognition_potential(self, chart: VedicChart) -> str:
        """Assess public recognition potential."""
        # Check for planets in 1st, 10th, or 11th houses
        recognition_houses = [1, 10, 11]
        recognition_planets = [p for p in chart.planets if p.house in recognition_houses]

        if len(recognition_planets) >= 2:
            return "High public recognition potential"
        elif len(recognition_planets) == 1:
            return "Moderate public recognition potential"
        else:
            return "Gradual recognition through consistent effort"

    def _assess_career_opportunity_at_date(self, chart: VedicChart, target_date: date, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Assess career opportunity at specific date."""
        # Simplified calculation
        base_strength = 0.6
        dasha_bonus = 0.1 if current_dasha.planet in ["Jupiter", "Sun", "Mercury"] else 0.0
        seasonal_bonus = 0.1 if target_date.month in [3, 4, 9, 10] else 0.0  # Spring and fall

        total_strength = base_strength + dasha_bonus + seasonal_bonus

        return {
            "date": target_date.isoformat(),
            "strength": min(total_strength, 1.0),
            "factors": {
                "dasha_influence": dasha_bonus,
                "seasonal_timing": seasonal_bonus,
                "base_potential": base_strength
            }
        }

    def _assess_career_planet_strength(self, chart: VedicChart) -> float:
        """Assess career planet strength."""
        career_planets = ["Sun", "Mars", "Mercury", "Jupiter", "Saturn"]
        strong_positions = 0
        total_career_planets = 0

        for planet in chart.planets:
            if planet.name in career_planets:
                total_career_planets += 1
                # Simplified strength assessment
                if planet.house in [1, 4, 7, 10]:  # Angular houses
                    strong_positions += 1

        return strong_positions / total_career_planets if total_career_planets > 0 else 0.5

    def _analyze_career_planets(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze career-relevant planets."""
        career_analysis = {}
        for planet_name in self.career_planets:
            planet = next((p for p in chart.planets if p.name == planet_name), None)
            if planet:
                career_analysis[planet_name] = {
                    "house": planet.house,
                    "sign": planet.sign,
                    "career_influence": self._get_career_influence(planet_name, planet.house)
                }
        return career_analysis

    def _get_career_influence(self, planet_name: str, house: int) -> str:
        """Get career influence of planet in specific house."""
        influences = {
            "Sun": {1: "Leadership roles", 10: "Authority positions", 11: "Recognition and gains"},
            "Mars": {1: "Dynamic action", 6: "Competitive fields", 10: "Executive roles"},
            "Mercury": {3: "Communication", 6: "Analytical work", 10: "Business acumen"},
            "Jupiter": {9: "Teaching/advisory", 10: "Wisdom-based careers", 11: "Prosperity"},
            "Saturn": {6: "Service sectors", 10: "Long-term building", 12: "Behind-scenes work"}
        }
        return influences.get(planet_name, {}).get(house, "General career support")

    def _analyze_dasha_career_impact(self, current_dasha: DashaPeriod, chart: VedicChart) -> Dict[str, Any]:
        """Analyze current dasha impact on career."""
        dasha_planet = current_dasha.planet
        career_impact = {
            "Jupiter": "Expansion, teaching, advisory roles",
            "Saturn": "Building foundations, discipline, long-term projects",
            "Sun": "Leadership opportunities, recognition",
            "Mars": "Dynamic action, competitive advantage",
            "Mercury": "Communication, business development"
        }
        return {
            "current_phase": dasha_planet,
            "career_theme": career_impact.get(dasha_planet, "General career development"),
            "remaining_years": current_dasha.remaining_years,
            "opportunities": f"Focus on {career_impact.get(dasha_planet, 'career growth')} for next {current_dasha.remaining_years:.1f} years"
        }

    def _identify_professional_strengths(self, chart: VedicChart) -> List[str]:
        """Identify professional strengths from chart."""
        strengths = []

        # Analyze 10th house
        tenth_house_planets = [p for p in chart.planets if p.house == 10]
        if tenth_house_planets:
            strengths.append("Natural leadership abilities")

        # Analyze career planets
        for planet in chart.planets:
            if planet.name == "Mercury" and planet.house in [3, 6, 10]:
                strengths.append("Excellent communication skills")
            elif planet.name == "Jupiter" and planet.house in [9, 10, 11]:
                strengths.append("Wisdom and advisory capabilities")
            elif planet.name == "Mars" and planet.house in [1, 6, 10]:
                strengths.append("Dynamic execution abilities")

        return strengths[:5] if strengths else ["Balanced professional approach", "Adaptable skills"]

    def _identify_career_challenges(self, chart: VedicChart) -> List[str]:
        """Identify potential career challenges."""
        challenges = []

        # Check for challenging planetary positions
        for planet in chart.planets:
            if planet.name == "Saturn" and planet.house == 10:
                challenges.append("May face delays in career recognition")
            elif planet.name == "Rahu" and planet.house == 10:
                challenges.append("Unconventional career path with ups and downs")

        return challenges[:3] if challenges else ["Minor timing challenges", "Need for patience"]

    def _suggest_career_fields(self, chart: VedicChart) -> List[str]:
        """Suggest suitable career fields."""
        fields = []

        # Based on 10th house planets
        tenth_house_planets = [p for p in chart.planets if p.house == 10]
        for planet in tenth_house_planets:
            if planet.name == "Jupiter":
                fields.extend(["Education", "Consulting", "Law", "Finance"])
            elif planet.name == "Mercury":
                fields.extend(["Technology", "Communication", "Business", "Writing"])
            elif planet.name == "Mars":
                fields.extend(["Engineering", "Sports", "Military", "Real Estate"])

        return fields[:6] if fields else ["Business", "Technology", "Consulting", "Management"]

    # Add missing timing methods for CareerPredictionEngine
    def _calculate_promotion_periods(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate promotion periods."""
        return [
            {"period": "Q2 2024", "probability": 0.8, "guidance": "Strong promotion potential"},
            {"period": "Q4 2024", "probability": 0.7, "guidance": "Good advancement opportunities"}
        ]

    def _calculate_job_change_timing(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate job change timing."""
        return [
            {"period": "Q3 2024", "favorability": 0.75, "guidance": "Favorable for career transitions"},
            {"period": "Q1 2025", "favorability": 0.8, "guidance": "Excellent timing for new opportunities"}
        ]

    def _calculate_business_timing(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate business timing."""
        return [
            {"period": "Q4 2024", "success_probability": 0.8, "guidance": "Good time to start business ventures"},
            {"period": "Q2 2025", "success_probability": 0.85, "guidance": "Excellent business launch timing"}
        ]

    def _calculate_financial_growth_periods(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate financial growth periods."""
        return [
            {"period": "2024", "growth_potential": 0.75, "guidance": "Steady financial growth expected"},
            {"period": "2025", "growth_potential": 0.85, "guidance": "Strong financial advancement"}
        ]

    def _get_immediate_career_actions(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> List[str]:
        """Get immediate career actions."""
        return [
            "Focus on skill development in your core competencies",
            "Network with industry professionals",
            "Update your professional portfolio",
            "Seek mentorship opportunities",
            "Consider additional certifications"
        ]

    def _suggest_skill_development(self, analysis: Dict[str, Any]) -> List[str]:
        """Suggest skill development areas."""
        return [
            "Leadership and management skills",
            "Digital technology proficiency",
            "Communication and presentation skills",
            "Strategic thinking and planning",
            "Industry-specific expertise"
        ]

    def _provide_networking_guidance(self, timing: Dict[str, Any]) -> List[str]:
        """Provide networking guidance."""
        return [
            "Attend industry conferences and events",
            "Join professional associations",
            "Engage actively on LinkedIn",
            "Seek informational interviews",
            "Participate in professional workshops"
        ]

    def _provide_investment_advice(self, timing: Dict[str, Any]) -> List[str]:
        """Provide investment advice for career."""
        return [
            "Invest in professional development courses",
            "Consider advanced degree or certification",
            "Build a strong professional network",
            "Invest in personal branding",
            "Create multiple income streams"
        ]

    def _provide_risk_management_advice(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide risk management advice."""
        return [
            "Maintain an emergency fund",
            "Diversify your skill set",
            "Build strong professional relationships",
            "Stay updated with industry trends",
            "Have a backup career plan"
        ]

    def _develop_long_term_career_strategy(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> Dict[str, Any]:
        """Develop long-term career strategy."""
        return {
            "5_year_goals": [
                "Achieve senior leadership position",
                "Become industry expert",
                "Build substantial professional network",
                "Increase income by 50-100%"
            ],
            "10_year_vision": [
                "Executive or C-level position",
                "Industry thought leader",
                "Mentor to others",
                "Financial independence"
            ],
            "key_milestones": [
                "Year 1: Skill enhancement and networking",
                "Year 2-3: Promotion or role advancement",
                "Year 4-5: Leadership responsibilities",
                "Year 6-10: Executive development"
            ]
        }


class RelationshipPredictionEngine(BaseSpecializedEngine):
    """Specialized engine for relationship and compatibility predictions."""

    def __init__(self, analyzer: VedicAnalyzer, date_calculator: AstrologicalDateCalculator):
        super().__init__(analyzer, date_calculator)
        self.relationship_houses = [1, 5, 7, 8, 11]  # Key relationship houses
        self.relationship_planets = ["Venus", "Mars", "Moon", "Jupiter"]

    def generate_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                          current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate relationship-focused prediction."""

        # Analyze relationship factors
        relationship_analysis = self._analyze_relationship_factors(chart, current_dasha)

        # Calculate relationship timing
        relationship_timing = self._calculate_relationship_timing(chart, current_dasha)

        # Generate relationship guidance
        relationship_guidance = self._generate_relationship_guidance(relationship_analysis, relationship_timing)

        prediction = SpecializedPrediction(PredictionType.RELATIONSHIP, SpecializationLevel.ADVANCED)
        prediction.relationship_analysis = relationship_analysis
        prediction.timing_analysis = relationship_timing
        prediction.guidance = relationship_guidance
        prediction.confidence_score = self._calculate_relationship_confidence(chart)

        return prediction

    def get_specialization_areas(self) -> List[str]:
        """Get relationship specialization areas."""
        return [
            "Marriage Timing", "Compatibility Analysis", "Relationship Challenges",
            "Love Life", "Partnership Business", "Family Relationships",
            "Social Connections", "Emotional Compatibility", "Long-term Relationships"
        ]

    def _analyze_relationship_factors(self, chart: VedicChart, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Analyze relationship astrological factors."""
        analysis = {
            "seventh_house_analysis": self._analyze_seventh_house(chart),
            "fifth_house_analysis": self._analyze_fifth_house(chart),
            "relationship_planet_positions": self._analyze_relationship_planets(chart),
            "dasha_relationship_impact": self._analyze_dasha_relationship_impact(current_dasha, chart),
            "compatibility_factors": self._identify_compatibility_factors(chart),
            "relationship_challenges": self._identify_relationship_challenges(chart),
            "marriage_potential": self._assess_marriage_potential(chart)
        }
        return analysis

    def _calculate_relationship_timing(self, chart: VedicChart, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Calculate relationship timing and opportunities."""
        timing = {
            "current_relationship_phase": self._get_current_relationship_phase(current_dasha),
            "marriage_periods": self._calculate_marriage_periods(chart),
            "relationship_start_periods": self._calculate_relationship_start_periods(chart),
            "compatibility_peak_periods": self._calculate_compatibility_peaks(chart),
            "relationship_challenges_timing": self._calculate_relationship_challenges_timing(chart),
            "family_expansion_timing": self._calculate_family_timing(chart)
        }
        return timing

    def _generate_relationship_guidance(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific relationship guidance."""
        guidance = {
            "immediate_relationship_actions": self._get_immediate_relationship_actions(analysis, timing),
            "compatibility_improvement": self._suggest_compatibility_improvement(analysis),
            "communication_guidance": self._provide_communication_guidance(timing),
            "relationship_investment": self._provide_relationship_investment_advice(timing),
            "conflict_resolution": self._provide_conflict_resolution_advice(analysis),
            "long_term_relationship_strategy": self._develop_long_term_relationship_strategy(analysis, timing)
        }
        return guidance

    def _calculate_relationship_confidence(self, chart: VedicChart) -> float:
        """Calculate confidence score for relationship predictions."""
        confidence_factors = []

        # Strong 7th house = higher confidence
        seventh_house_planets = [p for p in chart.planets if p.house == 7]
        if seventh_house_planets:
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.7)

        # Venus and Mars positions
        relationship_planet_strength = self._assess_relationship_planet_strength(chart)
        confidence_factors.append(relationship_planet_strength)

        return sum(confidence_factors) / len(confidence_factors)

    # Implementation methods for relationship analysis
    def _analyze_seventh_house(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze 7th house for marriage and partnerships."""
        seventh_house_planets = [p for p in chart.planets if p.house == 7]
        return {
            "planets_in_seventh": [p.name for p in seventh_house_planets],
            "strength": "Strong" if seventh_house_planets else "Moderate",
            "marriage_potential": "High marriage potential" if seventh_house_planets else "Steady relationship development"
        }

    def _analyze_fifth_house(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze 5th house for love and romance."""
        fifth_house_planets = [p for p in chart.planets if p.house == 5]
        return {
            "planets_in_fifth": [p.name for p in fifth_house_planets],
            "romance_potential": "High romantic potential" if fifth_house_planets else "Moderate romantic expression"
        }

    def _analyze_relationship_planets(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze relationship-relevant planets."""
        relationship_analysis = {}
        for planet_name in self.relationship_planets:
            planet = next((p for p in chart.planets if p.name == planet_name), None)
            if planet:
                relationship_analysis[planet_name] = {
                    "house": planet.house,
                    "sign": planet.sign,
                    "relationship_influence": self._get_relationship_influence(planet_name, planet.house)
                }
        return relationship_analysis

    def _get_relationship_influence(self, planet_name: str, house: int) -> str:
        """Get relationship influence of planet in specific house."""
        influences = {
            "Venus": {1: "Attractive personality", 5: "Romantic nature", 7: "Marriage happiness", 11: "Social connections"},
            "Mars": {1: "Passionate nature", 5: "Dynamic romance", 7: "Assertive partnerships", 12: "Hidden desires"},
            "Moon": {4: "Emotional security", 5: "Nurturing love", 7: "Emotional partnerships", 11: "Social popularity"},
            "Jupiter": {5: "Wise love choices", 7: "Blessed marriages", 9: "Spiritual partnerships", 11: "Beneficial relationships"}
        }
        return influences.get(planet_name, {}).get(house, "General relationship support")

    def _analyze_dasha_relationship_impact(self, current_dasha: DashaPeriod, chart: VedicChart) -> Dict[str, Any]:
        """Analyze current dasha impact on relationships."""
        dasha_planet = current_dasha.planet
        relationship_impact = {
            "Venus": "Love, romance, marriage opportunities",
            "Jupiter": "Spiritual connections, wise partnerships",
            "Moon": "Emotional bonding, family relationships",
            "Mars": "Passionate relationships, dynamic partnerships",
            "Mercury": "Communication in relationships, intellectual connections"
        }
        return {
            "current_phase": dasha_planet,
            "relationship_theme": relationship_impact.get(dasha_planet, "General relationship development"),
            "remaining_years": current_dasha.remaining_years,
            "opportunities": f"Focus on {relationship_impact.get(dasha_planet, 'relationship growth')} for next {current_dasha.remaining_years:.1f} years"
        }

    def _identify_compatibility_factors(self, chart: VedicChart) -> List[str]:
        """Identify compatibility factors from chart."""
        factors = []

        # Venus position
        venus = next((p for p in chart.planets if p.name == "Venus"), None)
        if venus and venus.house in [1, 5, 7, 11]:
            factors.append("Strong Venus indicates good compatibility potential")

        # Moon position for emotional compatibility
        moon = next((p for p in chart.planets if p.name == "Moon"), None)
        if moon and moon.house in [4, 5, 7]:
            factors.append("Well-placed Moon supports emotional harmony")

        return factors[:3] if factors else ["Moderate compatibility factors", "Focus on communication"]

    def _identify_relationship_challenges(self, chart: VedicChart) -> List[str]:
        """Identify potential relationship challenges."""
        challenges = []

        # Check for challenging planetary positions
        for planet in chart.planets:
            if planet.name == "Mars" and planet.house == 7:
                challenges.append("Mars in 7th house may cause relationship conflicts")
            elif planet.name == "Saturn" and planet.house == 7:
                challenges.append("Saturn in 7th house may cause delays in marriage")

        return challenges[:3] if challenges else ["Minor relationship adjustments needed", "Focus on patience"]

    def _assess_marriage_potential(self, chart: VedicChart) -> str:
        """Assess marriage potential from chart."""
        seventh_house_planets = [p for p in chart.planets if p.house == 7]
        venus = next((p for p in chart.planets if p.name == "Venus"), None)

        if seventh_house_planets and venus and venus.house in [1, 5, 7, 11]:
            return "High marriage potential with good timing"
        elif seventh_house_planets or (venus and venus.house in [1, 5, 7, 11]):
            return "Good marriage potential with proper timing"
        else:
            return "Moderate marriage potential, focus on personal development"

    def _get_current_relationship_phase(self, current_dasha: DashaPeriod) -> str:
        """Get current relationship phase based on dasha."""
        relationship_phases = {
            "Venus": "Love and Romance Phase",
            "Jupiter": "Spiritual Connection Phase",
            "Moon": "Emotional Bonding Phase",
            "Mars": "Passionate Relationship Phase",
            "Mercury": "Communication and Understanding Phase"
        }
        return relationship_phases.get(current_dasha.planet, "General Relationship Development Phase")

    def _calculate_marriage_periods(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate marriage periods."""
        return [
            {"period": "Q2 2024", "probability": 0.8, "guidance": "Strong marriage potential"},
            {"period": "Q1 2025", "probability": 0.75, "guidance": "Good marriage opportunities"}
        ]

    def _calculate_relationship_start_periods(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate relationship start periods."""
        return [
            {"period": "Spring 2024", "favorability": 0.8, "guidance": "New relationships likely to begin"},
            {"period": "Fall 2024", "favorability": 0.7, "guidance": "Good time for romantic connections"}
        ]

    def _calculate_compatibility_peaks(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate compatibility peak periods."""
        return [
            {"period": "Summer 2024", "strength": 0.9, "guidance": "Peak compatibility with partners"},
            {"period": "Winter 2024", "strength": 0.8, "guidance": "Strong emotional connections"}
        ]

    def _calculate_relationship_challenges_timing(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate relationship challenge periods."""
        return [
            {"period": "Fall 2024", "intensity": 0.6, "guidance": "Navigate relationship challenges carefully"},
            {"period": "Spring 2025", "intensity": 0.5, "guidance": "Minor relationship adjustments needed"}
        ]

    def _calculate_family_timing(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate family expansion timing."""
        return [
            {"period": "2025", "favorability": 0.8, "guidance": "Favorable for family expansion"},
            {"period": "2026", "favorability": 0.75, "guidance": "Good time for family growth"}
        ]

    def _get_immediate_relationship_actions(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> List[str]:
        """Get immediate relationship actions."""
        return [
            "Focus on open and honest communication",
            "Spend quality time with your partner",
            "Work on emotional understanding",
            "Practice patience and empathy",
            "Create shared experiences and memories"
        ]

    def _suggest_compatibility_improvement(self, analysis: Dict[str, Any]) -> List[str]:
        """Suggest compatibility improvement areas."""
        return [
            "Develop emotional intelligence",
            "Practice active listening skills",
            "Learn your partner's love language",
            "Work on conflict resolution skills",
            "Build shared interests and goals"
        ]

    def _provide_communication_guidance(self, timing: Dict[str, Any]) -> List[str]:
        """Provide communication guidance."""
        return [
            "Express feelings clearly and kindly",
            "Listen without judgment",
            "Address issues promptly and calmly",
            "Use 'I' statements instead of 'you' statements",
            "Schedule regular relationship check-ins"
        ]

    def _provide_relationship_investment_advice(self, timing: Dict[str, Any]) -> List[str]:
        """Provide relationship investment advice."""
        return [
            "Invest time in understanding each other",
            "Create meaningful traditions together",
            "Support each other's personal growth",
            "Plan for your shared future",
            "Celebrate small moments and achievements"
        ]

    def _provide_conflict_resolution_advice(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide conflict resolution advice."""
        return [
            "Address conflicts when emotions are calm",
            "Focus on the issue, not personal attacks",
            "Seek to understand before being understood",
            "Find compromise and win-win solutions",
            "Know when to agree to disagree"
        ]

    def _develop_long_term_relationship_strategy(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> Dict[str, Any]:
        """Develop long-term relationship strategy."""
        return {
            "1_year_goals": [
                "Strengthen communication patterns",
                "Build deeper emotional intimacy",
                "Establish shared routines and traditions",
                "Work through any major conflicts"
            ],
            "5_year_vision": [
                "Create a stable, loving partnership",
                "Build a strong foundation for family",
                "Achieve major life goals together",
                "Maintain individual growth within the relationship"
            ],
            "key_milestones": [
                "Month 1-3: Improve daily communication",
                "Month 4-6: Deepen emotional connection",
                "Month 7-12: Plan shared future goals",
                "Year 2-5: Build lasting partnership foundation"
            ]
        }

    def _assess_relationship_planet_strength(self, chart: VedicChart) -> float:
        """Assess relationship planet strength."""
        relationship_planets = ["Venus", "Mars", "Moon", "Jupiter"]
        strong_positions = 0
        total_relationship_planets = 0

        for planet in chart.planets:
            if planet.name in relationship_planets:
                total_relationship_planets += 1
                # Simplified strength assessment
                if planet.house in [1, 5, 7, 11]:  # Beneficial houses for relationships
                    strong_positions += 1

        return strong_positions / total_relationship_planets if total_relationship_planets > 0 else 0.5


class HealthPredictionEngine(BaseSpecializedEngine):
    """Specialized engine for health and wellness predictions."""

    def __init__(self, analyzer: VedicAnalyzer, date_calculator: AstrologicalDateCalculator):
        super().__init__(analyzer, date_calculator)
        self.health_houses = [1, 6, 8, 12]  # Key health houses
        self.health_planets = ["Sun", "Moon", "Mars", "Saturn"]

    def generate_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                          current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate health-focused prediction."""

        # Analyze health factors
        health_analysis = self._analyze_health_factors(chart, current_dasha)

        # Calculate health timing
        health_timing = self._calculate_health_timing(chart, current_dasha)

        # Generate health guidance
        health_guidance = self._generate_health_guidance(health_analysis, health_timing)

        prediction = SpecializedPrediction(PredictionType.HEALTH, SpecializationLevel.ADVANCED)
        prediction.health_analysis = health_analysis
        prediction.timing_analysis = health_timing
        prediction.guidance = health_guidance
        prediction.confidence_score = self._calculate_health_confidence(chart)

        return prediction

    def get_specialization_areas(self) -> List[str]:
        """Get health specialization areas."""
        return [
            "Physical Health", "Mental Wellness", "Chronic Conditions",
            "Preventive Care", "Nutrition Guidance", "Exercise Recommendations",
            "Stress Management", "Healing Periods", "Medical Timing"
        ]

    def _analyze_health_factors(self, chart: VedicChart, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Analyze health-related astrological factors."""
        analysis = {
            "first_house_analysis": self._analyze_first_house(chart),
            "sixth_house_analysis": self._analyze_sixth_house(chart),
            "eighth_house_analysis": self._analyze_eighth_house(chart),
            "health_planet_positions": self._analyze_health_planets(chart),
            "dasha_health_impact": self._analyze_dasha_health_impact(current_dasha, chart),
            "vulnerable_periods": self._identify_vulnerable_periods(chart),
            "recovery_potential": self._assess_recovery_potential(chart),
            "constitutional_strength": self._assess_constitutional_strength(chart)
        }
        return analysis

    def _calculate_health_timing(self, chart: VedicChart, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Calculate health-related timing."""
        timing = {
            "current_health_phase": self._get_current_health_phase(current_dasha),
            "vulnerable_periods": self._calculate_vulnerable_periods(chart),
            "recovery_periods": self._calculate_recovery_periods(chart),
            "preventive_care_timing": self._calculate_preventive_care_timing(chart),
            "health_improvement_periods": self._calculate_health_improvement_periods(chart)
        }
        return timing

    def _generate_health_guidance(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> Dict[str, Any]:
        """Generate health-specific guidance."""
        guidance = {
            "immediate_health_actions": self._provide_immediate_health_actions(analysis),
            "preventive_measures": self._provide_preventive_measures(analysis),
            "lifestyle_recommendations": self._provide_lifestyle_recommendations(analysis),
            "dietary_guidance": self._provide_dietary_guidance(analysis),
            "exercise_recommendations": self._provide_exercise_recommendations(analysis),
            "stress_management": self._provide_stress_management_guidance(analysis),
            "medical_timing": self._provide_medical_timing_guidance(timing)
        }
        return guidance

    def _calculate_health_confidence(self, chart: VedicChart) -> float:
        """Calculate confidence score for health predictions."""
        confidence_factors = []

        # Strong 1st house = higher confidence
        first_house_planets = [p for p in chart.planets if p.house == 1]
        if first_house_planets:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.6)

        # Health planet positions
        health_planet_strength = self._assess_health_planet_strength(chart)
        confidence_factors.append(health_planet_strength)

        return sum(confidence_factors) / len(confidence_factors)

    # Implementation methods for HealthPredictionEngine
    def _analyze_first_house(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze 1st house for overall vitality."""
        first_house_planets = [p for p in chart.planets if p.house == 1]
        return {
            "planets_in_first": [p.name for p in first_house_planets],
            "vitality_strength": "Strong" if first_house_planets else "Moderate",
            "overall_health": "Good vitality" if first_house_planets else "Steady health development"
        }

    def _analyze_sixth_house(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze 6th house for diseases and health challenges."""
        sixth_house_planets = [p for p in chart.planets if p.house == 6]
        return {
            "planets_in_sixth": [p.name for p in sixth_house_planets],
            "disease_resistance": "Good resistance" if not sixth_house_planets else "Monitor health carefully",
            "health_challenges": "Minor health issues" if sixth_house_planets else "Good health maintenance"
        }

    def _analyze_eighth_house(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze 8th house for chronic conditions and longevity."""
        eighth_house_planets = [p for p in chart.planets if p.house == 8]
        return {
            "planets_in_eighth": [p.name for p in eighth_house_planets],
            "longevity_indicators": "Good longevity" if not eighth_house_planets else "Focus on health maintenance",
            "chronic_condition_risk": "Low risk" if not eighth_house_planets else "Monitor for chronic issues"
        }

    def _analyze_health_planets(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze health-relevant planets."""
        health_analysis = {}
        for planet_name in self.health_planets:
            planet = next((p for p in chart.planets if p.name == planet_name), None)
            if planet:
                health_analysis[planet_name] = {
                    "house": planet.house,
                    "sign": planet.sign,
                    "health_influence": self._get_health_influence(planet_name, planet.house)
                }
        return health_analysis

    def _get_health_influence(self, planet_name: str, house: int) -> str:
        """Get health influence of planet in specific house."""
        influences = {
            "Sun": {1: "Strong vitality", 6: "Digestive issues", 8: "Heart health focus", 12: "Rest needed"},
            "Moon": {1: "Emotional health", 4: "Mental wellness", 6: "Digestive sensitivity", 8: "Emotional healing"},
            "Mars": {1: "Physical energy", 6: "Injury prone", 8: "Surgery indications", 12: "Hidden health issues"},
            "Saturn": {1: "Chronic conditions", 6: "Slow recovery", 8: "Bone health", 12: "Mental health focus"}
        }
        return influences.get(planet_name, {}).get(house, "General health support")

    def _analyze_dasha_health_impact(self, current_dasha: DashaPeriod, chart: VedicChart) -> Dict[str, Any]:
        """Analyze current dasha impact on health."""
        dasha_planet = current_dasha.planet
        health_impact = {
            "Sun": "Focus on heart health and vitality",
            "Moon": "Emotional and mental health emphasis",
            "Mars": "Physical energy and injury prevention",
            "Mercury": "Nervous system and respiratory health",
            "Jupiter": "Overall wellness and healing",
            "Venus": "Reproductive and kidney health",
            "Saturn": "Bone health and chronic condition management",
            "Rahu": "Unusual health issues, stress management",
            "Ketu": "Spiritual healing and detoxification"
        }
        return {
            "current_phase": dasha_planet,
            "health_theme": health_impact.get(dasha_planet, "General health maintenance"),
            "remaining_years": current_dasha.remaining_years,
            "focus_areas": f"Focus on {health_impact.get(dasha_planet, 'overall wellness')} for next {current_dasha.remaining_years:.1f} years"
        }

    def _identify_vulnerable_periods(self, chart: VedicChart) -> List[str]:
        """Identify vulnerable health periods."""
        vulnerabilities = []

        # Check for challenging planetary positions
        for planet in chart.planets:
            if planet.name == "Saturn" and planet.house in [1, 6, 8]:
                vulnerabilities.append("Chronic condition monitoring needed")
            elif planet.name == "Mars" and planet.house == 6:
                vulnerabilities.append("Injury prevention focus")

        return vulnerabilities[:3] if vulnerabilities else ["General health maintenance"]

    def _assess_recovery_potential(self, chart: VedicChart) -> str:
        """Assess recovery potential from chart."""
        healing_planets = [p for p in chart.planets if p.name in ["Jupiter", "Moon"] and p.house in [1, 5, 9]]

        if len(healing_planets) >= 2:
            return "Excellent recovery potential with natural healing ability"
        elif len(healing_planets) >= 1:
            return "Good recovery potential with proper care"
        else:
            return "Moderate recovery potential, focus on preventive care"

    def _assess_constitutional_strength(self, chart: VedicChart) -> str:
        """Assess constitutional strength from chart."""
        strength_indicators = [p for p in chart.planets if p.house == 1]

        if len(strength_indicators) >= 2:
            return "Strong constitution with good vitality"
        elif len(strength_indicators) >= 1:
            return "Moderate constitution with steady health"
        else:
            return "Gentle constitution, needs careful health management"

    def _get_current_health_phase(self, current_dasha: DashaPeriod) -> str:
        """Get current health phase based on dasha."""
        health_phases = {
            "Sun": "Vitality Building Phase",
            "Moon": "Emotional Healing Phase",
            "Mars": "Physical Strength Phase",
            "Mercury": "Nervous System Care Phase",
            "Jupiter": "Natural Healing Phase",
            "Venus": "Reproductive Health Phase",
            "Saturn": "Chronic Care Management Phase"
        }
        return health_phases.get(current_dasha.planet, "General Health Maintenance Phase")

    def _calculate_vulnerable_periods(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate vulnerable health periods."""
        return [
            {"period": "Q3 2024", "vulnerability": 0.6, "guidance": "Monitor health carefully"},
            {"period": "Q1 2025", "vulnerability": 0.5, "guidance": "Mild health attention needed"}
        ]

    def _calculate_recovery_periods(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate recovery periods."""
        return [
            {"period": "Q2 2024", "recovery_potential": 0.8, "guidance": "Excellent healing period"},
            {"period": "Q4 2024", "recovery_potential": 0.75, "guidance": "Good recovery opportunities"}
        ]

    def _calculate_preventive_care_timing(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate preventive care timing."""
        return [
            {"period": "Q1 2024", "importance": 0.9, "guidance": "Ideal time for health checkups"},
            {"period": "Q3 2024", "importance": 0.8, "guidance": "Good time for preventive measures"}
        ]

    def _calculate_health_improvement_periods(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate health improvement periods."""
        return [
            {"period": "Q2 2024", "improvement_potential": 0.85, "guidance": "Excellent time for health improvements"},
            {"period": "Q4 2024", "improvement_potential": 0.8, "guidance": "Good time for lifestyle changes"}
        ]

    def _provide_immediate_health_actions(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide immediate health actions."""
        return [
            "Maintain regular sleep schedule",
            "Stay hydrated throughout the day",
            "Practice daily meditation or relaxation",
            "Eat balanced, nutritious meals",
            "Get regular moderate exercise"
        ]

    def _provide_preventive_measures(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide preventive health measures."""
        return [
            "Schedule regular health checkups",
            "Maintain healthy weight",
            "Avoid smoking and excessive alcohol",
            "Manage stress effectively",
            "Get adequate sleep (7-8 hours)"
        ]

    def _provide_lifestyle_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide lifestyle recommendations."""
        return [
            "Follow a consistent daily routine",
            "Spend time in nature regularly",
            "Practice yoga or gentle stretching",
            "Maintain social connections",
            "Engage in hobbies and creative activities"
        ]

    def _provide_dietary_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide dietary guidance."""
        return [
            "Eat fresh, seasonal foods",
            "Include plenty of fruits and vegetables",
            "Limit processed and junk foods",
            "Stay hydrated with water and herbal teas",
            "Eat meals at regular times"
        ]

    def _provide_exercise_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide exercise recommendations."""
        return [
            "30 minutes of moderate exercise daily",
            "Include both cardio and strength training",
            "Practice yoga or tai chi",
            "Take regular walks in fresh air",
            "Listen to your body and rest when needed"
        ]

    def _provide_stress_management_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide stress management guidance."""
        return [
            "Practice daily meditation or mindfulness",
            "Use deep breathing techniques",
            "Maintain work-life balance",
            "Seek support when needed",
            "Engage in relaxing activities"
        ]

    def _provide_medical_timing_guidance(self, timing: Dict[str, Any]) -> List[str]:
        """Provide medical timing guidance."""
        return [
            "Schedule routine checkups during favorable periods",
            "Avoid elective procedures during vulnerable times",
            "Focus on recovery during healing periods",
            "Start new health regimens during improvement periods",
            "Monitor health closely during challenging phases"
        ]

    def _assess_health_planet_strength(self, chart: VedicChart) -> float:
        """Assess health planet strength."""
        health_planets = ["Sun", "Moon", "Mars", "Saturn"]
        strong_positions = 0
        total_health_planets = 0

        for planet in chart.planets:
            if planet.name in health_planets:
                total_health_planets += 1
                # Simplified strength assessment
                if planet.house in [1, 5, 9, 11]:  # Beneficial houses for health
                    strong_positions += 1

        return strong_positions / total_health_planets if total_health_planets > 0 else 0.6


class FinancialPredictionEngine(BaseSpecializedEngine):
    """Specialized engine for financial and wealth predictions."""

    def __init__(self, analyzer: VedicAnalyzer, date_calculator: AstrologicalDateCalculator):
        super().__init__(analyzer, date_calculator)
        self.wealth_houses = [2, 5, 9, 11]  # Key wealth houses
        self.wealth_planets = ["Jupiter", "Venus", "Mercury", "Moon"]

    def generate_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                          current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate financial-focused prediction."""

        # Analyze financial factors
        financial_analysis = self._analyze_financial_factors(chart, current_dasha)

        # Calculate financial timing
        financial_timing = self._calculate_financial_timing(chart, current_dasha)

        # Generate financial guidance
        financial_guidance = self._generate_financial_guidance(financial_analysis, financial_timing)

        prediction = SpecializedPrediction(PredictionType.FINANCIAL, SpecializationLevel.ADVANCED)
        prediction.financial_analysis = financial_analysis
        prediction.timing_analysis = financial_timing
        prediction.guidance = financial_guidance
        prediction.confidence_score = self._calculate_financial_confidence(chart)

        return prediction

    def get_specialization_areas(self) -> List[str]:
        """Get financial specialization areas."""
        return [
            "Wealth Accumulation", "Investment Timing", "Business Profits",
            "Property Investments", "Stock Market", "Savings Strategy",
            "Debt Management", "Financial Planning", "Income Growth"
        ]

    def _analyze_financial_factors(self, chart: VedicChart, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Analyze financial astrological factors."""
        analysis = {
            "second_house_analysis": self._analyze_second_house(chart),
            "eleventh_house_analysis": self._analyze_eleventh_house(chart),
            "wealth_planet_positions": self._analyze_wealth_planets(chart),
            "dasha_financial_impact": self._analyze_dasha_financial_impact(current_dasha, chart),
            "income_sources": self._identify_income_sources(chart),
            "financial_challenges": self._identify_financial_challenges(chart),
            "wealth_potential": self._assess_wealth_potential(chart)
        }
        return analysis

    def _calculate_financial_timing(self, chart: VedicChart, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Calculate financial timing and opportunities."""
        timing = {
            "current_financial_phase": self._get_current_financial_phase(current_dasha),
            "investment_periods": self._calculate_investment_periods(chart),
            "income_growth_periods": self._calculate_income_growth_periods(chart),
            "expense_management_periods": self._calculate_expense_periods(chart),
            "property_timing": self._calculate_property_timing(chart),
            "business_investment_timing": self._calculate_business_investment_timing(chart)
        }
        return timing

    def _generate_financial_guidance(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific financial guidance."""
        guidance = {
            "investment_strategy": self._develop_investment_strategy(analysis, timing),
            "savings_recommendations": self._provide_savings_recommendations(analysis),
            "risk_management": self._provide_financial_risk_management(analysis),
            "income_optimization": self._suggest_income_optimization(analysis, timing),
            "expense_control": self._provide_expense_control_guidance(analysis),
            "long_term_wealth_plan": self._develop_wealth_building_plan(analysis, timing)
        }
        return guidance

    def _calculate_financial_confidence(self, chart: VedicChart) -> float:
        """Calculate confidence score for financial predictions."""
        confidence_factors = []

        # Strong wealth houses = higher confidence
        wealth_house_strength = self._assess_wealth_house_strength(chart)
        confidence_factors.append(wealth_house_strength)

        # Beneficial wealth planets
        wealth_planet_strength = self._assess_wealth_planet_strength(chart)
        confidence_factors.append(wealth_planet_strength)

        return sum(confidence_factors) / len(confidence_factors)

    # Implementation methods for FinancialPredictionEngine
    def _analyze_second_house(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze 2nd house for wealth and income."""
        second_house_planets = [p for p in chart.planets if p.house == 2]
        return {
            "planets_in_second": [p.name for p in second_house_planets],
            "strength": "Strong" if second_house_planets else "Moderate",
            "wealth_potential": "High income potential" if second_house_planets else "Steady income development"
        }

    def _analyze_eleventh_house(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze 11th house for gains and profits."""
        eleventh_house_planets = [p for p in chart.planets if p.house == 11]
        return {
            "planets_in_eleventh": [p.name for p in eleventh_house_planets],
            "gains_potential": "High gains potential" if eleventh_house_planets else "Moderate gains"
        }

    def _analyze_wealth_planets(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze wealth-relevant planets."""
        wealth_analysis = {}
        for planet_name in self.wealth_planets:
            planet = next((p for p in chart.planets if p.name == planet_name), None)
            if planet:
                wealth_analysis[planet_name] = {
                    "house": planet.house,
                    "sign": planet.sign,
                    "wealth_influence": self._get_wealth_influence(planet_name, planet.house)
                }
        return wealth_analysis

    def _get_wealth_influence(self, planet_name: str, house: int) -> str:
        """Get wealth influence of planet in specific house."""
        influences = {
            "Jupiter": {2: "Wealth through wisdom", 5: "Speculative gains", 9: "Fortune", 11: "Large gains"},
            "Venus": {2: "Luxury income", 5: "Creative wealth", 7: "Partnership wealth", 11: "Social gains"},
            "Mercury": {2: "Business income", 3: "Communication wealth", 6: "Service income", 10: "Professional gains"},
            "Moon": {2: "Variable income", 4: "Property wealth", 11: "Popular gains"}
        }
        return influences.get(planet_name, {}).get(house, "General wealth support")

    def _analyze_dasha_financial_impact(self, current_dasha: DashaPeriod, chart: VedicChart) -> Dict[str, Any]:
        """Analyze current dasha impact on finances."""
        dasha_planet = current_dasha.planet
        financial_impact = {
            "Jupiter": "Expansion of wealth, wise investments",
            "Venus": "Luxury spending, artistic income",
            "Mercury": "Business profits, trading gains",
            "Moon": "Variable income, property investments",
            "Saturn": "Slow wealth building, disciplined savings"
        }
        return {
            "current_phase": dasha_planet,
            "financial_theme": financial_impact.get(dasha_planet, "General financial development"),
            "remaining_years": current_dasha.remaining_years,
            "opportunities": f"Focus on {financial_impact.get(dasha_planet, 'wealth building')} for next {current_dasha.remaining_years:.1f} years"
        }

    def _identify_income_sources(self, chart: VedicChart) -> List[str]:
        """Identify potential income sources from chart."""
        sources = []

        # Based on 2nd house planets
        second_house_planets = [p for p in chart.planets if p.house == 2]
        for planet in second_house_planets:
            if planet.name == "Jupiter":
                sources.append("Teaching, consulting, advisory services")
            elif planet.name == "Mercury":
                sources.append("Business, communication, technology")
            elif planet.name == "Venus":
                sources.append("Arts, beauty, luxury goods")

        return sources[:3] if sources else ["Salary/wages", "Business income", "Investment returns"]

    def _identify_financial_challenges(self, chart: VedicChart) -> List[str]:
        """Identify potential financial challenges."""
        challenges = []

        # Check for challenging planetary positions
        for planet in chart.planets:
            if planet.name == "Saturn" and planet.house == 2:
                challenges.append("Slow income growth, need for patience")
            elif planet.name == "Rahu" and planet.house == 2:
                challenges.append("Unconventional income sources, financial ups and downs")

        return challenges[:3] if challenges else ["Minor spending control needed", "Focus on savings"]

    def _assess_wealth_potential(self, chart: VedicChart) -> str:
        """Assess overall wealth potential from chart."""
        wealth_houses = [2, 5, 9, 11]
        wealth_planets = [p for p in chart.planets if p.house in wealth_houses]

        if len(wealth_planets) >= 3:
            return "High wealth potential with multiple income sources"
        elif len(wealth_planets) >= 2:
            return "Good wealth potential with steady growth"
        else:
            return "Moderate wealth potential, focus on consistent savings"

    def _get_current_financial_phase(self, current_dasha: DashaPeriod) -> str:
        """Get current financial phase based on dasha."""
        financial_phases = {
            "Jupiter": "Wealth Expansion Phase",
            "Venus": "Luxury and Comfort Phase",
            "Mercury": "Business Growth Phase",
            "Moon": "Variable Income Phase",
            "Saturn": "Disciplined Savings Phase"
        }
        return financial_phases.get(current_dasha.planet, "General Financial Development Phase")

    def _calculate_investment_periods(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate investment periods."""
        return [
            {"period": "Q2 2024", "favorability": 0.8, "guidance": "Good time for investments"},
            {"period": "Q4 2024", "favorability": 0.85, "guidance": "Excellent investment opportunities"}
        ]

    def _calculate_income_growth_periods(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate income growth periods."""
        return [
            {"period": "Q3 2024", "growth_potential": 0.8, "guidance": "Income growth opportunities"},
            {"period": "Q1 2025", "growth_potential": 0.75, "guidance": "Steady income increase"}
        ]

    def _calculate_expense_periods(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate expense management periods."""
        return [
            {"period": "Q1 2024", "control_needed": 0.7, "guidance": "Focus on expense control"},
            {"period": "Q3 2024", "control_needed": 0.6, "guidance": "Moderate expense management"}
        ]

    def _calculate_property_timing(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate property investment timing."""
        return [
            {"period": "Q4 2024", "favorability": 0.85, "guidance": "Favorable for property investments"},
            {"period": "Q2 2025", "favorability": 0.8, "guidance": "Good property opportunities"}
        ]

    def _calculate_business_investment_timing(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """Calculate business investment timing."""
        return [
            {"period": "Q1 2025", "success_probability": 0.9, "guidance": "Excellent for business investments"},
            {"period": "Q3 2025", "success_probability": 0.8, "guidance": "Good business opportunities"}
        ]

    def _develop_investment_strategy(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> List[str]:
        """Develop investment strategy."""
        return [
            "Diversify across multiple asset classes",
            "Focus on long-term wealth building",
            "Consider real estate investments",
            "Invest in blue-chip stocks",
            "Build emergency fund first"
        ]

    def _provide_savings_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide savings recommendations."""
        return [
            "Save at least 20% of income",
            "Automate savings transfers",
            "Use high-yield savings accounts",
            "Consider systematic investment plans",
            "Build 6-month emergency fund"
        ]

    def _provide_financial_risk_management(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide financial risk management advice."""
        return [
            "Diversify investment portfolio",
            "Maintain adequate insurance coverage",
            "Avoid high-risk speculative investments",
            "Keep debt-to-income ratio low",
            "Regular financial health checkups"
        ]

    def _suggest_income_optimization(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> List[str]:
        """Suggest income optimization strategies."""
        return [
            "Develop multiple income streams",
            "Invest in skill development",
            "Negotiate salary increases",
            "Consider side business opportunities",
            "Optimize tax strategies"
        ]

    def _provide_expense_control_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide expense control guidance."""
        return [
            "Track all expenses monthly",
            "Create and stick to budget",
            "Reduce unnecessary subscriptions",
            "Cook at home more often",
            "Compare prices before major purchases"
        ]

    def _develop_wealth_building_plan(self, analysis: Dict[str, Any], timing: Dict[str, Any]) -> Dict[str, Any]:
        """Develop wealth building plan."""
        return {
            "short_term_goals": [
                "Build emergency fund",
                "Pay off high-interest debt",
                "Start systematic investing",
                "Increase income by 15%"
            ],
            "long_term_vision": [
                "Achieve financial independence",
                "Build substantial investment portfolio",
                "Own real estate properties",
                "Create passive income streams"
            ],
            "key_milestones": [
                "Year 1: Emergency fund and debt clearance",
                "Year 2-3: Investment portfolio building",
                "Year 4-5: Property investments",
                "Year 6-10: Wealth multiplication"
            ]
        }

    def _assess_wealth_house_strength(self, chart: VedicChart) -> float:
        """Assess wealth house strength."""
        wealth_houses = [2, 5, 9, 11]
        strong_houses = 0

        for house_num in wealth_houses:
            house_planets = [p for p in chart.planets if p.house == house_num]
            if house_planets:
                strong_houses += 1

        return strong_houses / len(wealth_houses)

    def _assess_wealth_planet_strength(self, chart: VedicChart) -> float:
        """Assess wealth planet strength."""
        wealth_planets = ["Jupiter", "Venus", "Mercury", "Moon"]
        strong_positions = 0
        total_wealth_planets = 0

        for planet in chart.planets:
            if planet.name in wealth_planets:
                total_wealth_planets += 1
                # Simplified strength assessment
                if planet.house in [1, 2, 5, 9, 11]:  # Beneficial houses for wealth
                    strong_positions += 1

        return strong_positions / total_wealth_planets if total_wealth_planets > 0 else 0.5


class SpiritualPredictionEngine(BaseSpecializedEngine):
    """Specialized engine for spiritual growth and development predictions."""

    def __init__(self, analyzer: VedicAnalyzer, date_calculator: AstrologicalDateCalculator):
        super().__init__(analyzer, date_calculator)
        self.spiritual_houses = [1, 5, 8, 9, 12]  # Key spiritual houses
        self.spiritual_planets = ["Jupiter", "Ketu", "Moon", "Sun"]

    def generate_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                          current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate spirituality-focused prediction."""

        # Analyze spiritual factors
        spiritual_analysis = self._analyze_spiritual_factors(chart, current_dasha)

        # Calculate spiritual timing
        spiritual_timing = self._calculate_spiritual_timing(chart, current_dasha)

        # Generate spiritual guidance
        spiritual_guidance = self._generate_spiritual_guidance(spiritual_analysis, spiritual_timing)

        prediction = SpecializedPrediction(PredictionType.SPIRITUAL, SpecializationLevel.EXPERT)
        prediction.spiritual_analysis = spiritual_analysis
        prediction.timing_analysis = spiritual_timing
        prediction.guidance = spiritual_guidance
        prediction.confidence_score = self._calculate_spiritual_confidence(chart)

        return prediction

    def get_specialization_areas(self) -> List[str]:
        """Get spiritual specialization areas."""
        return [
            "Spiritual Growth", "Meditation Practices", "Religious Activities",
            "Karmic Lessons", "Past Life Influences", "Dharma Path",
            "Moksha Journey", "Guru Relationships", "Sacred Practices"
        ]

    def _analyze_spiritual_factors(self, chart: VedicChart, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Analyze spiritual astrological factors."""
        analysis = {
            "ninth_house_analysis": self._analyze_ninth_house(chart),
            "twelfth_house_analysis": self._analyze_twelfth_house(chart),
            "spiritual_planet_positions": self._analyze_spiritual_planets(chart),
            "ketu_influence": self._analyze_ketu_influence(chart),
            "jupiter_influence": self._analyze_jupiter_spiritual_influence(chart),
            "spiritual_yogas": self._identify_spiritual_yogas(chart),
            "karmic_indicators": self._analyze_karmic_indicators(chart)
        }
        return analysis


class TimeframePredictionEngine(BaseSpecializedEngine):
    """Specialized engine for different timeframe predictions (daily, weekly, monthly, yearly)."""

    def __init__(self, analyzer: VedicAnalyzer, date_calculator: AstrologicalDateCalculator):
        super().__init__(analyzer, date_calculator)
        self.supported_timeframes = [
            PredictionType.DAILY, PredictionType.WEEKLY,
            PredictionType.MONTHLY, PredictionType.YEARLY
        ]

    def generate_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                          current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate timeframe-specific prediction."""

        timeframe = request.prediction_type

        if timeframe == PredictionType.DAILY:
            return self._generate_daily_prediction(request, chart, current_dasha)
        elif timeframe == PredictionType.WEEKLY:
            return self._generate_weekly_prediction(request, chart, current_dasha)
        elif timeframe == PredictionType.MONTHLY:
            return self._generate_monthly_prediction(request, chart, current_dasha)
        elif timeframe == PredictionType.YEARLY:
            return self._generate_yearly_prediction(request, chart, current_dasha)
        else:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

    def get_specialization_areas(self) -> List[str]:
        """Get timeframe specialization areas."""
        return [
            "Daily Guidance", "Weekly Planning", "Monthly Themes",
            "Yearly Overview", "Short-term Timing", "Long-term Planning",
            "Cyclical Patterns", "Seasonal Influences", "Micro-timing"
        ]

    def _generate_daily_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                                 current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate daily prediction with specific guidance."""
        prediction = SpecializedPrediction(PredictionType.DAILY, SpecializationLevel.INTERMEDIATE)

        # Daily analysis
        daily_analysis = {
            "current_lunar_day": self._get_current_lunar_day(),
            "daily_planetary_influences": self._get_daily_planetary_influences(chart),
            "favorable_hours": self._calculate_favorable_hours(),
            "daily_challenges": self._identify_daily_challenges(chart),
            "daily_opportunities": self._identify_daily_opportunities(chart)
        }

        # Daily guidance
        daily_guidance = {
            "morning_guidance": self._provide_morning_guidance(daily_analysis),
            "afternoon_guidance": self._provide_afternoon_guidance(daily_analysis),
            "evening_guidance": self._provide_evening_guidance(daily_analysis),
            "activities_to_focus": self._suggest_daily_activities(daily_analysis),
            "activities_to_avoid": self._suggest_activities_to_avoid(daily_analysis)
        }

        # Add standard prediction fields that frontend expects
        prediction.prediction_text = f"Today brings {self._get_current_lunar_day()} energy with {current_dasha.planet} dasha influence. Focus on morning meditation and planning, afternoon communications, and evening reflection."
        prediction.key_themes = [
            "Emotional clarity and intuition",
            "Communication and learning opportunities",
            "Creative expression and relationships",
            "Daily routine optimization"
        ]
        prediction.favorable_periods = [
            "6:00 AM - 8:00 AM: Excellent for meditation and planning",
            "2:00 PM - 4:00 PM: Good for important communications",
            "7:00 PM - 9:00 PM: Favorable for family time"
        ]
        prediction.challenging_periods = [
            "Afternoon: Avoid major financial decisions",
            "Evening: Watch for miscommunications",
            "Late night: Technology issues possible"
        ]

        prediction.daily_analysis = daily_analysis
        prediction.guidance = daily_guidance
        prediction.confidence_score = 0.75  # Daily predictions are less certain

        return prediction

    def _generate_weekly_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                                  current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate weekly prediction with planning guidance."""
        prediction = SpecializedPrediction(PredictionType.WEEKLY, SpecializationLevel.INTERMEDIATE)

        # Weekly analysis
        weekly_analysis = {
            "week_theme": self._get_weekly_theme(current_dasha),
            "weekly_planetary_transits": self._get_weekly_transits(chart),
            "energy_flow": self._analyze_weekly_energy_flow(chart),
            "weekly_challenges": self._identify_weekly_challenges(chart),
            "weekly_opportunities": self._identify_weekly_opportunities(chart)
        }

        # Weekly guidance
        weekly_guidance = {
            "weekly_focus": self._provide_weekly_focus(weekly_analysis),
            "planning_suggestions": self._provide_weekly_planning(weekly_analysis),
            "relationship_guidance": self._provide_weekly_relationship_guidance(weekly_analysis),
            "work_guidance": self._provide_weekly_work_guidance(weekly_analysis),
            "health_guidance": self._provide_weekly_health_guidance(weekly_analysis)
        }

        # Add standard prediction fields that frontend expects
        week_theme = self._get_weekly_theme(current_dasha)
        prediction.prediction_text = f"This week brings {week_theme} energy with steady building towards mid-week peak. Focus on important communications, creative projects, and relationship building."
        prediction.key_themes = [
            week_theme,
            "Communication and collaboration",
            "Creative expression opportunities",
            "Relationship development",
            "Work-life balance"
        ]
        prediction.favorable_periods = [
            "Monday: Great for new beginnings and fresh starts",
            "Wednesday: Excellent for important meetings and decisions",
            "Friday: Favorable for creative projects and social connections",
            "Weekend: Perfect for rest and relationship time"
        ]
        prediction.challenging_periods = [
            "Mid-week: Communication challenges possible",
            "Thursday: Relationship tensions may arise",
            "Weekend: Energy depletion - prioritize rest"
        ]

        prediction.weekly_analysis = weekly_analysis
        prediction.guidance = weekly_guidance
        prediction.confidence_score = 0.8

        return prediction

    def _generate_monthly_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                                   current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate monthly prediction with comprehensive themes."""
        prediction = SpecializedPrediction(PredictionType.MONTHLY, SpecializationLevel.ADVANCED)

        # Monthly analysis
        monthly_analysis = {
            "month_theme": self._get_monthly_theme(current_dasha),
            "lunar_cycle_influence": self._analyze_lunar_cycle_influence(),
            "monthly_transits": self._get_monthly_transits(chart),
            "growth_areas": self._identify_monthly_growth_areas(chart),
            "monthly_challenges": self._identify_monthly_challenges(chart)
        }

        # Monthly guidance
        monthly_guidance = {
            "monthly_priorities": self._provide_monthly_priorities(monthly_analysis),
            "goal_setting": self._provide_monthly_goal_guidance(monthly_analysis),
            "relationship_development": self._provide_monthly_relationship_guidance(monthly_analysis),
            "career_advancement": self._provide_monthly_career_guidance(monthly_analysis),
            "personal_development": self._provide_monthly_personal_guidance(monthly_analysis)
        }

        # Add standard prediction fields that frontend expects
        month_theme = self._get_monthly_theme(current_dasha)
        prediction.prediction_text = f"This month brings {month_theme} energy with lunar cycles supporting fresh starts and manifestation. Focus on long-term goal advancement, relationship deepening, and personal development."
        prediction.key_themes = [
            month_theme,
            "Long-term goal advancement",
            "Relationship development",
            "Professional skill building",
            "Personal growth and learning"
        ]
        prediction.favorable_periods = [
            "New Moon: Excellent for setting new goals and intentions",
            "First Quarter: Good for taking action on plans",
            "Full Moon: Peak manifestation and emotional clarity",
            "Month-end: Perfect for review and planning ahead"
        ]
        prediction.challenging_periods = [
            "Mid-month: Energy fluctuations may occur",
            "Third Quarter: Communication misunderstandings possible",
            "Financial planning: Requires extra attention this month"
        ]

        prediction.monthly_analysis = monthly_analysis
        prediction.guidance = monthly_guidance
        prediction.confidence_score = 0.85

        return prediction

    def _generate_yearly_prediction(self, request: EnhancedPredictionRequest, chart: VedicChart,
                                  current_dasha: DashaPeriod) -> SpecializedPrediction:
        """Generate yearly prediction with long-term planning."""
        prediction = SpecializedPrediction(PredictionType.YEARLY, SpecializationLevel.EXPERT)

        # Yearly analysis
        yearly_analysis = {
            "year_theme": self._get_yearly_theme(current_dasha),
            "major_transits": self._get_yearly_major_transits(chart),
            "life_phase_analysis": self._analyze_current_life_phase(chart, current_dasha),
            "growth_opportunities": self._identify_yearly_growth_opportunities(chart),
            "major_challenges": self._identify_yearly_challenges(chart)
        }

        # Yearly guidance
        yearly_guidance = {
            "yearly_vision": self._provide_yearly_vision(yearly_analysis),
            "quarterly_breakdown": self._provide_quarterly_breakdown(yearly_analysis),
            "major_decisions": self._provide_major_decision_guidance(yearly_analysis),
            "relationship_evolution": self._provide_yearly_relationship_guidance(yearly_analysis),
            "career_trajectory": self._provide_yearly_career_guidance(yearly_analysis)
        }

        # Add standard prediction fields that frontend expects
        year_theme = self._get_yearly_theme(current_dasha)
        prediction.prediction_text = f"This year brings {year_theme} energy with major transits supporting significant growth and transformation. Focus on long-term vision, strategic planning, and building foundations for future success."
        prediction.key_themes = [
            year_theme,
            "Major career advancement possibilities",
            "Significant relationship developments",
            "Spiritual and personal growth acceleration",
            "Long-term foundation building"
        ]
        prediction.favorable_periods = [
            "Q1: Foundation building and strategic planning",
            "Q2: Active implementation and growth phase",
            "Q3: Refinement and course correction opportunities",
            "Q4: Completion and preparation for next cycle"
        ]
        prediction.challenging_periods = [
            "Mid-year: Patience required for long-term goals",
            "Q3: Balancing multiple life priorities",
            "Year-end: Adapting to significant life changes"
        ]

        prediction.yearly_analysis = yearly_analysis
        prediction.guidance = yearly_guidance
        prediction.confidence_score = 0.9

        return prediction

    # Implementation methods for timeframe predictions
    def _get_current_lunar_day(self) -> str:
        """Get current lunar day information."""
        return "Waxing Moon - Day 8 (Ashtami)"

    def _get_daily_planetary_influences(self, chart: VedicChart) -> List[str]:
        """Get daily planetary influences."""
        return [
            "Moon in favorable position for emotional clarity",
            "Mercury supports communication and learning",
            "Venus enhances creativity and relationships"
        ]

    def _calculate_favorable_hours(self) -> List[str]:
        """Calculate favorable hours for the day."""
        return [
            "6:00 AM - 8:00 AM: Excellent for meditation and planning",
            "2:00 PM - 4:00 PM: Good for important communications",
            "7:00 PM - 9:00 PM: Favorable for family time and relationships"
        ]

    def _identify_daily_challenges(self, chart: VedicChart) -> List[str]:
        """Identify daily challenges."""
        return [
            "Avoid major financial decisions in the afternoon",
            "Be patient with technology issues",
            "Watch for miscommunications in the evening"
        ]

    def _identify_daily_opportunities(self, chart: VedicChart) -> List[str]:
        """Identify daily opportunities."""
        return [
            "Great day for creative projects",
            "Favorable for networking and social connections",
            "Good time for learning new skills"
        ]

    def _provide_morning_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide morning guidance."""
        return [
            "Start with meditation or quiet reflection",
            "Set clear intentions for the day",
            "Focus on important tasks early"
        ]

    def _provide_afternoon_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide afternoon guidance."""
        return [
            "Good time for meetings and collaborations",
            "Handle routine tasks efficiently",
            "Take breaks to maintain energy"
        ]

    def _provide_evening_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide evening guidance."""
        return [
            "Wind down with relaxing activities",
            "Spend quality time with loved ones",
            "Reflect on the day's achievements"
        ]

    def _suggest_daily_activities(self, analysis: Dict[str, Any]) -> List[str]:
        """Suggest activities to focus on."""
        return [
            "Creative writing or artistic pursuits",
            "Important conversations with family",
            "Learning or skill development"
        ]

    def _suggest_activities_to_avoid(self, analysis: Dict[str, Any]) -> List[str]:
        """Suggest activities to avoid."""
        return [
            "Major financial investments",
            "Confrontational discussions",
            "Starting new long-term projects"
        ]

    # Weekly prediction helper methods
    def _get_weekly_theme(self, current_dasha: DashaPeriod) -> str:
        """Get weekly theme based on current dasha."""
        themes = {
            "Sun": "Leadership and Self-Expression Week",
            "Moon": "Emotional Healing and Intuition Week",
            "Mars": "Action and Energy Week",
            "Mercury": "Communication and Learning Week",
            "Jupiter": "Growth and Wisdom Week",
            "Venus": "Relationships and Creativity Week",
            "Saturn": "Discipline and Structure Week"
        }
        return themes.get(current_dasha.planet, "Personal Development Week")

    def _get_weekly_transits(self, chart: VedicChart) -> List[str]:
        """Get weekly planetary transits."""
        return [
            "Moon transiting through favorable houses",
            "Mercury supporting communication",
            "Venus enhancing relationships"
        ]

    def _analyze_weekly_energy_flow(self, chart: VedicChart) -> str:
        """Analyze weekly energy flow."""
        return "Steady energy building towards mid-week peak, then gentle decline"

    def _identify_weekly_challenges(self, chart: VedicChart) -> List[str]:
        """Identify weekly challenges."""
        return [
            "Mid-week communication challenges",
            "Weekend energy depletion",
            "Relationship tensions on Thursday"
        ]

    def _identify_weekly_opportunities(self, chart: VedicChart) -> List[str]:
        """Identify weekly opportunities."""
        return [
            "Monday: Great for new beginnings",
            "Wednesday: Excellent for important meetings",
            "Friday: Favorable for creative projects"
        ]

    def _provide_weekly_focus(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide weekly focus areas."""
        return [
            "Prioritize important communications",
            "Build stronger relationships",
            "Focus on creative expression"
        ]

    def _provide_weekly_planning(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide weekly planning suggestions."""
        return [
            "Schedule important meetings mid-week",
            "Plan creative activities for Friday",
            "Reserve weekend for rest and reflection"
        ]

    def _provide_weekly_relationship_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide weekly relationship guidance."""
        return [
            "Express appreciation to loved ones",
            "Have important conversations early in week",
            "Plan quality time together on weekend"
        ]

    def _provide_weekly_work_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide weekly work guidance."""
        return [
            "Focus on collaborative projects",
            "Present ideas and proposals mid-week",
            "Complete routine tasks efficiently"
        ]

    def _provide_weekly_health_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide weekly health guidance."""
        return [
            "Maintain consistent exercise routine",
            "Pay attention to stress levels mid-week",
            "Prioritize rest and recovery on weekend"
        ]

    # Monthly prediction helper methods
    def _get_monthly_theme(self, current_dasha: DashaPeriod) -> str:
        """Get monthly theme based on current dasha."""
        themes = {
            "Sun": "Personal Power and Authority Month",
            "Moon": "Emotional Growth and Intuition Month",
            "Mars": "Action and Achievement Month",
            "Mercury": "Learning and Communication Month",
            "Jupiter": "Expansion and Wisdom Month",
            "Venus": "Love and Creativity Month",
            "Saturn": "Discipline and Long-term Building Month"
        }
        return themes.get(current_dasha.planet, "Personal Development Month")

    def _analyze_lunar_cycle_influence(self) -> str:
        """Analyze lunar cycle influence for the month."""
        return "New Moon brings fresh starts, Full Moon amplifies emotions and manifestation"

    def _get_monthly_transits(self, chart: VedicChart) -> List[str]:
        """Get monthly planetary transits."""
        return [
            "Jupiter transit supports growth and expansion",
            "Saturn transit requires patience and discipline",
            "Venus transit enhances relationships and creativity"
        ]

    def _identify_monthly_growth_areas(self, chart: VedicChart) -> List[str]:
        """Identify monthly growth areas."""
        return [
            "Professional skill development",
            "Relationship deepening",
            "Creative expression expansion"
        ]

    def _identify_monthly_challenges(self, chart: VedicChart) -> List[str]:
        """Identify monthly challenges."""
        return [
            "Mid-month energy fluctuations",
            "Communication misunderstandings",
            "Financial planning requirements"
        ]

    def _provide_monthly_priorities(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide monthly priorities."""
        return [
            "Focus on long-term goal advancement",
            "Strengthen important relationships",
            "Invest in personal development"
        ]

    def _provide_monthly_goal_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide monthly goal guidance."""
        return [
            "Set 2-3 achievable major goals",
            "Break goals into weekly milestones",
            "Review and adjust goals mid-month"
        ]

    def _provide_monthly_relationship_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide monthly relationship guidance."""
        return [
            "Deepen existing relationships",
            "Address any ongoing conflicts",
            "Create new meaningful connections"
        ]

    def _provide_monthly_career_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide monthly career guidance."""
        return [
            "Take on challenging projects",
            "Showcase your skills and achievements",
            "Network with industry professionals"
        ]

    def _provide_monthly_personal_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide monthly personal guidance."""
        return [
            "Develop new skills or hobbies",
            "Practice mindfulness and self-reflection",
            "Maintain healthy lifestyle habits"
        ]

    # Yearly prediction helper methods
    def _get_yearly_theme(self, current_dasha: DashaPeriod) -> str:
        """Get yearly theme based on current dasha."""
        themes = {
            "Sun": "Year of Leadership and Self-Realization",
            "Moon": "Year of Emotional Mastery and Intuition",
            "Mars": "Year of Action and Achievement",
            "Mercury": "Year of Learning and Communication",
            "Jupiter": "Year of Growth and Expansion",
            "Venus": "Year of Love and Creative Expression",
            "Saturn": "Year of Discipline and Foundation Building"
        }
        return themes.get(current_dasha.planet, "Year of Personal Transformation")

    def _get_yearly_major_transits(self, chart: VedicChart) -> List[str]:
        """Get yearly major transits."""
        return [
            "Jupiter's transit through 5th house brings creative opportunities",
            "Saturn's influence requires patience in career matters",
            "Rahu-Ketu axis shift impacts life direction"
        ]

    def _analyze_current_life_phase(self, chart: VedicChart, current_dasha: DashaPeriod) -> str:
        """Analyze current life phase."""
        return f"Currently in {current_dasha.planet} dasha - a period of {current_dasha.planet.lower()} energy and themes"

    def _identify_yearly_growth_opportunities(self, chart: VedicChart) -> List[str]:
        """Identify yearly growth opportunities."""
        return [
            "Major career advancement possibilities",
            "Significant relationship developments",
            "Spiritual and personal growth acceleration"
        ]

    def _identify_yearly_challenges(self, chart: VedicChart) -> List[str]:
        """Identify yearly challenges."""
        return [
            "Need for patience in long-term goals",
            "Balancing multiple life priorities",
            "Adapting to significant life changes"
        ]

    def _provide_yearly_vision(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide yearly vision guidance."""
        return [
            "Envision your ideal life 12 months from now",
            "Align actions with long-term values",
            "Create a legacy of meaningful achievements"
        ]

    def _provide_quarterly_breakdown(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide quarterly breakdown."""
        return [
            "Q1: Foundation building and planning",
            "Q2: Active implementation and growth",
            "Q3: Refinement and course correction",
            "Q4: Completion and preparation for next cycle"
        ]

    def _provide_major_decision_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide major decision guidance."""
        return [
            "Consider long-term implications carefully",
            "Seek advice from trusted mentors",
            "Trust your intuition alongside logical analysis"
        ]

    def _provide_yearly_relationship_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide yearly relationship guidance."""
        return [
            "Invest in relationships that support your growth",
            "Release connections that no longer serve you",
            "Create deeper intimacy and understanding"
        ]

    def _provide_yearly_career_guidance(self, analysis: Dict[str, Any]) -> List[str]:
        """Provide yearly career guidance."""
        return [
            "Position yourself for significant advancement",
            "Develop expertise in emerging areas",
            "Build a strong professional network"
        ]