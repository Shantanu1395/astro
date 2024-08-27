# process.py

import swisseph as swe
from data import planet_traits, zodiac_traits, house_traits, get_zodiac_sign, get_house


def calculate_positions(year, month, day, hour, minute, latitude, longitude):
    # Load Swiss Ephemeris data
    swe.set_ephe_path('/usr/share/ephe')  # Path to ephemeris files, change if needed

    # Calculate Julian Day number
    jd = swe.julday(year, month, day, hour + minute / 60.0)

    # Calculate positions of planets
    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mercury': swe.MERCURY,
        'Venus': swe.VENUS,
        'Mars': swe.MARS,
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN,
        'Uranus': swe.URANUS,
        'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO,
    }

    positions = {}
    for planet_name, planet_id in planets.items():
        pos, _ = swe.calc_ut(jd, planet_id)
        positions[planet_name] = pos[0]  # Store the longitude

    # Calculate Ascendant (rising sign) and Midheaven (MC)
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')  # Use byte string for house system
    positions['Ascendant'] = ascmc[0]  # Ascendant is the first point in ascmc
    positions['Midheaven'] = ascmc[1]  # Midheaven is the second point in ascmc

    return positions


def interpret_position(planet, sign, house):
    planet_description = planet_traits.get(planet, "")
    sign_description = zodiac_traits.get(sign, "")
    house_description = house_traits.get(house, "")

    return f"{planet_description} {sign_description} {house_description}"


def interpret_positions(positions):
    # Determine zodiac signs and houses based on positions
    ascendant = positions['Ascendant']
    interpretations = {}
    for planet, position in positions.items():
        if planet not in ['Ascendant', 'Midheaven']:
            sign = get_zodiac_sign(position)
            house = get_house(position, ascendant)
            interpretations[planet] = interpret_position(planet, sign, house)

    return interpretations


# process.py

def generate_structured_interpretation(planet, sign, house):
    """
    Generate a structured interpretation for a planet in a specific sign and house.

    Args:
    - planet (str): The name of the planet (e.g., "Sun").
    - sign (str): The zodiac sign in which the planet is located (e.g., "Aries").
    - house (int): The house number in which the planet is located (1-12).

    Returns:
    - dict: A structured interpretation as { "planet | sign | house": [[planet traits], [zodiac traits], [house traits]] }
    """
    # Retrieve the traits for the planet, sign, and house
    planet_description = planet_traits.get(planet, [])
    sign_description = zodiac_traits.get(sign, [])
    house_description = house_traits.get(house, [])

    # Create the structured interpretation
    key = f"{planet} | {sign} | {house}"
    interpretation = {
        key: [planet_description, sign_description, house_description]
    }

    return interpretation

