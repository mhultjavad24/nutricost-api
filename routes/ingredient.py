from typing import List, Dict
from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from routes.recipe import recipes_db
from schemas import IngredientCreate, Ingredient as IngredientSchema
from schemas.ingredient import CostEntry


ingredient_counter = 0

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.post("/{recipe_id}", response_model=IngredientSchema, status_code=status.HTTP_201_CREATED)
def create_ingredient(recipe_id: int, ingredient: IngredientCreate):
    global ingredient_counter
    

    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    ingredient_counter += 1
    

    cost_entries = []

    cost_entries.append({
        "cost": ingredient.cost,
        "date": datetime.now(),
        "vendor": None,
        "notes": "Initial cost"
    })
    

    if ingredient.cost_entries:
        for entry in ingredient.cost_entries:
            cost_entries.append({
                "cost": entry.cost,
                "date": entry.date,
                "vendor": entry.vendor,
                "notes": entry.notes
            })
    

    db_ingredient = {
        "id": ingredient_counter,
        "name": ingredient.name,
        "weight": ingredient.weight,
        "nutrition_facts": ingredient.nutrition_facts,
        "cost_entries": cost_entries,
        "recipe_id": recipe_id
    }
    

    recipes_db[recipe_id]["ingredients"].append(db_ingredient)
    
    return db_ingredient


@router.get("/", response_model=List[IngredientSchema])
def read_ingredients(skip: int = 0, limit: int = 100):

    all_ingredients = []
    for recipe in recipes_db.values():
        all_ingredients.extend(recipe["ingredients"])
    
    return all_ingredients[skip:skip+limit]


@router.get("/{ingredient_id}", response_model=IngredientSchema)
def read_ingredient(ingredient_id: int):

    for recipe in recipes_db.values():
        for ingredient in recipe["ingredients"]:
            if ingredient["id"] == ingredient_id:
                return ingredient
    
    raise HTTPException(status_code=404, detail="Ingredient not found")


@router.put("/{ingredient_id}", response_model=IngredientSchema)
def update_ingredient(ingredient_id: int, ingredient: IngredientCreate):

    for recipe_id, recipe in recipes_db.items():
        for i, ing in enumerate(recipe["ingredients"]):
            if ing["id"] == ingredient_id:

                cost_entries = ing.get("cost_entries", [])
                

                current_cost = ingredient.cost
                if not cost_entries or current_cost != cost_entries[-1]["cost"]:
                    cost_entries.append({
                        "cost": current_cost,
                        "date": datetime.now(),
                        "vendor": None,
                        "notes": "Updated cost"
                    })
                

                if ingredient.cost_entries:
                    for entry in ingredient.cost_entries:
                        cost_entries.append({
                            "cost": entry.cost,
                            "date": entry.date,
                            "vendor": entry.vendor,
                            "notes": entry.notes
                        })
                

                db_ingredient = {
                    "id": ingredient_id,
                    "name": ingredient.name,
                    "weight": ingredient.weight,
                    "nutrition_facts": ingredient.nutrition_facts,
                    "cost_entries": cost_entries,
                    "recipe_id": recipe_id
                }
                recipe["ingredients"][i] = db_ingredient
                return db_ingredient
    
    raise HTTPException(status_code=404, detail="Ingredient not found")


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: int):

    for recipe in recipes_db.values():
        for i, ingredient in enumerate(recipe["ingredients"]):
            if ingredient["id"] == ingredient_id:
                recipe["ingredients"].pop(i)
                return None
    
    raise HTTPException(status_code=404, detail="Ingredient not found")



@router.post("/{ingredient_id}/cost", response_model=IngredientSchema)
def add_cost_entry(ingredient_id: int, cost_entry: CostEntry):

    for recipe in recipes_db.values():
        for i, ingredient in enumerate(recipe["ingredients"]):
            if ingredient["id"] == ingredient_id:

                if "cost_entries" not in ingredient:
                    ingredient["cost_entries"] = []
                
                ingredient["cost_entries"].append({
                    "cost": cost_entry.cost,
                    "date": cost_entry.date,
                    "vendor": cost_entry.vendor,
                    "notes": cost_entry.notes
                })
                
                return ingredient
    
    raise HTTPException(status_code=404, detail="Ingredient not found")



@router.get("/{ingredient_id}/cost_history", response_model=List[CostEntry])
def get_cost_history(ingredient_id: int):

    for recipe in recipes_db.values():
        for ingredient in recipe["ingredients"]:
            if ingredient["id"] == ingredient_id:
                if "cost_entries" not in ingredient:
                    return []
                

                sorted_entries = sorted(
                    ingredient["cost_entries"], 
                    key=lambda x: x["date"] if isinstance(x["date"], datetime) else datetime.fromisoformat(x["date"]), 
                    reverse=True
                )
                return sorted_entries
    
    raise HTTPException(status_code=404, detail="Ingredient not found") 