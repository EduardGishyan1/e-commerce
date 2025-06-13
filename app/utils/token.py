from datetime import datetime, timezone, timedelta

from fastapi import Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.database.redis_session import redis_connection
from app.database.session import get_db
from app.models import User
from app.schemas.user import Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


def create_access_token(token_data: dict, user_id: int):
  expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  data = token_data.copy()
  data.update({"exp": expires, "sub": str(user_id)})
  auth_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

  return auth_token

def create_refresh_token(user: dict, user_id: int):
  expires = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
  data = user.copy()
  data.update({"exp": expires, "sub": str(user_id)})
  refresh_auth_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

  return refresh_auth_token

async def verify_access_token(
        request: Request,
        response: Response,
        token: str,
        db: AsyncSession):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

  except ExpiredSignatureError:
    token_code = request.cookies.get("refresh_token")
    refresh_token = await redis_connection.get(str(token_code))
    payload = await decode_refresh_token(refresh_token)
    user_id = int(payload.get("sub"))
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()
    token_data = {"role": user.role}
    new_token = create_access_token(token_data, user.id)
    response.set_cookie("access_token", new_token)

    return payload

  except Exception:
    return

async def get_current_user(
        request: Request,
        response: Response,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)):
  try:
    payload = await verify_access_token(request, response, token, db)
    user_id = int(payload.get("sub"))
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()

    return user

  except Exception:
    raise HTTPException(detail="Invalid token", status_code=status.HTTP_400_BAD_REQUEST)

async def decode_refresh_token(token):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
  except Exception:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid token")

async def get_current_admin(
        request: Request,
        response: Response,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)):

  payload = await verify_access_token(request, response, token, db)
  role = payload.get("role")

  if role != Role.admin:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="You don't have permission to do this action")

  return True

def get_client_ip(request: Request):
  x_forwarded_for = request.headers.get("X-Forwarded-For")

  if x_forwarded_for:
    client_ip = x_forwarded_for.split(",")[0]
  else:
    client_ip = request.client.host

  return client_ip