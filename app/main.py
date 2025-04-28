from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from . import models, schemas, auth
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.username == "admin"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ... other endpoints (products, tutorials, services, cart, purchases, requests) ...

@app.get("/products/", response_model=list[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}

@app.get("/tutorials/", response_model=list[schemas.Tutorial])
def read_tutorials(db: Session = Depends(get_db)):
    return db.query(models.Tutorial).all()

@app.post("/tutorials/", response_model=schemas.Tutorial)
def create_tutorial(tutorial: schemas.TutorialCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    db_tutorial = models.Tutorial(**tutorial.dict())
    db.add(db_tutorial)
    db.commit()
    db.refresh(db_tutorial)
    return db_tutorial

@app.put("/tutorials/{tutorial_id}", response_model=schemas.Tutorial)
def update_tutorial(tutorial_id: int, tutorial: schemas.TutorialCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    db_tutorial = db.query(models.Tutorial).filter(models.Tutorial.id == tutorial_id).first()
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    for key, value in tutorial.dict().items():
        setattr(db_tutorial, key, value)
    db.commit()
    db.refresh(db_tutorial)
    return db_tutorial

@app.delete("/tutorials/{tutorial_id}")
def delete_tutorial(tutorial_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    db_tutorial = db.query(models.Tutorial).filter(models.Tutorial.id == tutorial_id).first()
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    db.delete(db_tutorial)
    db.commit()
    return {"message": "Tutorial deleted"}

@app.get("/services/", response_model=list[schemas.Service])
def read_services(db: Session = Depends(get_db)):
    return db.query(models.Service).all()

@app.post("/services/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    db_service = models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@app.get("/cart/", response_model=list[schemas.CartItem])
def read_cart(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).all()

@app.post("/cart/", response_model=schemas.CartItem)
def add_to_cart(cart_item: schemas.CartItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_cart_item = models.CartItem(**cart_item.dict(), user_id=current_user.id)
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

@app.delete("/cart/{cart_item_id}")
def remove_from_cart(cart_item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id, models.CartItem.user_id == current_user.id).first()
    if db_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(db_cart_item)
    db.commit()
    return {"message": "Cart item removed"}

@app.post("/purchases/", response_model=schemas.Purchase)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_purchase = models.Purchase(**purchase.dict(), user_id=current_user.id)
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@app.get("/purchases/", response_model=list[schemas.Purchase])
def read_purchases(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Purchase).filter(models.Purchase.user_id == current_user.id).all()

@app.get("/requests/", response_model=list[schemas.Request])
def read_requests(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        return db.query(models.Request).filter(models.Request.user_id == current_user.id).all()
    return db.query(models.Request).all()

@app.post("/requests/", response_model=schemas.Request)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_request = models.Request(**request.dict(), user_id=current_user.id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@app.put("/requests/{request_id}", response_model=schemas.Request)
def update_request(request_id: int, request: schemas.Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    for key, value in request.dict().items():
        setattr(db_request, key, value)
    db.commit()
    db.refresh(db_request)
    return db_request