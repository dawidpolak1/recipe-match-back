from fastapi import APIRouter, HTTPException, Depends
from typing import Dict

from recipe_match.api_client import MealDBClient
from recipe_match.models import ErrorResponse, Meal

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

@router.get("/by-id/{meal_id}")
async def get_meal_by_id(
    meal_id: str,
    client: MealDBClient = Depends(get_meal_db_client)
):
    """Get a specific meal by its ID from the MealDB API."""
    response = client.get_meal_by_id(meal_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    if not response.get("meals") or not response["meals"][0]:
        raise HTTPException(status_code=404, detail=f"Meal with ID {meal_id} not found")
    
    # Create a Meal instance from the API response data
    meal_data = response["meals"][0]
    meal = Meal(**meal_data)
    
    # Explicitly construct the response dictionary with your desired field names
    return {
        "id": meal.id,
        "name": meal.name,
        "category": meal.category,
        "area": meal.area,
        "instructions": meal.instructions,
        "thumbnail": meal.thumbnail,
        "tags": meal.tags,
        "youtube": meal.youtube,
        "ingredients": meal.ingredients
    }
 