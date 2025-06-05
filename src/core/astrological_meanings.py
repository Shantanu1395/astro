"""
Comprehensive astrological meanings for signs, ascendants, and dashas.
Based on classical Vedic astrology texts and modern interpretations.
"""

from typing import Dict, Any

class AstrologicalMeanings:
    def __init__(self):
        self.sun_sign_meanings = {
            "Mesha": {
                "name": "Aries",
                "element": "Fire",
                "quality": "Cardinal",
                "ruler": "Mars",
                "general_meaning": "Dynamic, pioneering, and energetic. Natural leaders with strong initiative and courage.",
                "personality_traits": ["Courageous", "Independent", "Competitive", "Impulsive", "Enthusiastic"],
                "strengths": ["Leadership", "Initiative", "Courage", "Energy", "Honesty"],
                "challenges": ["Impatience", "Aggression", "Selfishness", "Impulsiveness"],
                "life_purpose": "To lead, initiate new ventures, and inspire others through courage and action.",
                "career_inclinations": ["Military", "Sports", "Entrepreneurship", "Leadership roles", "Emergency services"],
                "relationships": "Passionate and direct in relationships, seeks partners who can match their energy."
            },
            "Vrishabha": {
                "name": "Taurus",
                "element": "Earth",
                "quality": "Fixed",
                "ruler": "Venus",
                "general_meaning": "Stable, practical, and sensual. Values security, beauty, and material comfort.",
                "personality_traits": ["Reliable", "Patient", "Practical", "Stubborn", "Sensual"],
                "strengths": ["Stability", "Persistence", "Loyalty", "Practicality", "Artistic sense"],
                "challenges": ["Stubbornness", "Materialism", "Resistance to change", "Possessiveness"],
                "life_purpose": "To build lasting foundations, create beauty, and provide stability to others.",
                "career_inclinations": ["Banking", "Real estate", "Arts", "Agriculture", "Luxury goods"],
                "relationships": "Loyal and devoted partners who value long-term commitment and stability."
            },
            "Mithuna": {
                "name": "Gemini",
                "element": "Air",
                "quality": "Mutable",
                "ruler": "Mercury",
                "general_meaning": "Versatile, communicative, and intellectually curious. Masters of adaptation and learning.",
                "personality_traits": ["Curious", "Adaptable", "Communicative", "Restless", "Witty"],
                "strengths": ["Communication", "Adaptability", "Intelligence", "Versatility", "Social skills"],
                "challenges": ["Inconsistency", "Superficiality", "Nervousness", "Indecisiveness"],
                "life_purpose": "To communicate, learn, and connect people through information and ideas.",
                "career_inclinations": ["Media", "Writing", "Teaching", "Sales", "Technology", "Translation"],
                "relationships": "Seeks mental stimulation and variety in relationships, values communication."
            },
            "Karka": {
                "name": "Cancer",
                "element": "Water",
                "quality": "Cardinal",
                "ruler": "Moon",
                "general_meaning": "Nurturing, intuitive, and emotionally deep. Natural caregivers with strong family bonds.",
                "personality_traits": ["Nurturing", "Intuitive", "Emotional", "Protective", "Moody"],
                "strengths": ["Empathy", "Intuition", "Nurturing", "Loyalty", "Imagination"],
                "challenges": ["Moodiness", "Over-sensitivity", "Clinginess", "Pessimism"],
                "life_purpose": "To nurture, protect, and provide emotional support to family and community.",
                "career_inclinations": ["Healthcare", "Childcare", "Hospitality", "Real estate", "Psychology"],
                "relationships": "Deeply emotional and caring partners who prioritize family and home."
            },
            "Simha": {
                "name": "Leo",
                "element": "Fire",
                "quality": "Fixed",
                "ruler": "Sun",
                "general_meaning": "Confident, creative, and charismatic. Natural performers who seek recognition and admiration.",
                "personality_traits": ["Confident", "Creative", "Generous", "Dramatic", "Proud"],
                "strengths": ["Leadership", "Creativity", "Generosity", "Confidence", "Warmth"],
                "challenges": ["Ego", "Arrogance", "Attention-seeking", "Stubbornness"],
                "life_purpose": "To inspire, create, and lead others through personal magnetism and creative expression.",
                "career_inclinations": ["Entertainment", "Politics", "Management", "Arts", "Public speaking"],
                "relationships": "Romantic and generous partners who enjoy being admired and appreciated."
            },
            "Kanya": {
                "name": "Virgo",
                "element": "Earth",
                "quality": "Mutable",
                "ruler": "Mercury",
                "general_meaning": "Analytical, practical, and service-oriented. Perfectionists who seek to improve and heal.",
                "personality_traits": ["Analytical", "Practical", "Helpful", "Critical", "Modest"],
                "strengths": ["Attention to detail", "Service", "Analysis", "Reliability", "Healing"],
                "challenges": ["Perfectionism", "Criticism", "Worry", "Over-analysis"],
                "life_purpose": "To serve, heal, and improve systems through careful analysis and practical solutions.",
                "career_inclinations": ["Healthcare", "Research", "Administration", "Quality control", "Service industries"],
                "relationships": "Devoted and helpful partners who show love through acts of service."
            },
            "Tula": {
                "name": "Libra",
                "element": "Air",
                "quality": "Cardinal",
                "ruler": "Venus",
                "general_meaning": "Harmonious, diplomatic, and relationship-oriented. Seeks balance and beauty in all aspects of life.",
                "personality_traits": ["Diplomatic", "Charming", "Balanced", "Indecisive", "Social"],
                "strengths": ["Diplomacy", "Fairness", "Charm", "Artistic sense", "Cooperation"],
                "challenges": ["Indecisiveness", "People-pleasing", "Superficiality", "Avoidance of conflict"],
                "life_purpose": "To create harmony, beauty, and justice through relationships and partnerships.",
                "career_inclinations": ["Law", "Diplomacy", "Arts", "Fashion", "Counseling", "Public relations"],
                "relationships": "Seeks partnership and harmony, values equality and mutual respect."
            },
            "Vrishchik": {
                "name": "Scorpio",
                "element": "Water",
                "quality": "Fixed",
                "ruler": "Mars",
                "general_meaning": "Intense, transformative, and mysterious. Seeks depth and truth in all experiences.",
                "personality_traits": ["Intense", "Passionate", "Mysterious", "Determined", "Transformative"],
                "strengths": ["Depth", "Transformation", "Intuition", "Determination", "Healing"],
                "challenges": ["Jealousy", "Possessiveness", "Secretiveness", "Vindictiveness"],
                "life_purpose": "To transform, heal, and uncover hidden truths through deep experiences.",
                "career_inclinations": ["Psychology", "Research", "Medicine", "Investigation", "Occult sciences"],
                "relationships": "Seeks deep, transformative connections with complete emotional intimacy."
            },
            "Dhanu": {
                "name": "Sagittarius",
                "element": "Fire",
                "quality": "Mutable",
                "ruler": "Jupiter",
                "general_meaning": "Philosophical, adventurous, and truth-seeking. Natural teachers and explorers.",
                "personality_traits": ["Optimistic", "Philosophical", "Adventurous", "Honest", "Restless"],
                "strengths": ["Wisdom", "Optimism", "Adventure", "Teaching", "Honesty"],
                "challenges": ["Restlessness", "Tactlessness", "Over-confidence", "Impatience"],
                "life_purpose": "To seek truth, share wisdom, and expand horizons through exploration and teaching.",
                "career_inclinations": ["Teaching", "Travel", "Publishing", "Philosophy", "Sports", "Law"],
                "relationships": "Seeks freedom and adventure in relationships, values honesty and growth."
            },
            "Makara": {
                "name": "Capricorn",
                "element": "Earth",
                "quality": "Cardinal",
                "ruler": "Saturn",
                "general_meaning": "Ambitious, disciplined, and practical. Natural achievers who build lasting structures.",
                "personality_traits": ["Ambitious", "Disciplined", "Practical", "Reserved", "Responsible"],
                "strengths": ["Discipline", "Ambition", "Responsibility", "Persistence", "Leadership"],
                "challenges": ["Pessimism", "Rigidity", "Workaholism", "Emotional distance"],
                "life_purpose": "To achieve mastery, build lasting structures, and lead through example.",
                "career_inclinations": ["Management", "Government", "Engineering", "Architecture", "Finance"],
                "relationships": "Seeks stable, long-term partnerships with shared goals and values."
            },
            "Kumbha": {
                "name": "Aquarius",
                "element": "Air",
                "quality": "Fixed",
                "ruler": "Saturn",
                "general_meaning": "Innovative, humanitarian, and independent. Visionaries who seek to improve society.",
                "personality_traits": ["Independent", "Innovative", "Humanitarian", "Eccentric", "Detached"],
                "strengths": ["Innovation", "Humanitarianism", "Independence", "Vision", "Friendship"],
                "challenges": ["Detachment", "Rebelliousness", "Unpredictability", "Emotional distance"],
                "life_purpose": "To innovate, reform society, and serve humanity through unique contributions.",
                "career_inclinations": ["Technology", "Social work", "Science", "Astrology", "Reform movements"],
                "relationships": "Values friendship and intellectual connection, needs freedom in relationships."
            },
            "Meena": {
                "name": "Pisces",
                "element": "Water",
                "quality": "Mutable",
                "ruler": "Jupiter",
                "general_meaning": "Compassionate, intuitive, and spiritual. Natural healers and artists with deep empathy.",
                "personality_traits": ["Compassionate", "Intuitive", "Artistic", "Dreamy", "Sensitive"],
                "strengths": ["Compassion", "Intuition", "Creativity", "Spirituality", "Healing"],
                "challenges": ["Escapism", "Over-sensitivity", "Confusion", "Victim mentality"],
                "life_purpose": "To heal, inspire, and serve others through compassion and spiritual understanding.",
                "career_inclinations": ["Arts", "Healing", "Spirituality", "Charity", "Music", "Photography"],
                "relationships": "Seeks deep emotional and spiritual connection, highly empathetic partner."
            }
        }

        self.moon_sign_meanings = {
            "Mesha": {
                "name": "Aries",
                "emotional_nature": "Impulsive and direct emotions, quick to anger but also quick to forgive.",
                "inner_self": "Needs independence and freedom to express emotions authentically.",
                "instinctive_reactions": "React quickly and decisively to emotional situations.",
                "comfort_needs": "Needs physical activity and challenges to feel emotionally balanced.",
                "relationship_style": "Direct and honest in emotional expression, values independence in relationships."
            },
            "Vrishabha": {
                "name": "Taurus",
                "emotional_nature": "Stable and steady emotions, slow to change but deeply felt.",
                "inner_self": "Needs security, comfort, and sensual pleasures for emotional well-being.",
                "instinctive_reactions": "Slow and measured responses, prefers to think before reacting.",
                "comfort_needs": "Needs physical comfort, good food, and beautiful surroundings.",
                "relationship_style": "Loyal and possessive, seeks long-term emotional security."
            },
            "Mithuna": {
                "name": "Gemini",
                "emotional_nature": "Changeable and curious emotions, needs mental stimulation.",
                "inner_self": "Needs variety, communication, and intellectual engagement.",
                "instinctive_reactions": "Responds with words and seeks to understand through communication.",
                "comfort_needs": "Needs mental stimulation, books, and social interaction.",
                "relationship_style": "Seeks mental connection and variety in emotional expression."
            },
            "Karka": {
                "name": "Cancer",
                "emotional_nature": "Deep and intuitive emotions, highly sensitive to environment.",
                "inner_self": "Needs emotional security, family connections, and nurturing.",
                "instinctive_reactions": "Highly intuitive responses, often based on gut feelings.",
                "comfort_needs": "Needs home, family, and emotional safety to thrive.",
                "relationship_style": "Deeply nurturing and protective, forms strong emotional bonds."
            },
            "Simha": {
                "name": "Leo",
                "emotional_nature": "Warm and generous emotions, needs appreciation and recognition.",
                "inner_self": "Needs to feel special, appreciated, and creatively expressed.",
                "instinctive_reactions": "Dramatic and expressive responses, seeks attention.",
                "comfort_needs": "Needs admiration, creative outlets, and luxury.",
                "relationship_style": "Generous and romantic, enjoys being the center of attention."
            },
            "Kanya": {
                "name": "Virgo",
                "emotional_nature": "Analytical and reserved emotions, processes feelings through logic.",
                "inner_self": "Needs order, usefulness, and the ability to help others.",
                "instinctive_reactions": "Analyzes emotions before expressing them, seeks practical solutions.",
                "comfort_needs": "Needs routine, cleanliness, and the ability to be useful.",
                "relationship_style": "Shows love through service and practical care."
            },
            "Tula": {
                "name": "Libra",
                "emotional_nature": "Harmonious and balanced emotions, seeks peace and beauty.",
                "inner_self": "Needs partnership, beauty, and harmonious relationships.",
                "instinctive_reactions": "Seeks balance and fairness, avoids conflict when possible.",
                "comfort_needs": "Needs beautiful surroundings, partnership, and social harmony.",
                "relationship_style": "Seeks equality and harmony, values partnership above all."
            },
            "Vrishchik": {
                "name": "Scorpio",
                "emotional_nature": "Intense and transformative emotions, feels everything deeply.",
                "inner_self": "Needs emotional depth, transformation, and authentic connections.",
                "instinctive_reactions": "Intense and passionate responses, seeks truth and depth.",
                "comfort_needs": "Needs privacy, emotional intensity, and transformative experiences.",
                "relationship_style": "Seeks deep, transformative emotional bonds with complete trust."
            },
            "Dhanu": {
                "name": "Sagittarius",
                "emotional_nature": "Optimistic and adventurous emotions, seeks meaning and growth.",
                "inner_self": "Needs freedom, adventure, and philosophical understanding.",
                "instinctive_reactions": "Optimistic and expansive responses, seeks higher meaning.",
                "comfort_needs": "Needs freedom, travel, and philosophical exploration.",
                "relationship_style": "Seeks growth and adventure in relationships, values honesty."
            },
            "Makara": {
                "name": "Capricorn",
                "emotional_nature": "Reserved and practical emotions, processes feelings through achievement.",
                "inner_self": "Needs structure, achievement, and respect from others.",
                "instinctive_reactions": "Cautious and practical responses, seeks long-term security.",
                "comfort_needs": "Needs structure, achievement, and social recognition.",
                "relationship_style": "Seeks stable, long-term partnerships with shared goals."
            },
            "Kumbha": {
                "name": "Aquarius",
                "emotional_nature": "Detached and humanitarian emotions, processes feelings intellectually.",
                "inner_self": "Needs freedom, friendship, and the ability to help humanity.",
                "instinctive_reactions": "Detached and rational responses, seeks innovative solutions.",
                "comfort_needs": "Needs freedom, friendship, and intellectual stimulation.",
                "relationship_style": "Values friendship and intellectual connection over emotional intensity."
            },
            "Meena": {
                "name": "Pisces",
                "emotional_nature": "Compassionate and intuitive emotions, highly empathetic and sensitive.",
                "inner_self": "Needs spiritual connection, creativity, and the ability to help others.",
                "instinctive_reactions": "Intuitive and empathetic responses, often absorbs others' emotions.",
                "comfort_needs": "Needs spiritual practices, creativity, and emotional safety.",
                "relationship_style": "Seeks deep spiritual and emotional connection, highly empathetic."
            }
        }

        self.ascendant_meanings = {
            "Mesha": {
                "name": "Aries",
                "first_impression": "Energetic, confident, and direct. Others see you as a natural leader.",
                "physical_appearance": "Athletic build, strong features, often with a prominent forehead.",
                "approach_to_life": "Direct, pioneering, and action-oriented. You prefer to lead rather than follow.",
                "life_path": "Your path involves learning to balance independence with cooperation.",
                "challenges": "Learning patience and considering others' perspectives before acting."
            },
            "Vrishabha": {
                "name": "Taurus",
                "first_impression": "Stable, reliable, and grounded. Others see you as dependable.",
                "physical_appearance": "Sturdy build, attractive features, often with a pleasant voice.",
                "approach_to_life": "Steady, practical, and methodical. You prefer stability and routine.",
                "life_path": "Your path involves building lasting foundations and appreciating beauty.",
                "challenges": "Learning to embrace change and avoid excessive materialism."
            },
            "Mithuna": {
                "name": "Gemini",
                "first_impression": "Intelligent, communicative, and versatile. Others see you as quick-witted.",
                "physical_appearance": "Youthful appearance, expressive hands, often tall and slender.",
                "approach_to_life": "Curious, adaptable, and communicative. You seek variety and mental stimulation.",
                "life_path": "Your path involves learning to focus and develop deeper understanding.",
                "challenges": "Learning to commit and avoid superficiality in relationships and pursuits."
            },
            "Karka": {
                "name": "Cancer",
                "first_impression": "Nurturing, protective, and emotionally sensitive. Others see you as caring.",
                "physical_appearance": "Round face, expressive eyes, often with a protective demeanor.",
                "approach_to_life": "Intuitive, protective, and family-oriented. You prioritize emotional security.",
                "life_path": "Your path involves learning to balance nurturing others with self-care.",
                "challenges": "Learning to overcome moodiness and not take things too personally."
            },
            "Simha": {
                "name": "Leo",
                "first_impression": "Confident, charismatic, and dramatic. Others see you as a natural leader.",
                "physical_appearance": "Strong, regal bearing, often with impressive hair and warm smile.",
                "approach_to_life": "Creative, generous, and attention-seeking. You want to shine and inspire.",
                "life_path": "Your path involves learning to lead with humility and share the spotlight.",
                "challenges": "Learning to manage ego and not become overly dramatic or attention-seeking."
            },
            "Kanya": {
                "name": "Virgo",
                "first_impression": "Practical, helpful, and detail-oriented. Others see you as reliable.",
                "physical_appearance": "Clean, neat appearance, often with intelligent eyes and precise movements.",
                "approach_to_life": "Analytical, service-oriented, and perfectionist. You seek to improve and help.",
                "life_path": "Your path involves learning to accept imperfection and not be overly critical.",
                "challenges": "Learning to overcome perfectionism and excessive worry about details."
            },
            "Tula": {
                "name": "Libra",
                "first_impression": "Charming, diplomatic, and balanced. Others see you as harmonious.",
                "physical_appearance": "Attractive, well-proportioned features, often with a pleasant smile.",
                "approach_to_life": "Diplomatic, relationship-focused, and beauty-loving. You seek harmony.",
                "life_path": "Your path involves learning to make decisions and assert your own needs.",
                "challenges": "Learning to overcome indecisiveness and people-pleasing tendencies."
            },
            "Vrishchik": {
                "name": "Scorpio",
                "first_impression": "Intense, mysterious, and powerful. Others see you as magnetic.",
                "physical_appearance": "Penetrating eyes, strong features, often with an air of mystery.",
                "approach_to_life": "Intense, transformative, and truth-seeking. You seek depth in everything.",
                "life_path": "Your path involves learning to transform yourself and help others heal.",
                "challenges": "Learning to trust others and not become overly suspicious or controlling."
            },
            "Dhanu": {
                "name": "Sagittarius",
                "first_impression": "Optimistic, adventurous, and philosophical. Others see you as inspiring.",
                "physical_appearance": "Tall, athletic build, often with an open, friendly expression.",
                "approach_to_life": "Adventurous, truth-seeking, and freedom-loving. You seek meaning and growth.",
                "life_path": "Your path involves learning to balance freedom with responsibility.",
                "challenges": "Learning to be more tactful and not become overly restless or dogmatic."
            },
            "Makara": {
                "name": "Capricorn",
                "first_impression": "Serious, ambitious, and responsible. Others see you as mature.",
                "physical_appearance": "Strong bone structure, often with a serious expression and dignified bearing.",
                "approach_to_life": "Ambitious, disciplined, and goal-oriented. You seek achievement and respect.",
                "life_path": "Your path involves learning to balance ambition with emotional expression.",
                "challenges": "Learning to lighten up and not become overly serious or pessimistic."
            },
            "Kumbha": {
                "name": "Aquarius",
                "first_impression": "Unique, independent, and humanitarian. Others see you as innovative.",
                "physical_appearance": "Distinctive features, often with an unconventional or futuristic style.",
                "approach_to_life": "Independent, humanitarian, and innovative. You seek to reform and improve.",
                "life_path": "Your path involves learning to balance independence with emotional connection.",
                "challenges": "Learning to be more emotionally available and not become overly detached."
            },
            "Meena": {
                "name": "Pisces",
                "first_impression": "Compassionate, dreamy, and spiritual. Others see you as empathetic.",
                "physical_appearance": "Soft features, dreamy eyes, often with a gentle, flowing movement.",
                "approach_to_life": "Intuitive, compassionate, and spiritual. You seek to heal and inspire.",
                "life_path": "Your path involves learning to set boundaries and not lose yourself in others.",
                "challenges": "Learning to be more grounded and not escape into fantasy or victim mentality."
            }
        }

        self.dasha_meanings = {
            "Sun": {
                "general_nature": "Period of leadership, authority, and self-expression.",
                "themes": ["Leadership", "Authority", "Government", "Father", "Soul purpose", "Recognition"],
                "positive_effects": "Brings leadership opportunities, recognition, government favor, spiritual growth",
                "challenges": "Can cause ego issues, conflicts with authority, health problems related to heart/bones",
                "guidance": "Focus on leadership roles, seek recognition for your work, maintain humility",
                "duration": "6 years in Vimshottari Dasha system"
            },
            "Moon": {
                "general_nature": "Period of emotional growth, intuition, and nurturing relationships.",
                "themes": ["Emotions", "Mother", "Home", "Intuition", "Public", "Travel"],
                "positive_effects": "Enhances intuition, brings emotional fulfillment, good for family relationships",
                "challenges": "Can cause emotional instability, mood swings, issues with mother or women",
                "guidance": "Focus on emotional well-being, nurture relationships, trust your intuition",
                "duration": "10 years in Vimshottari Dasha system"
            },
            "Mars": {
                "general_nature": "Energetic phase favoring action, courage, and new initiatives.",
                "themes": ["Energy", "Courage", "Competition", "Brothers", "Property", "Sports"],
                "positive_effects": "Increases energy, courage, good for sports and competition, property gains",
                "challenges": "Can cause aggression, accidents, conflicts, legal issues",
                "guidance": "Channel energy constructively, avoid conflicts, focus on physical fitness",
                "duration": "7 years in Vimshottari Dasha system"
            },
            "Mercury": {
                "general_nature": "Period emphasizing communication, learning, and intellectual pursuits.",
                "themes": ["Communication", "Learning", "Business", "Writing", "Travel", "Skills"],
                "positive_effects": "Enhances communication skills, good for education and business",
                "challenges": "Can cause nervous tension, communication problems, restlessness",
                "guidance": "Focus on learning, improve communication skills, engage in intellectual pursuits",
                "duration": "17 years in Vimshottari Dasha system"
            },
            "Jupiter": {
                "general_nature": "Highly auspicious time for wisdom, spirituality, and expansion.",
                "themes": ["Wisdom", "Spirituality", "Teaching", "Children", "Wealth", "Knowledge"],
                "positive_effects": "Brings wisdom, spiritual growth, good fortune, children, wealth",
                "challenges": "Can cause over-optimism, weight gain, liver problems",
                "guidance": "Focus on spiritual growth, teaching, and expanding your knowledge",
                "duration": "16 years in Vimshottari Dasha system"
            },
            "Venus": {
                "general_nature": "Period of creativity, relationships, and material pleasures.",
                "themes": ["Love", "Beauty", "Arts", "Luxury", "Relationships", "Creativity"],
                "positive_effects": "Enhances creativity, brings love and luxury, good for arts",
                "challenges": "Can cause over-indulgence, relationship problems, materialism",
                "guidance": "Focus on creative pursuits, nurture relationships, appreciate beauty",
                "duration": "20 years in Vimshottari Dasha system"
            },
            "Saturn": {
                "general_nature": "Period of discipline, hard work, and karmic lessons.",
                "themes": ["Discipline", "Hard work", "Karma", "Delays", "Responsibility", "Service"],
                "positive_effects": "Builds character, brings lasting achievements, teaches discipline",
                "challenges": "Can cause delays, obstacles, depression, health issues",
                "guidance": "Practice patience, work hard, serve others, learn from challenges",
                "duration": "19 years in Vimshottari Dasha system"
            },
            "Rahu": {
                "general_nature": "Period of material ambition, foreign connections, and unconventional paths.",
                "themes": ["Ambition", "Foreign", "Technology", "Illusion", "Materialism", "Innovation"],
                "positive_effects": "Brings material success, foreign opportunities, technological advancement",
                "challenges": "Can cause confusion, illusions, addiction, unconventional problems",
                "guidance": "Stay grounded, avoid shortcuts, focus on spiritual practices",
                "duration": "18 years in Vimshottari Dasha system"
            },
            "Ketu": {
                "general_nature": "Period of spiritual growth, detachment, and past-life karma.",
                "themes": ["Spirituality", "Detachment", "Past karma", "Mysticism", "Liberation", "Research"],
                "positive_effects": "Enhances spiritual growth, brings mystical experiences, research abilities",
                "challenges": "Can cause confusion, detachment from material world, health issues",
                "guidance": "Focus on spiritual practices, research, and letting go of attachments",
                "duration": "7 years in Vimshottari Dasha system"
            }
        }

    def get_sun_sign_meaning(self, sign: str) -> Dict[str, Any]:
        """Get comprehensive meaning of sun sign."""
        return self.sun_sign_meanings.get(sign, {
            "name": sign,
            "general_meaning": f"Detailed information for {sign} sun sign is being compiled.",
            "personality_traits": ["Unique", "Individual", "Special"],
            "life_purpose": f"To express the unique qualities of {sign} energy."
        })

    def get_moon_sign_meaning(self, sign: str) -> Dict[str, Any]:
        """Get comprehensive meaning of moon sign."""
        return self.moon_sign_meanings.get(sign, {
            "name": sign,
            "emotional_nature": f"Emotional patterns influenced by {sign} energy.",
            "inner_self": f"Inner needs shaped by {sign} characteristics."
        })

    def get_ascendant_meaning(self, sign: str) -> Dict[str, Any]:
        """Get comprehensive meaning of ascendant sign."""
        return self.ascendant_meanings.get(sign, {
            "name": sign,
            "first_impression": f"Others perceive you through {sign} energy.",
            "approach_to_life": f"Your life approach is influenced by {sign} characteristics."
        })

    def get_dasha_meaning(self, planet: str) -> Dict[str, Any]:
        """Get comprehensive meaning of dasha period."""
        return self.dasha_meanings.get(planet, {
            "general_nature": f"Period influenced by {planet} energy.",
            "themes": [f"{planet} influence", "Personal growth", "Life lessons"],
            "guidance": f"Focus on {planet.lower()} related activities and growth."
        })

    def get_general_explanations(self) -> Dict[str, str]:
        """Get general explanations for astrological concepts."""
        return {
            "sun_sign": "Your Sun sign represents your core identity, ego, and life purpose. It shows how you express your essential self and what drives you in life.",
            "moon_sign": "Your Moon sign represents your emotional nature, inner self, and subconscious patterns. It shows how you process emotions and what you need for emotional security.",
            "ascendant": "Your Ascendant (Rising sign) represents your outer personality, first impressions, and approach to life. It's the mask you wear and how others initially perceive you.",
            "dasha": "Dasha periods are planetary time cycles in Vedic astrology that influence different phases of your life. Each planet's period brings specific themes, opportunities, and challenges."
        }
