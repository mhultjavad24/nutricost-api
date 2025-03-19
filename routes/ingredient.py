from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import IngredientCreate, Ingredient as IngredientSchema
from schemas.ingredient import CostEntry
from database import get_db
from repositories.ingredient_repository import IngredientRepository

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

async def get_ingredient_repository(db: AsyncSession = Depends(get_db)) -> IngredientRepository:
    return IngredientRepository(db)

@router.post("/{recipe_id}", response_model=IngredientSchema, status_code=status.HTTP_201_CREATED)
async def create_ingredient(recipe_id: int, ingredient: IngredientCreate, repository: IngredientRepository = Depends(get_ingredient_repository)):
    db_ingredient = await repository.create_ingredient(recipe_id, ingredient)
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_ingredient

@router.get("/", response_model=List[IngredientSchema])
async def read_ingredients(skip: int = 0, limit: int = 100, repository: IngredientRepository = Depends(get_ingredient_repository)):
    return await repository.get_ingredients(skip, limit)

@router.get("/{ingredient_id}", response_model=IngredientSchema)
async def read_ingredient(ingredient_id: int, repository: IngredientRepository = Depends(get_ingredient_repository)):
    ingredient = await repository.get_ingredient(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.put("/{ingredient_id}", response_model=IngredientSchema)
async def update_ingredient(ingredient_id: int, ingredient: IngredientCreate, repository: IngredientRepository = Depends(get_ingredient_repository)):
    updated_ingredient = await repository.update_ingredient(ingredient_id, ingredient)
    if not updated_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return updated_ingredient

@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(ingredient_id: int, repository: IngredientRepository = Depends(get_ingredient_repository)):
    success = await repository.delete_ingredient(ingredient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return None

@router.post("/{ingredient_id}/cost", response_model=IngredientSchema)
async def add_cost_entry(ingredient_id: int, cost_entry: CostEntry, repository: IngredientRepository = Depends(get_ingredient_repository)):
    updated_ingredient = await repository.add_cost_entry(ingredient_id, cost_entry)
    if not updated_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return updated_ingredient

@router.get("/{ingredient_id}/cost_history", response_model=List[CostEntry])
async def get_cost_history(ingredient_id: int, repository: IngredientRepository = Depends(get_ingredient_repository)):
    return await repository.get_cost_history(ingredient_id) 