from fastapi import APIRouter, HTTPException, Depends
from typing import Dict

from recipe_match.api_client import MealDBClient
from recipe_match.models import Meal, MealResponse, ErrorResponse

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

@router.get("/by-id/{meal_id}", response_model=MealResponse)
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
    
    # Extract the meal data from the response
    meal_data = response["meals"][0]
    
    # Process the response to extract ingredients
    ingredients = []
    for i in range(1, 21):  # TheMealDB has ingredients 1-20
        ingredient_key = f"strIngredient{i}"
        measure_key = f"strMeasure{i}"
        if meal_data.get(ingredient_key) and meal_data[ingredient_key].strip():
            ingredients.append({
                "name": meal_data[ingredient_key],
                "measurement": meal_data.get(measure_key, "").strip() or None
            })
    
    # Add the ingredients list to the meal data
    meal_data["ingredients"] = ingredients
    
    # Create a Meal instance from the processed data
    meal = Meal(**meal_data)
    
    # Return a MealResponse model
    return MealResponse(
        id=meal.id,
        name=meal.name,
        category=meal.category,
        area=meal.area,
        instructions=meal.instructions,
        thumbnail=meal.thumbnail,
        tags=meal.tags,
        youtube=meal.youtube,
        ingredients=meal.ingredients
    )
 