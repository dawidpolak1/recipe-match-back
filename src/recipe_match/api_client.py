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

if __name__ == "__main__":
    client = MealDBClient()
    # Example usage: Fetch and print a random meal.
    print("Random meal:", client.get_random_meal())
    # Example usage: Search for meals that contain 'chicken'.
    print("Meals with chicken:", client.search_meals_by_ingredient("chicken"))
