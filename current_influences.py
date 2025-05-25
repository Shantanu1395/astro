"""
Current Day/Month Astrological Influences
Calculates how current planetary positions affect the individual
"""

from datetime import date, datetime, timedelta
from typing import Dict, List, Any, Tuple
import swisseph as swe
from models import VedicChart, BirthData, LocationData
from utils import julian_day_from_datetime, calculate_ayanamsa, degrees_to_sign_and_degree, VEDIC_SIGNS

class CurrentInfluenceAnalyzer:
    def __init__(self):
        # Current planetary themes and their effects
        self.planetary_themes = {
            "Sun": {
                "daily_theme": "Leadership and self-expression",
                "monthly_theme": "Authority and recognition",
                "effects": "Increased confidence, leadership opportunities, focus on career",
                "feelings": "More authoritative, confident, desire for recognition",
                "physical": "Increased energy, better posture, stronger presence"
            },
            "Moon": {
                "daily_theme": "Emotions and intuition",
                "monthly_theme": "Family and nurturing",
                "effects": "Heightened emotions, family focus, intuitive insights",
                "feelings": "More emotional, nurturing, intuitive, changeable moods",
                "physical": "Fluid retention, digestive changes, sleep pattern shifts"
            },
            "Mars": {
                "daily_theme": "Action and energy",
                "monthly_theme": "Competition and courage",
                "effects": "Increased activity, competitive spirit, quick decisions",
                "feelings": "More aggressive, impatient, energetic, action-oriented",
                "physical": "Higher energy, possible inflammation, increased metabolism"
            },
            "Mercury": {
                "daily_theme": "Communication and learning",
                "monthly_theme": "Business and networking",
                "effects": "Enhanced communication, learning opportunities, travel",
                "feelings": "More talkative, curious, analytical, restless",
                "physical": "Nervous energy, hand/arm activity, mental alertness"
            },
            "Jupiter": {
                "daily_theme": "Wisdom and expansion",
                "monthly_theme": "Growth and spirituality",
                "effects": "Optimism, learning, spiritual growth, good fortune",
                "feelings": "More optimistic, generous, philosophical, expansive",
                "physical": "Weight gain tendency, improved liver function, vitality"
            },
            "Venus": {
                "daily_theme": "Love and beauty",
                "monthly_theme": "Relationships and creativity",
                "effects": "Romantic feelings, artistic inspiration, social activities",
                "feelings": "More loving, artistic, social, pleasure-seeking",
                "physical": "Enhanced beauty, kidney function, reproductive health"
            },
            "Saturn": {
                "daily_theme": "Discipline and responsibility",
                "monthly_theme": "Hard work and karma",
                "effects": "Increased responsibility, disciplined approach, delays",
                "feelings": "More serious, disciplined, pessimistic, patient",
                "physical": "Joint stiffness, slower metabolism, endurance focus"
            },
            "Rahu": {
                "daily_theme": "Ambition and illusion",
                "monthly_theme": "Material desires and confusion",
                "effects": "Ambitious pursuits, unconventional approaches, confusion",
                "feelings": "More ambitious, confused, materialistic, rebellious",
                "physical": "Nervous system effects, unusual symptoms, restlessness"
            },
            "Ketu": {
                "daily_theme": "Spirituality and detachment",
                "monthly_theme": "Liberation and past karma",
                "effects": "Spiritual insights, detachment, karmic experiences",
                "feelings": "More detached, spiritual, introspective, isolated",
                "physical": "Mysterious symptoms, immune system effects, energy depletion"
            }
        }

        # Sign-based monthly themes
        self.sign_monthly_themes = {
            "Mesha": "New beginnings, leadership, pioneering spirit",
            "Vrishabha": "Stability, material security, sensual pleasures",
            "Mithuna": "Communication, learning, versatility",
            "Karka": "Emotions, family, nurturing, home focus",
            "Simha": "Creativity, self-expression, recognition",
            "Kanya": "Service, health, attention to detail",
            "Tula": "Relationships, balance, harmony",
            "Vrishchika": "Transformation, intensity, hidden matters",
            "Dhanu": "Philosophy, higher learning, expansion",
            "Makara": "Discipline, career, responsibility",
            "Kumbha": "Innovation, humanitarian causes, friendship",
            "Meena": "Spirituality, compassion, imagination"
        }

    def analyze_current_influences(self, birth_data: BirthData, chart: VedicChart, location_data: LocationData) -> Dict[str, Any]:
        """Analyze current day/month influences on the person."""
        current_date = datetime.now()
        julian_day = julian_day_from_datetime(current_date)
        ayanamsa = calculate_ayanamsa(julian_day)

        # Get current planetary positions
        current_positions = self._get_current_planetary_positions(julian_day, ayanamsa)

        # Analyze how current positions affect the person's chart
        personal_effects = self._analyze_personal_effects(current_positions, chart)

        # Get current lunar phase and its effects
        lunar_phase = self._get_current_lunar_phase(julian_day)

        # Get current month's dominant theme
        month_theme = self._get_current_month_theme(current_date, current_positions)

        # Calculate specific changes the person might feel
        daily_changes = self._calculate_daily_changes(current_positions, chart)
        monthly_changes = self._calculate_monthly_changes(month_theme, chart)

        return {
            "current_date": current_date.strftime("%B %d, %Y"),
            "current_positions": current_positions,
            "lunar_phase": lunar_phase,
            "month_theme": month_theme,
            "personal_effects": personal_effects,
            "daily_changes": daily_changes,
            "monthly_changes": monthly_changes,
            "recommendations": self._get_current_recommendations(current_positions, chart)
        }

    def _get_current_planetary_positions(self, julian_day: float, ayanamsa: float) -> Dict[str, Dict[str, Any]]:
        """Get current sidereal positions of all planets."""
        positions = {}

        planet_ids = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mars": swe.MARS,
            "Mercury": swe.MERCURY,
            "Jupiter": swe.JUPITER,
            "Venus": swe.VENUS,
            "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_NODE
        }

        for planet_name, planet_id in planet_ids.items():
            try:
                pos, _ = swe.calc_ut(julian_day, planet_id)
                sidereal_longitude = (pos[0] - ayanamsa) % 360
                sign, degree_in_sign = degrees_to_sign_and_degree(sidereal_longitude, vedic=True)

                positions[planet_name] = {
                    "longitude": sidereal_longitude,
                    "sign": sign,
                    "degree": degree_in_sign,
                    "themes": self.planetary_themes.get(planet_name, {})
                }
            except Exception as e:
                print(f"Error calculating {planet_name}: {e}")

        return positions

    def _get_current_lunar_phase(self, julian_day: float) -> Dict[str, Any]:
        """Calculate current lunar phase and its effects."""
        try:
            # Get Sun and Moon positions
            sun_pos, _ = swe.calc_ut(julian_day, swe.SUN)
            moon_pos, _ = swe.calc_ut(julian_day, swe.MOON)

            # Calculate phase angle
            phase_angle = (moon_pos[0] - sun_pos[0]) % 360

            # Determine phase
            if 0 <= phase_angle < 45:
                phase = "New Moon"
                effects = "New beginnings, introspection, planning"
            elif 45 <= phase_angle < 135:
                phase = "Waxing Moon"
                effects = "Growth, building energy, taking action"
            elif 135 <= phase_angle < 225:
                phase = "Full Moon"
                effects = "Peak energy, emotions heightened, completion"
            else:
                phase = "Waning Moon"
                effects = "Release, letting go, reflection"

            return {
                "phase": phase,
                "angle": phase_angle,
                "effects": effects,
                "emotional_impact": self._get_lunar_emotional_impact(phase)
            }
        except Exception as e:
            return {"phase": "Unknown", "effects": "Unable to calculate", "emotional_impact": ""}

    def _get_lunar_emotional_impact(self, phase: str) -> str:
        """Get emotional impact of current lunar phase."""
        impacts = {
            "New Moon": "Feeling introspective, desire for new starts, lower energy",
            "Waxing Moon": "Increasing optimism, motivation building, social energy rising",
            "Full Moon": "Emotions at peak, heightened sensitivity, intense feelings",
            "Waning Moon": "Reflective mood, releasing emotions, calming energy"
        }
        return impacts.get(phase, "")

    def _get_current_month_theme(self, current_date: datetime, positions: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Get the dominant theme for current month."""
        # Primary theme based on Sun's current sign
        sun_sign = positions.get("Sun", {}).get("sign", "Unknown")
        primary_theme = self.sign_monthly_themes.get(sun_sign, "General growth and development")

        # Secondary influences from other planets
        secondary_influences = []
        for planet, data in positions.items():
            if planet != "Sun":
                planet_theme = data.get("themes", {}).get("monthly_theme", "")
                if planet_theme:
                    secondary_influences.append(f"{planet}: {planet_theme}")

        return {
            "primary_theme": primary_theme,
            "sun_sign": sun_sign,
            "secondary_influences": secondary_influences[:3],  # Top 3 influences
            "month_name": current_date.strftime("%B %Y")
        }

    def _analyze_personal_effects(self, current_positions: Dict[str, Dict[str, Any]], chart: VedicChart) -> List[Dict[str, Any]]:
        """Analyze how current planetary positions affect the person's birth chart."""
        effects = []

        for current_planet, current_data in current_positions.items():
            current_sign = current_data.get("sign", "")

            # Find if any birth planets are in the same sign (conjunction by sign)
            for birth_planet in chart.planets:
                if birth_planet.sign == current_sign and birth_planet.name != current_planet:
                    effect = {
                        "type": "Planetary Activation",
                        "description": f"Today's {current_planet} energy is highlighting your natural {birth_planet.name} qualities",
                        "impact": self._get_clear_impact_description(current_planet, birth_planet.name),
                        "house_affected": birth_planet.house,
                        "feeling": self._get_conjunction_feeling(current_planet, birth_planet.name)
                    }
                    effects.append(effect)

            # Check if current planet is transiting through important houses
            for birth_planet in chart.planets:
                if birth_planet.name == current_planet:
                    # This is the same planet - check house transit
                    effect = {
                        "type": "Current Energy Focus",
                        "description": f"Your {current_planet} energy is currently focused on {self._get_simple_house_description(birth_planet.house)}",
                        "impact": self._get_house_impact_description(current_planet, birth_planet.house),
                        "house_affected": birth_planet.house,
                        "feeling": current_data.get("themes", {}).get("feelings", "")
                    }
                    effects.append(effect)
                    break

        return effects[:5]  # Return top 5 most significant effects

    def _get_conjunction_feeling(self, transiting_planet: str, natal_planet: str) -> str:
        """Get comprehensive feeling descriptions for ALL planetary conjunctions based on classical Vedic texts."""
        combinations = {
            # SUN COMBINATIONS - Based on Brihat Parashara Hora Shastra & Phaladeepika
            ("Sun", "Moon"): "Feeling emotionally integrated and confident, your inner and outer selves are harmonized. Strong willpower combined with intuitive wisdom. You may feel more visible and emotionally expressive today.",

            ("Sun", "Mercury"): "Your intellect shines brightly today. Communication is authoritative and confident. Excellent for writing, speaking, and intellectual pursuits. You feel mentally sharp and articulate.",

            ("Sun", "Venus"): "Charismatic and attractive energy. Your creative and artistic abilities are enhanced. Feeling charming, diplomatic, and socially confident. Good for romance and artistic expression.",

            ("Sun", "Mars"): "Powerful energy and drive. Feeling bold, courageous, and action-oriented. Leadership qualities are amplified. You're ready to take charge and face challenges head-on.",

            ("Sun", "Jupiter"): "Feeling wise, optimistic, and naturally authoritative. Your moral compass is strong. Excellent for teaching, guiding others, and making important decisions. Spiritual confidence is high.",

            ("Sun", "Saturn"): "Serious, disciplined, and focused on long-term goals. You feel the weight of responsibility but also the strength to handle it. Patient and methodical approach to challenges.",

            ("Sun", "Rahu"): "Ambitious energy is heightened with unconventional approaches. Strong desire for recognition and material success. You may feel restless and eager to break boundaries.",

            ("Sun", "Ketu"): "Feeling spiritually inclined and less concerned with worldly recognition. Your ego is subdued, leading to introspection and spiritual insights. Detachment from material desires.",

            # MOON COMBINATIONS - Based on Jataka Parijata & Saravali
            ("Moon", "Mercury"): "Your emotions and intellect work in perfect harmony. Intuitive communication and emotional intelligence are heightened. You feel mentally flexible and emotionally articulate.",

            ("Moon", "Venus"): "Emotionally romantic and aesthetically sensitive. Your heart is open to beauty and love. Feeling nurturing, artistic, and socially graceful. Strong emotional connections.",

            ("Moon", "Mars"): "Emotions are intense and passionate. Quick emotional reactions and strong feelings. You feel energetic but may be emotionally impulsive. Protective instincts are strong.",

            ("Moon", "Jupiter"): "Emotionally optimistic and spiritually uplifted. Feeling blessed, generous, and wise. Your intuition is guided by higher wisdom. Maternal/paternal feelings are strong.",

            ("Moon", "Saturn"): "Emotions feel more controlled and serious. You're thinking practically about feelings. May feel emotionally reserved but stable. Patience in emotional matters.",

            ("Moon", "Rahu"): "Emotions are restless and craving new experiences. You feel emotionally ambitious and may seek unusual emotional connections. Changeable moods and desires.",

            ("Moon", "Ketu"): "Feeling emotionally detached and seeking inner peace. Your emotions are turned inward. You may feel disconnected from worldly emotional dramas, seeking solitude.",

            # MERCURY COMBINATIONS - Based on Hora Sara & Brihat Jataka
            ("Mercury", "Venus"): "Communication is charming, artistic, and persuasive. Your words carry beauty and grace. Excellent for negotiations, creative writing, and social interactions.",

            ("Mercury", "Mars"): "Sharp, quick thinking with direct communication. Mental energy is high and you speak with conviction. Good for debates, quick decisions, and assertive communication.",

            ("Mercury", "Jupiter"): "Wise and philosophical communication. Your words carry wisdom and moral authority. Excellent for teaching, counseling, and sharing knowledge. Ethical thinking.",

            ("Mercury", "Saturn"): "Careful, methodical thinking and precise communication. You speak with authority and seriousness. Good for detailed work, planning, and serious discussions.",

            ("Mercury", "Rahu"): "Mind is restless and curious about unconventional topics. Innovative thinking and unusual communication style. You may be drawn to foreign languages or technologies.",

            ("Mercury", "Ketu"): "Deep, intuitive thinking with less interest in superficial communication. You prefer meaningful conversations and may have insights into hidden knowledge.",

            # VENUS COMBINATIONS - Based on Uttara Kalamrita & Jataka Tattva
            ("Venus", "Mars"): "Passionate feelings with strong attraction and desire. Your romantic and sexual energy is heightened. You feel magnetically attractive and emotionally intense.",

            ("Venus", "Jupiter"): "Feeling generous in love and optimistic about relationships. Your heart is expansive and you attract good fortune in love. Spiritual love and wisdom in relationships.",

            ("Venus", "Saturn"): "More serious and committed approach to relationships. You value stability and long-term partnerships. May feel reserved in love but deeply loyal.",

            ("Venus", "Rahu"): "Unusual attractions and desire for exotic or foreign connections. You're drawn to unconventional beauty and relationships. Strong material desires and luxury.",

            ("Venus", "Ketu"): "Less attachment to material pleasures and more spiritual approach to love. You may feel detached from superficial attractions, seeking deeper connections.",

            # MARS COMBINATIONS - Based on Mansagari & Phaladeepika
            ("Mars", "Jupiter"): "Energetic optimism with wisdom guiding your actions. You feel motivated to take righteous action. Courage is combined with moral principles and higher purpose.",

            ("Mars", "Saturn"): "Controlled energy with disciplined action. You feel patient but determined. Your efforts are methodical and persistent. Good for long-term projects requiring endurance.",

            ("Mars", "Rahu"): "Aggressive ambition with unconventional methods. High energy directed toward material goals. You feel impulsive and eager to break traditional boundaries.",

            ("Mars", "Ketu"): "Energy is directed inward toward spiritual goals. You feel less aggressive and more contemplative. Your actions are guided by inner wisdom rather than external desires.",

            # JUPITER COMBINATIONS - Based on Brihat Parashara Hora Shastra
            ("Jupiter", "Saturn"): "Wisdom balanced with discipline and practical application. You feel both optimistic and realistic. Your judgment is sound and you can manifest your ideals practically.",

            ("Jupiter", "Rahu"): "Expansive ambitions with optimism about material success. You feel confident about achieving your goals through unconventional means. Spiritual materialism may be present.",

            ("Jupiter", "Ketu"): "Spiritual wisdom is heightened with philosophical detachment. You feel drawn to higher knowledge and may have insights into spiritual truths. Detachment from material success.",

            # SATURN COMBINATIONS - Based on Jataka Parijata & Hora Sara
            ("Saturn", "Rahu"): "Disciplined ambition working toward unconventional goals. You feel patient about achieving material success through persistent effort. Methodical approach to desires.",

            ("Saturn", "Ketu"): "Serious spiritual focus with disciplined detachment. You feel committed to inner work and spiritual practices. Patient approach to liberation and self-realization.",

            # RAHU-KETU COMBINATION - Based on classical texts on lunar nodes
            ("Rahu", "Ketu"): "Internal conflict between worldly desires and spiritual detachment. You feel torn between material ambitions and spiritual calling. Seeking balance between opposites.",

            # Additional combinations with correct sorted keys to prevent fallbacks
            ("Ketu", "Sun"): "Feeling spiritually inclined and less concerned with worldly recognition. Your ego is subdued, leading to introspection and spiritual insights. Detachment from material desires.",
            ("Ketu", "Mercury"): "Deep, intuitive thinking with less interest in superficial communication. You prefer meaningful conversations and may have insights into hidden knowledge.",

            # MISSING COMBINATIONS - Adding ALL remaining combinations for 100% coverage
            ("Ketu", "Moon"): "Feeling emotionally detached and seeking inner peace. Your emotions are turned inward. You may feel disconnected from worldly emotional dramas, seeking solitude.",
            ("Ketu", "Venus"): "Less attachment to material pleasures and more spiritual approach to love. You may feel detached from superficial attractions, seeking deeper connections.",
            ("Ketu", "Mars"): "Energy is directed inward toward spiritual goals. You feel less aggressive and more contemplative. Your actions are guided by inner wisdom rather than external desires.",
            ("Ketu", "Jupiter"): "Spiritual wisdom is heightened with philosophical detachment. You feel drawn to higher knowledge and may have insights into spiritual truths. Detachment from material success.",
            ("Ketu", "Saturn"): "Serious spiritual focus with disciplined detachment. You feel committed to inner work and spiritual practices. Patient approach to liberation and self-realization.",
            ("Ketu", "Rahu"): "Internal conflict between worldly desires and spiritual detachment. You feel torn between material ambitions and spiritual calling. Seeking balance between opposites.",

            # Additional missing sorted key combinations
            ("Mercury", "Moon"): "Your emotions and intellect work in perfect harmony. Intuitive communication and emotional intelligence are heightened. You feel mentally flexible and emotionally articulate.",
            ("Mars", "Moon"): "Emotions are intense and passionate. Quick emotional reactions and strong feelings. You feel energetic but may be emotionally impulsive. Protective instincts are strong.",
            ("Jupiter", "Moon"): "Emotionally optimistic and spiritually uplifted. Feeling blessed, generous, and wise. Your intuition is guided by higher wisdom. Maternal/paternal feelings are strong.",
            ("Saturn", "Moon"): "Emotions feel more controlled and serious. You're thinking practically about feelings. May feel emotionally reserved but stable. Patience in emotional matters.",
            ("Rahu", "Moon"): "Emotions are restless and craving new experiences. You feel emotionally ambitious and may seek unusual emotional connections. Changeable moods and desires.",

            ("Mars", "Mercury"): "Sharp, quick thinking with direct communication. Mental energy is high and you speak with conviction. Good for debates, quick decisions, and assertive communication.",
            ("Jupiter", "Mercury"): "Wise and philosophical communication. Your words carry wisdom and moral authority. Excellent for teaching, counseling, and sharing knowledge. Ethical thinking.",
            ("Saturn", "Mercury"): "Careful, methodical thinking and precise communication. You speak with authority and seriousness. Good for detailed work, planning, and serious discussions.",
            ("Rahu", "Mercury"): "Mind is restless and curious about unconventional topics. Innovative thinking and unusual communication style. You may be drawn to foreign languages or technologies.",

            ("Mars", "Venus"): "Passionate feelings with strong attraction and desire. Your romantic and sexual energy is heightened. You feel magnetically attractive and emotionally intense.",
            ("Jupiter", "Venus"): "Feeling generous in love and optimistic about relationships. Your heart is expansive and you attract good fortune in love. Spiritual love and wisdom in relationships.",
            ("Saturn", "Venus"): "More serious and committed approach to relationships. You value stability and long-term partnerships. May feel reserved in love but deeply loyal.",
            ("Rahu", "Venus"): "Unusual attractions and desire for exotic or foreign connections. You're drawn to unconventional beauty and relationships. Strong material desires and luxury.",

            ("Jupiter", "Mars"): "Energetic optimism with wisdom guiding your actions. You feel motivated to take righteous action. Courage is combined with moral principles and higher purpose.",
            ("Saturn", "Mars"): "Controlled energy with disciplined action. You feel patient but determined. Your efforts are methodical and persistent. Good for long-term projects requiring endurance.",
            ("Rahu", "Mars"): "Aggressive ambition with unconventional methods. High energy directed toward material goals. You feel impulsive and eager to break traditional boundaries.",

            ("Jupiter", "Saturn"): "Wisdom balanced with discipline and practical application. You feel both optimistic and realistic. Your judgment is sound and you can manifest your ideals practically.",
            ("Rahu", "Jupiter"): "Expansive ambitions with optimism about material success. You feel confident about achieving your goals through unconventional means. Spiritual materialism may be present.",

            ("Rahu", "Saturn"): "Disciplined ambition working toward unconventional goals. You feel patient about achieving material success through persistent effort. Methodical approach to desires.",

            # FINAL MISSING SUN COMBINATIONS - Adding sorted key versions
            ("Moon", "Sun"): "Feeling emotionally integrated and confident, your inner and outer selves are harmonized. Strong willpower combined with intuitive wisdom. You may feel more visible and emotionally expressive today.",
            ("Mercury", "Sun"): "Your intellect shines brightly today. Communication is authoritative and confident. Excellent for writing, speaking, and intellectual pursuits. You feel mentally sharp and articulate.",
            ("Mars", "Sun"): "Powerful energy and drive. Feeling bold, courageous, and action-oriented. Leadership qualities are amplified. You're ready to take charge and face challenges head-on.",
            ("Jupiter", "Sun"): "Feeling wise, optimistic, and naturally authoritative. Your moral compass is strong. Excellent for teaching, guiding others, and making important decisions. Spiritual confidence is high.",
            ("Saturn", "Sun"): "Serious, disciplined, and focused on long-term goals. You feel the weight of responsibility but also the strength to handle it. Patient and methodical approach to challenges.",
            ("Rahu", "Sun"): "Ambitious energy is heightened with unconventional approaches. Strong desire for recognition and material success. You may feel restless and eager to break boundaries."
        }

        key = tuple(sorted([transiting_planet, natal_planet]))
        # Ensure we never return generic text - always have a specific description
        result = combinations.get(key)
        if result:
            return result
        else:
            # Create specific descriptions for any missing combinations
            return self._get_fallback_combination_feeling(transiting_planet, natal_planet)

    def _get_clear_impact_description(self, current_planet: str, natal_planet: str) -> str:
        """Get comprehensive impact descriptions based on classical Vedic astrology texts."""
        impact_descriptions = {
            # SUN IMPACT DESCRIPTIONS - Based on Brihat Parashara Hora Shastra
            ("Sun", "Moon"): "Your emotional nature and self-confidence are perfectly aligned today. You feel emotionally strong and your personality shines with inner radiance. Leadership through emotional intelligence is highlighted.",

            ("Sun", "Mercury"): "Your intellectual abilities and communication skills are illuminated with authority and confidence. Excellent day for important conversations, writing, and mental work. Your words carry weight and influence.",

            ("Sun", "Venus"): "Your charm, artistic abilities, and social grace are enhanced with confident self-expression. You attract others through your refined personality. Excellent for creative work and romantic endeavors.",

            ("Sun", "Mars"): "Your courage, energy, and leadership abilities are powerfully amplified. You feel bold and ready to take decisive action. Excellent for starting new projects and overcoming obstacles with determination.",

            ("Sun", "Jupiter"): "Your wisdom, moral authority, and spiritual understanding are illuminated. You feel naturally wise and others look to you for guidance. Excellent for teaching, counseling, and making ethical decisions.",

            ("Sun", "Saturn"): "Your sense of responsibility, discipline, and long-term planning are strengthened with steady determination. You feel serious about your duties and capable of handling major responsibilities.",

            ("Sun", "Rahu"): "Your ambitions and desire for recognition are intensified with unconventional approaches to success. You feel driven to achieve something unique and may break traditional boundaries.",

            ("Sun", "Ketu"): "Your spiritual inclinations and detachment from ego are heightened. You feel less concerned with worldly recognition and more focused on inner development and self-realization.",

            # MOON IMPACT DESCRIPTIONS - Based on Jataka Parijata & Saravali
            ("Moon", "Mercury"): "Your emotional intelligence and communication abilities work in perfect harmony. You can express feelings clearly and understand others intuitively. Excellent for counseling and emotional discussions.",

            ("Moon", "Venus"): "Your emotional and aesthetic sensibilities are beautifully harmonized. You feel deeply romantic and artistically inspired. Your nurturing nature attracts love and appreciation from others.",

            ("Moon", "Mars"): "Your emotions are intense and you feel passionate about everything. Quick emotional responses and strong protective instincts. You may feel more aggressive in defending loved ones.",

            ("Moon", "Jupiter"): "Your emotional nature is blessed with wisdom and optimism. You feel emotionally generous and spiritually uplifted. Your intuition is guided by higher wisdom and moral principles.",

            ("Moon", "Saturn"): "Your emotions are more controlled and you think practically about feelings. You feel emotionally mature and stable, though perhaps more reserved than usual. Patience in emotional matters.",

            ("Moon", "Rahu"): "Your emotions are restless and you crave new, unusual experiences. You feel emotionally ambitious and may seek unconventional emotional connections or foreign influences.",

            ("Moon", "Ketu"): "Your emotional nature turns inward seeking peace and spiritual understanding. You feel detached from emotional dramas and may prefer solitude for inner reflection.",

            # MERCURY IMPACT DESCRIPTIONS - Based on Hora Sara & Brihat Jataka
            ("Mercury", "Venus"): "Your communication becomes charming, artistic, and diplomatically persuasive. You speak with grace and beauty, making others feel comfortable. Excellent for negotiations and creative expression.",

            ("Mercury", "Mars"): "Your thinking becomes sharp and decisive with direct, energetic communication. You speak with conviction and mental energy is high. Good for debates and quick decision-making.",

            ("Mercury", "Jupiter"): "Your communication carries wisdom and moral authority. You speak with philosophical depth and others seek your counsel. Excellent for teaching, writing, and sharing knowledge.",

            ("Mercury", "Saturn"): "Your thinking becomes methodical and your communication precise and authoritative. You speak with careful consideration and your words carry weight. Good for serious planning.",

            ("Mercury", "Rahu"): "Your mind becomes restless and curious about unconventional topics. You think innovatively and may be drawn to foreign languages, technology, or unusual subjects.",

            ("Mercury", "Ketu"): "Your thinking becomes deep and intuitive with preference for meaningful communication. You're less interested in small talk and more drawn to profound conversations.",

            # Additional combinations to ensure complete coverage - no duplicates
            ("Moon", "Mercury"): "Your emotional intelligence and communication abilities work in perfect harmony. You can express feelings clearly and understand others intuitively. Excellent for counseling and emotional discussions.",

            # VENUS IMPACT DESCRIPTIONS - Based on Uttara Kalamrita & Jataka Tattva
            ("Venus", "Mars"): "Your romantic and passionate energies are both strongly activated. You feel magnetically attractive and emotionally intense. Strong desires for love, beauty, and physical pleasure.",

            ("Venus", "Jupiter"): "Your capacity for love expands with wisdom and generosity. You feel optimistic about relationships and attract good fortune in love. Spiritual dimensions of love are highlighted.",

            ("Venus", "Saturn"): "Your approach to love becomes more serious and committed. You value stability and long-term relationships over casual attractions. May feel reserved but deeply loyal in love.",

            ("Venus", "Rahu"): "You're attracted to unusual, exotic, or foreign elements in love and beauty. Strong material desires and attraction to luxury. Unconventional relationships may appeal to you.",

            ("Venus", "Ketu"): "Your attachment to material pleasures decreases while spiritual love increases. You may feel detached from superficial attractions and seek deeper, more meaningful connections.",

            # MARS IMPACT DESCRIPTIONS - Based on Mansagari & Phaladeepika
            ("Mars", "Jupiter"): "Your energy is guided by wisdom and moral principles. You feel motivated to take righteous action and fight for just causes. Courage is combined with higher purpose.",

            ("Mars", "Saturn"): "Your energy becomes controlled and disciplined with patient, methodical action. You feel determined but not impulsive. Excellent for long-term projects requiring sustained effort.",

            ("Mars", "Rahu"): "Your energy becomes intense and directed toward ambitious material goals. You feel impulsive and eager to break traditional boundaries through aggressive action.",

            ("Mars", "Ketu"): "Your energy turns inward toward spiritual goals and self-realization. You feel less aggressive toward external goals and more focused on inner transformation.",

            # JUPITER IMPACT DESCRIPTIONS - Based on Brihat Parashara Hora Shastra
            ("Jupiter", "Saturn"): "Your wisdom combines with practical discipline to manifest ideals in reality. You feel both optimistic and realistic, able to achieve long-term goals through patient effort.",

            ("Jupiter", "Rahu"): "Your spiritual wisdom expands toward material success through unconventional means. You feel optimistic about achieving ambitious goals, though spiritual materialism may be present.",

            ("Jupiter", "Ketu"): "Your spiritual wisdom is heightened with philosophical detachment from material success. You feel drawn to higher knowledge and may have profound spiritual insights.",

            # SATURN IMPACT DESCRIPTIONS - Based on Jataka Parijata & Hora Sara
            ("Saturn", "Rahu"): "Your disciplined approach combines with ambitious desires to achieve unconventional goals through patient, methodical effort. You work steadily toward material success.",

            ("Saturn", "Ketu"): "Your discipline is directed toward spiritual practices and inner work. You feel committed to self-realization through patient, methodical spiritual effort.",

            # RAHU-KETU IMPACT - Based on classical texts on lunar nodes
            ("Rahu", "Ketu"): "You experience internal conflict between worldly desires and spiritual detachment. You feel torn between material ambitions and spiritual calling, seeking balance between opposites.",

            # Additional impact descriptions with correct sorted keys to prevent fallbacks
            ("Ketu", "Sun"): "Your spiritual inclinations and detachment from ego are heightened. You feel less concerned with worldly recognition and more focused on inner development and self-realization.",
            ("Ketu", "Mercury"): "Your thinking becomes deep and intuitive with preference for meaningful communication. You're less interested in small talk and more drawn to profound conversations.",

            # MISSING IMPACT DESCRIPTIONS - Adding ALL remaining combinations for 100% coverage
            ("Ketu", "Moon"): "Your emotional nature turns inward seeking peace and spiritual understanding. You feel detached from emotional dramas and may prefer solitude for inner reflection.",
            ("Ketu", "Venus"): "Your attachment to material pleasures decreases while spiritual love increases. You may feel detached from superficial attractions and seek deeper, more meaningful connections.",
            ("Ketu", "Mars"): "Your energy turns inward toward spiritual goals and self-realization. You feel less aggressive toward external goals and more focused on inner transformation.",
            ("Ketu", "Jupiter"): "Your spiritual wisdom is heightened with philosophical detachment from material success. You feel drawn to higher knowledge and may have profound spiritual insights.",
            ("Ketu", "Saturn"): "Your discipline is directed toward spiritual practices and inner work. You feel committed to self-realization through patient, methodical spiritual effort.",
            ("Ketu", "Rahu"): "You experience internal conflict between worldly desires and spiritual detachment. You feel torn between material ambitions and spiritual calling, seeking balance between opposites.",

            # Additional missing sorted key impact descriptions
            ("Mercury", "Moon"): "Your emotional intelligence and communication abilities work in perfect harmony. You can express feelings clearly and understand others intuitively. Excellent for counseling and emotional discussions.",
            ("Mars", "Moon"): "Your emotions are intense and you feel passionate about everything. Quick emotional responses and strong protective instincts. You may feel more aggressive in defending loved ones.",
            ("Jupiter", "Moon"): "Your emotional nature is blessed with wisdom and optimism. You feel emotionally generous and spiritually uplifted. Your intuition is guided by higher wisdom and moral principles.",
            ("Saturn", "Moon"): "Your emotions are more controlled and you think practically about feelings. You feel emotionally mature and stable, though perhaps more reserved than usual. Patience in emotional matters.",
            ("Rahu", "Moon"): "Your emotions are restless and you crave new, unusual experiences. You feel emotionally ambitious and may seek unconventional emotional connections or foreign influences.",

            ("Mars", "Mercury"): "Your thinking becomes sharp and decisive with direct, energetic communication. You speak with conviction and mental energy is high. Good for debates and quick decision-making.",
            ("Jupiter", "Mercury"): "Your communication carries wisdom and moral authority. You speak with philosophical depth and others seek your counsel. Excellent for teaching, writing, and sharing knowledge.",
            ("Saturn", "Mercury"): "Your thinking becomes methodical and your communication precise and authoritative. You speak with careful consideration and your words carry weight. Good for serious planning.",
            ("Rahu", "Mercury"): "Your mind becomes restless and curious about unconventional topics. You think innovatively and may be drawn to foreign languages, technology, or unusual subjects.",

            ("Mars", "Venus"): "Your romantic and passionate energies are both strongly activated. You feel magnetically attractive and emotionally intense. Strong desires for love, beauty, and physical pleasure.",
            ("Jupiter", "Venus"): "Your capacity for love expands with wisdom and generosity. You feel optimistic about relationships and attract good fortune in love. Spiritual dimensions of love are highlighted.",
            ("Saturn", "Venus"): "Your approach to love becomes more serious and committed. You value stability and long-term relationships over casual attractions. May feel reserved but deeply loyal in love.",
            ("Rahu", "Venus"): "You're attracted to unusual, exotic, or foreign elements in love and beauty. Strong material desires and attraction to luxury. Unconventional relationships may appeal to you.",

            ("Jupiter", "Mars"): "Your energy is guided by wisdom and moral principles. You feel motivated to take righteous action and fight for just causes. Courage is combined with higher purpose.",
            ("Saturn", "Mars"): "Your energy becomes controlled and disciplined with patient, methodical action. You feel determined but not impulsive. Excellent for long-term projects requiring sustained effort.",
            ("Rahu", "Mars"): "Your energy becomes intense and directed toward ambitious material goals. You feel impulsive and eager to break traditional boundaries through aggressive action.",

            ("Jupiter", "Saturn"): "Your wisdom combines with practical discipline to manifest ideals in reality. You feel both optimistic and realistic, able to achieve long-term goals through patient effort.",
            ("Rahu", "Jupiter"): "Your spiritual wisdom expands toward material success through unconventional means. You feel optimistic about achieving ambitious goals, though spiritual materialism may be present.",

            ("Rahu", "Saturn"): "Your disciplined approach combines with ambitious desires to achieve unconventional goals through patient, methodical effort. You work steadily toward material success.",

            # FINAL MISSING SUN IMPACT DESCRIPTIONS - Adding sorted key versions
            ("Moon", "Sun"): "Your emotional nature and self-confidence are perfectly aligned today. You feel emotionally strong and your personality shines with inner radiance. Leadership through emotional intelligence is highlighted.",
            ("Mercury", "Sun"): "Your intellectual abilities and communication skills are illuminated with authority and confidence. Excellent day for important conversations, writing, and mental work. Your words carry weight and influence.",
            ("Mars", "Sun"): "Your courage, energy, and leadership abilities are powerfully amplified. You feel bold and ready to take decisive action. Excellent for starting new projects and overcoming obstacles with determination.",
            ("Jupiter", "Sun"): "Your wisdom, moral authority, and spiritual understanding are illuminated. You feel naturally wise and others look to you for guidance. Excellent for teaching, counseling, and making ethical decisions.",
            ("Saturn", "Sun"): "Your sense of responsibility, discipline, and long-term planning are strengthened with steady determination. You feel serious about your duties and capable of handling major responsibilities.",
            ("Rahu", "Sun"): "Your ambitions and desire for recognition are intensified with unconventional approaches to success. You feel driven to achieve something unique and may break traditional boundaries."
        }

        key = tuple(sorted([current_planet, natal_planet]))
        # Ensure we never return generic text - always have a specific description
        result = impact_descriptions.get(key)
        if result:
            return result
        else:
            # Create specific descriptions for any missing combinations
            return self._get_fallback_impact_description(current_planet, natal_planet)

    def _get_simple_house_description(self, house: int) -> str:
        """Get simple, clear house descriptions."""
        descriptions = {
            1: "your personality and how others see you",
            2: "your money, possessions, and family matters",
            3: "communication, siblings, and short trips",
            4: "home, family, and emotional security",
            5: "creativity, children, and fun activities",
            6: "health, work routine, and daily responsibilities",
            7: "relationships, partnerships, and marriage",
            8: "deep changes, shared resources, and transformation",
            9: "higher learning, spirituality, and life philosophy",
            10: "career, reputation, and public image",
            11: "friendships, hopes, and financial gains",
            12: "spirituality, hidden matters, and letting go"
        }
        return descriptions.get(house, "various life areas")

    def _get_house_impact_description(self, planet: str, house: int) -> str:
        """Get comprehensive descriptions of how planets affect different life areas based on classical texts."""
        planet_house_impacts = {
            # SUN IN HOUSES - Based on Brihat Parashara Hora Shastra
            ("Sun", 1): "Your personality radiates confidence and natural authority. You feel strong, vital, and ready to lead. Others see you as a natural leader and your self-expression is powerful and magnetic.",
            ("Sun", 2): "Your focus is on building wealth, expressing your values clearly, and strengthening family bonds. You feel confident about your resources and ability to accumulate material security.",
            ("Sun", 3): "Your communication carries authority and confidence. You feel bold in expressing ideas and may take leadership in writing, speaking, or short-distance travel. Courage in communication is highlighted.",
            ("Sun", 4): "Home, family, and emotional foundations are illuminated with leadership energy. You may take charge of family matters or feel strong about your roots and domestic security.",
            ("Sun", 5): "Your creativity, self-expression, and relationship with children are at their peak. You feel artistically inspired and confident in romantic pursuits. Natural teaching abilities shine.",
            ("Sun", 6): "You're taking authoritative control of your health, daily routines, and service to others. You feel strong about overcoming obstacles and may lead in workplace situations.",
            ("Sun", 7): "Your partnerships and relationships are highlighted with confident energy. You attract strong partners and feel authoritative in one-on-one relationships and business partnerships.",
            ("Sun", 8): "You're courageously facing deep transformations and hidden matters. You feel strong about research, occult studies, or dealing with other people's resources and inheritances.",
            ("Sun", 9): "Your wisdom, spiritual understanding, and higher learning are illuminated. You feel naturally wise and may be drawn to teaching, philosophy, or long-distance travel.",
            ("Sun", 10): "Your career and public reputation are in the spotlight. You feel destined for recognition and leadership in your profession. Authority and status are emphasized.",
            ("Sun", 11): "You're confident about achieving your goals and feel strong in social networks. Friendships with influential people and gains through leadership are highlighted.",
            ("Sun", 12): "You're finding strength in solitude, spiritual practices, and behind-the-scenes work. You may feel drawn to foreign lands or charitable activities.",

            # MOON IN HOUSES - Based on Jataka Parijata & Saravali
            ("Moon", 1): "Your emotions are highly visible and you feel sensitive about your public image. Your personality reflects your changing moods and you appear nurturing and intuitive to others.",
            ("Moon", 2): "Strong emotional connection to money, family, and material security. You feel protective of your resources and family relationships are emotionally important today.",
            ("Moon", 3): "Your communication is emotionally charged and intuitive. You feel like sharing your feelings and may be more talkative about personal matters. Emotional connections with siblings.",
            ("Moon", 4): "Deep focus on home, family, and emotional security. You feel strongly connected to your roots and may be more nurturing toward family members. Domestic happiness is important.",
            ("Moon", 5): "Your creative and nurturing sides are emotionally highlighted. You feel romantic and may be more emotionally expressive in creative pursuits or with children.",
            ("Moon", 6): "Your emotions strongly affect your health and daily routines. You feel more sensitive to your work environment and may be emotionally invested in service to others.",
            ("Moon", 7): "Relationships and emotional partnerships are your primary focus. You feel deeply about your close relationships and may seek emotional security through partnerships.",
            ("Moon", 8): "Deep emotional changes and transformations are occurring. You feel psychically sensitive and may have intense emotional experiences related to hidden or occult matters.",
            ("Moon", 9): "Your intuition and spiritual feelings are heightened. You feel emotionally connected to higher wisdom and may be drawn to spiritual teachers or philosophical studies.",
            ("Moon", 10): "Your public image is closely tied to your emotional state. You feel that your reputation depends on your ability to nurture and care for others in your profession.",
            ("Moon", 11): "Emotional connections with friends and groups are very important. You feel supported by your social network and may gain through female friends or maternal figures.",
            ("Moon", 12): "You're seeking emotional peace and spiritual comfort. You feel drawn to solitude, meditation, or charitable work. Emotional healing through spiritual practices.",

            # MARS IN HOUSES - Based on Mansagari & Phaladeepika
            ("Mars", 1): "You're feeling highly energetic, assertive, and ready for action. Your personality radiates courage and determination. You appear bold and dynamic to others.",
            ("Mars", 2): "You're aggressively motivated to earn money and protect your material resources. You feel competitive about wealth and may take bold financial risks.",
            ("Mars", 3): "Your communication is direct, energetic, and sometimes aggressive. You feel like taking quick action and may be more assertive with siblings or in short travels.",
            ("Mars", 4): "You're putting high energy into home and family matters. You feel protective of your domestic space and may take aggressive action to secure your emotional foundations.",
            ("Mars", 5): "Your creative energy is intense and you feel passionate about fun activities, sports, or romantic pursuits. You may be more competitive in creative expressions.",
            ("Mars", 6): "You're tackling health and work challenges with exceptional energy and determination. You feel like fighting against obstacles and enemies with courage.",
            ("Mars", 7): "You're more assertive and sometimes aggressive in relationships and partnerships. You feel passionate about your close relationships but may also experience conflicts.",
            ("Mars", 8): "You're courageously facing deep transformations and may feel drawn to research hidden or dangerous matters. High energy for dealing with crises or emergencies.",
            ("Mars", 9): "You feel passionate about learning, teaching, and spiritual growth. You may take aggressive action in pursuit of higher knowledge or long-distance travel.",
            ("Mars", 10): "You're aggressively pursuing career goals and professional recognition. You feel highly competitive in your field and ready to fight for your position.",
            ("Mars", 11): "You're putting intense energy toward achieving your hopes and dreams. You feel competitive within your social groups and may gain through aggressive networking.",
            ("Mars", 12): "You're fighting inner battles and putting energy into spiritual growth. You may feel drawn to foreign lands or working behind the scenes with determination.",

            # MERCURY IN HOUSES - Based on Hora Sara & Brihat Jataka
            ("Mercury", 1): "Your communication skills and intellectual abilities are prominently displayed in your personality. You appear witty, intelligent, and articulate to others.",
            ("Mercury", 2): "You're thinking strategically about money and communicating with family about resources. Your intellectual abilities help you accumulate wealth and express family values.",
            ("Mercury", 3): "Your communication skills and mental agility are at their peak. You feel highly articulate and may excel in writing, speaking, or connecting with siblings.",
            ("Mercury", 4): "You're intellectually focused on home and family matters. You feel like communicating with family members and may use your mental skills to improve domestic situations.",
            ("Mercury", 5): "Your creative communication and learning abilities shine brightly. You feel intellectually creative and may excel in teaching, writing, or artistic expression.",
            ("Mercury", 6): "You're using your analytical skills to organize your daily routine and health matters. You feel mentally sharp about solving practical problems and work efficiency.",
            ("Mercury", 7): "Communication in relationships and partnerships is crucial today. You feel like your intellectual connection with partners is especially important for harmony.",
            ("Mercury", 8): "You're thinking deeply about transformations, hidden matters, and research. Your mind is drawn to mysteries, occult subjects, or investigating complex topics.",
            ("Mercury", 9): "Your learning and teaching abilities are enhanced with philosophical thinking. You feel intellectually drawn to higher wisdom, foreign cultures, or spiritual studies.",
            ("Mercury", 10): "Your communication skills are vital for your career success. You feel that your intellectual abilities and articulation are key to your professional reputation.",
            ("Mercury", 11): "You're actively networking and communicating with friends about your goals. Your intellectual connections within social groups help you achieve your aspirations.",
            ("Mercury", 12): "You're thinking deeply about spiritual and hidden matters. Your mind is drawn to meditation, foreign languages, or behind-the-scenes intellectual work.",

            # VENUS IN HOUSES - Based on Uttara Kalamrita & Jataka Tattva
            ("Venus", 1): "Your charm, beauty, and artistic nature are prominently displayed in your personality. You appear attractive, graceful, and harmonious to others.",
            ("Venus", 2): "You're focused on accumulating beautiful possessions and enjoying material pleasures. Your aesthetic sense helps you attract wealth and family harmony.",
            ("Venus", 3): "Your communication is charming and artistic. You feel like expressing yourself beautifully and may excel in creative writing or harmonious relationships with siblings.",
            ("Venus", 4): "You're bringing beauty and harmony to your home and family life. You feel emotionally satisfied through aesthetic pleasures and domestic comfort.",
            ("Venus", 5): "Your creativity, romance, and artistic expression are at their peak. You feel deeply romantic and may attract love through your creative talents.",
            ("Venus", 6): "You're bringing harmony to your work environment and daily routines. You feel like creating beauty in service to others and maintaining pleasant working relationships.",
            ("Venus", 7): "Your relationships and partnerships are filled with love, beauty, and harmony. You feel romantically fulfilled and attract harmonious business partnerships.",
            ("Venus", 8): "You're attracted to hidden beauty and may find pleasure in research or transformation. Your aesthetic sense is drawn to mysterious or occult subjects.",
            ("Venus", 9): "Your love of beauty extends to higher learning and spiritual wisdom. You feel attracted to foreign cultures, philosophy, or beautiful spiritual practices.",
            ("Venus", 10): "Your career benefits from your charm, artistic abilities, and harmonious nature. You feel that beauty and diplomacy are key to your professional success.",
            ("Venus", 11): "You're attracting gains through your social charm and artistic abilities. Your friendships are harmonious and you may gain through female friends or artistic networks.",
            ("Venus", 12): "You're finding beauty in solitude and spiritual practices. You feel drawn to charitable work or may find romantic connections in foreign lands.",

            # JUPITER IN HOUSES - Based on Brihat Parashara Hora Shastra
            ("Jupiter", 1): "Your wisdom, optimism, and moral authority are prominently displayed in your personality. You appear wise, generous, and naturally blessed to others.",
            ("Jupiter", 2): "You're blessed with wisdom about wealth accumulation and family values. Your moral principles guide your approach to material resources and family relationships.",
            ("Jupiter", 3): "Your communication carries wisdom and moral authority. You feel like sharing knowledge and may excel in teaching, writing, or guiding siblings.",
            ("Jupiter", 4): "Your home and family life are blessed with wisdom and spiritual growth. You feel emotionally fulfilled through higher learning and moral family values.",
            ("Jupiter", 5): "Your creativity is blessed with wisdom and you feel optimistic about children and romantic relationships. Your teaching abilities and moral guidance shine.",
            ("Jupiter", 6): "You're bringing wisdom and moral principles to your work and health routines. You feel blessed in service to others and may overcome obstacles through higher guidance.",
            ("Jupiter", 7): "Your relationships and partnerships are blessed with wisdom and moral harmony. You attract wise partners and feel guided by higher principles in relationships.",
            ("Jupiter", 8): "You're blessed with wisdom about transformation and hidden knowledge. Your moral principles guide you through deep changes and research into spiritual mysteries.",
            ("Jupiter", 9): "Your spiritual wisdom and higher learning are at their peak. You feel naturally wise and may be drawn to teaching, philosophy, or spiritual guidance.",
            ("Jupiter", 10): "Your career is blessed with wisdom and moral authority. You feel that your professional success comes through ethical behavior and spiritual principles.",
            ("Jupiter", 11): "You're blessed with wise friends and feel optimistic about achieving your goals. Your social network supports your spiritual and material growth.",
            ("Jupiter", 12): "You're blessed with spiritual wisdom and feel drawn to charitable work. Your connection to higher guidance is strong in solitude and foreign lands.",

            # SATURN IN HOUSES - Based on Jataka Parijata & Hora Sara
            ("Saturn", 1): "Your personality reflects discipline, responsibility, and serious determination. You appear mature, reliable, and committed to long-term goals.",
            ("Saturn", 2): "You're taking a disciplined approach to wealth accumulation and family responsibilities. Your patience and hard work slowly build material security.",
            ("Saturn", 3): "Your communication is serious, careful, and carries weight. You feel responsible for your words and may take a methodical approach to learning or sibling relationships.",
            ("Saturn", 4): "You're taking serious responsibility for home and family matters. You feel the weight of domestic duties but also the strength to handle long-term family commitments.",
            ("Saturn", 5): "Your approach to creativity and children is serious and disciplined. You feel responsible for proper education and may take a structured approach to creative expression.",
            ("Saturn", 6): "You're disciplined about health, work routines, and service to others. You feel committed to overcoming obstacles through patient, persistent effort.",
            ("Saturn", 7): "Your relationships and partnerships require serious commitment and responsibility. You feel that lasting relationships are built through patience and mutual duty.",
            ("Saturn", 8): "You're taking a disciplined approach to transformation and hidden matters. Your research into deep subjects is methodical and you handle crises with maturity.",
            ("Saturn", 9): "Your approach to higher learning and spirituality is disciplined and traditional. You feel committed to structured spiritual practices and ethical principles.",
            ("Saturn", 10): "Your career requires serious discipline and long-term commitment. You feel that professional success comes through patient effort and taking on major responsibilities.",
            ("Saturn", 11): "You're taking a disciplined approach to achieving your goals and may have serious responsibilities within your social groups. Gains come through persistent effort.",
            ("Saturn", 12): "You're disciplined in spiritual practices and may feel responsible for charitable work. Your approach to solitude and foreign connections is serious and committed.",

            # RAHU IN HOUSES - Based on classical texts on lunar nodes
            ("Rahu", 1): "Your personality reflects ambitious, unconventional energy. You appear unique, foreign, or unusual to others and may break traditional boundaries in self-expression.",
            ("Rahu", 2): "You're ambitiously pursuing wealth through unconventional means. Your approach to family and resources may be unusual or involve foreign elements.",
            ("Rahu", 3): "Your communication style is unconventional and you may be drawn to foreign languages or unusual subjects. Your relationship with siblings may involve unique circumstances.",
            ("Rahu", 4): "Your approach to home and family involves unconventional or foreign elements. You may feel restless about domestic security and seek unusual emotional foundations.",
            ("Rahu", 5): "Your creativity and romantic pursuits involve unconventional or foreign elements. You may be attracted to unusual forms of artistic expression or exotic romantic partners.",
            ("Rahu", 6): "Your approach to health and work involves unconventional methods. You may overcome obstacles through unusual means or work in foreign or technical fields.",
            ("Rahu", 7): "Your relationships and partnerships involve unconventional or foreign elements. You may be attracted to unusual partners or conduct business in foreign markets.",
            ("Rahu", 8): "You're drawn to unconventional research and transformation. Your interest in hidden or occult matters may involve foreign or unusual approaches to deep knowledge.",
            ("Rahu", 9): "Your approach to higher learning and spirituality involves unconventional or foreign elements. You may be drawn to unusual philosophies or foreign spiritual teachers.",
            ("Rahu", 10): "Your career involves unconventional or foreign elements. You may achieve recognition through unusual means or work in technical, foreign, or innovative fields.",
            ("Rahu", 11): "Your goals and social connections involve unconventional or foreign elements. You may gain through unusual networks or achieve ambitions through innovative means.",
            ("Rahu", 12): "Your spiritual practices and foreign connections involve unconventional approaches. You may be drawn to unusual forms of meditation or charitable work in foreign lands.",

            # KETU IN HOUSES - Based on classical texts on lunar nodes
            ("Ketu", 1): "Your personality reflects spiritual detachment and inner wisdom. You appear otherworldly or spiritually inclined to others and may be less concerned with material self-expression.",
            ("Ketu", 2): "You're developing detachment from material wealth and family attachments. Your approach to resources may be spiritually guided rather than materially motivated.",
            ("Ketu", 3): "Your communication reflects inner wisdom and you may prefer meaningful conversations over small talk. Your relationship with siblings may involve spiritual or karmic elements.",
            ("Ketu", 4): "Your approach to home and family involves spiritual detachment. You may feel emotionally distant from domestic concerns while seeking inner emotional security.",
            ("Ketu", 5): "Your creativity and romantic pursuits are guided by spiritual wisdom. You may be less attached to material creative success and more focused on inner artistic expression.",
            ("Ketu", 6): "Your approach to health and work involves spiritual detachment. You may overcome obstacles through inner strength and serve others with selfless dedication.",
            ("Ketu", 7): "Your relationships and partnerships involve spiritual detachment. You may seek deeper, more meaningful connections while being less attached to conventional relationship expectations.",
            ("Ketu", 8): "You're naturally drawn to spiritual transformation and hidden wisdom. Your research into occult or spiritual matters comes from inner knowing rather than external ambition.",
            ("Ketu", 9): "Your spiritual wisdom and detachment from conventional learning are highlighted. You may have natural access to higher knowledge through inner guidance.",
            ("Ketu", 10): "Your career may involve spiritual service or you may feel detached from conventional professional ambitions. Recognition may come through spiritual or selfless work.",
            ("Ketu", 11): "You're developing detachment from material goals while maintaining spiritual friendships. Your gains may come through spiritual networks or selfless service.",
            ("Ketu", 12): "Your spiritual practices and inner work are naturally strong. You may have natural access to meditation, foreign spiritual wisdom, or charitable service."
        }

        key = (planet, house)
        return planet_house_impacts.get(key, f"Your {planet} energy is influencing this important life area")

    def _get_house_theme(self, house: int) -> str:
        """Get the life theme for a house."""
        themes = {
            1: "personality and self-image",
            2: "wealth and family matters",
            3: "communication and siblings",
            4: "home and emotional foundation",
            5: "creativity and children",
            6: "health and daily routine",
            7: "relationships and partnerships",
            8: "transformation and hidden matters",
            9: "spirituality and higher learning",
            10: "career and public image",
            11: "gains and friendships",
            12: "spirituality and foreign connections"
        }
        return themes.get(house, "life experiences")

    def _get_fallback_combination_feeling(self, transiting_planet: str, natal_planet: str) -> str:
        """Provide clear, specific descriptions for any missing combinations."""
        planet_meanings = {
            "Sun": "confidence, leadership, and self-expression",
            "Moon": "emotions, intuition, and nurturing feelings",
            "Mercury": "communication, thinking, and mental agility",
            "Venus": "love, beauty, and artistic expression",
            "Mars": "energy, courage, and action-oriented drive",
            "Jupiter": "wisdom, optimism, and spiritual growth",
            "Saturn": "discipline, responsibility, and long-term focus",
            "Rahu": "ambition, unconventional desires, and material success",
            "Ketu": "spiritual detachment, inner wisdom, and letting go of ego"
        }

        transiting_meaning = planet_meanings.get(transiting_planet, "energy")
        natal_meaning = planet_meanings.get(natal_planet, "qualities")

        return f"Today's {transiting_meaning} is enhancing your natural {natal_meaning}. You feel a harmonious blend of these energies working together in your life."

    def _get_fallback_impact_description(self, current_planet: str, natal_planet: str) -> str:
        """Provide clear, specific impact descriptions for any missing combinations."""
        impact_templates = {
            "Sun": "Your {natal} nature is illuminated with confidence and authority today",
            "Moon": "Your {natal} qualities are emotionally enhanced and more intuitive",
            "Mercury": "Your {natal} abilities are mentally sharpened and more articulate",
            "Venus": "Your {natal} nature is beautified and more harmonious",
            "Mars": "Your {natal} qualities are energized with courage and determination",
            "Jupiter": "Your {natal} nature is blessed with wisdom and optimism",
            "Saturn": "Your {natal} qualities are disciplined and more focused",
            "Rahu": "Your {natal} nature is amplified with ambitious, unconventional energy",
            "Ketu": "Your {natal} qualities are spiritualized and more detached from ego"
        }

        planet_qualities = {
            "Sun": "leadership and self-confidence",
            "Moon": "emotional intelligence and intuition",
            "Mercury": "communication and analytical thinking",
            "Venus": "love, beauty, and artistic expression",
            "Mars": "energy, courage, and action",
            "Jupiter": "wisdom, optimism, and spiritual understanding",
            "Saturn": "discipline, patience, and responsibility",
            "Rahu": "ambition, innovation, and material desires",
            "Ketu": "spiritual wisdom, detachment, and inner knowing"
        }

        template = impact_templates.get(current_planet, "Your {natal} nature is influenced by today's energy")
        natal_quality = planet_qualities.get(natal_planet, "core qualities")

        return template.format(natal=natal_quality)

    def _calculate_daily_changes(self, positions: Dict[str, Dict[str, Any]], chart: VedicChart) -> List[str]:
        """Calculate specific daily changes the person might feel."""
        changes = []

        # Moon's daily influence (most immediate)
        moon_data = positions.get("Moon", {})
        if moon_data:
            moon_feeling = moon_data.get("themes", {}).get("feelings", "")
            if moon_feeling:
                changes.append(f"Today you may feel: {moon_feeling}")

        # Mercury's daily influence (communication/thinking)
        mercury_data = positions.get("Mercury", {})
        if mercury_data:
            mercury_feeling = mercury_data.get("themes", {}).get("feelings", "")
            if mercury_feeling:
                changes.append(f"Your communication style today: {mercury_feeling}")

        # Mars daily influence (energy/action)
        mars_data = positions.get("Mars", {})
        if mars_data:
            mars_feeling = mars_data.get("themes", {}).get("feelings", "")
            if mars_feeling:
                changes.append(f"Your energy levels: {mars_feeling}")

        return changes[:3]  # Top 3 daily changes

    def _calculate_monthly_changes(self, month_theme: Dict[str, Any], chart: VedicChart) -> List[str]:
        """Calculate monthly changes and trends."""
        changes = []

        primary_theme = month_theme.get("primary_theme", "")
        sun_sign = month_theme.get("sun_sign", "")

        changes.append(f"This month's focus: {primary_theme}")
        changes.append(f"With Sun in {sun_sign}, you're experiencing themes of {primary_theme.lower()}")

        # Add secondary influences
        secondary = month_theme.get("secondary_influences", [])
        for influence in secondary[:2]:
            changes.append(f"Additional influence: {influence}")

        return changes

    def _get_current_recommendations(self, positions: Dict[str, Dict[str, Any]], chart: VedicChart) -> List[str]:
        """Get recommendations based on current influences."""
        recommendations = []

        # Based on strongest current planetary influence
        strongest_influences = ["Jupiter", "Venus", "Sun", "Moon", "Mercury"]

        for planet in strongest_influences:
            if planet in positions:
                planet_data = positions[planet]
                themes = planet_data.get("themes", {})
                daily_theme = themes.get("daily_theme", "")

                if daily_theme:
                    if planet == "Jupiter":
                        recommendations.append("Focus on learning and spiritual growth today")
                    elif planet == "Venus":
                        recommendations.append("Good time for relationships and creative activities")
                    elif planet == "Sun":
                        recommendations.append("Take leadership roles and express yourself confidently")
                    elif planet == "Moon":
                        recommendations.append("Trust your intuition and focus on emotional well-being")
                    elif planet == "Mercury":
                        recommendations.append("Engage in communication, learning, and networking")

                if len(recommendations) >= 3:
                    break

        return recommendations[:3]
