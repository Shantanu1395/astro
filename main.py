# main.py

import datetime
import pytz
from data import zodiac_traits
from process import calculate_positions, generate_structured_interpretation, get_zodiac_sign, get_house


def generate_natal_chart(birth_date, hh, mm, latitude, longitude):
    # Convert birth time to UTC
    birth_time = datetime.time(hh, mm)
    birth_datetime = datetime.datetime.combine(birth_date, birth_time)
    local_tz = pytz.timezone('Asia/Kolkata')  # Assuming Delhi, India timezone
    birth_datetime = local_tz.localize(birth_datetime)
    birth_datetime_utc = birth_datetime.astimezone(pytz.utc)

    # Extract year, month, day, hour, minute
    year = birth_datetime_utc.year
    month = birth_datetime_utc.month
    day = birth_datetime_utc.day
    hour = birth_datetime_utc.hour
    minute = birth_datetime_utc.minute

    # Calculate planetary positions including Ascendant and Midheaven
    positions = calculate_positions(year, month, day, hour, minute, latitude, longitude)

    # Determine the Sun sign
    sun_sign = get_zodiac_sign(positions['Sun'])

    # Interpret the positions
    interpretations = {}
    ascendant_sign = get_zodiac_sign(positions['Ascendant'])
    midheaven_sign = get_zodiac_sign(positions['Midheaven'])

    # Add Ascendant and Midheaven traits separately
    ascendant_trait = f"Your Ascendant in {ascendant_sign} gives you traits such as {', '.join(zodiac_traits.get(ascendant_sign, [])).lower()} that influence your outward behavior and first impressions."
    midheaven_trait = f"Your Midheaven in {midheaven_sign} suggests that you seek to achieve {', '.join(zodiac_traits.get(midheaven_sign, [])).lower()} traits in your career and public life."

    # Store Ascendant and Midheaven interpretations
    interpretations['Ascendant'] = ascendant_trait
    interpretations['Midheaven'] = midheaven_trait

    # Process the other planets
    for planet, position in positions.items():
        if planet not in ['Ascendant', 'Midheaven']:
            sign = get_zodiac_sign(position)
            house = get_house(position, positions['Ascendant'])
            planet_interpretation = generate_structured_interpretation(planet, sign, house)
            interpretations.update(planet_interpretation)

    return positions, interpretations


if __name__ == "__main__":
    # Example usage
    birth_date = datetime.date(1994, 3, 1)  # Example birth date
    hh = 23  # Example birth hour (11 PM)
    mm = 2  # Example birth minute (2 minutes)
    latitude = 28.6139  # Example latitude (Delhi, India)
    longitude = 77.2090  # Example longitude (Delhi, India)

    positions, interpretations = generate_natal_chart(birth_date, hh, mm, latitude, longitude)

    print("Planetary Positions:")
    for planet, position in positions.items():
        print(f"{planet}: {position:.2f}°")

    print("\nAscendant and Midheaven Traits:")
    print(f"Ascendant: {interpretations['Ascendant']}")
    print(f"Midheaven: {interpretations['Midheaven']}")

    print("\nDetailed Interpretations:")
    for key, value in interpretations.items():
        if key not in ['Ascendant', 'Midheaven']:
            planet_traits_str = ', '.join(value[0])
            zodiac_traits_str = ', '.join(value[1])
            house_traits_str = ', '.join(value[2])
            print(
                f"{key}: Planet Traits: {planet_traits_str}, Zodiac Traits: {zodiac_traits_str}, House Traits: {house_traits_str}")
