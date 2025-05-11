from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db

router = APIRouter()

@router.post("/purchases/", response_model=schemas.Purchase)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_purchase = models.Purchase(user_id=current_user.id, **purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@router.get("/purchases/", response_model=List[schemas.Purchase])
def read_purchases(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Purchase).filter(models.Purchase.user_id == current_user.id).all()