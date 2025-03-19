from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.ingredient import Ingredient, CostEntry
from models.recipe import Recipe
from schemas import IngredientCreate, Ingredient as IngredientSchema
from schemas.ingredient import CostEntry as CostEntrySchema
from datetime import datetime

class IngredientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_ingredient(self, recipe_id: int, ingredient: IngredientCreate) -> Ingredient:
        recipe = await self.session.get(Recipe, recipe_id)
        if not recipe:
            return None

        db_ingredient = Ingredient(
            name=ingredient.name,
            weight=ingredient.weight,
            nutrition_facts=ingredient.nutrition_facts,
            recipe_id=recipe_id
        )
        self.session.add(db_ingredient)
        await self.session.flush()

        cost_entry = CostEntry(
            cost=ingredient.cost,
            date=datetime.now(),
            notes="Initial cost",
            ingredient_id=db_ingredient.id
        )
        self.session.add(cost_entry)

        if ingredient.cost_entries:
            for entry in ingredient.cost_entries:
                cost_entry = CostEntry(
                    cost=entry.cost,
                    date=entry.date,
                    vendor=entry.vendor,
                    notes=entry.notes,
                    ingredient_id=db_ingredient.id
                )
                self.session.add(cost_entry)

        await self.session.commit()
        await self.session.refresh(db_ingredient)
        return db_ingredient

    async def get_ingredients(self, skip: int = 0, limit: int = 100) -> List[Ingredient]:
        query = select(Ingredient).options(joinedload(Ingredient.cost_entries)).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().unique())

    async def get_ingredient(self, ingredient_id: int) -> Optional[Ingredient]:
        query = select(Ingredient).where(Ingredient.id == ingredient_id).options(joinedload(Ingredient.cost_entries))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_ingredient(self, ingredient_id: int, ingredient: IngredientCreate) -> Optional[Ingredient]:
        db_ingredient = await self.get_ingredient(ingredient_id)
        if not db_ingredient:
            return None

        db_ingredient.name = ingredient.name
        db_ingredient.weight = ingredient.weight
        db_ingredient.nutrition_facts = ingredient.nutrition_facts

        cost_entry = CostEntry(
            cost=ingredient.cost,
            date=datetime.now(),
            notes="Updated cost",
            ingredient_id=db_ingredient.id
        )
        self.session.add(cost_entry)

        if ingredient.cost_entries:
            for entry in ingredient.cost_entries:
                cost_entry = CostEntry(
                    cost=entry.cost,
                    date=entry.date,
                    vendor=entry.vendor,
                    notes=entry.notes,
                    ingredient_id=db_ingredient.id
                )
                self.session.add(cost_entry)

        await self.session.commit()
        await self.session.refresh(db_ingredient)
        return db_ingredient

    async def delete_ingredient(self, ingredient_id: int) -> bool:
        db_ingredient = await self.get_ingredient(ingredient_id)
        if not db_ingredient:
            return False

        await self.session.delete(db_ingredient)
        await self.session.commit()
        return True

    async def add_cost_entry(self, ingredient_id: int, cost_entry: CostEntrySchema) -> Optional[Ingredient]:
        db_ingredient = await self.get_ingredient(ingredient_id)
        if not db_ingredient:
            return None

        new_cost_entry = CostEntry(
            cost=cost_entry.cost,
            date=cost_entry.date,
            vendor=cost_entry.vendor,
            notes=cost_entry.notes,
            ingredient_id=ingredient_id
        )
        self.session.add(new_cost_entry)
        await self.session.commit()
        await self.session.refresh(db_ingredient)
        return db_ingredient

    async def get_cost_history(self, ingredient_id: int) -> List[CostEntry]:
        db_ingredient = await self.get_ingredient(ingredient_id)
        if not db_ingredient:
            return []
        return sorted(db_ingredient.cost_entries, key=lambda x: x.date, reverse=True) 