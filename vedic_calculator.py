import swisseph as swe
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple
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
