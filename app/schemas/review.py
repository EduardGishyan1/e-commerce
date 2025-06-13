from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi import HTTPException, status
from enum import IntEnum

class LikeDislikeEnum(IntEnum): 
  like = 1
  dislike = 0

class ReviewBase(BaseModel):
  content: str = Field(...)
  rating: int = Field(..., ge=0, le=5)

  @field_validator('rating', mode='before')
  @classmethod
  def validate_rating(cls, value: int) -> int:
    if type(value) != int:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Rating must be integer")
    if value > 5 or value < 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be between 0 to 5")
    return value
  
  @field_validator('content', mode='before')
  @classmethod
  def validate_content(cls, content: str) -> str:
    if not content.strip():
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Content can't be empty."
        )
    return content
  
class ReviewCreate(ReviewBase):
  product_id: int = Field(...)
  
class LikeDislike(BaseModel):
  like_dislike: LikeDislikeEnum
  review_id: int

  @field_validator("like_dislike", mode='before')
  @classmethod
  def validate_like_dislike(cls, value):
    if value not in LikeDislikeEnum.__members__.values():
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Value must be 0 or 1")
    return value
  
  model_config = ConfigDict(use_enum_values=True)
  
class ReviewUpdate(ReviewBase):
  pass

class ReviewResponse(ReviewBase):
  product_id: Optional[int]

class Review(ReviewBase):
  id: int
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)