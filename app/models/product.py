import enum
from sqlalchemy import Column, Integer, String, Float, Text, TIMESTAMP, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class CategoryEnum(str, enum.Enum):
  electronics = "electronics"
  fashion = "fashion"
  home = "home"
  books = "books"


class Product(Base):
  __tablename__ = "products"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  name = Column(String(100), nullable=False)
  description = Column(Text, nullable=True)
  price = Column(Float, nullable=False)
  stock = Column(Integer, nullable=False)
  category = Column(Enum(CategoryEnum), nullable=False)
  vendor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
  updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
  is_active = Column(Boolean, nullable=False)
  image_url = Column(String, nullable=True)
  view_count = Column(Integer, default=0)

  order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")
  cart_items = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
  reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
  wishlist = relationship("Wishlist", back_populates="product", cascade="all, delete-orphan")