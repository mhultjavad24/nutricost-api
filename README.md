# Recipe API

A FastAPI backend for managing recipes and ingredients

## Features

- Store and manage recipes in memory
- Track ingredients with nutrition facts and costs
- RESTful API with CRUD operations

## Models

- **Recipe**: Contains recipe name and associated ingredients
- **Ingredient**: Contains name, weight, nutrition facts, and cost information

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## API Endpoints

### Recipes

- `GET /recipes` - List all recipes
- `GET /recipes/{recipe_id}` - Get a specific recipe
- `POST /recipes` - Create a new recipe
- `PUT /recipes/{recipe_id}` - Update a recipe
- `DELETE /recipes/{recipe_id}` - Delete a recipe

### Ingredients

- `GET /ingredients` - List all ingredients
- `GET /ingredients/{ingredient_id}` - Get a specific ingredient
- `POST /ingredients/{recipe_id}` - Add an ingredient to a recipe
- `PUT /ingredients/{ingredient_id}` - Update an ingredient
- `DELETE /ingredients/{ingredient_id}` - Delete an ingredient 