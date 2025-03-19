# Nutricost API

A Python backend for managing recipes and ingredients with cost tracking

## Features

- Store and manage recipes in SQLite database
- Track ingredients with nutrition facts and cost history
- RESTful API with CRUD operations
- Cost tracking with vendor information and notes
- Async database operations with SQLAlchemy

## Models

- **Recipe**: Contains recipe name and associated ingredients
- **Ingredient**: Contains name, weight, nutrition facts, and cost information
- **CostEntry**: Tracks cost history with vendor information and notes

## Setup

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8080`

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
- `POST /ingredients/{ingredient_id}/cost` - Add a cost entry to an ingredient
- `GET /ingredients/{ingredient_id}/cost_history` - Get cost history for an ingredient 