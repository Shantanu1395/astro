# main.py

import datetime
import pytz
from process import calculate_positions, interpret_positions

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

    # Interpret the positions
    interpretations = interpret_positions(positions)

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

    print("\nInterpretations:")
    for planet, interpretation in interpretations.items():
        print(f"{planet}: {interpretation}")
