from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=schemas.CartItem, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    cart_item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    logger.info(f"Adding to cart for user {current_user.id}: {cart_item.dict()}")
    # Validate item existence
    if cart_item.item_type == "tutorial":
        item = db.query(models.Tutorial).filter(models.Tutorial.id == cart_item.item_id).first()
    elif cart_item.item_type == "service":
        item = db.query(models.Service).filter(models.Service.id == cart_item.item_id).first()
    elif cart_item.item_type == "product":
        item = db.query(models.Product).filter(models.Product.id == cart_item.item_id).first()
    else:
        logger.error(f"Invalid item_type: {cart_item.item_type}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item_type")

    if not item:
        logger.error(f"Item not found: {cart_item.item_type} ID {cart_item.item_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    # Check if item already exists in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id,
        models.CartItem.item_type == cart_item.item_type,
        models.CartItem.item_id == cart_item.item_id
    ).first()

    if existing_item:
        existing_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_item)
        logger.info(f"Updated existing cart item: {existing_item.id}")
        return existing_item

    # Create new cart item
    db_cart_item = models.CartItem(
        user_id=current_user.id,
        item_type=cart_item.item_type,
        item_id=cart_item.item_id,
        quantity=cart_item.quantity
    )
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    logger.info(f"Created new cart item: {db_cart_item.id}")
    return db_cart_item

@router.get("/", response_model=List[schemas.CartItem])
def read_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    logger.info(f"Fetching cart for user: {current_user.id}")
    return db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).all()

@router.patch("/{cart_item_id}", response_model=schemas.CartItem)
def update_cart_item(
    cart_item_id: int,
    update_data: schemas.CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    logger.info(f"Updating cart item {cart_item_id} with quantity {update_data.quantity} for user {current_user.id}")
    db_cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == cart_item_id,
        models.CartItem.user_id == current_user.id
    ).first()

    if not db_cart_item:
        logger.error(f"Cart item {cart_item_id} not found for user {current_user.id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    if update_data.quantity <= 0:
        logger.error(f"Invalid quantity {update_data.quantity} for cart item {cart_item_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be positive")

    db_cart_item.quantity = update_data.quantity
    db.commit()
    db.refresh(db_cart_item)
    logger.info(f"Updated cart item {cart_item_id} to quantity {db_cart_item.quantity}")
    return db_cart_item

@router.delete("/{cart_item_id}")
def remove_from_cart(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    logger.info(f"Removing cart item {cart_item_id} for user {current_user.id}")
    db_cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == cart_item_id,
        models.CartItem.user_id == current_user.id
    ).first()

    if not db_cart_item:
        logger.error(f"Cart item {cart_item_id} not found for user {current_user.id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    db.delete(db_cart_item)
    db.commit()
    logger.info(f"Removed cart item {cart_item_id}")
    return {"detail": "Cart item removed"}