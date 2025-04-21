from pydantic import BaseModel
from datetime import date

class ProductBase(BaseModel):
    name: str
    type: str
    price: float
    description: str
    image: str | None = None
    posted_date: date

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class TutorialBase(BaseModel):
    title: str
    content: str
    posted_date: date

class TutorialCreate(TutorialBase):
    pass

class Tutorial(TutorialBase):
    id: int

    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str