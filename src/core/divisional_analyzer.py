"""
Comprehensive Divisional Charts (Vargas) Analyzer
Provides detailed, specific interpretations of planetary positions in divisional charts.
"""

from typing import Dict, List, Any
from src.models.models import VedicChart, PlanetPosition


class DivisionalAnalyzer:
    """Comprehensive analyzer for divisional charts with detailed interpretations."""

    def __init__(self):
        self.divisional_meanings = self._initialize_divisional_meanings()
        self.planetary_effects = self._initialize_planetary_effects()

    def _initialize_divisional_meanings(self) -> Dict[str, Dict]:
        """Initialize comprehensive meanings for each divisional chart."""
        return {
            "D2": {
                "name": "Hora Chart",
                "primary_significance": "Wealth, Money, Material Resources",
                "detailed_areas": [
                    "Financial prosperity and wealth accumulation",
                    "Relationship with money and material possessions",
                    "Income sources and earning capacity",
                    "Financial stability and security",
                    "Attitude towards material comforts"
                ],
                "sun_hora_effects": {
                    "positive": "Strong earning capacity, leadership in financial matters, government-related income",
                    "negative": "Ego issues with money, overspending on status, financial pride"
                },
                "moon_hora_effects": {
                    "positive": "Intuitive money management, emotional security through wealth, family wealth",
                    "negative": "Emotional spending, fluctuating income, dependency on others financially"
                }
            },
            "D3": {
                "name": "Drekkana Chart",
                "primary_significance": "Siblings, Courage, Communication",
                "detailed_areas": [
                    "Relationship with brothers and sisters",
                    "Personal courage and bravery",
                    "Communication skills and writing ability",
                    "Short journeys and local travel",
                    "Hands, arms, and manual dexterity",
                    "Initiative and enterprise"
                ],
                "house_effects": {
                    1: "Strong personality, courageous nature, leadership among siblings",
                    2: "Financial support from siblings, speech-related talents",
                    3: "Excellent sibling relationships, strong communication skills",
                    4: "Emotional bonds with siblings, protective nature",
                    5: "Creative collaboration with siblings, intelligent communication",
                    6: "Competitive with siblings, health issues affecting communication",
                    7: "Partnership-oriented communication, diplomatic siblings",
                    8: "Transformative relationships with siblings, occult communication",
                    9: "Philosophical siblings, higher learning through communication",
                    10: "Professional communication skills, career through siblings",
                    11: "Gains through siblings, large social network",
                    12: "Spiritual communication, distant siblings"
                }
            },
            "D9": {
                "name": "Navamsa Chart",
                "primary_significance": "Marriage, Spouse, Spiritual Development",
                "detailed_areas": [
                    "Marriage compatibility and spouse characteristics",
                    "Post-marriage life and marital happiness",
                    "Spiritual growth and dharma",
                    "Second half of life (after 35)",
                    "Inner strength and character",
                    "Religious inclinations and higher wisdom"
                ],
                "house_effects": {
                    1: "Strong marriage, spiritually inclined spouse, good character",
                    2: "Wealthy spouse, family-oriented marriage, traditional values",
                    3: "Communicative spouse, sibling-like relationship, short travels together",
                    4: "Emotionally nurturing marriage, domestic happiness, property through spouse",
                    5: "Creative and intelligent spouse, children bring joy, romantic marriage",
                    6: "Service-oriented spouse, health challenges in marriage, daily routine conflicts",
                    7: "Harmonious marriage, business partnerships with spouse, diplomatic partner",
                    8: "Transformative marriage, spouse brings changes, occult interests together",
                    9: "Spiritual marriage, philosophical spouse, foreign connections through marriage",
                    10: "Career-oriented spouse, public recognition through marriage, authoritative partner",
                    11: "Gains through marriage, large friend circle, fulfillment of desires through spouse",
                    12: "Spiritual spouse, foreign settlement, sacrifices in marriage"
                }
            },
            "D10": {
                "name": "Dasamsa Chart",
                "primary_significance": "Career, Profession, Public Reputation",
                "detailed_areas": [
                    "Professional success and career growth",
                    "Public image and social status",
                    "Authority and leadership positions",
                    "Government connections and recognition",
                    "Professional skills and expertise",
                    "Career stability and achievements"
                ],
                "house_effects": {
                    1: "Natural leadership, self-made career, strong professional identity",
                    2: "Career in finance/food, family business, speech-related profession",
                    3: "Communication-based career, media, writing, sales, marketing",
                    4: "Real estate, education, psychology, nurturing professions",
                    5: "Creative fields, entertainment, education, speculation, sports",
                    6: "Healthcare, service sector, legal profession, problem-solving careers",
                    7: "Business partnerships, diplomacy, counseling, public relations",
                    8: "Research, investigation, occult sciences, transformation industries",
                    9: "Teaching, law, philosophy, publishing, international business",
                    10: "Government service, politics, administration, high authority positions",
                    11: "Large organizations, networking, technology, gains through career",
                    12: "Foreign employment, spiritual professions, behind-the-scenes work"
                }
            },
            "D12": {
                "name": "Dwadasamsa Chart",
                "primary_significance": "Parents, Ancestry, Family Heritage",
                "detailed_areas": [
                    "Relationship with mother and father",
                    "Family lineage and ancestral influences",
                    "Inherited traits and family karma",
                    "Parental blessings and support",
                    "Family traditions and cultural heritage",
                    "Ancestral property and inheritance"
                ],
                "house_effects": {
                    1: "Strong parental influence on personality, family leadership qualities",
                    2: "Financial inheritance, family wealth, traditional family values",
                    3: "Good communication with parents, siblings support family",
                    4: "Deep emotional bond with mother, strong family roots",
                    5: "Creative family, intelligent parents, good relationship with children",
                    6: "Service to parents, health issues in family, family conflicts",
                    7: "Balanced relationship with both parents, family partnerships",
                    8: "Family secrets, transformative family events, occult family traditions",
                    9: "Spiritual family, learned parents, family involved in higher education",
                    10: "Authoritative parents, family reputation, career through family connections",
                    11: "Gains through family, large extended family, fulfillment of family desires",
                    12: "Spiritual family background, foreign family connections, family sacrifices"
                }
            },
            "D4": {
                "name": "Chaturthamsa Chart",
                "primary_significance": "Fortune, Property, Vehicles, Fixed Assets",
                "detailed_areas": [
                    "Real estate and property ownership",
                    "Vehicles and transportation",
                    "Fixed assets and material comforts",
                    "Fortune and luck in material matters",
                    "Home and residential properties",
                    "Land and agricultural assets"
                ],
                "house_effects": {
                    1: "Self-acquired property, natural fortune, personal assets",
                    2: "Family property, inherited assets, wealth through property",
                    3: "Property through siblings, short-distance real estate",
                    4: "Maternal property, home ownership, domestic assets",
                    5: "Property through speculation, creative real estate ventures",
                    6: "Property disputes, legal issues with assets, service properties",
                    7: "Property through spouse, business real estate, partnership assets",
                    8: "Hidden assets, property through inheritance, transformative real estate",
                    9: "Foreign property, property through higher learning, dharmic assets",
                    10: "Property through career, government assets, authoritative real estate",
                    11: "Gains through property, large real estate holdings, profitable assets",
                    12: "Foreign property, spiritual assets, property losses or sacrifices"
                }
            },
            "D7": {
                "name": "Saptamsa Chart",
                "primary_significance": "Children, Creativity, Progeny, Grandchildren",
                "detailed_areas": [
                    "Relationship with children and grandchildren",
                    "Creative abilities and artistic talents",
                    "Fertility and reproductive health",
                    "Creative projects and innovations",
                    "Entertainment and recreational activities",
                    "Speculative gains and investments"
                ],
                "house_effects": {
                    1: "Natural creativity, self-expression, leadership in creative fields",
                    2: "Creative wealth, children bring financial gains, artistic family",
                    3: "Creative communication, artistic siblings, creative writing",
                    4: "Creative home environment, artistic mother, domestic creativity",
                    5: "Excellent for children, strong creative abilities, artistic talents",
                    6: "Health issues affecting creativity, competitive creative fields",
                    7: "Creative partnerships, artistic spouse, collaborative creativity",
                    8: "Transformative creativity, occult creative abilities, hidden talents",
                    9: "Philosophical creativity, higher creative learning, dharmic arts",
                    10: "Creative career, artistic reputation, public creative recognition",
                    11: "Gains through creativity, large creative network, fulfilled creative desires",
                    12: "Spiritual creativity, foreign creative connections, creative sacrifices"
                }
            },
            "D16": {
                "name": "Shodasamsa Chart",
                "primary_significance": "Vehicles, Comforts, Happiness, Luxuries",
                "detailed_areas": [
                    "Vehicles and transportation comforts",
                    "Material happiness and luxuries",
                    "Comfort level in life",
                    "Enjoyment and pleasure",
                    "Material satisfaction",
                    "Lifestyle and living standards"
                ],
                "house_effects": {
                    1: "Personal comfort, self-acquired luxuries, natural happiness",
                    2: "Family comforts, inherited luxuries, traditional happiness",
                    3: "Comfort through siblings, communication-based happiness",
                    4: "Domestic comfort, maternal luxuries, home-based happiness",
                    5: "Creative comforts, entertainment luxuries, speculative happiness",
                    6: "Service-based comfort, health-related luxuries, competitive happiness",
                    7: "Partnership comfort, spouse-related luxuries, diplomatic happiness",
                    8: "Hidden comforts, transformative luxuries, occult happiness",
                    9: "Spiritual comfort, foreign luxuries, dharmic happiness",
                    10: "Career comfort, authoritative luxuries, public happiness",
                    11: "Gains through comfort, large luxury network, fulfilled happiness",
                    12: "Foreign comfort, spiritual luxuries, sacrificial happiness"
                }
            },
            "D20": {
                "name": "Vimsamsa Chart",
                "primary_significance": "Spiritual Practices, Religious Inclinations, Devotion",
                "detailed_areas": [
                    "Spiritual practices and meditation",
                    "Religious inclinations and devotion",
                    "Worship and ritual practices",
                    "Spiritual growth and development",
                    "Connection with divine",
                    "Religious studies and philosophy"
                ],
                "house_effects": {
                    1: "Natural spirituality, self-initiated practices, spiritual leadership",
                    2: "Family spirituality, traditional practices, inherited devotion",
                    3: "Spiritual communication, religious siblings, devotional expression",
                    4: "Domestic spirituality, maternal devotion, home-based practices",
                    5: "Creative spirituality, intelligent devotion, speculative practices",
                    6: "Service-oriented spirituality, healing practices, competitive devotion",
                    7: "Partnership spirituality, spouse-related practices, diplomatic devotion",
                    8: "Transformative spirituality, occult practices, hidden devotion",
                    9: "Higher spirituality, guru connection, dharmic practices",
                    10: "Public spirituality, authoritative practices, career-based devotion",
                    11: "Gains through spirituality, large spiritual network, fulfilled devotion",
                    12: "Foreign spirituality, renunciation practices, sacrificial devotion"
                }
            },
            "D24": {
                "name": "Chaturvimsamsa Chart",
                "primary_significance": "Learning, Education, Knowledge, Wisdom",
                "detailed_areas": [
                    "Educational achievements and learning",
                    "Knowledge acquisition and wisdom",
                    "Academic success and scholarship",
                    "Teaching and mentoring abilities",
                    "Intellectual development",
                    "Research and study capabilities"
                ],
                "house_effects": {
                    1: "Natural learning ability, self-education, intellectual leadership",
                    2: "Family education, traditional knowledge, inherited wisdom",
                    3: "Communication-based learning, sibling education, expressive knowledge",
                    4: "Domestic education, maternal learning, home-based knowledge",
                    5: "Creative learning, intelligent education, speculative knowledge",
                    6: "Service-based learning, practical education, competitive knowledge",
                    7: "Partnership learning, spouse education, diplomatic knowledge",
                    8: "Transformative learning, occult education, hidden knowledge",
                    9: "Higher learning, guru education, dharmic knowledge",
                    10: "Public learning, authoritative education, career-based knowledge",
                    11: "Gains through learning, large educational network, fulfilled knowledge",
                    12: "Foreign learning, spiritual education, sacrificial knowledge"
                }
            },
            "D30": {
                "name": "Trimsamsa Chart",
                "primary_significance": "Misfortunes, Diseases, Enemies, Obstacles",
                "detailed_areas": [
                    "Health challenges and diseases",
                    "Enemies and opposition",
                    "Obstacles and difficulties",
                    "Misfortunes and setbacks",
                    "Legal troubles and conflicts",
                    "Hidden dangers and threats"
                ],
                "house_effects": {
                    1: "Personal health issues, self-created obstacles, individual challenges",
                    2: "Family health problems, financial obstacles, traditional challenges",
                    3: "Communication obstacles, sibling conflicts, expressive challenges",
                    4: "Domestic health issues, maternal obstacles, home-based challenges",
                    5: "Creative obstacles, speculative challenges, entertainment problems",
                    6: "Service health issues, competitive obstacles, work-related challenges",
                    7: "Partnership obstacles, spouse conflicts, diplomatic challenges",
                    8: "Hidden health issues, transformative obstacles, occult challenges",
                    9: "Spiritual obstacles, foreign challenges, dharmic difficulties",
                    10: "Career obstacles, public health issues, authoritative challenges",
                    11: "Network obstacles, gain-related challenges, social difficulties",
                    12: "Foreign health issues, spiritual obstacles, sacrificial challenges"
                }
            },
            "D60": {
                "name": "Shashtyamsa Chart",
                "primary_significance": "Past Life Karma, Overall Destiny, Karmic Patterns",
                "detailed_areas": [
                    "Past life karma and influences",
                    "Overall destiny and life purpose",
                    "Karmic patterns and lessons",
                    "Soul evolution and growth",
                    "Inherited karmic debts",
                    "Spiritual destiny and path"
                ],
                "house_effects": {
                    1: "Personal karma, self-created destiny, individual soul purpose",
                    2: "Family karma, inherited destiny, traditional soul patterns",
                    3: "Communication karma, sibling destiny, expressive soul purpose",
                    4: "Domestic karma, maternal destiny, home-based soul patterns",
                    5: "Creative karma, speculative destiny, entertainment soul purpose",
                    6: "Service karma, competitive destiny, work-related soul patterns",
                    7: "Partnership karma, spouse destiny, diplomatic soul purpose",
                    8: "Hidden karma, transformative destiny, occult soul patterns",
                    9: "Spiritual karma, foreign destiny, dharmic soul purpose",
                    10: "Career karma, public destiny, authoritative soul patterns",
                    11: "Network karma, gain-related destiny, social soul purpose",
                    12: "Foreign karma, spiritual destiny, sacrificial soul patterns"
                }
            }
        }

    def _initialize_planetary_effects(self) -> Dict[str, Dict]:
        """Initialize specific planetary effects in divisional charts."""
        return {
            "Sun": {
                "D2": "Leadership in financial matters, government income, authoritative wealth",
                "D3": "Courageous communication, leadership among siblings, authoritative speech",
                "D9": "Authoritative spouse, government connections through marriage, spiritual leadership",
                "D10": "Government career, leadership positions, political success, public recognition",
                "D12": "Authoritative father, government family background, family leadership",
                "D4": "Government property, authoritative assets, leadership in real estate",
                "D7": "Authoritative children, leadership creativity, government artistic expression",
                "D16": "Authoritative comforts, government luxury, leadership happiness",
                "D20": "Authoritative spirituality, government practices, leadership devotion",
                "D24": "Government education, authoritative learning, leadership knowledge",
                "D30": "Government health issues, authoritative enemies, leadership obstacles",
                "D60": "Authoritative karma, government destiny, leadership soul patterns"
            },
            "Moon": {
                "D2": "Emotional relationship with money, fluctuating income, family wealth",
                "D3": "Emotional communication, nurturing siblings, intuitive courage",
                "D9": "Emotionally nurturing spouse, domestic happiness, caring marriage",
                "D10": "Public-oriented career, emotional connection to work, caring professions",
                "D12": "Strong bond with mother, emotional family ties, nurturing family",
                "D4": "Emotional property, nurturing assets, domestic real estate",
                "D7": "Nurturing children, emotional creativity, caring artistic expression",
                "D16": "Emotional comforts, nurturing luxury, domestic happiness",
                "D20": "Emotional spirituality, nurturing practices, caring devotion",
                "D24": "Emotional learning, nurturing education, caring knowledge",
                "D30": "Emotional health issues, nurturing enemies, caring obstacles",
                "D60": "Emotional karma, nurturing destiny, caring soul patterns"
            },
            "Mars": {
                "D2": "Aggressive earning, real estate wealth, competitive financial approach",
                "D3": "Courageous nature, competitive siblings, assertive communication",
                "D9": "Energetic spouse, passionate marriage, protective partner",
                "D10": "Engineering, military, sports career, competitive professional approach",
                "D12": "Protective family, military family background, assertive parents",
                "D4": "Aggressive property, competitive assets, military real estate",
                "D7": "Energetic children, competitive creativity, assertive artistic expression",
                "D16": "Competitive comforts, aggressive luxury, energetic happiness",
                "D20": "Aggressive spirituality, competitive practices, energetic devotion",
                "D24": "Competitive learning, aggressive education, energetic knowledge",
                "D30": "Aggressive health issues, competitive enemies, energetic obstacles",
                "D60": "Aggressive karma, competitive destiny, energetic soul patterns"
            },
            "Mercury": {
                "D2": "Business acumen, intellectual wealth, communication-based income",
                "D3": "Excellent communication, intelligent siblings, writing abilities",
                "D9": "Intelligent spouse, communicative marriage, business partnerships",
                "D10": "Communication-based career, business, writing, intellectual professions",
                "D12": "Intelligent parents, business family, communicative family environment",
                "D4": "Intelligent property, business assets, communicative real estate",
                "D7": "Intelligent children, communicative creativity, business artistic expression",
                "D16": "Intelligent comforts, business luxury, communicative happiness",
                "D20": "Intelligent spirituality, business practices, communicative devotion",
                "D24": "Excellent learning, intelligent education, business knowledge",
                "D30": "Intelligent health issues, business enemies, communicative obstacles",
                "D60": "Intelligent karma, business destiny, communicative soul patterns"
            },
            "Jupiter": {
                "D2": "Ethical wealth, teaching income, spiritual approach to money",
                "D3": "Wise communication, learned siblings, philosophical courage",
                "D9": "Wise spouse, spiritual marriage, dharmic partnership",
                "D10": "Teaching, law, spiritual career, advisory positions, ethical professions",
                "D12": "Learned parents, spiritual family, traditional family values",
                "D4": "Ethical property, spiritual assets, dharmic real estate",
                "D7": "Wise children, spiritual creativity, dharmic artistic expression",
                "D16": "Ethical comforts, spiritual luxury, dharmic happiness",
                "D20": "Deep spirituality, wise practices, dharmic devotion",
                "D24": "Wise learning, spiritual education, dharmic knowledge",
                "D30": "Spiritual health issues, wise enemies, dharmic obstacles",
                "D60": "Wise karma, spiritual destiny, dharmic soul patterns"
            },
            "Venus": {
                "D2": "Artistic wealth, luxury income, beautiful possessions",
                "D3": "Artistic communication, harmonious siblings, diplomatic speech",
                "D9": "Beautiful spouse, harmonious marriage, artistic partnership",
                "D10": "Artistic career, beauty industry, entertainment, diplomatic professions",
                "D12": "Artistic family, beautiful family environment, harmonious parents",
                "D4": "Beautiful property, artistic assets, harmonious real estate",
                "D7": "Beautiful children, artistic creativity, harmonious artistic expression",
                "D16": "Beautiful comforts, artistic luxury, harmonious happiness",
                "D20": "Artistic spirituality, beautiful practices, harmonious devotion",
                "D24": "Artistic learning, beautiful education, harmonious knowledge",
                "D30": "Artistic health issues, beautiful enemies, harmonious obstacles",
                "D60": "Artistic karma, beautiful destiny, harmonious soul patterns"
            },
            "Saturn": {
                "D2": "Slow but steady wealth, hard-earned money, disciplined finances",
                "D3": "Serious communication, responsible siblings, disciplined courage",
                "D9": "Mature spouse, serious marriage, long-lasting partnership",
                "D10": "Hard work career, slow career growth, disciplined professional approach",
                "D12": "Disciplined family, traditional parents, family responsibilities",
                "D4": "Slow property acquisition, disciplined asset management, traditional real estate",
                "D7": "Delayed children, serious creativity, disciplined artistic expression",
                "D16": "Simple comforts, disciplined luxury, traditional happiness",
                "D20": "Disciplined spirituality, traditional practices, serious devotion",
                "D24": "Slow learning, disciplined education, traditional knowledge",
                "D30": "Chronic health issues, persistent enemies, long-term obstacles",
                "D60": "Heavy karma, disciplined destiny, traditional soul patterns"
            },
            "Rahu": {
                "D2": "Unconventional wealth, foreign income, sudden financial gains",
                "D3": "Unusual communication, foreign siblings, innovative courage",
                "D9": "Foreign spouse, unconventional marriage, cross-cultural partnership",
                "D10": "Technology career, foreign profession, unconventional success",
                "D12": "Foreign family, unconventional parents, mixed heritage",
                "D4": "Foreign property, unconventional assets, technology-based real estate",
                "D7": "Unusual children, innovative creativity, foreign artistic expression",
                "D16": "Foreign comforts, unconventional luxury, modern happiness",
                "D20": "Foreign spirituality, unconventional practices, innovative devotion",
                "D24": "Foreign education, unconventional learning, modern knowledge",
                "D30": "Foreign health issues, hidden enemies, unusual obstacles",
                "D60": "Foreign karma, unconventional destiny, modern soul patterns"
            },
            "Ketu": {
                "D2": "Spiritual wealth, detached finances, past-life money karma",
                "D3": "Spiritual communication, detached siblings, intuitive courage",
                "D9": "Spiritual spouse, detached marriage, karmic partnership",
                "D10": "Spiritual career, detached profession, past-life skills",
                "D12": "Spiritual family, detached parents, karmic heritage",
                "D4": "Spiritual property, detached assets, karmic real estate",
                "D7": "Spiritual children, detached creativity, karmic artistic expression",
                "D16": "Spiritual comforts, detached luxury, inner happiness",
                "D20": "Deep spirituality, mystical practices, transcendent devotion",
                "D24": "Intuitive learning, spiritual education, mystical knowledge",
                "D30": "Karmic health issues, spiritual enemies, mystical obstacles",
                "D60": "Deep karma, spiritual destiny, transcendent soul patterns"
            }
        }

    def analyze_comprehensive_divisional_charts(self, main_chart: VedicChart, divisional_charts: Dict) -> Dict[str, Any]:
        """Provide comprehensive analysis of all divisional charts."""
        comprehensive_analysis = {}

        for division, chart_data in divisional_charts.items():
            if division in self.divisional_meanings:
                comprehensive_analysis[division] = self._analyze_single_divisional_chart(
                    division, chart_data, main_chart
                )

        return comprehensive_analysis

    def _analyze_single_divisional_chart(self, division: str, chart_data: Dict, main_chart: VedicChart) -> Dict[str, Any]:
        """Analyze a single divisional chart comprehensively."""
        division_info = self.divisional_meanings[division]

        analysis = {
            "name": division_info["name"],
            "primary_significance": division_info["primary_significance"],
            "detailed_areas": division_info["detailed_areas"],
            "planetary_analysis": [],
            "overall_strength": self._calculate_divisional_strength(chart_data),
            "key_insights": [],
            "practical_guidance": [],
            "specific_predictions": []
        }

        # Analyze each planet in the divisional chart INCLUDING RAHU/KETU
        planetary_positions = chart_data.get("planetary_positions", {})
        for planet_name, planet_info in planetary_positions.items():
            # Include ALL planets including Rahu and Ketu for comprehensive analysis

            planet_analysis = self._analyze_planet_in_division(
                planet_name, planet_info, division, division_info, main_chart
            )
            analysis["planetary_analysis"].append(planet_analysis)

        # Generate key insights and guidance
        analysis["key_insights"] = self._generate_divisional_insights(division, chart_data, division_info)
        analysis["practical_guidance"] = self._generate_practical_guidance(division, chart_data, division_info)
        analysis["specific_predictions"] = self._generate_specific_predictions(division, chart_data, division_info)

        return analysis

    def _analyze_planet_in_division(self, planet_name: str, planet_info: Dict, division: str, division_info: Dict, main_chart: VedicChart) -> Dict[str, Any]:
        """Analyze a specific planet in a divisional chart."""
        divisional_sign = planet_info.get("divisional_sign", "Unknown")
        original_sign = planet_info.get("original_sign", "Unknown")
        significance = planet_info.get("significance", "Moderate")

        # Calculate house position (simplified - using sign number as house for now)
        house = self._get_sign_number(divisional_sign)

        analysis = {
            "planet": planet_name,
            "position": f"{divisional_sign} in House {house}",
            "strength_assessment": self._extract_strength_from_significance(significance),
            "specific_effects": "",
            "life_impact": "",
            "recommendations": []
        }

        # Get planet-specific effects for this division
        if planet_name in self.planetary_effects and division in self.planetary_effects[planet_name]:
            analysis["specific_effects"] = self.planetary_effects[planet_name][division]

        # Get house-specific effects
        if "house_effects" in division_info and house in division_info["house_effects"]:
            analysis["life_impact"] = division_info["house_effects"][house]

        # Generate recommendations based on strength
        analysis["recommendations"] = self._generate_planet_recommendations(
            planet_name, planet_info, division
        )

        return analysis

    def _get_sign_number(self, sign_name: str) -> int:
        """Convert sign name to number (1-12)."""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        try:
            return signs.index(sign_name) + 1
        except ValueError:
            return 1

    def _extract_strength_from_significance(self, significance: str) -> str:
        """Extract strength assessment from significance text."""
        if "Very strong" in significance or "Excellent" in significance:
            return "Very Strong"
        elif "Good" in significance:
            return "Good"
        elif "Challenging" in significance or "Weak" in significance:
            return "Challenging"
        else:
            return "Moderate"

    def _calculate_divisional_strength(self, chart_data: Dict) -> str:
        """Calculate overall strength of divisional chart."""
        strong_count = 0
        total_count = 0

        planetary_positions = chart_data.get("planetary_positions", {})
        for planet_name, planet_info in planetary_positions.items():
            # Include ALL planets including Rahu and Ketu for strength calculation
            total_count += 1
            significance = planet_info.get("significance", "")
            if "Very strong" in significance or "Excellent" in significance:
                strong_count += 1

        if total_count == 0:
            return "Moderate"

        strength_ratio = strong_count / total_count
        if strength_ratio >= 0.6:
            return "Very Strong"
        elif strength_ratio >= 0.4:
            return "Strong"
        elif strength_ratio >= 0.2:
            return "Moderate"
        else:
            return "Needs Attention"

    def _generate_divisional_insights(self, division: str, chart_data: Dict, division_info: Dict) -> List[str]:
        """Generate key insights for the divisional chart."""
        insights = []

        # Add division-specific insights based on planetary positions
        strong_planets = []
        weak_planets = []

        planetary_positions = chart_data.get("planetary_positions", {})
        for planet_name, planet_info in planetary_positions.items():
            # Include ALL planets including Rahu and Ketu for insights
            significance = planet_info.get("significance", "")
            if "Very strong" in significance or "Excellent" in significance:
                strong_planets.append(planet_name)
            elif "Weak" in significance or "Challenging" in significance:
                weak_planets.append(planet_name)

        if strong_planets:
            insights.append(f"Strong {division_info['primary_significance'].lower()} due to well-placed {', '.join(strong_planets)}")

        if weak_planets:
            insights.append(f"Challenges in {division_info['primary_significance'].lower()} due to weak {', '.join(weak_planets)}")

        return insights

    def _generate_practical_guidance(self, division: str, chart_data: Dict, division_info: Dict) -> List[str]:
        """Generate practical guidance based on divisional chart."""
        guidance = []

        division_guidance = {
            "D2": [
                "Focus on building multiple income streams",
                "Develop a disciplined approach to saving and investing",
                "Avoid impulsive financial decisions"
            ],
            "D3": [
                "Strengthen communication skills through practice",
                "Maintain good relationships with siblings and neighbors",
                "Develop courage through gradual challenges"
            ],
            "D9": [
                "Focus on spiritual growth for marital harmony",
                "Develop patience and understanding in relationships",
                "Seek compatibility in values and life goals"
            ],
            "D10": [
                "Develop professional skills continuously",
                "Build a strong professional network",
                "Maintain ethical standards in career"
            ],
            "D12": [
                "Honor and respect your parents and ancestors",
                "Maintain family traditions and values",
                "Seek parental blessings for important decisions"
            ],
            "D4": [
                "Invest wisely in real estate and property",
                "Maintain and protect your fixed assets",
                "Plan for long-term material security"
            ],
            "D7": [
                "Nurture your creative abilities and talents",
                "Maintain good relationships with children",
                "Express creativity in constructive ways"
            ],
            "D16": [
                "Appreciate and maintain your comforts responsibly",
                "Share your happiness and luxuries with others",
                "Avoid excessive materialism"
            ],
            "D20": [
                "Develop regular spiritual practices",
                "Study religious and philosophical texts",
                "Seek guidance from spiritual teachers"
            ],
            "D24": [
                "Pursue continuous learning and education",
                "Share your knowledge with others",
                "Develop both practical and theoretical understanding"
            ],
            "D30": [
                "Maintain good health through preventive care",
                "Resolve conflicts peacefully",
                "Practice patience during difficult periods"
            ],
            "D60": [
                "Accept your karmic patterns with wisdom",
                "Work on spiritual evolution and growth",
                "Practice selfless service and compassion"
            ]
        }

        if division in division_guidance:
            guidance.extend(division_guidance[division])

        return guidance

    def _generate_specific_predictions(self, division: str, chart_data: Dict, division_info: Dict) -> List[str]:
        """Generate specific predictions based on divisional chart."""
        predictions = []

        # Add division-specific predictions based on overall strength
        overall_strength = self._calculate_divisional_strength(chart_data)

        division_predictions = {
            "D2": {
                "Very Strong": "Excellent wealth accumulation potential, multiple income sources",
                "Strong": "Good financial stability, steady income growth",
                "Moderate": "Average financial situation, requires careful planning",
                "Needs Attention": "Financial challenges, need for disciplined money management"
            },
            "D3": {
                "Very Strong": "Excellent communication skills, strong sibling support",
                "Strong": "Good courage and initiative, supportive siblings",
                "Moderate": "Average communication abilities, normal sibling relationships",
                "Needs Attention": "Communication challenges, potential sibling conflicts"
            },
            "D9": {
                "Very Strong": "Excellent marriage prospects, spiritual growth through partnership",
                "Strong": "Good marital harmony, supportive spouse",
                "Moderate": "Average marriage, requires effort for harmony",
                "Needs Attention": "Marriage challenges, need for spiritual development"
            },
            "D10": {
                "Very Strong": "Excellent career prospects, high professional achievements",
                "Strong": "Good career growth, professional recognition",
                "Moderate": "Average career progress, steady professional development",
                "Needs Attention": "Career challenges, need for skill development"
            },
            "D12": {
                "Very Strong": "Excellent family support, strong ancestral blessings",
                "Strong": "Good family relationships, parental support",
                "Moderate": "Average family dynamics, normal parental relationships",
                "Needs Attention": "Family challenges, need for ancestral healing"
            },
            "D4": {
                "Very Strong": "Excellent property acquisition, multiple real estate assets",
                "Strong": "Good property ownership, stable material assets",
                "Moderate": "Average property situation, requires careful planning",
                "Needs Attention": "Property challenges, need for asset management"
            },
            "D7": {
                "Very Strong": "Excellent creative abilities, blessed with talented children",
                "Strong": "Good creativity, supportive children",
                "Moderate": "Average creative expression, normal children relationships",
                "Needs Attention": "Creative blocks, challenges with children"
            },
            "D16": {
                "Very Strong": "Excellent comforts and luxuries, high happiness levels",
                "Strong": "Good material comforts, satisfying lifestyle",
                "Moderate": "Average comfort levels, requires effort for happiness",
                "Needs Attention": "Comfort challenges, need for lifestyle improvement"
            },
            "D20": {
                "Very Strong": "Excellent spiritual growth, deep religious connection",
                "Strong": "Good spiritual practices, meaningful devotion",
                "Moderate": "Average spiritual development, requires effort",
                "Needs Attention": "Spiritual challenges, need for religious guidance"
            },
            "D24": {
                "Very Strong": "Excellent learning abilities, high educational achievements",
                "Strong": "Good knowledge acquisition, successful education",
                "Moderate": "Average learning capacity, requires effort",
                "Needs Attention": "Learning challenges, need for educational support"
            },
            "D30": {
                "Very Strong": "Excellent health, minimal obstacles and enemies",
                "Strong": "Good health management, manageable challenges",
                "Moderate": "Average health, normal life obstacles",
                "Needs Attention": "Health challenges, significant obstacles to overcome"
            },
            "D60": {
                "Very Strong": "Excellent karmic patterns, favorable destiny",
                "Strong": "Good karmic balance, positive life direction",
                "Moderate": "Average karmic situation, requires spiritual effort",
                "Needs Attention": "Challenging karma, need for spiritual transformation"
            }
        }

        if division in division_predictions and overall_strength in division_predictions[division]:
            predictions.append(division_predictions[division][overall_strength])

        return predictions

    def _generate_planet_recommendations(self, planet_name: str, planet_info: Dict, division: str) -> List[str]:
        """Generate recommendations for specific planet in divisional chart."""
        recommendations = []
        significance = planet_info.get("significance", "")

        if "Weak" in significance or "Challenging" in significance:
            planet_remedies = {
                "Sun": "Offer water to Sun at sunrise, practice leadership qualities",
                "Moon": "Practice meditation, maintain emotional balance",
                "Mars": "Practice physical exercise, develop patience",
                "Mercury": "Improve communication skills, practice writing",
                "Jupiter": "Study spiritual texts, practice charity",
                "Venus": "Appreciate arts and beauty, practice harmony",
                "Saturn": "Practice discipline, serve the elderly"
            }

            if planet_name in planet_remedies:
                recommendations.append(planet_remedies[planet_name])

        return recommendations
