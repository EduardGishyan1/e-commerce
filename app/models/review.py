from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class Review(Base):
  __tablename__ = "reviews"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
  content = Column(Text, nullable=False)
  rating = Column(Integer, nullable=False)
  likes_count = Column(Integer, nullable=False, default=0)
  dislikes_count = Column(Integer, nullable=False, default=0)
  created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

  __table_args__ = (
    CheckConstraint('likes_count >= 0'),
  )

  user = relationship("User", back_populates="reviews")
  product = relationship("Product", back_populates="reviews")