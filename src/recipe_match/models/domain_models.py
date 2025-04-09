"""Domain models for the Recipe Match application.

These models represent core business entities used across the application.
"""

from typing import Optional
from pydantic import BaseModel

class Ingredient(BaseModel):
    """Model representing a recipe ingredient with measurement."""
    name: str
    measurement: Optional[str] = None 