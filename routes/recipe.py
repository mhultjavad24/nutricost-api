from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import RecipeCreate, Recipe as RecipeSchema
from database import get_db
from repositories.recipe_repository import RecipeRepository

router = APIRouter(prefix="/recipes", tags=["recipes"])

async def get_recipe_repository(db: AsyncSession = Depends(get_db)) -> RecipeRepository:
    return RecipeRepository(db)

@router.post("/", response_model=RecipeSchema, status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: RecipeCreate, repository: RecipeRepository = Depends(get_recipe_repository)):
    return await repository.create_recipe(recipe)

@router.get("/", response_model=List[RecipeSchema])
async def read_recipes(skip: int = 0, limit: int = 100, repository: RecipeRepository = Depends(get_recipe_repository)):
    return await repository.get_recipes(skip, limit)

@router.get("/{recipe_id}", response_model=RecipeSchema)
async def read_recipe(recipe_id: int, repository: RecipeRepository = Depends(get_recipe_repository)):
    recipe = await repository.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}", response_model=RecipeSchema)
async def update_recipe(recipe_id: int, recipe: RecipeCreate, repository: RecipeRepository = Depends(get_recipe_repository)):
    updated_recipe = await repository.update_recipe(recipe_id, recipe)
    if not updated_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id: int, repository: RecipeRepository = Depends(get_recipe_repository)):
    success = await repository.delete_recipe(recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return None 