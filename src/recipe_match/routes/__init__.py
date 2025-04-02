from recipe_match.routes.recipe_routes import router as recipe_router
from recipe_match.routes.local_recipes import router as local_recipes_router
from recipe_match.routes.detailed_recipes import router as detailed_recipes_router

__all__ = ["recipe_router", "local_recipes_router", "detailed_recipes_router"] 