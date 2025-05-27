"""
System Manager for Multi-Astrological System Architecture.

This module provides the main interface for managing all astrological systems,
handling requests, validation, and cross-system analysis.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from models import (
    BirthData, LocationData, AstrologySystem, PredictionType,
    EnhancedPredictionRequest, SubscriptionTier, FeatureAccess
)
from astrological_systems import (
    AstrologicalSystemInterface, system_registry, CrossSystemAnalyzer,
    Chart, Prediction
)
from pricing_system import pricing_engine
from vedic_system import VedicSystem
from other_systems import WesternSystem, ChineseSystem, MayanSystem


class UniversalCrossSystemAnalyzer(CrossSystemAnalyzer):
    """Implementation of cross-system analysis."""
    
    def find_common_themes(self, predictions: List[Prediction]) -> Dict[str, Any]:
        """Find common themes across different astrological systems."""
        if len(predictions) < 2:
            return {"common_themes": [], "note": "Need at least 2 systems for comparison"}
        
        # Extract themes from all predictions
        all_themes = []
        for prediction in predictions:
            all_themes.extend(prediction.key_themes)
        
        # Find themes that appear in multiple systems
        theme_counts = {}
        for theme in all_themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        common_themes = [
            {"theme": theme, "systems_count": count, "agreement_level": count / len(predictions)}
            for theme, count in theme_counts.items()
            if count > 1
        ]
        
        # Sort by agreement level
        common_themes.sort(key=lambda x: x["agreement_level"], reverse=True)
        
        return {
            "common_themes": common_themes,
            "total_systems": len(predictions),
            "convergence_areas": [theme["theme"] for theme in common_themes[:3]]
        }
    
    def synthesize_predictions(self, predictions: List[Prediction]) -> Dict[str, Any]:
        """Create unified prediction from multiple systems."""
        if not predictions:
            return {"error": "No predictions to synthesize"}
        
        # Combine prediction texts
        combined_text = "\n\n".join([
            f"**{pred.system.value.title()} Perspective:**\n{pred.prediction_text}"
            for pred in predictions
        ])
        
        # Find common themes
        common_themes = self.find_common_themes(predictions)
        
        # Calculate average confidence
        avg_confidence = sum(pred.confidence_score for pred in predictions) / len(predictions)
        
        return {
            "unified_prediction": combined_text,
            "common_themes": common_themes["common_themes"],
            "systems_analyzed": [pred.system.value for pred in predictions],
            "overall_confidence": avg_confidence,
            "convergence_score": self.calculate_convergence_score(predictions),
            "synthesis_note": "This unified reading combines insights from multiple astrological traditions."
        }
    
    def calculate_convergence_score(self, predictions: List[Prediction]) -> float:
        """Calculate how much different systems agree (0.0 to 1.0)."""
        if len(predictions) < 2:
            return 1.0
        
        common_themes = self.find_common_themes(predictions)
        total_themes = sum(len(pred.key_themes) for pred in predictions)
        common_theme_count = len(common_themes["common_themes"])
        
        if total_themes == 0:
            return 0.0
        
        # Simple convergence calculation based on theme overlap
        convergence = (common_theme_count * 2) / total_themes
        return min(1.0, convergence)


class SystemManager:
    """Main manager for all astrological systems."""
    
    def __init__(self):
        self.cross_system_analyzer = UniversalCrossSystemAnalyzer()
        self._initialize_systems()
    
    def _initialize_systems(self):
        """Initialize and register all astrological systems."""
        # Register Vedic system (fully implemented)
        vedic_system = VedicSystem()
        system_registry.register_system(vedic_system)
        
        # Register other systems (stubs for now)
        western_system = WesternSystem()
        chinese_system = ChineseSystem()
        # mayan_system = MayanSystem()  # Commented out as it's incomplete
        
        system_registry.register_system(western_system)
        system_registry.register_system(chinese_system)
        # system_registry.register_system(mayan_system)
    
    def process_prediction_request(self, request: EnhancedPredictionRequest, 
                                 location_data: LocationData, user_id: str) -> Dict[str, Any]:
        """Process a complete prediction request with validation and pricing."""
        
        # Validate subscription tier and feature access
        feature_access = pricing_engine.validate_request(request, user_id)
        
        if feature_access.upgrade_required:
            return {
                "success": False,
                "error": "upgrade_required",
                "message": feature_access.upgrade_message,
                "feature_access": feature_access.dict(),
                "upgrade_options": self._get_upgrade_options(request.subscription_tier)
            }
        
        # Get the requested system
        system = system_registry.get_system(request.system)
        if not system:
            return {
                "success": False,
                "error": "system_not_available",
                "message": f"System '{request.system.value}' is not available",
                "available_systems": [s.value for s in system_registry.get_available_systems()]
            }
        
        try:
            # Process the prediction
            prediction = system.process_request(request, location_data)
            
            # Record usage for billing/limits
            pricing_engine.record_request(user_id)
            
            # Prepare response
            response = {
                "success": True,
                "prediction": {
                    "system": prediction.system.value,
                    "prediction_type": prediction.prediction_type.value,
                    "text": prediction.prediction_text,
                    "key_themes": prediction.key_themes,
                    "confidence_score": prediction.confidence_score,
                    "timing_information": prediction.get_timing_information(),
                    "remedial_suggestions": prediction.get_remedial_suggestions(),
                    "generated_at": prediction.generated_at.isoformat()
                },
                "feature_access": feature_access.dict()
            }
            
            # Add cross-system analysis for Gold tier
            if (request.subscription_tier == SubscriptionTier.GOLD and 
                feature_access.can_access_cross_system):
                response["cross_system_analysis"] = self._generate_cross_system_preview(
                    request, location_data, prediction
                )
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": "processing_error",
                "message": f"Error processing prediction: {str(e)}"
            }
    
    def _generate_cross_system_preview(self, request: EnhancedPredictionRequest, 
                                     location_data: LocationData, 
                                     primary_prediction: Prediction) -> Dict[str, Any]:
        """Generate cross-system analysis preview for Gold tier users."""
        predictions = [primary_prediction]
        
        # Generate predictions from other available systems
        for system_type in system_registry.get_available_systems():
            if system_type != request.system:
                try:
                    system = system_registry.get_system(system_type)
                    other_request = EnhancedPredictionRequest(
                        birth_data=request.birth_data,
                        system=system_type,
                        prediction_type=request.prediction_type,
                        subscription_tier=request.subscription_tier
                    )
                    other_prediction = system.process_request(other_request, location_data)
                    predictions.append(other_prediction)
                except Exception as e:
                    # Skip systems that fail
                    continue
        
        if len(predictions) > 1:
            return self.cross_system_analyzer.synthesize_predictions(predictions)
        else:
            return {"note": "Cross-system analysis requires multiple working systems"}
    
    def _get_upgrade_options(self, current_tier: SubscriptionTier) -> Dict[str, Any]:
        """Get upgrade options for current tier."""
        upgrade_options = {}
        
        for tier in SubscriptionTier:
            if tier.value > current_tier.value:  # Higher tier
                benefits = pricing_engine.calculate_upgrade_benefits(current_tier, tier)
                upgrade_options[tier.value] = {
                    "tier": tier.value,
                    "benefits": benefits,
                    "features": pricing_engine.get_tier_features(tier)
                }
        
        return upgrade_options
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all astrological systems."""
        systems_status = {}
        
        for system_type in AstrologySystem:
            system = system_registry.get_system(system_type)
            if system:
                systems_status[system_type.value] = {
                    "available": True,
                    "info": system.get_system_info(),
                    "status": "operational"
                }
            else:
                systems_status[system_type.value] = {
                    "available": False,
                    "status": "not_implemented"
                }
        
        return {
            "systems": systems_status,
            "total_available": len(system_registry.get_available_systems()),
            "cross_system_analysis": True
        }
    
    def get_pricing_info(self) -> Dict[str, Any]:
        """Get complete pricing information."""
        return {
            "tiers": pricing_engine.get_all_tier_comparison(),
            "features_by_tier": {
                tier.value: pricing_engine.get_tier_features(tier)
                for tier in SubscriptionTier
            }
        }


# Global system manager instance
system_manager = SystemManager()
