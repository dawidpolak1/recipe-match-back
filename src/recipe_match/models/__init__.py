"""
Models for the Recipe Match application.

This package contains all the data models used in the application,
including API models, domain models, and response models.
"""

# Import models to expose them at the package level
from recipe_match.models.api_models import Meal, MealList, MealSummary
from recipe_match.models.domain_models import Ingredient
from recipe_match.models.response_models import DetailMealResponse, MealSummaryResponse, ErrorResponse

# Export all models
__all__ = [
    'Meal',
    'MealList',
    'MealSummary',
    'Ingredient',
    'DetailMealResponse',
    'MealSummaryResponse',
    'ErrorResponse',
] 