from datetime import datetime

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends

from app.schemas.user import Role
from app.models.product import Product
from app.models.order import OrderStatus
from app.models.cart_item import CartItem
from app.schemas.order import OrderResponse
from app.utils.token import get_current_user
from app.models import Order, User, OrderItem


class OrderService:
  @staticmethod
  async def create_order(db, current_user):
    total_amount = await db.execute(
      select(func.sum(CartItem.quantity * Product.price)).join(Product, CartItem.product_id == Product.id)
      .where(CartItem.user_id == current_user.id))

    total_amount = total_amount.scalar()
    order_data = {"total_amount": total_amount, "user_id": current_user.id}
    order = Order(**order_data)

    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

  @staticmethod
  async def get_order_by_id(
          order_id: int,
          db: AsyncSession,
          current_user: User = Depends(get_current_user)):

    query = await db.execute(select(Order).filter(Order.id == order_id))
    order = query.scalars().first()

    if not order:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.user_id != current_user.id and not current_user.role == Role.admin:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return OrderResponse.model_validate(order)
  
  @staticmethod
  async def cancel_order(
          order_id: int,
          db: AsyncSession,
          current_user: User = Depends(get_current_user)):

    query = await db.execute(select(Order).filter(Order.id == order_id))
    order = query.scalars().first()

    if not order:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    if order.user_id != current_user.id and not current_user.role == Role.admin:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    if order.order_status == OrderStatus.canceled:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Order already cancelled")

    order.order_status=OrderStatus.canceled

    order_item = await db.execute(select(OrderItem).filter(OrderItem.order_id == order_id))
    order_item = order_item.scalars().first()
    product = await db.execute(select(Product).filter(Product.id == order_item.product_id))
    product = product.scalars().first()
    product.stock = product.stock + order_item.quantity

    await db.commit()
    await db.refresh(order)
    await db.refresh(product)
    return {"message":"Order canceled successfully"}
  
  @staticmethod
  async def update_order_status(
          order_id: int,
          updated_status: str,
          db: AsyncSession,
          current_user: User = Depends(get_current_user)):

    query = await db.execute(select(Order).filter(Order.id == order_id))
    order = query.scalars().first()

    if not order:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if not current_user.role == Role.admin:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    order.order_status = updated_status
    order.updated_at = datetime.now()
    await db.commit()
    await db.refresh(order)
    return {"message":"Order status updated successfully"}

  @staticmethod
  async def list_orders(
          db: AsyncSession,
          current_user: User = Depends(get_current_user)):

    if current_user.role == Role.admin:
      query = await db.execute(select(Order))
      order = query.scalars().all()
    else:
      query = await db.execute(select(Order).filter(Order.user_id == current_user.id)
                               .where(Order.order_status != OrderStatus.canceled))
      order = query.scalars().all()

    if not order:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    return order

  @staticmethod
  async def get_order_by_status(order_status, current_user,db):
    get_status = await db.execute(select(Order).filter(Order.order_status == order_status)
                                  .where(Order.user_id == current_user.id))

    return  get_status.scalars().all()