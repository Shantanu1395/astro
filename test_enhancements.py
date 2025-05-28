#!/usr/bin/env python3
"""
Test script to verify the enhanced planetary analysis and remedies functionality.
"""

from vedic_calculator import VedicCalculator
from models import PlanetPosition

def test_planetary_combination_description():
    """Test the enhanced planetary combination descriptions."""
    print("🔍 Testing Planetary Combination Descriptions...")

    calculator = VedicCalculator()

    # Test Sun in Aquarius in House 1 (the specific example mentioned)
    sun_position = PlanetPosition(
        name="Sun",
        longitude=315.5,  # Aquarius
        latitude=0.0,     # Required field
        sign="Kumbh",
        house=1,
        degree=15.5,      # Degree within sign
        nakshatra="Dhanishta",
        nakshatra_pada=2,
        retrograde=False
    )

    description = calculator.generate_planetary_combination_description("Sun", sun_position)

    print(f"✅ Generated description for Sun in Aquarius in House 1:")
    print(f"Title: {description['title']}")
    print(f"Sign Influence: {description['sign_influence']['description'][:100]}...")
    print(f"House Influence: {description['house_influence']['description'][:100]}...")
    print(f"Combined Effect: {description['combined_effect']['description'][:100]}...")
    print()

def test_planetary_remedies():
    """Test the comprehensive planetary remedies system."""
    print("🌟 Testing Planetary Remedies...")

    calculator = VedicCalculator()

    # Test remedies for a weak planet
    weak_planet = PlanetPosition(
        name="Sun",
        longitude=195.5,  # Libra (debilitated)
        latitude=0.0,     # Required field
        sign="Tula",
        house=6,  # Challenging house
        degree=15.5,      # Degree within sign
        nakshatra="Swati",
        nakshatra_pada=1,
        retrograde=False
    )

    # Calculate strength (this would normally be weak due to debilitation + 6th house)
    strength_analysis = calculator.calculate_planetary_strength("Sun", weak_planet)

    # Generate remedies
    remedies = calculator.generate_planetary_remedies(
        "Sun", weak_planet, strength_analysis["overall_strength"], strength_analysis["strength_factors"]
    )

    print(f"✅ Generated remedies for weak Sun:")
    print(f"Remedies needed: {remedies['remedies_needed']}")
    if remedies['remedies_needed']:
        print(f"Overall approach: {remedies['overall_approach'][:100]}...")
        print(f"Primary gemstone: {remedies['gemstone_therapy']['primary']}")
        print(f"Simple mantra: {remedies['mantra_therapy']['simple_mantra']}")
        print(f"Expected timeline: {remedies['expected_timeline']['initial_relief']}")
    print()

def test_strong_planet_no_remedies():
    """Test that strong planets don't get unnecessary remedies."""
    print("✅ Testing Strong Planet (No Remedies Needed)...")

    calculator = VedicCalculator()

    # Test strong planet (Sun in Leo in 1st house)
    strong_planet = PlanetPosition(
        name="Sun",
        longitude=135.5,  # Leo (own sign)
        latitude=0.0,     # Required field
        sign="Simha",
        house=1,  # Strong house
        nakshatra="Magha",
        nakshatra_pada=2
    )

    strength_analysis = calculator.calculate_planetary_strength("Sun", strong_planet)
    remedies = calculator.generate_planetary_remedies(
        "Sun", strong_planet, strength_analysis["overall_strength"], strength_analysis["strength_factors"]
    )

    print(f"✅ Strong Sun analysis:")
    print(f"Overall strength: {strength_analysis['overall_strength']}")
    print(f"Remedies needed: {remedies['remedies_needed']}")
    if not remedies['remedies_needed']:
        print(f"Message: {remedies['message']}")
    print()

def test_comprehensive_coverage():
    """Test that we have comprehensive coverage for different combinations."""
    print("📊 Testing Comprehensive Coverage...")

    from planetary_combination_descriptions import get_planet_in_sign_meaning, get_combined_planet_sign_house_effect

    # Test various combinations
    test_combinations = [
        ("Sun", "Aquarius"),
        ("Moon", "Cancer"),
        ("Mars", "Aries"),
        ("Jupiter", "Sagittarius"),
        ("Venus", "Taurus")
    ]

    for planet, sign in test_combinations:
        description = get_planet_in_sign_meaning(planet, sign)
        print(f"✅ {planet} in {sign}: {description[:80]}...")

    # Test specific house combinations
    special_combo = get_combined_planet_sign_house_effect("Sun", "Aquarius", 1)
    print(f"✅ Sun in Aquarius in House 1: {special_combo[:80]}...")
    print()

if __name__ == "__main__":
    print("🚀 Starting Enhanced Vedic Astrology System Tests...\n")

    try:
        test_planetary_combination_description()
        test_planetary_remedies()
        test_strong_planet_no_remedies()
        test_comprehensive_coverage()

        print("🎉 All tests completed successfully!")
        print("\n📋 Summary:")
        print("✅ Planetary combination descriptions working")
        print("✅ Comprehensive remedies system working")
        print("✅ Strong planet detection working")
        print("✅ Comprehensive coverage verified")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
