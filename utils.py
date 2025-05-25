import swisseph as swe
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from datetime import datetime, timezone
import pytz
from typing import Tuple, Optional
from models import LocationData

# Initialize Swiss Ephemeris
swe.set_ephe_path('/usr/share/swisseph:/usr/local/share/swisseph')

# Zodiac signs in order
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Vedic/Sidereal zodiac signs
VEDIC_SIGNS = [
    "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
    "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"
]

# Nakshatras (27 lunar mansions)
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Planet names mapping
PLANET_NAMES = {
    swe.SUN: "Sun",
    swe.MOON: "Moon", 
    swe.MERCURY: "Mercury",
    swe.VENUS: "Venus",
    swe.MARS: "Mars",
    swe.JUPITER: "Jupiter",
    swe.SATURN: "Saturn",
    swe.MEAN_NODE: "Rahu",  # North Node
    swe.MEAN_APOG: "Ketu"   # South Node (calculated as opposite of Rahu)
}

def get_location_data(location_string: str) -> Optional[LocationData]:
    """
    Get latitude, longitude, and timezone for a given location string.
    """
    try:
        geolocator = Nominatim(user_agent="vedic_astrology_app")
        location = geolocator.geocode(location_string, timeout=10)
        
        if not location:
            return None
            
        # Get timezone (simplified - in production, use a proper timezone API)
        # For now, we'll use a basic mapping or default to UTC
        timezone_name = "UTC"  # This should be improved with proper timezone detection
        
        return LocationData(
            latitude=location.latitude,
            longitude=location.longitude,
            timezone=timezone_name,
            city=location_string.split(',')[0].strip(),
            country=location_string.split(',')[-1].strip() if ',' in location_string else location_string
        )
        
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
        return None

def degrees_to_sign_and_degree(longitude: float, vedic: bool = True) -> Tuple[str, float]:
    """
    Convert longitude to zodiac sign and degree within sign.
    """
    # Normalize longitude to 0-360 range
    longitude = longitude % 360
    
    sign_index = int(longitude // 30)
    degree_in_sign = longitude % 30
    
    if vedic:
        sign_name = VEDIC_SIGNS[sign_index]
    else:
        sign_name = ZODIAC_SIGNS[sign_index]
    
    return sign_name, degree_in_sign

def longitude_to_nakshatra(longitude: float) -> Tuple[str, int]:
    """
    Convert longitude to nakshatra and pada.
    Each nakshatra is 13°20' (13.333...), divided into 4 padas of 3°20' each.
    """
    # Normalize longitude
    longitude = longitude % 360
    
    # Each nakshatra is 13.333... degrees
    nakshatra_length = 360 / 27
    nakshatra_index = int(longitude / nakshatra_length)
    
    # Calculate pada (1-4)
    degree_in_nakshatra = longitude % nakshatra_length
    pada = int(degree_in_nakshatra / (nakshatra_length / 4)) + 1
    
    return NAKSHATRAS[nakshatra_index], pada

def julian_day_from_datetime(dt: datetime) -> float:
    """
    Convert datetime to Julian Day for Swiss Ephemeris calculations.
    """
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0 + dt.second/3600.0)

def calculate_ayanamsa(julian_day: float) -> float:
    """
    Calculate ayanamsa (precession correction) for sidereal calculations.
    Using Lahiri ayanamsa by default.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    return swe.get_ayanamsa(julian_day)
