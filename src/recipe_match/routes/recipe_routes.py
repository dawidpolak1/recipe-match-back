from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List

from recipe_match.api_client import MealDBClient
from recipe_match.models import MealList, ErrorResponse

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