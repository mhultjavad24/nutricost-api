from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base

class CostEntry(Base):
    __tablename__ = "cost_entries"

    id = Column(Integer, primary_key=True, index=True)
    cost = Column(Float)
    date = Column(DateTime)
    vendor = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    ingredient = relationship("Ingredient", back_populates="cost_entries")

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Float)
    nutrition_facts = Column(JSON)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    
    recipe = relationship("Recipe", back_populates="ingredients")
    cost_entries = relationship("CostEntry", back_populates="ingredient", cascade="all, delete-orphan") 