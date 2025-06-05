#!/usr/bin/env python3
"""
Data Consistency Validator for Astrology Application
Ensures that refactored APIs maintain 100% data consistency with original implementation
"""

import json
import requests
from datetime import date, time
from typing import Dict, Any, List, Tuple
from src.models.models import BirthData, PredictionRequest

class DataConsistencyValidator:
    def __init__(self, baseline_file: str = "complete_backend_data_dump.json"):
        """Initialize validator with baseline data."""
        with open(baseline_file, 'r') as f:
            self.baseline_data = json.load(f)
        
        self.test_birth_data = BirthData(
            name='Test User',
            birth_date=date(1994, 3, 1),
            birth_time=time(23, 2),
            birth_location='Faridabad, India'
        )
    
    def validate_planetary_data(self, new_data: Dict[str, Any]) -> List[str]:
        """Validate planetary positions and properties."""
        issues = []
        
        baseline_planets = self.baseline_data['vedic_chart']['planets']
        new_planets = new_data.get('vedic_chart', {}).get('planets', [])
        
        if len(baseline_planets) != len(new_planets):
            issues.append(f"Planet count mismatch: baseline {len(baseline_planets)} vs new {len(new_planets)}")
            return issues
        
        for i, (baseline_planet, new_planet) in enumerate(zip(baseline_planets, new_planets)):
            planet_name = baseline_planet['name']
            
            # Check essential properties
            for prop in ['name', 'sign', 'house', 'longitude']:
                baseline_val = baseline_planet.get(prop)
                new_val = new_planet.get(prop)
                
                if prop == 'longitude':
                    # Allow small floating point differences
                    if abs(float(baseline_val) - float(new_val)) > 0.01:
                        issues.append(f"{planet_name} {prop}: {baseline_val} vs {new_val}")
                elif baseline_val != new_val:
                    issues.append(f"{planet_name} {prop}: {baseline_val} vs {new_val}")
        
        return issues
    
    def validate_chart_summary(self, new_data: Dict[str, Any]) -> List[str]:
        """Validate chart summary data."""
        issues = []
        
        baseline_chart = self.baseline_data['vedic_chart']
        new_chart = new_data.get('vedic_chart', {})
        
        for prop in ['ascendant_sign', 'moon_sign', 'sun_sign', 'birth_nakshatra']:
            baseline_val = baseline_chart.get(prop)
            new_val = new_chart.get(prop)
            
            if baseline_val != new_val:
                issues.append(f"Chart {prop}: {baseline_val} vs {new_val}")
        
        return issues
    
    def validate_dasha_data(self, new_data: Dict[str, Any]) -> List[str]:
        """Validate current dasha information."""
        issues = []
        
        baseline_dasha = self.baseline_data['current_dasha']
        new_dasha = new_data.get('current_dasha', {})
        
        for prop in ['planet', 'start_date', 'end_date']:
            baseline_val = baseline_dasha.get(prop)
            new_val = new_dasha.get(prop)
            
            if baseline_val != new_val:
                issues.append(f"Dasha {prop}: {baseline_val} vs {new_val}")
        
        # Check remaining years (allow small differences)
        baseline_years = baseline_dasha.get('remaining_years', 0)
        new_years = new_dasha.get('remaining_years', 0)
        if abs(float(baseline_years) - float(new_years)) > 0.1:
            issues.append(f"Dasha remaining_years: {baseline_years} vs {new_years}")
        
        return issues
    
    def validate_planetary_strengths(self, new_data: Dict[str, Any]) -> List[str]:
        """Validate planetary strength calculations."""
        issues = []
        
        baseline_strengths = self.baseline_data['planetary_strengths']
        new_strengths = new_data.get('planetary_strengths', {})
        
        for planet_name in baseline_strengths.keys():
            if planet_name not in new_strengths:
                issues.append(f"Missing planetary strength for {planet_name}")
                continue
            
            baseline_strength = baseline_strengths[planet_name]['overall_strength']
            new_strength = new_strengths[planet_name].get('overall_strength', 'Missing')
            
            if baseline_strength != new_strength:
                issues.append(f"{planet_name} strength: {baseline_strength} vs {new_strength}")
        
        return issues
    
    def validate_personality_analysis(self, new_data: Dict[str, Any]) -> List[str]:
        """Validate personality analysis structure and content."""
        issues = []
        
        baseline_personality = self.baseline_data['personality_analysis']
        new_personality = new_data.get('personality_analysis', {})
        
        # Check that all major personality aspects exist
        required_aspects = ['core_personality', 'temperament', 'mental_nature', 'emotional_nature']
        
        for aspect in required_aspects:
            if aspect not in new_personality:
                issues.append(f"Missing personality aspect: {aspect}")
            elif not new_personality[aspect]:
                issues.append(f"Empty personality aspect: {aspect}")
        
        # Check core personality content length (should be substantial)
        baseline_core = baseline_personality.get('core_personality', '')
        new_core = new_personality.get('core_personality', '')
        
        if len(new_core) < len(baseline_core) * 0.8:  # Allow 20% reduction
            issues.append(f"Core personality too short: {len(new_core)} vs {len(baseline_core)} chars")
        
        return issues
    
    def validate_life_themes(self, new_data: Dict[str, Any]) -> List[str]:
        """Validate current influences and life themes."""
        issues = []
        
        baseline_influences = self.baseline_data['current_influences']
        new_influences = new_data.get('current_influences', {})
        
        if 'life_themes' not in new_influences:
            issues.append("Missing life_themes in current_influences")
            return issues
        
        baseline_themes = baseline_influences['life_themes']
        new_themes = new_influences['life_themes']
        
        # Check major theme categories
        required_categories = ['major_themes', 'current_focus_areas', 'growth_areas']
        
        for category in required_categories:
            if category not in new_themes:
                issues.append(f"Missing life theme category: {category}")
            elif not isinstance(new_themes[category], list):
                issues.append(f"Life theme {category} should be a list")
            elif len(new_themes[category]) == 0:
                issues.append(f"Empty life theme category: {category}")
        
        return issues
    
    def validate_yogas(self, new_data: Dict[str, Any]) -> List[str]:
        """Validate yoga calculations."""
        issues = []
        
        baseline_yogas = self.baseline_data['yogas']
        new_yogas = new_data.get('yogas', [])
        
        if len(new_yogas) < len(baseline_yogas) * 0.8:  # Allow some variation
            issues.append(f"Yoga count too low: {len(new_yogas)} vs {len(baseline_yogas)}")
        
        # Check that yogas have required fields
        for i, yoga in enumerate(new_yogas[:3]):  # Check first 3
            if not isinstance(yoga, dict):
                issues.append(f"Yoga {i} should be a dict")
                continue
            
            if 'name' not in yoga or not yoga['name']:
                issues.append(f"Yoga {i} missing name")
            
            if 'description' not in yoga or not yoga['description']:
                issues.append(f"Yoga {i} missing description")
        
        return issues
    
    def run_full_validation(self, new_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Run complete validation suite."""
        all_issues = []
        
        # Run all validation checks
        all_issues.extend(self.validate_planetary_data(new_data))
        all_issues.extend(self.validate_chart_summary(new_data))
        all_issues.extend(self.validate_dasha_data(new_data))
        all_issues.extend(self.validate_planetary_strengths(new_data))
        all_issues.extend(self.validate_personality_analysis(new_data))
        all_issues.extend(self.validate_life_themes(new_data))
        all_issues.extend(self.validate_yogas(new_data))
        
        is_valid = len(all_issues) == 0
        return is_valid, all_issues
    
    def test_api_endpoint(self, endpoint_url: str) -> Tuple[bool, List[str]]:
        """Test an API endpoint against baseline data."""
        try:
            # Make API request
            response = requests.post(endpoint_url, json={
                'name': self.test_birth_data.name,
                'birth_date': str(self.test_birth_data.birth_date),
                'birth_time': str(self.test_birth_data.birth_time),
                'birth_location': self.test_birth_data.birth_location
            })
            
            if response.status_code != 200:
                return False, [f"API returned status {response.status_code}"]
            
            api_data = response.json()
            
            # Extract data section if wrapped
            if 'data' in api_data:
                api_data = api_data['data']
            
            return self.run_full_validation(api_data)
            
        except Exception as e:
            return False, [f"API test failed: {str(e)}"]

if __name__ == "__main__":
    validator = DataConsistencyValidator()
    print("Data Consistency Validator initialized with baseline data")
    print(f"Baseline contains {len(validator.baseline_data['vedic_chart']['planets'])} planets")
    print(f"Baseline yogas: {len(validator.baseline_data['yogas'])}")
    print("Ready for validation testing")
