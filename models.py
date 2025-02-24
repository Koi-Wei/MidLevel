from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from database import Base

class StrengthPrediction(Base):
    __tablename__ = "strength_predictions"

    id = Column(Integer, primary_key=True, index=True)
    batch_number = Column(String, unique=True, index=True)
    predicted_strength = Column(Float)
    input_features = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RawMaterialOptimization(Base):
    __tablename__ = "raw_material_optimizations"

    id = Column(Integer, primary_key=True, index=True)
    batch_number = Column(String, unique=True, index=True)
    optimization_result = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())