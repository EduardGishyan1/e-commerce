from sqlalchemy import Column, String, Integer, ForeignKey, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class Payment(Base):
  __tablename__ = "payments"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
  amount = Column(Float, nullable=False)
  status = Column(String(100), default="Pending")
  currency = Column(String, nullable=False)
  stripe_session_id = Column(String, unique=True, nullable=False)
  created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

  user = relationship("User", back_populates="payments")
  order = relationship("Order", back_populates="payments")