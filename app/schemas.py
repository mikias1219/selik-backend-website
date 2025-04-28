from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    type: str
    price: float
    description: str
    image: Optional[str] = None
    posted_date: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True

class TutorialBase(BaseModel):
    title: str
    content: str
    category: str
    price: float
    posted_date: str
    video_url: Optional[str] = None

class TutorialCreate(TutorialBase):
    pass

class Tutorial(TutorialBase):
    id: int
    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    name: str
    category: str
    price: float
    description: str
    image: Optional[str] = None
    video_url: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int
    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    item_type: str  # "tutorial" or "service"
    item_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class RequestBase(BaseModel):
    title: str
    description: str
    posted_date: str

class RequestCreate(RequestBase):
    pass

class Request(RequestBase):
    id: int
    user_id: int
    status: str
    class Config:
        from_attributes = True

class PurchaseBase(BaseModel):
    item_type: str
    item_id: int
    quantity: int
    total_price: float
    purchase_date: str

class PurchaseCreate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True