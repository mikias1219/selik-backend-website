from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import Optional, Union

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

class ProductCreate(ProductBase):
    posted_date: Optional[datetime] = None

class Product(ProductBase):
    id: int
    posted_date: datetime
    class Config:
        from_attributes = True

class TutorialBase(BaseModel):
    title: str
    content: str
    tutorial_type: str  # Removed category
    price: float
    video_url: Optional[str] = None
    video_file: Optional[str] = None

class TutorialCreate(TutorialBase):
    posted_date: Optional[Union[datetime, date]] = None

    @validator('posted_date', pre=True)
    def parse_posted_date(cls, value):
        if value is None:
            return datetime.utcnow()  # Default to current time if None
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return datetime.strptime(value, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        return value

class Tutorial(TutorialBase):
    id: int
    posted_date: datetime
    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    name: str
    category: str
    price: float
    description: str
    image: Optional[str] = None
    video_url: Optional[str] = None
    video_file: Optional[str] = None

class ServiceCreate(ServiceBase):
    posted_date: Optional[datetime] = None

class Service(ServiceBase):
    id: int
    posted_date: datetime
    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    item_id: int
    item_type: str
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItem(CartItemBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class PurchaseBase(BaseModel):
    item_id: int
    item_type: str
    quantity: int
    total_price: float

class PurchaseCreate(PurchaseBase):
    purchase_date: Optional[datetime] = None

class Purchase(PurchaseBase):
    id: int
    user_id: int
    purchase_date: datetime
    class Config:
        from_attributes = True

class RequestBase(BaseModel):
    title: str
    description: str
    status: str = "pending"

class RequestCreate(RequestBase):
    posted_date: Optional[datetime] = None

class Request(RequestBase):
    id: int
    user_id: int
    posted_date: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str