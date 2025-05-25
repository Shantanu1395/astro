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
