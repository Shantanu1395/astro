#!/usr/bin/env python3
"""
Test script for Vedic astrology calculations
"""

from datetime import date, time
from src.models.models import BirthData, LocationData
from src.core.vedic_calculator import VedicCalculator
from src.core.prediction_engine import VedicPredictionEngine
from src.utils.utils import get_location_data

def test_vedic_calculation():
    """Test Vedic astrology calculation with sample data."""

    print("🌟 Testing Vedic Astrology Calculation System")
    print("=" * 50)

    # Sample birth data
    birth_data = BirthData(
        name="Test Person",
        birth_date=date(1990, 5, 15),
        birth_time=time(14, 30),  # 2:30 PM
        birth_location="Mumbai, India"
    )

    print(f"Birth Data:")
    print(f"  Name: {birth_data.name}")
    print(f"  Date: {birth_data.birth_date}")
    print(f"  Time: {birth_data.birth_time}")
    print(f"  Location: {birth_data.birth_location}")
    print()

    # Get location coordinates
    print("Getting location coordinates...")
    location_data = get_location_data(birth_data.birth_location)

    if not location_data:
        print("❌ Could not get location data")
        return False

    print(f"Location Data:")
    print(f"  Latitude: {location_data.latitude}")
    print(f"  Longitude: {location_data.longitude}")
    print(f"  Timezone: {location_data.timezone}")
    print()

    # Initialize calculator
    vedic_calc = VedicCalculator()

    # Calculate birth chart
    print("Calculating Vedic birth chart...")
    try:
        chart = vedic_calc.calculate_birth_chart(birth_data, location_data)

        print(f"Chart Summary:")
        print(f"  Ascendant: {chart.ascendant_sign}")
        print(f"  Moon Sign: {chart.moon_sign}")
        print(f"  Sun Sign: {chart.sun_sign}")
        print(f"  Birth Nakshatra: {chart.birth_nakshatra} (Pada {chart.birth_nakshatra_pada})")
        print()

        print("Planetary Positions:")
        for planet in chart.planets:
            print(f"  {planet.name}: {planet.sign} (House {planet.house})")
            if planet.nakshatra:
                print(f"    Nakshatra: {planet.nakshatra}")
        print()

        # Calculate current dasha
        print("Calculating current Dasha period...")
        current_dasha = vedic_calc.calculate_current_dasha(birth_data, chart)

        print(f"Current Dasha:")
        print(f"  Planet: {current_dasha.planet}")
        print(f"  Remaining Years: {current_dasha.remaining_years:.1f}")
        print(f"  Period: {current_dasha.start_date} to {current_dasha.end_date}")
        print()

        # Generate enhanced prediction
        print("Generating enhanced AI prediction...")
        prediction_engine = VedicPredictionEngine()
        prediction = prediction_engine.generate_vedic_prediction(birth_data, chart, current_dasha, location_data)

        print("Prediction Summary:")
        print(f"  Key Themes: {', '.join(prediction.key_themes)}")
        print()
        print("Prediction Text:")
        print("-" * 40)
        print(prediction.prediction_text)
        print("-" * 40)

        print("\n✅ Vedic calculation test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Error during calculation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_vedic_calculation()
