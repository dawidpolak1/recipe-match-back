# src/api_client.py

import requests

class MealDBClient:
    BASE_URL: str = "https://www.themealdb.com/api/json/v1/1"

    def __init__(self, api_key: str = "1") -> None:
        """
        Initializes the MealDBClient.
        
        Args:
            api_key (str): The API key for accessing theMealDB. Defaults to "1".
                           For production, consider loading this from a secure .env file.
        """
        self.api_key = api_key

    def get_random_meal(self) -> dict:
        """
        Fetches a random meal from theMealDB.
        
        Returns:
            dict: The JSON response from the API or dummy error data.
        """
        url = f"{self.BASE_URL}/random.php"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            # In a real implementation, log the error details.
            return {"error": f"Failed to fetch random meal: {error}"}

    def search_meals_by_ingredient(self, ingredient: str) -> dict:
        """
        Searches for meals that include the given ingredient.
        
        Args:
            ingredient (str): The ingredient to search for.
        
        Returns:
            dict: The JSON response from the API or dummy error data.
        """
        url = f"{self.BASE_URL}/filter.php?i={ingredient}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            # In a real implementation, log the error details.
            return {"error": f"Failed to search meals by ingredient '{ingredient}': {error}"}
        
    def get_meal_by_id(self, meal_id: str) -> dict:
        """
        Fetches a specific meal by its ID from theMealDB and transforms it to our model format.
        
        Args:
            meal_id (str): The ID of the meal to fetch.
        
        Returns:
            dict: The JSON response from the API or error data.
        """
        url = f"{self.BASE_URL}/lookup.php?i={meal_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Process the response to extract ingredients
            if data.get("meals") and data["meals"][0]:
                meal = data["meals"][0]
                # Extract ingredients and their measurements
                ingredients = []
                for i in range(1, 21):  # TheMealDB has ingredients 1-20
                    ingredient_key = f"strIngredient{i}"
                    measure_key = f"strMeasure{i}"
                    if meal.get(ingredient_key) and meal[ingredient_key].strip():
                        ingredients.append({
                            "name": meal[ingredient_key],
                            "measurement": meal.get(measure_key, "").strip() or None
                        })
                
                # Add the ingredients list to the meal data
                meal["ingredients"] = ingredients
                
            return data
        except requests.RequestException as error:
            # In a real implementation, log the error details.
            return {"error": f"Failed to fetch meal with ID '{meal_id}': {error}"}

if __name__ == "__main__":
    client = MealDBClient()
    # Example usage: Fetch and print a random meal.
    print("Random meal:", client.get_random_meal())
    # Example usage: Search for meals that contain 'chicken'.
    print("Meals with chicken:", client.search_meals_by_ingredient("chicken"))
