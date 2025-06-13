from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Request

from app.models import User
from app.database.session import get_db
from app.utils.token import get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserUpdate
from app.responses.user_responses import user_responses


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}", response_model=UserResponse, responses=user_responses)
async def get_user_by_id(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
  try:
    users = await UserService.get_user_by_id_in_db(user_id, db, current_user)
    return users
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.put("/{user_id}", response_model=UserResponse, responses=user_responses)
async def update_user(
        request: Request,
        user_id: int,
        user_data: UserUpdate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
  try:
    users = await UserService.update_user_in_db(request, user_id, current_user, user_data, db)
    return users
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.delete("/{user_id}", responses=user_responses)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
  try:
    users = await UserService.delete_user_in_db(user_id, current_user, db)
    return users
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)