from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base
from app.schemas.user import Role


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  username = Column(String(100), nullable=True)
  phone_number = Column(String(100), nullable=True)
  name = Column(String(100), nullable=True)
  surname = Column(String(100), nullable=True)
  email = Column(String(100), unique=True, nullable=False)
  password = Column(String(255), nullable=False)
  role = Column(Enum(Role), nullable=True, default=Role.customer)
  image_url = Column(Text, nullable=True)
  sensitive_info = Column(JSON, nullable=True)
  is_active = Column(Boolean, nullable=True, default=True)
  is_verified = Column(Boolean, default=False)
  created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
  updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

  orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
  cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
  reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
  payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
  wishlist = relationship("Wishlist", back_populates="user", cascade="all, delete-orphan")