from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class Wishlist(Base):
  __tablename__ = "wishlist"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
  description = Column(Text, nullable=True)
  created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

  user = relationship("User", back_populates="wishlist")
  product = relationship("Product", back_populates="wishlist")