from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class CostEntry(BaseModel):
    cost: float = Field(ge=0)
    date: datetime = Field(default_factory=datetime.now)
    vendor: Optional[str] = None
    notes: Optional[str] = None


class IngredientBase(BaseModel):
    name: str
    weight: float = Field(gt=0)
    nutrition_facts: Dict[str, float]
    

class IngredientCreate(IngredientBase):
    cost: float = Field(ge=0)
    cost_entries: Optional[List[CostEntry]] = None
    

class Ingredient(IngredientBase):
    id: int
    recipe_id: Optional[int] = None
    cost_entries: List[CostEntry] = []
    
    @property
    def cost(self) -> float:
    
        if not self.cost_entries:
            return 0.0
        return sorted(self.cost_entries, key=lambda x: x.date, reverse=True)[0].cost

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    } 