from typing import Dict, Optional
from pydantic import BaseModel, Field


class IngredientBase(BaseModel):
    name: str
    weight: float = Field(gt=0)
    nutrition_facts: Dict[str, float]
    cost: float = Field(ge=0)


class IngredientCreate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int
    recipe_id: Optional[int] = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    } 