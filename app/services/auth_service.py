from random import randint
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends, Response, status

from app.models import User
from app.database.session import get_db
from app.config.settings import settings
from app.services.email_service import EmailService
from app.schemas.user import UserCreate, UserResponse
from app.database.redis_session import redis_connection
from app.utils.hashing import hash_password, verify_password
from app.utils.token import create_access_token, create_refresh_token


SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM

class AuthService:
  @staticmethod
  async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user_result_email = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user_email = existing_user_result_email.scalar_one_or_none()
    existing_user_result_phone_number = await db.execute(
      select(User).filter(User.phone_number == user_data.phone_number))
    existing_user_phone_number = existing_user_result_phone_number.scalar_one_or_none()
    existing_user_result_username = await db.execute(select(User).filter(User.username == user_data.username))
    existing_user_username = existing_user_result_username.scalar_one_or_none()

    if existing_user_email:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email is already registered",
      )
    if existing_user_phone_number:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Phone number is already registered",
      )

    if existing_user_username:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username is already registered",
      )

    hashed_password = hash_password(user_data.password)
    user_data = {**user_data.model_dump(), "password": hashed_password, "created_at": datetime.now()}

    new_user = User(**user_data)
    await EmailService.send_verification_email(new_user.email)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserResponse.model_validate(new_user)

  @staticmethod
  async def login_user(email: str, password: str, response: Response,db: AsyncSession):
      user_query = await db.execute(select(User).where(User.email == email))
      user = user_query.scalar_one_or_none()
 
      if not user:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid email or password"
        )

      if not verify_password(password, user.password):
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid email or password"
        )

      if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")

      if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

      token_data = {"role": user.role}
      access_token = create_access_token(token_data, user_id=user.id)
      response.set_cookie(key="access_token", value=access_token, httponly=True)
      refresh_token = create_refresh_token(token_data, user_id=user.id)
      unique_id = hex(randint(0,255))
      response.set_cookie(key="refresh_token", value=unique_id, httponly=True)
      await redis_connection.set(unique_id, refresh_token)

      return {
        "user": UserResponse.model_validate(user)
      }
  
  @staticmethod
  async def logout_user(request,response):
    for cookie in request.cookies:
      response.delete_cookie(cookie)
    return {"message": "Successfully logged out"}
