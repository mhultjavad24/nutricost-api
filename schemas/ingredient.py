from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class CostEntry(BaseModel):
    cost: float = Field(ge=0)
    date: datetime = Field(default_factory=datetime.now)
    vendor: Optional[str] = None
    notes: Optional[str] = None


class NutrientBase(BaseModel):
    name: str
    unit: str
    
class NutrientCreate(NutrientBase):
    pass

class Nutrient(NutrientBase):
    id: int
    
    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

class IngredientNutrient(BaseModel):
    nutrient: Nutrient
    amount: float = Field(gt=0)  # Amount per 100g of ingredient

class IngredientBase(BaseModel):
    name: str
    weight: float = Field(gt=0)  # Weight in grams
    

class IngredientCreate(IngredientBase):
    cost: float = Field(ge=0)
    cost_entries: Optional[List[CostEntry]] = None
    nutrients: List[IngredientNutrient] = []
    

class Ingredient(IngredientBase):
    id: int
    recipe_id: Optional[int] = None
    cost_entries: List[CostEntry] = []
    nutrients: List[IngredientNutrient] = []
    
    @property
    def cost(self) -> float:
        if not self.cost_entries:
            return 0.0
        return sorted(self.cost_entries, key=lambda x: x.date, reverse=True)[0].cost

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }