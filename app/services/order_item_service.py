from sqlalchemy import update, delete
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import Role
from app.models.order import Order
from sqlalchemy.future import select
from app.models.product import Product
from app.models.cart_item import CartItem
from app.models.order_item import OrderItem
from app.services.order_service import OrderService
from app.services.email_service import EmailService


class OrderItemService:
  async def create_order_item(db: AsyncSession, current_user):
    result = await db.execute(
      select(CartItem, Product)
      .join(Product, CartItem.product_id == Product.id)
      .filter(CartItem.user_id == current_user.id))

    cart_items = result.all()

    if not cart_items:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty")

    order = await OrderService.create_order(db, current_user)

    for cart_item, product in cart_items:
      if product.stock < cart_item.quantity:
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"Insufficient stock for product {product.id}")

      new_stock = product.stock - cart_item.quantity
      is_active = False if new_stock == 0 else product.is_active

      await db.execute(
        update(Product)
        .where(Product.id == product.id)
        .values(stock=new_stock, is_active=is_active))

    order_items = [
      OrderItem(
        order_id=order.id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
        price=cart_item.price)

      for cart_item, _ in cart_items
    ]
    db.add_all(order_items)

    await db.execute(delete(CartItem).where(CartItem.user_id == current_user.id))

    try:
      await db.commit()
    except SQLAlchemyError:
      await db.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          detail="Database error")

    await EmailService.order_placement_message(current_user.email)
    return order_items

  @staticmethod
  async def get_order_item_by_id(db: AsyncSession, order_item_id: int, current_user):
    query = select(OrderItem).where(OrderItem.id == order_item_id)
    result = await db.execute(query)
    order_item = result.scalars().first()

    if not order_item:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Order item not found.")

    query = select(Order).where(Order.id == order_item.order_id)
    result = await db.execute(query)
    order = result.scalars().first()

    admin = current_user.role == Role.admin

    if order.user_id == current_user.id or admin:
      return order_item

    else:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this order item.")