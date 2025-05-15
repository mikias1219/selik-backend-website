from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        type=product.type,
        price=product.price,
        description=product.description,
        image=product.image or "/products/placeholder.jpg",
        posted_date=product.posted_date
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.type = product.type
        db_product.price = product.price
        db_product.description = product.description
        db_product.image = product.image or "/products/placeholder.jpg"
        db_product.posted_date = product.posted_date
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

def get_tutorials(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tutorial).offset(skip).limit(limit).all()

def get_tutorial(db: Session, tutorial_id: int):
    return db.query(models.Tutorial).filter(models.Tutorial.id == tutorial_id).first()

def create_tutorial(db: Session, tutorial: schemas.TutorialCreate):
    db_tutorial = models.Tutorial(
        title=tutorial.title,
        content=tutorial.content,
        tutorial_type=tutorial.tutorial_type,
        price=tutorial.price,
        posted_date=tutorial.posted_date,
        video_url=tutorial.video_url,
        video_file=tutorial.video_file
    )
    db.add(db_tutorial)
    db.commit()
    db.refresh(db_tutorial)
    return db_tutorial

def update_tutorial(db: Session, tutorial_id: int, tutorial: schemas.TutorialCreate):
    db_tutorial = db.query(models.Tutorial).filter(models.Tutorial.id == tutorial_id).first()
    if db_tutorial:
        db_tutorial.title = tutorial.title
        db_tutorial.content = tutorial.content
        db_tutorial.tutorial_type = tutorial.tutorial_type
        db_tutorial.price = tutorial.price
        db_tutorial.posted_date = tutorial.posted_date
        db_tutorial.video_url = tutorial.video_url
        db_tutorial.video_file = tutorial.video_file
        db.commit()
        db.refresh(db_tutorial)
    return db_tutorial

def delete_tutorial(db: Session, tutorial_id: int):
    db_tutorial = db.query(models.Tutorial).filter(models.Tutorial.id == tutorial_id).first()
    if db_tutorial:
        db.delete(db_tutorial)
        db.commit()
    return db_tutorial

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, hashed_password: str):
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user