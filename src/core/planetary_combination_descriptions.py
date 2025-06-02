"""
Comprehensive planetary combination descriptions for Vedic astrology.
Based on classical texts: Brihat Parashara Hora Shastra, Jataka Parijata, Saravali.
"""

def get_planet_in_sign_meaning(planet_name: str, sign: str) -> str:
    """Get detailed meaning of planet in specific sign."""

    # Normalize sign name
    sign_mapping = {
        "Mesh": "Aries", "Vrishabh": "Taurus", "Mithun": "Gemini", "Kark": "Cancer",
        "Simha": "Leo", "Kanya": "Virgo", "Tula": "Libra", "Vrishchik": "Scorpio",
        "Dhanu": "Sagittarius", "Makar": "Capricorn", "Kumbh": "Aquarius", "Meen": "Pisces"
    }
    normalized_sign = sign_mapping.get(sign, sign)

    combinations = {
        ("Sun", "Aries"): "Sun in Aries creates a powerful, dynamic personality with natural leadership abilities. You have pioneering spirit, courage, and strong willpower. This placement gives authority, independence, and the ability to initiate new projects. You're naturally confident and prefer to lead rather than follow.",

        ("Sun", "Taurus"): "Sun in Taurus creates a stable, practical personality with strong determination. You have a methodical approach to life, appreciate beauty and comfort, and possess great endurance. This placement gives material success through persistent effort and practical wisdom.",

        ("Sun", "Gemini"): "Sun in Gemini creates a versatile, communicative personality with intellectual curiosity. You have excellent communication skills, adaptability, and mental agility. This placement gives success through writing, speaking, teaching, or any field requiring mental dexterity.",

        ("Sun", "Cancer"): "Sun in Cancer creates a nurturing, intuitive personality with strong emotional depth. You have protective instincts, excellent memory, and deep connection to family and home. This placement gives success through caring professions and emotional intelligence.",

        ("Sun", "Leo"): "Sun in Leo creates a charismatic, creative personality with natural magnetism. You have dramatic flair, generous nature, and strong creative abilities. This placement gives leadership through inspiration, success in entertainment, and natural authority that others respect.",

        ("Sun", "Virgo"): "Sun in Virgo creates an analytical, service-oriented personality with attention to detail. You have practical wisdom, healing abilities, and perfectionist tendencies. This placement gives success through service, health fields, and methodical approaches to problems.",

        ("Sun", "Libra"): "Sun in Libra (debilitated) creates challenges with self-confidence and decision-making. However, it gives diplomatic skills, artistic appreciation, and ability to create harmony. Success comes through partnerships, arts, and balancing opposing forces.",

        ("Sun", "Scorpio"): "Sun in Scorpio creates an intense, transformative personality with deep psychological insight. You have magnetic presence, investigative abilities, and power to transform situations. This placement gives success through research, healing, and understanding hidden truths.",

        ("Sun", "Sagittarius"): "Sun in Sagittarius creates an optimistic, philosophical personality with love for wisdom and travel. You have teaching abilities, moral principles, and expansive vision. This placement gives success through education, spirituality, and sharing knowledge.",

        ("Sun", "Capricorn"): "Sun in Capricorn creates an ambitious, disciplined personality with strong organizational abilities. You have patience, responsibility, and ability to build lasting structures. This placement gives success through hard work, administration, and long-term planning.",

        ("Sun", "Aquarius"): "Sun in Aquarius creates an innovative, humanitarian personality with unique perspective. You have progressive ideas, scientific temperament, and concern for society. This placement gives success through technology, social causes, and unconventional approaches. Though the Sun is debilitated in Aquarius, it creates a unique individual who leads through innovation rather than traditional authority.",

        ("Sun", "Pisces"): "Sun in Pisces creates a compassionate, intuitive personality with spiritual inclinations. You have artistic abilities, empathetic nature, and connection to the divine. This placement gives success through healing, arts, spirituality, and serving others.",

        # Moon combinations
        ("Moon", "Aries"): "Moon in Aries creates an emotionally dynamic, impulsive nature with quick reactions. You have pioneering emotions, courage in feelings, and need for emotional independence. This placement gives emotional leadership and quick emotional recovery.",

        ("Moon", "Taurus"): "Moon in Taurus (exalted) creates emotional stability, sensual nature, and strong need for security. You have practical emotions, appreciation for beauty, and steady emotional responses. This placement gives emotional strength and material comfort.",

        ("Moon", "Gemini"): "Moon in Gemini creates emotionally versatile, communicative nature with changeable moods. You have intellectual emotions, need for mental stimulation, and ability to express feelings through words. This placement gives emotional adaptability.",

        ("Moon", "Cancer"): "Moon in Cancer (own sign) creates deeply nurturing, protective emotional nature with strong intuition. You have powerful maternal instincts, excellent memory, and deep emotional sensitivity. This placement gives emotional fulfillment through caring for others.",

        ("Moon", "Leo"): "Moon in Leo creates emotionally dramatic, generous nature with need for appreciation. You have warm emotions, creative feelings, and desire for emotional recognition. This placement gives emotional satisfaction through creative expression and being appreciated.",

        ("Moon", "Virgo"): "Moon in Virgo creates emotionally analytical, service-oriented nature with practical feelings. You have discriminating emotions, need for emotional order, and healing emotional nature. This placement gives emotional satisfaction through helping others.",

        ("Moon", "Libra"): "Moon in Libra creates emotionally harmonious, diplomatic nature with need for balance. You have refined emotions, appreciation for beauty, and desire for emotional partnership. This placement gives emotional fulfillment through relationships.",

        ("Moon", "Scorpio"): "Moon in Scorpio (debilitated) creates emotionally intense, transformative nature with deep feelings. You have powerful emotions, psychic abilities, and need for emotional depth. This placement gives emotional transformation through intense experiences.",

        ("Moon", "Sagittarius"): "Moon in Sagittarius creates emotionally optimistic, philosophical nature with love for freedom. You have expansive emotions, moral feelings, and need for emotional growth. This placement gives emotional satisfaction through learning and teaching.",

        ("Moon", "Capricorn"): "Moon in Capricorn creates emotionally disciplined, ambitious nature with practical feelings. You have controlled emotions, need for emotional achievement, and responsible emotional nature. This placement gives emotional satisfaction through accomplishment.",

        ("Moon", "Aquarius"): "Moon in Aquarius creates emotionally detached, humanitarian nature with unique feelings. You have progressive emotions, need for emotional freedom, and concern for collective welfare. This placement gives emotional satisfaction through social causes.",

        ("Moon", "Pisces"): "Moon in Pisces creates emotionally compassionate, intuitive nature with spiritual feelings. You have psychic emotions, empathetic nature, and connection to universal consciousness. This placement gives emotional fulfillment through spiritual service."
    }

    key = (planet_name, normalized_sign)
    return combinations.get(key, f"{planet_name} in {normalized_sign} creates a unique blend of {planet_name.lower()} energy expressed through {normalized_sign.lower()} characteristics. This combination influences how {planet_name.lower()} energy manifests in your life through {normalized_sign.lower()} traits and qualities.")

def get_planet_in_house_meaning(planet_name: str, house: int) -> str:
    """Get detailed meaning of planet in specific house."""

    house_meanings = {
        (1, "Sun"): "Sun in 1st house creates strong personality, leadership qualities, and natural authority. You have confidence, vitality, and ability to influence others. This placement gives success through personal efforts and individual achievements.",

        (1, "Moon"): "Moon in 1st house creates emotional, intuitive personality with changeable nature. You have strong connection to public, maternal qualities, and emotional expressiveness. This placement gives success through emotional intelligence and public relations.",

        (1, "Mars"): "Mars in 1st house creates energetic, courageous personality with competitive nature. You have physical strength, leadership through action, and pioneering spirit. This placement gives success through personal initiative and physical activities.",

        (1, "Mercury"): "Mercury in 1st house creates intelligent, communicative personality with quick thinking. You have excellent speaking abilities, youthful appearance, and mental agility. This placement gives success through communication and intellectual pursuits.",

        (1, "Jupiter"): "Jupiter in 1st house creates wise, optimistic personality with natural teaching abilities. You have moral character, spiritual inclinations, and ability to guide others. This placement gives success through wisdom and ethical conduct.",

        (1, "Venus"): "Venus in 1st house creates attractive, artistic personality with harmonious nature. You have natural charm, appreciation for beauty, and diplomatic skills. This placement gives success through arts, relationships, and aesthetic pursuits.",

        (1, "Saturn"): "Saturn in 1st house creates disciplined, serious personality with strong sense of responsibility. You have patience, endurance, and ability to work hard. This placement gives success through persistent effort and overcoming obstacles.",

        (1, "Rahu"): "Rahu in 1st house creates ambitious, unconventional personality with desire for recognition. You have magnetic presence, innovative ideas, and ability to break traditions. This placement gives success through unique approaches and foreign connections.",

        (1, "Ketu"): "Ketu in 1st house creates spiritual, detached personality with mystical inclinations. You have intuitive wisdom, disinterest in material recognition, and spiritual insights. This placement gives success through spiritual pursuits and inner development."
    }

    key = (house, planet_name)
    if key in house_meanings:
        return house_meanings[key]

    # Generic house meanings for other combinations
    generic_house_meanings = {
        1: f"{planet_name} in 1st house influences your personality, appearance, and overall approach to life. This placement makes {planet_name.lower()} energy a core part of your identity and how others perceive you.",
        2: f"{planet_name} in 2nd house influences your wealth, speech, family values, and resources. This placement affects how you earn money, communicate, and relate to family traditions.",
        3: f"{planet_name} in 3rd house influences your communication, siblings, courage, and short journeys. This placement affects your writing abilities, relationship with brothers/sisters, and personal initiative.",
        4: f"{planet_name} in 4th house influences your home, mother, emotional foundation, and inner peace. This placement affects your domestic life, relationship with mother, and emotional security.",
        5: f"{planet_name} in 5th house influences your creativity, children, intelligence, and romance. This placement affects your artistic abilities, relationship with children, and capacity for joy.",
        6: f"{planet_name} in 6th house influences your health, service, daily work, and enemies. This placement affects your work environment, health issues, and ability to overcome obstacles.",
        7: f"{planet_name} in 7th house influences your partnerships, marriage, business relationships, and open enemies. This placement affects your spouse, business partners, and public relationships.",
        8: f"{planet_name} in 8th house influences transformation, occult knowledge, shared resources, and longevity. This placement affects your ability to handle crises, research abilities, and spiritual transformation.",
        9: f"{planet_name} in 9th house influences your higher learning, spirituality, long journeys, and father. This placement affects your philosophical beliefs, relationship with father, and spiritual growth.",
        10: f"{planet_name} in 10th house influences your career, reputation, public image, and achievements. This placement affects your professional success, social status, and public recognition.",
        11: f"{planet_name} in 11th house influences your gains, friends, hopes, and elder siblings. This placement affects your income, social circle, and fulfillment of desires.",
        12: f"{planet_name} in 12th house influences your spirituality, losses, foreign connections, and liberation. This placement affects your spiritual development, expenses, and connection to foreign lands."
    }

    return generic_house_meanings.get(house, f"{planet_name} in house {house} creates specific influences in that life area.")

def get_combined_planet_sign_house_effect(planet_name: str, sign: str, house: int) -> str:
    """Get combined effect of planet in specific sign and house."""

    # Normalize sign name
    sign_mapping = {
        "Mesh": "Aries", "Vrishabh": "Taurus", "Mithun": "Gemini", "Kark": "Cancer",
        "Simha": "Leo", "Kanya": "Virgo", "Tula": "Libra", "Vrishchik": "Scorpio",
        "Dhanu": "Sagittarius", "Makar": "Capricorn", "Kumbh": "Aquarius", "Meen": "Pisces"
    }
    normalized_sign = sign_mapping.get(sign, sign)

    # Special combinations that create unique effects
    special_combinations = {
        ("Sun", "Aquarius", 1): "Sun in Aquarius in 1st house creates a unique personality that balances individual authority with humanitarian concerns. While the Sun is weakened in Aquarius, being in the 1st house gives personal strength. You have innovative leadership style, progressive ideas, and ability to lead social causes. This combination makes you a reformer who uses personal authority for collective benefit. You stand out as someone who challenges conventional thinking while maintaining respect for human dignity.",

        ("Sun", "Aquarius", 2): "Sun in Aquarius in 2nd house creates unconventional approaches to wealth and values. You earn money through innovative methods, technology, or humanitarian work. Your speech is progressive and inspiring. Family values may be non-traditional but deeply humanitarian.",

        ("Sun", "Aquarius", 3): "Sun in Aquarius in 3rd house creates innovative communication style and progressive relationships with siblings. You excel in modern communication methods, social media, and spreading humanitarian messages. Your courage comes from fighting for social causes.",

        ("Sun", "Aquarius", 4): "Sun in Aquarius in 4th house creates an unconventional home environment and progressive relationship with mother. Your emotional foundation is built on humanitarian ideals. You may live in modern, technologically advanced homes or communities.",

        ("Sun", "Aquarius", 5): "Sun in Aquarius in 5th house creates innovative creativity and progressive approach to children and education. You excel in modern arts, technology-based creativity, and progressive educational methods. Children may be raised with humanitarian values.",

        ("Sun", "Aquarius", 6): "Sun in Aquarius in 6th house creates service through humanitarian work and innovative health approaches. You excel in social service, modern healthcare, or technology-based solutions to everyday problems. Work involves helping society progress.",

        ("Sun", "Aquarius", 7): "Sun in Aquarius in 7th house creates partnerships based on shared humanitarian ideals. Your spouse or business partners are likely progressive, innovative, or involved in social causes. Relationships are based on friendship and shared vision for humanity.",

        ("Sun", "Aquarius", 8): "Sun in Aquarius in 8th house creates transformation through humanitarian work and innovative research. You excel in occult sciences, modern psychology, or revolutionary research. Transformation comes through serving collective consciousness.",

        ("Sun", "Aquarius", 9): "Sun in Aquarius in 9th house creates progressive spiritual beliefs and humanitarian philosophy. You excel in modern spiritual movements, progressive education, or spreading humanitarian ideals globally. Father may be progressive or humanitarian.",

        ("Sun", "Aquarius", 10): "Sun in Aquarius in 10th house creates career success through humanitarian work, technology, or social reform. You achieve recognition as an innovator, social reformer, or leader in progressive causes. Public image is that of a humanitarian leader.",

        ("Sun", "Aquarius", 11): "Sun in Aquarius in 11th house creates gains through humanitarian networks and progressive friendships. Your social circle consists of innovators, reformers, and humanitarian workers. Income comes through collective efforts and social causes.",

        ("Sun", "Aquarius", 12): "Sun in Aquarius in 12th house creates spiritual liberation through humanitarian service. You excel in behind-the-scenes humanitarian work, modern spiritual practices, or serving humanity without seeking recognition. Liberation comes through selfless service to collective consciousness.",

        ("Sun", "Leo", 10): "Sun in Leo in 10th house creates exceptional career success and public recognition. This is one of the most powerful combinations for leadership and authority. You have natural command over others, royal bearing, and ability to achieve high positions. This combination gives fame, respect, and success in government or leadership roles.",

        ("Moon", "Cancer", 4): "Moon in Cancer in 4th house creates the strongest possible emotional foundation and domestic happiness. This combination gives deep connection to mother, beautiful home, emotional stability, and nurturing nature. You have excellent intuition, strong family bonds, and ability to create emotional security for others.",

        ("Mars", "Aries", 1): "Mars in Aries in 1st house creates exceptional physical energy, courage, and leadership abilities. This combination gives warrior-like qualities, competitive spirit, and ability to overcome any obstacle. You have natural authority, physical strength, and pioneering capabilities that make you a natural leader.",

        ("Jupiter", "Sagittarius", 9): "Jupiter in Sagittarius in 9th house creates the highest spiritual wisdom and teaching abilities. This combination gives deep philosophical knowledge, moral character, and ability to guide others spiritually. You have natural connection to higher learning, foreign cultures, and spiritual traditions."
    }

    key = (planet_name, normalized_sign, house)
    if key in special_combinations:
        return special_combinations[key]

    # Generic combined effect
    return f"The combination of {planet_name} in {normalized_sign} in house {house} creates a unique blend where {planet_name.lower()}'s energy is expressed through {normalized_sign.lower()} characteristics and manifests in the {house}th house life area. This creates specific patterns in how {planet_name.lower()} influences your life through both the sign's qualities and the house's domain."

def get_life_manifestation_description(planet_name: str, sign: str, house: int) -> str:
    """Get description of how this combination manifests in daily life."""

    manifestations = {
        ("Sun", "Aquarius", 1): "In daily life, this manifests as someone who stands out for their unique perspective and humanitarian approach. People see you as an innovative leader who cares about social causes. You may work in technology, social reform, or progressive fields. Your leadership style is democratic rather than authoritarian, and you inspire others through your vision for a better future.",

        ("Sun", "Leo", 10): "In daily life, this manifests as natural authority and recognition in your career. You likely hold leadership positions, receive public acclaim, and have a reputation for excellence. People look up to you as a role model. Your career may involve entertainment, politics, or any field where you can shine and inspire others.",

        ("Moon", "Cancer", 4): "In daily life, this manifests as deep emotional satisfaction from home and family. You create a nurturing environment wherever you go. Your home is likely beautiful and welcoming. You have strong intuitive abilities and may be involved in real estate, hospitality, or caring professions. Family relationships are central to your happiness."
    }

    # Normalize sign name
    sign_mapping = {
        "Mesh": "Aries", "Vrishabh": "Taurus", "Mithun": "Gemini", "Kark": "Cancer",
        "Simha": "Leo", "Kanya": "Virgo", "Tula": "Libra", "Vrishchik": "Scorpio",
        "Dhanu": "Sagittarius", "Makar": "Capricorn", "Kumbh": "Aquarius", "Meen": "Pisces"
    }
    normalized_sign = sign_mapping.get(sign, sign)

    key = (planet_name, normalized_sign, house)
    if key in manifestations:
        return manifestations[key]

    return f"In daily life, this combination manifests through {planet_name.lower()}'s influence expressed via {normalized_sign.lower()} qualities in the {house}th house area of life. This creates specific patterns in how you experience and express {planet_name.lower()}'s energy in practical, everyday situations."

def get_timing_activation_description(planet_name: str, house: int) -> str:
    """Get description of when and how this planetary placement gets activated."""

    return f"This {planet_name} placement becomes most active during {planet_name} dasha periods, {planet_name}'s transit through important signs, and when the {house}th house is activated by other planetary transits. The effects are strongest during {planet_name}'s favorable periods and when you consciously work with {planet_name.lower()}'s energy through appropriate remedies and practices."
