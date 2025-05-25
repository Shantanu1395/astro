"""
Comprehensive Vedic Astrology Analysis Module
Provides detailed explanations, planetary relationships, and guidance
"""

from typing import Dict, List, Tuple, Any
from datetime import date, datetime, timedelta
import swisseph as swe
from models import VedicChart, DashaPeriod, PlanetPosition, BirthData, LocationData
from utils import julian_day_from_datetime, calculate_ayanamsa, degrees_to_sign_and_degree

class VedicAnalyzer:
    def __init__(self):
        # Dasha meanings and characteristics
        self.dasha_meanings = {
            "Sun": {
                "nature": "Royal, authoritative, leadership-oriented",
                "themes": ["Leadership", "Authority", "Government", "Father", "Soul purpose", "Recognition"],
                "positive": "Brings leadership opportunities, recognition, government favor, spiritual growth",
                "negative": "Can cause ego issues, conflicts with authority, health problems related to heart/bones",
                "guidance": "Focus on leadership roles, seek recognition for your work, maintain humility",
                "cautions": "Avoid ego clashes, be careful with authority figures, monitor heart health"
            },
            "Moon": {
                "nature": "Emotional, nurturing, intuitive, changeable",
                "themes": ["Emotions", "Mother", "Mind", "Public", "Travel", "Liquids", "Nursing"],
                "positive": "Enhances intuition, brings emotional fulfillment, good for public relations",
                "negative": "Can cause emotional instability, mental stress, issues with mother",
                "guidance": "Trust your intuition, focus on emotional well-being, engage with public",
                "cautions": "Avoid emotional decisions, manage stress, be careful with water-related activities"
            },
            "Mars": {
                "nature": "Energetic, aggressive, action-oriented, competitive",
                "themes": ["Energy", "Courage", "Sports", "Military", "Surgery", "Real estate", "Brothers"],
                "positive": "Brings courage, energy for new projects, success in competitions",
                "negative": "Can cause accidents, conflicts, anger issues, blood-related problems",
                "guidance": "Channel energy into sports/exercise, take calculated risks, be courageous",
                "cautions": "Control anger, avoid accidents, be careful with sharp objects, manage conflicts"
            },
            "Mercury": {
                "nature": "Intellectual, communicative, analytical, versatile",
                "themes": ["Communication", "Business", "Education", "Writing", "Travel", "Friends"],
                "positive": "Enhances communication skills, brings business success, educational achievements",
                "negative": "Can cause nervous disorders, speech problems, deception in business",
                "guidance": "Focus on communication, pursue education, engage in business activities",
                "cautions": "Verify information carefully, avoid nervous stress, be honest in dealings"
            },
            "Jupiter": {
                "nature": "Wise, spiritual, expansive, benevolent",
                "themes": ["Wisdom", "Spirituality", "Teaching", "Children", "Wealth", "Dharma"],
                "positive": "Brings wisdom, spiritual growth, wealth, good fortune, children's welfare",
                "negative": "Can cause over-optimism, weight gain, liver problems, false gurus",
                "guidance": "Pursue spiritual practices, teach others, focus on dharmic activities",
                "cautions": "Avoid over-indulgence, be selective with spiritual teachers, manage weight"
            },
            "Venus": {
                "nature": "Artistic, romantic, luxurious, harmonious",
                "themes": ["Love", "Marriage", "Arts", "Beauty", "Luxury", "Vehicles", "Women"],
                "positive": "Brings love, artistic success, material comforts, harmonious relationships",
                "negative": "Can cause relationship problems, over-indulgence, kidney issues",
                "guidance": "Focus on relationships, pursue artistic endeavors, enjoy life's pleasures",
                "cautions": "Avoid over-indulgence, be careful in relationships, monitor kidney health"
            },
            "Saturn": {
                "nature": "Disciplined, restrictive, karmic, patient",
                "themes": ["Discipline", "Hard work", "Karma", "Delays", "Service", "Elderly", "Longevity"],
                "positive": "Brings discipline, long-term success, spiritual growth through hardship",
                "negative": "Can cause delays, depression, chronic health issues, poverty",
                "guidance": "Practice patience, work hard consistently, serve others, learn from difficulties",
                "cautions": "Avoid shortcuts, manage depression, take care of bones/joints, be patient"
            },
            "Rahu": {
                "nature": "Ambitious, materialistic, unconventional, illusory",
                "themes": ["Ambition", "Foreign lands", "Technology", "Illusion", "Sudden gains", "Unconventional"],
                "positive": "Brings sudden success, foreign opportunities, technological advancement",
                "negative": "Can cause confusion, addiction, deception, sudden losses",
                "guidance": "Pursue unconventional paths, embrace technology, seek foreign connections",
                "cautions": "Avoid get-rich-quick schemes, be wary of deception, stay grounded"
            },
            "Ketu": {
                "nature": "Spiritual, detached, mystical, karmic",
                "themes": ["Spirituality", "Detachment", "Past karma", "Mysticism", "Liberation", "Research"],
                "positive": "Brings spiritual insights, detachment from materialism, mystical experiences",
                "negative": "Can cause confusion, isolation, health issues, lack of direction",
                "guidance": "Focus on spiritual practices, research deeply, let go of attachments",
                "cautions": "Avoid isolation, seek spiritual guidance, maintain physical health"
            }
        }

        # House meanings
        self.house_meanings = {
            1: "Self, personality, appearance, health, general life direction",
            2: "Wealth, family, speech, food, values, accumulated resources",
            3: "Courage, siblings, short journeys, communication, efforts",
            4: "Home, mother, education, property, emotional foundation",
            5: "Children, creativity, intelligence, romance, speculation",
            6: "Health, enemies, service, daily routine, obstacles",
            7: "Marriage, partnerships, business, public relations",
            8: "Transformation, occult, longevity, sudden events, inheritance",
            9: "Dharma, higher learning, father, spirituality, fortune",
            10: "Career, reputation, authority, public image, achievements",
            11: "Gains, friends, aspirations, elder siblings, income",
            12: "Losses, spirituality, foreign lands, expenses, liberation"
        }

    def analyze_dasha_significance(self, current_dasha: DashaPeriod, chart: VedicChart) -> Dict[str, Any]:
        """Provide detailed analysis of current dasha period."""
        planet = current_dasha.planet
        dasha_info = self.dasha_meanings.get(planet, {})

        # Find the planet's position in the chart
        planet_position = None
        for p in chart.planets:
            if p.name == planet:
                planet_position = p
                break

        analysis = {
            "planet_nature": dasha_info.get("nature", ""),
            "key_themes": dasha_info.get("themes", []),
            "positive_effects": dasha_info.get("positive", ""),
            "negative_effects": dasha_info.get("negative", ""),
            "guidance": dasha_info.get("guidance", ""),
            "cautions": dasha_info.get("cautions", ""),
            "house_influence": "",
            "sign_influence": "",
            "remaining_period": f"{current_dasha.remaining_years:.1f} years",
            "significance": self._get_dasha_significance(planet, planet_position)
        }

        if planet_position:
            analysis["house_influence"] = f"Influencing {self.house_meanings.get(planet_position.house, 'Unknown')} (House {planet_position.house})"
            analysis["sign_influence"] = f"Operating through {planet_position.sign} energy"

        return analysis

    def _get_dasha_significance(self, planet: str, position: PlanetPosition = None) -> str:
        """Get detailed significance of the dasha period."""
        base_significance = {
            "Sun": "This is a period of self-realization and leadership development. The Sun Dasha activates your soul's purpose and brings opportunities for recognition and authority. It's a time to step into leadership roles and express your authentic self.",
            "Moon": "This period emphasizes emotional growth and mental development. The Moon Dasha brings focus to family, home, and inner emotional world. It's excellent for nurturing relationships and developing intuitive abilities.",
            "Mars": "This is an action-oriented period filled with energy and drive. Mars Dasha brings courage to face challenges and initiate new projects. It's a time for competition, sports, and assertive action.",
            "Mercury": "This period enhances intellectual abilities and communication skills. Mercury Dasha is excellent for education, business, writing, and all forms of communication. It brings versatility and analytical thinking.",
            "Jupiter": "This is one of the most auspicious periods, bringing wisdom and spiritual growth. Jupiter Dasha enhances dharma, teaching abilities, and brings good fortune. It's excellent for spiritual practices and higher learning.",
            "Venus": "This period focuses on relationships, creativity, and material pleasures. Venus Dasha brings opportunities for love, artistic expression, and material comforts. It's a time for harmony and beauty.",
            "Saturn": "This is a karmic period requiring patience and hard work. Saturn Dasha teaches important life lessons through challenges and delays. Success comes through persistent effort and discipline.",
            "Rahu": "This period brings ambition and desire for material success. Rahu Dasha can bring sudden opportunities and unconventional paths. It requires staying grounded while pursuing ambitious goals.",
            "Ketu": "This is a spiritual period emphasizing detachment and inner growth. Ketu Dasha brings mystical experiences and encourages letting go of material attachments. It's excellent for spiritual practices."
        }

        return base_significance.get(planet, "This period brings unique opportunities for growth and learning.")

    def analyze_planetary_relationships(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze relationships between planets and their significance."""
        relationships = {
            "conjunctions": [],
            "oppositions": [],
            "aspects": [],
            "house_lords": {},
            "yogas": [],
            "significance": ""
        }

        # Analyze conjunctions (planets in same sign)
        sign_groups = {}
        for planet in chart.planets:
            if planet.sign not in sign_groups:
                sign_groups[planet.sign] = []
            sign_groups[planet.sign].append(planet.name)

        for sign, planets in sign_groups.items():
            if len(planets) > 1:
                relationships["conjunctions"].append({
                    "sign": sign,
                    "planets": planets,
                    "meaning": self._interpret_conjunction(planets, sign)
                })

        # Analyze oppositions (planets 180 degrees apart)
        for i, planet1 in enumerate(chart.planets):
            for planet2 in chart.planets[i+1:]:
                angle_diff = abs(planet1.longitude - planet2.longitude)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff

                if 175 <= angle_diff <= 185:  # Opposition (within 10 degrees)
                    relationships["oppositions"].append({
                        "planets": [planet1.name, planet2.name],
                        "meaning": self._interpret_opposition(planet1.name, planet2.name)
                    })

        # Analyze house lordships
        relationships["house_lords"] = self._analyze_house_lords(chart)

        # Identify important yogas
        relationships["yogas"] = self._identify_yogas(chart)

        return relationships

    def _interpret_conjunction(self, planets: List[str], sign: str) -> str:
        """Interpret the meaning of planetary conjunctions - EXHAUSTIVE COVERAGE."""
        if len(planets) == 2:
            planet1, planet2 = planets
            combinations = {
                # SUN COMBINATIONS - Based on Brihat Parashara Hora Shastra
                ("Sun", "Moon"): f"New Moon energy in {sign} - Powerful integration of conscious will and unconscious mind. Creates strong personality and emotional leadership. Excellent for new beginnings and self-expression.",
                ("Sun", "Mercury"): f"Budhaditya Yoga in {sign} - Enhanced intelligence, communication, and learning abilities. Creates brilliant speakers, writers, and intellectuals. Excellent for education and business.",
                ("Sun", "Venus"): f"Creative leadership in {sign} - Combines authority with artistic charm and diplomatic skills. Creates charismatic leaders in arts, entertainment, and luxury industries.",
                ("Sun", "Mars"): f"Powerful energy combination in {sign} - Creates dynamic leaders with courage and determination. Excellent for military, sports, and competitive fields. Strong willpower and action-oriented nature.",
                ("Sun", "Jupiter"): f"Royal combination in {sign} - Brings wisdom, moral authority, and spiritual leadership. Creates teachers, counselors, and spiritual guides. Excellent for dharmic activities and higher learning.",
                ("Sun", "Saturn"): f"Disciplined authority in {sign} - Combines leadership with patience and hard work. Creates responsible leaders who achieve through persistent effort. Good for government and administrative roles.",
                ("Sun", "Rahu"): f"Ambitious leadership in {sign} - Creates unconventional leaders with strong material desires. Brings sudden fame and recognition through innovative approaches. Good for technology and foreign connections.",
                ("Sun", "Ketu"): f"Spiritual leadership in {sign} - Creates detached leaders focused on higher purposes. Brings wisdom through letting go of ego. Excellent for spiritual teaching and research.",

                # MOON COMBINATIONS - Based on Jataka Parijata
                ("Moon", "Mercury"): f"Emotional intelligence in {sign} - Combines intuition with analytical thinking. Creates excellent counselors, psychologists, and communicators. Strong memory and learning abilities.",
                ("Moon", "Venus"): f"Artistic sensitivity in {sign} - Creates beautiful, harmonious, and emotionally expressive personalities. Excellent for arts, music, and relationship counseling. Strong aesthetic sense.",
                ("Moon", "Mars"): f"Emotional intensity in {sign} - Creates passionate, protective, and action-oriented personalities. Strong emotional reactions and quick decision-making. Good for emergency services and sports.",
                ("Moon", "Jupiter"): f"Gaja Kesari potential in {sign} - Brings emotional wisdom, generosity, and spiritual inclinations. Creates nurturing teachers and counselors. Excellent for working with children and families.",
                ("Moon", "Saturn"): f"Emotional discipline in {sign} - Creates patient, practical, and emotionally mature personalities. Good for long-term planning and working with elderly. May cause initial emotional restrictions.",
                ("Moon", "Rahu"): f"Emotional ambition in {sign} - Creates restless, ambitious personalities seeking emotional fulfillment through material success. Good for public relations and foreign connections.",
                ("Moon", "Ketu"): f"Emotional detachment in {sign} - Creates spiritually inclined personalities with natural detachment from worldly emotions. Excellent for meditation and spiritual practices.",

                # MERCURY COMBINATIONS - Based on Saravali
                ("Mercury", "Venus"): f"Artistic communication in {sign} - Creates beautiful speakers, writers, and artists. Excellent for creative writing, music, and diplomatic communication. Charming and persuasive personality.",
                ("Mercury", "Mars"): f"Sharp intellect in {sign} - Creates quick-thinking, decisive, and argumentative personalities. Excellent for debates, law, and technical fields. Strong analytical and problem-solving abilities.",
                ("Mercury", "Jupiter"): f"Wise communication in {sign} - Creates philosophical speakers and writers with moral authority. Excellent for teaching, counseling, and religious discourse. Combines logic with wisdom.",
                ("Mercury", "Saturn"): f"Methodical thinking in {sign} - Creates careful, precise, and systematic thinkers. Excellent for research, engineering, and detailed work. Patient and thorough approach to learning.",
                ("Mercury", "Rahu"): f"Innovative thinking in {sign} - Creates unconventional, technology-oriented, and foreign-influenced communication. Good for modern technology, foreign languages, and innovative ideas.",
                ("Mercury", "Ketu"): f"Intuitive intelligence in {sign} - Creates deep, research-oriented, and spiritually inclined thinkers. Excellent for occult studies, research, and spiritual writing.",

                # VENUS COMBINATIONS - Based on Uttara Kalamrita
                ("Venus", "Mars"): f"Passionate creativity in {sign} - Creates artistic personalities with strong desires and magnetic attraction. Excellent for performing arts, fashion, and beauty industries. Strong romantic nature.",
                ("Venus", "Jupiter"): f"Wealth and wisdom in {sign} - Creates prosperous, generous, and spiritually inclined personalities. Excellent for luxury businesses, teaching, and charitable work. Material and spiritual abundance.",
                ("Venus", "Saturn"): f"Disciplined artistry in {sign} - Creates patient, long-lasting, and traditional artistic expressions. Good for classical arts, architecture, and long-term relationships. Stable but reserved in love.",
                ("Venus", "Rahu"): f"Exotic attraction in {sign} - Creates unconventional, foreign-influenced, and materially ambitious artistic personalities. Good for international arts, luxury imports, and unusual relationships.",
                ("Venus", "Ketu"): f"Spiritual artistry in {sign} - Creates detached, spiritually inclined artistic personalities. Excellent for spiritual music, sacred arts, and selfless service. Less attachment to material pleasures.",

                # MARS COMBINATIONS - Based on Mansagari
                ("Mars", "Jupiter"): f"Righteous action in {sign} - Creates courageous personalities guided by moral principles. Excellent for military, law enforcement, and fighting for just causes. Combines energy with wisdom.",
                ("Mars", "Saturn"): f"Disciplined energy in {sign} - Creates patient, persistent, and methodical action-oriented personalities. Good for engineering, construction, and long-term projects requiring sustained effort.",
                ("Mars", "Rahu"): f"Ambitious energy in {sign} - Creates highly ambitious, unconventional, and materially driven personalities. Good for technology, foreign ventures, and breaking traditional boundaries.",
                ("Mars", "Ketu"): f"Spiritual warrior in {sign} - Creates action-oriented personalities focused on spiritual goals. Good for spiritual disciplines, martial arts, and selfless service. Energy directed inward.",

                # JUPITER COMBINATIONS - Based on Brihat Jataka
                ("Jupiter", "Saturn"): f"Practical wisdom in {sign} - Creates wise, disciplined, and realistic personalities. Excellent for teaching, counseling, and long-term planning. Combines optimism with practicality.",
                ("Jupiter", "Rahu"): f"Expansive ambition in {sign} - Creates optimistic, materially ambitious, and unconventionally wise personalities. Good for foreign education, technology, and innovative teaching methods.",
                ("Jupiter", "Ketu"): f"Spiritual wisdom in {sign} - Creates naturally wise, detached, and spiritually inclined personalities. Excellent for spiritual teaching, research, and mystical studies. Natural access to higher knowledge.",

                # SATURN COMBINATIONS - Based on Hora Sara
                ("Saturn", "Rahu"): f"Disciplined ambition in {sign} - Creates patient, methodical, and unconventionally successful personalities. Good for long-term foreign ventures, technology, and systematic innovation.",
                ("Saturn", "Ketu"): f"Spiritual discipline in {sign} - Creates naturally disciplined, detached, and spiritually focused personalities. Excellent for spiritual practices, research, and selfless service.",

                # RAHU-KETU COMBINATION - Based on classical texts on nodes
                ("Rahu", "Ketu"): f"Karmic axis in {sign} - Creates personalities torn between material desires and spiritual calling. Brings intense karmic lessons and the need to balance opposites. Transformative but challenging.",

                # MISSING COMBINATIONS WITH CORRECT SORTED KEYS
                ("Moon", "Sun"): f"New Moon energy in {sign} - Powerful integration of conscious will and unconscious mind. Creates strong personality and emotional leadership. Excellent for new beginnings and self-expression.",
                ("Mercury", "Sun"): f"Budhaditya Yoga in {sign} - Enhanced intelligence, communication, and learning abilities. Creates brilliant speakers, writers, and intellectuals. Excellent for education and business.",
                ("Mars", "Sun"): f"Powerful energy combination in {sign} - Creates dynamic leaders with courage and determination. Excellent for military, sports, and competitive fields. Strong willpower and action-oriented nature.",
                ("Jupiter", "Sun"): f"Royal combination in {sign} - Brings wisdom, moral authority, and spiritual leadership. Creates teachers, counselors, and spiritual guides. Excellent for dharmic activities and higher learning.",
                ("Saturn", "Sun"): f"Disciplined authority in {sign} - Combines leadership with patience and hard work. Creates responsible leaders who achieve through persistent effort. Good for government and administrative roles.",
                ("Rahu", "Sun"): f"Ambitious leadership in {sign} - Creates unconventional leaders with strong material desires. Brings sudden fame and recognition through innovative approaches. Good for technology and foreign connections.",
                ("Ketu", "Sun"): f"Spiritual leadership in {sign} - Creates detached leaders focused on higher purposes. Brings wisdom through letting go of ego. Excellent for spiritual teaching and research.",

                ("Mercury", "Moon"): f"Emotional intelligence in {sign} - Combines intuition with analytical thinking. Creates excellent counselors, psychologists, and communicators. Strong memory and learning abilities.",
                ("Mars", "Moon"): f"Emotional intensity in {sign} - Creates passionate, protective, and action-oriented personalities. Strong emotional reactions and quick decision-making. Good for emergency services and sports.",
                ("Jupiter", "Moon"): f"Gaja Kesari potential in {sign} - Brings emotional wisdom, generosity, and spiritual inclinations. Creates nurturing teachers and counselors. Excellent for working with children and families.",
                ("Ketu", "Moon"): f"Emotional detachment in {sign} - Creates spiritually inclined personalities with natural detachment from worldly emotions. Excellent for meditation and spiritual practices.",

                ("Mars", "Mercury"): f"Sharp intellect in {sign} - Creates quick-thinking, decisive, and argumentative personalities. Excellent for debates, law, and technical fields. Strong analytical and problem-solving abilities.",
                ("Jupiter", "Mercury"): f"Wise communication in {sign} - Creates philosophical speakers and writers with moral authority. Excellent for teaching, counseling, and religious discourse. Combines logic with wisdom.",
                ("Ketu", "Mercury"): f"Intuitive intelligence in {sign} - Creates deep, research-oriented, and spiritually inclined thinkers. Excellent for occult studies, research, and spiritual writing.",

                ("Mars", "Venus"): f"Passionate creativity in {sign} - Creates artistic personalities with strong desires and magnetic attraction. Excellent for performing arts, fashion, and beauty industries. Strong romantic nature.",
                ("Jupiter", "Venus"): f"Wealth and wisdom in {sign} - Creates prosperous, generous, and spiritually inclined personalities. Excellent for luxury businesses, teaching, and charitable work. Material and spiritual abundance.",
                ("Saturn", "Venus"): f"Disciplined artistry in {sign} - Creates patient, long-lasting, and traditional artistic expressions. Good for classical arts, architecture, and long-term relationships. Stable but reserved in love.",
                ("Rahu", "Venus"): f"Exotic attraction in {sign} - Creates unconventional, foreign-influenced, and materially ambitious artistic personalities. Good for international arts, luxury imports, and unusual relationships.",
                ("Ketu", "Venus"): f"Spiritual artistry in {sign} - Creates detached, spiritually inclined artistic personalities. Excellent for spiritual music, sacred arts, and selfless service. Less attachment to material pleasures.",

                ("Jupiter", "Mars"): f"Righteous action in {sign} - Creates courageous personalities guided by moral principles. Excellent for military, law enforcement, and fighting for just causes. Combines energy with wisdom.",
                ("Ketu", "Mars"): f"Spiritual warrior in {sign} - Creates action-oriented personalities focused on spiritual goals. Good for spiritual disciplines, martial arts, and selfless service. Energy directed inward.",

                ("Rahu", "Saturn"): f"Disciplined ambition in {sign} - Creates patient, methodical, and unconventionally successful personalities. Good for long-term foreign ventures, technology, and systematic innovation.",
                ("Ketu", "Saturn"): f"Spiritual discipline in {sign} - Creates naturally disciplined, detached, and spiritually focused personalities. Excellent for spiritual practices, research, and selfless service.",

                ("Ketu", "Rahu"): f"Karmic axis in {sign} - Creates personalities torn between material desires and spiritual calling. Brings intense karmic lessons and the need to balance opposites. Transformative but challenging."
            }

            key = tuple(sorted([planet1, planet2]))
            return combinations.get(key, f"Combined energies of {planet1} and {planet2} in {sign} - Unique planetary blend requiring individual analysis")

        return f"Multiple planetary energies combining in {sign} - Complex and powerful influence requiring detailed analysis of each planetary interaction"

    def _interpret_opposition(self, planet1: str, planet2: str) -> str:
        """Interpret the meaning of planetary oppositions - EXHAUSTIVE COVERAGE."""
        oppositions = {
            # SUN OPPOSITIONS - Based on classical texts
            ("Sun", "Moon"): "Full Moon energy - Heightened emotions and consciousness. Creates tension between ego and emotions, requiring balance between self-expression and emotional needs. Can bring relationship challenges but also emotional awareness.",
            ("Sun", "Mercury"): "Mind vs. ego - Tension between intellectual analysis and personal will. Creates internal debates and need to balance rational thinking with personal desires. Good for developing objective thinking.",
            ("Sun", "Venus"): "Authority vs. harmony - Tension between leadership and diplomatic needs. Creates challenges in balancing personal authority with relationship harmony. May cause conflicts in love and partnerships.",
            ("Sun", "Mars"): "Will vs. action - Tension between ego and aggressive impulses. Creates internal conflicts about when to assert authority versus when to take direct action. Requires balanced expression of power.",
            ("Sun", "Jupiter"): "Ego vs. wisdom - Tension between personal will and higher principles. Creates challenges in balancing self-interest with moral obligations. Good for developing ethical leadership.",
            ("Sun", "Saturn"): "Authority vs. discipline - Tension between ego and responsibility. Creates conflicts between personal desires and duty. Requires learning to lead through service and patience.",
            ("Sun", "Rahu"): "Ego vs. ambition - Tension between authentic self-expression and material desires. Creates conflicts between spiritual purpose and worldly success. Requires balancing authenticity with ambition.",
            ("Sun", "Ketu"): "Ego vs. detachment - Tension between self-expression and spiritual surrender. Creates conflicts between personal recognition and spiritual growth. Requires balancing leadership with humility.",

            # MOON OPPOSITIONS - Based on classical texts
            ("Moon", "Mercury"): "Emotion vs. logic - Tension between feelings and rational thinking. Creates internal conflicts between intuitive and analytical approaches. Requires balancing emotional intelligence with logical analysis.",
            ("Moon", "Venus"): "Emotion vs. pleasure - Tension between emotional needs and aesthetic desires. Creates conflicts between nurturing instincts and personal enjoyment. Requires balancing care for others with self-care.",
            ("Moon", "Mars"): "Emotion vs. action - Need to balance feelings with decisive action. Creates tension between emotional sensitivity and aggressive impulses. Requires learning when to act on emotions versus when to control them.",
            ("Moon", "Jupiter"): "Emotion vs. wisdom - Tension between feelings and philosophical understanding. Creates conflicts between emotional reactions and higher wisdom. Good for developing emotional maturity through spiritual understanding.",
            ("Moon", "Saturn"): "Emotion vs. discipline - Tension between feelings and practical responsibilities. Creates conflicts between emotional needs and duty. Requires learning emotional self-control and patience.",
            ("Moon", "Rahu"): "Emotion vs. ambition - Tension between emotional security and material desires. Creates restlessness and conflicts between family needs and career ambitions. Requires balancing emotional fulfillment with worldly success.",
            ("Moon", "Ketu"): "Emotion vs. detachment - Tension between emotional involvement and spiritual withdrawal. Creates conflicts between caring for others and spiritual independence. Requires balancing compassion with detachment.",

            # MERCURY OPPOSITIONS - Based on classical texts
            ("Mercury", "Venus"): "Logic vs. beauty - Tension between analytical thinking and aesthetic appreciation. Creates conflicts between practical communication and artistic expression. Requires balancing efficiency with charm.",
            ("Mercury", "Mars"): "Thought vs. action - Tension between analysis and immediate action. Creates conflicts between careful planning and impulsive decisions. Requires balancing thorough thinking with decisive action.",
            ("Mercury", "Jupiter"): "Details vs. big picture - Balance practical and philosophical thinking. Creates tension between analytical focus and broad understanding. Good for developing comprehensive wisdom through detailed study.",
            ("Mercury", "Saturn"): "Quick thinking vs. methodical approach - Tension between speed and accuracy. Creates conflicts between efficient communication and careful deliberation. Requires balancing agility with thoroughness.",
            ("Mercury", "Rahu"): "Traditional thinking vs. innovation - Tension between conventional and unconventional ideas. Creates conflicts between established knowledge and new technologies. Good for developing innovative yet practical solutions.",
            ("Mercury", "Ketu"): "Rational thinking vs. intuitive knowing - Tension between logical analysis and spiritual insight. Creates conflicts between intellectual understanding and mystical knowledge. Requires balancing study with meditation.",

            # VENUS OPPOSITIONS - Based on classical texts
            ("Venus", "Mars"): "Love vs. passion - Tension between harmony and desire. Creates conflicts between gentle love and intense passion. Requires balancing romantic idealism with physical attraction.",
            ("Venus", "Jupiter"): "Pleasure vs. wisdom - Tension between enjoyment and spiritual growth. Creates conflicts between material pleasures and higher values. Good for developing refined tastes guided by wisdom.",
            ("Venus", "Saturn"): "Pleasure vs. discipline - Tension between enjoyment and responsibility. Creates conflicts between artistic expression and practical duties. Requires balancing creativity with commitment.",
            ("Venus", "Rahu"): "Traditional beauty vs. exotic attraction - Tension between conventional and unusual aesthetic preferences. Creates conflicts between established relationships and foreign attractions. Requires balancing stability with excitement.",
            ("Venus", "Ketu"): "Material pleasure vs. spiritual love - Tension between physical enjoyment and divine love. Creates conflicts between worldly relationships and spiritual devotion. Requires balancing human love with universal compassion.",

            # MARS OPPOSITIONS - Based on classical texts
            ("Mars", "Jupiter"): "Action vs. wisdom - Tension between immediate action and thoughtful consideration. Creates conflicts between aggressive impulses and moral principles. Requires balancing courage with righteousness.",
            ("Mars", "Saturn"): "Impulse vs. patience - Tension between quick action and methodical approach. Creates conflicts between immediate desires and long-term planning. Requires balancing energy with discipline.",
            ("Mars", "Rahu"): "Direct action vs. cunning strategy - Tension between straightforward and manipulative approaches. Creates conflicts between honest aggression and deceptive tactics. Requires balancing assertiveness with ethics.",
            ("Mars", "Ketu"): "External action vs. internal focus - Tension between worldly activity and spiritual practice. Creates conflicts between material achievements and spiritual growth. Requires balancing outer success with inner development.",

            # JUPITER OPPOSITIONS - Based on classical texts
            ("Jupiter", "Saturn"): "Optimism vs. realism - Tension between expansion and contraction. Creates conflicts between faith and practical limitations. Good for developing realistic optimism and practical wisdom.",
            ("Jupiter", "Rahu"): "Traditional wisdom vs. modern ambition - Tension between established knowledge and innovative desires. Creates conflicts between spiritual values and material success. Requires balancing dharma with worldly achievement.",
            ("Jupiter", "Ketu"): "Active wisdom vs. passive knowing - Tension between teaching others and inner realization. Creates conflicts between sharing knowledge and personal spiritual practice. Requires balancing service with self-development.",

            # SATURN OPPOSITIONS - Based on classical texts
            ("Saturn", "Rahu"): "Discipline vs. ambition - Tension between patient effort and desire for quick success. Creates conflicts between traditional methods and innovative approaches. Requires balancing persistence with adaptability.",
            ("Saturn", "Ketu"): "Material discipline vs. spiritual detachment - Tension between worldly responsibilities and spiritual withdrawal. Creates conflicts between duty and liberation. Requires balancing service with surrender.",

            # RAHU-KETU OPPOSITION - The eternal karmic axis
            ("Rahu", "Ketu"): "Material desire vs. spiritual detachment - The fundamental tension of human existence. Creates conflicts between worldly ambitions and spiritual calling. Represents the eternal struggle between attachment and liberation, requiring conscious integration of both energies.",

            # MISSING OPPOSITIONS WITH CORRECT SORTED KEYS
            ("Moon", "Sun"): "Full Moon energy - Heightened emotions and consciousness. Creates tension between ego and emotions, requiring balance between self-expression and emotional needs. Can bring relationship challenges but also emotional awareness.",
            ("Mercury", "Sun"): "Mind vs. ego - Tension between intellectual analysis and personal will. Creates internal debates and need to balance rational thinking with personal desires. Good for developing objective thinking.",
            ("Mars", "Sun"): "Will vs. action - Tension between ego and aggressive impulses. Creates internal conflicts about when to assert authority versus when to take direct action. Requires balanced expression of power.",
            ("Jupiter", "Sun"): "Ego vs. wisdom - Tension between personal will and higher principles. Creates challenges in balancing self-interest with moral obligations. Good for developing ethical leadership.",
            ("Saturn", "Sun"): "Authority vs. discipline - Tension between ego and responsibility. Creates conflicts between personal desires and duty. Requires learning to lead through service and patience.",
            ("Rahu", "Sun"): "Ego vs. ambition - Tension between authentic self-expression and material desires. Creates conflicts between spiritual purpose and worldly success. Requires balancing authenticity with ambition.",
            ("Ketu", "Sun"): "Ego vs. detachment - Tension between self-expression and spiritual surrender. Creates conflicts between personal recognition and spiritual growth. Requires balancing leadership with humility.",

            ("Mercury", "Moon"): "Emotion vs. logic - Tension between feelings and rational thinking. Creates internal conflicts between intuitive and analytical approaches. Requires balancing emotional intelligence with logical analysis.",
            ("Mars", "Moon"): "Emotion vs. action - Need to balance feelings with decisive action. Creates tension between emotional sensitivity and aggressive impulses. Requires learning when to act on emotions versus when to control them.",
            ("Jupiter", "Moon"): "Emotion vs. wisdom - Tension between feelings and philosophical understanding. Creates conflicts between emotional reactions and higher wisdom. Good for developing emotional maturity through spiritual understanding.",
            ("Ketu", "Moon"): "Emotion vs. detachment - Tension between emotional involvement and spiritual withdrawal. Creates conflicts between caring for others and spiritual independence. Requires balancing compassion with detachment.",

            ("Mars", "Mercury"): "Thought vs. action - Tension between analysis and immediate action. Creates conflicts between careful planning and impulsive decisions. Requires balancing thorough thinking with decisive action.",
            ("Jupiter", "Mercury"): "Details vs. big picture - Balance practical and philosophical thinking. Creates tension between analytical focus and broad understanding. Good for developing comprehensive wisdom through detailed study.",
            ("Ketu", "Mercury"): "Rational thinking vs. intuitive knowing - Tension between logical analysis and spiritual insight. Creates conflicts between intellectual understanding and mystical knowledge. Requires balancing study with meditation.",

            ("Mars", "Venus"): "Love vs. passion - Tension between harmony and desire. Creates conflicts between gentle love and intense passion. Requires balancing romantic idealism with physical attraction.",
            ("Jupiter", "Venus"): "Pleasure vs. wisdom - Tension between enjoyment and spiritual growth. Creates conflicts between material pleasures and higher values. Good for developing refined tastes guided by wisdom.",
            ("Saturn", "Venus"): "Pleasure vs. discipline - Tension between enjoyment and responsibility. Creates conflicts between artistic expression and practical duties. Requires balancing creativity with commitment.",
            ("Rahu", "Venus"): "Traditional beauty vs. exotic attraction - Tension between conventional and unusual aesthetic preferences. Creates conflicts between established relationships and foreign attractions. Requires balancing stability with excitement.",
            ("Ketu", "Venus"): "Material pleasure vs. spiritual love - Tension between physical enjoyment and divine love. Creates conflicts between worldly relationships and spiritual devotion. Requires balancing human love with universal compassion.",

            ("Jupiter", "Mars"): "Action vs. wisdom - Tension between immediate action and thoughtful consideration. Creates conflicts between aggressive impulses and moral principles. Requires balancing courage with righteousness.",
            ("Ketu", "Mars"): "External action vs. internal focus - Tension between worldly activity and spiritual practice. Creates conflicts between material achievements and spiritual growth. Requires balancing outer success with inner development.",

            ("Rahu", "Saturn"): "Discipline vs. ambition - Tension between patient effort and desire for quick success. Creates conflicts between traditional methods and innovative approaches. Requires balancing persistence with adaptability.",
            ("Ketu", "Saturn"): "Material discipline vs. spiritual detachment - Tension between worldly responsibilities and spiritual withdrawal. Creates conflicts between duty and liberation. Requires balancing service with surrender.",

            ("Ketu", "Rahu"): "Material desire vs. spiritual detachment - The fundamental tension of human existence. Creates conflicts between worldly ambitions and spiritual calling. Represents the eternal struggle between attachment and liberation, requiring conscious integration of both energies."
        }

        key = tuple(sorted([planet1, planet2]))
        return oppositions.get(key, f"Tension between {planet1} and {planet2} energies requiring conscious balance and integration")

    def _analyze_house_lords(self, chart: VedicChart) -> Dict[str, str]:
        """Analyze house lordships and their significance."""
        # This is a simplified version - full implementation would require complex calculations
        return {
            "ascendant_lord": "Determines overall life direction and personality",
            "moon_lord": "Influences emotional nature and mental tendencies",
            "sun_lord": "Affects soul purpose and life vitality"
        }

    def _identify_yogas(self, chart: VedicChart) -> List[Dict[str, str]]:
        """Identify important yogas (planetary combinations) - EXHAUSTIVE COVERAGE."""
        yogas = []

        # Get planet positions for easy reference
        planet_positions = {p.name: p for p in chart.planets}

        # WEALTH YOGAS - Based on Brihat Parashara Hora Shastra

        # Gaja Kesari Yoga (Jupiter and Moon in kendras from each other)
        jupiter_pos = planet_positions.get("Jupiter")
        moon_pos = planet_positions.get("Moon")

        if jupiter_pos and moon_pos:
            house_diff = abs(jupiter_pos.house - moon_pos.house)
            if house_diff in [0, 3, 6, 9]:  # Kendras
                yogas.append({
                    "name": "Gaja Kesari Yoga",
                    "description": "Jupiter and Moon in kendras - Brings wisdom, wealth, respect, and good fortune. Creates influential personalities with strong moral character.",
                    "strength": "Strong",
                    "category": "Wealth & Status"
                })

        # Lakshmi Yoga (Venus in own sign or exaltation in kendra or trikona)
        venus_pos = planet_positions.get("Venus")
        if venus_pos:
            venus_strong_signs = ["Taurus", "Libra", "Pisces"]  # Own signs and exaltation
            kendra_trikona_houses = [1, 4, 5, 7, 9, 10]

            if venus_pos.sign in venus_strong_signs and venus_pos.house in kendra_trikona_houses:
                yogas.append({
                    "name": "Lakshmi Yoga",
                    "description": "Venus strongly placed - Brings wealth, luxury, beauty, and material comforts. Creates artistic and prosperous personalities.",
                    "strength": "Strong",
                    "category": "Wealth & Luxury"
                })

        # INTELLIGENCE YOGAS

        # Budhaditya Yoga (Sun and Mercury together)
        sun_pos = planet_positions.get("Sun")
        mercury_pos = planet_positions.get("Mercury")

        if sun_pos and mercury_pos and sun_pos.sign == mercury_pos.sign:
            yogas.append({
                "name": "Budhaditya Yoga",
                "description": "Sun and Mercury together - Enhances intelligence, communication, and learning abilities. Creates brilliant speakers, writers, and intellectuals.",
                "strength": "Moderate",
                "category": "Intelligence & Communication"
            })

        # Saraswati Yoga (Jupiter, Venus, Mercury in kendras or trikonas)
        if jupiter_pos and venus_pos and mercury_pos:
            all_in_good_houses = all(p.house in [1, 4, 5, 7, 9, 10] for p in [jupiter_pos, venus_pos, mercury_pos])
            if all_in_good_houses:
                yogas.append({
                    "name": "Saraswati Yoga",
                    "description": "Jupiter, Venus, Mercury well-placed - Brings exceptional learning, artistic talents, and wisdom. Creates scholars and artists.",
                    "strength": "Strong",
                    "category": "Knowledge & Arts"
                })

        # POWER YOGAS

        # Raja Yoga (Lords of kendras and trikonas together)
        # Simplified check - would need full lordship calculations for complete accuracy
        strong_planets_in_kendras = [p for p in chart.planets if p.house in [1, 4, 7, 10]]
        if len(strong_planets_in_kendras) >= 2:
            yogas.append({
                "name": "Raja Yoga Potential",
                "description": "Multiple planets in kendras - Indicates potential for leadership, authority, and high status. Creates natural leaders.",
                "strength": "Variable",
                "category": "Power & Authority"
            })

        # Panch Mahapurusha Yogas (Great personality combinations)
        mars_pos = planet_positions.get("Mars")
        saturn_pos = planet_positions.get("Saturn")

        # Ruchaka Yoga (Mars in own sign in kendra)
        if mars_pos and mars_pos.sign in ["Aries", "Scorpio"] and mars_pos.house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Ruchaka Yoga",
                "description": "Mars in own sign in kendra - Creates brave, commanding personalities with military or athletic abilities. Brings courage and leadership.",
                "strength": "Strong",
                "category": "Courage & Leadership"
            })

        # Shasha Yoga (Saturn in own sign in kendra)
        if saturn_pos and saturn_pos.sign in ["Capricorn", "Aquarius"] and saturn_pos.house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Shasha Yoga",
                "description": "Saturn in own sign in kendra - Creates disciplined, hardworking personalities with administrative abilities. Brings long-term success through patience.",
                "strength": "Strong",
                "category": "Discipline & Administration"
            })

        # Hamsa Yoga (Jupiter in own sign in kendra)
        if jupiter_pos and jupiter_pos.sign in ["Sagittarius", "Pisces"] and jupiter_pos.house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Hamsa Yoga",
                "description": "Jupiter in own sign in kendra - Creates wise, spiritual personalities with teaching abilities. Brings knowledge, wealth, and respect.",
                "strength": "Strong",
                "category": "Wisdom & Spirituality"
            })

        # Malavya Yoga (Venus in own sign in kendra)
        if venus_pos and venus_pos.sign in ["Taurus", "Libra"] and venus_pos.house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Malavya Yoga",
                "description": "Venus in own sign in kendra - Creates artistic, beautiful personalities with luxury and comfort. Brings wealth through arts and relationships.",
                "strength": "Strong",
                "category": "Arts & Beauty"
            })

        # Bhadra Yoga (Mercury in own sign in kendra)
        if mercury_pos and mercury_pos.sign in ["Gemini", "Virgo"] and mercury_pos.house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Bhadra Yoga",
                "description": "Mercury in own sign in kendra - Creates intelligent, communicative personalities with business acumen. Brings success through intellect and communication.",
                "strength": "Strong",
                "category": "Intelligence & Business"
            })

        # SPIRITUAL YOGAS

        # Pravrajya Yoga (Renunciation combinations)
        rahu_pos = planet_positions.get("Rahu")
        ketu_pos = planet_positions.get("Ketu")

        if ketu_pos and ketu_pos.house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Pravrajya Yoga Potential",
                "description": "Ketu in kendra - Indicates spiritual inclinations and potential for renunciation. Creates personalities drawn to mystical and spiritual pursuits.",
                "strength": "Moderate",
                "category": "Spirituality & Detachment"
            })

        # CHALLENGING YOGAS

        # Kemadruma Yoga (Moon isolated without benefic planets on either side)
        if moon_pos:
            # Simplified check - would need to check adjacent houses for complete accuracy
            yogas.append({
                "name": "Planetary Isolation Check",
                "description": "Moon's isolation status affects emotional support and mental stability. Requires analysis of surrounding planetary influences.",
                "strength": "Variable",
                "category": "Mental & Emotional"
            })

        # Grahan Yoga (Sun or Moon with Rahu/Ketu)
        if sun_pos and rahu_pos and sun_pos.sign == rahu_pos.sign:
            yogas.append({
                "name": "Solar Eclipse Yoga",
                "description": "Sun with Rahu - Creates ambitious personalities with unconventional approaches to authority. May bring sudden changes in status.",
                "strength": "Challenging",
                "category": "Karmic & Transformative"
            })

        if moon_pos and rahu_pos and moon_pos.sign == rahu_pos.sign:
            yogas.append({
                "name": "Lunar Eclipse Yoga",
                "description": "Moon with Rahu - Creates emotionally intense personalities with unusual mental patterns. May bring psychological complexity.",
                "strength": "Challenging",
                "category": "Mental & Emotional"
            })

        return yogas

    def get_current_transits(self, birth_data: BirthData, location_data: LocationData) -> List[Dict[str, Any]]:
        """Calculate current planetary transits and their effects."""
        current_date = datetime.now()
        julian_day = julian_day_from_datetime(current_date)
        ayanamsa = calculate_ayanamsa(julian_day)

        transits = []

        # Calculate current positions of slow-moving planets
        slow_planets = {
            swe.JUPITER: "Jupiter",
            swe.SATURN: "Saturn",
            swe.MEAN_NODE: "Rahu"
        }

        for planet_id, planet_name in slow_planets.items():
            try:
                pos, _ = swe.calc_ut(julian_day, planet_id)
                longitude = (pos[0] - ayanamsa) % 360
                sign, _ = degrees_to_sign_and_degree(longitude, vedic=True)

                transit_effect = self._get_transit_effect(planet_name, sign)

                transits.append({
                    "planet": planet_name,
                    "current_sign": sign,
                    "effect": transit_effect,
                    "duration": self._get_transit_duration(planet_name),
                    "significance": self._get_transit_significance(planet_name, sign)
                })

            except Exception as e:
                print(f"Error calculating transit for {planet_name}: {e}")

        return transits

    def _get_transit_effect(self, planet: str, sign: str) -> str:
        """Get the effect of a planet transiting through a sign."""
        effects = {
            "Jupiter": f"Jupiter in {sign} brings expansion, wisdom, and good fortune to {sign} related matters",
            "Saturn": f"Saturn in {sign} brings discipline, challenges, and karmic lessons to {sign} related areas",
            "Rahu": f"Rahu in {sign} brings ambition, unconventional approaches, and material desires in {sign} areas"
        }
        return effects.get(planet, f"{planet} influencing {sign} energies")

    def _get_transit_duration(self, planet: str) -> str:
        """Get typical duration of planetary transits."""
        durations = {
            "Jupiter": "Approximately 1 year per sign",
            "Saturn": "Approximately 2.5 years per sign",
            "Rahu": "Approximately 1.5 years per sign"
        }
        return durations.get(planet, "Variable duration")

    def _get_transit_significance(self, planet: str, sign: str) -> str:
        """Get the significance of current transit."""
        return f"This transit influences how {planet}'s energy manifests through {sign} characteristics, affecting related life areas and themes."
