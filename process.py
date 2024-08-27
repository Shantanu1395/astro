# process.py

import swisseph as swe
from data import get_zodiac_sign, planet_interpretations

def calculate_positions(year, month, day, hour, minute, latitude, longitude):
    # Load Swiss Ephemeris data
    swe.set_ephe_path('/usr/share/ephe')  # Path to ephemeris files, change if needed

    # Calculate Julian Day number
    jd = swe.julday(year, month, day, hour + minute/60.0)

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
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    positions['Ascendant'] = ascmc[0]  # Ascendant is the first point in ascmc
    positions['Midheaven'] = ascmc[1]  # Midheaven is the second point in ascmc

    return positions


def interpret_positions(positions):
    # Determine zodiac signs based on positions
    interpretations = {}
    for planet, position in positions.items():
        sign = get_zodiac_sign(position)
        if planet in planet_interpretations:
            interpretations[planet] = planet_interpretations[planet][sign]

    return interpretations
