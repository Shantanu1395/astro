import openai
from typing import List, Dict, Any, Tuple
from datetime import date, datetime, timedelta
import json
import swisseph as swe

from models import VedicChart, DashaPeriod, VedicPrediction, BirthData, LocationData
from config import config
from vedic_analysis import VedicAnalyzer
from date_calculator import AstrologicalDateCalculator

class VedicPredictionEngine:
    def __init__(self):
        if config.OPENAI_API_KEY:
            openai.api_key = config.OPENAI_API_KEY
        else:
            print("Warning: OpenAI API key not found. Predictions will use fallback text.")

        # Initialize analysis modules
        self.analyzer = VedicAnalyzer()
        self.date_calculator = AstrologicalDateCalculator()

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

        return VedicPrediction(
            current_dasha=current_dasha,
            upcoming_dasha=upcoming_dasha,
            current_transits=formatted_transits,
            prediction_text=prediction_text,
            key_themes=key_themes,
            favorable_periods=formatted_favorable,
            challenging_periods=formatted_challenging
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
        """
        Generate prediction text using OpenAI LLM.
        """
        if not config.OPENAI_API_KEY:
            return self._generate_fallback_prediction(chart_summary)

        try:
            prompt = self._create_prediction_prompt(birth_data, chart_summary)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
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
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating LLM prediction: {e}")
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
        """Generate enhanced prediction with detailed analysis."""
        if not config.OPENAI_API_KEY:
            return self._generate_enhanced_fallback_prediction(chart_summary, dasha_analysis)

        try:
            prompt = self._create_enhanced_prediction_prompt(birth_data, chart_summary, dasha_analysis)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
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
                max_tokens=config.MAX_TOKENS * 2,  # More tokens for detailed analysis
                temperature=config.TEMPERATURE
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating enhanced LLM prediction: {e}")
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

        Please provide a detailed analysis covering:

        1. CURRENT DASHA SIGNIFICANCE:
        - What does the current {chart_summary['current_dasha']['planet']} dasha mean for this person?
        - How is this period influencing their life themes and experiences?
        - What opportunities and challenges does this period bring?

        2. PLANETARY RELATIONSHIPS & THEIR IMPACT:
        - How do the planetary positions and relationships affect the person?
        - What are the key yogas and their significance?
        - How do conjunctions and aspects influence life areas?

        3. SPECIFIC GUIDANCE FOR CURRENT PERIOD:
        - What should they focus on during this dasha?
        - What actions will bring the best results?
        - What practices or remedies would be beneficial?

        4. CAUTIONS AND AREAS TO WATCH:
        - What challenges or obstacles should they be aware of?
        - What areas of life need extra attention?
        - What should they avoid during this period?

        5. TIMING AND OPPORTUNITIES:
        - When are the most favorable periods within this dasha?
        - What types of activities are best suited for different times?
        - How can they make the most of upcoming opportunities?

        Make the analysis practical, specific, and actionable while maintaining authenticity to Vedic principles.
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
