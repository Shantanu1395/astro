"""
Pricing and subscription tier management system.

This module handles subscription tiers, feature access validation,
and pricing rules for different astrological services.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

from models import (
    SubscriptionTier, AstrologySystem, PredictionType, DetailLevel,
    EnhancedPredictionRequest, PricingRule, FeatureAccess
)


class PricingEngine:
    """Engine for managing pricing, tiers, and feature access."""
    
    def __init__(self):
        self.pricing_rules = self._initialize_pricing_rules()
        self.user_usage: Dict[str, Dict] = {}  # In production, this would be a database
    
    def _initialize_pricing_rules(self) -> Dict[SubscriptionTier, PricingRule]:
        """Initialize pricing rules for all subscription tiers."""
        return {
            SubscriptionTier.FREE: PricingRule(
                tier=SubscriptionTier.FREE,
                allowed_systems=[AstrologySystem.VEDIC],
                allowed_prediction_types=[PredictionType.CURRENT_PERIOD],
                max_requests_per_month=5,
                includes_cross_system_analysis=False,
                includes_detailed_timing=False,
                includes_personalized_remedies=False,
                cost_per_request=0.0
            ),
            SubscriptionTier.SILVER: PricingRule(
                tier=SubscriptionTier.SILVER,
                allowed_systems=[AstrologySystem.VEDIC, AstrologySystem.WESTERN],  # Can choose one
                allowed_prediction_types=[
                    PredictionType.CURRENT_PERIOD,
                    PredictionType.YEARLY,
                    PredictionType.MONTHLY,
                    PredictionType.CAREER,
                    PredictionType.RELATIONSHIP,
                    PredictionType.HEALTH
                ],
                max_requests_per_month=50,
                includes_cross_system_analysis=False,
                includes_detailed_timing=True,
                includes_personalized_remedies=True,
                cost_per_request=2.99
            ),
            SubscriptionTier.GOLD: PricingRule(
                tier=SubscriptionTier.GOLD,
                allowed_systems=[
                    AstrologySystem.VEDIC,
                    AstrologySystem.WESTERN,
                    AstrologySystem.CHINESE,
                    AstrologySystem.MAYAN
                ],
                allowed_prediction_types=list(PredictionType),  # All types
                max_requests_per_month=200,
                includes_cross_system_analysis=True,
                includes_detailed_timing=True,
                includes_personalized_remedies=True,
                cost_per_request=9.99
            )
        }
    
    def validate_request(self, request: EnhancedPredictionRequest, user_id: str) -> FeatureAccess:
        """Validate if user can access requested features."""
        tier = request.subscription_tier
        pricing_rule = self.pricing_rules[tier]
        
        # Check system access
        can_access_system = request.system in pricing_rule.allowed_systems
        
        # Check prediction type access
        can_access_prediction_type = request.prediction_type in pricing_rule.allowed_prediction_types
        
        # Check cross-system access (for future multi-system requests)
        can_access_cross_system = pricing_rule.includes_cross_system_analysis
        
        # Check usage limits
        remaining_requests = self._get_remaining_requests(user_id, tier)
        
        # Determine if upgrade is required
        upgrade_required = False
        upgrade_message = None
        
        if not can_access_system:
            upgrade_required = True
            upgrade_message = f"System '{request.system.value}' requires {self._get_minimum_tier_for_system(request.system).value} tier or higher"
        
        elif not can_access_prediction_type:
            upgrade_required = True
            upgrade_message = f"Prediction type '{request.prediction_type.value}' requires {self._get_minimum_tier_for_prediction_type(request.prediction_type).value} tier or higher"
        
        elif remaining_requests <= 0:
            upgrade_required = True
            upgrade_message = f"Monthly request limit reached. Upgrade to increase limit."
        
        return FeatureAccess(
            tier=tier,
            can_access_system=can_access_system,
            can_access_prediction_type=can_access_prediction_type,
            can_access_cross_system=can_access_cross_system,
            remaining_requests=remaining_requests,
            upgrade_required=upgrade_required,
            upgrade_message=upgrade_message
        )
    
    def _get_remaining_requests(self, user_id: str, tier: SubscriptionTier) -> int:
        """Get remaining requests for user this month."""
        current_month = datetime.now().strftime("%Y-%m")
        
        if user_id not in self.user_usage:
            self.user_usage[user_id] = {}
        
        if current_month not in self.user_usage[user_id]:
            self.user_usage[user_id][current_month] = 0
        
        used_requests = self.user_usage[user_id][current_month]
        max_requests = self.pricing_rules[tier].max_requests_per_month
        
        return max(0, max_requests - used_requests)
    
    def record_request(self, user_id: str) -> None:
        """Record a request for usage tracking."""
        current_month = datetime.now().strftime("%Y-%m")
        
        if user_id not in self.user_usage:
            self.user_usage[user_id] = {}
        
        if current_month not in self.user_usage[user_id]:
            self.user_usage[user_id][current_month] = 0
        
        self.user_usage[user_id][current_month] += 1
    
    def _get_minimum_tier_for_system(self, system: AstrologySystem) -> SubscriptionTier:
        """Get minimum tier required for a system."""
        for tier, rule in self.pricing_rules.items():
            if system in rule.allowed_systems:
                return tier
        return SubscriptionTier.GOLD  # Default to highest tier
    
    def _get_minimum_tier_for_prediction_type(self, prediction_type: PredictionType) -> SubscriptionTier:
        """Get minimum tier required for a prediction type."""
        for tier, rule in self.pricing_rules.items():
            if prediction_type in rule.allowed_prediction_types:
                return tier
        return SubscriptionTier.GOLD  # Default to highest tier
    
    def get_tier_features(self, tier: SubscriptionTier) -> Dict[str, any]:
        """Get detailed features for a subscription tier."""
        rule = self.pricing_rules[tier]
        
        return {
            "tier": tier.value,
            "monthly_cost": rule.cost_per_request * rule.max_requests_per_month if rule.cost_per_request > 0 else 0,
            "cost_per_request": rule.cost_per_request,
            "max_requests_per_month": rule.max_requests_per_month,
            "allowed_systems": [system.value for system in rule.allowed_systems],
            "allowed_prediction_types": [pt.value for pt in rule.allowed_prediction_types],
            "features": {
                "cross_system_analysis": rule.includes_cross_system_analysis,
                "detailed_timing": rule.includes_detailed_timing,
                "personalized_remedies": rule.includes_personalized_remedies
            }
        }
    
    def get_all_tier_comparison(self) -> Dict[str, Dict[str, any]]:
        """Get comparison of all subscription tiers."""
        return {
            tier.value: self.get_tier_features(tier)
            for tier in SubscriptionTier
        }
    
    def calculate_upgrade_benefits(self, current_tier: SubscriptionTier, target_tier: SubscriptionTier) -> Dict[str, any]:
        """Calculate benefits of upgrading from current to target tier."""
        current_features = self.get_tier_features(current_tier)
        target_features = self.get_tier_features(target_tier)
        
        return {
            "additional_systems": list(set(target_features["allowed_systems"]) - set(current_features["allowed_systems"])),
            "additional_prediction_types": list(set(target_features["allowed_prediction_types"]) - set(current_features["allowed_prediction_types"])),
            "additional_requests": target_features["max_requests_per_month"] - current_features["max_requests_per_month"],
            "new_features": {
                feature: target_features["features"][feature]
                for feature in target_features["features"]
                if not current_features["features"].get(feature, False)
            },
            "cost_difference": target_features["monthly_cost"] - current_features["monthly_cost"]
        }


# Global pricing engine instance
pricing_engine = PricingEngine()
