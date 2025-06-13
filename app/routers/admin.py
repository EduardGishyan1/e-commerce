from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.responses.admin_responses import (for_user, for_order, for_sales,
                                           for_review, for_analytics)
from app.schemas.user import UserCreate, UserResponse
from app.services.admin_service import AdminService
from app.utils.token import get_current_admin


router = APIRouter(prefix="/admin", tags=['Admin'])

@router.get("/all-reviews", responses=for_review)
async def get_all_reviews(
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_admin)):
  try:
    all_reviews = await AdminService.all_reviews(db)
    return all_reviews
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/all-orders", status_code=status.HTTP_200_OK, responses=for_order)
async def get_all_orders(
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_admin)):
  try:
    result = await AdminService.get_all_orders(db)
    return result
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/sales-statistics", responses=for_sales, status_code=status.HTTP_200_OK)
async def get_sales_statistics(
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_admin)):
  try:
    statistics = await AdminService.get_sales_statistics(db)
    return statistics
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/analytics", responses=for_analytics)
async def get_analytics(
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_admin)):
  try:
    analytics = await AdminService.generate_analytics(db)
    return analytics
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/users", response_model=UserResponse, responses=for_user)
async def create_user(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_db),
        admin: User = Depends(get_current_admin)):
  try:
    if admin:
      users = await AdminService.create_user_in_db(user_data, db)
      return users
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": status.HTTP_403_FORBIDDEN})
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/users", response_model=List[UserResponse], responses=for_user)
async def get_all_users(
        is_admin: User = Depends(get_current_admin),
        db: AsyncSession = Depends(get_db)):
  try:
    if is_admin:
      users = await AdminService.get_all_users_db(db)
      return users
  except HTTPException as exc:
    return JSONResponse(content=str(exc), status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)