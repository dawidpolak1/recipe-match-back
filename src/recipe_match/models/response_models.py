"""Response models for the Recipe Match API.

These models define the structure of responses returned by our API endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel

from recipe_match.models.domain_models import Ingredient

class MealResponse(BaseModel):
    """Model representing the API response for a meal."""
    id: str
    name: str
    category: Optional[str] = None
    area: Optional[str] = None
    instructions: Optional[str] = None
    thumbnail: Optional[str] = None
    tags: Optional[str] = None
    youtube: Optional[str] = None
    ingredients: Optional[List[Ingredient]] = None

class ErrorResponse(BaseModel):
    """Model representing an error response."""
    detail: str 