from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator

class CategoryEnum(str, Enum):
  electronics = "electronics"
  fashion = "fashion"
  home = "home"
  books = "books"
  
class ProductBase(BaseModel):
  name: str = Field(..., max_length=100)
  description: Optional[str] = Field(None, max_length=500)
  price: float = Field(..., gt=0)
  stock: int = Field(..., ge=0)
  category: CategoryEnum = Field(None) 
  image_url: Optional[str] = Field(None)
  
  model_config = ConfigDict(from_attributes=True, 
                            use_enum_values=True)
    
  @field_validator('name', 'category', mode='before')
  @classmethod
  def validate_non_empty(cls, value: str, info) -> str:
    if not isinstance(value,str):
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"'{info.field_name}' must be string")
    if not value.strip():
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"'{info.field_name}' can't be empty.")
    return value
  
  @field_validator('description', mode='before')
  @classmethod
  def validate_description(cls, value: Optional[str]) -> Optional[str]:
    if value and len(value) > 500:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Description too long.")
    if not value.strip():
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Description can't be empty.")
    return value
  
  @field_validator('price', mode='before')
  @classmethod
  def validate_price(cls, value: float) -> float:
    if value < 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price must be positive")
    return value
  
  @field_validator('stock', mode='before')
  @classmethod
  def validate_stock(cls, value: int) -> int:
    if value < 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock field must be positive")
    return value
  
class ProductCreate(ProductBase):
  pass

class ProductResponse(ProductBase):
  id: int
  created_at: datetime
  updated_at: Optional[datetime] = None

  model_config = ConfigDict(from_attributes=True)

class ProductUpdate(BaseModel):
  name: Optional[str] = Field(None, max_length=100)
  description: Optional[str] = Field(None, max_length=500)
  price: Optional[float] = Field(None, gt=0)
  stock: Optional[int] = Field(None, ge=0)
  category: Optional[str] = Field(None, max_length=100)
  image_url: Optional[str] = Field(None, json_schema_extra={"description" : "URL of the product's image"})

  @field_validator('name', 'description', 'category', 'image_url', mode="before")
  @classmethod
  def validate_optional_fields(cls, value: Optional[str], info) -> Optional[str]:
        if value is not None and not str(value).strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The field '{info.field_name}' can't be empty."
            )
        return value
  
  @field_validator('price',mode='before')
  @classmethod
  def validate_price(cls, value: Optional[float]) -> Optional[float]:
    if value < 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Price must be positive")
    return value
  
  @field_validator('stock',mode='before')
  @classmethod
  def validate_stock(cls, value: Optional[int]) -> Optional[int]:
    if value < 0:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock must be positive")
    return value
  
class ProductFilter(BaseModel):
  page: int = 1
  size: int = 10
  category: Optional[str] = None
  min_price: Optional[float] = None
  max_price: Optional[float] = None
  availability: Optional[bool] = None

  @field_validator('min_price', 'max_price', mode="before")
  @classmethod
  def validate_optional_fields(cls, value: Optional[float], info) -> Optional[float]:
    if value is not None and float(value) < 0:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"The field '{info.field_name}' can't be negative."
        )
    return value
  
  @field_validator('category', mode="before")
  @classmethod
  def validate_category(cls, value: Optional[str], info) -> Optional[str]:
    if value is not None and not str(value).strip():
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"The field '{info.field_name}' can't be empty."
        )
    return value