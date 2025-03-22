from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.ingredient import Nutrient
from schemas.ingredient import NutrientCreate

class NutrientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_nutrient(self, nutrient: NutrientCreate) -> Nutrient:
        db_nutrient = Nutrient(
            name=nutrient.name,
            unit=nutrient.unit
        )
        self.session.add(db_nutrient)
        await self.session.commit()
        await self.session.refresh(db_nutrient)
        return db_nutrient

    async def get_nutrients(self, skip: int = 0, limit: int = 100) -> List[Nutrient]:
        query = select(Nutrient).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().unique())

    async def get_nutrient(self, nutrient_id: int) -> Optional[Nutrient]:
        return await self.session.get(Nutrient, nutrient_id)

    async def get_nutrient_by_name(self, name: str) -> Optional[Nutrient]:
        query = select(Nutrient).where(Nutrient.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete_nutrient(self, nutrient_id: int) -> bool:
        db_nutrient = await self.get_nutrient(nutrient_id)
        if not db_nutrient:
            return False
        await self.session.delete(db_nutrient)
        await self.session.commit()
        return True