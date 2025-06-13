from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistCreate, WishlistFilter
from app.utils.pagination import apply_wishlist_filters, apply_wishlist_pagination


class WishlistService:

  @staticmethod
  async def get_all_wishlists(
          db: AsyncSession,
          filters: WishlistFilter,
          current_user):

    query = await apply_wishlist_filters(filters, current_user)
    wishlists = await apply_wishlist_pagination(query, filters, db)

    return wishlists

  @staticmethod
  async def get_wishlisht_by_id(product_id: int, current_user, db: AsyncSession):
    query = await db.execute(select(Wishlist)
                             .where(Wishlist.product_id == product_id)
                             .filter(Wishlist.user_id == current_user.id))
    wishlist = query.scalar_one_or_none()

    if not wishlist:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"Wishlist not found with ID {product_id}")

    return wishlist

  @staticmethod
  async def create_wishlist(
          wishlist_data: WishlistCreate,
          db: AsyncSession,
          current_user):

    user_id = current_user.id
    existing_product_id_wishlist = await db.execute(
      select(Wishlist).where(Wishlist.product_id == wishlist_data.product_id,
                             Wishlist.user_id == user_id))
    wishlist = existing_product_id_wishlist.scalars().all()

    product = await db.execute(select(Product).where(Product.id == wishlist_data.product_id))
    product = product.scalar_one_or_none()

    if not product:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found .")

    if wishlist:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists")

    new_wishlist_dict = wishlist_data.model_dump()
    new_wishlist_dict["user_id"] = user_id
    new_wishlist_dict["description"] = product.description
    new_wishlist = Wishlist(**new_wishlist_dict)

    db.add(new_wishlist)
    await db.commit()
    await db.refresh(new_wishlist)

    return new_wishlist

  @staticmethod
  async def delete_wishlist(product_id: int, current_user, db: AsyncSession):
    wishlist_query = await db.execute(select(Wishlist).where(Wishlist.product_id == product_id))
    wishlist_result = wishlist_query.scalar_one_or_none()

    if not wishlist_result:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wishlist's item not found with ID {product_id}.")

    if wishlist_result.user_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    await db.delete(wishlist_result)
    await db.commit()

  @staticmethod
  async def delete_all_wishlists(current_user, db: AsyncSession):
    wishlist_items = await db.execute(select(Wishlist).where(Wishlist.user_id == current_user.id))
    wishlist_items = wishlist_items.scalars().all()

    if not wishlist_items:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No wishlists found")

    for wishlist in wishlist_items:
      await db.delete(wishlist)
    await db.commit()

    return {"message": "All Wishlists deleted"}