from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan") 