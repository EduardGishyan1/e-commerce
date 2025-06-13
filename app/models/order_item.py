from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.base import Base


class OrderItem(Base):
  __tablename__ = "order_items"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
  product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
  quantity = Column(Integer, nullable=False)
  price = Column(Float, nullable=False)

  order = relationship("Order", back_populates="order_items")
  product = relationship("Product", back_populates="order_items")