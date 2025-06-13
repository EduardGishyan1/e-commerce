from fastapi import status, HTTPException
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.order import Order
from app.models.review import Review
from app.models.product import Product
from app.utils.hashing import pwd_context
from app.models.order_item import OrderItem
from app.schemas.user import UserResponse, UserCreate
from app.services.email_service import EmailService

class AdminService:
  @staticmethod
  async def get_all_users_db(
          db: AsyncSession):

    query = await db.execute(select(User))
    users = query.scalars().all()

    if not users:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")

    return [UserResponse.model_validate(user) for user in users]

  @staticmethod
  async def create_user_in_db(
          user_data: UserCreate,
          db: AsyncSession,
  ):

    existing_user_query = await db.execute(select(User).where(User.email == user_data.email))

    if existing_user_query.scalar_one_or_none():
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User with this email already exists")

    hashed_password = pwd_context.hash(user_data.password)
    new_user_data = user_data.model_dump(exclude={"password", "sensitive_info"})
    if user_data.sensitive_info:
      sensitive_info_data = user_data.sensitive_info
      new_user = User(**new_user_data, password=hashed_password, sensitive_info=sensitive_info_data)
    else:
      new_user = User(**new_user_data, password=hashed_password, sensitive_info=None)

    await EmailService.send_verification_email(new_user.email)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserResponse.model_validate(new_user)

  @staticmethod
  async def all_reviews(db: AsyncSession):
    all_reviews = await db.execute(select(Review))
    return all_reviews.scalars().all()

  @staticmethod
  async def get_all_orders(db: AsyncSession):
    orders = await db.execute(select(Order))
    return orders.scalars().all()

  @staticmethod
  async def get_sales_statistics(db: AsyncSession):
    total_revenue = await db.execute(select(func.sum(Order.total_amount)))
    total_revenue = total_revenue.scalar() or 0
    total_sales = await db.execute(select(func.count(Order.id)))
    total_sales = total_sales.scalar() or 0
    top_selling_products = await db.execute(
      select(OrderItem.product_id, func.sum(OrderItem.quantity).label('sales_count'))
      .group_by(OrderItem.product_id)
      .order_by(func.sum(OrderItem.quantity).desc())
      .limit(5))
    top_selling_products = top_selling_products.all()
    return {
      "total_revenue": total_revenue,
      "total_sales": total_sales,
      "top_selling_products":
        [{"product_id": product[0], "sales_count": product[1]} for product in top_selling_products]}

  @staticmethod
  async def generate_analytics(db: AsyncSession):

    most_active_user_query = (
      select(
        User.username,
        User.name,
        User.surname,
        User.email,
        func.count(Order.id).label('order_count')
      )
      .join(Order, Order.user_id == User.id)
      .group_by(
        User.username,
        User.name,
        User.surname,
        User.email
      )
      .order_by(func.count(Order.id).desc()))
    most_active_user_result = await db.execute(most_active_user_query)
    most_active_user = most_active_user_result.mappings().first()

    most_viewed_product_query = (
      select(Product)
      .order_by(Product.view_count.desc())
    )
    most_viewed_product_result = await db.execute(most_viewed_product_query)
    most_viewed_product = most_viewed_product_result.scalars().first()

    return {
      'most_active_user': most_active_user,
      'most_viewed_product': most_viewed_product
    }
