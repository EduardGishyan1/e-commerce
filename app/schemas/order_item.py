from pydantic import BaseModel

class OrderItemBase(BaseModel):
  cart_item_id: int

class OrderItemCreate(OrderItemBase):
  pass

class OrderItemUpdate(OrderItemBase):
  pass
  
class OrderItemResponse(OrderItemBase):
  id: int
  order_id: int 
  product_id: int
  quantity: int
  price: float