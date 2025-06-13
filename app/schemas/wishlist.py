from enum import Enum
from typing import Optional
from datetime import datetime
from fastapi import HTTPException, status
from pydantic import BaseModel,ConfigDict, Field, field_validator

class WishlistBase(BaseModel):
  id: Optional[int] = Field(default=None)
  description: Optional[str] = Field(max_length=500, default=None)
  total_amount: float = Field(..., gt=0)

  @field_validator('total_amount', mode='before')
  @classmethod
  def validate_total_amount(cls, value: int) -> int:
    if value < 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total amount can't be negative.")
    return value

  @field_validator('description', mode='before')
  @classmethod
  def validate_description(cls, description: str) -> str:
    if not description.strip():
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Description can't be empty."
                          )
    if not 1 <= len(description) <= 500:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Description should be between 1 and 500 characters in length."
      )
    return description


class WishlistCreate(BaseModel):
  product_id: Optional[int] = Field(1, gt=0)


class WishlistResponse(BaseModel):
  id: int
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)


class WishlistUpdate(BaseModel):
  id: Optional[int] = Field(None, gt=0)
  description: Optional[str] = Field(None, max_length=500)
  total_amount: Optional[float] = Field(None, gt=0)
  updated_at: Optional[datetime] = None

  @field_validator('description', mode='before')
  @classmethod
  def validate_description(cls, description: str) -> str:
    if not description.strip():
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail="Description can't be empty."
                          )
    if not 1 <= len(description) <= 500:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Description should be between 1 and 500 characters in length."
      )
    return description

  @field_validator('total_amount', mode='before')
  @classmethod
  def validate_total_amount(cls, value: int) -> int:
    if value < 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total amount can't be negative")
    return value


class WishlistFilter(BaseModel):
  page: int = 1
  size: int = 10
  min_price: Optional[float] = None
  max_price: Optional[float] = None
  category: Optional[str] = None
  availability: Optional[bool] = True
  user_id: Optional[int] = None
  product_id: Optional[int] = None
