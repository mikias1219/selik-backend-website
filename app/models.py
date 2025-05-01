from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    requests = relationship("Request", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    price = Column(Float)
    description = Column(String)
    image = Column(String, nullable=True)
    posted_date = Column(DateTime, default=datetime.utcnow)

class Tutorial(Base):
    __tablename__ = "tutorials"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category = Column(String)
    price = Column(Float)
    posted_date = Column(DateTime, default=datetime.utcnow)
    video_url = Column(String, nullable=True)  # YouTube URL
    video_file = Column(String, nullable=True)  # File path for uploaded video

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    price = Column(Float)
    description = Column(String)
    image = Column(String, nullable=True)
    posted_date = Column(DateTime, default=datetime.utcnow)
    video_url = Column(String, nullable=True)  # YouTube URL
    video_file = Column(String, nullable=True)  # File path for uploaded video

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer)
    item_type = Column(String)  # "product", "tutorial", "service"
    quantity = Column(Integer, default=1)
    user = relationship("User", back_populates="cart_items")

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer)
    item_type = Column(String)
    quantity = Column(Integer)
    purchase_date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="purchases")

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    status = Column(String, default="pending")
    posted_date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="requests")