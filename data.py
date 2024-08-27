# data.py

# Define how each zodiac sign modifies a planet's expression
zodiac_traits = {
    "Aries": ["assertiveness", "energy", "pioneering spirit"],
    "Taurus": ["stability", "practicality", "focus on security"],
    "Gemini": ["curiosity", "communication skills", "adaptability"],
    "Cancer": ["emotional sensitivity", "nurturing", "focus on home"],
    "Leo": ["confidence", "creativity", "desire for recognition"],
    "Virgo": ["analytical thinking", "attention to detail", "practicality"],
    "Libra": ["diplomacy", "sense of balance", "focus on relationships"],
    "Scorpio": ["intensity", "passion", "focus on transformation"],
    "Sagittarius": ["love for adventure", "learning", "freedom"],
    "Capricorn": ["ambition", "discipline", "focus on long-term goals"],
    "Aquarius": ["innovation", "independence", "focus on humanity"],
    "Pisces": ["compassion", "imagination", "spiritual focus"]
}

# Example of other components already defined
planet_traits = {
    "Sun": ["core identity", "ego", "sense of self"],
    "Moon": ["emotions", "instincts", "subconscious mind"],
    "Mercury": ["communication", "intellect", "learning"],
    "Venus": ["love", "beauty", "relationships"],
    "Mars": ["energy", "action", "assertiveness"],
    "Jupiter": ["expansion", "growth", "wisdom"],
    "Saturn": ["discipline", "structure", "limits"],
    "Uranus": ["innovation", "rebellion", "sudden changes"],
    "Neptune": ["imagination", "dreams", "spirituality"],
    "Pluto": ["transformation", "power", "regeneration"]
}

house_traits = {
    1: ["self", "identity", "personal appearance"],
    2: ["wealth", "possessions", "self-worth"],
    3: ["communication", "learning", "immediate environment"],
    4: ["home", "family", "emotional foundations"],
    5: ["creativity", "romance", "children"],
    6: ["work", "health", "daily routines"],
    7: ["partnerships", "marriage", "close relationships"],
    8: ["transformation", "shared resources", "intimacy"],
    9: ["philosophy", "higher learning", "travel"],
    10: ["career", "public life", "reputation"],
    11: ["friendships", "social groups", "aspirations"],
    12: ["spirituality", "subconscious", "hidden matters"]
}

# Include get_zodiac_sign and get_house functions as defined earlier
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

def get_house(position, ascendant):
    offset = (position - ascendant) % 360
    house = int(offset / 30) + 1
    return house
