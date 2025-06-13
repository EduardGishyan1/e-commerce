from typing import List

from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status, Depends

from app.database.session import get_db
from app.utils.token import get_current_user
from app.services.cart_item_service import CartService
from app.schemas.cart_item import CartItemCreate, CartItemUpdate, CartItemResponse
from app.responses.cart_item_response import cart_item_post_response, delete_response


router = APIRouter(prefix='/cart_items', tags=['Cart Items'])

@router.post('/', response_model=CartItemResponse, responses=cart_item_post_response)
async def create_cart_item(
  cart_item_data: CartItemCreate,
  db: AsyncSession = Depends(get_db),
  current_user=Depends(get_current_user)):
  try:
    if not cart_item_data:
      return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'Invalid input data'})
    new_cart_item = await CartService.create_cart_item(cart_item_data, db, current_user)
    return new_cart_item
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get('/', response_model=List[CartItemResponse])
async def get_cart_items(
  db: AsyncSession=Depends(get_db),
  current_user=Depends(get_current_user)):
  try:
    cart_items = await CartService.get_cart_items(db, current_user)
    return cart_items
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get('/{cart_item_id}', response_model=CartItemResponse)
async def get_cart_item_by_id(
  cart_item_id: int, 
  db: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user)):
  try:
    cart_item = await CartService.get_cart_item_by_id(cart_item_id, db, current_user)
    return cart_item
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.patch('/{cart_item_id}')
async def update_cart_item(
    cart_item_id: int,
    cart_item: CartItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)):
  try:
    update_cart = await CartService.update_cart_item(cart_item_id, cart_item, db, current_user)
    return update_cart
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)


@router.delete('/{cart_item_id}', responses=delete_response)
async def delete_cart_item_by_id(
  cart_item_id: int,
  db: AsyncSession = Depends(get_db),
  current_user = Depends(get_current_user)):
  try:
    result = await CartService.delete_cart_item(cart_item_id, db, current_user)
    return result
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)