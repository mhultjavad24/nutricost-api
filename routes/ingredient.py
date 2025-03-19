from typing import List, Dict
from fastapi import APIRouter, HTTPException, status

from routes.recipe import recipes_db
from schemas import IngredientCreate, Ingredient as IngredientSchema

# In-memory storage
ingredient_counter = 0

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.post("/{recipe_id}", response_model=IngredientSchema, status_code=status.HTTP_201_CREATED)
def create_ingredient(recipe_id: int, ingredient: IngredientCreate):
    global ingredient_counter
    
    # Verify recipe exists
    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    ingredient_counter += 1
    
    # Create ingredient
    db_ingredient = {
        "id": ingredient_counter,
        "name": ingredient.name,
        "weight": ingredient.weight,
        "nutrition_facts": ingredient.nutrition_facts,
        "cost": ingredient.cost,
        "recipe_id": recipe_id
    }
    
    # Add to recipe's ingredients
    recipes_db[recipe_id]["ingredients"].append(db_ingredient)
    
    return db_ingredient


@router.get("/", response_model=List[IngredientSchema])
def read_ingredients(skip: int = 0, limit: int = 100):
    # Collect all ingredients from all recipes
    all_ingredients = []
    for recipe in recipes_db.values():
        all_ingredients.extend(recipe["ingredients"])
    
    return all_ingredients[skip:skip+limit]


@router.get("/{ingredient_id}", response_model=IngredientSchema)
def read_ingredient(ingredient_id: int):
    # Find ingredient across all recipes
    for recipe in recipes_db.values():
        for ingredient in recipe["ingredients"]:
            if ingredient["id"] == ingredient_id:
                return ingredient
    
    raise HTTPException(status_code=404, detail="Ingredient not found")


@router.put("/{ingredient_id}", response_model=IngredientSchema)
def update_ingredient(ingredient_id: int, ingredient: IngredientCreate):
    # Find and update ingredient
    for recipe_id, recipe in recipes_db.items():
        for i, ing in enumerate(recipe["ingredients"]):
            if ing["id"] == ingredient_id:
                # Update ingredient
                db_ingredient = {
                    "id": ingredient_id,
                    "name": ingredient.name,
                    "weight": ingredient.weight,
                    "nutrition_facts": ingredient.nutrition_facts,
                    "cost": ingredient.cost,
                    "recipe_id": recipe_id
                }
                recipe["ingredients"][i] = db_ingredient
                return db_ingredient
    
    raise HTTPException(status_code=404, detail="Ingredient not found")


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: int):
    # Find and delete ingredient
    for recipe in recipes_db.values():
        for i, ingredient in enumerate(recipe["ingredients"]):
            if ingredient["id"] == ingredient_id:
                recipe["ingredients"].pop(i)
                return None
    
    raise HTTPException(status_code=404, detail="Ingredient not found") 