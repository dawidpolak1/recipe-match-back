from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Any

from recipe_match.recipe_discovery import find_recipes_by_ingredients
from recipe_match.models import ErrorResponse

# Create a router for local recipe database endpoints
router = APIRouter(
    prefix="/local-recipes",
    tags=["local-recipes"],
    responses={404: {"model": ErrorResponse}},
)

@router.get("/by-ingredients", response_model=List[Dict[str, Any]])
async def get_recipes_by_ingredients(
    ingredients: List[str] = Query(..., description="List of available ingredients"),
    match_threshold: float = Query(0.5, description="Minimum proportion of recipe ingredients that must be available", ge=0.0, le=1.0)
):
    """
    Find recipes that can be made with the provided ingredients from our local database.
    
    Args:
        ingredients: List of ingredients available to the user
        match_threshold: Minimum proportion of recipe ingredients that must be available (default: 0.5)
    
    Returns:
        List of matching recipes, sorted by match percentage (highest first)
    """
    if not ingredients:
        raise HTTPException(status_code=400, detail="At least one ingredient must be provided")
    
    matching_recipes = find_recipes_by_ingredients(ingredients, match_threshold)
    
    if not matching_recipes:
        return []
    
    return matching_recipes  