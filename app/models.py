from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    requests = relationship("Request", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    price = Column(Float)
    description = Column(String)
    image = Column(String)
    posted_date = Column(String)

class Tutorial(Base):
    __tablename__ = "tutorials"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category = Column(String)  # e.g., Cleaning, Repair, Upgrades
    price = Column(Float, default=9.99)
    posted_date = Column(String)
    video_url = Column(String, nullable=True)

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)  # e.g., Kits, Professional
    price = Column(Float)
    description = Column(String)
    image = Column(String, nullable=True)
    video_url = Column(String, nullable=True)

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_type = Column(String)  # "tutorial" or "service"
    item_id = Column(Integer)
    quantity = Column(Integer, default=1)
    user = relationship("User", back_populates="cart_items")

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    status = Column(String, default="pending")  # pending, approved, rejected
    posted_date = Column(String)
    user = relationship("User", back_populates="requests")

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_type = Column(String)  # "tutorial" or "service"
    item_id = Column(Integer)
    quantity = Column(Integer)
    total_price = Column(Float)
    purchase_date = Column(String)
    user = relationship("User", back_populates="purchases")