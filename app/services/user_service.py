from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends

from app.models import User
from app.utils.token import get_current_user
from app.services.email_service import EmailService
from app.schemas.user import UserUpdate, UserResponse, Role


class UserService:
  @staticmethod
  async def get_user_by_id_in_db(
          user_id: int,
          db: AsyncSession,
          current_user: User = Depends(get_current_user)):

    query = await db.execute(select(User).filter(User.id == user_id))
    user = query.scalars().first()

    if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.id != current_user.id and not current_user.role == Role.admin:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return UserResponse.model_validate(user)

  @staticmethod
  async def update_user_in_db(
          user_id: int,
          current_user: User,
          user_data: UserUpdate,
          db: AsyncSession):

    if user_data.email is not None:
      existing_user_result_email = await db.execute(select(User).filter(User.email == user_data.email))
      existing_user_email = existing_user_result_email.scalar_one_or_none()

      if existing_user_email:
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Email is already registered")

    if user_data.phone_number is not None:
      existing_user_result_phone_number = await db.execute(
        select(User).filter(User.phone_number == user_data.phone_number))
      existing_user_phone_number = existing_user_result_phone_number.scalar_one_or_none()

      if existing_user_phone_number:
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Phone number is already registered")

    if user_data.username is not None:
      existing_user_result_username = await db.execute(select(User).filter(User.username == user_data.username))
      existing_user_username = existing_user_result_username.scalar_one_or_none()

      if existing_user_username:
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Username is already registered")

    if current_user.role != Role.admin and current_user.id != user_id:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to update this user's data")

    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalars().first()

    if not user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found")

    if user_data.email and user_data.email != user.email:
      user.is_verified = False
      await EmailService.send_verification_email(user_data.email)

    updated_data = user_data.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
      setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return UserResponse.model_validate(user)

  @staticmethod
  async def delete_user_in_db(
          user_id: int,
          current_user: User,
          db: AsyncSession):

    if current_user.role != Role.admin and current_user.id != user_id:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to delete this user")

    query = await db.execute(select(User).filter(User.id == user_id))
    user = query.scalars().first()

    if not user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found")

    user.is_active = False
    await db.commit()
    await db.refresh(user)

    return {"message": "User deleted successfully"}