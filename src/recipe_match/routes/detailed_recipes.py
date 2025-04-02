from fastapi import APIRouter, HTTPException, Depends
from typing import Dict

from recipe_match.api_client import MealDBClient
from recipe_match.models import ErrorResponse, Meal

# Create a router for detailed recipe endpoints
router = APIRouter(
    prefix="/detailed-recipes",
    tags=["detailed-recipes"],
    responses={404: {"model": ErrorResponse}},
)

# Dependency to get the MealDB client
def get_meal_db_client():
    return MealDBClient()

@router.get("/{meal_id}")
async def get_recipe_details(
    meal_id: str,
    client: MealDBClient = Depends(get_meal_db_client)
):
    """
    Get detailed recipe information including ingredients and instructions.
    
    This endpoint returns the complete recipe information including
    preparation instructions, ingredients list, and other details.
    """
    response = client.get_meal_by_id(meal_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    if not response.get("meals") or not response["meals"][0]:
        raise HTTPException(status_code=404, detail=f"Recipe with ID {meal_id} not found")
    
    # Create a Meal instance from the API response data
    meal_data = response["meals"][0]
    meal = Meal(**meal_data)
    
    # Return a structured recipe response
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