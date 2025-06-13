from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator


class CartItemBase(BaseModel):
  product_id: int = Field(...)
  quantity: int = Field(..., gt=0)

  model_config = ConfigDict(from_attributes=True,
                            use_enum_values=True)


class CartItemCreate(CartItemBase):

  @field_validator("quantity", mode='before')
  @classmethod
  def validate_quantity(cls, quantity: int) -> int:
    if not quantity:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Quantity field is required."
      )
    if quantity <= 0:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Quantity must be greater than 0."
      )
    return quantity

  @field_validator("product_id", mode='before')
  @classmethod
  def validate_product_id(cls, product_id: int) -> int:
    if product_id <= 0:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Product ID must be a positive integer."
      )
    return product_id


class CartItemUpdate(BaseModel):
  quantity: int = Field(..., gt=0)


class CartItemResponse(CartItemBase):
  id: int