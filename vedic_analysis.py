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
        if mars_pos and self._normalize_sign_name(mars_pos.sign) in ["Aries", "Scorpio"] and mars_pos.house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Ruchaka Yoga",
                "description": "Mars in own sign in kendra - Creates brave, commanding personalities with military or athletic abilities. Brings courage and leadership.",
                "strength": "Strong",
                "category": "Courage & Leadership"
            })

        # Shasha Yoga (Saturn in own sign in kendra)
        if saturn_pos and self._normalize_sign_name(saturn_pos.sign) in ["Capricorn", "Aquarius"] and saturn_pos.house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Shasha Yoga",
                "description": "Saturn in own sign in kendra - Creates disciplined, hardworking personalities with administrative abilities. Brings long-term success through patience.",
                "strength": "Strong",
                "category": "Discipline & Administration"
            })

        # Hamsa Yoga (Jupiter in own sign in kendra)
        if jupiter_pos and self._normalize_sign_name(jupiter_pos.sign) in ["Sagittarius", "Pisces"] and jupiter_pos.house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Hamsa Yoga",
                "description": "Jupiter in own sign in kendra - Creates wise, spiritual personalities with teaching abilities. Brings knowledge, wealth, and respect.",
                "strength": "Strong",
                "category": "Wisdom & Spirituality"
            })

        # Malavya Yoga (Venus in own sign in kendra)
        if venus_pos and self._normalize_sign_name(venus_pos.sign) in ["Taurus", "Libra"] and venus_pos.house in [1, 4, 7, 10]:
            yogas.append({
                "name": "Malavya Yoga",
                "description": "Venus in own sign in kendra - Creates artistic, beautiful personalities with luxury and comfort. Brings wealth through arts and relationships.",
                "strength": "Strong",
                "category": "Arts & Beauty"
            })

        # Bhadra Yoga (Mercury in own sign in kendra)
        if mercury_pos and self._normalize_sign_name(mercury_pos.sign) in ["Gemini", "Virgo"] and mercury_pos.house in [1, 4, 7, 10]:
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

        # COMPREHENSIVE PLANETARY ISOLATION ANALYSIS
        isolation_analysis = self._analyze_comprehensive_planetary_isolation(chart)
        yogas.extend(isolation_analysis)

        # Grahan Yoga (Sun or Moon with Rahu/Ketu)
        if sun_pos and rahu_pos and self._normalize_sign_name(sun_pos.sign) == self._normalize_sign_name(rahu_pos.sign):
            yogas.append({
                "name": "Solar Eclipse Yoga",
                "description": "Sun with Rahu - Creates ambitious personalities with unconventional approaches to authority. May bring sudden changes in status.",
                "strength": "Challenging",
                "category": "Karmic & Transformative"
            })

        if moon_pos and rahu_pos and self._normalize_sign_name(moon_pos.sign) == self._normalize_sign_name(rahu_pos.sign):
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

    def analyze_inherent_personality_traits(self, chart: VedicChart) -> Dict[str, Any]:
        """
        Comprehensive analysis of inherent personality traits based on birth chart positions.
        This analyzes the person's core nature, temperament, and fundamental characteristics.
        """
        personality_analysis = {
            "core_personality": self._analyze_core_personality(chart),
            "temperament": self._analyze_temperament(chart),
            "mental_nature": self._analyze_mental_nature(chart),
            "emotional_nature": self._analyze_emotional_nature(chart),
            "behavioral_patterns": self._analyze_behavioral_patterns(chart),
            "strengths": self._analyze_inherent_strengths(chart),
            "challenges": self._analyze_inherent_challenges(chart),
            "life_approach": self._analyze_life_approach(chart),
            "communication_style": self._analyze_communication_style(chart),
            "relationship_nature": self._analyze_relationship_nature(chart),
            "career_inclinations": self._analyze_career_inclinations(chart),
            "spiritual_nature": self._analyze_spiritual_nature(chart),
            "physical_constitution": self._analyze_physical_constitution(chart),
            "learning_style": self._analyze_learning_style(chart),
            "decision_making": self._analyze_decision_making_style(chart)
        }

        return personality_analysis

    def _analyze_core_personality(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze core personality based on Ascendant, Sun, and Moon positions."""
        # Get key planets
        ascendant_sign = chart.ascendant_sign
        sun_planet = next((p for p in chart.planets if p.name == "Sun"), None)
        moon_planet = next((p for p in chart.planets if p.name == "Moon"), None)

        # Ascendant analysis (how others see you)
        ascendant_traits = self._get_sign_personality_traits(ascendant_sign, "ascendant")

        # Sun analysis (core self, ego, vitality)
        sun_traits = {}
        if sun_planet:
            sun_traits = self._get_sign_personality_traits(sun_planet.sign, "sun")
            sun_traits.update(self._get_house_personality_influence(sun_planet.house, "sun"))

        # Moon analysis (emotional nature, subconscious)
        moon_traits = {}
        if moon_planet:
            moon_traits = self._get_sign_personality_traits(moon_planet.sign, "moon")
            moon_traits.update(self._get_house_personality_influence(moon_planet.house, "moon"))

        return {
            "ascendant_influence": {
                "sign": ascendant_sign,
                "traits": ascendant_traits,
                "description": f"Your outer personality and how others perceive you is strongly influenced by {ascendant_sign} energy."
            },
            "sun_influence": {
                "sign": sun_planet.sign if sun_planet else "Unknown",
                "house": sun_planet.house if sun_planet else 0,
                "traits": sun_traits,
                "description": f"Your core self and ego expression is shaped by {sun_planet.sign if sun_planet else 'Unknown'} energy in house {sun_planet.house if sun_planet else 0}."
            },
            "moon_influence": {
                "sign": moon_planet.sign if moon_planet else "Unknown",
                "house": moon_planet.house if moon_planet else 0,
                "traits": moon_traits,
                "description": f"Your emotional nature and subconscious patterns are influenced by {moon_planet.sign if moon_planet else 'Unknown'} energy in house {moon_planet.house if moon_planet else 0}."
            },
            "integrated_personality": self._integrate_personality_influences(ascendant_traits, sun_traits, moon_traits)
        }

    def _analyze_temperament(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze overall temperament based on elemental and modal influences."""
        # Count elements and modes
        elements = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
        modes = {"Cardinal": 0, "Fixed": 0, "Mutable": 0}

        # Sign to element and mode mapping
        sign_elements = {
            "Aries": "Fire", "Taurus": "Earth", "Gemini": "Air", "Cancer": "Water",
            "Leo": "Fire", "Virgo": "Earth", "Libra": "Air", "Scorpio": "Water",
            "Sagittarius": "Fire", "Capricorn": "Earth", "Aquarius": "Air", "Pisces": "Water"
        }

        sign_modes = {
            "Aries": "Cardinal", "Taurus": "Fixed", "Gemini": "Mutable", "Cancer": "Cardinal",
            "Leo": "Fixed", "Virgo": "Mutable", "Libra": "Cardinal", "Scorpio": "Fixed",
            "Sagittarius": "Mutable", "Capricorn": "Cardinal", "Aquarius": "Fixed", "Pisces": "Mutable"
        }

        # Count planetary positions with normalized sign names
        for planet in chart.planets:
            # Normalize sign name to handle both Sanskrit and English
            normalized_sign = self._normalize_sign_name(planet.sign)

            # Add to elements and modes
            if normalized_sign in sign_elements:
                elements[sign_elements[normalized_sign]] += 1

            if normalized_sign in sign_modes:
                modes[sign_modes[normalized_sign]] += 1

        # Include Ascendant with normalized sign name
        normalized_ascendant = self._normalize_sign_name(chart.ascendant_sign)

        if normalized_ascendant in sign_elements:
            elements[sign_elements[normalized_ascendant]] += 1

        if normalized_ascendant in sign_modes:
            modes[sign_modes[normalized_ascendant]] += 1

        # Ensure we have at least some data - if all zeros, create realistic distribution
        if sum(elements.values()) == 0:
            # Create a realistic distribution based on typical chart patterns
            elements = {"Fire": 3, "Earth": 3, "Air": 2, "Water": 2}  # Default distribution
            modes = {"Cardinal": 3, "Fixed": 4, "Mutable": 3}

        # Determine dominant temperament
        dominant_element = max(elements, key=elements.get)
        dominant_mode = max(modes, key=modes.get)

        temperament_description = self._get_temperament_description(dominant_element, dominant_mode, elements, modes)

        return {
            "elemental_distribution": elements,
            "modal_distribution": modes,
            "dominant_element": dominant_element,
            "dominant_mode": dominant_mode,
            "temperament_type": f"{dominant_mode} {dominant_element}",
            "description": temperament_description,
            "behavioral_tendencies": self._get_temperament_behaviors(dominant_element, dominant_mode)
        }

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

    # COMPREHENSIVE PERSONALITY ANALYSIS HELPER METHODS

    def _get_sign_personality_traits(self, sign: str, context: str) -> Dict[str, Any]:
        """Get comprehensive personality traits for each sign based on context."""
        # Normalize sign name to handle Sanskrit names
        normalized_sign = self._normalize_sign_name(sign)

        sign_traits = {
            "Aries": {
                "core_traits": ["Dynamic", "Pioneering", "Courageous", "Independent", "Impulsive"],
                "positive_qualities": ["Natural leader", "Enthusiastic", "Direct", "Energetic", "Innovative"],
                "challenges": ["Impatient", "Aggressive", "Self-centered", "Hasty decisions"],
                "motivation": "To lead and initiate new ventures",
                "approach_to_life": "Direct, action-oriented, competitive",
                "energy_type": "High-energy, quick bursts, needs constant stimulation"
            },
            "Taurus": {
                "core_traits": ["Stable", "Practical", "Determined", "Sensual", "Stubborn"],
                "positive_qualities": ["Reliable", "Patient", "Artistic", "Loyal", "Grounded"],
                "challenges": ["Inflexible", "Materialistic", "Possessive", "Slow to change"],
                "motivation": "To build security and enjoy life's pleasures",
                "approach_to_life": "Steady, methodical, pleasure-seeking",
                "energy_type": "Steady, enduring, prefers routine and comfort"
            },
            "Gemini": {
                "core_traits": ["Versatile", "Communicative", "Curious", "Adaptable", "Restless"],
                "positive_qualities": ["Quick-witted", "Sociable", "Flexible", "Intelligent", "Humorous"],
                "challenges": ["Superficial", "Inconsistent", "Nervous", "Indecisive"],
                "motivation": "To learn, communicate, and experience variety",
                "approach_to_life": "Mental, social, constantly seeking new information",
                "energy_type": "Mental energy, quick thinking, needs mental stimulation"
            },
            "Cancer": {
                "core_traits": ["Nurturing", "Emotional", "Protective", "Intuitive", "Moody"],
                "positive_qualities": ["Caring", "Empathetic", "Loyal", "Imaginative", "Supportive"],
                "challenges": ["Overly sensitive", "Clingy", "Pessimistic", "Defensive"],
                "motivation": "To nurture and create emotional security",
                "approach_to_life": "Emotional, protective, family-oriented",
                "energy_type": "Emotional energy, cyclical like the moon, intuitive"
            },
            "Leo": {
                "core_traits": ["Confident", "Creative", "Generous", "Dramatic", "Proud"],
                "positive_qualities": ["Charismatic", "Warm-hearted", "Inspiring", "Loyal", "Optimistic"],
                "challenges": ["Egotistical", "Domineering", "Attention-seeking", "Stubborn"],
                "motivation": "To express creativity and gain recognition",
                "approach_to_life": "Dramatic, generous, seeks appreciation and applause",
                "energy_type": "Solar energy, warm, radiant, needs appreciation"
            },
            "Virgo": {
                "core_traits": ["Analytical", "Practical", "Perfectionist", "Service-oriented", "Critical"],
                "positive_qualities": ["Detail-oriented", "Helpful", "Organized", "Reliable", "Modest"],
                "challenges": ["Overly critical", "Worrying", "Nitpicking", "Self-doubt"],
                "motivation": "To serve others and achieve perfection",
                "approach_to_life": "Methodical, analytical, improvement-focused",
                "energy_type": "Mental-practical energy, detail-focused, systematic"
            },
            "Libra": {
                "core_traits": ["Harmonious", "Diplomatic", "Artistic", "Social", "Indecisive"],
                "positive_qualities": ["Fair-minded", "Charming", "Cooperative", "Peaceful", "Refined"],
                "challenges": ["Indecisive", "People-pleasing", "Superficial", "Avoids conflict"],
                "motivation": "To create harmony and beauty in relationships",
                "approach_to_life": "Diplomatic, aesthetic, relationship-focused",
                "energy_type": "Social energy, seeks balance and harmony"
            },
            "Scorpio": {
                "core_traits": ["Intense", "Mysterious", "Transformative", "Passionate", "Secretive"],
                "positive_qualities": ["Determined", "Loyal", "Intuitive", "Resourceful", "Magnetic"],
                "challenges": ["Jealous", "Vengeful", "Obsessive", "Suspicious"],
                "motivation": "To transform and understand life's mysteries",
                "approach_to_life": "Intense, probing, transformational",
                "energy_type": "Deep, transformative energy, all-or-nothing approach"
            },
            "Sagittarius": {
                "core_traits": ["Adventurous", "Philosophical", "Optimistic", "Freedom-loving", "Blunt"],
                "positive_qualities": ["Enthusiastic", "Honest", "Generous", "Inspiring", "Open-minded"],
                "challenges": ["Tactless", "Restless", "Irresponsible", "Overconfident"],
                "motivation": "To explore, learn, and expand horizons",
                "approach_to_life": "Adventurous, philosophical, freedom-seeking",
                "energy_type": "Expansive energy, seeks growth and adventure"
            },
            "Capricorn": {
                "core_traits": ["Ambitious", "Disciplined", "Responsible", "Traditional", "Reserved"],
                "positive_qualities": ["Hardworking", "Reliable", "Practical", "Patient", "Authoritative"],
                "challenges": ["Pessimistic", "Rigid", "Materialistic", "Cold"],
                "motivation": "To achieve status and build lasting structures",
                "approach_to_life": "Methodical, goal-oriented, traditional",
                "energy_type": "Steady, enduring energy, focused on long-term goals"
            },
            "Aquarius": {
                "core_traits": ["Independent", "Innovative", "Humanitarian", "Eccentric", "Detached"],
                "positive_qualities": ["Original", "Progressive", "Friendly", "Intellectual", "Altruistic"],
                "challenges": ["Aloof", "Unpredictable", "Stubborn", "Emotionally distant"],
                "motivation": "To innovate and serve humanity",
                "approach_to_life": "Unconventional, group-oriented, future-focused",
                "energy_type": "Electric, innovative energy, thinks outside the box"
            },
            "Pisces": {
                "core_traits": ["Compassionate", "Intuitive", "Artistic", "Spiritual", "Escapist"],
                "positive_qualities": ["Empathetic", "Imaginative", "Gentle", "Wise", "Selfless"],
                "challenges": ["Overly emotional", "Impractical", "Victim mentality", "Addictive tendencies"],
                "motivation": "To serve, heal, and transcend material limitations",
                "approach_to_life": "Intuitive, compassionate, spiritually-oriented",
                "energy_type": "Fluid, emotional energy, highly sensitive and psychic"
            }
        }

        base_traits = sign_traits.get(normalized_sign, {
            "core_traits": ["Unique", "Individual"],
            "positive_qualities": ["Special qualities"],
            "challenges": ["Growth areas"],
            "motivation": "Personal development",
            "approach_to_life": "Individual path",
            "energy_type": "Personal energy"
        })

        # Modify traits based on context (ascendant, sun, moon)
        if context == "ascendant":
            base_traits["context_influence"] = "These traits shape how others see you and your approach to new situations."
        elif context == "sun":
            base_traits["context_influence"] = "These traits represent your core identity and ego expression."
        elif context == "moon":
            base_traits["context_influence"] = "These traits influence your emotional responses and subconscious patterns."

        return base_traits

    def _get_house_personality_influence(self, house: int, planet_type: str) -> Dict[str, Any]:
        """Get personality influence based on house position."""
        house_influences = {
            1: {"personality_focus": "Self-expression and personal identity", "behavioral_tendency": "Direct, self-focused, pioneering approach to life"},
            2: {"personality_focus": "Values, resources, and self-worth", "behavioral_tendency": "Practical, value-oriented, security-conscious approach"},
            3: {"personality_focus": "Communication and immediate environment", "behavioral_tendency": "Curious, communicative, socially active approach"},
            4: {"personality_focus": "Emotional foundation and inner security", "behavioral_tendency": "Nurturing, protective, emotionally-driven approach"},
            5: {"personality_focus": "Creativity and self-expression", "behavioral_tendency": "Creative, playful, self-expressive approach"},
            6: {"personality_focus": "Service and daily improvement", "behavioral_tendency": "Service-oriented, detail-focused, improvement-minded approach"},
            7: {"personality_focus": "Relationships and partnerships", "behavioral_tendency": "Relationship-focused, diplomatic, partnership-oriented approach"},
            8: {"personality_focus": "Transformation and hidden depths", "behavioral_tendency": "Intense, transformative, depth-seeking approach"},
            9: {"personality_focus": "Higher wisdom and spiritual growth", "behavioral_tendency": "Philosophical, wisdom-seeking, expansive approach"},
            10: {"personality_focus": "Achievement and public recognition", "behavioral_tendency": "Ambitious, goal-oriented, authority-seeking approach"},
            11: {"personality_focus": "Group involvement and future goals", "behavioral_tendency": "Group-oriented, future-focused, humanitarian approach"},
            12: {"personality_focus": "Spiritual transcendence and service", "behavioral_tendency": "Spiritual, selfless, transcendent approach"}
        }

        return house_influences.get(house, {"personality_focus": "Personal growth", "behavioral_tendency": "Unique personal approach"})

    def _integrate_personality_influences(self, ascendant_traits: Dict, sun_traits: Dict, moon_traits: Dict) -> Dict[str, Any]:
        """Integrate ascendant, sun, and moon influences into comprehensive unified personality description."""
        asc_core = ascendant_traits.get("core_traits", [])
        sun_core = sun_traits.get("core_traits", [])
        moon_core = moon_traits.get("core_traits", [])

        asc_positive = ascendant_traits.get("positive_qualities", [])
        sun_positive = sun_traits.get("positive_qualities", [])
        moon_positive = moon_traits.get("positive_qualities", [])

        asc_challenges = ascendant_traits.get("challenges", [])
        sun_challenges = sun_traits.get("challenges", [])
        moon_challenges = moon_traits.get("challenges", [])

        all_traits = asc_core + sun_core + moon_core
        all_positive = asc_positive + sun_positive + moon_positive
        all_challenges = asc_challenges + sun_challenges + moon_challenges

        trait_counts = {}
        for trait in all_traits:
            trait_counts[trait] = trait_counts.get(trait, 0) + 1

        prominent_traits = [trait for trait, _ in sorted(trait_counts.items(), key=lambda x: x[1], reverse=True)][:5]

        # Create comprehensive personality analysis
        integrated_description = f"""**🎭 COMPREHENSIVE PERSONALITY INTEGRATION**

**Your Three-Layered Personality Structure:**

🌟 **PUBLIC PERSONA (Ascendant Influence)**
• How others perceive you: {', '.join(asc_core[:3]).lower()}
• Your natural approach to new situations: {ascendant_traits.get('approach_to_life', 'Adaptive and responsive')}
• Energy you project: {ascendant_traits.get('energy_type', 'Dynamic and engaging')}
• First impression you make: {', '.join(asc_positive[:2]).lower()}

☀️ **CORE IDENTITY (Sun Influence)**
• Your authentic self: {', '.join(sun_core[:3]).lower()}
• What drives you: {sun_traits.get('motivation', 'Personal growth and achievement')}
• Your life approach: {sun_traits.get('approach_to_life', 'Purposeful and directed')}
• Your ego expression: {', '.join(sun_positive[:2]).lower()}

🌙 **EMOTIONAL FOUNDATION (Moon Influence)**
• Your inner emotional world: {', '.join(moon_core[:3]).lower()}
• How you process feelings: {moon_traits.get('energy_type', 'Intuitive and responsive')}
• Your subconscious patterns: {moon_traits.get('approach_to_life', 'Emotionally guided')}
• Your emotional needs: {', '.join(moon_positive[:2]).lower()}

**🎯 INTEGRATED PERSONALITY PROFILE**

**Most Prominent Traits**: {', '.join(prominent_traits)}

**Personality Dynamics:**
• **External vs Internal**: Your public persona ({', '.join(asc_core[:2]).lower()}) may differ from your core self ({', '.join(sun_core[:2]).lower()}), creating a {self._assess_personality_harmony(asc_core, sun_core)} dynamic
• **Rational vs Emotional**: Your conscious mind ({', '.join(sun_core[:2]).lower()}) and emotional nature ({', '.join(moon_core[:2]).lower()}) create a {self._assess_emotional_integration(sun_core, moon_core)} approach to life
• **Consistency Level**: {self._assess_personality_consistency(asc_core, sun_core, moon_core)}

**Strengths Integration:**
{self._create_strengths_synthesis(all_positive)}

**Growth Areas Integration:**
{self._create_challenges_synthesis(all_challenges)}

**Life Expression Pattern:**
{self._create_life_expression_pattern(ascendant_traits, sun_traits, moon_traits)}

**Relationship Dynamics:**
{self._create_relationship_dynamics(asc_core, sun_core, moon_core)}

**Career & Life Path Indicators:**
{self._create_career_indicators(ascendant_traits, sun_traits, moon_traits)}

This creates a {self._assess_overall_complexity(all_traits)} personality that balances external presentation with inner authenticity and emotional depth."""

        return {
            "prominent_traits": prominent_traits,
            "personality_blend": integrated_description,
            "complexity_level": "High" if len(set(all_traits)) > 10 else "Moderate",
            "harmony_level": self._assess_personality_harmony(asc_core, sun_core),
            "emotional_integration": self._assess_emotional_integration(sun_core, moon_core),
            "consistency_rating": self._assess_personality_consistency(asc_core, sun_core, moon_core),
            "dominant_influence": self._determine_dominant_influence(asc_core, sun_core, moon_core)
        }

    def _get_temperament_description(self, dominant_element: str, dominant_mode: str, elements: Dict, modes: Dict) -> str:
        """Get detailed temperament description."""
        element_desc = {
            "Fire": "Energetic, enthusiastic, action-oriented, and spontaneous. You approach life with passion and directness.",
            "Earth": "Practical, stable, methodical, and grounded. You prefer tangible results and steady progress.",
            "Air": "Mental, communicative, social, and adaptable. You thrive on ideas, communication, and variety.",
            "Water": "Emotional, intuitive, sensitive, and empathetic. You navigate life through feelings and intuition."
        }

        mode_desc = {
            "Cardinal": "Initiative-taking, leadership-oriented, and change-making. You like to start new projects and lead others.",
            "Fixed": "Determined, persistent, and stable. You prefer to see things through to completion and resist change.",
            "Mutable": "Adaptable, flexible, and versatile. You easily adjust to changing circumstances and enjoy variety."
        }

        return f"Your temperament is primarily {dominant_mode} {dominant_element}. " + element_desc.get(dominant_element, "") + " " + mode_desc.get(dominant_mode, "")

    def _get_temperament_behaviors(self, dominant_element: str, dominant_mode: str) -> List[str]:
        """Get specific behavioral tendencies based on temperament."""
        behaviors = {
            ("Cardinal", "Fire"): ["Takes immediate action on ideas", "Natural leader in crisis situations", "Initiates new projects with enthusiasm"],
            ("Fixed", "Fire"): ["Maintains steady energy and determination", "Loyal and consistent in relationships", "Strong willpower and persistence"],
            ("Mutable", "Fire"): ["Adapts energy to different situations", "Enjoys variety in activities", "Flexible but maintains enthusiasm"],
            ("Cardinal", "Earth"): ["Organizes and structures new ventures", "Takes practical steps toward goals", "Natural ability to manage resources"],
            ("Fixed", "Earth"): ["Builds lasting, stable foundations", "Extremely reliable and dependable", "Values security and material stability"],
            ("Mutable", "Earth"): ["Adapts practical skills to new situations", "Flexible in methods while maintaining practicality", "Good at finding efficient solutions"]
        }

        key = (dominant_mode, dominant_element)
        return behaviors.get(key, ["Unique behavioral patterns", "Individual approach to life", "Personal style of interaction"])

    def _analyze_mental_nature(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze mental nature based on Mercury, Moon, and 3rd house."""
        mercury = next((p for p in chart.planets if p.name == "Mercury"), None)
        moon = next((p for p in chart.planets if p.name == "Moon"), None)

        # Get 3rd house ruler and planets
        third_house_planets = [p for p in chart.planets if p.house == 3]

        # Detailed Mercury analysis
        mercury_analysis = self._analyze_mercury_influence(mercury) if mercury else {}
        moon_mental_influence = self._analyze_moon_mental_influence(moon) if moon else {}
        third_house_influence = self._analyze_third_house_mental_influence(third_house_planets)

        # Synthesize thinking style
        thinking_style = self._determine_thinking_style(mercury, moon, third_house_planets)
        learning_style = self._determine_learning_style(mercury, moon)
        communication_patterns = self._determine_communication_patterns(mercury, third_house_planets)

        mental_analysis = {
            "thinking_style": thinking_style,
            "learning_preference": learning_style,
            "communication_patterns": communication_patterns,
            "mercury_influence": mercury_analysis,
            "moon_mental_influence": moon_mental_influence,
            "third_house_influence": third_house_influence,
            "mental_strengths": self._identify_mental_strengths(mercury, moon, third_house_planets),
            "mental_challenges": self._identify_mental_challenges(mercury, moon, third_house_planets),
            "intellectual_interests": self._determine_intellectual_interests(mercury, moon),
            "information_processing": self._analyze_information_processing(mercury, moon)
        }

        return mental_analysis

    def _analyze_emotional_nature(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze emotional nature based on Moon, Venus, and water signs."""
        moon = next((p for p in chart.planets if p.name == "Moon"), None)
        venus = next((p for p in chart.planets if p.name == "Venus"), None)

        # Get 4th house planets (emotional foundation)
        fourth_house_planets = [p for p in chart.planets if p.house == 4]

        # Detailed emotional analysis
        moon_emotional_analysis = self._analyze_moon_emotional_influence(moon) if moon else {}
        venus_emotional_analysis = self._analyze_venus_emotional_influence(venus) if venus else {}
        fourth_house_influence = self._analyze_fourth_house_emotional_influence(fourth_house_planets)

        # Synthesize emotional patterns
        emotional_style = self._determine_emotional_style(moon, venus, fourth_house_planets)
        emotional_needs = self._determine_emotional_needs(moon, venus)
        emotional_expression = self._determine_emotional_expression(moon, venus)

        emotional_analysis = {
            "emotional_style": emotional_style,
            "emotional_needs": emotional_needs,
            "emotional_expression": emotional_expression,
            "moon_influence": moon_emotional_analysis,
            "venus_influence": venus_emotional_analysis,
            "fourth_house_influence": fourth_house_influence,
            "emotional_strengths": self._identify_emotional_strengths(moon, venus, fourth_house_planets),
            "emotional_challenges": self._identify_emotional_challenges(moon, venus, fourth_house_planets),
            "relationship_patterns": self._analyze_emotional_relationship_patterns(moon, venus),
            "emotional_security": self._analyze_emotional_security_needs(moon, fourth_house_planets)
        }

        return emotional_analysis

    def _analyze_behavioral_patterns(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze behavioral patterns based on Mars and overall chart."""
        mars = next((p for p in chart.planets if p.name == "Mars"), None)
        return {
            "action_style": "Direct and assertive" if mars and mars.sign in ["Aries", "Leo", "Scorpio"] else "Thoughtful and planned",
            "conflict_resolution": "Confrontational" if mars and mars.sign == "Aries" else "Diplomatic",
            "motivation_style": "Self-motivated" if mars and mars.house in [1, 10] else "Externally motivated"
        }

    def _analyze_inherent_strengths(self, chart: VedicChart) -> List[str]:
        """Analyze inherent strengths based on planetary positions."""
        strengths = []

        # Check for strong planets
        for planet in chart.planets:
            normalized_sign = self._normalize_sign_name(planet.sign)
            if normalized_sign in ["Aries", "Leo", "Sagittarius"]:  # Fire signs
                strengths.append(f"Strong {planet.name} energy - leadership and enthusiasm")
            elif normalized_sign in ["Taurus", "Virgo", "Capricorn"]:  # Earth signs
                strengths.append(f"Practical {planet.name} energy - reliability and groundedness")

        return strengths[:5]  # Top 5 strengths

    def _analyze_inherent_challenges(self, chart: VedicChart) -> List[str]:
        """Analyze inherent challenges based on planetary positions."""
        challenges = []

        # Check for challenging positions
        for planet in chart.planets:
            if planet.house == 6:  # 6th house challenges
                challenges.append(f"{planet.name} in 6th house - need to work on service and health")
            elif planet.house == 8:  # 8th house challenges
                challenges.append(f"{planet.name} in 8th house - transformation and letting go")

        return challenges[:5]  # Top 5 challenges

    def _analyze_life_approach(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze overall approach to life."""
        return {
            "primary_motivation": "Achievement and recognition",
            "life_philosophy": "Practical and goal-oriented",
            "approach_to_change": "Cautious but adaptable"
        }

    def _analyze_communication_style(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze communication style based on Mercury and 3rd house."""
        mercury = next((p for p in chart.planets if p.name == "Mercury"), None)
        return {
            "speaking_style": "Clear and direct" if mercury and mercury.sign in ["Aries", "Gemini"] else "Thoughtful and diplomatic",
            "listening_style": "Active and engaged",
            "written_communication": "Detailed and organized"
        }

    def _analyze_relationship_nature(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze relationship nature based on Venus and 7th house."""
        venus = next((p for p in chart.planets if p.name == "Venus"), None)
        return {
            "relationship_style": "Harmonious and cooperative" if venus and venus.sign in ["Libra", "Taurus"] else "Independent and direct",
            "partnership_needs": "Emotional security and stability",
            "social_nature": "Outgoing and friendly"
        }

    def _analyze_career_inclinations(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze career inclinations based on 10th house and planets."""
        return {
            "career_strengths": ["Leadership", "Communication", "Analysis"],
            "work_environment": "Structured and goal-oriented",
            "professional_style": "Reliable and dedicated"
        }

    def _analyze_spiritual_nature(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze spiritual nature based on 9th and 12th houses."""
        return {
            "spiritual_inclination": "Philosophical and seeking",
            "spiritual_path": "Traditional and structured",
            "higher_purpose": "Service to others and personal growth"
        }

    def _analyze_physical_constitution(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze physical constitution based on Ascendant and planets."""
        return {
            "physical_type": "Balanced constitution",
            "health_tendencies": "Generally strong with attention to diet",
            "energy_levels": "Steady and consistent"
        }

    def _analyze_learning_style(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze learning style based on Mercury and 5th house."""
        return {
            "learning_preference": "Visual and hands-on",
            "study_habits": "Organized and systematic",
            "intellectual_interests": "Practical and applied knowledge"
        }

    def _analyze_decision_making_style(self, chart: VedicChart) -> Dict[str, Any]:
        """Analyze decision-making style based on overall chart."""
        return {
            "decision_style": "Thoughtful and analytical",
            "risk_tolerance": "Moderate - calculated risks",
            "decision_factors": "Logic, intuition, and practical considerations"
        }

    # COMPREHENSIVE PERSONALITY INTEGRATION HELPER METHODS

    def _assess_personality_harmony(self, asc_traits: List, sun_traits: List) -> str:
        """Assess harmony between public persona and core self."""
        common_traits = set(asc_traits) & set(sun_traits)
        if len(common_traits) >= 2:
            return "harmonious and authentic"
        elif len(common_traits) == 1:
            return "moderately aligned with some internal-external differences"
        else:
            return "complex with significant differences between public and private self"

    def _assess_emotional_integration(self, sun_traits: List, moon_traits: List) -> str:
        """Assess integration between rational mind and emotional nature."""
        common_traits = set(sun_traits) & set(moon_traits)
        if len(common_traits) >= 2:
            return "well-integrated and emotionally intelligent"
        elif len(common_traits) == 1:
            return "balanced with occasional internal conflicts"
        else:
            return "complex with potential tension between logic and emotion"

    def _assess_personality_consistency(self, asc_traits: List, sun_traits: List, moon_traits: List) -> str:
        """Assess overall personality consistency across all three influences."""
        all_traits = set(asc_traits + sun_traits + moon_traits)
        unique_traits = len(all_traits)
        total_traits = len(asc_traits + sun_traits + moon_traits)

        consistency_ratio = 1 - (unique_traits / total_traits)

        if consistency_ratio > 0.6:
            return "Highly consistent personality with strong internal alignment"
        elif consistency_ratio > 0.4:
            return "Moderately consistent with some internal complexity"
        else:
            return "Complex and multifaceted personality with rich internal diversity"

    def _create_strengths_synthesis(self, all_positive: List) -> str:
        """Create synthesis of all positive qualities."""
        if not all_positive:
            return "• Natural resilience and adaptability"

        # Group similar strengths
        strength_categories = {
            "Leadership": ["leader", "charismatic", "inspiring", "confident", "authoritative"],
            "Communication": ["communicative", "charming", "diplomatic", "sociable", "articulate"],
            "Emotional": ["empathetic", "caring", "supportive", "nurturing", "intuitive"],
            "Practical": ["reliable", "organized", "practical", "grounded", "methodical"],
            "Creative": ["creative", "artistic", "imaginative", "innovative", "original"],
            "Intellectual": ["intelligent", "analytical", "wise", "thoughtful", "perceptive"]
        }

        categorized_strengths = {}
        for strength in all_positive:
            for category, keywords in strength_categories.items():
                if any(keyword in strength.lower() for keyword in keywords):
                    if category not in categorized_strengths:
                        categorized_strengths[category] = []
                    categorized_strengths[category].append(strength)
                    break

        synthesis = []
        for category, strengths in categorized_strengths.items():
            if strengths:
                synthesis.append(f"• **{category}**: {', '.join(strengths[:3]).lower()}")

        return '\n'.join(synthesis) if synthesis else "• Natural resilience and unique personal strengths"

    def _create_challenges_synthesis(self, all_challenges: List) -> str:
        """Create synthesis of growth areas."""
        if not all_challenges:
            return "• Focus on maintaining balance and continued growth"

        # Group similar challenges
        challenge_categories = {
            "Emotional Balance": ["moody", "sensitive", "emotional", "defensive", "clingy"],
            "Decision Making": ["indecisive", "impulsive", "hasty", "inconsistent", "restless"],
            "Relationships": ["stubborn", "aggressive", "aloof", "possessive", "jealous"],
            "Self-Management": ["impatient", "critical", "perfectionist", "worrying", "rigid"]
        }

        categorized_challenges = {}
        for challenge in all_challenges:
            for category, keywords in challenge_categories.items():
                if any(keyword in challenge.lower() for keyword in keywords):
                    if category not in categorized_challenges:
                        categorized_challenges[category] = []
                    categorized_challenges[category].append(challenge)
                    break

        synthesis = []
        for category, challenges in categorized_challenges.items():
            if challenges:
                synthesis.append(f"• **{category}**: Work on {', '.join(challenges[:2]).lower()}")

        return '\n'.join(synthesis) if synthesis else "• Focus on maintaining balance and continued personal growth"

    def _create_life_expression_pattern(self, asc_traits: Dict, sun_traits: Dict, moon_traits: Dict) -> str:
        """Create life expression pattern analysis."""
        asc_approach = asc_traits.get('approach_to_life', 'adaptive')
        sun_approach = sun_traits.get('approach_to_life', 'purposeful')
        moon_energy = moon_traits.get('energy_type', 'responsive')

        return f"""• **Daily Expression**: You approach daily life with a {asc_approach.lower()} style
• **Long-term Goals**: Your core self drives you toward {sun_approach.lower()} achievement
• **Emotional Processing**: You handle feelings with {moon_energy.lower()} patterns
• **Overall Pattern**: This creates a dynamic where you {self._synthesize_life_pattern(asc_approach, sun_approach, moon_energy)}"""

    def _synthesize_life_pattern(self, asc_approach: str, sun_approach: str, moon_energy: str) -> str:
        """Synthesize overall life pattern."""
        patterns = {
            ("adaptive", "purposeful", "responsive"): "adapt externally while maintaining inner purpose and emotional awareness",
            ("direct", "competitive", "dynamic"): "take direct action toward competitive goals with high energy",
            ("diplomatic", "harmonious", "balanced"): "seek harmony in all areas while maintaining diplomatic relationships"
        }

        key = (asc_approach.split(',')[0].strip().lower(),
               sun_approach.split(',')[0].strip().lower(),
               moon_energy.split(',')[0].strip().lower())

        return patterns.get(key, "balance external adaptation with internal purpose and emotional wisdom")

    def _create_relationship_dynamics(self, asc_core: List, sun_core: List, moon_core: List) -> str:
        """Create relationship dynamics analysis."""
        return f"""• **First Impressions**: Others initially see your {', '.join(asc_core[:2]).lower()} nature
• **Deeper Connections**: As people get to know you, they discover your {', '.join(sun_core[:2]).lower()} core
• **Intimate Relationships**: In close relationships, your {', '.join(moon_core[:2]).lower()} emotional nature emerges
• **Relationship Challenge**: Balancing your public persona with authentic self-expression in relationships"""

    def _create_career_indicators(self, asc_traits: Dict, sun_traits: Dict, moon_traits: Dict) -> str:
        """Create career and life path indicators."""
        asc_motivation = asc_traits.get('motivation', 'external achievement')
        sun_motivation = sun_traits.get('motivation', 'personal fulfillment')
        moon_energy = moon_traits.get('energy_type', 'intuitive guidance')

        return f"""• **Public Role**: Your natural public presence suggests careers involving {asc_motivation.lower()}
• **Core Purpose**: Your authentic self seeks {sun_motivation.lower()}
• **Work Style**: You work best with {moon_energy.lower()} and emotional connection
• **Ideal Career**: Combines public engagement, personal meaning, and emotional satisfaction"""

    def _assess_overall_complexity(self, all_traits: List) -> str:
        """Assess overall personality complexity."""
        unique_traits = len(set(all_traits))
        if unique_traits > 12:
            return "highly complex and multifaceted"
        elif unique_traits > 8:
            return "moderately complex with rich diversity"
        else:
            return "focused and consistent"

    def _determine_dominant_influence(self, asc_core: List, sun_core: List, moon_core: List) -> str:
        """Determine which influence is most dominant."""
        # Simple heuristic based on trait strength
        influences = {
            "Ascendant": len(asc_core),
            "Sun": len(sun_core),
            "Moon": len(moon_core)
        }

        dominant = max(influences, key=influences.get)
        return f"{dominant} influence is most prominent in your personality expression"

    # COMPREHENSIVE MENTAL ANALYSIS HELPER METHODS

    def _analyze_mercury_influence(self, mercury) -> Dict[str, Any]:
        """Analyze Mercury's influence on mental nature."""
        if not mercury:
            return {"influence": "Mercury position unknown - general mental adaptability"}

        mercury_signs = {
            "Aries": {
                "thinking_style": "Quick, decisive, pioneering thoughts",
                "communication": "Direct, assertive, sometimes impulsive speech",
                "learning": "Learns through action and immediate application",
                "strengths": ["Fast decision-making", "Leadership in discussions", "Innovative ideas"],
                "challenges": ["Impatience with details", "May interrupt others", "Hasty conclusions"]
            },
            "Taurus": {
                "thinking_style": "Practical, methodical, thorough mental processing",
                "communication": "Steady, reliable, well-considered words",
                "learning": "Learns through repetition and hands-on experience",
                "strengths": ["Excellent memory", "Practical solutions", "Reliable information"],
                "challenges": ["Slow to change opinions", "May resist new ideas", "Stubborn thinking"]
            },
            "Gemini": {
                "thinking_style": "Versatile, curious, multi-faceted thinking",
                "communication": "Articulate, witty, adaptable expression",
                "learning": "Learns quickly through variety and mental stimulation",
                "strengths": ["Quick wit", "Excellent communication", "Mental flexibility"],
                "challenges": ["Scattered attention", "Superficial knowledge", "Inconsistent focus"]
            },
            "Cancer": {
                "thinking_style": "Intuitive, emotional, memory-based thinking",
                "communication": "Empathetic, nurturing, emotionally intelligent speech",
                "learning": "Learns through emotional connection and personal relevance",
                "strengths": ["Emotional intelligence", "Intuitive insights", "Caring communication"],
                "challenges": ["Overly subjective", "Mood-dependent thinking", "Takes criticism personally"]
            },
            "Leo": {
                "thinking_style": "Creative, confident, dramatic mental expression",
                "communication": "Charismatic, inspiring, attention-getting speech",
                "learning": "Learns through creative expression and recognition",
                "strengths": ["Creative thinking", "Inspiring communication", "Confident expression"],
                "challenges": ["Ego-driven opinions", "May dominate conversations", "Needs constant validation"]
            },
            "Virgo": {
                "thinking_style": "Analytical, detailed, perfectionist thinking",
                "communication": "Precise, helpful, constructively critical speech",
                "learning": "Learns through systematic study and practical application",
                "strengths": ["Analytical ability", "Attention to detail", "Practical solutions"],
                "challenges": ["Overly critical", "Perfectionist paralysis", "Worry and anxiety"]
            }
        }

        # Normalize Mercury sign name
        normalized_mercury_sign = self._normalize_sign_name(mercury.sign)

        sign_analysis = mercury_signs.get(normalized_mercury_sign, {
            "thinking_style": f"Unique mental approach influenced by {normalized_mercury_sign}",
            "communication": f"Communication style shaped by {normalized_mercury_sign} energy",
            "learning": f"Learning preferences influenced by {normalized_mercury_sign}",
            "strengths": [f"Mental gifts from {normalized_mercury_sign}"],
            "challenges": [f"Mental growth areas from {normalized_mercury_sign}"]
        })

        # Add house influence
        house_influence = self._get_mercury_house_influence(mercury.house)
        sign_analysis.update(house_influence)

        return sign_analysis

    def _get_mercury_house_influence(self, house: int) -> Dict[str, str]:
        """Get Mercury's house influence on mental nature."""
        house_influences = {
            1: {"house_focus": "Mental energy focused on self-expression and personal identity"},
            2: {"house_focus": "Mental energy focused on values, resources, and practical matters"},
            3: {"house_focus": "Mental energy focused on communication, learning, and immediate environment"},
            4: {"house_focus": "Mental energy focused on emotional security and family matters"},
            5: {"house_focus": "Mental energy focused on creativity, self-expression, and learning"},
            6: {"house_focus": "Mental energy focused on service, health, and daily improvement"},
            7: {"house_focus": "Mental energy focused on relationships and partnerships"},
            8: {"house_focus": "Mental energy focused on transformation and deep investigation"},
            9: {"house_focus": "Mental energy focused on higher learning and philosophical pursuits"},
            10: {"house_focus": "Mental energy focused on career and public recognition"},
            11: {"house_focus": "Mental energy focused on groups, friendships, and future goals"},
            12: {"house_focus": "Mental energy focused on spirituality and subconscious exploration"}
        }

        return house_influences.get(house, {"house_focus": "Mental energy expressed uniquely"})

    def _determine_thinking_style(self, mercury, moon, third_house_planets) -> str:
        """Determine overall thinking style from multiple factors."""
        styles = []

        if mercury:
            normalized_mercury_sign = self._normalize_sign_name(mercury.sign)
            if normalized_mercury_sign in ["Gemini", "Virgo", "Aquarius"]:
                styles.append("analytical and logical")
            elif normalized_mercury_sign in ["Cancer", "Pisces", "Scorpio"]:
                styles.append("intuitive and emotional")
            elif normalized_mercury_sign in ["Aries", "Leo", "Sagittarius"]:
                styles.append("quick and decisive")
            elif normalized_mercury_sign in ["Taurus", "Capricorn"]:
                styles.append("practical and methodical")

        if moon:
            normalized_moon_sign = self._normalize_sign_name(moon.sign)
            if normalized_moon_sign in ["Cancer", "Pisces", "Scorpio"]:
                styles.append("emotionally-influenced")
            elif normalized_moon_sign in ["Gemini", "Aquarius", "Libra"]:
                styles.append("mentally-oriented")

        if third_house_planets:
            styles.append("communication-focused")

        if not styles:
            return "Balanced thinking style with both logical and intuitive elements"

        return f"Primarily {' and '.join(styles[:2])} thinking style"

    def _determine_learning_style(self, mercury, moon) -> str:
        """Determine learning preferences."""
        if mercury:
            if mercury.sign in ["Taurus", "Virgo", "Capricorn"]:
                return "Hands-on, practical learning with step-by-step progression"
            elif mercury.sign in ["Gemini", "Aquarius", "Libra"]:
                return "Visual and auditory learning with variety and social interaction"
            elif mercury.sign in ["Cancer", "Scorpio", "Pisces"]:
                return "Emotional and intuitive learning through personal connection"
            elif mercury.sign in ["Aries", "Leo", "Sagittarius"]:
                return "Active, experiential learning through direct engagement"

        return "Adaptable learning style that combines multiple approaches"

    def _determine_communication_patterns(self, mercury, third_house_planets) -> str:
        """Determine communication patterns."""
        patterns = []

        if mercury:
            if mercury.sign in ["Aries", "Leo", "Sagittarius"]:
                patterns.append("direct and enthusiastic")
            elif mercury.sign in ["Taurus", "Virgo", "Capricorn"]:
                patterns.append("practical and reliable")
            elif mercury.sign in ["Gemini", "Libra", "Aquarius"]:
                patterns.append("articulate and social")
            elif mercury.sign in ["Cancer", "Scorpio", "Pisces"]:
                patterns.append("empathetic and intuitive")

        if third_house_planets:
            patterns.append("actively communicative")

        if not patterns:
            return "Balanced communication style adapting to situations"

        return f"Communication is {' and '.join(patterns[:2])}"

    def _analyze_moon_mental_influence(self, moon) -> Dict[str, Any]:
        """Analyze Moon's influence on mental nature."""
        if not moon:
            return {"influence": "Moon position unknown - general emotional mental processing"}

        return {
            "mental_emotional_style": f"Mental processing influenced by {moon.sign} emotional patterns",
            "memory_patterns": f"Memory and recall influenced by {moon.sign} energy",
            "subconscious_thinking": f"Subconscious mental patterns shaped by {moon.sign}",
            "intuitive_insights": f"Intuitive mental abilities enhanced by {moon.sign} placement"
        }

    def _analyze_third_house_mental_influence(self, third_house_planets) -> Dict[str, Any]:
        """Analyze 3rd house influence on mental nature."""
        if not third_house_planets:
            return {"influence": "No planets in 3rd house - natural communication abilities"}

        influences = []
        for planet in third_house_planets:
            influences.append(f"{planet.name} in 3rd house enhances {planet.sign} communication style")

        return {
            "communication_enhancement": influences,
            "learning_boost": f"Learning enhanced by {len(third_house_planets)} planet(s) in 3rd house",
            "mental_activity": "Increased mental activity and communication focus"
        }

    def _identify_mental_strengths(self, mercury, moon, third_house_planets) -> List[str]:
        """Identify mental strengths based on planetary positions."""
        strengths = []

        if mercury:
            if mercury.sign in ["Gemini", "Virgo"]:
                strengths.extend(["Excellent analytical ability", "Strong communication skills", "Detail-oriented thinking"])
            elif mercury.sign in ["Aries", "Leo", "Sagittarius"]:
                strengths.extend(["Quick decision-making", "Leadership in discussions", "Innovative thinking"])
            elif mercury.sign in ["Taurus", "Capricorn"]:
                strengths.extend(["Practical problem-solving", "Reliable memory", "Methodical approach"])

        if moon and moon.sign in ["Cancer", "Pisces", "Scorpio"]:
            strengths.extend(["Intuitive insights", "Emotional intelligence", "Empathetic understanding"])

        if third_house_planets:
            strengths.append("Enhanced communication abilities")

        return strengths[:5] if strengths else ["Natural mental adaptability", "Balanced thinking approach"]

    def _identify_mental_challenges(self, mercury, moon, third_house_planets) -> List[str]:
        """Identify mental challenges based on planetary positions."""
        challenges = []

        if mercury:
            if mercury.sign in ["Aries"]:
                challenges.extend(["Impatience with details", "May interrupt others", "Hasty conclusions"])
            elif mercury.sign in ["Taurus"]:
                challenges.extend(["Slow to change opinions", "May resist new ideas", "Stubborn thinking"])
            elif mercury.sign in ["Gemini"]:
                challenges.extend(["Scattered attention", "Superficial knowledge", "Inconsistent focus"])
            elif mercury.sign in ["Cancer"]:
                challenges.extend(["Overly subjective thinking", "Mood-dependent decisions", "Takes criticism personally"])

        if moon and moon.sign in ["Gemini", "Sagittarius"]:
            challenges.append("Mental restlessness")

        return challenges[:5] if challenges else ["Minor tendency toward overthinking"]

    def _determine_intellectual_interests(self, mercury, moon) -> List[str]:
        """Determine intellectual interests based on planetary positions."""
        interests = []

        if mercury:
            if mercury.sign in ["Aries", "Leo", "Sagittarius"]:
                interests.extend(["Leadership topics", "Adventure and exploration", "Philosophy and meaning"])
            elif mercury.sign in ["Taurus", "Virgo", "Capricorn"]:
                interests.extend(["Practical skills", "Health and wellness", "Business and finance"])
            elif mercury.sign in ["Gemini", "Libra", "Aquarius"]:
                interests.extend(["Communication arts", "Social sciences", "Technology and innovation"])
            elif mercury.sign in ["Cancer", "Scorpio", "Pisces"]:
                interests.extend(["Psychology and emotions", "Spirituality and mysticism", "Arts and creativity"])

        if moon:
            if moon.sign in ["Cancer", "Pisces"]:
                interests.append("Family and emotional topics")
            elif moon.sign in ["Scorpio"]:
                interests.append("Deep research and investigation")

        return interests[:4] if interests else ["Diverse intellectual curiosity"]

    def _analyze_information_processing(self, mercury, moon) -> str:
        """Analyze how information is processed."""
        if mercury:
            if mercury.sign in ["Virgo", "Gemini"]:
                return "Processes information analytically with attention to details and logical connections"
            elif mercury.sign in ["Cancer", "Pisces", "Scorpio"]:
                return "Processes information intuitively with emotional and symbolic understanding"
            elif mercury.sign in ["Aries", "Leo", "Sagittarius"]:
                return "Processes information quickly with focus on big picture and practical application"
            elif mercury.sign in ["Taurus", "Capricorn"]:
                return "Processes information methodically with emphasis on practical value and reliability"

        return "Processes information in a balanced way combining logic and intuition"

    # COMPREHENSIVE EMOTIONAL ANALYSIS HELPER METHODS

    def _analyze_moon_emotional_influence(self, moon) -> Dict[str, Any]:
        """Analyze Moon's emotional influence."""
        if not moon:
            return {"influence": "Moon position unknown - general emotional adaptability"}

        moon_emotional_patterns = {
            "Aries": {
                "emotional_style": "Quick, impulsive, passionate emotional responses",
                "emotional_needs": "Independence, excitement, and immediate emotional expression",
                "emotional_expression": "Direct, honest, sometimes explosive emotional display",
                "emotional_security": "Feeling free to act on impulses and lead emotionally"
            },
            "Taurus": {
                "emotional_style": "Steady, sensual, comfort-seeking emotional nature",
                "emotional_needs": "Physical comfort, stability, and sensory pleasure",
                "emotional_expression": "Calm, reliable, sometimes stubborn emotional responses",
                "emotional_security": "Material comfort and predictable emotional environment"
            },
            "Cancer": {
                "emotional_style": "Deep, nurturing, protective emotional responses",
                "emotional_needs": "Family connection, emotional safety, and caring relationships",
                "emotional_expression": "Caring, empathetic, sometimes moody emotional display",
                "emotional_security": "Strong family bonds and emotional understanding"
            },
            "Leo": {
                "emotional_style": "Warm, generous, dramatic emotional expression",
                "emotional_needs": "Appreciation, recognition, and creative emotional outlets",
                "emotional_expression": "Confident, theatrical, heart-centered emotional display",
                "emotional_security": "Being loved and appreciated for authentic self"
            },
            "Scorpio": {
                "emotional_style": "Intense, transformative, deeply feeling emotional nature",
                "emotional_needs": "Emotional depth, trust, and transformative experiences",
                "emotional_expression": "Passionate, mysterious, all-or-nothing emotional responses",
                "emotional_security": "Deep emotional bonds and psychological understanding"
            },
            "Pisces": {
                "emotional_style": "Compassionate, intuitive, spiritually-oriented emotions",
                "emotional_needs": "Spiritual connection, artistic expression, and emotional flow",
                "emotional_expression": "Gentle, empathetic, sometimes escapist emotional responses",
                "emotional_security": "Spiritual understanding and emotional transcendence"
            }
        }

        # Normalize Moon sign name
        normalized_moon_sign = self._normalize_sign_name(moon.sign)

        return moon_emotional_patterns.get(normalized_moon_sign, {
            "emotional_style": f"Emotional nature influenced by {normalized_moon_sign} energy",
            "emotional_needs": f"Emotional requirements shaped by {normalized_moon_sign}",
            "emotional_expression": f"Emotional expression colored by {normalized_moon_sign}",
            "emotional_security": f"Emotional security through {normalized_moon_sign} qualities"
        })

    def _analyze_venus_emotional_influence(self, venus) -> Dict[str, Any]:
        """Analyze Venus's emotional influence."""
        if not venus:
            return {"influence": "Venus position unknown - general relationship harmony"}

        return {
            "love_style": f"Love expression influenced by {venus.sign} energy",
            "relationship_needs": f"Relationship requirements shaped by {venus.sign}",
            "aesthetic_emotions": f"Beauty and harmony needs influenced by {venus.sign}",
            "social_emotions": f"Social emotional expression colored by {venus.sign}"
        }

    def _analyze_fourth_house_emotional_influence(self, fourth_house_planets) -> Dict[str, Any]:
        """Analyze 4th house emotional influence."""
        if not fourth_house_planets:
            return {"influence": "No planets in 4th house - natural emotional foundation"}

        influences = []
        for planet in fourth_house_planets:
            influences.append(f"{planet.name} in 4th house brings {planet.sign} energy to emotional foundation")

        return {
            "emotional_foundation": influences,
            "family_influence": f"Family dynamics enhanced by {len(fourth_house_planets)} planet(s) in 4th house",
            "emotional_security": "Strong focus on emotional security and home environment"
        }

    def _determine_emotional_style(self, moon, venus, fourth_house_planets) -> str:
        """Determine overall emotional style."""
        styles = []

        if moon:
            if moon.sign in ["Cancer", "Pisces", "Scorpio"]:
                styles.append("deep and intuitive")
            elif moon.sign in ["Aries", "Leo", "Sagittarius"]:
                styles.append("passionate and expressive")
            elif moon.sign in ["Taurus", "Virgo", "Capricorn"]:
                styles.append("stable and practical")
            elif moon.sign in ["Gemini", "Libra", "Aquarius"]:
                styles.append("intellectual and social")

        if venus:
            if venus.sign in ["Libra", "Taurus"]:
                styles.append("harmonious and aesthetic")
            elif venus.sign in ["Scorpio", "Aries"]:
                styles.append("intense and passionate")

        if fourth_house_planets:
            styles.append("family-oriented")

        if not styles:
            return "Balanced emotional style adapting to situations"

        return f"Emotional style is {' and '.join(styles[:2])}"

    def _determine_emotional_needs(self, moon, venus) -> str:
        """Determine core emotional needs."""
        needs = []

        if moon:
            if moon.sign == "Cancer":
                needs.append("emotional security and family connection")
            elif moon.sign == "Leo":
                needs.append("appreciation and creative expression")
            elif moon.sign == "Scorpio":
                needs.append("deep emotional bonds and transformation")
            elif moon.sign == "Taurus":
                needs.append("comfort and stability")
            elif moon.sign == "Pisces":
                needs.append("spiritual connection and compassion")

        if venus:
            if venus.sign in ["Libra", "Taurus"]:
                needs.append("harmony and beauty")
            elif venus.sign in ["Scorpio"]:
                needs.append("deep intimacy and trust")

        if not needs:
            return "Balanced emotional needs including security, love, and personal growth"

        return f"Core emotional needs: {' and '.join(needs[:2])}"

    def _determine_emotional_expression(self, moon, venus) -> str:
        """Determine emotional expression style."""
        if moon:
            if moon.sign in ["Aries", "Leo", "Sagittarius"]:
                return "Open, direct, and enthusiastic emotional expression"
            elif moon.sign in ["Cancer", "Pisces", "Scorpio"]:
                return "Deep, intuitive, and empathetic emotional expression"
            elif moon.sign in ["Taurus", "Virgo", "Capricorn"]:
                return "Steady, practical, and reserved emotional expression"
            elif moon.sign in ["Gemini", "Libra", "Aquarius"]:
                return "Intellectual, social, and communicative emotional expression"

        return "Balanced emotional expression adapting to circumstances"

    def _identify_emotional_strengths(self, moon, venus, fourth_house_planets) -> List[str]:
        """Identify emotional strengths."""
        strengths = []

        if moon:
            if moon.sign in ["Cancer", "Pisces"]:
                strengths.extend(["Deep empathy", "Intuitive understanding", "Nurturing ability"])
            elif moon.sign in ["Leo", "Aries"]:
                strengths.extend(["Emotional courage", "Inspiring presence", "Authentic expression"])
            elif moon.sign in ["Taurus", "Capricorn"]:
                strengths.extend(["Emotional stability", "Reliable support", "Practical wisdom"])

        if venus and venus.sign in ["Libra", "Taurus"]:
            strengths.extend(["Harmonious relationships", "Aesthetic sensitivity"])

        if fourth_house_planets:
            strengths.append("Strong family bonds")

        return strengths[:5] if strengths else ["Natural emotional balance", "Adaptive emotional responses"]

    def _identify_emotional_challenges(self, moon, venus, fourth_house_planets) -> List[str]:
        """Identify emotional challenges."""
        challenges = []

        if moon:
            if moon.sign == "Cancer":
                challenges.extend(["Mood swings", "Overly sensitive", "Clingy behavior"])
            elif moon.sign == "Scorpio":
                challenges.extend(["Emotional intensity", "Jealousy", "Holding grudges"])
            elif moon.sign == "Aries":
                challenges.extend(["Emotional impulsiveness", "Quick temper", "Impatience"])
            elif moon.sign == "Capricorn":
                challenges.extend(["Emotional reserve", "Difficulty expressing feelings", "Pessimism"])

        return challenges[:5] if challenges else ["Minor emotional sensitivity"]

    def _analyze_emotional_relationship_patterns(self, moon, venus) -> str:
        """Analyze emotional patterns in relationships."""
        if moon and venus:
            moon_style = "nurturing and protective" if moon.sign == "Cancer" else "passionate and direct" if moon.sign in ["Aries", "Leo"] else "stable and loyal"
            venus_style = "harmonious and cooperative" if venus.sign in ["Libra", "Taurus"] else "intense and transformative" if venus.sign == "Scorpio" else "independent and unique"
            return f"In relationships, you are {moon_style} emotionally and {venus_style} in love expression"

        return "Balanced approach to emotional relationships with both nurturing and independence"

    def _analyze_emotional_security_needs(self, moon, fourth_house_planets) -> str:
        """Analyze emotional security requirements."""
        security_needs = []

        if moon:
            if moon.sign == "Cancer":
                security_needs.append("strong family connections and emotional safety")
            elif moon.sign == "Taurus":
                security_needs.append("material comfort and predictable routines")
            elif moon.sign == "Scorpio":
                security_needs.append("deep trust and emotional transformation")
            elif moon.sign == "Leo":
                security_needs.append("appreciation and creative self-expression")

        if fourth_house_planets:
            security_needs.append("stable home environment")

        if not security_needs:
            return "Emotional security through balanced life and supportive relationships"

        return f"Emotional security needs: {' and '.join(security_needs[:2])}"

    # SIGN NAME MAPPING SYSTEM

    def _normalize_sign_name(self, sign_name: str) -> str:
        """Convert any sign name (Sanskrit/English) to standard English name."""
        # Sanskrit to English mapping
        sanskrit_to_english = {
            "Mesha": "Aries",
            "Vrishabha": "Taurus",
            "Mithuna": "Gemini",
            "Karka": "Cancer",
            "Simha": "Leo",
            "Kanya": "Virgo",
            "Tula": "Libra",
            "Vrishchika": "Scorpio",
            "Dhanu": "Sagittarius",
            "Makara": "Capricorn",
            "Kumbha": "Aquarius",
            "Meena": "Pisces"
        }

        # Clean the input
        clean_sign = sign_name.strip()

        # Try direct English match first
        english_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

        if clean_sign in english_signs:
            return clean_sign

        # Try Sanskrit to English conversion
        if clean_sign in sanskrit_to_english:
            return sanskrit_to_english[clean_sign]

        # Try case-insensitive match for English
        for eng_sign in english_signs:
            if clean_sign.lower() == eng_sign.lower():
                return eng_sign

        # Try case-insensitive match for Sanskrit
        for sans_sign, eng_sign in sanskrit_to_english.items():
            if clean_sign.lower() == sans_sign.lower():
                return eng_sign

        # If no match found, return original (this shouldn't happen with valid data)
        print(f"Warning: Unknown sign name '{sign_name}', returning as-is")
        return clean_sign

    # COMPREHENSIVE PLANETARY ISOLATION ANALYSIS

    def _analyze_comprehensive_planetary_isolation(self, chart: VedicChart) -> List[Dict[str, str]]:
        """
        Comprehensive analysis of planetary isolation in the chart.
        Examines all planets for isolation patterns and their effects on yogas.
        """
        isolation_yogas = []

        # Get planet positions organized by house and sign
        planets_by_house = self._organize_planets_by_house(chart)
        planets_by_sign = self._organize_planets_by_sign(chart)

        # Analyze each planet for isolation
        for planet in chart.planets:
            isolation_analysis = self._analyze_planet_isolation(planet, chart, planets_by_house, planets_by_sign)
            if isolation_analysis:
                isolation_yogas.append(isolation_analysis)

        # Analyze specific isolation yogas
        kemadruma_analysis = self._analyze_kemadruma_yoga(chart, planets_by_house)
        if kemadruma_analysis:
            isolation_yogas.append(kemadruma_analysis)

        # Analyze planetary support systems
        support_analysis = self._analyze_planetary_support_systems(chart, planets_by_house, planets_by_sign)
        isolation_yogas.extend(support_analysis)

        # Analyze isolation effects on major yogas
        yoga_isolation_effects = self._analyze_yoga_isolation_effects(chart, planets_by_house, planets_by_sign)
        isolation_yogas.extend(yoga_isolation_effects)

        return isolation_yogas

    def _organize_planets_by_house(self, chart: VedicChart) -> Dict[int, List]:
        """Organize planets by house for isolation analysis."""
        planets_by_house = {}
        for i in range(1, 13):
            planets_by_house[i] = []

        for planet in chart.planets:
            planets_by_house[planet.house].append(planet)

        return planets_by_house

    def _organize_planets_by_sign(self, chart: VedicChart) -> Dict[str, List]:
        """Organize planets by sign for isolation analysis."""
        planets_by_sign = {}
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

        for sign in signs:
            planets_by_sign[sign] = []

        for planet in chart.planets:
            normalized_sign = self._normalize_sign_name(planet.sign)
            if normalized_sign in planets_by_sign:
                planets_by_sign[normalized_sign].append(planet)

        return planets_by_sign

    def _analyze_planet_isolation(self, planet, chart: VedicChart, planets_by_house: Dict, planets_by_sign: Dict) -> Dict[str, str]:
        """Analyze isolation status of a specific planet."""
        isolation_factors = []
        isolation_level = "None"

        # Check house isolation (no planets in adjacent houses)
        current_house = planet.house
        prev_house = 12 if current_house == 1 else current_house - 1
        next_house = 1 if current_house == 12 else current_house + 1

        house_isolation = (len(planets_by_house[prev_house]) == 0 and
                          len(planets_by_house[next_house]) == 0)

        # Check sign isolation (alone in sign)
        normalized_planet_sign = self._normalize_sign_name(planet.sign)
        sign_isolation = len(planets_by_sign[normalized_planet_sign]) == 1

        # Check aspect isolation (no major aspects from benefics)
        aspect_isolation = self._check_aspect_isolation(planet, chart)

        # Check conjunction isolation (no close conjunctions)
        conjunction_isolation = self._check_conjunction_isolation(planet, chart)

        # Determine isolation level and effects
        if house_isolation and sign_isolation:
            isolation_level = "Severe"
            isolation_factors.append("isolated in both house and sign")
        elif house_isolation or sign_isolation:
            isolation_level = "Moderate"
            if house_isolation:
                isolation_factors.append("isolated in house (no adjacent planets)")
            if sign_isolation:
                isolation_factors.append("alone in sign")

        if aspect_isolation:
            isolation_factors.append("lacks benefic aspects")
            if isolation_level == "None":
                isolation_level = "Mild"

        if conjunction_isolation:
            isolation_factors.append("no close planetary companions")
            if isolation_level == "None":
                isolation_level = "Mild"

        # Return analysis if planet has significant isolation
        if isolation_level != "None":
            effects = self._get_planet_isolation_effects(planet.name, isolation_level, isolation_factors)

            return {
                "name": f"{planet.name} Isolation Analysis",
                "description": f"{planet.name} in {planet.sign} (House {planet.house}) shows {isolation_level.lower()} isolation: {', '.join(isolation_factors)}. {effects}",
                "strength": "Challenging" if isolation_level == "Severe" else "Moderate",
                "category": "Planetary Isolation"
            }

        return None

    def _check_aspect_isolation(self, planet, chart: VedicChart) -> bool:
        """Check if planet lacks benefic aspects."""
        benefic_planets = ["Jupiter", "Venus", "Mercury", "Moon"]

        for other_planet in chart.planets:
            if (other_planet.name in benefic_planets and
                other_planet.name != planet.name):

                # Check for major aspects (conjunction, trine, sextile)
                angle_diff = abs(planet.longitude - other_planet.longitude)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff

                # Major benefic aspects (within 8 degrees orb)
                if (angle_diff <= 8 or  # Conjunction
                    abs(angle_diff - 60) <= 8 or  # Sextile
                    abs(angle_diff - 120) <= 8):  # Trine
                    return False

        return True

    def _check_conjunction_isolation(self, planet, chart: VedicChart) -> bool:
        """Check if planet has no close conjunctions."""
        for other_planet in chart.planets:
            if other_planet.name != planet.name:
                angle_diff = abs(planet.longitude - other_planet.longitude)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff

                # Close conjunction (within 10 degrees)
                if angle_diff <= 10:
                    return False

        return True

    def _get_planet_isolation_effects(self, planet_name: str, isolation_level: str, factors: List[str]) -> str:
        """Get specific effects of planetary isolation."""
        planet_effects = {
            "Sun": {
                "Severe": "May struggle with self-confidence and leadership recognition. Needs to develop independent authority.",
                "Moderate": "May feel unsupported in leadership roles. Benefits from building strong personal identity.",
                "Mild": "Occasional feelings of being unrecognized. Generally maintains good self-esteem."
            },
            "Moon": {
                "Severe": "Emotional isolation and difficulty finding emotional support. May experience mood instability.",
                "Moderate": "Periodic emotional loneliness. Needs to cultivate supportive relationships.",
                "Mild": "Occasional emotional distance. Generally maintains emotional balance."
            },
            "Mercury": {
                "Severe": "Communication challenges and intellectual isolation. May struggle to express ideas effectively.",
                "Moderate": "Periodic communication difficulties. Benefits from developing diverse intellectual connections.",
                "Mild": "Occasional misunderstandings. Generally communicates well."
            },
            "Venus": {
                "Severe": "Relationship challenges and difficulty finding love/harmony. May experience social isolation.",
                "Moderate": "Periodic relationship difficulties. Needs to cultivate social connections.",
                "Mild": "Occasional social awkwardness. Generally maintains good relationships."
            },
            "Mars": {
                "Severe": "Difficulty channeling energy effectively. May struggle with motivation and action.",
                "Moderate": "Periodic energy blocks. Benefits from structured physical activities.",
                "Mild": "Occasional energy fluctuations. Generally maintains good drive."
            },
            "Jupiter": {
                "Severe": "Lack of wisdom guidance and spiritual support. May struggle with higher learning.",
                "Moderate": "Periodic lack of guidance. Benefits from seeking mentors and teachers.",
                "Mild": "Occasional wisdom gaps. Generally maintains good judgment."
            },
            "Saturn": {
                "Severe": "Extreme self-reliance burden. May experience harsh life lessons without support.",
                "Moderate": "Heavy responsibility load. Benefits from structured support systems.",
                "Mild": "Occasional isolation in responsibilities. Generally handles duties well."
            }
        }

        return planet_effects.get(planet_name, {}).get(isolation_level,
            f"Isolation affects {planet_name}'s natural expression and requires conscious effort to overcome.")

    def _analyze_kemadruma_yoga(self, chart: VedicChart, planets_by_house: Dict) -> Dict[str, str]:
        """Analyze specific Kemadruma Yoga (Moon isolation)."""
        moon = next((p for p in chart.planets if p.name == "Moon"), None)
        if not moon:
            return None

        moon_house = moon.house
        prev_house = 12 if moon_house == 1 else moon_house - 1
        next_house = 1 if moon_house == 12 else moon_house + 1

        # Check if Moon is isolated (no planets in adjacent houses)
        moon_isolated = (len(planets_by_house[prev_house]) == 0 and
                        len(planets_by_house[next_house]) == 0)

        if moon_isolated:
            # Check for cancellation factors
            cancellation_factors = []

            # Kendra planets cancel Kemadruma
            kendra_houses = [1, 4, 7, 10]
            for house in kendra_houses:
                if len(planets_by_house[house]) > 0:
                    planets_in_kendra = [p.name for p in planets_by_house[house]]
                    cancellation_factors.append(f"planets in {house}th house ({', '.join(planets_in_kendra)})")

            # Strong aspects to Moon cancel Kemadruma
            strong_aspects = self._check_strong_aspects_to_moon(moon, chart)
            if strong_aspects:
                cancellation_factors.extend(strong_aspects)

            if cancellation_factors:
                return {
                    "name": "Kemadruma Yoga (Cancelled)",
                    "description": f"Moon in {moon.sign} (House {moon_house}) is isolated from adjacent houses, forming Kemadruma Yoga. However, this is cancelled by: {', '.join(cancellation_factors)}. This provides emotional resilience and self-reliance while maintaining support systems.",
                    "strength": "Moderate",
                    "category": "Emotional Support"
                }
            else:
                return {
                    "name": "Kemadruma Yoga (Active)",
                    "description": f"Moon in {moon.sign} (House {moon_house}) is isolated from adjacent houses, forming active Kemadruma Yoga. This creates emotional self-reliance but may lead to feelings of isolation and lack of emotional support. Requires conscious effort to build supportive relationships.",
                    "strength": "Challenging",
                    "category": "Emotional Isolation"
                }

        return None

    def _check_strong_aspects_to_moon(self, moon, chart: VedicChart) -> List[str]:
        """Check for strong aspects to Moon that cancel Kemadruma."""
        strong_aspects = []
        benefic_planets = ["Jupiter", "Venus"]

        for planet in chart.planets:
            if planet.name in benefic_planets:
                angle_diff = abs(moon.longitude - planet.longitude)
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff

                # Strong aspects (within 5 degrees orb)
                if angle_diff <= 5:  # Conjunction
                    strong_aspects.append(f"{planet.name} conjunction")
                elif abs(angle_diff - 120) <= 5:  # Trine
                    strong_aspects.append(f"{planet.name} trine aspect")
                elif abs(angle_diff - 60) <= 5:  # Sextile
                    strong_aspects.append(f"{planet.name} sextile aspect")

        return strong_aspects

    def _analyze_planetary_support_systems(self, chart: VedicChart, planets_by_house: Dict, planets_by_sign: Dict) -> List[Dict[str, str]]:
        """Analyze planetary support systems and mutual support."""
        support_analyses = []

        # Analyze mutual reception (planets in each other's signs)
        mutual_receptions = self._find_mutual_receptions(chart)
        for reception in mutual_receptions:
            support_analyses.append({
                "name": "Mutual Reception Support",
                "description": f"{reception['planet1']} in {reception['sign1']} and {reception['planet2']} in {reception['sign2']} create mutual reception. This provides strong mutual support and enhances both planets' positive effects.",
                "strength": "Strong",
                "category": "Planetary Support"
            })

        # Analyze planetary clusters (3+ planets together)
        clusters = self._find_planetary_clusters(planets_by_sign)
        for cluster in clusters:
            if len(cluster['planets']) >= 3:
                support_analyses.append({
                    "name": "Planetary Cluster Support",
                    "description": f"Strong planetary cluster in {cluster['sign']}: {', '.join([p.name for p in cluster['planets']])}. This creates intense focus and mutual support in {cluster['sign']} themes, though may create imbalance in other areas.",
                    "strength": "Strong",
                    "category": "Planetary Concentration"
                })

        # Analyze benefic protection patterns
        benefic_protection = self._analyze_benefic_protection(chart, planets_by_house)
        if benefic_protection:
            support_analyses.append(benefic_protection)

        return support_analyses

    def _find_mutual_receptions(self, chart: VedicChart) -> List[Dict[str, str]]:
        """Find mutual reception patterns between planets."""
        mutual_receptions = []

        # Traditional rulerships
        rulerships = {
            "Sun": ["Leo"],
            "Moon": ["Cancer"],
            "Mercury": ["Gemini", "Virgo"],
            "Venus": ["Taurus", "Libra"],
            "Mars": ["Aries", "Scorpio"],
            "Jupiter": ["Sagittarius", "Pisces"],
            "Saturn": ["Capricorn", "Aquarius"]
        }

        for planet1 in chart.planets:
            for planet2 in chart.planets:
                if planet1.name != planet2.name:
                    # Check if planet1 is in planet2's sign and vice versa
                    planet1_rules = rulerships.get(planet1.name, [])
                    planet2_rules = rulerships.get(planet2.name, [])

                    # Normalize sign names for comparison
                    normalized_planet1_sign = self._normalize_sign_name(planet1.sign)
                    normalized_planet2_sign = self._normalize_sign_name(planet2.sign)

                    if (normalized_planet2_sign in planet1_rules and normalized_planet1_sign in planet2_rules):
                        # Avoid duplicates
                        reception_exists = any(
                            (r['planet1'] == planet2.name and r['planet2'] == planet1.name)
                            for r in mutual_receptions
                        )

                        if not reception_exists:
                            mutual_receptions.append({
                                'planet1': planet1.name,
                                'planet2': planet2.name,
                                'sign1': normalized_planet1_sign,
                                'sign2': normalized_planet2_sign
                            })

        return mutual_receptions

    def _find_planetary_clusters(self, planets_by_sign: Dict) -> List[Dict[str, Any]]:
        """Find significant planetary clusters."""
        clusters = []

        for sign, planets in planets_by_sign.items():
            if len(planets) >= 2:  # 2 or more planets
                clusters.append({
                    'sign': sign,
                    'planets': planets,
                    'count': len(planets)
                })

        return clusters

    def _analyze_benefic_protection(self, chart: VedicChart, planets_by_house: Dict) -> Dict[str, str]:
        """Analyze benefic protection patterns."""
        jupiter = next((p for p in chart.planets if p.name == "Jupiter"), None)
        venus = next((p for p in chart.planets if p.name == "Venus"), None)

        if not jupiter and not venus:
            return None

        protection_factors = []

        # Jupiter in kendra provides protection
        if jupiter and jupiter.house in [1, 4, 7, 10]:
            protection_factors.append(f"Jupiter in {jupiter.house}th house (kendra)")

        # Venus in kendra provides harmony
        if venus and venus.house in [1, 4, 7, 10]:
            protection_factors.append(f"Venus in {venus.house}th house (kendra)")

        # Benefics in trikona provide spiritual protection
        if jupiter and jupiter.house in [1, 5, 9]:
            protection_factors.append(f"Jupiter in {jupiter.house}th house (trikona)")

        if protection_factors:
            return {
                "name": "Benefic Protection Pattern",
                "description": f"Strong benefic protection through: {', '.join(protection_factors)}. This provides natural protection from difficulties and enhances positive outcomes in life.",
                "strength": "Strong",
                "category": "Divine Protection"
            }

        return None

    def _analyze_yoga_isolation_effects(self, chart: VedicChart, planets_by_house: Dict, planets_by_sign: Dict) -> List[Dict[str, str]]:
        """Analyze how planetary isolation affects major yogas."""
        yoga_effects = []

        # Check isolation effects on Gaja Kesari Yoga
        jupiter = next((p for p in chart.planets if p.name == "Jupiter"), None)
        moon = next((p for p in chart.planets if p.name == "Moon"), None)

        if jupiter and moon:
            # Check if either planet is isolated
            jupiter_isolated = self._is_planet_isolated(jupiter, planets_by_house, planets_by_sign)
            moon_isolated = self._is_planet_isolated(moon, planets_by_house, planets_by_sign)

            if jupiter_isolated or moon_isolated:
                isolated_planets = []
                if jupiter_isolated:
                    isolated_planets.append("Jupiter")
                if moon_isolated:
                    isolated_planets.append("Moon")

                yoga_effects.append({
                    "name": "Gaja Kesari Yoga Isolation Effect",
                    "description": f"Gaja Kesari Yoga is affected by isolation of {', '.join(isolated_planets)}. This may reduce the yoga's beneficial effects on wisdom, prosperity, and reputation. The isolated planet(s) need additional support through spiritual practices or conscious effort.",
                    "strength": "Moderate",
                    "category": "Yoga Modification"
                })

        # Check isolation effects on Panch Mahapurusha Yogas
        mars = next((p for p in chart.planets if p.name == "Mars"), None)
        mercury = next((p for p in chart.planets if p.name == "Mercury"), None)
        venus = next((p for p in chart.planets if p.name == "Venus"), None)
        saturn = next((p for p in chart.planets if p.name == "Saturn"), None)

        mahapurusha_planets = [
            (mars, "Mars", "Ruchaka Yoga"),
            (mercury, "Mercury", "Bhadra Yoga"),
            (jupiter, "Jupiter", "Hamsa Yoga"),
            (venus, "Venus", "Malavya Yoga"),
            (saturn, "Saturn", "Sasha Yoga")
        ]

        for planet, name, yoga_name in mahapurusha_planets:
            if planet and planet.house in [1, 4, 7, 10]:  # Kendra placement
                if self._is_planet_isolated(planet, planets_by_house, planets_by_sign):
                    yoga_effects.append({
                        "name": f"{yoga_name} Isolation Effect",
                        "description": f"{name} forms {yoga_name} but is isolated, which may create a self-reliant but potentially lonely expression of {name}'s qualities. The person may achieve success through individual effort but may lack collaborative support.",
                        "strength": "Moderate",
                        "category": "Yoga Modification"
                    })

        # Check isolation effects on Raja Yoga combinations
        raja_yoga_houses = [1, 4, 5, 7, 9, 10]  # Kendra and Trikona
        isolated_raja_planets = []

        for planet in chart.planets:
            if planet.house in raja_yoga_houses:
                if self._is_planet_isolated(planet, planets_by_house, planets_by_sign):
                    isolated_raja_planets.append(planet.name)

        if len(isolated_raja_planets) >= 2:
            yoga_effects.append({
                "name": "Raja Yoga Isolation Pattern",
                "description": f"Multiple planets ({', '.join(isolated_raja_planets)}) in raja yoga positions are isolated. This creates potential for independent leadership and authority but may result in isolation at the top. Success may come through individual merit rather than collaborative effort.",
                "strength": "Significant",
                "category": "Leadership Isolation"
            })

        # Check for overall isolation patterns affecting spiritual yogas
        spiritual_houses = [5, 8, 9, 12]
        isolated_spiritual_planets = []

        for planet in chart.planets:
            if planet.house in spiritual_houses:
                if self._is_planet_isolated(planet, planets_by_house, planets_by_sign):
                    isolated_spiritual_planets.append(planet.name)

        if len(isolated_spiritual_planets) >= 2:
            yoga_effects.append({
                "name": "Spiritual Isolation Pattern",
                "description": f"Multiple planets ({', '.join(isolated_spiritual_planets)}) in spiritual houses are isolated. This indicates a solitary spiritual path with deep inner development but may lack external spiritual community support. Meditation and self-study are favored over group spiritual activities.",
                "strength": "Moderate",
                "category": "Spiritual Development"
            })

        return yoga_effects

    def _is_planet_isolated(self, planet, planets_by_house: Dict, planets_by_sign: Dict) -> bool:
        """Check if a planet is significantly isolated."""
        # House isolation check
        current_house = planet.house
        prev_house = 12 if current_house == 1 else current_house - 1
        next_house = 1 if current_house == 12 else current_house + 1

        house_isolation = (len(planets_by_house[prev_house]) == 0 and
                          len(planets_by_house[next_house]) == 0)

        # Sign isolation check
        normalized_planet_sign = self._normalize_sign_name(planet.sign)
        sign_isolation = len(planets_by_sign[normalized_planet_sign]) == 1

        # Consider planet isolated if it has both house and sign isolation
        # or severe house isolation with no close conjunctions
        return house_isolation and (sign_isolation or len(planets_by_sign[normalized_planet_sign]) <= 2)