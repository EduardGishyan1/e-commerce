from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from app.database.session import get_db
from app.utils.token import get_current_user
from app.services.review_service import ReviewService
from app.schemas.review import ReviewCreate, LikeDislike
from app.responses.reviews_response import (review_post_response,
                                            review_put_response,
                                            review_delete_response)


router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("/me")
async def get_all_reviews(
        db:AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)):
  try:
    reviews = await ReviewService.get_my_reviews(db, current_user)
    return {"reviews": reviews}
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/{product_id}")
async def get_review_by_product_id(
        product_id:int,
        db:AsyncSession = Depends(get_db)):
  try:
    review = await ReviewService.get_review_by_id(product_id, db)
    return {"review": review}
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/", responses=review_post_response)
async def create_review(
        review:ReviewCreate,
        db:AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)):
  try:
    review_result = await ReviewService.create_review(review, db,current_user)
    return {"review": review_result}
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.put("/{review_id}", responses=review_put_response)
async def update_review(
        review_id:int,
        review:ReviewCreate,
        db:AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)):
  try:
    review_result = await ReviewService.update_review(review_id, review, db, current_user)
    return {"review": review_result}
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.delete("/{review_id}", responses=review_delete_response)
async def delete_review(
        review_id:int,
        db:AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)):
  try:
    await ReviewService.delete_review(review_id, db, current_user)
    return JSONResponse({"message": f"Review #{review_id} deleted"})
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.post('/reactions')
async def like_dislike(
        reaction: LikeDislike,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)):
  try:
    reviews = await ReviewService.like_dislike(reaction, db, current_user)
    return {"reviews": reviews}
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)