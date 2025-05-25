"""
Current Day/Month Astrological Influences
Calculates how current planetary positions affect the individual
"""

from datetime import date, datetime, timedelta
from typing import Dict, List, Any, Tuple
import swisseph as swe
from models import VedicChart, BirthData, LocationData
from utils import julian_day_from_datetime, calculate_ayanamsa, degrees_to_sign_and_degree, VEDIC_SIGNS

class CurrentInfluenceAnalyzer:
    def __init__(self):
        # Current planetary themes and their effects
        self.planetary_themes = {
            "Sun": {
                "daily_theme": "Leadership and self-expression",
                "monthly_theme": "Authority and recognition",
                "effects": "Increased confidence, leadership opportunities, focus on career",
                "feelings": "More authoritative, confident, desire for recognition",
                "physical": "Increased energy, better posture, stronger presence"
            },
            "Moon": {
                "daily_theme": "Emotions and intuition",
                "monthly_theme": "Family and nurturing",
                "effects": "Heightened emotions, family focus, intuitive insights",
                "feelings": "More emotional, nurturing, intuitive, changeable moods",
                "physical": "Fluid retention, digestive changes, sleep pattern shifts"
            },
            "Mars": {
                "daily_theme": "Action and energy",
                "monthly_theme": "Competition and courage",
                "effects": "Increased activity, competitive spirit, quick decisions",
                "feelings": "More aggressive, impatient, energetic, action-oriented",
                "physical": "Higher energy, possible inflammation, increased metabolism"
            },
            "Mercury": {
                "daily_theme": "Communication and learning",
                "monthly_theme": "Business and networking",
                "effects": "Enhanced communication, learning opportunities, travel",
                "feelings": "More talkative, curious, analytical, restless",
                "physical": "Nervous energy, hand/arm activity, mental alertness"
            },
            "Jupiter": {
                "daily_theme": "Wisdom and expansion",
                "monthly_theme": "Growth and spirituality",
                "effects": "Optimism, learning, spiritual growth, good fortune",
                "feelings": "More optimistic, generous, philosophical, expansive",
                "physical": "Weight gain tendency, improved liver function, vitality"
            },
            "Venus": {
                "daily_theme": "Love and beauty",
                "monthly_theme": "Relationships and creativity",
                "effects": "Romantic feelings, artistic inspiration, social activities",
                "feelings": "More loving, artistic, social, pleasure-seeking",
                "physical": "Enhanced beauty, kidney function, reproductive health"
            },
            "Saturn": {
                "daily_theme": "Discipline and responsibility",
                "monthly_theme": "Hard work and karma",
                "effects": "Increased responsibility, disciplined approach, delays",
                "feelings": "More serious, disciplined, pessimistic, patient",
                "physical": "Joint stiffness, slower metabolism, endurance focus"
            },
            "Rahu": {
                "daily_theme": "Ambition and illusion",
                "monthly_theme": "Material desires and confusion",
                "effects": "Ambitious pursuits, unconventional approaches, confusion",
                "feelings": "More ambitious, confused, materialistic, rebellious",
                "physical": "Nervous system effects, unusual symptoms, restlessness"
            },
            "Ketu": {
                "daily_theme": "Spirituality and detachment",
                "monthly_theme": "Liberation and past karma",
                "effects": "Spiritual insights, detachment, karmic experiences",
                "feelings": "More detached, spiritual, introspective, isolated",
                "physical": "Mysterious symptoms, immune system effects, energy depletion"
            }
        }
        
        # Sign-based monthly themes
        self.sign_monthly_themes = {
            "Mesha": "New beginnings, leadership, pioneering spirit",
            "Vrishabha": "Stability, material security, sensual pleasures",
            "Mithuna": "Communication, learning, versatility",
            "Karka": "Emotions, family, nurturing, home focus",
            "Simha": "Creativity, self-expression, recognition",
            "Kanya": "Service, health, attention to detail",
            "Tula": "Relationships, balance, harmony",
            "Vrishchika": "Transformation, intensity, hidden matters",
            "Dhanu": "Philosophy, higher learning, expansion",
            "Makara": "Discipline, career, responsibility",
            "Kumbha": "Innovation, humanitarian causes, friendship",
            "Meena": "Spirituality, compassion, imagination"
        }

    def analyze_current_influences(self, birth_data: BirthData, chart: VedicChart, location_data: LocationData) -> Dict[str, Any]:
        """Analyze current day/month influences on the person."""
        current_date = datetime.now()
        julian_day = julian_day_from_datetime(current_date)
        ayanamsa = calculate_ayanamsa(julian_day)
        
        # Get current planetary positions
        current_positions = self._get_current_planetary_positions(julian_day, ayanamsa)
        
        # Analyze how current positions affect the person's chart
        personal_effects = self._analyze_personal_effects(current_positions, chart)
        
        # Get current lunar phase and its effects
        lunar_phase = self._get_current_lunar_phase(julian_day)
        
        # Get current month's dominant theme
        month_theme = self._get_current_month_theme(current_date, current_positions)
        
        # Calculate specific changes the person might feel
        daily_changes = self._calculate_daily_changes(current_positions, chart)
        monthly_changes = self._calculate_monthly_changes(month_theme, chart)
        
        return {
            "current_date": current_date.strftime("%B %d, %Y"),
            "current_positions": current_positions,
            "lunar_phase": lunar_phase,
            "month_theme": month_theme,
            "personal_effects": personal_effects,
            "daily_changes": daily_changes,
            "monthly_changes": monthly_changes,
            "recommendations": self._get_current_recommendations(current_positions, chart)
        }

    def _get_current_planetary_positions(self, julian_day: float, ayanamsa: float) -> Dict[str, Dict[str, Any]]:
        """Get current sidereal positions of all planets."""
        positions = {}
        
        planet_ids = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mars": swe.MARS,
            "Mercury": swe.MERCURY,
            "Jupiter": swe.JUPITER,
            "Venus": swe.VENUS,
            "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_NODE
        }
        
        for planet_name, planet_id in planet_ids.items():
            try:
                pos, _ = swe.calc_ut(julian_day, planet_id)
                sidereal_longitude = (pos[0] - ayanamsa) % 360
                sign, degree_in_sign = degrees_to_sign_and_degree(sidereal_longitude, vedic=True)
                
                positions[planet_name] = {
                    "longitude": sidereal_longitude,
                    "sign": sign,
                    "degree": degree_in_sign,
                    "themes": self.planetary_themes.get(planet_name, {})
                }
            except Exception as e:
                print(f"Error calculating {planet_name}: {e}")
        
        return positions

    def _get_current_lunar_phase(self, julian_day: float) -> Dict[str, Any]:
        """Calculate current lunar phase and its effects."""
        try:
            # Get Sun and Moon positions
            sun_pos, _ = swe.calc_ut(julian_day, swe.SUN)
            moon_pos, _ = swe.calc_ut(julian_day, swe.MOON)
            
            # Calculate phase angle
            phase_angle = (moon_pos[0] - sun_pos[0]) % 360
            
            # Determine phase
            if 0 <= phase_angle < 45:
                phase = "New Moon"
                effects = "New beginnings, introspection, planning"
            elif 45 <= phase_angle < 135:
                phase = "Waxing Moon"
                effects = "Growth, building energy, taking action"
            elif 135 <= phase_angle < 225:
                phase = "Full Moon"
                effects = "Peak energy, emotions heightened, completion"
            else:
                phase = "Waning Moon"
                effects = "Release, letting go, reflection"
            
            return {
                "phase": phase,
                "angle": phase_angle,
                "effects": effects,
                "emotional_impact": self._get_lunar_emotional_impact(phase)
            }
        except Exception as e:
            return {"phase": "Unknown", "effects": "Unable to calculate", "emotional_impact": ""}

    def _get_lunar_emotional_impact(self, phase: str) -> str:
        """Get emotional impact of current lunar phase."""
        impacts = {
            "New Moon": "Feeling introspective, desire for new starts, lower energy",
            "Waxing Moon": "Increasing optimism, motivation building, social energy rising",
            "Full Moon": "Emotions at peak, heightened sensitivity, intense feelings",
            "Waning Moon": "Reflective mood, releasing emotions, calming energy"
        }
        return impacts.get(phase, "")

    def _get_current_month_theme(self, current_date: datetime, positions: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Get the dominant theme for current month."""
        # Primary theme based on Sun's current sign
        sun_sign = positions.get("Sun", {}).get("sign", "Unknown")
        primary_theme = self.sign_monthly_themes.get(sun_sign, "General growth and development")
        
        # Secondary influences from other planets
        secondary_influences = []
        for planet, data in positions.items():
            if planet != "Sun":
                planet_theme = data.get("themes", {}).get("monthly_theme", "")
                if planet_theme:
                    secondary_influences.append(f"{planet}: {planet_theme}")
        
        return {
            "primary_theme": primary_theme,
            "sun_sign": sun_sign,
            "secondary_influences": secondary_influences[:3],  # Top 3 influences
            "month_name": current_date.strftime("%B %Y")
        }

    def _analyze_personal_effects(self, current_positions: Dict[str, Dict[str, Any]], chart: VedicChart) -> List[Dict[str, Any]]:
        """Analyze how current planetary positions affect the person's birth chart."""
        effects = []
        
        for current_planet, current_data in current_positions.items():
            current_sign = current_data.get("sign", "")
            
            # Find if any birth planets are in the same sign (conjunction by sign)
            for birth_planet in chart.planets:
                if birth_planet.sign == current_sign and birth_planet.name != current_planet:
                    effect = {
                        "type": "Sign Conjunction",
                        "description": f"Current {current_planet} activating your natal {birth_planet.name}",
                        "impact": f"Heightened {birth_planet.name} themes in your life",
                        "house_affected": birth_planet.house,
                        "feeling": self._get_conjunction_feeling(current_planet, birth_planet.name)
                    }
                    effects.append(effect)
            
            # Check if current planet is transiting through important houses
            for birth_planet in chart.planets:
                if birth_planet.name == current_planet:
                    # This is the same planet - check house transit
                    effect = {
                        "type": "House Transit",
                        "description": f"{current_planet} currently influencing your life themes",
                        "impact": f"Current {current_planet} energy affecting your {self._get_house_theme(birth_planet.house)}",
                        "house_affected": birth_planet.house,
                        "feeling": current_data.get("themes", {}).get("feelings", "")
                    }
                    effects.append(effect)
                    break
        
        return effects[:5]  # Return top 5 most significant effects

    def _get_conjunction_feeling(self, transiting_planet: str, natal_planet: str) -> str:
        """Get the feeling description for planetary conjunctions."""
        combinations = {
            ("Sun", "Moon"): "Feeling more integrated, confident in emotions",
            ("Mars", "Mercury"): "Quick thinking, impulsive communication",
            ("Jupiter", "Venus"): "Optimistic about relationships, generous feelings",
            ("Saturn", "Sun"): "Feeling restricted, serious about goals",
            ("Moon", "Venus"): "Emotionally romantic, nurturing feelings"
        }
        
        key = tuple(sorted([transiting_planet, natal_planet]))
        return combinations.get(key, f"Blended {transiting_planet}-{natal_planet} energy")

    def _get_house_theme(self, house: int) -> str:
        """Get the life theme for a house."""
        themes = {
            1: "personality and self-image",
            2: "wealth and family matters",
            3: "communication and siblings",
            4: "home and emotional foundation",
            5: "creativity and children",
            6: "health and daily routine",
            7: "relationships and partnerships",
            8: "transformation and hidden matters",
            9: "spirituality and higher learning",
            10: "career and public image",
            11: "gains and friendships",
            12: "spirituality and foreign connections"
        }
        return themes.get(house, "life experiences")

    def _calculate_daily_changes(self, positions: Dict[str, Dict[str, Any]], chart: VedicChart) -> List[str]:
        """Calculate specific daily changes the person might feel."""
        changes = []
        
        # Moon's daily influence (most immediate)
        moon_data = positions.get("Moon", {})
        if moon_data:
            moon_feeling = moon_data.get("themes", {}).get("feelings", "")
            if moon_feeling:
                changes.append(f"Today you may feel: {moon_feeling}")
        
        # Mercury's daily influence (communication/thinking)
        mercury_data = positions.get("Mercury", {})
        if mercury_data:
            mercury_feeling = mercury_data.get("themes", {}).get("feelings", "")
            if mercury_feeling:
                changes.append(f"Your communication style today: {mercury_feeling}")
        
        # Mars daily influence (energy/action)
        mars_data = positions.get("Mars", {})
        if mars_data:
            mars_feeling = mars_data.get("themes", {}).get("feelings", "")
            if mars_feeling:
                changes.append(f"Your energy levels: {mars_feeling}")
        
        return changes[:3]  # Top 3 daily changes

    def _calculate_monthly_changes(self, month_theme: Dict[str, Any], chart: VedicChart) -> List[str]:
        """Calculate monthly changes and trends."""
        changes = []
        
        primary_theme = month_theme.get("primary_theme", "")
        sun_sign = month_theme.get("sun_sign", "")
        
        changes.append(f"This month's focus: {primary_theme}")
        changes.append(f"With Sun in {sun_sign}, you're experiencing themes of {primary_theme.lower()}")
        
        # Add secondary influences
        secondary = month_theme.get("secondary_influences", [])
        for influence in secondary[:2]:
            changes.append(f"Additional influence: {influence}")
        
        return changes

    def _get_current_recommendations(self, positions: Dict[str, Dict[str, Any]], chart: VedicChart) -> List[str]:
        """Get recommendations based on current influences."""
        recommendations = []
        
        # Based on strongest current planetary influence
        strongest_influences = ["Jupiter", "Venus", "Sun", "Moon", "Mercury"]
        
        for planet in strongest_influences:
            if planet in positions:
                planet_data = positions[planet]
                themes = planet_data.get("themes", {})
                daily_theme = themes.get("daily_theme", "")
                
                if daily_theme:
                    if planet == "Jupiter":
                        recommendations.append("Focus on learning and spiritual growth today")
                    elif planet == "Venus":
                        recommendations.append("Good time for relationships and creative activities")
                    elif planet == "Sun":
                        recommendations.append("Take leadership roles and express yourself confidently")
                    elif planet == "Moon":
                        recommendations.append("Trust your intuition and focus on emotional well-being")
                    elif planet == "Mercury":
                        recommendations.append("Engage in communication, learning, and networking")
                
                if len(recommendations) >= 3:
                    break
        
        return recommendations[:3]
