from routes.recipe import router as recipe_router
from routes.ingredient import router as ingredient_router
from routes.nutrient import router as nutrient_router

__all__ = ["recipe_router", "ingredient_router", "nutrient_router"] 