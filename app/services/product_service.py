from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import Role
from app.models.product import Product
from app.utils.token import get_client_ip
from app.database.redis_session import redis_connection
from app.utils.pagination import apply_filters, apply_pagination
from app.schemas.product import ProductCreate, ProductUpdate, ProductFilter, ProductResponse


class ProductService:
  @staticmethod
  async def get_all_products(db: AsyncSession, filters: ProductFilter):
    query = await apply_filters(db, filters)
    products = await apply_pagination(query, filters, db)
    if not products:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return products

  @staticmethod
  async def create_product(db: AsyncSession, product_data: ProductCreate,
                           current_user):
    if current_user.role.lower() not in (Role.admin, Role.vendor):
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to create a product.")
    product_dict = product_data.model_dump()
    product_dict["vendor_id"] = current_user.id
    if product_dict["stock"] == 0:
      product_dict["is_active"] = False
    if product_dict["stock"] > 0:
      product_dict["is_active"] = True
    product_db = Product(**product_dict)

    db.add(product_db)
    await db.commit()
    await db.refresh(product_db)

    return ProductResponse.model_validate(product_db)

  @staticmethod
  async def get_product_by_id(request, db: AsyncSession, product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalars().first()

    if not product:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found.")

    client_ip = get_client_ip(request)
    view_state = await redis_connection.get(client_ip)

    if view_state is None:
      await redis_connection.set(client_ip, 1)
      product.view_count += 1
      await db.commit()
      await db.refresh(product)

    return product

  @staticmethod
  async def update_product(
          request, db: AsyncSession,
          product_id: int,
          product_data: ProductUpdate,
          current_user):

    product = await ProductService.get_product_by_id(request, db, product_id)
    if not product:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found.")

    if current_user.role.lower() not in ("admin", "vendor") or (
            current_user.role.lower() == "vendor" and product.vendor_id != current_user.id):

      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to update this product.")

    updated_data = product_data.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
      setattr(product, key, value)

    if product.stock > 0:
      product.is_active = True
    elif product.stock == 0:
      product.is_active = False

    await db.commit()
    await db.refresh(product)
    return product

  @staticmethod
  async def delete_product(
          request,
          db: AsyncSession,
          product_id: int,
          current_user):

    product = await ProductService.get_product_by_id(request, db, product_id)

    if not product:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found.")

    if current_user.role.lower() not in ("admin", "vendor") \
            or (current_user.role.lower() == "vendor"
                and product.vendor_id != current_user.id):

      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to delete this product.")

    product.is_active = False
    product.stock = 0

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return {"detail": "Product deleted successfully."}