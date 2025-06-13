from sqlalchemy import and_
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wishlist import Wishlist
from app.schemas.product import ProductFilter
from app.schemas.wishlist import WishlistFilter
from app.models.product import Product, CategoryEnum


async def apply_filters(db: AsyncSession, filters: ProductFilter):
  if (filters.min_price and filters.max_price) and (filters.min_price > filters.max_price):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="min_price cannot be greater than max_price.")

  categories_query = select(Product.category).distinct()
  await db.execute(categories_query)
  valid_categories = set(CategoryEnum.__members__)

  if filters.category and filters.category not in valid_categories:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=f"Invalid category: {filters.category}. "
             f"Valid categories are: {', '.join(valid_categories)}.")

  conditions = []

  if filters.availability:
    conditions.append(Product.is_active == filters.availability)

  if filters.category:
    conditions.append(Product.category == filters.category)

  if filters.min_price:
    conditions.append(Product.price >= filters.min_price)

  if filters.max_price:
    conditions.append(Product.price <= filters.max_price)

  query = select(Product).where(and_(*conditions))

  return query

async def apply_pagination(query, filters: ProductFilter, db: AsyncSession):
  if filters.page < 1 or filters.size < 1 or filters.size > 100:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid pagination parameters. Page must be >= 1 and size must be between 1 and 100.")

  offset = (filters.page - 1) * filters.size
  paginated_query = query.offset(offset).limit(filters.size)
  result = await db.execute(paginated_query)
  items = result.scalars().all()

  return items

async def apply_wishlist_filters(filters: WishlistFilter, current_user):
  if (filters.min_price and filters.max_price) and (filters.min_price > filters.max_price):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="min price cannot be greater than max price.")

  conditions = [Wishlist.user_id == current_user.id]

  if filters.availability:
    conditions.append(Product.is_active == filters.availability)

  if filters.category:
    conditions.append(Product.category == filters.category)

  if filters.min_price:
    conditions.append(Product.price >= filters.min_price)

  if filters.max_price:
    conditions.append(Product.price <= filters.max_price)

  query = (select(Product)
           .join(Wishlist, Wishlist.product_id == Product.id)
           .where(and_(*conditions)))

  return query

async def apply_wishlist_pagination(query, filters: WishlistFilter, db: AsyncSession):
  if filters.page < 1 or filters.size < 1 or filters.size > 100:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid pagination parameters. Page must be >= 1 and size must be between 1 and 100.")

  offset = (filters.page - 1) * filters.size
  paginated_query = query.offset(offset).limit(filters.size)
  result = await db.execute(paginated_query)
  items = result.scalars().all()

  return items