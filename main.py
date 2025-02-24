from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import models
from database import get_db, engine
from datetime import datetime, timedelta

app = FastAPI(title="MidLevel API")

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

@app.get("/strength/recent")
def get_recent_predictions(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取最近的强度预测记录"""
    predictions = db.query(models.StrengthPrediction)\
        .order_by(models.StrengthPrediction.created_at.desc())\
        .limit(limit)\
        .all()
    return predictions

@app.get("/strength/batch/{batch_number}")
def get_prediction_by_batch(
    batch_number: str,
    db: Session = Depends(get_db)
):
    """通过批次号获取强度预测"""
    prediction = db.query(models.StrengthPrediction)\
        .filter(models.StrengthPrediction.batch_number == batch_number)\
        .first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Batch number not found")
    return prediction

@app.get("/optimization/recent")
def get_recent_optimizations(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取最近的原材料优化记录"""
    optimizations = db.query(models.RawMaterialOptimization)\
        .order_by(models.RawMaterialOptimization.created_at.desc())\
        .limit(limit)\
        .all()
    return optimizations

@app.get("/optimization/batch/{batch_number}")
def get_optimization_by_batch(
    batch_number: str,
    db: Session = Depends(get_db)
):
    """通过批次号获取原材料优化记录"""
    optimization = db.query(models.RawMaterialOptimization)\
        .filter(models.RawMaterialOptimization.batch_number == batch_number)\
        .first()
    if not optimization:
        raise HTTPException(status_code=404, detail="Batch number not found")
    return optimization

@app.get("/stats/daily")
def get_daily_stats(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """获取每日统计数据"""
    cutoff_date = datetime.now() - timedelta(days=days)
    
    strength_count = db.query(models.StrengthPrediction)\
        .filter(models.StrengthPrediction.created_at >= cutoff_date)\
        .count()
    
    optimization_count = db.query(models.RawMaterialOptimization)\
        .filter(models.RawMaterialOptimization.created_at >= cutoff_date)\
        .count()
    
    return {
        "period": f"Last {days} days",
        "strength_predictions": strength_count,
        "optimizations": optimization_count
    }