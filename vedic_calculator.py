import swisseph as swe
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Any
import math

from models import BirthData, LocationData, PlanetPosition, VedicChart, DashaPeriod
from utils import (
    PLANET_NAMES, degrees_to_sign_and_degree, longitude_to_nakshatra,
    julian_day_from_datetime, calculate_ayanamsa, get_location_data
)

class VedicCalculator:
    def __init__(self):
        # Vimshottari Dasha periods in years
        self.dasha_periods = {
            "Ketu": 7,
            "Venus": 20,
            "Sun": 6,
            "Moon": 10,
            "Mars": 7,
            "Rahu": 18,
            "Jupiter": 16,
            "Saturn": 19,
            "Mercury": 17
        }

        # Dasha sequence
        self.dasha_sequence = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

        # EXHAUSTIVE PLANETARY DIGNITIES - Based on classical texts
        self.planetary_dignities = {
            "Sun": {
                "own_signs": ["Leo"],
                "exaltation": {"sign": "Aries", "degree": 10},
                "debilitation": {"sign": "Libra", "degree": 10},
                "moolatrikona": {"sign": "Leo", "start": 0, "end": 20},
                "friendly_signs": ["Aries", "Sagittarius", "Scorpio"],
                "enemy_signs": ["Libra", "Aquarius", "Capricorn"],
                "neutral_signs": ["Taurus", "Gemini", "Cancer", "Virgo", "Pisces"]
            },
            "Moon": {
                "own_signs": ["Cancer"],
                "exaltation": {"sign": "Taurus", "degree": 3},
                "debilitation": {"sign": "Scorpio", "degree": 3},
                "moolatrikona": {"sign": "Taurus", "start": 4, "end": 20},
                "friendly_signs": ["Taurus", "Gemini", "Cancer", "Virgo", "Libra", "Sagittarius", "Pisces"],
                "enemy_signs": [],
                "neutral_signs": ["Aries", "Leo", "Scorpio", "Capricorn", "Aquarius"]
            },
            "Mercury": {
                "own_signs": ["Gemini", "Virgo"],
                "exaltation": {"sign": "Virgo", "degree": 15},
                "debilitation": {"sign": "Pisces", "degree": 15},
                "moolatrikona": {"sign": "Virgo", "start": 16, "end": 20},
                "friendly_signs": ["Taurus", "Gemini", "Virgo", "Libra", "Capricorn", "Aquarius"],
                "enemy_signs": ["Sagittarius", "Pisces"],
                "neutral_signs": ["Aries", "Cancer", "Leo", "Scorpio"]
            },
            "Venus": {
                "own_signs": ["Taurus", "Libra"],
                "exaltation": {"sign": "Pisces", "degree": 27},
                "debilitation": {"sign": "Virgo", "degree": 27},
                "moolatrikona": {"sign": "Libra", "start": 0, "end": 15},
                "friendly_signs": ["Taurus", "Gemini", "Cancer", "Virgo", "Libra", "Capricorn", "Aquarius", "Pisces"],
                "enemy_signs": ["Aries", "Leo", "Scorpio"],
                "neutral_signs": ["Sagittarius"]
            },
            "Mars": {
                "own_signs": ["Aries", "Scorpio"],
                "exaltation": {"sign": "Capricorn", "degree": 28},
                "debilitation": {"sign": "Cancer", "degree": 28},
                "moolatrikona": {"sign": "Aries", "start": 0, "end": 12},
                "friendly_signs": ["Aries", "Cancer", "Leo", "Scorpio", "Sagittarius", "Pisces"],
                "enemy_signs": ["Taurus", "Gemini", "Virgo", "Libra", "Capricorn", "Aquarius"],
                "neutral_signs": []
            },
            "Jupiter": {
                "own_signs": ["Sagittarius", "Pisces"],
                "exaltation": {"sign": "Cancer", "degree": 5},
                "debilitation": {"sign": "Capricorn", "degree": 5},
                "moolatrikona": {"sign": "Sagittarius", "start": 0, "end": 10},
                "friendly_signs": ["Aries", "Cancer", "Leo", "Scorpio", "Sagittarius", "Pisces"],
                "enemy_signs": ["Taurus", "Gemini", "Virgo", "Libra", "Capricorn", "Aquarius"],
                "neutral_signs": []
            },
            "Saturn": {
                "own_signs": ["Capricorn", "Aquarius"],
                "exaltation": {"sign": "Libra", "degree": 20},
                "debilitation": {"sign": "Aries", "degree": 20},
                "moolatrikona": {"sign": "Aquarius", "start": 0, "end": 20},
                "friendly_signs": ["Taurus", "Gemini", "Virgo", "Libra", "Capricorn", "Aquarius"],
                "enemy_signs": ["Aries", "Cancer", "Leo", "Scorpio", "Sagittarius", "Pisces"],
                "neutral_signs": []
            },
            "Rahu": {
                "own_signs": [],
                "exaltation": {"sign": "Taurus", "degree": 20},
                "debilitation": {"sign": "Scorpio", "degree": 20},
                "moolatrikona": {"sign": "Gemini", "start": 0, "end": 30},
                "friendly_signs": ["Taurus", "Gemini", "Virgo", "Libra", "Capricorn", "Aquarius"],
                "enemy_signs": ["Cancer", "Leo", "Scorpio", "Sagittarius", "Pisces"],
                "neutral_signs": ["Aries"]
            },
            "Ketu": {
                "own_signs": [],
                "exaltation": {"sign": "Scorpio", "degree": 20},
                "debilitation": {"sign": "Taurus", "degree": 20},
                "moolatrikona": {"sign": "Sagittarius", "start": 0, "end": 30},
                "friendly_signs": ["Cancer", "Leo", "Scorpio", "Sagittarius", "Pisces"],
                "enemy_signs": ["Taurus", "Gemini", "Virgo", "Libra", "Capricorn", "Aquarius"],
                "neutral_signs": ["Aries"]
            }
        }

        # EXHAUSTIVE PLANETARY ASPECTS - Based on classical texts
        self.planetary_aspects = {
            "Sun": [7],  # 7th house aspect
            "Moon": [7],  # 7th house aspect
            "Mercury": [7],  # 7th house aspect
            "Venus": [7],  # 7th house aspect
            "Mars": [4, 7, 8],  # 4th, 7th, 8th house aspects
            "Jupiter": [5, 7, 9],  # 5th, 7th, 9th house aspects
            "Saturn": [3, 7, 10],  # 3rd, 7th, 10th house aspects
            "Rahu": [5, 7, 9],  # Same as Jupiter
            "Ketu": [5, 7, 9]   # Same as Jupiter
        }

        # DIVISIONAL CHART DIVISIONS - Based on Brihat Parashara Hora Shastra
        self.divisional_charts = {
            "D1": {"name": "Rasi", "divisions": 1, "significance": "Overall life, personality, general fortune"},
            "D2": {"name": "Hora", "divisions": 2, "significance": "Wealth, financial status, material prosperity"},
            "D3": {"name": "Drekkana", "divisions": 3, "significance": "Siblings, courage, short journeys"},
            "D4": {"name": "Chaturthamsa", "divisions": 4, "significance": "Fortune, property, vehicles"},
            "D7": {"name": "Saptamsa", "divisions": 7, "significance": "Children, creativity, progeny"},
            "D9": {"name": "Navamsa", "divisions": 9, "significance": "Marriage, spouse, spiritual strength"},
            "D10": {"name": "Dasamsa", "divisions": 10, "significance": "Career, profession, reputation"},
            "D12": {"name": "Dwadasamsa", "divisions": 12, "significance": "Parents, ancestry, family lineage"},
            "D16": {"name": "Shodasamsa", "divisions": 16, "significance": "Vehicles, comforts, happiness"},
            "D20": {"name": "Vimsamsa", "divisions": 20, "significance": "Spiritual practices, religious inclinations"},
            "D24": {"name": "Chaturvimsamsa", "divisions": 24, "significance": "Learning, education, knowledge"},
            "D27": {"name": "Bhamsa", "divisions": 27, "significance": "Strengths, weaknesses, general fortune"},
            "D30": {"name": "Trimsamsa", "divisions": 30, "significance": "Misfortunes, diseases, enemies"},
            "D40": {"name": "Khavedamsa", "divisions": 40, "significance": "Maternal relatives, auspicious events"},
            "D45": {"name": "Akshavedamsa", "divisions": 45, "significance": "Character, conduct, general behavior"},
            "D60": {"name": "Shashtyamsa", "divisions": 60, "significance": "Past life karma, overall destiny"}
        }

    def calculate_birth_chart(self, birth_data: BirthData, location_data: LocationData) -> VedicChart:
        """
        Calculate complete Vedic birth chart.
        """
        # Convert birth data to datetime
        birth_datetime = datetime.combine(birth_data.birth_date, birth_data.birth_time)
        julian_day = julian_day_from_datetime(birth_datetime)

        # Calculate ayanamsa for sidereal positions
        ayanamsa = calculate_ayanamsa(julian_day)

        # Calculate planetary positions
        planets = []
        houses = {i: [] for i in range(1, 13)}

        # Calculate positions for main planets
        for planet_id, planet_name in PLANET_NAMES.items():
            if planet_name == "Ketu":
                # Ketu is opposite to Rahu
                rahu_pos = None
                for p in planets:
                    if p.name == "Rahu":
                        rahu_pos = p
                        break
                if rahu_pos:
                    ketu_longitude = (rahu_pos.longitude + 180) % 360
                    sign, _ = degrees_to_sign_and_degree(ketu_longitude, vedic=True)
                    house = self._calculate_house(ketu_longitude, julian_day, location_data)

                    planet_pos = PlanetPosition(
                        name="Ketu",
                        longitude=ketu_longitude,
                        latitude=0,  # Ketu has no latitude
                        sign=sign,
                        house=house
                    )
                    planets.append(planet_pos)
                    houses[house].append("Ketu")
                continue

            # Calculate planet position
            try:
                pos, _ = swe.calc_ut(julian_day, planet_id)
                longitude = pos[0] - ayanamsa  # Convert to sidereal
                longitude = longitude % 360  # Normalize
                latitude = pos[1]

                sign, _ = degrees_to_sign_and_degree(longitude, vedic=True)
                house = self._calculate_house(longitude, julian_day, location_data)

                # Calculate nakshatra for Moon
                nakshatra = None
                nakshatra_pada = None
                if planet_name == "Moon":
                    nakshatra, nakshatra_pada = longitude_to_nakshatra(longitude)

                planet_pos = PlanetPosition(
                    name=planet_name,
                    longitude=longitude,
                    latitude=latitude,
                    sign=sign,
                    house=house,
                    nakshatra=nakshatra,
                    nakshatra_pada=nakshatra_pada
                )

                planets.append(planet_pos)
                houses[house].append(planet_name)

            except Exception as e:
                print(f"Error calculating {planet_name}: {e}")
                continue

        # Calculate Ascendant
        ascendant_longitude = self._calculate_ascendant(julian_day, location_data)
        ascendant_longitude = (ascendant_longitude - ayanamsa) % 360
        ascendant_sign, _ = degrees_to_sign_and_degree(ascendant_longitude, vedic=True)

        # Get Moon and Sun signs
        moon_sign = next((p.sign for p in planets if p.name == "Moon"), "Unknown")
        sun_sign = next((p.sign for p in planets if p.name == "Sun"), "Unknown")

        # Get birth nakshatra (Moon's nakshatra)
        moon_planet = next((p for p in planets if p.name == "Moon"), None)
        birth_nakshatra = moon_planet.nakshatra if moon_planet else "Unknown"
        birth_nakshatra_pada = moon_planet.nakshatra_pada if moon_planet else 1

        return VedicChart(
            planets=planets,
            houses=houses,
            ascendant=ascendant_longitude,
            ascendant_sign=ascendant_sign,
            moon_sign=moon_sign,
            sun_sign=sun_sign,
            birth_nakshatra=birth_nakshatra,
            birth_nakshatra_pada=birth_nakshatra_pada
        )

    def _calculate_ascendant(self, julian_day: float, location_data: LocationData) -> float:
        """
        Calculate ascendant (rising sign) longitude.
        """
        try:
            houses = swe.houses(julian_day, location_data.latitude, location_data.longitude, b'P')
            return houses[0][0]  # Ascendant longitude
        except Exception as e:
            print(f"Error calculating ascendant: {e}")
            return 0.0

    def _calculate_house(self, planet_longitude: float, julian_day: float, location_data: LocationData) -> int:
        """
        Calculate which house a planet is in using Placidus house system.
        """
        try:
            houses = swe.houses(julian_day, location_data.latitude, location_data.longitude, b'P')
            house_cusps = houses[0]

            # Find which house the planet is in
            for i in range(12):
                current_cusp = house_cusps[i]
                next_cusp = house_cusps[(i + 1) % 12]

                # Handle the case where house crosses 0 degrees
                if current_cusp > next_cusp:
                    if planet_longitude >= current_cusp or planet_longitude < next_cusp:
                        return i + 1
                else:
                    if current_cusp <= planet_longitude < next_cusp:
                        return i + 1

            return 1  # Default to first house if calculation fails

        except Exception as e:
            print(f"Error calculating house: {e}")
            return 1

    def calculate_current_dasha(self, birth_data: BirthData, chart: VedicChart) -> DashaPeriod:
        """
        Calculate current Vimshottari Dasha period based on Moon's nakshatra.
        """
        # Get Moon's nakshatra
        moon_nakshatra = chart.birth_nakshatra

        # Determine starting dasha lord based on nakshatra
        nakshatra_lords = {
            "Ashwini": "Ketu", "Bharani": "Venus", "Krittika": "Sun",
            "Rohini": "Moon", "Mrigashira": "Mars", "Ardra": "Rahu",
            "Punarvasu": "Jupiter", "Pushya": "Saturn", "Ashlesha": "Mercury",
            "Magha": "Ketu", "Purva Phalguni": "Venus", "Uttara Phalguni": "Sun",
            "Hasta": "Moon", "Chitra": "Mars", "Swati": "Rahu",
            "Vishakha": "Jupiter", "Anuradha": "Saturn", "Jyeshtha": "Mercury",
            "Mula": "Ketu", "Purva Ashadha": "Venus", "Uttara Ashadha": "Sun",
            "Shravana": "Moon", "Dhanishta": "Mars", "Shatabhisha": "Rahu",
            "Purva Bhadrapada": "Jupiter", "Uttara Bhadrapada": "Saturn", "Revati": "Mercury"
        }

        starting_dasha_lord = nakshatra_lords.get(moon_nakshatra, "Sun")

        # Calculate dasha start date (simplified calculation)
        # In a full implementation, this would consider the exact Moon position within the nakshatra
        birth_date = birth_data.birth_date

        # Find current dasha
        current_date = date.today()
        total_cycle = 120  # Total Vimshottari cycle is 120 years

        # Calculate elapsed time since birth
        elapsed_days = (current_date - birth_date).days
        elapsed_years = elapsed_days / 365.25

        # Find current dasha period
        current_dasha_lord, dasha_start, dasha_end, remaining_years = self._find_current_dasha_period(
            starting_dasha_lord, birth_date, elapsed_years
        )

        return DashaPeriod(
            planet=current_dasha_lord,
            start_date=dasha_start,
            end_date=dasha_end,
            level="mahadasha",
            remaining_years=remaining_years
        )

    def _find_current_dasha_period(self, starting_lord: str, birth_date: date, elapsed_years: float) -> Tuple[str, date, date, float]:
        """
        Find the current dasha period given the starting lord and elapsed time.
        """
        # Find starting position in sequence
        start_index = self.dasha_sequence.index(starting_lord)

        current_years = 0
        current_date = birth_date

        for cycle in range(2):  # Allow for one complete cycle
            for i in range(9):  # 9 dashas in sequence
                dasha_index = (start_index + i) % 9
                dasha_lord = self.dasha_sequence[dasha_index]
                dasha_duration = self.dasha_periods[dasha_lord]

                if current_years <= elapsed_years < current_years + dasha_duration:
                    # Found current dasha
                    dasha_start = current_date
                    dasha_end = current_date + timedelta(days=int(dasha_duration * 365.25))
                    remaining_years = (current_years + dasha_duration) - elapsed_years

                    return dasha_lord, dasha_start, dasha_end, remaining_years

                current_years += dasha_duration
                current_date += timedelta(days=int(dasha_duration * 365.25))

        # Fallback
        return starting_lord, birth_date, birth_date + timedelta(days=365), 1.0

    def calculate_planetary_strength(self, planet_name: str, planet_position: PlanetPosition) -> Dict[str, Any]:
        """
        Calculate comprehensive planetary strength - EXHAUSTIVE ANALYSIS.
        Based on Brihat Parashara Hora Shastra and Saravali.
        """
        if planet_name not in self.planetary_dignities:
            return {"strength": "Unknown", "score": 0, "factors": []}

        dignities = self.planetary_dignities[planet_name]
        strength_factors = []
        total_score = 0

        # 1. SIGN STRENGTH (Sthana Bala)
        sign_strength = self._calculate_sign_strength(planet_name, planet_position, dignities)
        strength_factors.append(sign_strength)
        total_score += sign_strength["score"]

        # 2. EXALTATION/DEBILITATION STRENGTH
        exalt_strength = self._calculate_exaltation_strength(planet_name, planet_position, dignities)
        strength_factors.append(exalt_strength)
        total_score += exalt_strength["score"]

        # 3. DIRECTIONAL STRENGTH (Dig Bala)
        directional_strength = self._calculate_directional_strength(planet_name, planet_position)
        strength_factors.append(directional_strength)
        total_score += directional_strength["score"]

        # 4. TEMPORAL STRENGTH (Kala Bala)
        temporal_strength = self._calculate_temporal_strength(planet_name)
        strength_factors.append(temporal_strength)
        total_score += temporal_strength["score"]

        # 5. NATURAL STRENGTH (Naisargika Bala)
        natural_strength = self._calculate_natural_strength(planet_name)
        strength_factors.append(natural_strength)
        total_score += natural_strength["score"]

        # Determine overall strength category
        if total_score >= 80:
            overall_strength = "Excellent"
        elif total_score >= 60:
            overall_strength = "Good"
        elif total_score >= 40:
            overall_strength = "Average"
        elif total_score >= 20:
            overall_strength = "Weak"
        else:
            overall_strength = "Very Weak"

        return {
            "planet": planet_name,
            "overall_strength": overall_strength,
            "total_score": total_score,
            "strength_factors": strength_factors,
            "interpretation": self._interpret_planetary_strength(planet_name, overall_strength, strength_factors)
        }

    def _calculate_sign_strength(self, planet_name: str, planet_position: PlanetPosition, dignities: Dict) -> Dict[str, Any]:
        """Calculate strength based on sign placement."""
        current_sign = planet_position.sign

        if current_sign in dignities["own_signs"]:
            return {
                "factor": "Own Sign (Swakshetra)",
                "score": 20,
                "description": f"{planet_name} is in its own sign {current_sign}, providing maximum comfort and natural expression"
            }
        elif current_sign in dignities["friendly_signs"]:
            return {
                "factor": "Friendly Sign (Mitra Kshetra)",
                "score": 15,
                "description": f"{planet_name} is in friendly sign {current_sign}, providing good support and positive expression"
            }
        elif current_sign in dignities["neutral_signs"]:
            return {
                "factor": "Neutral Sign (Sama Kshetra)",
                "score": 10,
                "description": f"{planet_name} is in neutral sign {current_sign}, providing moderate support"
            }
        elif current_sign in dignities["enemy_signs"]:
            return {
                "factor": "Enemy Sign (Shatru Kshetra)",
                "score": 5,
                "description": f"{planet_name} is in enemy sign {current_sign}, creating challenges and restrictions"
            }
        else:
            return {
                "factor": "Unknown Sign Relationship",
                "score": 10,
                "description": f"{planet_name} in {current_sign} - relationship unclear"
            }

    def _calculate_exaltation_strength(self, planet_name: str, planet_position: PlanetPosition, dignities: Dict) -> Dict[str, Any]:
        """Calculate strength based on exaltation/debilitation."""
        current_sign = planet_position.sign
        exaltation = dignities["exaltation"]
        debilitation = dignities["debilitation"]

        if current_sign == exaltation["sign"]:
            # Calculate exact exaltation strength based on degree
            exalt_degree = exaltation["degree"]
            current_degree = planet_position.longitude % 30  # Degree within sign
            degree_difference = abs(current_degree - exalt_degree)

            # Maximum strength at exact degree, decreasing with distance
            if degree_difference <= 1:
                score = 25
                strength = "Maximum Exaltation"
            elif degree_difference <= 5:
                score = 20
                strength = "High Exaltation"
            elif degree_difference <= 10:
                score = 15
                strength = "Moderate Exaltation"
            else:
                score = 10
                strength = "Weak Exaltation"

            return {
                "factor": f"Exaltation in {current_sign}",
                "score": score,
                "description": f"{planet_name} is exalted in {current_sign} - {strength}. Brings exceptional results and maximum potential."
            }

        elif current_sign == debilitation["sign"]:
            # Calculate exact debilitation weakness based on degree
            debilt_degree = debilitation["degree"]
            current_degree = planet_position.longitude % 30
            degree_difference = abs(current_degree - debilt_degree)

            # Maximum weakness at exact degree
            if degree_difference <= 1:
                score = -15
                weakness = "Maximum Debilitation"
            elif degree_difference <= 5:
                score = -10
                weakness = "High Debilitation"
            elif degree_difference <= 10:
                score = -5
                weakness = "Moderate Debilitation"
            else:
                score = 0
                weakness = "Weak Debilitation"

            return {
                "factor": f"Debilitation in {current_sign}",
                "score": score,
                "description": f"{planet_name} is debilitated in {current_sign} - {weakness}. Requires extra effort to manifest positive results."
            }

        else:
            return {
                "factor": "Neither Exalted nor Debilitated",
                "score": 0,
                "description": f"{planet_name} in {current_sign} - normal strength from exaltation perspective"
            }

    def _calculate_directional_strength(self, planet_name: str, planet_position: PlanetPosition) -> Dict[str, Any]:
        """Calculate directional strength (Dig Bala) based on house placement."""
        # Directional strengths based on classical texts
        directional_houses = {
            "Sun": 10,      # Strong in 10th house (South)
            "Moon": 4,      # Strong in 4th house (North)
            "Mercury": 1,   # Strong in 1st house (East)
            "Venus": 4,     # Strong in 4th house (North)
            "Mars": 10,     # Strong in 10th house (South)
            "Jupiter": 1,   # Strong in 1st house (East)
            "Saturn": 7,    # Strong in 7th house (West)
            "Rahu": 10,     # Strong in 10th house (South)
            "Ketu": 4       # Strong in 4th house (North)
        }

        strong_house = directional_houses.get(planet_name, 1)
        current_house = planet_position.house

        if current_house == strong_house:
            return {
                "factor": f"Directional Strength (Dig Bala)",
                "score": 15,
                "description": f"{planet_name} is in its directional strength house {current_house}, providing maximum directional power"
            }
        elif current_house == ((strong_house + 6) % 12) or current_house == ((strong_house - 6) % 12):
            return {
                "factor": "Directional Weakness",
                "score": -5,
                "description": f"{planet_name} is opposite to its directional strength, creating directional weakness"
            }
        else:
            return {
                "factor": "Neutral Directional Position",
                "score": 0,
                "description": f"{planet_name} in house {current_house} - neutral directional strength"
            }

    def _calculate_temporal_strength(self, planet_name: str) -> Dict[str, Any]:
        """Calculate temporal strength based on current time factors."""
        # Simplified temporal strength - in full implementation would consider:
        # Day/night strength, lunar month, solar month, weekday, etc.

        temporal_strengths = {
            "Sun": {"day": 15, "night": 5},
            "Moon": {"day": 5, "night": 15},
            "Mercury": {"day": 10, "night": 10},
            "Venus": {"day": 5, "night": 15},
            "Mars": {"day": 15, "night": 5},
            "Jupiter": {"day": 15, "night": 5},
            "Saturn": {"day": 5, "night": 15},
            "Rahu": {"day": 5, "night": 15},
            "Ketu": {"day": 15, "night": 5}
        }

        # Simplified: assume current time is day (in full implementation would check actual time)
        current_time = "day"
        strength_data = temporal_strengths.get(planet_name, {"day": 10, "night": 10})
        score = strength_data[current_time]

        return {
            "factor": f"Temporal Strength ({current_time}time)",
            "score": score,
            "description": f"{planet_name} has {'good' if score >= 10 else 'moderate'} temporal strength during {current_time}time"
        }

    def _calculate_natural_strength(self, planet_name: str) -> Dict[str, Any]:
        """Calculate natural strength (Naisargika Bala) - inherent planetary strength."""
        # Natural strengths based on classical texts
        natural_strengths = {
            "Sun": 15,      # Naturally strong (royal planet)
            "Moon": 12,     # Strong (queen planet)
            "Mercury": 8,   # Moderate (prince planet)
            "Venus": 10,    # Good (minister planet)
            "Mars": 12,     # Strong (commander planet)
            "Jupiter": 18,  # Strongest (guru planet)
            "Saturn": 6,    # Weak (servant planet)
            "Rahu": 8,      # Moderate (shadow planet)
            "Ketu": 8       # Moderate (shadow planet)
        }

        score = natural_strengths.get(planet_name, 10)

        return {
            "factor": "Natural Strength (Naisargika Bala)",
            "score": score,
            "description": f"{planet_name} has {'high' if score >= 15 else 'good' if score >= 10 else 'moderate'} natural strength"
        }

    def _interpret_planetary_strength(self, planet_name: str, overall_strength: str, strength_factors: List[Dict]) -> str:
        """Provide interpretation of planetary strength."""
        interpretations = {
            "Excellent": f"{planet_name} is exceptionally strong and will give excellent results. This planet can fulfill its highest potential and bring significant positive outcomes.",
            "Good": f"{planet_name} is well-placed and strong. It will generally give good results with some minor challenges that can be easily overcome.",
            "Average": f"{planet_name} has moderate strength. Results will be mixed - some positive and some challenging. Conscious effort can improve outcomes.",
            "Weak": f"{planet_name} is weak and may struggle to give positive results. Extra care and remedial measures may be needed to strengthen this planet.",
            "Very Weak": f"{planet_name} is very weak and may give challenging results. Strong remedial measures and spiritual practices are recommended."
        }

        base_interpretation = interpretations.get(overall_strength, "Strength analysis unclear.")

        # Add specific factor insights
        key_factors = [f["factor"] for f in strength_factors if f["score"] >= 15 or f["score"] <= -5]
        if key_factors:
            factor_text = ", ".join(key_factors)
            base_interpretation += f" Key strength factors: {factor_text}."

        return base_interpretation

    def generate_planetary_remedies(self, planet_name: str, planet_position: PlanetPosition, overall_strength: str, strength_factors: List[Dict]) -> Dict[str, Any]:
        """
        Generate comprehensive remedial suggestions for weak planets.
        Based on classical Vedic texts: Brihat Parashara Hora Shastra, Lal Kitab, and Jataka Parijata.
        """
        if overall_strength in ["Excellent", "Good"]:
            return {
                "remedies_needed": False,
                "message": f"{planet_name} is strong and doesn't require remedial measures. Continue current positive practices."
            }

        # Get comprehensive remedies based on planet and its weaknesses
        remedies = {
            "remedies_needed": True,
            "overall_approach": self._get_overall_remedy_approach(planet_name, overall_strength),
            "gemstone_therapy": self._get_gemstone_remedies(planet_name, planet_position),
            "mantra_therapy": self._get_mantra_remedies(planet_name),
            "yantra_therapy": self._get_yantra_remedies(planet_name),
            "color_therapy": self._get_color_remedies(planet_name),
            "metal_therapy": self._get_metal_remedies(planet_name),
            "day_specific_practices": self._get_day_specific_remedies(planet_name),
            "dietary_recommendations": self._get_dietary_remedies(planet_name),
            "charitable_activities": self._get_charity_remedies(planet_name),
            "lifestyle_modifications": self._get_lifestyle_remedies(planet_name, planet_position),
            "spiritual_practices": self._get_spiritual_remedies(planet_name),
            "timing_recommendations": self._get_timing_remedies(planet_name),
            "specific_weaknesses": self._get_specific_weakness_remedies(planet_name, strength_factors),
            "precautions": self._get_planetary_precautions(planet_name),
            "expected_timeline": self._get_remedy_timeline(planet_name, overall_strength)
        }

        return remedies

    def generate_planetary_combination_description(self, planet_name: str, planet_position: PlanetPosition) -> Dict[str, str]:
        """
        Generate detailed description of planet in sign and house combination.
        Based on classical texts: Brihat Parashara Hora Shastra, Jataka Parijata, Saravali.
        """
        sign = planet_position.sign
        house = planet_position.house

        # Get comprehensive combination analysis
        sign_influence = self._get_planet_in_sign_meaning(planet_name, sign)
        house_influence = self._get_planet_in_house_meaning(planet_name, house)
        combined_effect = self._get_combined_planet_sign_house_effect(planet_name, sign, house)
        life_manifestation = self._get_life_manifestation_description(planet_name, sign, house)
        timing_activation = self._get_timing_activation_description(planet_name, house)

        return {
            "title": f"{planet_name} in {sign} in House {house} - Comprehensive Analysis",
            "sign_influence": {
                "title": f"Sign Influence ({planet_name} in {sign})",
                "description": sign_influence
            },
            "house_influence": {
                "title": f"House Influence ({planet_name} in House {house})",
                "description": house_influence
            },
            "combined_effect": {
                "title": "Combined Effect",
                "description": combined_effect
            },
            "life_manifestation": {
                "title": "Life Manifestation",
                "description": life_manifestation
            },
            "timing_activation": {
                "title": "Timing & Activation",
                "description": timing_activation
            }
        }

    def calculate_planetary_aspects(self, chart: VedicChart) -> List[Dict[str, Any]]:
        """
        Calculate all planetary aspects - EXHAUSTIVE COVERAGE.
        Based on classical Vedic astrology aspect rules.
        """
        aspects = []

        for i, planet1 in enumerate(chart.planets):
            for j, planet2 in enumerate(chart.planets):
                if i >= j:  # Avoid duplicates and self-aspects
                    continue

                aspect_info = self._calculate_aspect_between_planets(planet1, planet2)
                if aspect_info:
                    aspects.append(aspect_info)

        return aspects

    def _calculate_aspect_between_planets(self, planet1: PlanetPosition, planet2: PlanetPosition) -> Dict[str, Any]:
        """Calculate aspect between two planets."""
        house_diff = abs(planet1.house - planet2.house)
        if house_diff > 6:
            house_diff = 12 - house_diff

        # Check if planet1 aspects planet2
        planet1_aspects = self.planetary_aspects.get(planet1.name, [7])
        planet2_aspects = self.planetary_aspects.get(planet2.name, [7])

        aspect_found = False
        aspect_type = None
        aspecting_planet = None

        if house_diff in planet1_aspects:
            aspect_found = True
            aspect_type = f"{house_diff}th house aspect"
            aspecting_planet = planet1.name
        elif house_diff in planet2_aspects:
            aspect_found = True
            aspect_type = f"{house_diff}th house aspect"
            aspecting_planet = planet2.name

        if aspect_found:
            # Calculate aspect strength based on planetary dignities and house positions
            aspect_strength = self._calculate_aspect_strength(planet1, planet2, house_diff)

            return {
                "aspecting_planet": aspecting_planet,
                "aspected_planet": planet2.name if aspecting_planet == planet1.name else planet1.name,
                "aspect_type": aspect_type,
                "house_difference": house_diff,
                "strength": aspect_strength["strength"],
                "effect": aspect_strength["effect"],
                "interpretation": self._interpret_aspect(planet1, planet2, house_diff, aspect_strength)
            }

        return None

    def _calculate_aspect_strength(self, planet1: PlanetPosition, planet2: PlanetPosition, house_diff: int) -> Dict[str, Any]:
        """Calculate the strength and effect of an aspect."""
        # Aspect strengths based on house difference
        aspect_strengths = {
            3: {"strength": "Moderate", "nature": "Growth-oriented"},
            4: {"strength": "Strong", "nature": "Protective"},
            5: {"strength": "Very Strong", "nature": "Creative"},
            7: {"strength": "Strong", "nature": "Relationship-focused"},
            8: {"strength": "Intense", "nature": "Transformative"},
            9: {"strength": "Very Strong", "nature": "Wisdom-oriented"},
            10: {"strength": "Strong", "nature": "Achievement-focused"}
        }

        base_strength = aspect_strengths.get(house_diff, {"strength": "Moderate", "nature": "General"})

        # Modify strength based on planetary nature
        benefic_planets = ["Jupiter", "Venus", "Moon", "Mercury"]
        malefic_planets = ["Mars", "Saturn", "Rahu", "Ketu", "Sun"]

        if planet1.name in benefic_planets:
            effect = "Positive"
        elif planet1.name in malefic_planets:
            effect = "Challenging"
        else:
            effect = "Neutral"

        return {
            "strength": base_strength["strength"],
            "nature": base_strength["nature"],
            "effect": effect
        }

    def _interpret_aspect(self, planet1: PlanetPosition, planet2: PlanetPosition, house_diff: int, aspect_strength: Dict) -> str:
        """Provide interpretation of planetary aspect."""
        aspecting = planet1.name
        aspected = planet2.name
        strength = aspect_strength["strength"]
        effect = aspect_strength["effect"]
        nature = aspect_strength["nature"]

        base_interpretation = f"{aspecting} casts a {strength.lower()} {house_diff}th house aspect on {aspected}, creating {effect.lower()} {nature.lower()} influence."

        # Add specific planetary combination effects
        combination_effects = {
            ("Jupiter", "Sun"): "Enhances leadership qualities and spiritual wisdom",
            ("Jupiter", "Moon"): "Brings emotional stability and good fortune",
            ("Jupiter", "Mercury"): "Enhances learning and communication abilities",
            ("Jupiter", "Venus"): "Brings wealth, luxury, and harmonious relationships",
            ("Jupiter", "Mars"): "Provides righteous courage and moral strength",
            ("Jupiter", "Saturn"): "Creates disciplined wisdom and long-term success",
            ("Venus", "Mars"): "Creates passionate relationships and artistic talents",
            ("Saturn", "Sun"): "May create delays in recognition but builds character",
            ("Saturn", "Moon"): "May cause emotional restrictions but builds resilience",
            ("Mars", "Mercury"): "Creates sharp intellect but may cause arguments",
            ("Rahu", "Sun"): "Brings unconventional leadership and sudden changes",
            ("Ketu", "Moon"): "Creates spiritual detachment and intuitive abilities"
        }

        key = tuple(sorted([aspecting, aspected]))
        if key in combination_effects:
            base_interpretation += f" Specifically, this aspect {combination_effects[key].lower()}."

        return base_interpretation

    def calculate_divisional_chart(self, chart: VedicChart, division: str) -> Dict[str, Any]:
        """
        Calculate divisional chart (Varga) - EXHAUSTIVE COVERAGE.
        Based on Brihat Parashara Hora Shastra.
        """
        if division not in self.divisional_charts:
            return {"error": f"Division {division} not supported"}

        division_info = self.divisional_charts[division]
        divisions = division_info["divisions"]

        divisional_positions = {}

        for planet in chart.planets:
            # Calculate divisional position
            sign_number = self._get_sign_number(planet.sign)
            degree_in_sign = planet.longitude % 30

            # Calculate divisional sign based on division type
            if division == "D2":  # Hora chart
                divisional_sign = self._calculate_hora_position(sign_number, degree_in_sign)
            elif division == "D3":  # Drekkana chart
                divisional_sign = self._calculate_drekkana_position(sign_number, degree_in_sign)
            elif division == "D9":  # Navamsa chart
                divisional_sign = self._calculate_navamsa_position(sign_number, degree_in_sign)
            elif division == "D10":  # Dasamsa chart
                divisional_sign = self._calculate_dasamsa_position(sign_number, degree_in_sign)
            elif division == "D12":  # Dwadasamsa chart
                divisional_sign = self._calculate_dwadasamsa_position(sign_number, degree_in_sign)
            else:
                # Generic calculation for other divisions
                divisional_sign = self._calculate_generic_division(sign_number, degree_in_sign, divisions)

            divisional_positions[planet.name] = {
                "original_sign": planet.sign,
                "divisional_sign": self._get_sign_name(divisional_sign),
                "significance": self._get_divisional_significance(planet.name, division, divisional_sign)
            }

        return {
            "division": division,
            "name": division_info["name"],
            "significance": division_info["significance"],
            "planetary_positions": divisional_positions,
            "analysis": self._analyze_divisional_chart(divisional_positions, division)
        }

    def _get_sign_number(self, sign_name: str) -> int:
        """Convert sign name to number (1-12)."""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        return signs.index(sign_name) + 1 if sign_name in signs else 1

    def _get_sign_name(self, sign_number: int) -> str:
        """Convert sign number to name."""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        return signs[(sign_number - 1) % 12]

    def _calculate_hora_position(self, sign_number: int, degree: float) -> int:
        """Calculate Hora (D2) position."""
        # First 15 degrees go to Sun's hora, next 15 to Moon's hora
        if degree < 15:
            # Odd signs: Leo (Sun), Even signs: Cancer (Moon)
            return 5 if sign_number % 2 == 1 else 4  # Leo or Cancer
        else:
            # Odd signs: Cancer (Moon), Even signs: Leo (Sun)
            return 4 if sign_number % 2 == 1 else 5  # Cancer or Leo

    def _calculate_drekkana_position(self, sign_number: int, degree: float) -> int:
        """Calculate Drekkana (D3) position."""
        # Each 10-degree segment goes to a different sign
        segment = int(degree // 10)
        return ((sign_number - 1) + segment * 4) % 12 + 1

    def _calculate_navamsa_position(self, sign_number: int, degree: float) -> int:
        """Calculate Navamsa (D9) position."""
        # Each 3°20' segment goes to a different sign
        segment = int(degree // (30/9))

        # Navamsa calculation based on sign type
        if sign_number in [1, 5, 9]:  # Fire signs start from Aries
            base = 1
        elif sign_number in [2, 6, 10]:  # Earth signs start from Capricorn
            base = 10
        elif sign_number in [3, 7, 11]:  # Air signs start from Libra
            base = 7
        else:  # Water signs start from Cancer
            base = 4

        return ((base - 1) + segment) % 12 + 1

    def _calculate_dasamsa_position(self, sign_number: int, degree: float) -> int:
        """Calculate Dasamsa (D10) position."""
        # Each 3-degree segment goes to a different sign
        segment = int(degree // 3)

        # Odd signs start from same sign, even signs start from 9th sign
        if sign_number % 2 == 1:
            base = sign_number
        else:
            base = (sign_number + 8) % 12 + 1

        return ((base - 1) + segment) % 12 + 1

    def _calculate_dwadasamsa_position(self, sign_number: int, degree: float) -> int:
        """Calculate Dwadasamsa (D12) position."""
        # Each 2.5-degree segment goes to a different sign
        segment = int(degree // 2.5)
        return ((sign_number - 1) + segment) % 12 + 1

    def _calculate_generic_division(self, sign_number: int, degree: float, divisions: int) -> int:
        """Calculate generic divisional position."""
        segment = int(degree // (30 / divisions))
        return ((sign_number - 1) + segment) % 12 + 1

    def _get_divisional_significance(self, planet_name: str, division: str, divisional_sign: int) -> str:
        """Get significance of planet in divisional chart."""
        sign_name = self._get_sign_name(divisional_sign)

        # Check if planet is strong in divisional chart
        if planet_name in self.planetary_dignities:
            dignities = self.planetary_dignities[planet_name]

            if sign_name in dignities["own_signs"]:
                return f"Very strong in {division} - in own sign {sign_name}"
            elif sign_name == dignities["exaltation"]["sign"]:
                return f"Excellent in {division} - exalted in {sign_name}"
            elif sign_name in dignities["friendly_signs"]:
                return f"Good in {division} - in friendly sign {sign_name}"
            elif sign_name in dignities["enemy_signs"]:
                return f"Challenging in {division} - in enemy sign {sign_name}"
            elif sign_name == dignities["debilitation"]["sign"]:
                return f"Weak in {division} - debilitated in {sign_name}"

        return f"Moderate in {division} - in {sign_name}"

    def _analyze_divisional_chart(self, positions: Dict, division: str) -> str:
        """Provide analysis of divisional chart."""
        strong_planets = []
        weak_planets = []

        for planet, info in positions.items():
            if "Very strong" in info["significance"] or "Excellent" in info["significance"]:
                strong_planets.append(planet)
            elif "Weak" in info["significance"] or "Challenging" in info["significance"]:
                weak_planets.append(planet)

        analysis = f"In the {division} chart: "

        if strong_planets:
            analysis += f"Strong planets: {', '.join(strong_planets)}. "

        if weak_planets:
            analysis += f"Planets needing attention: {', '.join(weak_planets)}. "

        # Add division-specific insights
        division_insights = {
            "D2": "This chart shows your relationship with wealth and material resources.",
            "D3": "This chart reveals your relationship with siblings and personal courage.",
            "D9": "This chart is crucial for marriage, spouse, and spiritual development.",
            "D10": "This chart determines your career success and professional reputation.",
            "D12": "This chart shows your relationship with parents and family lineage."
        }

        if division in division_insights:
            analysis += division_insights[division]

        return analysis

    # COMPREHENSIVE REMEDY METHODS

    def _get_overall_remedy_approach(self, planet_name: str, strength: str) -> str:
        """Get overall approach for planetary remedies."""
        approaches = {
            "Sun": "Focus on building confidence, leadership qualities, and spiritual practices. Strengthen your connection with divine authority and paternal figures.",
            "Moon": "Emphasize emotional healing, nurturing practices, and connection with mother/feminine energy. Work on mental peace and intuitive development.",
            "Mars": "Channel energy constructively through physical activities, courage-building practices, and righteous action. Avoid conflicts and anger.",
            "Mercury": "Enhance communication skills, learning abilities, and intellectual pursuits. Focus on clarity of thought and speech.",
            "Jupiter": "Develop wisdom, spiritual knowledge, and teaching abilities. Connect with gurus and engage in charitable activities.",
            "Venus": "Cultivate artistic abilities, harmonious relationships, and aesthetic appreciation. Focus on love, beauty, and creativity.",
            "Saturn": "Practice discipline, patience, and service to others. Accept responsibilities and work on long-term goals with persistence.",
            "Rahu": "Ground yourself through spiritual practices and avoid excessive materialism. Focus on ethical pursuits and avoid shortcuts.",
            "Ketu": "Develop spiritual detachment while maintaining worldly responsibilities. Practice meditation and seek inner wisdom."
        }

        base_approach = approaches.get(planet_name, "Focus on balancing this planetary energy through conscious effort and spiritual practices.")

        if strength == "Very Weak":
            return f"URGENT: {base_approach} Immediate and consistent remedial measures are essential."
        elif strength == "Weak":
            return f"IMPORTANT: {base_approach} Regular remedial practices will significantly help."
        else:
            return f"MODERATE: {base_approach} Some remedial support will be beneficial."

    def _get_gemstone_remedies(self, planet_name: str, planet_position: PlanetPosition) -> Dict[str, Any]:
        """Get gemstone therapy recommendations."""
        gemstone_data = {
            "Sun": {
                "primary": "Ruby (Manik)",
                "alternatives": ["Red Garnet", "Red Spinel"],
                "weight": "3-6 carats",
                "metal": "Gold",
                "finger": "Ring finger (right hand)",
                "day_to_wear": "Sunday morning",
                "mantra_before_wearing": "Om Suryaya Namaha (108 times)",
                "benefits": "Enhances leadership, confidence, vitality, and authority",
                "precautions": "Avoid if you have high blood pressure or anger issues"
            },
            "Moon": {
                "primary": "Pearl (Moti)",
                "alternatives": ["Moonstone", "White Coral"],
                "weight": "4-7 carats",
                "metal": "Silver",
                "finger": "Little finger (right hand)",
                "day_to_wear": "Monday evening",
                "mantra_before_wearing": "Om Chandraya Namaha (108 times)",
                "benefits": "Improves emotional stability, intuition, and mental peace",
                "precautions": "Replace every 2-3 years as pearls lose energy"
            },
            "Mars": {
                "primary": "Red Coral (Moonga)",
                "alternatives": ["Carnelian", "Red Jasper"],
                "weight": "5-8 carats",
                "metal": "Gold or Copper",
                "finger": "Ring finger (right hand)",
                "day_to_wear": "Tuesday morning",
                "mantra_before_wearing": "Om Mangalaya Namaha (108 times)",
                "benefits": "Increases courage, energy, and protection from enemies",
                "precautions": "Avoid if you have excessive anger or aggression"
            },
            "Mercury": {
                "primary": "Emerald (Panna)",
                "alternatives": ["Green Tourmaline", "Peridot"],
                "weight": "3-6 carats",
                "metal": "Gold or Silver",
                "finger": "Little finger (right hand)",
                "day_to_wear": "Wednesday morning",
                "mantra_before_wearing": "Om Budhaya Namaha (108 times)",
                "benefits": "Enhances communication, intelligence, and business skills",
                "precautions": "Test for 7 days before permanent wearing"
            },
            "Jupiter": {
                "primary": "Yellow Sapphire (Pukhraj)",
                "alternatives": ["Citrine", "Yellow Topaz"],
                "weight": "4-7 carats",
                "metal": "Gold",
                "finger": "Index finger (right hand)",
                "day_to_wear": "Thursday morning",
                "mantra_before_wearing": "Om Gurave Namaha (108 times)",
                "benefits": "Brings wisdom, prosperity, and spiritual growth",
                "precautions": "Ensure high quality as low-grade stones can be harmful"
            },
            "Venus": {
                "primary": "Diamond (Heera)",
                "alternatives": ["White Sapphire", "Zircon"],
                "weight": "1-3 carats",
                "metal": "Platinum or White Gold",
                "finger": "Middle finger (right hand)",
                "day_to_wear": "Friday morning",
                "mantra_before_wearing": "Om Shukraya Namaha (108 times)",
                "benefits": "Improves relationships, creativity, and material comforts",
                "precautions": "Very expensive; alternatives work well too"
            },
            "Saturn": {
                "primary": "Blue Sapphire (Neelam)",
                "alternatives": ["Amethyst", "Lapis Lazuli"],
                "weight": "4-7 carats",
                "metal": "Silver or Iron",
                "finger": "Middle finger (right hand)",
                "day_to_wear": "Saturday evening",
                "mantra_before_wearing": "Om Shanaye Namaha (108 times)",
                "benefits": "Provides discipline, patience, and karmic protection",
                "precautions": "MUST test for 7 days - can give immediate negative effects if unsuitable"
            },
            "Rahu": {
                "primary": "Hessonite (Gomed)",
                "alternatives": ["Smoky Quartz", "Garnet"],
                "weight": "5-8 carats",
                "metal": "Silver or Panchdhatu",
                "finger": "Middle finger (right hand)",
                "day_to_wear": "Saturday evening",
                "mantra_before_wearing": "Om Rahave Namaha (108 times)",
                "benefits": "Reduces confusion, provides clarity, and material success",
                "precautions": "Test carefully as Rahu stones can be unpredictable"
            },
            "Ketu": {
                "primary": "Cat's Eye (Lehsunia)",
                "alternatives": ["Tiger's Eye", "Chrysoberyl"],
                "weight": "4-7 carats",
                "metal": "Silver or Panchdhatu",
                "finger": "Ring finger (right hand)",
                "day_to_wear": "Tuesday or Saturday",
                "mantra_before_wearing": "Om Ketave Namaha (108 times)",
                "benefits": "Enhances spiritual insight and protects from hidden enemies",
                "precautions": "Test for 7 days - can cause sudden changes"
            }
        }

        return gemstone_data.get(planet_name, {
            "primary": "Consult an expert",
            "note": "Specific gemstone recommendations require detailed analysis"
        })

    def _get_mantra_remedies(self, planet_name: str) -> Dict[str, Any]:
        """Get mantra therapy recommendations."""
        mantra_data = {
            "Sun": {
                "beej_mantra": "Om Hraam Hreem Hraum Sah Suryaya Namaha",
                "simple_mantra": "Om Suryaya Namaha",
                "gayatri_mantra": "Om Bhaskaraya Vidmahe Mahadhyutikaraya Dhimahi Tanno Aditya Prachodayat",
                "repetitions": "108 times daily or 7000 times in 40 days",
                "best_time": "Sunrise to 1 hour after sunrise",
                "direction": "Face East",
                "benefits": "Increases vitality, confidence, and leadership abilities",
                "special_days": "Sundays, Solar eclipses, Makar Sankranti"
            },
            "Moon": {
                "beej_mantra": "Om Shraam Shreem Shraum Sah Chandraya Namaha",
                "simple_mantra": "Om Chandraya Namaha",
                "gayatri_mantra": "Om Padmadwajaya Vidmahe Hema Roopaya Dhimahi Tanno Soma Prachodayat",
                "repetitions": "108 times daily or 11000 times in 40 days",
                "best_time": "Evening after sunset or Monday evenings",
                "direction": "Face North",
                "benefits": "Improves emotional stability, intuition, and mental peace",
                "special_days": "Mondays, Full moon days, Sharad Purnima"
            },
            "Mars": {
                "beej_mantra": "Om Kraam Kreem Kraum Sah Bhaumaya Namaha",
                "simple_mantra": "Om Mangalaya Namaha",
                "gayatri_mantra": "Om Angarakaya Vidmahe Bhoomiputraya Dhimahi Tanno Mangal Prachodayat",
                "repetitions": "108 times daily or 10000 times in 40 days",
                "best_time": "Tuesday morning or evening",
                "direction": "Face South",
                "benefits": "Increases courage, energy, and protection",
                "special_days": "Tuesdays, Hanuman Jayanti, Kartikeya festivals"
            },
            "Mercury": {
                "beej_mantra": "Om Braam Breem Braum Sah Budhaya Namaha",
                "simple_mantra": "Om Budhaya Namaha",
                "gayatri_mantra": "Om Gajadhwajaya Vidmahe Sukha Hastaya Dhimahi Tanno Budh Prachodayat",
                "repetitions": "108 times daily or 17000 times in 40 days",
                "best_time": "Wednesday morning or evening",
                "direction": "Face North",
                "benefits": "Enhances intelligence, communication, and business skills",
                "special_days": "Wednesdays, Ganesha Chaturthi, Saraswati Puja"
            },
            "Jupiter": {
                "beej_mantra": "Om Graam Greem Graum Sah Gurave Namaha",
                "simple_mantra": "Om Gurave Namaha",
                "gayatri_mantra": "Om Vrishabadhwajaya Vidmahe Kruni Hastaya Dhimahi Tanno Guru Prachodayat",
                "repetitions": "108 times daily or 16000 times in 40 days",
                "best_time": "Thursday morning",
                "direction": "Face Northeast",
                "benefits": "Brings wisdom, prosperity, and spiritual growth",
                "special_days": "Thursdays, Guru Purnima, Brihaspati festivals"
            },
            "Venus": {
                "beej_mantra": "Om Draam Dreem Draum Sah Shukraya Namaha",
                "simple_mantra": "Om Shukraya Namaha",
                "gayatri_mantra": "Om Aswadhwajaya Vidmahe Dhanur Hastaya Dhimahi Tanno Shukra Prachodayat",
                "repetitions": "108 times daily or 20000 times in 40 days",
                "best_time": "Friday morning or evening",
                "direction": "Face Southeast",
                "benefits": "Improves relationships, creativity, and material comforts",
                "special_days": "Fridays, Devi festivals, Lakshmi Puja"
            },
            "Saturn": {
                "beej_mantra": "Om Praam Preem Praum Sah Shanaye Namaha",
                "simple_mantra": "Om Shanaye Namaha",
                "gayatri_mantra": "Om Kaakadhwajaya Vidmahe Khadga Hastaya Dhimahi Tanno Mandah Prachodayat",
                "repetitions": "108 times daily or 19000 times in 40 days",
                "best_time": "Saturday evening",
                "direction": "Face West",
                "benefits": "Provides discipline, patience, and karmic relief",
                "special_days": "Saturdays, Shani Amavasya, Hanuman Jayanti"
            },
            "Rahu": {
                "beej_mantra": "Om Bhraam Bhreem Bhraum Sah Rahave Namaha",
                "simple_mantra": "Om Rahave Namaha",
                "gayatri_mantra": "Om Naagadhwajaya Vidmahe Padma Hastaya Dhimahi Tanno Rahu Prachodayat",
                "repetitions": "108 times daily or 18000 times in 40 days",
                "best_time": "Saturday evening or Rahu Kaal",
                "direction": "Face Southwest",
                "benefits": "Reduces confusion and provides material success",
                "special_days": "Saturdays, Solar eclipses, Nag Panchami"
            },
            "Ketu": {
                "beej_mantra": "Om Sraam Sreem Sraum Sah Ketave Namaha",
                "simple_mantra": "Om Ketave Namaha",
                "gayatri_mantra": "Om Ashwadhwajaya Vidmahe Soola Hastaya Dhimahi Tanno Ketu Prachodayat",
                "repetitions": "108 times daily or 7000 times in 40 days",
                "best_time": "Tuesday evening or Ketu Kaal",
                "direction": "Face Northwest",
                "benefits": "Enhances spiritual insight and inner wisdom",
                "special_days": "Tuesdays, Lunar eclipses, Ganesha festivals"
            }
        }

        return mantra_data.get(planet_name, {
            "simple_mantra": f"Om {planet_name}aya Namaha",
            "repetitions": "108 times daily",
            "note": "Consult a qualified astrologer for specific mantras"
        })

    def _get_yantra_remedies(self, planet_name: str) -> Dict[str, Any]:
        """Get yantra therapy recommendations."""
        yantra_data = {
            "Sun": {"yantra": "Surya Yantra", "material": "Copper or Gold", "size": "3x3 inches", "placement": "East wall, worship room"},
            "Moon": {"yantra": "Chandra Yantra", "material": "Silver", "size": "3x3 inches", "placement": "North wall, bedroom"},
            "Mars": {"yantra": "Mangal Yantra", "material": "Copper", "size": "3x3 inches", "placement": "South wall, workout area"},
            "Mercury": {"yantra": "Budh Yantra", "material": "Bronze", "size": "3x3 inches", "placement": "North wall, study room"},
            "Jupiter": {"yantra": "Guru Yantra", "material": "Gold or Copper", "size": "3x3 inches", "placement": "Northeast corner"},
            "Venus": {"yantra": "Shukra Yantra", "material": "Silver", "size": "3x3 inches", "placement": "Southeast corner"},
            "Saturn": {"yantra": "Shani Yantra", "material": "Iron or Silver", "size": "3x3 inches", "placement": "West wall"},
            "Rahu": {"yantra": "Rahu Yantra", "material": "Mixed metals", "size": "3x3 inches", "placement": "Southwest corner"},
            "Ketu": {"yantra": "Ketu Yantra", "material": "Mixed metals", "size": "3x3 inches", "placement": "Northwest corner"}
        }
        return yantra_data.get(planet_name, {"yantra": f"{planet_name} Yantra", "note": "Consult expert for specific yantra"})

    def _get_color_remedies(self, planet_name: str) -> Dict[str, Any]:
        """Get color therapy recommendations."""
        color_data = {
            "Sun": {"primary_colors": ["Orange", "Red", "Gold"], "avoid_colors": ["Black", "Dark Blue"], "clothing": "Wear orange/red on Sundays", "home_decor": "Use warm colors in east-facing rooms"},
            "Moon": {"primary_colors": ["White", "Silver", "Light Blue"], "avoid_colors": ["Dark colors"], "clothing": "Wear white/silver on Mondays", "home_decor": "Use cool colors in north-facing rooms"},
            "Mars": {"primary_colors": ["Red", "Orange", "Coral"], "avoid_colors": ["Green"], "clothing": "Wear red on Tuesdays", "home_decor": "Use energetic colors in south-facing rooms"},
            "Mercury": {"primary_colors": ["Green", "Light Blue"], "avoid_colors": ["Red"], "clothing": "Wear green on Wednesdays", "home_decor": "Use fresh colors in study areas"},
            "Jupiter": {"primary_colors": ["Yellow", "Gold", "Orange"], "avoid_colors": ["Dark colors"], "clothing": "Wear yellow on Thursdays", "home_decor": "Use bright colors in northeast areas"},
            "Venus": {"primary_colors": ["White", "Pink", "Light Blue"], "avoid_colors": ["Dark colors"], "clothing": "Wear white/pink on Fridays", "home_decor": "Use soft colors in southeast areas"},
            "Saturn": {"primary_colors": ["Dark Blue", "Black", "Purple"], "avoid_colors": ["Bright colors"], "clothing": "Wear dark blue on Saturdays", "home_decor": "Use deep colors in west-facing rooms"},
            "Rahu": {"primary_colors": ["Smoky colors", "Grey", "Brown"], "avoid_colors": ["Bright colors"], "clothing": "Wear muted colors", "home_decor": "Use earth tones"},
            "Ketu": {"primary_colors": ["Brown", "Grey", "Maroon"], "avoid_colors": ["Bright colors"], "clothing": "Wear earth tones", "home_decor": "Use natural colors"}
        }
        return color_data.get(planet_name, {"primary_colors": ["Neutral colors"], "note": "Consult expert for specific colors"})

    def _get_metal_remedies(self, planet_name: str) -> Dict[str, Any]:
        """Get metal therapy recommendations."""
        metal_data = {
            "Sun": {"primary_metal": "Gold", "alternatives": ["Copper"], "wearing": "Gold jewelry, especially rings", "home_items": "Copper vessels for water"},
            "Moon": {"primary_metal": "Silver", "alternatives": ["White metals"], "wearing": "Silver jewelry", "home_items": "Silver vessels for milk/water"},
            "Mars": {"primary_metal": "Copper", "alternatives": ["Red metals"], "wearing": "Copper bracelet", "home_items": "Copper items in kitchen"},
            "Mercury": {"primary_metal": "Bronze", "alternatives": ["Mixed metals"], "wearing": "Bronze accessories", "home_items": "Bronze items in study"},
            "Jupiter": {"primary_metal": "Gold", "alternatives": ["Yellow metals"], "wearing": "Gold jewelry", "home_items": "Brass items in worship area"},
            "Venus": {"primary_metal": "Silver", "alternatives": ["White metals"], "wearing": "Silver jewelry", "home_items": "Silver decorative items"},
            "Saturn": {"primary_metal": "Iron", "alternatives": ["Dark metals"], "wearing": "Iron ring (with caution)", "home_items": "Iron items for protection"},
            "Rahu": {"primary_metal": "Mixed metals", "alternatives": ["Alloys"], "wearing": "Mixed metal jewelry", "home_items": "Avoid pure metals"},
            "Ketu": {"primary_metal": "Mixed metals", "alternatives": ["Alloys"], "wearing": "Simple metal accessories", "home_items": "Minimal metal items"}
        }
        return metal_data.get(planet_name, {"primary_metal": "Consult expert", "note": "Metal therapy requires careful consideration"})

    def _get_day_specific_remedies(self, planet_name: str) -> Dict[str, Any]:
        """Get day-specific remedy recommendations."""
        day_data = {
            "Sun": {"day": "Sunday", "fasting": "Sunrise to sunset", "worship": "Surya temples", "activities": "Leadership activities, helping father figures", "donations": "Wheat, jaggery, copper items"},
            "Moon": {"day": "Monday", "fasting": "Evening fast", "worship": "Shiva temples", "activities": "Nurturing activities, helping mothers", "donations": "Rice, milk, silver items"},
            "Mars": {"day": "Tuesday", "fasting": "Morning fast", "worship": "Hanuman temples", "activities": "Physical exercise, courage-building", "donations": "Red lentils, red clothes"},
            "Mercury": {"day": "Wednesday", "fasting": "Partial fast", "worship": "Ganesha temples", "activities": "Learning, communication", "donations": "Green items, books"},
            "Jupiter": {"day": "Thursday", "fasting": "Yellow food only", "worship": "Vishnu temples", "activities": "Teaching, spiritual study", "donations": "Yellow items, turmeric"},
            "Venus": {"day": "Friday", "fasting": "White food only", "worship": "Devi temples", "activities": "Artistic pursuits, relationship harmony", "donations": "White items, sweets"},
            "Saturn": {"day": "Saturday", "fasting": "Oil-free food", "worship": "Shani temples", "activities": "Service to elderly, discipline", "donations": "Black items, oil, iron"},
            "Rahu": {"day": "Saturday", "fasting": "Avoid non-veg", "worship": "Durga temples", "activities": "Meditation, avoiding shortcuts", "donations": "Blue/black items"},
            "Ketu": {"day": "Tuesday", "fasting": "Simple food", "worship": "Ganesha temples", "activities": "Spiritual practices, detachment", "donations": "Brown items, spiritual books"}
        }
        return day_data.get(planet_name, {"day": "Consult expert", "note": "Day-specific remedies require proper guidance"})

    def _get_dietary_remedies(self, planet_name: str) -> Dict[str, Any]:
        """Get dietary recommendations for planetary strengthening."""
        diet_data = {
            "Sun": {"beneficial_foods": ["Wheat", "Jaggery", "Orange fruits", "Almonds", "Saffron"], "avoid_foods": ["Cold foods", "Excessive salt"], "timing": "Eat warm foods during sunrise", "special_items": "Offer water to Sun with copper vessel"},
            "Moon": {"beneficial_foods": ["Rice", "Milk", "White foods", "Coconut", "Cucumber"], "avoid_foods": ["Spicy foods", "Alcohol"], "timing": "Eat cooling foods in evening", "special_items": "Drink milk with cardamom"},
            "Mars": {"beneficial_foods": ["Red lentils", "Pomegranate", "Red foods", "Garlic", "Ginger"], "avoid_foods": ["Excessive meat", "Alcohol"], "timing": "Eat energizing foods in morning", "special_items": "Drink water from copper vessel"},
            "Mercury": {"beneficial_foods": ["Green vegetables", "Mint", "Green gram", "Fennel", "Cardamom"], "avoid_foods": ["Heavy foods", "Excessive oil"], "timing": "Light, fresh foods", "special_items": "Chew fennel after meals"},
            "Jupiter": {"beneficial_foods": ["Yellow foods", "Turmeric", "Banana", "Chickpeas", "Ghee"], "avoid_foods": ["Non-vegetarian", "Alcohol"], "timing": "Sattvic foods only", "special_items": "Add turmeric to milk"},
            "Venus": {"beneficial_foods": ["White foods", "Sugar", "Dairy", "Sweet fruits", "Rose water"], "avoid_foods": ["Bitter foods", "Excessive spice"], "timing": "Sweet foods in moderation", "special_items": "Rose water in drinks"},
            "Saturn": {"beneficial_foods": ["Black gram", "Sesame", "Dark foods", "Iron-rich foods"], "avoid_foods": ["Excessive sweets", "Rich foods"], "timing": "Simple, disciplined eating", "special_items": "Sesame oil in cooking"},
            "Rahu": {"beneficial_foods": ["Radish", "Garlic", "Onion", "Mustard"], "avoid_foods": ["Processed foods", "Shortcuts in cooking"], "timing": "Avoid eating during eclipses", "special_items": "Natural, unprocessed foods"},
            "Ketu": {"beneficial_foods": ["Simple foods", "Spiritual foods", "Minimal spices"], "avoid_foods": ["Excessive variety", "Rich foods"], "timing": "Eat mindfully", "special_items": "Offer food before eating"}
        }
        return diet_data.get(planet_name, {"beneficial_foods": ["Sattvic foods"], "note": "Consult expert for specific dietary guidance"})

    def _get_charity_remedies(self, planet_name: str) -> Dict[str, Any]:
        """Get charitable activity recommendations."""
        charity_data = {
            "Sun": {"primary_charity": "Help government employees, fathers, authority figures", "items_to_donate": ["Wheat", "Jaggery", "Copper items", "Orange clothes"], "timing": "Sundays", "beneficiaries": "Government workers, elderly men"},
            "Moon": {"primary_charity": "Help mothers, women, children", "items_to_donate": ["Rice", "Milk", "Silver items", "White clothes"], "timing": "Mondays, Full moon", "beneficiaries": "Mothers, children, elderly women"},
            "Mars": {"primary_charity": "Help soldiers, athletes, young men", "items_to_donate": ["Red lentils", "Red clothes", "Copper items"], "timing": "Tuesdays", "beneficiaries": "Military personnel, athletes, laborers"},
            "Mercury": {"primary_charity": "Help students, teachers, communicators", "items_to_donate": ["Books", "Green items", "Educational materials"], "timing": "Wednesdays", "beneficiaries": "Students, teachers, writers"},
            "Jupiter": {"primary_charity": "Help teachers, priests, wise people", "items_to_donate": ["Yellow items", "Turmeric", "Religious books"], "timing": "Thursdays", "beneficiaries": "Teachers, priests, scholars"},
            "Venus": {"primary_charity": "Help artists, women, young people", "items_to_donate": ["White items", "Sweets", "Artistic materials"], "timing": "Fridays", "beneficiaries": "Artists, young women, couples"},
            "Saturn": {"primary_charity": "Help elderly, disabled, servants", "items_to_donate": ["Black items", "Oil", "Iron items", "Blankets"], "timing": "Saturdays", "beneficiaries": "Elderly, disabled, poor people"},
            "Rahu": {"primary_charity": "Help foreigners, outcasts, technology workers", "items_to_donate": ["Blue/black items", "Modern items"], "timing": "Saturdays", "beneficiaries": "Foreigners, social outcasts"},
            "Ketu": {"primary_charity": "Help spiritual seekers, researchers", "items_to_donate": ["Spiritual books", "Simple items"], "timing": "Tuesdays", "beneficiaries": "Spiritual seekers, researchers"}
        }
        return charity_data.get(planet_name, {"primary_charity": "Help those in need", "note": "Charity should be done with pure intentions"})

    def _get_lifestyle_remedies(self, planet_name: str, planet_position: PlanetPosition) -> Dict[str, Any]:
        """Get lifestyle modification recommendations."""
        lifestyle_data = {
            "Sun": {"wake_time": "Before sunrise", "exercise": "Surya Namaskara, outdoor activities", "meditation": "Sun gazing (safely)", "work_style": "Leadership roles, authority positions"},
            "Moon": {"wake_time": "Early morning", "exercise": "Gentle yoga, swimming", "meditation": "Moon meditation, water meditation", "work_style": "Nurturing roles, public relations"},
            "Mars": {"wake_time": "Early morning", "exercise": "Vigorous exercise, martial arts", "meditation": "Active meditation, sports", "work_style": "Competitive fields, physical work"},
            "Mercury": {"wake_time": "Variable", "exercise": "Mental exercises, light physical activity", "meditation": "Mindfulness, study meditation", "work_style": "Communication, learning, business"},
            "Jupiter": {"wake_time": "Early morning", "exercise": "Moderate exercise, yoga", "meditation": "Spiritual meditation, chanting", "work_style": "Teaching, counseling, spiritual work"},
            "Venus": {"wake_time": "Comfortable timing", "exercise": "Dance, artistic movement", "meditation": "Beauty meditation, music", "work_style": "Creative fields, relationship work"},
            "Saturn": {"wake_time": "Very early", "exercise": "Disciplined routine, endurance", "meditation": "Discipline meditation, service", "work_style": "Structured work, long-term projects"},
            "Rahu": {"wake_time": "Irregular", "exercise": "Modern fitness, technology-aided", "meditation": "Innovative meditation techniques", "work_style": "Technology, foreign connections"},
            "Ketu": {"wake_time": "Spiritual timing", "exercise": "Minimal, spiritual practices", "meditation": "Deep meditation, detachment", "work_style": "Research, spiritual work"}
        }
        return lifestyle_data.get(planet_name, {"note": "Consult expert for specific lifestyle recommendations"})

    def _get_spiritual_remedies(self, planet_name: str) -> Dict[str, Any]:
        """Get spiritual practice recommendations."""
        spiritual_data = {
            "Sun": {"primary_practice": "Surya meditation", "deity": "Lord Surya", "sacred_texts": "Aditya Hridayam", "pilgrimage": "Sun temples"},
            "Moon": {"primary_practice": "Moon meditation", "deity": "Lord Shiva", "sacred_texts": "Chandra Stotra", "pilgrimage": "Shiva temples"},
            "Mars": {"primary_practice": "Hanuman worship", "deity": "Lord Hanuman", "sacred_texts": "Hanuman Chalisa", "pilgrimage": "Hanuman temples"},
            "Mercury": {"primary_practice": "Ganesha worship", "deity": "Lord Ganesha", "sacred_texts": "Ganesha Stotra", "pilgrimage": "Ganesha temples"},
            "Jupiter": {"primary_practice": "Guru meditation", "deity": "Lord Vishnu", "sacred_texts": "Vishnu Sahasranama", "pilgrimage": "Vishnu temples"},
            "Venus": {"primary_practice": "Devi worship", "deity": "Goddess Lakshmi", "sacred_texts": "Lakshmi Stotra", "pilgrimage": "Devi temples"},
            "Saturn": {"primary_practice": "Shani meditation", "deity": "Lord Shani", "sacred_texts": "Shani Stotra", "pilgrimage": "Shani temples"},
            "Rahu": {"primary_practice": "Durga worship", "deity": "Goddess Durga", "sacred_texts": "Durga Stotra", "pilgrimage": "Durga temples"},
            "Ketu": {"primary_practice": "Ganesha worship", "deity": "Lord Ganesha", "sacred_texts": "Ganesha Atharvashirsha", "pilgrimage": "Ancient temples"}
        }
        return spiritual_data.get(planet_name, {"primary_practice": "General meditation", "note": "Consult spiritual guide"})

    def _get_timing_remedies(self, planet_name: str) -> Dict[str, Any]:
        """Get timing-based remedy recommendations."""
        timing_data = {
            "Sun": {"best_time": "Sunrise to 10 AM", "avoid_time": "Sunset to midnight", "planetary_hours": "Sunday 1st, 8th hour", "auspicious_periods": "Solar festivals"},
            "Moon": {"best_time": "Evening to midnight", "avoid_time": "Noon to 3 PM", "planetary_hours": "Monday 1st, 8th hour", "auspicious_periods": "Full moon, new moon"},
            "Mars": {"best_time": "Morning 6-9 AM", "avoid_time": "Evening 6-9 PM", "planetary_hours": "Tuesday 1st, 8th hour", "auspicious_periods": "Mars festivals"},
            "Mercury": {"best_time": "Morning 9-12 PM", "avoid_time": "No specific restriction", "planetary_hours": "Wednesday 1st, 8th hour", "auspicious_periods": "Mercury festivals"},
            "Jupiter": {"best_time": "Morning 6-10 AM", "avoid_time": "Evening 6-10 PM", "planetary_hours": "Thursday 1st, 8th hour", "auspicious_periods": "Guru Purnima"},
            "Venus": {"best_time": "Evening 6-10 PM", "avoid_time": "Morning 6-10 AM", "planetary_hours": "Friday 1st, 8th hour", "auspicious_periods": "Venus festivals"},
            "Saturn": {"best_time": "Evening after sunset", "avoid_time": "Morning sunrise", "planetary_hours": "Saturday 1st, 8th hour", "auspicious_periods": "Shani festivals"},
            "Rahu": {"best_time": "Rahu Kaal", "avoid_time": "Auspicious times", "planetary_hours": "Saturday 4th, 5th hour", "auspicious_periods": "Eclipse times"},
            "Ketu": {"best_time": "Ketu Kaal", "avoid_time": "Auspicious times", "planetary_hours": "Tuesday 4th, 5th hour", "auspicious_periods": "Eclipse times"}
        }
        return timing_data.get(planet_name, {"best_time": "Consult expert", "note": "Timing is crucial for remedies"})

    def _get_specific_weakness_remedies(self, planet_name: str, strength_factors: List[Dict]) -> List[str]:
        """Get remedies for specific weaknesses identified in strength analysis."""
        specific_remedies = []

        for factor in strength_factors:
            if factor["score"] < 0:  # Negative factors need specific remedies
                factor_name = factor["factor"]

                if "debilitation" in factor_name.lower():
                    specific_remedies.append(f"CRITICAL: {planet_name} is debilitated. Perform daily mantras and wear gemstone after proper consultation.")
                elif "enemy sign" in factor_name.lower():
                    specific_remedies.append(f"IMPORTANT: {planet_name} in enemy sign. Strengthen through friendly planet remedies and avoid conflicts.")
                elif "6th house" in factor_name.lower():
                    specific_remedies.append(f"Focus on service and health. {planet_name} in 6th house needs service-oriented activities.")
                elif "8th house" in factor_name.lower():
                    specific_remedies.append(f"Practice transformation rituals. {planet_name} in 8th house needs spiritual practices for transformation.")
                elif "12th house" in factor_name.lower():
                    specific_remedies.append(f"Engage in charitable activities. {planet_name} in 12th house benefits from selfless service.")
                elif "combustion" in factor_name.lower():
                    specific_remedies.append(f"URGENT: {planet_name} is combust. Perform specific mantras to reduce Sun's overpowering influence.")
                elif "retrograde" in factor_name.lower():
                    specific_remedies.append(f"Practice patience and review. {planet_name} retrograde needs careful, methodical approach.")

        if not specific_remedies:
            specific_remedies.append(f"Continue general {planet_name} strengthening practices for optimal results.")

        return specific_remedies

    def _get_planetary_precautions(self, planet_name: str) -> List[str]:
        """Get precautions to observe while doing planetary remedies."""
        precautions = {
            "Sun": ["Avoid ego inflation", "Don't become overly authoritative", "Respect father figures", "Avoid anger during remedies"],
            "Moon": ["Avoid emotional extremes", "Don't become overly dependent", "Respect mother figures", "Maintain emotional balance"],
            "Mars": ["Control anger and aggression", "Avoid conflicts during remedies", "Channel energy positively", "Respect younger siblings"],
            "Mercury": ["Avoid gossip and lies", "Don't overthink", "Maintain honesty in communication", "Respect teachers and students"],
            "Jupiter": ["Avoid pride in knowledge", "Don't become preachy", "Respect gurus and elders", "Maintain humility"],
            "Venus": ["Avoid excessive indulgence", "Don't become materialistic", "Maintain relationship harmony", "Respect women"],
            "Saturn": ["Don't become overly pessimistic", "Avoid shortcuts", "Accept responsibilities", "Respect elderly and servants"],
            "Rahu": ["Avoid shortcuts and unethical means", "Don't become obsessive", "Stay grounded", "Avoid foreign entanglements"],
            "Ketu": ["Don't become overly detached", "Maintain worldly responsibilities", "Avoid isolation", "Balance spirituality with practicality"]
        }
        return precautions.get(planet_name, ["Follow general ethical guidelines", "Consult expert for specific precautions"])

    def _get_remedy_timeline(self, planet_name: str, strength: str) -> Dict[str, str]:
        """Get expected timeline for remedy effects."""
        base_timelines = {
            "Sun": {"immediate": "1-2 weeks", "moderate": "1-3 months", "significant": "6-12 months"},
            "Moon": {"immediate": "3-7 days", "moderate": "2-4 weeks", "significant": "3-6 months"},
            "Mars": {"immediate": "1-2 weeks", "moderate": "1-2 months", "significant": "6-9 months"},
            "Mercury": {"immediate": "1 week", "moderate": "1 month", "significant": "3-6 months"},
            "Jupiter": {"immediate": "2-4 weeks", "moderate": "3-6 months", "significant": "1-2 years"},
            "Venus": {"immediate": "1-2 weeks", "moderate": "2-4 months", "significant": "6-12 months"},
            "Saturn": {"immediate": "1-3 months", "moderate": "6-12 months", "significant": "2-3 years"},
            "Rahu": {"immediate": "2-4 weeks", "moderate": "3-6 months", "significant": "1.5-3 years"},
            "Ketu": {"immediate": "1-3 weeks", "moderate": "2-4 months", "significant": "1-2 years"}
        }

        timeline = base_timelines.get(planet_name, {"immediate": "2-4 weeks", "moderate": "2-6 months", "significant": "1-2 years"})

        if strength == "Very Weak":
            return {
                "initial_relief": timeline["immediate"],
                "noticeable_improvement": timeline["moderate"],
                "significant_change": timeline["significant"],
                "note": "Consistency is crucial for weak planets. Results may take longer but will be lasting."
            }
        elif strength == "Weak":
            return {
                "initial_relief": timeline["immediate"],
                "noticeable_improvement": f"Half of {timeline['moderate']}",
                "significant_change": f"Half of {timeline['significant']}",
                "note": "Regular practice will show steady improvement."
            }
        else:
            return {
                "initial_relief": f"Half of {timeline['immediate']}",
                "noticeable_improvement": f"Half of {timeline['moderate']}",
                "significant_change": f"Half of {timeline['significant']}",
                "note": "Moderate weakness responds well to consistent remedies."
            }

    # PLANETARY COMBINATION DESCRIPTION METHODS

    def _get_planet_in_sign_meaning(self, planet_name: str, sign: str) -> str:
        """Get detailed meaning of planet in specific sign."""
        from planetary_combination_descriptions import get_planet_in_sign_meaning
        return get_planet_in_sign_meaning(planet_name, sign)

    def _get_planet_in_house_meaning(self, planet_name: str, house: int) -> str:
        """Get detailed meaning of planet in specific house."""
        from planetary_combination_descriptions import get_planet_in_house_meaning
        return get_planet_in_house_meaning(planet_name, house)

    def _get_combined_planet_sign_house_effect(self, planet_name: str, sign: str, house: int) -> str:
        """Get combined effect of planet in specific sign and house."""
        from planetary_combination_descriptions import get_combined_planet_sign_house_effect
        return get_combined_planet_sign_house_effect(planet_name, sign, house)

    def _get_life_manifestation_description(self, planet_name: str, sign: str, house: int) -> str:
        """Get description of how this combination manifests in daily life."""
        from planetary_combination_descriptions import get_life_manifestation_description
        return get_life_manifestation_description(planet_name, sign, house)

    def _get_timing_activation_description(self, planet_name: str, house: int) -> str:
        """Get description of when and how this planetary placement gets activated."""
        from planetary_combination_descriptions import get_timing_activation_description
        return get_timing_activation_description(planet_name, house)
