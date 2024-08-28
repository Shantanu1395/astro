# process.py

from data import planetary_energies


def get_zodiac_sign(position):
    if 0 <= position < 30:
        return "Aries"
    elif 30 <= position < 60:
        return "Taurus"
    elif 60 <= position < 90:
        return "Gemini"
    elif 90 <= position < 120:
        return "Cancer"
    elif 120 <= position < 150:
        return "Leo"
    elif 150 <= position < 180:
        return "Virgo"
    elif 180 <= position < 210:
        return "Libra"
    elif 210 <= position < 240:
        return "Scorpio"
    elif 240 <= position < 270:
        return "Sagittarius"
    elif 270 <= position < 300:
        return "Capricorn"
    elif 300 <= position < 330:
        return "Aquarius"
    elif 330 <= position < 360:
        return "Pisces"


def get_house(cusp_positions, planet_position):
    for i in range(12):
        if cusp_positions[i] <= planet_position < cusp_positions[(i + 1) % 12]:
            return f"{i + 1}th House"
    return "12th House"  # Default to 12th House if no match found


def interpret_positions(positions, cusp_positions):
    interpretations = []
    for planet, position in positions.items():
        zodiac = get_zodiac_sign(position)
        house = get_house(cusp_positions, position)

        core_identity = planetary_energies.get(planet, {}).get('core_energy', {}).get('core identity', {})
        zodiac_data = core_identity.get(zodiac, {})
        house_data = zodiac_data.get(house, {})

        manifestation = house_data.get("manifestation", [])
        challenges = house_data.get("challenges", [])

        interpretations.append({
            "Planet": planet,
            "Zodiac": zodiac,
            "House": house,
            "Manifestation": manifestation,
            "Challenges": challenges
        })

    return interpretations
