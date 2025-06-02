#!/usr/bin/env python3
"""
Test script to call the API and save formatted output.
"""

import requests
import json

def test_shantanu_api():
    """Test the Shantanu API endpoint and save formatted output."""
    try:
        response = requests.get("http://localhost:8000/api/test/shantanu")
        
        if response.status_code == 200:
            data = response.json()
            
            # Save full response to file
            with open("shantanu_prediction.json", "w") as f:
                json.dump(data, f, indent=2)
            
            print("✅ API Test Successful!")
            print(f"📊 Response saved to: shantanu_prediction.json")
            
            # Print summary
            if data.get("success"):
                print("\n📋 SUMMARY:")
                print(f"Name: {data['birth_data']['name']}")
                print(f"Birth Date: {data['birth_data']['birth_date']}")
                print(f"Ascendant: {data['chart_summary']['ascendant_sign']}")
                print(f"Moon Sign: {data['chart_summary']['moon_sign']}")
                print(f"Sun Sign: {data['chart_summary']['sun_sign']}")
                print(f"Current Dasha: {data['current_dasha']['planet']} ({data['current_dasha']['remaining_years']:.1f} years remaining)")
                
                # Count remedies needed
                remedies_needed = sum(1 for planet_data in data['planetary_analysis']['remedies'].values() 
                                    if planet_data.get('remedies_needed', False))
                print(f"Planets needing remedies: {remedies_needed}/9")
                
                # Count yogas
                yogas_count = len(data.get('yogas', []))
                print(f"Yogas identified: {yogas_count}")
                
                print("\n🌟 KEY THEMES:")
                for theme in data['prediction']['key_themes']:
                    print(f"  • {theme}")
                
            else:
                print(f"❌ API Error: {data.get('error', 'Unknown error')}")
                
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_shantanu_api()
