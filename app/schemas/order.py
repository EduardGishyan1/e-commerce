from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrderStatus(str, Enum):
  pending = "pending"
  paid = "paid"
  shipped = "shipped"
  canceled = "canceled"

class OrderBase(BaseModel):
  total_amount: float = Field(..., ge=0,
                    json_schema_extra={"description": "Total amount must be greater than 0"})

  order_status: OrderStatus = Field(json_schema_extra={"description": "Order status"})
  model_config = ConfigDict(from_attributes=True, use_enum_values=True)

  @field_validator("total_amount", mode="before")
  @classmethod
  def validate_total_amount(cls, total_amount: float) -> float:
    if total_amount <= 0:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Total Amount must be greater than 0."
      )
    return total_amount

class OrderCreate(OrderBase):
  pass

class OrderUpdate(OrderBase):
  pass

class OrderResponse(OrderBase):
  created_at: datetime
  updated_at: Optional[datetime] = None
  id: int