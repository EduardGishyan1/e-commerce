from sqlalchemy.future import select
from fastapi  import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.models.cart_item import CartItem
from app.schemas.cart_item import CartItemCreate, CartItemResponse


class CartService:
  @staticmethod
  async def create_cart_item(
          cart_item_data: CartItemCreate,
          db: AsyncSession, current_user):

    product_price = await db.execute(select(Product.price).where(Product.id == cart_item_data.product_id))
    product_price = product_price.scalar()
    
    cart_item_dict = cart_item_data.model_dump()

    cart_item_dict['user_id'] = current_user.id
    cart_item_dict['price'] = product_price
    cart_item = CartItem(**cart_item_dict)

    product_query = select(Product).where(Product.id == cart_item_data.product_id)
    product_result = await db.execute(product_query)
    product_item = product_result.scalars().first()

    if not product_item or product_item.is_active == False:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail='Product not found')

    if product_item.stock < cart_item_data.quantity:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail=f'Product stock exceeded. Available stock: {product_item.stock}')

    cart_item.price = product_item.price * cart_item.quantity

    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)
    return CartItemResponse.model_validate(cart_item)

  @staticmethod
  async def get_cart_items(db: AsyncSession, current_user):
    cart_query = select(CartItem).where(CartItem.user_id == current_user.id)
    cart_items_result = await db.execute(cart_query)
    cart_items = cart_items_result.scalars().all()

    return cart_items

  @staticmethod
  async def get_cart_item_by_id(cart_item_id: int, db: AsyncSession, current_user):
    cart_item_query = select(CartItem).where(CartItem.id == cart_item_id)
    cart_item_result = await db.execute(cart_item_query)
    cart_item = cart_item_result.scalar_one_or_none()

    if not cart_item:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cart Item not found')

    if not cart_item.user_id == current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return cart_item

  @staticmethod
  async def update_cart_item(cart_item_id: int, cart_item, db: AsyncSession, current_user):
    cart_item_result = await CartService.get_cart_item_by_id(cart_item_id, db, current_user)
    if not cart_item_result:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cart Item not found')

    product_result = await db.execute(select(Product).where(Product.id == cart_item_result.product_id))
    product = product_result.scalar_one_or_none()
    if cart_item.quantity > product.stock:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail=f"Product stock exceeded. Available stock: {product.stock}")
    cart_item_result.quantity = cart_item.quantity

    cart_item_result.price = product.price * cart_item_result.quantity

    db.add(cart_item_result)
    await db.commit()
    await db.refresh(cart_item_result)
    return cart_item_result

  @staticmethod
  async def delete_cart_item(cart_item_id: int, db: AsyncSession, current_user):
    cart_item_query = select(CartItem).where(CartItem.id == cart_item_id)
    cart_item_result = await db.execute(cart_item_query)
    cart_item = cart_item_result.scalar_one_or_none()

    if not cart_item:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Cart Item not found')

    if not cart_item.user_id == current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    await db.delete(cart_item)
    await db.commit()
    return {"message": "Cart item deleted successfully"}