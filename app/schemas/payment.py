from enum import Enum
from datetime import datetime
from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator

class PaymentStatus(str, Enum):
  pending = "pending"
  completed = "completed"
  failed = "failed"

class PaymentCreate(BaseModel):
  currency: str = Field(...)
  order_id: int = Field(..., gt = 0)

  @field_validator('order_id', mode='before')
  @classmethod
  def validate_order_id(cls, order_id):
    if order_id <= 0:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Order ID must be greater than 0"
        )
    return order_id

class PaymentResponse(BaseModel):
  id: int
  user_id: int
  order_id: int
  payment_status: PaymentStatus
  amount: float
  created_at: datetime

  model_config = ConfigDict(from_attributes=True,
                            use_enum_values=True)