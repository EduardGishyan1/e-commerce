from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from app.database.session import get_db
from app.utils.token import get_current_user
from app.services.order_item_service import OrderItemService
from app.responses.order_item_response import order_item_responses


router =  APIRouter(prefix="/order_items", tags=['Order items'])

@router.post("/", responses=order_item_responses)
async def create_order_item(
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)):
  try:
    new_order_item = await OrderItemService.create_order_item(db, current_user)
    return new_order_item
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/{order_item_id}")
async def get_order_item_by_id(
        order_item_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)):
  try:
    order_item = await OrderItemService.get_order_item_by_id(db, order_item_id, current_user)
    return order_item
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)