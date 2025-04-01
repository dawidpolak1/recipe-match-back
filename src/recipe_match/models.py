from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    """Model representing a recipe ingredient with measurement."""
    name: str
    measurement: Optional[str] = None

class Meal(BaseModel):
    """Model representing a meal from TheMealDB API."""
    id: str = Field(..., alias="idMeal")
    name: str = Field(..., alias="strMeal")
    category: Optional[str] = Field(None, alias="strCategory")
    area: Optional[str] = Field(None, alias="strArea")
    instructions: Optional[str] = Field(None, alias="strInstructions")
    thumbnail: Optional[str] = Field(None, alias="strMealThumb")
    tags: Optional[str] = Field(None, alias="strTags")
    youtube: Optional[str] = Field(None, alias="strYoutube")
    ingredients: Optional[List[Ingredient]] = None
    
    class Config:
        """Pydantic config for the Meal model."""
        populate_by_name = True
        # This is crucial - it tells Pydantic to use the model field names in the JSON output
        alias_generator = None
        json_encoders = {
            # Add any custom serialization here if needed
        }

class MealList(BaseModel):
    """Model representing a list of meals."""
    meals: Optional[List[Meal]] = None

class ErrorResponse(BaseModel):
    """Model representing an error response."""
    detail: str 