from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, List, Any

from recipe_match.api_client import MealDBClient
from recipe_match.models import MealList, ErrorResponse
from recipe_match.recipe_discovery import find_recipes_by_ingredients

# Create a router for recipe-related endpoints
router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    responses={404: {"model": ErrorResponse}},
)

# Dependency to get the MealDB client
def get_meal_db_client():
    return MealDBClient()

@router.get("/random", response_model=Dict)
async def get_random_recipe(
    client: MealDBClient = Depends(get_meal_db_client)
):
    """Get a random recipe from the MealDB API."""
    response = client.get_random_meal()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response

@router.get("/by-ingredient/{ingredient}", response_model=Dict)
async def get_recipes_by_ingredient(
    ingredient: str,
    client: MealDBClient = Depends(get_meal_db_client)
):
    """Get recipes that contain the specified ingredient."""
    response = client.search_meals_by_ingredient(ingredient)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response

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

@router.get("/combined-search", response_model=Dict[str, Any])
async def get_combined_recipes(
    ingredients: List[str] = Query(..., description="List of available ingredients"),
    match_threshold: float = Query(0.5, description="Minimum threshold for local recipes"),
    client: MealDBClient = Depends(get_meal_db_client)
):
    """
    Find recipes that match the provided ingredients from both local database and external API.
    
    This endpoint combines results from our static dataset and the MealDB API.
    
    Args:
        ingredients: List of ingredients available to the user
        match_threshold: Threshold for local recipe matching
        client: MealDB API client
    
    Returns:
        Dictionary containing both local and external matching recipes
    """
    if not ingredients:
        raise HTTPException(status_code=400, detail="At least one ingredient must be provided")
    
    # Get local matches
    local_matches = find_recipes_by_ingredients(ingredients, match_threshold)
    
    # Get external matches from MealDB API (for the first ingredient only, as the API 
    # currently only supports searching by a single ingredient)
    external_matches = {}
    if ingredients:
        response = client.search_meals_by_ingredient(ingredients[0])
        if "error" not in response:
            external_matches = response
    
    return {
        "local_recipes": local_matches,
        "external_recipes": external_matches
    } 