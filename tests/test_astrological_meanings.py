"""
Test cases for astrological meanings validation.
Ensures all sun signs, moon signs, ascendants, and dashas have complete data.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.astrological_meanings import AstrologicalMeanings

class TestAstrologicalMeanings:
    """Test suite for comprehensive astrological meanings validation."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.meanings = AstrologicalMeanings()
        
        # All Vedic zodiac signs
        self.all_signs = [
            "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
            "Tula", "Vrishchik", "Dhanu", "Makara", "Kumbha", "Meena"
        ]
        
        # All planets for dasha periods
        self.all_planets = [
            "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", 
            "Saturn", "Rahu", "Ketu"
        ]
        
        # Required fields for each meaning type
        self.sun_sign_required_fields = [
            "name", "element", "quality", "ruler", "general_meaning",
            "personality_traits", "strengths", "challenges", "life_purpose",
            "career_inclinations", "relationships"
        ]
        
        self.moon_sign_required_fields = [
            "name", "emotional_nature", "inner_self", "instinctive_reactions",
            "comfort_needs", "relationship_style"
        ]
        
        self.ascendant_required_fields = [
            "name", "first_impression", "physical_appearance", "approach_to_life",
            "life_path", "challenges"
        ]
        
        self.dasha_required_fields = [
            "general_nature", "themes", "positive_effects", "challenges",
            "guidance", "duration"
        ]

    def test_all_sun_signs_have_complete_data(self):
        """Test that all 12 zodiac signs have complete sun sign meanings."""
        for sign in self.all_signs:
            meaning = self.meanings.get_sun_sign_meaning(sign)
            
            # Check that meaning exists
            assert meaning is not None, f"No sun sign meaning found for {sign}"
            
            # Check all required fields are present
            for field in self.sun_sign_required_fields:
                assert field in meaning, f"Missing field '{field}' in sun sign meaning for {sign}"
                assert meaning[field] is not None, f"Field '{field}' is None for sun sign {sign}"
                assert meaning[field] != "", f"Field '{field}' is empty for sun sign {sign}"
            
            # Check specific field types
            assert isinstance(meaning["personality_traits"], list), f"personality_traits should be list for {sign}"
            assert len(meaning["personality_traits"]) > 0, f"personality_traits should not be empty for {sign}"
            
            assert isinstance(meaning["strengths"], list), f"strengths should be list for {sign}"
            assert len(meaning["strengths"]) > 0, f"strengths should not be empty for {sign}"
            
            assert isinstance(meaning["challenges"], list), f"challenges should be list for {sign}"
            assert len(meaning["challenges"]) > 0, f"challenges should not be empty for {sign}"
            
            assert isinstance(meaning["career_inclinations"], list), f"career_inclinations should be list for {sign}"
            assert len(meaning["career_inclinations"]) > 0, f"career_inclinations should not be empty for {sign}"

    def test_all_moon_signs_have_complete_data(self):
        """Test that all 12 zodiac signs have complete moon sign meanings."""
        for sign in self.all_signs:
            meaning = self.meanings.get_moon_sign_meaning(sign)
            
            # Check that meaning exists
            assert meaning is not None, f"No moon sign meaning found for {sign}"
            
            # Check all required fields are present
            for field in self.moon_sign_required_fields:
                assert field in meaning, f"Missing field '{field}' in moon sign meaning for {sign}"
                assert meaning[field] is not None, f"Field '{field}' is None for moon sign {sign}"
                assert meaning[field] != "", f"Field '{field}' is empty for moon sign {sign}"

    def test_all_ascendants_have_complete_data(self):
        """Test that all 12 zodiac signs have complete ascendant meanings."""
        for sign in self.all_signs:
            meaning = self.meanings.get_ascendant_meaning(sign)
            
            # Check that meaning exists
            assert meaning is not None, f"No ascendant meaning found for {sign}"
            
            # Check all required fields are present
            for field in self.ascendant_required_fields:
                assert field in meaning, f"Missing field '{field}' in ascendant meaning for {sign}"
                assert meaning[field] is not None, f"Field '{field}' is None for ascendant {sign}"
                assert meaning[field] != "", f"Field '{field}' is empty for ascendant {sign}"

    def test_all_dashas_have_complete_data(self):
        """Test that all 9 planets have complete dasha meanings."""
        for planet in self.all_planets:
            meaning = self.meanings.get_dasha_meaning(planet)
            
            # Check that meaning exists
            assert meaning is not None, f"No dasha meaning found for {planet}"
            
            # Check all required fields are present
            for field in self.dasha_required_fields:
                assert field in meaning, f"Missing field '{field}' in dasha meaning for {planet}"
                assert meaning[field] is not None, f"Field '{field}' is None for dasha {planet}"
                assert meaning[field] != "", f"Field '{field}' is empty for dasha {planet}"
            
            # Check specific field types
            assert isinstance(meaning["themes"], list), f"themes should be list for {planet}"
            assert len(meaning["themes"]) > 0, f"themes should not be empty for {planet}"

    def test_general_explanations_exist(self):
        """Test that general explanations for all concepts exist."""
        explanations = self.meanings.get_general_explanations()
        
        required_concepts = ["sun_sign", "moon_sign", "ascendant", "dasha"]
        
        for concept in required_concepts:
            assert concept in explanations, f"Missing general explanation for {concept}"
            assert explanations[concept] is not None, f"General explanation for {concept} is None"
            assert explanations[concept] != "", f"General explanation for {concept} is empty"
            assert len(explanations[concept]) > 50, f"General explanation for {concept} is too short"

    def test_sun_sign_data_quality(self):
        """Test the quality and completeness of sun sign data."""
        for sign in self.all_signs:
            meaning = self.meanings.get_sun_sign_meaning(sign)
            
            # Check description lengths are reasonable
            assert len(meaning["general_meaning"]) > 50, f"General meaning too short for {sign}"
            assert len(meaning["life_purpose"]) > 30, f"Life purpose too short for {sign}"
            assert len(meaning["relationships"]) > 30, f"Relationships description too short for {sign}"
            
            # Check trait counts are reasonable
            assert 3 <= len(meaning["personality_traits"]) <= 10, f"Personality traits count unreasonable for {sign}"
            assert 3 <= len(meaning["strengths"]) <= 10, f"Strengths count unreasonable for {sign}"
            assert 2 <= len(meaning["challenges"]) <= 8, f"Challenges count unreasonable for {sign}"
            assert 3 <= len(meaning["career_inclinations"]) <= 10, f"Career inclinations count unreasonable for {sign}"

    def test_moon_sign_data_quality(self):
        """Test the quality and completeness of moon sign data."""
        for sign in self.all_signs:
            meaning = self.meanings.get_moon_sign_meaning(sign)
            
            # Check description lengths are reasonable
            assert len(meaning["emotional_nature"]) > 30, f"Emotional nature too short for {sign}"
            assert len(meaning["inner_self"]) > 20, f"Inner self too short for {sign}"
            assert len(meaning["comfort_needs"]) > 20, f"Comfort needs too short for {sign}"
            assert len(meaning["relationship_style"]) > 30, f"Relationship style too short for {sign}"

    def test_ascendant_data_quality(self):
        """Test the quality and completeness of ascendant data."""
        for sign in self.all_signs:
            meaning = self.meanings.get_ascendant_meaning(sign)
            
            # Check description lengths are reasonable
            assert len(meaning["first_impression"]) > 30, f"First impression too short for {sign}"
            assert len(meaning["approach_to_life"]) > 30, f"Approach to life too short for {sign}"
            assert len(meaning["life_path"]) > 30, f"Life path too short for {sign}"
            assert len(meaning["challenges"]) > 30, f"Challenges too short for {sign}"

    def test_dasha_data_quality(self):
        """Test the quality and completeness of dasha data."""
        for planet in self.all_planets:
            meaning = self.meanings.get_dasha_meaning(planet)
            
            # Check description lengths are reasonable
            assert len(meaning["general_nature"]) > 30, f"General nature too short for {planet}"
            assert len(meaning["positive_effects"]) > 30, f"Positive effects too short for {planet}"
            assert len(meaning["challenges"]) > 30, f"Challenges too short for {planet}"
            assert len(meaning["guidance"]) > 30, f"Guidance too short for {planet}"
            
            # Check theme count is reasonable
            assert 3 <= len(meaning["themes"]) <= 10, f"Themes count unreasonable for {planet}"
            
            # Check duration format
            assert "years" in meaning["duration"], f"Duration should mention years for {planet}"

    def test_fallback_behavior(self):
        """Test fallback behavior for unknown signs/planets."""
        # Test unknown sun sign
        unknown_sun = self.meanings.get_sun_sign_meaning("UnknownSign")
        assert "name" in unknown_sun
        assert unknown_sun["name"] == "UnknownSign"
        
        # Test unknown moon sign
        unknown_moon = self.meanings.get_moon_sign_meaning("UnknownSign")
        assert "name" in unknown_moon
        assert unknown_moon["name"] == "UnknownSign"
        
        # Test unknown ascendant
        unknown_asc = self.meanings.get_ascendant_meaning("UnknownSign")
        assert "name" in unknown_asc
        assert unknown_asc["name"] == "UnknownSign"
        
        # Test unknown dasha
        unknown_dasha = self.meanings.get_dasha_meaning("UnknownPlanet")
        assert "general_nature" in unknown_dasha

    def test_data_consistency(self):
        """Test consistency across different meaning types."""
        for sign in self.all_signs:
            sun_meaning = self.meanings.get_sun_sign_meaning(sign)
            moon_meaning = self.meanings.get_moon_sign_meaning(sign)
            asc_meaning = self.meanings.get_ascendant_meaning(sign)
            
            # Check that the English names are consistent
            assert sun_meaning["name"] == moon_meaning["name"] == asc_meaning["name"], \
                f"Inconsistent English names for {sign}"

if __name__ == "__main__":
    # Run tests
    test_instance = TestAstrologicalMeanings()
    test_instance.setup_method()
    
    print("🧪 Running Astrological Meanings Tests...")
    
    try:
        test_instance.test_all_sun_signs_have_complete_data()
        print("✅ All sun signs have complete data")
        
        test_instance.test_all_moon_signs_have_complete_data()
        print("✅ All moon signs have complete data")
        
        test_instance.test_all_ascendants_have_complete_data()
        print("✅ All ascendants have complete data")
        
        test_instance.test_all_dashas_have_complete_data()
        print("✅ All dashas have complete data")
        
        test_instance.test_general_explanations_exist()
        print("✅ General explanations exist")
        
        test_instance.test_sun_sign_data_quality()
        print("✅ Sun sign data quality validated")
        
        test_instance.test_moon_sign_data_quality()
        print("✅ Moon sign data quality validated")
        
        test_instance.test_ascendant_data_quality()
        print("✅ Ascendant data quality validated")
        
        test_instance.test_dasha_data_quality()
        print("✅ Dasha data quality validated")
        
        test_instance.test_fallback_behavior()
        print("✅ Fallback behavior validated")
        
        test_instance.test_data_consistency()
        print("✅ Data consistency validated")
        
        print("\n🎉 ALL TESTS PASSED! Astrological meanings data is complete and valid.")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
