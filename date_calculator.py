"""
Date Calculator for Astrological Events and Periods
Calculates specific dates for favorable and challenging periods
"""

from datetime import date, datetime, timedelta
from typing import List, Dict, Tuple, Any
import swisseph as swe
from models import DashaPeriod, BirthData, LocationData
from utils import julian_day_from_datetime, calculate_ayanamsa, degrees_to_sign_and_degree

class AstrologicalDateCalculator:
    def __init__(self):
        # Dasha sequence for calculations
        self.dasha_sequence = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        self.dasha_periods = {
            "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
            "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
        }
        
        # Antardasha proportions (simplified)
        self.antardasha_proportions = {
            "Ketu": 0.49, "Venus": 3.33, "Sun": 0.30, "Moon": 0.70, "Mars": 0.49,
            "Rahu": 1.80, "Jupiter": 1.07, "Saturn": 1.33, "Mercury": 1.19
        }

    def calculate_favorable_periods(self, current_dasha: DashaPeriod, birth_data: BirthData) -> List[Dict[str, Any]]:
        """Calculate specific favorable periods with dates."""
        favorable_periods = []
        current_date = date.today()
        
        # Current dasha favorable sub-periods
        if current_dasha.planet in ["Jupiter", "Venus", "Mercury", "Moon"]:
            # These are generally favorable planets
            favorable_periods.extend(self._get_current_dasha_favorable_periods(current_dasha, current_date))
        
        # Upcoming favorable transits
        favorable_periods.extend(self._get_favorable_transit_periods(current_date))
        
        # Festival and auspicious periods
        favorable_periods.extend(self._get_auspicious_periods(current_date))
        
        return sorted(favorable_periods, key=lambda x: x['start_date'])

    def calculate_challenging_periods(self, current_dasha: DashaPeriod, birth_data: BirthData) -> List[Dict[str, Any]]:
        """Calculate specific challenging periods with dates."""
        challenging_periods = []
        current_date = date.today()
        
        # Current dasha challenging aspects
        if current_dasha.planet in ["Saturn", "Rahu", "Ketu", "Mars"]:
            challenging_periods.extend(self._get_current_dasha_challenging_periods(current_dasha, current_date))
        
        # Eclipse periods
        challenging_periods.extend(self._get_eclipse_periods(current_date))
        
        # Retrograde periods
        challenging_periods.extend(self._get_retrograde_periods(current_date))
        
        # Challenging transits
        challenging_periods.extend(self._get_challenging_transit_periods(current_date))
        
        return sorted(challenging_periods, key=lambda x: x['start_date'])

    def _get_current_dasha_favorable_periods(self, current_dasha: DashaPeriod, current_date: date) -> List[Dict[str, Any]]:
        """Get favorable sub-periods within current dasha."""
        periods = []
        
        # Calculate antardasha periods
        remaining_days = (current_dasha.end_date - current_date).days
        if remaining_days > 0:
            # Next 6 months of favorable antardashas
            favorable_antardashas = ["Jupiter", "Venus", "Mercury", "Moon"]
            
            for i, antardasha_lord in enumerate(favorable_antardashas):
                if antardasha_lord != current_dasha.planet:  # Avoid same planet
                    start_date = current_date + timedelta(days=i*45)  # Approximate 45-day periods
                    end_date = start_date + timedelta(days=45)
                    
                    if start_date < current_dasha.end_date:
                        periods.append({
                            "type": "Favorable Antardasha",
                            "period": f"{current_dasha.planet}-{antardasha_lord}",
                            "start_date": start_date,
                            "end_date": min(end_date, current_dasha.end_date),
                            "description": f"{antardasha_lord} antardasha brings positive energy within {current_dasha.planet} mahadasha",
                            "guidance": self._get_antardasha_guidance(current_dasha.planet, antardasha_lord)
                        })
        
        return periods

    def _get_current_dasha_challenging_periods(self, current_dasha: DashaPeriod, current_date: date) -> List[Dict[str, Any]]:
        """Get challenging sub-periods within current dasha."""
        periods = []
        
        if current_dasha.planet in ["Saturn", "Rahu", "Ketu"]:
            # These dashas have inherent challenges
            challenging_months = self._get_challenging_months_in_dasha(current_dasha.planet, current_date)
            
            for month_info in challenging_months:
                periods.append({
                    "type": "Challenging Dasha Period",
                    "period": f"{current_dasha.planet} Intensity",
                    "start_date": month_info["start"],
                    "end_date": month_info["end"],
                    "description": month_info["description"],
                    "cautions": month_info["cautions"]
                })
        
        return periods

    def _get_challenging_months_in_dasha(self, dasha_planet: str, current_date: date) -> List[Dict[str, Any]]:
        """Get specific challenging months within a dasha."""
        challenging_months = []
        
        if dasha_planet == "Saturn":
            # Saturn's challenging periods
            for i in range(3):  # Next 3 challenging periods
                start_date = current_date + timedelta(days=i*120)  # Every 4 months
                end_date = start_date + timedelta(days=30)
                
                challenging_months.append({
                    "start": start_date,
                    "end": end_date,
                    "description": "Saturn's intensified influence - period of karmic lessons",
                    "cautions": "Avoid major decisions, practice patience, focus on discipline"
                })
        
        elif dasha_planet == "Rahu":
            # Rahu's challenging periods
            for i in range(4):  # Next 4 challenging periods
                start_date = current_date + timedelta(days=i*90)  # Every 3 months
                end_date = start_date + timedelta(days=21)
                
                challenging_months.append({
                    "start": start_date,
                    "end": end_date,
                    "description": "Rahu's intensified influence - period of illusions and ambitions",
                    "cautions": "Avoid speculation, verify information, stay grounded"
                })
        
        return challenging_months

    def _get_favorable_transit_periods(self, current_date: date) -> List[Dict[str, Any]]:
        """Calculate favorable transit periods."""
        periods = []
        
        # Jupiter favorable transits (approximate)
        jupiter_periods = [
            {
                "start": current_date + timedelta(days=30),
                "end": current_date + timedelta(days=60),
                "description": "Jupiter's favorable aspect brings wisdom and opportunities"
            },
            {
                "start": current_date + timedelta(days=120),
                "end": current_date + timedelta(days=150),
                "description": "Jupiter's blessing period for new ventures and learning"
            }
        ]
        
        for period in jupiter_periods:
            periods.append({
                "type": "Favorable Transit",
                "period": "Jupiter Blessing",
                "start_date": period["start"],
                "end_date": period["end"],
                "description": period["description"],
                "guidance": "Excellent time for education, spiritual practices, and new beginnings"
            })
        
        return periods

    def _get_auspicious_periods(self, current_date: date) -> List[Dict[str, Any]]:
        """Get traditional auspicious periods."""
        periods = []
        year = current_date.year
        
        # Major Hindu festivals and auspicious periods (approximate dates)
        auspicious_dates = [
            {"name": "Diwali Period", "month": 10, "duration": 5, "description": "Most auspicious period for new ventures"},
            {"name": "Navratri", "month": 3, "duration": 9, "description": "Powerful period for spiritual practices"},
            {"name": "Navratri", "month": 9, "duration": 9, "description": "Excellent for new beginnings"},
            {"name": "Akshaya Tritiya", "month": 4, "duration": 1, "description": "Highly auspicious for investments"},
        ]
        
        for festival in auspicious_dates:
            try:
                start_date = date(year, festival["month"], 15)  # Approximate mid-month
                if start_date < current_date:
                    start_date = date(year + 1, festival["month"], 15)
                
                end_date = start_date + timedelta(days=festival["duration"])
                
                periods.append({
                    "type": "Auspicious Period",
                    "period": festival["name"],
                    "start_date": start_date,
                    "end_date": end_date,
                    "description": festival["description"],
                    "guidance": "Ideal time for important ceremonies, investments, and new ventures"
                })
            except ValueError:
                continue  # Skip invalid dates
        
        return periods

    def _get_eclipse_periods(self, current_date: date) -> List[Dict[str, Any]]:
        """Calculate upcoming eclipse periods (approximate)."""
        periods = []
        
        # Eclipses occur roughly every 6 months
        eclipse_dates = []
        for i in range(4):  # Next 4 eclipse seasons
            eclipse_date = current_date + timedelta(days=i*180)  # Approximate 6-month intervals
            eclipse_dates.append(eclipse_date)
        
        for eclipse_date in eclipse_dates:
            periods.append({
                "type": "Eclipse Period",
                "period": "Solar/Lunar Eclipse",
                "start_date": eclipse_date - timedelta(days=3),
                "end_date": eclipse_date + timedelta(days=3),
                "description": "Eclipse period - time of transformation and caution",
                "cautions": "Avoid important decisions, practice meditation, be extra careful"
            })
        
        return periods

    def _get_retrograde_periods(self, current_date: date) -> List[Dict[str, Any]]:
        """Calculate retrograde periods (approximate)."""
        periods = []
        
        # Mercury retrograde occurs 3-4 times per year
        mercury_retrogrades = []
        for i in range(4):  # Next 4 Mercury retrogrades
            retrograde_start = current_date + timedelta(days=i*120)  # Approximate 4-month intervals
            mercury_retrogrades.append(retrograde_start)
        
        for retrograde_start in mercury_retrogrades:
            periods.append({
                "type": "Retrograde Period",
                "period": "Mercury Retrograde",
                "start_date": retrograde_start,
                "end_date": retrograde_start + timedelta(days=21),  # Typical 3-week duration
                "description": "Mercury retrograde - communication and technology challenges",
                "cautions": "Double-check communications, backup data, avoid signing contracts"
            })
        
        return periods

    def _get_challenging_transit_periods(self, current_date: date) -> List[Dict[str, Any]]:
        """Calculate challenging transit periods."""
        periods = []
        
        # Saturn challenging transits
        saturn_challenges = [
            {
                "start": current_date + timedelta(days=45),
                "end": current_date + timedelta(days=75),
                "description": "Saturn's challenging aspect - period of tests and delays"
            }
        ]
        
        for period in saturn_challenges:
            periods.append({
                "type": "Challenging Transit",
                "period": "Saturn Challenge",
                "start_date": period["start"],
                "end_date": period["end"],
                "description": period["description"],
                "cautions": "Practice patience, avoid major changes, focus on discipline"
            })
        
        return periods

    def _get_antardasha_guidance(self, mahadasha: str, antardasha: str) -> str:
        """Get specific guidance for antardasha combinations."""
        combinations = {
            ("Saturn", "Jupiter"): "Use Jupiter's wisdom to navigate Saturn's challenges",
            ("Rahu", "Venus"): "Channel Rahu's ambition through Venus's harmony",
            ("Mars", "Mercury"): "Combine Mars's energy with Mercury's intelligence",
            ("Jupiter", "Venus"): "Excellent period for wealth and spiritual growth"
        }
        
        key = (mahadasha, antardasha)
        return combinations.get(key, f"Blend {mahadasha}'s energy with {antardasha}'s influence")

    def get_next_major_dasha_transition(self, current_dasha: DashaPeriod) -> Dict[str, Any]:
        """Calculate the next major dasha transition."""
        current_index = self.dasha_sequence.index(current_dasha.planet)
        next_index = (current_index + 1) % len(self.dasha_sequence)
        next_planet = self.dasha_sequence[next_index]
        
        return {
            "next_dasha_planet": next_planet,
            "transition_date": current_dasha.end_date,
            "preparation_period": current_dasha.end_date - timedelta(days=365),  # 1 year before
            "significance": f"Transition from {current_dasha.planet} to {next_planet} energy",
            "preparation_guidance": f"Prepare for {next_planet}'s influence by understanding its themes and requirements"
        }
