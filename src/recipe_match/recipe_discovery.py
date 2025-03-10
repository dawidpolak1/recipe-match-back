from typing import List, Dict, Any

# Static dataset of recipes with their ingredients
# This would typically come from a database or larger JSON file
RECIPE_DATABASE = [
    {
        "id": 1,
        "name": "Simple Pasta",
        "ingredients": ["pasta", "tomato sauce", "cheese", "garlic"],
        "instructions": "Boil pasta. Heat sauce with garlic. Combine and top with cheese."
    },
    {
        "id": 2,
        "name": "Vegetable Stir Fry",
        "ingredients": ["rice", "broccoli", "carrot", "soy sauce", "garlic"],
        "instructions": "Cook rice. Stir fry vegetables with garlic and soy sauce. Serve over rice."
    },
    {
        "id": 3,
        "name": "Chicken Sandwich",
        "ingredients": ["bread", "chicken", "lettuce", "mayo"],
        "instructions": "Toast bread. Add mayo, chicken, and lettuce."
    },
    {
        "id": 4,
        "name": "Omelette",
        "ingredients": ["eggs", "cheese", "salt", "pepper", "butter"],
        "instructions": "Beat eggs. Melt butter in pan. Cook eggs, add cheese, fold."
    },
    {
        "id": 5,
        "name": "Simple Salad",
        "ingredients": ["lettuce", "tomato", "cucumber", "olive oil", "vinegar"],
        "instructions": "Chop vegetables. Toss with oil and vinegar."
    }
]

def find_recipes_by_ingredients(available_ingredients: List[str], match_threshold: float = 0.5) -> List[Dict[str, Any]]:
    """
    Find recipes that can be made with the available ingredients.
    
    Args:
        available_ingredients: List of ingredients available to the user
        match_threshold: Minimum proportion of recipe ingredients that must be available (default: 0.5)
                        For example, 0.5 means at least half of the recipe ingredients must be available
    
    Returns:
        List of matching recipes, sorted by match percentage (highest first)
    """
    # Normalize ingredients (lowercase)
    normalized_available = [ingredient.lower().strip() for ingredient in available_ingredients]
    
    matching_recipes = []
    
    for recipe in RECIPE_DATABASE:
        recipe_ingredients = [ingredient.lower() for ingredient in recipe["ingredients"]]
        
        # Count how many ingredients match
        matching_ingredients = [i for i in recipe_ingredients if i in normalized_available]
        match_count = len(matching_ingredients)
        
        # Calculate match percentage
        match_percentage = match_count / len(recipe_ingredients)
        
        # Add recipe if it meets the threshold
        if match_percentage >= match_threshold:
            matching_recipes.append({
                **recipe,
                "match_percentage": match_percentage,
                "matching_ingredients": matching_ingredients,
                "missing_ingredients": [i for i in recipe_ingredients if i not in normalized_available]
            })
    
    # Sort by match percentage (highest first)
    matching_recipes.sort(key=lambda x: x["match_percentage"], reverse=True)
    
    return matching_recipes

if __name__ == "__main__":
    # Example usage
    my_ingredients = ["pasta", "cheese", "garlic", "tomato sauce"]
    recipes = find_recipes_by_ingredients(my_ingredients)
    
    if recipes:
        print(f"Found {len(recipes)} matching recipes:")
        for recipe in recipes:
            print(f"- {recipe['name']} (Match: {recipe['match_percentage']*100:.0f}%)")
            print(f"  Missing: {', '.join(recipe['missing_ingredients']) if recipe['missing_ingredients'] else 'None'}")
    else:
        print("No matching recipes found.") 