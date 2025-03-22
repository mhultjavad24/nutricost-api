from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.ingredient import NutrientCreate, Nutrient
from database import get_db
from repositories.nutrient_repository import NutrientRepository

router = APIRouter(prefix="/nutrients", tags=["nutrients"])

async def get_nutrient_repository(db: AsyncSession = Depends(get_db)) -> NutrientRepository:
    return NutrientRepository(db)

@router.post("/", response_model=Nutrient, status_code=status.HTTP_201_CREATED)
async def create_nutrient(nutrient: NutrientCreate, repository: NutrientRepository = Depends(get_nutrient_repository)):
    return await repository.create_nutrient(nutrient)

@router.get("/", response_model=List[Nutrient])
async def read_nutrients(skip: int = 0, limit: int = 100, repository: NutrientRepository = Depends(get_nutrient_repository)):
    return await repository.get_nutrients(skip, limit)

@router.get("/{nutrient_id}", response_model=Nutrient)
async def read_nutrient(nutrient_id: int, repository: NutrientRepository = Depends(get_nutrient_repository)):
    nutrient = await repository.get_nutrient(nutrient_id)
    if not nutrient:
        raise HTTPException(status_code=404, detail="Nutrient not found")
    return nutrient

@router.delete("/{nutrient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_nutrient(nutrient_id: int, repository: NutrientRepository = Depends(get_nutrient_repository)):
    success = await repository.delete_nutrient(nutrient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Nutrient not found")
    return None