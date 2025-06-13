from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.base import Base


class CartItem(Base):
  __tablename__ = "cart_items"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  price = Column(Float, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
  quantity = Column(Integer, nullable=False, default=1)

  user = relationship("User", back_populates="cart_items")
  product = relationship("Product", back_populates="cart_items")