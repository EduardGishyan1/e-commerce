import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import PasswordInitiate, ChangePassword, UserBase, SetNewPassword
from app.services.email_service import EmailService
from app.utils.hashing import verify_password, hash_password


class InitPasswordRecovery:
  @staticmethod
  async def initiate_password_recovery(
          user: PasswordInitiate,
          db: AsyncSession):
    stmt = select(User).filter(User.email == user.email)
    result = await db.execute(stmt)
    existing_user_db = result.scalars().first()

    if not existing_user_db:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    user_pydantic = UserBase.model_validate(existing_user_db)
    await EmailService.password_recovery_email(user_pydantic.email)
    return {"message": "Check your email"}

  @staticmethod
  async def do_password_recovery(userinfo: SetNewPassword, db: AsyncSession):
    stmt = select(User).filter(User.email == userinfo.email)
    result = await db.execute(stmt)
    existing_user_db = result.scalars().first()

    if not existing_user_db:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if userinfo.new_password != userinfo.repeat_password:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't match")

    new_hashed_password = hash_password(userinfo.new_password)
    existing_user_db.password = new_hashed_password
    existing_user_db.updated_at = datetime.datetime.now()

    await EmailService.verify_email(userinfo.token, db)

    db.add(existing_user_db)
    await db.commit()
    await db.refresh(existing_user_db)

    await EmailService.change_password_message(userinfo.email)

    return {"message": "Changed password successfully"}

  @staticmethod
  async def change_password(
          userinfo: ChangePassword,
          current_user, db: AsyncSession):
    email = select(User).filter(User.email == current_user.email)
    result = await db.execute(email)
    existing_user_db = result.scalars().first()

    if not existing_user_db:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not verify_password(userinfo.password, existing_user_db.password):
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    new_hashed_password = hash_password(userinfo.new_password)
    existing_user_db.password = new_hashed_password
    existing_user_db.updated_at = datetime.datetime.now()

    db.add(existing_user_db)
    await db.commit()
    await db.refresh(existing_user_db)
    await EmailService.change_password_message(current_user.email)

    return {"message": "Password recovery successful"}