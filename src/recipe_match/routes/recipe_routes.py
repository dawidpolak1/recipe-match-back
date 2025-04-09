from fastapi import APIRouter, HTTPException, Depends, Path, Query
from typing import Dict, Any, List
import re

from recipe_match.api_client import MealDBClient
from recipe_match.models import Meal, DetailMealResponse, MealList, ErrorResponse, MealSummaryResponse

# Create a router for recipe-related endpoints
router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    responses={404: {"model": ErrorResponse}},
)

# Dependency to get the MealDB client
def get_meal_db_client():
    return MealDBClient()

def process_meal_data(meal_data: Dict[str, Any]) -> DetailMealResponse:
    """
    Process raw meal data from TheMealDB API into a structured DetailMealResponse.
    
    Args:
        meal_data: Raw meal data from TheMealDB API
        
    Returns:
        DetailMealResponse: Processed meal data in the API response format
    """
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
    return DetailMealResponse(
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

@router.get("/random", response_model=DetailMealResponse)
async def get_random_recipe(
    client: MealDBClient = Depends(get_meal_db_client)
):
    """Get a random recipe from the MealDB API."""
    response = client.get_random_meal()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
    if not response.get("meals") or not response["meals"][0]:
        raise HTTPException(status_code=404, detail="No random meal found")
    
    # Extract and process the meal data
    return process_meal_data(response["meals"][0])

@router.get("/by-ingredient", response_model=List[MealSummaryResponse])
async def get_recipes_by_ingredient(
    ingredient: str = Query(
        None,  # Default is None, so we can check if it's provided
        title="Ingredient",
        description="The ingredient to search for in recipes",
    ),
    client: MealDBClient = Depends(get_meal_db_client)
):
    """Get recipes that contain the specified ingredient."""
    if not ingredient:
        raise HTTPException(
            status_code=400, 
            detail="Ingredient is required and must be a string"
        )
    
    # Check if the ingredient is just a number
    if ingredient.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Ingredient cannot be a number"
        )
        
    response = client.search_meals_by_ingredient(ingredient)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
    # Handle empty response
    if not response.get("meals"):
        return []
    
    # Transform the API response to use our own response model
    return [
        MealSummaryResponse(
            id=meal.get("idMeal"),
            name=meal.get("strMeal"),
            thumbnail=meal.get("strMealThumb")
        ) 
        for meal in response.get("meals", [])
    ]

@router.get("/by-id/{meal_id}", response_model=DetailMealResponse)
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
    
    # Extract and process the meal data
    return process_meal_data(response["meals"][0])
 