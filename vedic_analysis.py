"""
Comprehensive Vedic Astrology Analysis Module
Provides detailed explanations, planetary relationships, and guidance
"""

from typing import Dict, List, Tuple, Any
from datetime import date, datetime, timedelta
import swisseph as swe
from models import VedicChart, DashaPeriod, PlanetPosition, BirthData, LocationData
from utils import julian_day_from_datetime, calculate_ayanamsa, degrees_to_sign_and_degree

class VedicAnalyzer:
    def __init__(self):
        # Dasha meanings and characteristics
        self.dasha_meanings = {
            "Sun": {
                "nature": "Royal, authoritative, leadership-oriented",
                "themes": ["Leadership", "Authority", "Government", "Father", "Soul purpose", "Recognition"],
                "positive": "Brings leadership opportunities, recognition, government favor, spiritual growth",
                "negative": "Can cause ego issues, conflicts with authority, health problems related to heart/bones",
                "guidance": "Focus on leadership roles, seek recognition for your work, maintain humility",
                "cautions": "Avoid ego clashes, be careful with authority figures, monitor heart health"
            },
            "Moon": {
                "nature": "Emotional, nurturing, intuitive, changeable",
                "themes": ["Emotions", "Mother", "Mind", "Public", "Travel", "Liquids", "Nursing"],
                "positive": "Enhances intuition, brings emotional fulfillment, good for public relations",
                "negative": "Can cause emotional instability, mental stress, issues with mother",
                "guidance": "Trust your intuition, focus on emotional well-being, engage with public",
                "cautions": "Avoid emotional decisions, manage stress, be careful with water-related activities"
            },
            "Mars": {
                "nature": "Energetic, aggressive, action-oriented, competitive",
                "themes": ["Energy", "Courage", "Sports", "Military", "Surgery", "Real estate", "Brothers"],
                "positive": "Brings courage, energy for new projects, success in competitions",
                "negative": "Can cause accidents, conflicts, anger issues, blood-related problems",
                "guidance": "Channel energy into sports/exercise, take calculated risks, be courageous",
                "cautions": "Control anger, avoid accidents, be careful with sharp objects, manage conflicts"
            },
            "Mercury": {
                "nature": "Intellectual, communicative, analytical, versatile",
                "themes": ["Communication", "Business", "Education", "Writing", "Travel", "Friends"],
                "positive": "Enhances communication skills, brings business success, educational achievements",
                "negative": "Can cause nervous disorders, speech problems, deception in business",
                "guidance": "Focus on communication, pursue education, engage in business activities",
                "cautions": "Verify information carefully, avoid nervous stress, be honest in dealings"
            },
            "Jupiter": {
                "nature": "Wise, spiritual, expansive, benevolent",
                "themes": ["Wisdom", "Spirituality", "Teaching", "Children", "Wealth", "Dharma"],
                "positive": "Brings wisdom, spiritual growth, wealth, good fortune, children's welfare",
                "negative": "Can cause over-optimism, weight gain, liver problems, false gurus",
                "guidance": "Pursue spiritual practices, teach others, focus on dharmic activities",
                "cautions": "Avoid over-indulgence, be selective with spiritual teachers, manage weight"
            },
            "Venus": {
                "nature": "Artistic, romantic, luxurious, harmonious",
                "themes": ["Love", "Marriage", "Arts", "Beauty", "Luxury", "Vehicles", "Women"],
                "positive": "Brings love, artistic success, material comforts, harmonious relationships",
                "negative": "Can cause relationship problems, over-indulgence, kidney issues",
                "guidance": "Focus on relationships, pursue artistic endeavors, enjoy life's pleasures",
                "cautions": "Avoid over-indulgence, be careful in relationships, monitor kidney health"
            },
            "Saturn": {
                "nature": "Disciplined, restrictive, karmic, patient",
                "themes": ["Discipline", "Hard work", "Karma", "Delays", "Service", "Elderly", "Longevity"],
                "positive": "Brings discipline, long-term success, spiritual growth through hardship",
                "negative": "Can cause delays, depression, chronic health issues, poverty",
                "guidance": "Practice patience, work hard consistently, serve others, learn from difficulties",
                "cautions": "Avoid shortcuts, manage depression, take care of bones/joints, be patient"
            },
            "Rahu": {
                "nature": "Ambitious, materialistic, unconventional, illusory",
                "themes": ["Ambition", "Foreign lands", "Technology", "Illusion", "Sudden gains", "Unconventional"],
                "positive": "Brings sudden success, foreign opportunities, technological advancement",
                "negative": "Can cause confusion, addiction, deception, sudden losses",
                "guidance": "Pursue unconventional paths, embrace technology, seek foreign connections",
                "cautions": "Avoid get-rich-quick schemes, be wary of deception, stay grounded"
            },
            "Ketu": {
                "nature": "Spiritual, detached, mystical, karmic",
                "themes": ["Spirituality", "Detachment", "Past karma", "Mysticism", "Liberation", "Research"],
                "positive": "Brings spiritual insights, detachment from materialism, mystical experiences",
                "negative": "Can cause confusion, isolation, health issues, lack of direction",
                "guidance": "Focus on spiritual practices, research deeply, let go of attachments",
                "cautions": "Avoid isolation, seek spiritual guidance, maintain physical health"
            }
        }
        
        # House meanings
        self.house_meanings = {
            1: "Self, personality, appearance, health, general life direction",
            2: "Wealth, family, speech, food, values, accumulated resources",
            3: "Courage, siblings, short journeys, communication, efforts",
            4: "Home, mother, education, property, emotional foundation",
            5: "Children, creativity, intelligence, romance, speculation",
            6: "Health, enemies, service, daily routine, obstacles",
            7: "Marriage, partnerships, business, public relations",
            8: "Transformation, occult, longevity, sudden events, inheritance",
            9: "Dharma, higher learning, father, spirituality, fortune",
            10: "Career, reputation, authority, public image, achievements",
            11: "Gains, friends, aspirations, elder siblings, income",
            12: "Losses, spirituality, foreign lands, expenses, liberation"
        }

    def analyze_dasha_significance(self, current_dasha: DashaPeriod, chart: VedicChart) -> Dict[str, Any]:
        """Provide detailed analysis of current dasha period."""
        planet = current_dasha.planet
        dasha_info = self.dasha_meanings.get(planet, {})
        
        # Find the planet's position in the chart
        planet_position = None
        for p in chart.planets:
            if p.name == planet:
                planet_position = p
                break
        
        analysis = {
            "planet_nature": dasha_info.get("nature", ""),
            "key_themes": dasha_info.get("themes", []),
            "positive_effects": dasha_info.get("positive", ""),
            "negative_effects": dasha_info.get("negative", ""),
            "guidance": dasha_info.get("guidance", ""),
            "cautions": dasha_info.get("cautions", ""),
            "house_influence": "",
            "sign_influence": "",
            "remaining_period": f"{current_dasha.remaining_years:.1f} years",
            "significance": self._get_dasha_significance(planet, planet_position)
        }
        
        if planet_position:
            analysis["house_influence"] = f"Influencing {self.house_meanings.get(planet_position.house, 'Unknown')} (House {planet_position.house})"
            analysis["sign_influence"] = f"Operating through {planet_position.sign} energy"
        
        return analysis

    def _get_dasha_significance(self, planet: str, position: PlanetPosition = None) -> str:
        """Get detailed significance of the dasha period."""
        base_significance = {
            "Sun": "This is a period of self-realization and leadership development. The Sun Dasha activates your soul's purpose and brings opportunities for recognition and authority. It's a time to step into leadership roles and express your authentic self.",
            "Moon": "This period emphasizes emotional growth and mental development. The Moon Dasha brings focus to family, home, and inner emotional world. It's excellent for nurturing relationships and developing intuitive abilities.",
            "Mars": "This is an action-oriented period filled with energy and drive. Mars Dasha brings courage to face challenges and initiate new projects. It's a time for competition, sports, and assertive action.",
            "Mercury": "This period enhances intellectual abilities and communication skills. Mercury Dasha is excellent for education, business, writing, and all forms of communication. It brings versatility and analytical thinking.",
            "Jupiter": "This is one of the most auspicious periods, bringing wisdom and spiritual growth. Jupiter Dasha enhances dharma, teaching abilities, and brings good fortune. It's excellent for spiritual practices and higher learning.",
            "Venus": "This period focuses on relationships, creativity, and material pleasures. Venus Dasha brings opportunities for love, artistic expression, and material comforts. It's a time for harmony and beauty.",
            "Saturn": "This is a karmic period requiring patience and hard work. Saturn Dasha teaches important life lessons through challenges and delays. Success comes through persistent effort and discipline.",
            "Rahu": "This period brings ambition and desire for material success. Rahu Dasha can bring sudden opportunities and unconventional paths. It requires staying grounded while pursuing ambitious goals.",
            "Ketu": "This is a spiritual period emphasizing detachment and inner growth. Ketu Dasha brings mystical experiences and encourages letting go of material attachments. It's excellent for spiritual practices."
        }
        
        return base_significance.get(planet, "This period brings unique opportunities for growth and learning.")

    def analyze_planetary_relationships(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze relationships between planets and their significance."""
        relationships = {
            "conjunctions": [],
            "oppositions": [],
            "aspects": [],
            "house_lords": {},
            "yogas": [],
            "significance": ""
        }
        
        # Analyze conjunctions (planets in same sign)
        sign_groups = {}
        for planet in chart.planets:
            if planet.sign not in sign_groups:
                sign_groups[planet.sign] = []
            sign_groups[planet.sign].append(planet.name)
        
        for sign, planets in sign_groups.items():
            if len(planets) > 1:
                relationships["conjunctions"].append({
                    "sign": sign,
                    "planets": planets,
                    "meaning": self._interpret_conjunction(planets, sign)
                })
        
        # Analyze oppositions (planets 180 degrees apart)
        for i, planet1 in enumerate(chart.planets):
            for planet2 in chart.planets[i+1:]:
                angle_diff = abs(planet1.longitude - planet2.longitude)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                if 175 <= angle_diff <= 185:  # Opposition (within 10 degrees)
                    relationships["oppositions"].append({
                        "planets": [planet1.name, planet2.name],
                        "meaning": self._interpret_opposition(planet1.name, planet2.name)
                    })
        
        # Analyze house lordships
        relationships["house_lords"] = self._analyze_house_lords(chart)
        
        # Identify important yogas
        relationships["yogas"] = self._identify_yogas(chart)
        
        return relationships

    def _interpret_conjunction(self, planets: List[str], sign: str) -> str:
        """Interpret the meaning of planetary conjunctions."""
        if len(planets) == 2:
            planet1, planet2 = planets
            combinations = {
                ("Sun", "Moon"): f"New Moon energy in {sign} - Integration of conscious and unconscious mind",
                ("Sun", "Mercury"): f"Budhaditya Yoga in {sign} - Enhanced intelligence and communication",
                ("Sun", "Venus"): f"Creative leadership in {sign} - Artistic authority and charm",
                ("Moon", "Mars"): f"Emotional intensity in {sign} - Strong feelings and quick reactions",
                ("Mercury", "Venus"): f"Artistic communication in {sign} - Beautiful speech and creative writing",
                ("Jupiter", "Venus"): f"Wealth and wisdom in {sign} - Material and spiritual abundance",
            }
            
            key = tuple(sorted([planet1, planet2]))
            return combinations.get(key, f"Combined energies of {planet1} and {planet2} in {sign}")
        
        return f"Multiple planetary energies combining in {sign} - Complex and powerful influence"

    def _interpret_opposition(self, planet1: str, planet2: str) -> str:
        """Interpret the meaning of planetary oppositions."""
        oppositions = {
            ("Sun", "Moon"): "Full Moon energy - Heightened emotions and consciousness",
            ("Sun", "Saturn"): "Authority vs. discipline - Tension between ego and responsibility",
            ("Moon", "Mars"): "Emotional vs. action - Need to balance feelings with decisive action",
            ("Mercury", "Jupiter"): "Details vs. big picture - Balance practical and philosophical thinking",
        }
        
        key = tuple(sorted([planet1, planet2]))
        return oppositions.get(key, f"Tension between {planet1} and {planet2} energies requiring balance")

    def _analyze_house_lords(self, chart: VedicChart) -> Dict[str, str]:
        """Analyze house lordships and their significance."""
        # This is a simplified version - full implementation would require complex calculations
        return {
            "ascendant_lord": "Determines overall life direction and personality",
            "moon_lord": "Influences emotional nature and mental tendencies",
            "sun_lord": "Affects soul purpose and life vitality"
        }

    def _identify_yogas(self, chart: VedicChart) -> List[Dict[str, str]]:
        """Identify important yogas (planetary combinations)."""
        yogas = []
        
        # Check for Gaja Kesari Yoga (Jupiter and Moon in kendras from each other)
        jupiter_pos = next((p for p in chart.planets if p.name == "Jupiter"), None)
        moon_pos = next((p for p in chart.planets if p.name == "Moon"), None)
        
        if jupiter_pos and moon_pos:
            house_diff = abs(jupiter_pos.house - moon_pos.house)
            if house_diff in [0, 3, 6, 9]:  # Kendras
                yogas.append({
                    "name": "Gaja Kesari Yoga",
                    "description": "Jupiter and Moon in kendras - Brings wisdom, wealth, and respect",
                    "strength": "Strong"
                })
        
        # Check for Budhaditya Yoga (Sun and Mercury together)
        sun_pos = next((p for p in chart.planets if p.name == "Sun"), None)
        mercury_pos = next((p for p in chart.planets if p.name == "Mercury"), None)
        
        if sun_pos and mercury_pos and sun_pos.sign == mercury_pos.sign:
            yogas.append({
                "name": "Budhaditya Yoga",
                "description": "Sun and Mercury together - Enhances intelligence and communication",
                "strength": "Moderate"
            })
        
        return yogas

    def get_current_transits(self, birth_data: BirthData, location_data: LocationData) -> List[Dict[str, Any]]:
        """Calculate current planetary transits and their effects."""
        current_date = datetime.now()
        julian_day = julian_day_from_datetime(current_date)
        ayanamsa = calculate_ayanamsa(julian_day)
        
        transits = []
        
        # Calculate current positions of slow-moving planets
        slow_planets = {
            swe.JUPITER: "Jupiter",
            swe.SATURN: "Saturn",
            swe.MEAN_NODE: "Rahu"
        }
        
        for planet_id, planet_name in slow_planets.items():
            try:
                pos, _ = swe.calc_ut(julian_day, planet_id)
                longitude = (pos[0] - ayanamsa) % 360
                sign, _ = degrees_to_sign_and_degree(longitude, vedic=True)
                
                transit_effect = self._get_transit_effect(planet_name, sign)
                
                transits.append({
                    "planet": planet_name,
                    "current_sign": sign,
                    "effect": transit_effect,
                    "duration": self._get_transit_duration(planet_name),
                    "significance": self._get_transit_significance(planet_name, sign)
                })
                
            except Exception as e:
                print(f"Error calculating transit for {planet_name}: {e}")
        
        return transits

    def _get_transit_effect(self, planet: str, sign: str) -> str:
        """Get the effect of a planet transiting through a sign."""
        effects = {
            "Jupiter": f"Jupiter in {sign} brings expansion, wisdom, and good fortune to {sign} related matters",
            "Saturn": f"Saturn in {sign} brings discipline, challenges, and karmic lessons to {sign} related areas",
            "Rahu": f"Rahu in {sign} brings ambition, unconventional approaches, and material desires in {sign} areas"
        }
        return effects.get(planet, f"{planet} influencing {sign} energies")

    def _get_transit_duration(self, planet: str) -> str:
        """Get typical duration of planetary transits."""
        durations = {
            "Jupiter": "Approximately 1 year per sign",
            "Saturn": "Approximately 2.5 years per sign", 
            "Rahu": "Approximately 1.5 years per sign"
        }
        return durations.get(planet, "Variable duration")

    def _get_transit_significance(self, planet: str, sign: str) -> str:
        """Get the significance of current transit."""
        return f"This transit influences how {planet}'s energy manifests through {sign} characteristics, affecting related life areas and themes."
