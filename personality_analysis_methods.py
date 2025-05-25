"""
Additional personality analysis methods for vedic_analysis.py
These methods will be integrated into the VedicAnalyzer class
"""

def _get_house_personality_influence(self, house: int, planet_type: str) -> Dict[str, Any]:
    """Get personality influence based on house position."""
    house_influences = {
        1: {
            "personality_focus": "Self-expression and personal identity",
            "life_emphasis": "Personal development and self-awareness",
            "behavioral_tendency": "Direct, self-focused, pioneering approach to life"
        },
        2: {
            "personality_focus": "Values, resources, and self-worth",
            "life_emphasis": "Building security and expressing personal values",
            "behavioral_tendency": "Practical, value-oriented, security-conscious approach"
        },
        3: {
            "personality_focus": "Communication and immediate environment",
            "life_emphasis": "Learning, communicating, and connecting with others",
            "behavioral_tendency": "Curious, communicative, socially active approach"
        },
        4: {
            "personality_focus": "Emotional foundation and inner security",
            "life_emphasis": "Creating emotional stability and nurturing others",
            "behavioral_tendency": "Nurturing, protective, emotionally-driven approach"
        },
        5: {
            "personality_focus": "Creativity and self-expression",
            "life_emphasis": "Creative expression and personal joy",
            "behavioral_tendency": "Creative, playful, self-expressive approach"
        },
        6: {
            "personality_focus": "Service and daily improvement",
            "life_emphasis": "Helping others and perfecting skills",
            "behavioral_tendency": "Service-oriented, detail-focused, improvement-minded approach"
        },
        7: {
            "personality_focus": "Relationships and partnerships",
            "life_emphasis": "Creating harmony and cooperation with others",
            "behavioral_tendency": "Relationship-focused, diplomatic, partnership-oriented approach"
        },
        8: {
            "personality_focus": "Transformation and hidden depths",
            "life_emphasis": "Deep transformation and understanding mysteries",
            "behavioral_tendency": "Intense, transformative, depth-seeking approach"
        },
        9: {
            "personality_focus": "Higher wisdom and spiritual growth",
            "life_emphasis": "Seeking truth and expanding consciousness",
            "behavioral_tendency": "Philosophical, wisdom-seeking, expansive approach"
        },
        10: {
            "personality_focus": "Achievement and public recognition",
            "life_emphasis": "Building reputation and achieving goals",
            "behavioral_tendency": "Ambitious, goal-oriented, authority-seeking approach"
        },
        11: {
            "personality_focus": "Group involvement and future goals",
            "life_emphasis": "Working with groups and achieving aspirations",
            "behavioral_tendency": "Group-oriented, future-focused, humanitarian approach"
        },
        12: {
            "personality_focus": "Spiritual transcendence and service",
            "life_emphasis": "Spiritual growth and selfless service",
            "behavioral_tendency": "Spiritual, selfless, transcendent approach"
        }
    }
    
    base_influence = house_influences.get(house, {
        "personality_focus": "Personal growth",
        "life_emphasis": "Individual development",
        "behavioral_tendency": "Unique personal approach"
    })
    
    # Add planet-specific context
    if planet_type == "sun":
        base_influence["sun_context"] = f"Your core identity and ego are expressed through {base_influence['personality_focus'].lower()}."
    elif planet_type == "moon":
        base_influence["moon_context"] = f"Your emotional nature and instincts are channeled through {base_influence['personality_focus'].lower()}."
    
    return base_influence

def _integrate_personality_influences(self, ascendant_traits: Dict, sun_traits: Dict, moon_traits: Dict) -> Dict[str, Any]:
    """Integrate ascendant, sun, and moon influences into unified personality description."""
    
    # Extract key traits from each influence
    asc_core = ascendant_traits.get("core_traits", [])
    sun_core = sun_traits.get("core_traits", [])
    moon_core = moon_traits.get("core_traits", [])
    
    # Combine and prioritize traits
    all_traits = asc_core + sun_core + moon_core
    trait_counts = {}
    for trait in all_traits:
        trait_counts[trait] = trait_counts.get(trait, 0) + 1
    
    # Get most prominent traits
    prominent_traits = [trait for trait, count in sorted(trait_counts.items(), key=lambda x: x[1], reverse=True)][:5]
    
    # Create integrated description
    integrated_description = f"""
    Your personality is a unique blend of influences:
    
    **Public Persona (Ascendant)**: Others see you as {', '.join(asc_core[:3]).lower()}
    **Core Self (Sun)**: Your authentic self is {', '.join(sun_core[:3]).lower()}
    **Emotional Nature (Moon)**: Your inner emotional world is {', '.join(moon_core[:3]).lower()}
    
    **Most Prominent Traits**: {', '.join(prominent_traits)}
    
    This creates a personality that balances external presentation with inner authenticity and emotional depth.
    """
    
    return {
        "prominent_traits": prominent_traits,
        "personality_blend": integrated_description,
        "complexity_level": "High" if len(set(all_traits)) > 10 else "Moderate",
        "internal_harmony": "Harmonious" if len(set(prominent_traits[:3])) == len(prominent_traits[:3]) else "Complex"
    }

def _get_temperament_description(self, dominant_element: str, dominant_mode: str, elements: Dict, modes: Dict) -> str:
    """Get detailed temperament description based on elemental and modal distribution."""
    
    element_descriptions = {
        "Fire": "Energetic, enthusiastic, action-oriented, and spontaneous. You approach life with passion and directness.",
        "Earth": "Practical, stable, methodical, and grounded. You prefer tangible results and steady progress.",
        "Air": "Mental, communicative, social, and adaptable. You thrive on ideas, communication, and variety.",
        "Water": "Emotional, intuitive, sensitive, and empathetic. You navigate life through feelings and intuition."
    }
    
    mode_descriptions = {
        "Cardinal": "Initiative-taking, leadership-oriented, and change-making. You like to start new projects and lead others.",
        "Fixed": "Determined, persistent, and stable. You prefer to see things through to completion and resist change.",
        "Mutable": "Adaptable, flexible, and versatile. You easily adjust to changing circumstances and enjoy variety."
    }
    
    base_description = f"Your temperament is primarily {dominant_mode} {dominant_element}. "
    base_description += element_descriptions.get(dominant_element, "")
    base_description += " " + mode_descriptions.get(dominant_mode, "")
    
    # Add secondary influences
    sorted_elements = sorted(elements.items(), key=lambda x: x[1], reverse=True)
    sorted_modes = sorted(modes.items(), key=lambda x: x[1], reverse=True)
    
    if len(sorted_elements) > 1 and sorted_elements[1][1] > 0:
        secondary_element = sorted_elements[1][0]
        base_description += f" You also have significant {secondary_element} influence, adding {element_descriptions.get(secondary_element, '').lower()}"
    
    return base_description

def _get_temperament_behaviors(self, dominant_element: str, dominant_mode: str) -> List[str]:
    """Get specific behavioral tendencies based on temperament."""
    
    behaviors = {
        ("Cardinal", "Fire"): [
            "Takes immediate action on ideas",
            "Natural leader in crisis situations", 
            "Initiates new projects with enthusiasm",
            "Can be impatient with slow progress",
            "Prefers to lead rather than follow"
        ],
        ("Fixed", "Fire"): [
            "Maintains steady energy and determination",
            "Loyal and consistent in relationships",
            "Can be stubborn about changing direction",
            "Builds lasting creative projects",
            "Strong willpower and persistence"
        ],
        ("Mutable", "Fire"): [
            "Adapts energy to different situations",
            "Enjoys variety in activities and interests",
            "Can scatter energy across many projects",
            "Flexible in approach but maintains enthusiasm",
            "Good at inspiring others through change"
        ],
        ("Cardinal", "Earth"): [
            "Organizes and structures new ventures",
            "Takes practical steps toward goals",
            "Natural ability to manage resources",
            "Prefers concrete, measurable results",
            "Initiates practical solutions to problems"
        ],
        ("Fixed", "Earth"): [
            "Builds lasting, stable foundations",
            "Extremely reliable and dependable",
            "Resists change unless absolutely necessary",
            "Values security and material stability",
            "Patient and methodical in approach"
        ],
        ("Mutable", "Earth"): [
            "Adapts practical skills to new situations",
            "Flexible in methods while maintaining practicality",
            "Good at finding efficient solutions",
            "Can adjust plans based on practical considerations",
            "Balances stability with necessary change"
        ],
        ("Cardinal", "Air"): [
            "Initiates communication and social connections",
            "Natural networker and relationship builder",
            "Starts intellectual projects and discussions",
            "Can be impatient with detailed follow-through",
            "Prefers to delegate rather than execute"
        ],
        ("Fixed", "Air"): [
            "Maintains consistent communication style",
            "Loyal to ideas and intellectual principles",
            "Can be stubborn about changing opinions",
            "Builds lasting intellectual relationships",
            "Persistent in pursuing knowledge"
        ],
        ("Mutable", "Air"): [
            "Adapts communication to different audiences",
            "Enjoys learning about diverse topics",
            "Can change opinions based on new information",
            "Flexible in social situations",
            "Good at mediating different viewpoints"
        ],
        ("Cardinal", "Water"): [
            "Initiates emotional connections and healing",
            "Natural caregiver and emotional leader",
            "Starts projects based on emotional inspiration",
            "Can be moody when things don't go as planned",
            "Prefers to nurture rather than compete"
        ],
        ("Fixed", "Water"): [
            "Maintains deep, lasting emotional bonds",
            "Extremely loyal and protective of loved ones",
            "Can hold onto emotions for long periods",
            "Builds emotional security through consistency",
            "Persistent in emotional and spiritual pursuits"
        ],
        ("Mutable", "Water"): [
            "Adapts emotionally to different situations",
            "Empathetic and understanding of others' feelings",
            "Can absorb others' emotions easily",
            "Flexible in emotional expression",
            "Good at helping others through emotional changes"
        ]
    }
    
    key = (dominant_mode, dominant_element)
    return behaviors.get(key, [
        "Unique behavioral patterns",
        "Individual approach to life",
        "Personal style of interaction",
        "Distinctive way of handling challenges",
        "Special combination of traits"
    ])
