# main.py

import swisseph as swe
import datetime
import pytz
from process import interpret_positions


def calculate_positions(year, month, day, hour, minute, latitude, longitude):
    swe.set_ephe_path('/usr/share/ephe')
    jd = swe.julday(year, month, day, hour + minute / 60.0)

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
        'Pluto': swe.PLUTO
    }

    positions = {}
    for planet_name, planet_id in planets.items():
        pos, _ = swe.calc_ut(jd, planet_id)
        positions[planet_name] = pos[0]

    return positions


def calculate_cusps(year, month, day, hour, minute, latitude, longitude):
    jd = swe.julday(year, month, day, hour + minute / 60.0)
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    return cusps


def generate_natal_chart(birth_date, hh, mm, latitude, longitude):
    birth_time = datetime.time(hh, mm)
    birth_datetime = datetime.datetime.combine(birth_date, birth_time)
    local_tz = pytz.timezone('Asia/Kolkata')  # Adjust timezone as necessary
    birth_datetime = local_tz.localize(birth_datetime)
    birth_datetime_utc = birth_datetime.astimezone(pytz.utc)

    year = birth_datetime_utc.year
    month = birth_datetime_utc.month
    day = birth_datetime_utc.day
    hour = birth_datetime_utc.hour
    minute = birth_datetime_utc.minute

    positions = calculate_positions(year, month, day, hour, minute, latitude, longitude)
    cusps = calculate_cusps(year, month, day, hour, minute, latitude, longitude)

    interpretations = interpret_positions(positions, cusps)

    return interpretations


# Example usage
if __name__ == "__main__":
    birth_date = datetime.date(1994, 3, 1)
    hh = 23
    mm = 2
    latitude = 28.6139
    longitude = 77.2090

    interpretations = generate_natal_chart(birth_date, hh, mm, latitude, longitude)

    for interpretation in interpretations:
        print(f"{interpretation['Planet']} | {interpretation['Zodiac']} | {interpretation['House']}")
        print(f"Manifestations: {interpretation['Manifestation']}")
        print(f"Challenges: {interpretation['Challenges']}")
        print("\n")
