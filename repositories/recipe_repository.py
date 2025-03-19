from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.recipe import Recipe
from models.ingredient import Ingredient, CostEntry
from schemas import RecipeCreate, Recipe as RecipeSchema
from datetime import datetime

class RecipeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_recipe(self, recipe: RecipeCreate) -> Recipe:
        db_recipe = Recipe(name=recipe.name)
        self.session.add(db_recipe)
        await self.session.flush()

        for ingredient_data in recipe.ingredients:
            db_ingredient = Ingredient(
                name=ingredient_data.name,
                weight=ingredient_data.weight,
                nutrition_facts=ingredient_data.nutrition_facts,
                recipe_id=db_recipe.id
            )
            self.session.add(db_ingredient)
            await self.session.flush()

            cost_entry = CostEntry(
                cost=ingredient_data.cost,
                date=datetime.now(),
                notes="Initial cost",
                ingredient_id=db_ingredient.id
            )
            self.session.add(cost_entry)

            if hasattr(ingredient_data, 'cost_entries') and ingredient_data.cost_entries:
                for entry in ingredient_data.cost_entries:
                    cost_entry = CostEntry(
                        cost=entry.cost,
                        date=entry.date,
                        vendor=entry.vendor,
                        notes=entry.notes,
                        ingredient_id=db_ingredient.id
                    )
                    self.session.add(cost_entry)

        await self.session.commit()
        await self.session.refresh(db_recipe)
        return db_recipe

    async def get_recipes(self, skip: int = 0, limit: int = 100) -> List[Recipe]:
        query = select(Recipe).options(joinedload(Recipe.ingredients).joinedload(Ingredient.cost_entries)).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().unique())

    async def get_recipe(self, recipe_id: int) -> Optional[Recipe]:
        query = select(Recipe).where(Recipe.id == recipe_id).options(joinedload(Recipe.ingredients).joinedload(Ingredient.cost_entries))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_recipe(self, recipe_id: int, recipe: RecipeCreate) -> Optional[Recipe]:
        db_recipe = await self.get_recipe(recipe_id)
        if not db_recipe:
            return None

        db_recipe.name = recipe.name

        for ingredient in db_recipe.ingredients:
            await self.session.delete(ingredient)

        for ingredient_data in recipe.ingredients:
            db_ingredient = Ingredient(
                name=ingredient_data.name,
                weight=ingredient_data.weight,
                nutrition_facts=ingredient_data.nutrition_facts,
                recipe_id=db_recipe.id
            )
            self.session.add(db_ingredient)
            await self.session.flush()

            cost_entry = CostEntry(
                cost=ingredient_data.cost,
                date=datetime.now(),
                notes="Updated cost",
                ingredient_id=db_ingredient.id
            )
            self.session.add(cost_entry)

            if hasattr(ingredient_data, 'cost_entries') and ingredient_data.cost_entries:
                for entry in ingredient_data.cost_entries:
                    cost_entry = CostEntry(
                        cost=entry.cost,
                        date=entry.date,
                        vendor=entry.vendor,
                        notes=entry.notes,
                        ingredient_id=db_ingredient.id
                    )
                    self.session.add(cost_entry)

        await self.session.commit()
        await self.session.refresh(db_recipe)
        return db_recipe

    async def delete_recipe(self, recipe_id: int) -> bool:
        db_recipe = await self.get_recipe(recipe_id)
        if not db_recipe:
            return False

        await self.session.delete(db_recipe)
        await self.session.commit()
        return True 