from sqlalchemy import Column, Integer, String
from database import Base

class Nutrient(Base):
    __tablename__ = "nutrients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    unit = Column(String)  # e.g., "g" for grams, "mg" for milligrams