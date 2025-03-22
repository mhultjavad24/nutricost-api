from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from database import Base
from models.nutrient import Nutrient

class CostEntry(Base):
    __tablename__ = "cost_entries"

    id = Column(Integer, primary_key=True, index=True)
    cost = Column(Float)
    date = Column(DateTime)
    vendor = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    ingredient = relationship("Ingredient", back_populates="cost_entries")

ingredient_nutrients = Table(
    'ingredient_nutrients',
    Base.metadata,
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'), primary_key=True),
    Column('nutrient_id', Integer, ForeignKey('nutrients.id'), primary_key=True),
    Column('amount', Float, nullable=False)  # Amount per 100g of ingredient
)

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Float)  # Weight in grams
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    
    recipe = relationship("Recipe", back_populates="ingredients")
    cost_entries = relationship("CostEntry", back_populates="ingredient", cascade="all, delete-orphan")
    nutrients = relationship("Nutrient", secondary=ingredient_nutrients, lazy="joined")