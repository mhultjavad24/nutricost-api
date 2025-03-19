from typing import List, Optional
from pydantic import BaseModel

from schemas.ingredient import Ingredient, IngredientCreate


class RecipeBase(BaseModel):
    name: str


class RecipeCreate(RecipeBase):
    ingredients: Optional[List[IngredientCreate]] = []


class Recipe(RecipeBase):
    id: int
    ingredients: List[Ingredient] = []

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    } 