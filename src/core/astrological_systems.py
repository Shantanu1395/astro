"""
Abstract base classes and interfaces for multi-astrological system architecture.

This module defines the core interfaces that all astrological systems must implement,
enabling seamless integration of Vedic, Western, Chinese, and other systems.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date

from src.models.models import (
    BirthData, LocationData, Chart, Prediction, AstrologySystem, 
    PredictionType, EnhancedPredictionRequest, SubscriptionTier
)


class AstrologicalCalculator(ABC):
    """Abstract base class for all astrological calculation engines."""
    
    def __init__(self, system: AstrologySystem):
        self.system = system
    
    @abstractmethod
    def calculate_chart(self, birth_data: BirthData, location_data: LocationData) -> Chart:
        """Calculate birth chart for the specific astrological system."""
        pass
    
    @abstractmethod
    def calculate_current_transits(self, birth_chart: Chart, current_date: datetime) -> Dict[str, Any]:
        """Calculate current planetary transits affecting the birth chart."""
        pass
    
    @abstractmethod
    def calculate_planetary_periods(self, birth_chart: Chart) -> List[Dict[str, Any]]:
        """Calculate planetary periods/cycles specific to the system."""
        pass
    
    @abstractmethod
    def calculate_planetary_strengths(self, birth_chart: Chart) -> Dict[str, float]:
        """Calculate planetary strength scores (0.0 to 1.0)."""
        pass


class PredictionEngine(ABC):
    """Abstract base class for all prediction engines."""
    
    def __init__(self, system: AstrologySystem, calculator: AstrologicalCalculator):
        self.system = system
        self.calculator = calculator
    
    @abstractmethod
    def generate_prediction(self, request: EnhancedPredictionRequest, chart: Chart) -> Prediction:
        """Generate prediction based on request and chart."""
        pass
    
    @abstractmethod
    def get_supported_prediction_types(self) -> List[PredictionType]:
        """Get list of prediction types supported by this engine."""
        pass
    
    @abstractmethod
    def validate_request(self, request: EnhancedPredictionRequest) -> Tuple[bool, Optional[str]]:
        """Validate if request can be processed by this engine."""
        pass


class RemedialSystem(ABC):
    """Abstract base class for remedial recommendation systems."""
    
    def __init__(self, system: AstrologySystem):
        self.system = system
    
    @abstractmethod
    def get_remedies(self, chart: Chart, focus_area: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get remedial recommendations for the chart."""
        pass
    
    @abstractmethod
    def get_timing_for_remedies(self, chart: Chart, remedies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get optimal timing for implementing remedies."""
        pass


class CrossSystemAnalyzer(ABC):
    """Abstract base class for cross-system analysis."""
    
    @abstractmethod
    def find_common_themes(self, predictions: List[Prediction]) -> Dict[str, Any]:
        """Find common themes across different astrological systems."""
        pass
    
    @abstractmethod
    def synthesize_predictions(self, predictions: List[Prediction]) -> Dict[str, Any]:
        """Create unified prediction from multiple systems."""
        pass
    
    @abstractmethod
    def calculate_convergence_score(self, predictions: List[Prediction]) -> float:
        """Calculate how much different systems agree (0.0 to 1.0)."""
        pass


class AstrologicalSystemInterface(ABC):
    """Main interface that each astrological system must implement."""
    
    def __init__(self, system: AstrologySystem):
        self.system = system
        self.calculator = self._create_calculator()
        self.prediction_engine = self._create_prediction_engine()
        self.remedial_system = self._create_remedial_system()
    
    @abstractmethod
    def _create_calculator(self) -> AstrologicalCalculator:
        """Create system-specific calculator."""
        pass
    
    @abstractmethod
    def _create_prediction_engine(self) -> PredictionEngine:
        """Create system-specific prediction engine."""
        pass
    
    @abstractmethod
    def _create_remedial_system(self) -> RemedialSystem:
        """Create system-specific remedial system."""
        pass
    
    def process_request(self, request: EnhancedPredictionRequest, location_data: LocationData) -> Prediction:
        """Process a complete prediction request."""
        # Calculate chart
        chart = self.calculator.calculate_chart(request.birth_data, location_data)
        
        # Generate prediction
        prediction = self.prediction_engine.generate_prediction(request, chart)
        
        return prediction
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get information about this astrological system."""
        return {
            "system": self.system.value,
            "supported_prediction_types": [pt.value for pt in self.prediction_engine.get_supported_prediction_types()],
            "features": self._get_system_features()
        }
    
    @abstractmethod
    def _get_system_features(self) -> List[str]:
        """Get list of features supported by this system."""
        pass


# ===== SYSTEM REGISTRY =====

class SystemRegistry:
    """Registry for managing all available astrological systems."""
    
    def __init__(self):
        self._systems: Dict[AstrologySystem, AstrologicalSystemInterface] = {}
    
    def register_system(self, system_interface: AstrologicalSystemInterface):
        """Register a new astrological system."""
        self._systems[system_interface.system] = system_interface
    
    def get_system(self, system: AstrologySystem) -> Optional[AstrologicalSystemInterface]:
        """Get a registered system interface."""
        return self._systems.get(system)
    
    def get_available_systems(self) -> List[AstrologySystem]:
        """Get list of all available systems."""
        return list(self._systems.keys())
    
    def is_system_available(self, system: AstrologySystem) -> bool:
        """Check if a system is available."""
        return system in self._systems


# Global system registry instance
system_registry = SystemRegistry()
