from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, database, auth
from .database import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)



app = FastAPI(title="Selik Labs API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication
@app.post("/login", response_model=schemas.Token)
def login(form_data: schemas.AdminLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Products
@app.get("/products/", response_model=List[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    return crud.create_product(db, product)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    db_product = crud.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    db_product = crud.delete_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Tutorials
@app.get("/tutorials/", response_model=List[schemas.Tutorial])
def read_tutorials(db: Session = Depends(get_db)):
    return crud.get_tutorials(db)

@app.get("/tutorials/{tutorial_id}", response_model=schemas.Tutorial)
def read_tutorial(tutorial_id: int, db: Session = Depends(get_db)):
    db_tutorial = crud.get_tutorial(db, tutorial_id)
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return db_tutorial

@app.post("/tutorials/", response_model=schemas.Tutorial)
def create_tutorial(tutorial: schemas.TutorialCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    return crud.create_tutorial(db, tutorial)

@app.put("/tutorials/{tutorial_id}", response_model=schemas.Tutorial)
def update_tutorial(tutorial_id: int, tutorial: schemas.TutorialCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    db_tutorial = crud.update_tutorial(db, tutorial_id, tutorial)
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return db_tutorial

@app.delete("/tutorials/{tutorial_id}", response_model=schemas.Tutorial)
def delete_tutorial(tutorial_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    auth.verify_token(token)
    db_tutorial = crud.delete_tutorial(db, tutorial_id)
    if db_tutorial is None:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return db_tutorial