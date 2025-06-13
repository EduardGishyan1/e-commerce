from typing import Optional
from datetime import datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Category(BaseModel):
  name: str = Field(..., max_length=100)
  description: Optional[str] = Field(None, max_length=1000)

  @field_validator("name", mode='before')
  @classmethod
  def valid_name(cls, name: str) -> str:
    if name is None or not name.strip():
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Name can't be None or empty."
        )
    if not 1 <= len(name) <= 100:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Name should be between 1 and 100 characters in length."
        )
    return name

  @field_validator('description', mode='before')
  @classmethod
  def validate_description(cls, description: Optional[str]) -> Optional[str]:
    if description is None or not description.strip():
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Description can't be None or empty."
        )
    if not 1 <= len(description) <= 1000:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Description should be between 1 and 1000 characters in length."
        )
    return description

class CategoryResponse(Category):
  id: int
  created_at: datetime
  updated_at: Optional[datetime] = None

  model_config = ConfigDict(from_attributes=True)