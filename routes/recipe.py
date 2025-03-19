from typing import List, Dict
from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from schemas import RecipeCreate, Recipe as RecipeSchema, Ingredient as IngredientSchema

# In-memory storage
recipes_db: Dict[int, dict] = {}
recipe_counter = 0

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/", response_model=RecipeSchema, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: RecipeCreate):
    global recipe_counter
    recipe_counter += 1
    
    # Create new recipe with ID
    db_recipe = {
        "id": recipe_counter,
        "name": recipe.name,
        "ingredients": []
    }
    
    # Add ingredients if provided
    if recipe.ingredients:
        for i, ingredient_data in enumerate(recipe.ingredients):
            # Create cost entries from the ingredient cost
            cost_entries = [{
                "cost": ingredient_data.cost,
                "date": datetime.now(),
                "vendor": None,
                "notes": "Initial cost"
            }]
            
            # Add any additional cost entries if provided
            if hasattr(ingredient_data, 'cost_entries') and ingredient_data.cost_entries:
                for entry in ingredient_data.cost_entries:
                    cost_entries.append({
                        "cost": entry.cost,
                        "date": entry.date,
                        "vendor": entry.vendor,
                        "notes": entry.notes
                    })
            
            db_ingredient = {
                "id": i + 1,
                "name": ingredient_data.name,
                "weight": ingredient_data.weight,
                "nutrition_facts": ingredient_data.nutrition_facts,
                "cost_entries": cost_entries,
                "recipe_id": recipe_counter
            }
            db_recipe["ingredients"].append(db_ingredient)
    
    # Store in our in-memory db
    recipes_db[recipe_counter] = db_recipe
    
    return db_recipe


@router.get("/", response_model=List[RecipeSchema])
def read_recipes(skip: int = 0, limit: int = 100):
    recipes = list(recipes_db.values())
    return recipes[skip:skip+limit]


@router.get("/{recipe_id}", response_model=RecipeSchema)
def read_recipe(recipe_id: int):
    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return recipes_db[recipe_id]


@router.put("/{recipe_id}", response_model=RecipeSchema)
def update_recipe(recipe_id: int, recipe: RecipeCreate):
    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Update recipe
    db_recipe = {
        "id": recipe_id,
        "name": recipe.name,
        "ingredients": []
    }
    
    # Add new ingredients
    for i, ingredient_data in enumerate(recipe.ingredients):
        # Create cost entries from the ingredient cost
        cost_entries = [{
            "cost": ingredient_data.cost,
            "date": datetime.now(),
            "vendor": None,
            "notes": "Updated cost"
        }]
        
        # Add any additional cost entries if provided
        if hasattr(ingredient_data, 'cost_entries') and ingredient_data.cost_entries:
            for entry in ingredient_data.cost_entries:
                cost_entries.append({
                    "cost": entry.cost,
                    "date": entry.date,
                    "vendor": entry.vendor,
                    "notes": entry.notes
                })
        
        db_ingredient = {
            "id": i + 1,
            "name": ingredient_data.name,
            "weight": ingredient_data.weight,
            "nutrition_facts": ingredient_data.nutrition_facts,
            "cost_entries": cost_entries,
            "recipe_id": recipe_id
        }
        db_recipe["ingredients"].append(db_ingredient)
    
    recipes_db[recipe_id] = db_recipe
    
    return db_recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int):
    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    del recipes_db[recipe_id]
    
    return None 