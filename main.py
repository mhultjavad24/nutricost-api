from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routes import recipe_router, ingredient_router
from routes.recipe import recipes_db, recipe_counter


def create_example_recipes():
    global recipe_counter
    
    # Create example 1: Chocolate Protein Shake
    recipe_counter += 1
    shake_id = recipe_counter
    shake = {
        "id": shake_id,
        "name": "Chocolate Protein Shake",
        "ingredients": []
    }
    
    # Add ingredients
    ingredients = [
        {
            "id": 1,
            "name": "Protein Powder", 
            "weight": 30.0, 
            "nutrition_facts": {"protein": 24, "carbs": 3, "fat": 1, "calories": 120},
            "cost": 1.20,
            "recipe_id": shake_id
        },
        {
            "id": 2,
            "name": "Almond Milk", 
            "weight": 240.0, 
            "nutrition_facts": {"protein": 1, "carbs": 2, "fat": 3, "calories": 40},
            "cost": 0.50,
            "recipe_id": shake_id
        },
        {
            "id": 3,
            "name": "Banana", 
            "weight": 100.0, 
            "nutrition_facts": {"protein": 1, "carbs": 23, "fat": 0, "calories": 105},
            "cost": 0.30,
            "recipe_id": shake_id
        },
    ]
    shake["ingredients"] = ingredients
    recipes_db[shake_id] = shake
    
    # Create example 2: Chicken Salad
    recipe_counter += 1
    salad_id = recipe_counter
    salad = {
        "id": salad_id,
        "name": "Chicken Salad",
        "ingredients": []
    }
    
    # Add ingredients
    ingredients = [
        {
            "id": 4,
            "name": "Chicken Breast", 
            "weight": 150.0, 
            "nutrition_facts": {"protein": 45, "carbs": 0, "fat": 5, "calories": 235},
            "cost": 2.50,
            "recipe_id": salad_id
        },
        {
            "id": 5,
            "name": "Mixed Greens", 
            "weight": 100.0, 
            "nutrition_facts": {"protein": 2, "carbs": 5, "fat": 0, "calories": 25},
            "cost": 1.00,
            "recipe_id": salad_id
        },
        {
            "id": 6,
            "name": "Cherry Tomatoes", 
            "weight": 50.0, 
            "nutrition_facts": {"protein": 1, "carbs": 4, "fat": 0, "calories": 18},
            "cost": 0.75,
            "recipe_id": salad_id
        },
        {
            "id": 7,
            "name": "Olive Oil", 
            "weight": 15.0, 
            "nutrition_facts": {"protein": 0, "carbs": 0, "fat": 14, "calories": 120},
            "cost": 0.30,
            "recipe_id": salad_id
        },
    ]
    salad["ingredients"] = ingredients
    recipes_db[salad_id] = salad


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create example data on startup
    create_example_recipes()
    
    yield
    
    # Clean up resources on shutdown (not needed for in-memory)
    pass


app = FastAPI(
    title="Recipe API",
    description="API for managing recipes and ingredients",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recipe_router)
app.include_router(ingredient_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Recipe API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True) 