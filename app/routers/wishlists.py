from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models import User
from app.responses.whishlist_response import (wishlist_post_response,
                                              delete_wishlist_response,
                                              delete_all_wishlists_response)
from app.schemas.wishlist import WishlistCreate, WishlistFilter
from app.services.wishlist_service import WishlistService
from app.utils.token import get_current_user


router = APIRouter(prefix="/wishlists", tags=["Wishlists"])


@router.get("/")
async def get_all_filtered_wishlists(
        filters: WishlistFilter = Depends(),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
  try:
    wishlists = await WishlistService.get_all_wishlists(db, filters, current_user)
    if not wishlists:
      return JSONResponse(content={"message": "No products found in your wishlist."},
                          status_code=status.HTTP_400_BAD_REQUEST)
    return wishlists
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/{product_id}")
async def get_wishlist_by_id(
        product_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
  try:
    wishlist_product = await WishlistService.get_wishlisht_by_id(product_id, current_user, db)
    return wishlist_product
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/", responses=wishlist_post_response)
async def create_wishlist(
        wishlist_data: WishlistCreate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)):
  try:
    new_wishlist = await WishlistService.create_wishlist(wishlist_data, db, current_user)
    return new_wishlist
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.delete("/{product_id}", responses=delete_wishlist_response)
async def delete_wishlist(
        product_id: int,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)):
  try:
    await WishlistService.delete_wishlist(product_id, current_user, db)
    return JSONResponse(content={"Detail": "Wishlist is successfully deleted"})
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.delete("/", responses=delete_all_wishlists_response)
async def delete_all_wishlist(
        db: AsyncSession = Depends(get_db),
        current_user=Depends(get_current_user)):
  try:
    message = await WishlistService.delete_all_wishlists(current_user, db)
    return JSONResponse(content=message)
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)