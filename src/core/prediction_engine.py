import requests
from typing import List, Dict, Any, Tuple
from datetime import date, datetime, timedelta
import json
import swisseph as swe
from enum import Enum

from src.models.models import VedicChart, DashaPeriod, VedicPrediction, BirthData, LocationData, CurrentInfluences
from config.config import config
from src.core.vedic_analysis import VedicAnalyzer
from src.utils.date_calculator import AstrologicalDateCalculator
from src.core.current_influences import CurrentInfluenceAnalyzer

# Import OpenAI only if needed
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI library not installed. OpenAI provider will not be available.")

class LLMProvider(Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    OLLAMA = "ollama"
    FALLBACK = "fallback"

class VedicPredictionEngine:
    def __init__(self, llm_provider: str = None):
        """
        Initialize prediction engine with configurable LLM provider.

        Args:
            llm_provider: Override config LLM provider ("openai", "ollama", "fallback")
        """
        # Determine LLM provider
        self.llm_provider = LLMProvider(llm_provider or config.LLM_PROVIDER)

        # Initialize LLM clients based on provider
        self.openai_client = None
        self.ollama_available = False

        if self.llm_provider == LLMProvider.OPENAI:
            self._init_openai()
        elif self.llm_provider == LLMProvider.OLLAMA:
            self._init_ollama()
        else:
            print(f"🔄 Using fallback predictions (no LLM)")

        # Initialize analysis modules
        self.analyzer = VedicAnalyzer()
        self.date_calculator = AstrologicalDateCalculator()
        self.current_influence_analyzer = CurrentInfluenceAnalyzer()

    def _init_openai(self):
        """Initialize OpenAI client."""
        if not OPENAI_AVAILABLE:
            print("❌ OpenAI library not installed. Falling back to local predictions.")
            self.llm_provider = LLMProvider.FALLBACK
            return

        if not config.OPENAI_API_KEY:
            print("❌ OpenAI API key not found. Falling back to local predictions.")
            self.llm_provider = LLMProvider.FALLBACK
            return

        try:
            self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
            print(f"✅ OpenAI initialized with model: {config.OPENAI_MODEL}")
        except Exception as e:
            print(f"❌ OpenAI initialization failed: {e}. Falling back to local predictions.")
            self.llm_provider = LLMProvider.FALLBACK

    def _init_ollama(self):
        """Initialize Ollama client."""
        self.ollama_available = self._check_ollama_availability()
        if self.ollama_available:
            print(f"✅ Ollama available at {config.OLLAMA_URL} with model: {config.OLLAMA_MODEL}")
        else:
            print("❌ Ollama not available. Falling back to local predictions.")
            self.llm_provider = LLMProvider.FALLBACK

    def _check_ollama_availability(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Ollama not available: {e}")
            return False

    def generate_vedic_prediction(self, birth_data: BirthData, chart: VedicChart, current_dasha: DashaPeriod, location_data: LocationData = None) -> VedicPrediction:
        """
        Generate comprehensive Vedic astrology prediction using enhanced analysis.
        """
        # Get comprehensive dasha analysis
        dasha_analysis = self.analyzer.analyze_dasha_significance(current_dasha, chart)

        # Get planetary relationships analysis
        planetary_relationships = self.analyzer.analyze_planetary_relationships(chart)

        # Get current transits with detailed analysis
        if location_data:
            current_transits = self.analyzer.get_current_transits(birth_data, location_data)
        else:
            current_transits = self._get_current_transits()

        # Get current day/month influences and personal effects
        current_influences = None
        if location_data:
            current_influences = self.current_influence_analyzer.analyze_current_influences(birth_data, chart, location_data)

        # Calculate specific favorable and challenging periods with dates
        favorable_periods = self.date_calculator.calculate_favorable_periods(current_dasha, birth_data)
        challenging_periods = self.date_calculator.calculate_challenging_periods(current_dasha, birth_data)

        # Prepare comprehensive chart data for LLM
        chart_summary = self._prepare_comprehensive_chart_summary(
            chart, current_dasha, dasha_analysis, planetary_relationships, current_transits
        )

        # Generate enhanced prediction using LLM
        prediction_text = self._generate_enhanced_llm_prediction(birth_data, chart_summary, dasha_analysis)

        # Extract enhanced key themes
        key_themes = self._extract_enhanced_key_themes(chart, current_dasha, dasha_analysis)

        # Calculate upcoming dasha with detailed transition info
        upcoming_dasha = self._calculate_upcoming_dasha(current_dasha)

        # Format periods for display
        formatted_favorable = self._format_periods_for_display(favorable_periods)
        formatted_challenging = self._format_periods_for_display(challenging_periods)
        formatted_transits = self._format_transits_for_display(current_transits)

        # Format current influences for display
        formatted_current_influences = None
        if current_influences:
            formatted_current_influences = CurrentInfluences(
                current_date=current_influences["current_date"],
                lunar_phase=current_influences["lunar_phase"],
                month_theme=current_influences["month_theme"],
                daily_changes=current_influences["daily_changes"],
                monthly_changes=current_influences["monthly_changes"],
                personal_effects=current_influences["personal_effects"],
                recommendations=current_influences["recommendations"]
            )

        return VedicPrediction(
            current_dasha=current_dasha,
            upcoming_dasha=upcoming_dasha,
            current_transits=formatted_transits,
            prediction_text=prediction_text,
            key_themes=key_themes,
            favorable_periods=formatted_favorable,
            challenging_periods=formatted_challenging,
            current_influences=formatted_current_influences
        )

    def _prepare_chart_summary(self, chart: VedicChart, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """
        Prepare a structured summary of the chart for LLM processing.
        """
        return {
            "ascendant_sign": chart.ascendant_sign,
            "moon_sign": chart.moon_sign,
            "sun_sign": chart.sun_sign,
            "birth_nakshatra": chart.birth_nakshatra,
            "current_dasha": {
                "planet": current_dasha.planet,
                "remaining_years": round(current_dasha.remaining_years, 1)
            },
            "planetary_positions": [
                {
                    "planet": planet.name,
                    "sign": planet.sign,
                    "house": planet.house
                }
                for planet in chart.planets
            ],
            "house_occupancy": {
                str(house): planets for house, planets in chart.houses.items() if planets
            }
        }

    def _generate_llm_prediction(self, birth_data: BirthData, chart_summary: Dict[str, Any]) -> str:
        """Generate prediction text using configured LLM provider."""
        if self.llm_provider == LLMProvider.OPENAI:
            return self._generate_openai_prediction(birth_data, chart_summary)
        elif self.llm_provider == LLMProvider.OLLAMA:
            return self._generate_ollama_prediction(birth_data, chart_summary)
        else:
            return self._generate_fallback_prediction(chart_summary)

    def _generate_openai_prediction(self, birth_data: BirthData, chart_summary: Dict[str, Any]) -> str:
        """Generate prediction using OpenAI."""
        if not self.openai_client:
            return self._generate_fallback_prediction(chart_summary)

        try:
            prompt = self._create_prediction_prompt(birth_data, chart_summary)
            print(f"🔮 Generating prediction using OpenAI ({config.OPENAI_MODEL})...")

            response = self.openai_client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Vedic astrologer with deep knowledge of Jyotish. Provide insightful, practical predictions based on the birth chart data provided. Focus on current life themes, opportunities, and guidance."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=config.OPENAI_MAX_TOKENS,
                temperature=config.OPENAI_TEMPERATURE,
                timeout=config.OPENAI_TIMEOUT
            )

            prediction_text = response.choices[0].message.content.strip()
            print(f"✅ OpenAI prediction generated successfully ({len(prediction_text)} characters)")
            return prediction_text

        except Exception as e:
            print(f"❌ Error generating OpenAI prediction: {e}")
            return self._generate_fallback_prediction(chart_summary)

    def _generate_ollama_prediction(self, birth_data: BirthData, chart_summary: Dict[str, Any]) -> str:
        """Generate prediction using Ollama."""
        if not self.ollama_available:
            return self._generate_fallback_prediction(chart_summary)

        try:
            prompt = self._create_prediction_prompt(birth_data, chart_summary)
            print(f"🔮 Generating prediction using Ollama ({config.OLLAMA_MODEL})...")

            # Add system context to the prompt
            full_prompt = f"""You are an expert Vedic astrologer with deep knowledge of Jyotish. Provide insightful, practical predictions based on the birth chart data provided. Focus on current life themes, opportunities, and guidance.

{prompt}"""

            response = requests.post(
                config.OLLAMA_URL,
                json={
                    "model": config.OLLAMA_MODEL,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=config.OLLAMA_TIMEOUT
            )

            if response.status_code == 200:
                result = response.json()
                prediction_text = result.get("response", "").strip()
                print(f"✅ Ollama prediction generated successfully ({len(prediction_text)} characters)")
                return prediction_text
            else:
                print(f"❌ Ollama API error: {response.status_code}")
                return self._generate_fallback_prediction(chart_summary)

        except Exception as e:
            print(f"❌ Error generating Ollama prediction: {e}")
            return self._generate_fallback_prediction(chart_summary)

    def _create_prediction_prompt(self, birth_data: BirthData, chart_summary: Dict[str, Any]) -> str:
        """
        Create a detailed prompt for the LLM based on chart data.
        """
        current_date = date.today()
        age = current_date.year - birth_data.birth_date.year

        prompt = f"""
        Please provide a comprehensive Vedic astrology prediction for {birth_data.name}, age {age}.

        Birth Chart Summary:
        - Ascendant (Lagna): {chart_summary['ascendant_sign']}
        - Moon Sign (Rashi): {chart_summary['moon_sign']}
        - Sun Sign: {chart_summary['sun_sign']}
        - Birth Nakshatra: {chart_summary['birth_nakshatra']}

        Current Dasha Period:
        - Planet: {chart_summary['current_dasha']['planet']}
        - Remaining Years: {chart_summary['current_dasha']['remaining_years']}

        Planetary Positions:
        {self._format_planetary_positions(chart_summary['planetary_positions'])}

        House Occupancy:
        {self._format_house_occupancy(chart_summary['house_occupancy'])}

        Please provide:
        1. Current life phase analysis based on the dasha period
        2. Key themes and opportunities in the coming months
        3. Areas of life to focus on (career, relationships, health, spirituality)
        4. Practical guidance and recommendations
        5. Timing considerations for important decisions

        Keep the prediction practical, positive, and actionable while being authentic to Vedic astrological principles.
        """

        return prompt

    def _format_planetary_positions(self, positions: List[Dict]) -> str:
        """Format planetary positions for the prompt."""
        formatted = []
        for pos in positions:
            formatted.append(f"- {pos['planet']}: {pos['sign']} (House {pos['house']})")
        return "\n".join(formatted)

    def _format_house_occupancy(self, houses: Dict[str, List[str]]) -> str:
        """Format house occupancy for the prompt."""
        formatted = []
        for house, planets in houses.items():
            planets_str = ", ".join(planets)
            formatted.append(f"- House {house}: {planets_str}")
        return "\n".join(formatted)

    def _generate_fallback_prediction(self, chart_summary: Dict[str, Any]) -> str:
        """
        Generate a basic prediction when LLM is not available.
        """
        dasha_planet = chart_summary['current_dasha']['planet']
        moon_sign = chart_summary['moon_sign']
        ascendant = chart_summary['ascendant_sign']

        dasha_meanings = {
            "Sun": "a period of leadership, authority, and self-expression. Focus on career advancement and personal recognition.",
            "Moon": "a time of emotional growth, intuition, and nurturing relationships. Pay attention to family and inner well-being.",
            "Mars": "an energetic phase favoring action, courage, and new initiatives. Good for sports, competition, and overcoming obstacles.",
            "Mercury": "a period emphasizing communication, learning, and intellectual pursuits. Favorable for education and business.",
            "Jupiter": "a highly auspicious time for wisdom, spirituality, and expansion. Excellent for teaching, learning, and growth.",
            "Venus": "a period of creativity, relationships, and material pleasures. Focus on arts, beauty, and partnerships.",
            "Saturn": "a time of discipline, hard work, and karmic lessons. Patience and perseverance will bring long-term rewards.",
            "Rahu": "a period of ambition, innovation, and unconventional approaches. Be mindful of illusions and stay grounded.",
            "Ketu": "a spiritual phase emphasizing detachment and inner growth. Good for meditation and letting go of material attachments."
        }

        prediction = f"""
        Based on your Vedic birth chart analysis:

        Current Life Phase:
        You are currently in the {dasha_planet} Mahadasha, which represents {dasha_meanings.get(dasha_planet, 'a significant period of growth and learning')}.

        Key Insights:
        - Your Moon sign {moon_sign} indicates your emotional nature and mental tendencies
        - Your {ascendant} ascendant shapes your personality and life approach
        - The current {dasha_planet} period will influence your experiences for the next {chart_summary['current_dasha']['remaining_years']} years

        Recommendations:
        1. Align your actions with the energy of {dasha_planet}
        2. Pay attention to the houses and signs where your planets are placed
        3. Use this time for personal growth and spiritual development
        4. Maintain balance between material and spiritual pursuits

        This is a general interpretation. For detailed analysis, consult with a qualified Vedic astrologer.
        """

        return prediction.strip()

    def _prepare_comprehensive_chart_summary(self, chart: VedicChart, current_dasha: DashaPeriod,
                                           dasha_analysis: Dict[str, Any], planetary_relationships: Dict[str, Any],
                                           current_transits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare comprehensive chart summary with detailed analysis."""
        return {
            "basic_info": {
                "ascendant_sign": chart.ascendant_sign,
                "moon_sign": chart.moon_sign,
                "sun_sign": chart.sun_sign,
                "birth_nakshatra": chart.birth_nakshatra
            },
            "current_dasha": {
                "planet": current_dasha.planet,
                "remaining_years": round(current_dasha.remaining_years, 1),
                "nature": dasha_analysis.get("planet_nature", ""),
                "themes": dasha_analysis.get("key_themes", []),
                "guidance": dasha_analysis.get("guidance", ""),
                "cautions": dasha_analysis.get("cautions", "")
            },
            "planetary_positions": [
                {
                    "planet": planet.name,
                    "sign": planet.sign,
                    "house": planet.house,
                    "nakshatra": planet.nakshatra
                }
                for planet in chart.planets
            ],
            "planetary_relationships": planetary_relationships,
            "current_transits": current_transits,
            "house_occupancy": {
                str(house): planets for house, planets in chart.houses.items() if planets
            }
        }

    def _generate_enhanced_llm_prediction(self, birth_data: BirthData, chart_summary: Dict[str, Any],
                                        dasha_analysis: Dict[str, Any]) -> str:
        """Generate enhanced prediction with detailed analysis using configured LLM provider."""
        if self.llm_provider == LLMProvider.OPENAI:
            return self._generate_enhanced_openai_prediction(birth_data, chart_summary, dasha_analysis)
        elif self.llm_provider == LLMProvider.OLLAMA:
            return self._generate_enhanced_ollama_prediction(birth_data, chart_summary, dasha_analysis)
        else:
            return self._generate_enhanced_fallback_prediction(chart_summary, dasha_analysis)

    def _generate_enhanced_openai_prediction(self, birth_data: BirthData, chart_summary: Dict[str, Any],
                                           dasha_analysis: Dict[str, Any]) -> str:
        """Generate enhanced prediction using OpenAI."""
        if not self.openai_client:
            return self._generate_enhanced_fallback_prediction(chart_summary, dasha_analysis)

        try:
            prompt = self._create_enhanced_prediction_prompt(birth_data, chart_summary, dasha_analysis)
            print(f"🔮 Generating enhanced prediction using OpenAI ({config.OPENAI_MODEL})...")

            response = self.openai_client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a master Vedic astrologer with deep knowledge of Jyotish, planetary relationships, and dasha systems. Provide detailed, practical predictions with specific guidance and explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=config.OPENAI_MAX_TOKENS * 2,  # More tokens for detailed analysis
                temperature=config.OPENAI_TEMPERATURE,
                timeout=config.OPENAI_TIMEOUT
            )

            prediction_text = response.choices[0].message.content.strip()
            print(f"✅ OpenAI enhanced prediction generated successfully ({len(prediction_text)} characters)")
            return prediction_text

        except Exception as e:
            print(f"❌ Error generating enhanced OpenAI prediction: {e}")
            return self._generate_enhanced_fallback_prediction(chart_summary, dasha_analysis)

    def _generate_enhanced_ollama_prediction(self, birth_data: BirthData, chart_summary: Dict[str, Any],
                                           dasha_analysis: Dict[str, Any]) -> str:
        """Generate enhanced prediction using Ollama."""
        if not self.ollama_available:
            return self._generate_enhanced_fallback_prediction(chart_summary, dasha_analysis)

        try:
            prompt = self._create_enhanced_prediction_prompt(birth_data, chart_summary, dasha_analysis)
            print(f"🔮 Generating enhanced prediction using Ollama ({config.OLLAMA_MODEL})...")

            # Add system context to the prompt
            full_prompt = f"""You are a master Vedic astrologer with deep knowledge of Jyotish, planetary relationships, and dasha systems. Provide detailed, practical predictions with specific guidance and explanations.

{prompt}"""

            response = requests.post(
                config.OLLAMA_URL,
                json={
                    "model": config.OLLAMA_MODEL,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=config.OLLAMA_TIMEOUT
            )

            if response.status_code == 200:
                result = response.json()
                prediction_text = result.get("response", "").strip()
                print(f"✅ Ollama enhanced prediction generated successfully ({len(prediction_text)} characters)")
                return prediction_text
            else:
                print(f"❌ Ollama API error: {response.status_code}")
                return self._generate_enhanced_fallback_prediction(chart_summary, dasha_analysis)

        except Exception as e:
            print(f"❌ Error generating enhanced Ollama prediction: {e}")
            return self._generate_enhanced_fallback_prediction(chart_summary, dasha_analysis)

    def _create_enhanced_prediction_prompt(self, birth_data: BirthData, chart_summary: Dict[str, Any],
                                         dasha_analysis: Dict[str, Any]) -> str:
        """Create detailed prompt for enhanced prediction."""
        current_date = date.today()
        age = current_date.year - birth_data.birth_date.year

        prompt = f"""
        Provide a comprehensive Vedic astrology analysis for {birth_data.name}, age {age}.

        BIRTH CHART DETAILS:
        - Ascendant: {chart_summary['basic_info']['ascendant_sign']}
        - Moon Sign: {chart_summary['basic_info']['moon_sign']}
        - Sun Sign: {chart_summary['basic_info']['sun_sign']}
        - Birth Nakshatra: {chart_summary['basic_info']['birth_nakshatra']}

        CURRENT DASHA ANALYSIS:
        - Planet: {chart_summary['current_dasha']['planet']} ({chart_summary['current_dasha']['remaining_years']} years remaining)
        - Nature: {chart_summary['current_dasha']['nature']}
        - Key Themes: {', '.join(chart_summary['current_dasha']['themes'])}

        PLANETARY POSITIONS:
        {self._format_planetary_positions_detailed(chart_summary['planetary_positions'])}

        PLANETARY RELATIONSHIPS:
        {self._format_planetary_relationships(chart_summary['planetary_relationships'])}

        Please provide a detailed analysis with proper formatting using the following structure:

        🌟 CURRENT DASHA SIGNIFICANCE:
        What does the current {chart_summary['current_dasha']['planet']} dasha mean for this person? How is this period influencing their life themes and experiences? What opportunities and challenges does this period bring?

        🎯 PLANETARY RELATIONSHIPS & THEIR IMPACT:
        How do the planetary positions and relationships affect the person? What are the key yogas and their significance? How do conjunctions and aspects influence life areas?

        💡 SPECIFIC GUIDANCE FOR CURRENT PERIOD:
        What should they focus on during this dasha? What actions will bring the best results? What practices or remedies would be beneficial?

        ⚠️ CAUTIONS AND AREAS TO WATCH:
        What challenges or obstacles should they be aware of? What areas of life need extra attention? What should they avoid during this period?

        🔮 TIMING AND OPPORTUNITIES:
        When are the most favorable periods within this dasha? What types of activities are best suited for different times? How can they make the most of upcoming opportunities?

        FORMATTING REQUIREMENTS:
        - Use the emoji headers exactly as shown above
        - Separate each section with a blank line
        - Write in clear, readable paragraphs
        - Make the analysis practical, specific, and actionable while maintaining authenticity to Vedic principles
        """

        return prompt

    def _generate_enhanced_fallback_prediction(self, chart_summary: Dict[str, Any], dasha_analysis: Dict[str, Any]) -> str:
        """Generate enhanced fallback prediction when LLM is not available."""
        dasha_planet = chart_summary['current_dasha']['planet']
        remaining_years = chart_summary['current_dasha']['remaining_years']

        prediction = f"""
        COMPREHENSIVE VEDIC ASTROLOGY ANALYSIS

        🌟 CURRENT DASHA SIGNIFICANCE:
        You are in the {dasha_planet} Mahadasha with {remaining_years} years remaining. {dasha_analysis.get('significance', '')}

        The {dasha_planet} period is characterized by: {dasha_analysis.get('planet_nature', '')}

        Key themes during this period include: {', '.join(dasha_analysis.get('key_themes', []))}

        🎯 SPECIFIC GUIDANCE FOR THIS PERIOD:
        {dasha_analysis.get('guidance', 'Focus on aligning with the planetary energy and themes.')}

        ⚠️ CAUTIONS AND AREAS TO WATCH:
        {dasha_analysis.get('cautions', 'Be mindful of the challenges associated with this planetary period.')}

        🏠 HOUSE AND SIGN INFLUENCES:
        {dasha_analysis.get('house_influence', '')}
        {dasha_analysis.get('sign_influence', '')}

        📅 TIMING CONSIDERATIONS:
        - Current period: {dasha_planet} Mahadasha ({remaining_years} years remaining)
        - This is a significant life phase that will shape your experiences and growth
        - Different sub-periods (antardashas) within this time will bring varying influences

        🔮 PLANETARY RELATIONSHIPS:
        Your birth chart shows specific planetary combinations that influence how this dasha period manifests in your life. The relationships between planets create unique opportunities and challenges.

        💫 RECOMMENDATIONS:
        1. Align your actions with {dasha_planet}'s natural themes and characteristics
        2. Use this period for growth in areas ruled by {dasha_planet}
        3. Practice patience and work with the natural timing of planetary cycles
        4. Consider appropriate remedial measures if facing challenges

        This analysis provides a foundation for understanding your current astrological period. For personalized guidance, consider consulting with a qualified Vedic astrologer.
        """

        return prediction.strip()

    def _extract_enhanced_key_themes(self, chart: VedicChart, current_dasha: DashaPeriod, dasha_analysis: Dict[str, Any]) -> List[str]:
        """Extract enhanced key life themes based on comprehensive analysis."""
        themes = []

        # Add themes from dasha analysis
        themes.extend(dasha_analysis.get('key_themes', []))

        # Add themes based on chart patterns
        themes.append(f"{chart.moon_sign} Moon influence")
        themes.append(f"{chart.ascendant_sign} Rising energy")

        # Add current period theme
        themes.append(f"Current {current_dasha.planet} period focus")

        return themes[:6]  # Return top 6 themes

    def _format_periods_for_display(self, periods: List[Dict[str, Any]]) -> List[str]:
        """Format periods for display in the UI."""
        formatted = []
        for period in periods[:5]:  # Show top 5 periods
            start_date = period.get('start_date', '')
            end_date = period.get('end_date', '')
            period_name = period.get('period', '')
            description = period.get('description', '')

            if start_date and end_date:
                date_range = f"{start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}"
                formatted.append(f"{period_name} ({date_range}): {description}")
            else:
                formatted.append(f"{period_name}: {description}")

        return formatted

    def _format_transits_for_display(self, transits: List[Dict[str, Any]]) -> List[str]:
        """Format current transits for display."""
        if isinstance(transits, list) and len(transits) > 0 and isinstance(transits[0], dict):
            formatted = []
            for transit in transits:
                planet = transit.get('planet', '')
                sign = transit.get('current_sign', '')
                effect = transit.get('effect', '')
                formatted.append(f"{planet} in {sign}: {effect}")
            return formatted
        else:
            # Fallback for simple string list
            return transits if isinstance(transits, list) else ["Current planetary influences active"]

    def _format_planetary_positions_detailed(self, positions: List[Dict]) -> str:
        """Format planetary positions with detailed information."""
        formatted = []
        for pos in positions:
            planet = pos['planet']
            sign = pos['sign']
            house = pos['house']
            nakshatra = pos.get('nakshatra', '')

            line = f"- {planet}: {sign} (House {house})"
            if nakshatra:
                line += f" in {nakshatra}"
            formatted.append(line)

        return "\n".join(formatted)

    def _format_planetary_relationships(self, relationships: Dict[str, Any]) -> str:
        """Format planetary relationships for the prompt."""
        formatted = []

        # Format conjunctions
        conjunctions = relationships.get('conjunctions', [])
        if conjunctions:
            formatted.append("Conjunctions:")
            for conj in conjunctions:
                planets = ', '.join(conj['planets'])
                sign = conj['sign']
                meaning = conj['meaning']
                formatted.append(f"  - {planets} in {sign}: {meaning}")

        # Format yogas
        yogas = relationships.get('yogas', [])
        if yogas:
            formatted.append("Important Yogas:")
            for yoga in yogas:
                name = yoga['name']
                description = yoga['description']
                formatted.append(f"  - {name}: {description}")

        return "\n".join(formatted) if formatted else "No significant planetary combinations found."

    def _identify_favorable_periods(self, current_dasha: DashaPeriod) -> List[str]:
        """Identify favorable time periods."""
        return [
            f"Remaining {current_dasha.planet} Dasha period",
            "Next 3-6 months for new initiatives",
            "Upcoming festival seasons"
        ]

    def _identify_challenging_periods(self, current_dasha: DashaPeriod) -> List[str]:
        """Identify potentially challenging periods."""
        challenging_planets = ["Saturn", "Rahu", "Ketu", "Mars"]

        if current_dasha.planet in challenging_planets:
            return [
                f"Current {current_dasha.planet} period requires patience",
                "Avoid major decisions during eclipse periods",
                "Be cautious during retrograde periods"
            ]
        else:
            return [
                "Eclipse periods",
                "Mercury retrograde phases",
                "Saturn transit periods"
            ]

    def _calculate_upcoming_dasha(self, current_dasha: DashaPeriod) -> DashaPeriod:
        """Calculate the next dasha period (simplified)."""
        dasha_sequence = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        dasha_periods = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}

        current_index = dasha_sequence.index(current_dasha.planet)
        next_index = (current_index + 1) % len(dasha_sequence)
        next_planet = dasha_sequence[next_index]

        return DashaPeriod(
            planet=next_planet,
            start_date=current_dasha.end_date,
            end_date=date.today(),  # This should be calculated properly
            level="mahadasha",
            remaining_years=float(dasha_periods[next_planet])
        )

    def _get_current_transits(self) -> List[str]:
        """Get current planetary transits (simplified)."""
        return [
            "Jupiter transit effects",
            "Saturn transit influences",
            "Current lunar phase impact"
        ]
