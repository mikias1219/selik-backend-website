from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db

router = APIRouter()

@router.post("/cart/", response_model=schemas.CartItem)
def add_to_cart(cart_item: schemas.CartItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_cart_item = models.CartItem(user_id=current_user.id, **cart_item.dict())
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

@router.get("/cart/", response_model=List[schemas.CartItem])
def read_cart(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).all()

@router.delete("/cart/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id, models.CartItem.user_id == current_user.id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(db_cart_item)
    db.commit()
    return {"detail": "Cart item removed"}